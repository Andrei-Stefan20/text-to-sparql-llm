#!/usr/bin/env python3

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)


@dataclass
class GenerationResult:
    question_id: str
    question: str
    gold_query: str
    generated_query: str
    is_correct: bool
    timestamp: str


@dataclass
class DPOPair:
    prompt: str
    chosen: str
    rejected: str
    prompt_id: str


class QueryComparator:

    @staticmethod
    def normalize_query(query: str) -> str:
        query = query.strip()
        query = " ".join(query.split())
        return query.lower()

    @staticmethod
    def is_correct(generated: str, gold: str) -> bool:
        gen_norm = QueryComparator.normalize_query(generated)
        gold_norm = QueryComparator.normalize_query(gold)
        return gen_norm == gold_norm


class DataHandler:

    @staticmethod
    def load_jsonl(filepath: Path) -> List[Dict]:
        data = []
        with open(filepath, "r") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data

    @staticmethod
    def save_jsonl(data: List[Dict], filepath: Path) -> None:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")

    @staticmethod
    def save_json(data: Any, filepath: Path) -> None:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)


class InferenceEngine:

    def __init__(
        self,
        model_name: str,
        device: str = "auto",
        use_4bit: bool = False,
        use_8bit: bool = False,
    ):
        self.model_name = model_name
        logger.info(f"Loading model: {model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        quantization_config = None
        if use_4bit or use_8bit:
            from transformers import BitsAndBytesConfig

            if use_4bit:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,
                )
            else:
                quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map=device,
            torch_dtype=torch.float16 if (use_4bit or use_8bit) else torch.float32,
            trust_remote_code=True,
        )
        self.model.eval()
        logger.info(f"Model loaded")

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_new_tokens: int = 512,
    ) -> str:
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048
        )
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                temperature=temperature,
                top_p=top_p,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
            )

        generated_text = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1] :],
            skip_special_tokens=True,
        )
        return generated_text.strip()


def inference_stage(
    model_name: str,
    dataset: List[Dict],
    output_dir: Path,
    config: Dict = None,
) -> Tuple[List[GenerationResult], Path]:
    config = config or {}
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"\nSTAGE 1: INFERENCE\n")

    engine = InferenceEngine(
        model_name=model_name,
        use_4bit=config.get("use_4bit", False),
        use_8bit=config.get("use_8bit", False),
    )

    results = []
    for sample in tqdm(dataset, desc="Generating"):
        question_id = sample.get("id", f"q_{len(results)}")
        question = sample.get("question", "")
        gold_query = sample.get("gold_query", "")

        prompt = f"Question: {question}\nSPARQL:"

        try:
            generated = engine.generate(
                prompt=prompt,
                temperature=config.get("temperature", 0.7),
                max_new_tokens=config.get("max_new_tokens", 512),
            )
            is_correct = QueryComparator.is_correct(generated, gold_query)

            results.append(
                GenerationResult(
                    question_id=question_id,
                    question=question,
                    gold_query=gold_query,
                    generated_query=generated,
                    is_correct=is_correct,
                    timestamp=datetime.now().isoformat(),
                )
            )
        except Exception as e:
            logger.warning(f"Error on {question_id}: {e}")

    # Save results
    results_file = output_dir / "results.json"
    DataHandler.save_json([asdict(r) for r in results], results_file)

    correct = sum(1 for r in results if r.is_correct)
    logger.info(
        f"{len(results)} samples, {correct} correct ({100*correct/len(results):.1f}%)\n"
    )

    return results, results_file


def create_dpo_dataset(
    inference_results: List[GenerationResult],
    output_dir: Path,
) -> Tuple[List[DPOPair], Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"\nSTAGE 2: DPO DATASET\n")

    dpo_pairs = []
    for result in inference_results:
        if not result.is_correct:
            dpo_pairs.append(
                DPOPair(
                    prompt=f"Question: {result.question}\nSPARQL:",
                    chosen=result.gold_query,
                    rejected=result.generated_query,
                    prompt_id=result.question_id,
                )
            )

    dataset_file = output_dir / "dpo_pairs.json"
    DataHandler.save_json([asdict(p) for p in dpo_pairs], dataset_file)
    logger.info(
        f"Created {len(dpo_pairs)} pairs ({100*len(dpo_pairs)/len(inference_results):.1f}% error rate)\n"
    )

    return dpo_pairs, dataset_file


def finetune_model(
    dpo_pairs: List[DPOPair],
    model_name: str,
    output_dir: Path,
    config: Dict = None,
) -> Optional[Path]:
    config = config or {}
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"\nSTAGE 3: FINE-TUNING\n")

    if not dpo_pairs:
        logger.warning("No DPO pairs, skipping fine-tuning\n")
        return None

    try:
        from datasets import Dataset
        from transformers import TrainingArguments
        from trl import DPOTrainer

        dataset = Dataset.from_dict(
            {
                "prompt": [p.prompt for p in dpo_pairs],
                "chosen": [p.chosen for p in dpo_pairs],
                "rejected": [p.rejected for p in dpo_pairs],
            }
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        model_dir = output_dir / "model"
        model_dir.mkdir(exist_ok=True)

        training_args = TrainingArguments(
            output_dir=str(model_dir / "checkpoint"),
            num_train_epochs=config.get("num_epochs", 3),
            per_device_train_batch_size=config.get("batch_size", 4),
            learning_rate=config.get("learning_rate", 5e-5),
            logging_steps=10,
            save_strategy="epoch",
            bf16=True,
        )

        trainer = DPOTrainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            tokenizer=tokenizer,
            beta=config.get("beta", 0.1),
        )

        logger.info("Training...")
        trainer.train()

        model.save_pretrained(str(model_dir / "final"))
        tokenizer.save_pretrained(str(model_dir / "final"))
        logger.info(f"Model saved to {model_dir / 'final'}\n")
        return model_dir / "final"

    except ImportError:
        logger.error("Missing TRL, install: pip install trl\n")
        return None
    except Exception as e:
        logger.error(f"Fine-tuning failed: {e}\n")
        return None


def evaluate_model(
    model_name: str,
    dataset: List[Dict],
    output_dir: Path,
    config: Dict = None,
) -> Tuple[List[GenerationResult], Path]:
    config = config or {}
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"\nSTAGE 4: EVALUATION\n")

    engine = InferenceEngine(
        model_name=model_name,
        use_4bit=config.get("use_4bit", False),
    )

    results = []
    for sample in tqdm(dataset, desc="Evaluating"):
        question_id = sample.get("id", f"q_{len(results)}")
        question = sample.get("question", "")
        gold_query = sample.get("gold_query", "")
        prompt = f"Question: {question}\nSPARQL:"

        try:
            generated = engine.generate(
                prompt=prompt, temperature=0.3, max_new_tokens=512
            )
            is_correct = QueryComparator.is_correct(generated, gold_query)

            results.append(
                GenerationResult(
                    question_id=question_id,
                    question=question,
                    gold_query=gold_query,
                    generated_query=generated,
                    is_correct=is_correct,
                    timestamp=datetime.now().isoformat(),
                )
            )
        except Exception as e:
            logger.warning(f"Error on {question_id}: {e}")

    results_file = output_dir / "results.json"
    DataHandler.save_json([asdict(r) for r in results], results_file)

    correct = sum(1 for r in results if r.is_correct)
    accuracy = correct / len(results) if results else 0
    logger.info(f"Accuracy: {100*accuracy:.1f}%\n")

    return results, results_file


def compare_results(
    base_results: List[GenerationResult],
    ft_results: Optional[List[GenerationResult]],
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"\nSTAGE 5: COMPARISON\n")

    base_acc = sum(1 for r in base_results if r.is_correct) / len(base_results)

    comparison = {
        "base_accuracy": base_acc,
        "base_correct": sum(1 for r in base_results if r.is_correct),
        "base_total": len(base_results),
    }

    if ft_results:
        ft_acc = sum(1 for r in ft_results if r.is_correct) / len(ft_results)
        comparison["finetuned_accuracy"] = ft_acc
        comparison["finetuned_correct"] = sum(1 for r in ft_results if r.is_correct)
        comparison["improvement"] = ft_acc - base_acc

        logger.info(f"Base:       {100*base_acc:.1f}%")
        logger.info(f"Fine-tuned: {100*ft_acc:.1f}%")
        logger.info(f"Improvement: {100*(ft_acc-base_acc):+.1f}%\n")
    else:
        logger.info(f"Base accuracy: {100*base_acc:.1f}%\n")

    comp_file = output_dir / "comparison.json"
    DataHandler.save_json(comparison, comp_file)

    return comp_file


def run_pipeline(
    train_data: List[Dict],
    test_data: List[Dict],
    model_name: str,
    output_dir: Path,
    config: Dict = None,
    finetuned_model: Optional[Path] = None,
) -> Dict:
    config = config or {}
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"\nCOMPLETE FINE-TUNING PIPELINE\n")

    results_summary = {
        "start_time": datetime.now().isoformat(),
        "base_model": model_name,
    }

    try:
        base_results, _ = inference_stage(
            model_name=model_name,
            dataset=train_data,
            output_dir=output_dir / "1_inference",
            config=config.get("inference", {}),
        )

        dpo_pairs, _ = create_dpo_dataset(
            inference_results=base_results,
            output_dir=output_dir / "2_dpo_dataset",
        )

        ft_model_path = None
        if not finetuned_model:
            ft_model_path = finetune_model(
                dpo_pairs=dpo_pairs,
                model_name=model_name,
                output_dir=output_dir / "3_finetuning",
                config=config.get("finetuning", {}),
            )
        else:
            ft_model_path = finetuned_model

        test_base, _ = evaluate_model(
            model_name=model_name,
            dataset=test_data,
            output_dir=output_dir / "4_eval_base",
            config=config.get("evaluation", {}),
        )

        test_ft = None
        if ft_model_path:
            test_ft, _ = evaluate_model(
                model_name=str(ft_model_path),
                dataset=test_data,
                output_dir=output_dir / "4_eval_ft",
                config=config.get("evaluation", {}),
            )

        compare_results(
            base_results=test_base,
            ft_results=test_ft,
            output_dir=output_dir / "5_comparison",
        )

        results_summary["end_time"] = datetime.now().isoformat()
        results_summary["status"] = "completed"
        results_summary["finetuned_model"] = (
            str(ft_model_path) if ft_model_path else None
        )

        logger.info(f"\nPIPELINE COMPLETED")
        logger.info(f"Results: {output_dir}\n")

        DataHandler.save_json(results_summary, output_dir / "summary.json")
        return results_summary

    except Exception as e:
        logger.error(f"\nPipeline failed: {e}")
        results_summary["status"] = "failed"
        results_summary["error"] = str(e)
        DataHandler.save_json(results_summary, output_dir / "summary.json")
        raise

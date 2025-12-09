"""
Evaluation pipeline for local LLM models using HuggingFace Transformers.
Executes Text-to-SPARQL translation with few-shot learning and self-correction.
"""

import json
import sys
import traceback
import torch
from pathlib import Path
from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv

FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

from src.config import config
from src.exceptions import ModelError, DataError
from src.validators import validate_file_exists, validate_json_file
from src.logging_config import get_logger
from src.models.generator import build_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import ExampleRetriever
from src.evaluation.mlflow_reporter import MLflowReporter
from src.evaluation.metrics import (
    SPARQLSyntaxMetric,
    SPARQLExecutionMetric,
    SPARQLAnswerCorrectnessMetric,
    create_test_case
)
from src.utils.sparql_client import SPARQLClient
from src.pipeline_utils import timer

logger = get_logger(__name__)

class LocalQueryGenerator:
    """Wrapper for HuggingFace Transformers models with hardware optimization."""
    
    def __init__(self, model_id: str):
        """
        Initialize local LLM.
        
        Args:
            model_id: HuggingFace model identifier
        """
        self.model_id = model_id
        logger.info(f"Initializing Local Model: {model_id}")
        
        attn_impl = "eager"
        try:
            import flash_attn
            attn_impl = "flash_attention_2"
            logger.info("Optimization: Flash Attention 2 enabled.")
        except ImportError:
            attn_impl = "sdpa"
            logger.info("Optimization: Using SDPA (Flash Attention 2 not available).")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, 
                torch_dtype=torch.float16, 
                device_map="auto",
                attn_implementation=attn_impl
            )
            self.model.eval()
            
            if torch.cuda.is_available():
                logger.info("GPU available, optimizing model...")
                try:
                    self.model = torch.compile(self.model)
                    logger.info("Model compiled successfully.")
                except Exception as e:
                    logger.warning(f"Compilation failed (continuing): {e}")
            
        except Exception as e:
            raise ModelError(f"Failed to load model {model_id}: {e}") from e

    def generate_raw(self, prompt: str, stop: Optional[list] = None, max_new_tokens: int = 512) -> str:
        """
        Generates text completion from the model.
        
        Args:
            prompt: Input prompt
            stop: Stop sequences
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Generated text or empty string on error
        """
        if not prompt or not isinstance(prompt, str):
            return ""
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=config.model.temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1
                )
            
            full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract generated part
            if prompt in full_text:
                generated_text = full_text.split(prompt, 1)[-1]
            else:
                generated_text = full_text[len(prompt):]
            
            # Apply stop sequences
            if stop:
                for s in stop:
                    if s in generated_text:
                        generated_text = generated_text.split(s)[0]
            
            return generated_text.strip()
        
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return ""

def get_model_id() -> str:
    """Get the default local model ID."""
    return "Qwen/Qwen2.5-Coder-3B-Instruct"

def main():
    """Main evaluation pipeline for local model."""
    logger.info(">>> STARTING LOCAL MODEL EVALUATION FEW-SHOT...")
    
    # Validate configuration
    try:
        config.validate()
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return

    model_id = get_model_id()
    
    # Initialize and validate data
    index_path = PROJECT_ROOT / "data/processed/train_index.faiss"
    meta_path = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    test_file = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"
    
    try:
        validate_file_exists(index_path, "FAISS index")
        validate_file_exists(meta_path, "Metadata file")
        validate_file_exists(test_file, "Test data")
        
        test_data = validate_json_file(test_file)
        if 'questions' not in test_data:
            raise DataError(f"Missing 'questions' key in {test_file}")
    
    except (FileNotFoundError, DataError) as e:
        logger.error(f"Data validation error: {e}")
        return

    # Initialize components
    try:
        with timer("Component initialization"):
            retriever = ExampleRetriever(index_path, meta_path)
            sparql_client = SPARQLClient(timeout=30)
            generator = LocalQueryGenerator(model_id)
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        return
    
    # Initialize MLflow reporter
    try:
        reporter = MLflowReporter(
            experiment_name=f"local-{model_id.split('/')[-1]}-evaluation",
            artifact_location=PROJECT_ROOT / "mlruns"
        )
        
        reporter.log_params({
            "model": model_id,
            "temperature": config.model.temperature,
            "max_retries": config.model.max_retries,
            "k_examples": config.retrieval.k_examples,
            "dataset": "QALD-10",
            "sample_size": 20
        })
    except Exception as e:
        logger.error(f"Failed to initialize MLflow: {e}")
        return
    
    # Initialize metrics
    syntax_metric = SPARQLSyntaxMetric()
    execution_metric = SPARQLExecutionMetric()
    answer_metric = SPARQLAnswerCorrectnessMetric(threshold=0.8)

    test_data = test_data['questions']
    SAMPLES = test_data[:20]
    total_q = len(SAMPLES)
    
    logger.info(f"Starting evaluation on {total_q} questions...")

    for i, q_obj in enumerate(SAMPLES):
        try:
            logger.info(f"Q{i+1}/{total_q}: ", end="")
            
            question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
            gold_sparql = q_obj['query'].get('sparql', '')
            
            if not question:
                logger.warning("No English question")
                continue
            
            # Execute gold query
            gold_results, gold_error = sparql_client.execute_remote(gold_sparql)
            if gold_error:
                logger.warning(f"Gold query failed: {gold_error}")
                gold_results = []

            # Prompt construction
            examples = retriever.retrieve(question, k=config.retrieval.k_examples)
            context = extract_gold_context(gold_sparql)
            prompt = build_prompt(question, examples, context)

            # Generation loop with self-correction
            MAX_RETRIES = config.model.max_retries
            best_result = None

            for attempt in range(1, MAX_RETRIES + 2):
                try:
                    raw_response = generator.generate_raw(prompt, stop=["User:", "```", "###", "Question:"])
                    gen_sparql = sparql_client.clean_query(raw_response)
                    
                    syntax_check = sparql_client.validate_syntax_local(gen_sparql)
                    results, exec_error = None, None
                    error_info = {}
                    
                    if syntax_check["valid"]:
                        results, exec_error = sparql_client.execute_remote(gen_sparql)
                        if exec_error:
                            syntax_check["valid"] = False
                            error_info = {"type": "Execution Error", "detail": exec_error}
                        else:
                            best_result = (gen_sparql, raw_response, True, {}, results, attempt)
                            break
                    else:
                        error_info = {"type": syntax_check["type"], "detail": syntax_check["detail"]}

                    # Self-correction prompt
                    if attempt <= MAX_RETRIES:
                        prompt += f"\n{gen_sparql}\n```\n\nSYSTEM: Invalid. {error_info.get('detail')}\nFix:\n```sparql"
                    else:
                        best_result = (gen_sparql, raw_response, False, error_info, None, attempt)
                
                except Exception as e:
                    logger.debug(f"Attempt {attempt} error: {str(e)[:50]}")
                    best_result = ("", "", False, {"type": type(e).__name__, "detail": str(e)[:80]}, None, attempt)
                    break

            if not best_result:
                logger.warning("No result generated")
                continue
            
            gen_sparql, raw_resp, is_valid, error_info, gen_results, attempts = best_result
            
            f1 = 0.0
            if is_valid and gen_results:
                f1 = sparql_client.calculate_f1(gold_results, gen_results)
                if f1 < 1.0 and not error_info:
                    error_info = {"type": "Wrong Answer", "detail": f"F1: {f1:.2f}"}
            
            logger.info(f"Valid: {is_valid}, F1: {f1:.2f}, Attempts: {attempts}")
            
            # DeepEval metrics
            test_case = create_test_case(question, gen_sparql, gold_sparql, examples)
            custom_metrics = {}
            
            try:
                custom_metrics = {
                    "syntax_validity": syntax_metric.measure(test_case),
                    "execution_success": execution_metric.measure(test_case),
                    "answer_correctness": answer_metric.measure(test_case)
                }
            except Exception as e:
                logger.debug(f"Metric error: {e}")
            
            # Log to MLflow
            reporter.log_question_result(
                question_id=i+1,
                question=question,
                gold_sparql=gold_sparql,
                generated_sparql=gen_sparql,
                is_valid=is_valid,
                f1_score=f1,
                attempts=attempts,
                error_info=error_info if error_info else None,
                metrics=custom_metrics
            )
            
        except Exception as e:
            logger.error(f"Error processing Q{i+1}: {e}")
            continue

    # Finalize
    try:
        summary = reporter.finalize()
        logger.info(f"Evaluation complete! {summary}")
        logger.info("View results: mlflow ui --port 5000")
    except Exception as e:
        logger.error(f"Failed to finalize: {e}")

if __name__ == "__main__":
    main()
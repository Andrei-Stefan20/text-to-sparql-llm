"""
Evaluate DPO fine-tuned model on SPARQL generation tasks.

This script:
1. Loads the fine-tuned model
2. Generates SPARQL from natural language questions
3. Compares with gold standard queries
4. Calculates evaluation metrics (BLEU, exact match, etc.)
5. Generates evaluation reports
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import logging
from collections import defaultdict

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SPARQLEvaluator:
    """Evaluate SPARQL generation quality."""
    
    def __init__(self, model_path: Path, device: str = "cuda"):
        """Initialize evaluator with fine-tuned model."""
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.model.eval()
        
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        logger.info(f"Loaded model from {model_path}")
    
    def generate_sparql(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_beams: int = 1,
    ) -> str:
        """Generate SPARQL query from natural language prompt."""
        
        # Format prompt
        formatted_prompt = f"{prompt}\n"
        
        # Tokenize
        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_beams=num_beams,
                do_sample=(num_beams == 1),
                pad_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract SPARQL (remove prompt)
        if formatted_prompt in generated_text:
            sparql = generated_text.split(formatted_prompt)[-1].strip()
        else:
            sparql = generated_text.strip()
        
        return sparql
    
    def calculate_bleu(self, reference: str, generated: str) -> float:
        """Calculate BLEU score."""
        ref_tokens = reference.split()
        gen_tokens = generated.split()
        
        smoothing = SmoothingFunction().method1
        bleu = sentence_bleu(
            [ref_tokens],
            gen_tokens,
            weights=(0.25, 0.25, 0.25, 0.25),
            smoothing_function=smoothing,
        )
        return bleu
    
    def calculate_rouge(self, reference: str, generated: str) -> Dict[str, float]:
        """Calculate ROUGE scores."""
        scores = self.rouge_scorer.score(reference, generated)
        return {
            'rouge1': scores['rouge1'].fmeasure,
            'rougeL': scores['rougeL'].fmeasure,
        }
    
    def exact_match(self, reference: str, generated: str) -> bool:
        """Check for exact match."""
        return reference.strip().lower() == generated.strip().lower()
    
    def calculate_keyword_overlap(self, reference: str, generated: str) -> float:
        """Calculate keyword overlap (for SPARQL-specific metrics)."""
        # Extract keywords from SPARQL
        keywords = {'SELECT', 'WHERE', 'FILTER', 'OPTIONAL', 'SERVICE', 'LIMIT', 'ORDER BY'}
        
        ref_keywords = set(keyword for keyword in keywords if keyword in reference.upper())
        gen_keywords = set(keyword for keyword in keywords if keyword in generated.upper())
        
        if not ref_keywords and not gen_keywords:
            return 1.0
        
        if not ref_keywords or not gen_keywords:
            return 0.0
        
        overlap = len(ref_keywords & gen_keywords) / len(ref_keywords | gen_keywords)
        return overlap
    
    def evaluate_pair(self, reference: str, generated: str) -> Dict:
        """Evaluate a single reference-generated pair."""
        
        return {
            'exact_match': self.exact_match(reference, generated),
            'bleu': self.calculate_bleu(reference, generated),
            'rouge': self.calculate_rouge(reference, generated),
            'keyword_overlap': self.calculate_keyword_overlap(reference, generated),
        }


def load_evaluation_data(filepath: Path) -> List[Dict]:
    """Load evaluation data."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def run_evaluation(
    model_path: Path,
    eval_data_path: Path,
    output_dir: Path,
    num_samples: int = None,
    device: str = "cuda",
):
    """Run evaluation on dataset."""
    
    # Initialize evaluator
    evaluator = SPARQLEvaluator(model_path, device=device)
    
    # Load evaluation data
    eval_data = load_evaluation_data(eval_data_path)
    if num_samples:
        eval_data = eval_data[:num_samples]
    
    logger.info(f"Evaluating on {len(eval_data)} examples")
    
    # Run evaluation
    results = []
    metrics_agg = defaultdict(list)
    
    for idx, example in enumerate(eval_data):
        if (idx + 1) % 10 == 0:
            logger.info(f"Processed {idx + 1}/{len(eval_data)} examples")
        
        # Generate SPARQL
        generated_sparql = evaluator.generate_sparql(example['prompt'])
        
        # Evaluate
        metrics = evaluator.evaluate_pair(
            example['chosen'],
            generated_sparql
        )
        
        results.append({
            'question_id': example.get('question_id'),
            'prompt': example['prompt'],
            'reference': example['chosen'],
            'generated': generated_sparql,
            'metrics': metrics,
        })
        
        # Aggregate metrics
        for key, value in metrics.items():
            if key != 'rouge':
                metrics_agg[key].append(value)
            else:
                for rouge_key, rouge_val in value.items():
                    metrics_agg[f'rouge_{rouge_key}'].append(rouge_val)
    
    # Calculate aggregate statistics
    aggregate_stats = {}
    for key, values in metrics_agg.items():
        aggregate_stats[key] = {
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
        }
    
    # Print results
    logger.info(f"\n{'='*80}")
    logger.info(f"EVALUATION RESULTS")
    logger.info(f"{'='*80}")
    
    logger.info(f"\nExact Match: {aggregate_stats['exact_match']['mean']:.4f}")
    logger.info(f"BLEU: {aggregate_stats['bleu']['mean']:.4f} (±{aggregate_stats['bleu']['std']:.4f})")
    logger.info(f"ROUGE-1: {aggregate_stats['rouge_rouge1']['mean']:.4f}")
    logger.info(f"ROUGE-L: {aggregate_stats['rouge_rougeL']['mean']:.4f}")
    logger.info(f"Keyword Overlap: {aggregate_stats['keyword_overlap']['mean']:.4f}")
    
    # Save results
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "evaluation_results.json", 'w') as f:
        json.dump({
            'aggregate_stats': aggregate_stats,
            'examples': results[:100],  # Save first 100 examples
        }, f, indent=2)
    
    # Save detailed results
    with open(output_dir / "detailed_results.jsonl", 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')
    
    logger.info(f"\nResults saved to {output_dir}")
    
    return aggregate_stats


def main():
    parser = argparse.ArgumentParser(description="Evaluate DPO fine-tuned model")
    parser.add_argument(
        "--model",
        type=Path,
        required=True,
        help="Path to fine-tuned model"
    )
    parser.add_argument(
        "--eval-data",
        type=Path,
        required=True,
        help="Path to evaluation data (JSONL)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("evaluation_results"),
        help="Output directory for results"
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=None,
        help="Number of samples to evaluate (default: all)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to use for inference"
    )
    
    args = parser.parse_args()
    
    try:
        stats = run_evaluation(
            args.model,
            args.eval_data,
            args.output_dir,
            args.num_samples,
            args.device,
        )
        return 0
    except Exception as e:
        logger.error(f"Evaluation failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())

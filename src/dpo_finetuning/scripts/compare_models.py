"""
Compare baseline model with DPO fine-tuned model.

This script:
1. Generates SPARQL using both baseline and fine-tuned models
2. Evaluates both using standard metrics
3. Compares results and generates comparative analysis
4. Identifies improvements and regressions
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import logging
from collections import defaultdict

import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelComparison:
    """Compare baseline and fine-tuned models."""
    
    def __init__(self, baseline_path: Path, finetuned_path: Path, device: str = "cuda"):
        """Initialize with both models."""
        
        self.device = device
        
        # Load baseline model
        logger.info(f"Loading baseline model from {baseline_path}")
        self.baseline_tokenizer = AutoTokenizer.from_pretrained(baseline_path)
        self.baseline_model = AutoModelForCausalLM.from_pretrained(
            baseline_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.baseline_model.eval()
        
        # Load fine-tuned model
        logger.info(f"Loading fine-tuned model from {finetuned_path}")
        self.finetuned_tokenizer = AutoTokenizer.from_pretrained(finetuned_path)
        self.finetuned_model = AutoModelForCausalLM.from_pretrained(
            finetuned_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.finetuned_model.eval()
        
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    
    def generate_sparql(
        self,
        model,
        tokenizer,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """Generate SPARQL from a model."""
        
        formatted_prompt = f"{prompt}\n"
        
        inputs = tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(self.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if formatted_prompt in generated_text:
            sparql = generated_text.split(formatted_prompt)[-1].strip()
        else:
            sparql = generated_text.strip()
        
        return sparql
    
    def calculate_metrics(self, reference: str, generated: str) -> Dict:
        """Calculate evaluation metrics."""
        
        # Exact match
        exact_match = reference.strip().lower() == generated.strip().lower()
        
        # BLEU
        ref_tokens = reference.split()
        gen_tokens = generated.split()
        smoothing = SmoothingFunction().method1
        bleu = sentence_bleu(
            [ref_tokens],
            gen_tokens,
            weights=(0.25, 0.25, 0.25, 0.25),
            smoothing_function=smoothing,
        )
        
        # ROUGE
        rouge_scores = self.rouge_scorer.score(reference, generated)
        
        # Keyword overlap
        keywords = {'SELECT', 'WHERE', 'FILTER', 'OPTIONAL', 'SERVICE', 'LIMIT', 'ORDER BY'}
        ref_keywords = set(k for k in keywords if k in reference.upper())
        gen_keywords = set(k for k in keywords if k in generated.upper())
        
        if ref_keywords or gen_keywords:
            keyword_overlap = len(ref_keywords & gen_keywords) / len(ref_keywords | gen_keywords)
        else:
            keyword_overlap = 1.0
        
        return {
            'exact_match': exact_match,
            'bleu': bleu,
            'rouge1': rouge_scores['rouge1'].fmeasure,
            'rougeL': rouge_scores['rougeL'].fmeasure,
            'keyword_overlap': keyword_overlap,
        }
    
    def compare_models(
        self,
        eval_data: List[Dict],
        output_dir: Path,
    ) -> Dict:
        """Compare models on evaluation data."""
        
        logger.info(f"Comparing models on {len(eval_data)} examples")
        
        results = []
        baseline_metrics_agg = defaultdict(list)
        finetuned_metrics_agg = defaultdict(list)
        improvements = defaultdict(int)
        
        for idx, example in enumerate(eval_data):
            if (idx + 1) % 10 == 0:
                logger.info(f"Processed {idx + 1}/{len(eval_data)} examples")
            
            # Generate with baseline
            baseline_sparql = self.generate_sparql(
                self.baseline_model,
                self.baseline_tokenizer,
                example['prompt']
            )
            
            # Generate with fine-tuned
            finetuned_sparql = self.generate_sparql(
                self.finetuned_model,
                self.finetuned_tokenizer,
                example['prompt']
            )
            
            # Calculate metrics
            baseline_metrics = self.calculate_metrics(example['chosen'], baseline_sparql)
            finetuned_metrics = self.calculate_metrics(example['chosen'], finetuned_sparql)
            
            # Aggregate
            for key in baseline_metrics:
                baseline_metrics_agg[key].append(baseline_metrics[key])
                finetuned_metrics_agg[key].append(finetuned_metrics[key])
                
                # Track improvements
                if finetuned_metrics[key] > baseline_metrics[key]:
                    improvements[f'{key}_improvement'] += 1
                elif finetuned_metrics[key] < baseline_metrics[key]:
                    improvements[f'{key}_regression'] += 1
            
            results.append({
                'question_id': example.get('question_id'),
                'prompt': example['prompt'],
                'reference': example['chosen'],
                'baseline_sparql': baseline_sparql,
                'finetuned_sparql': finetuned_sparql,
                'baseline_metrics': baseline_metrics,
                'finetuned_metrics': finetuned_metrics,
                'improvement': {
                    k: finetuned_metrics[k] - baseline_metrics[k]
                    for k in baseline_metrics
                }
            })
        
        # Calculate aggregate statistics
        aggregate_comparison = {}
        for metric in baseline_metrics_agg:
            baseline_values = baseline_metrics_agg[metric]
            finetuned_values = finetuned_metrics_agg[metric]
            
            aggregate_comparison[metric] = {
                'baseline': {
                    'mean': float(np.mean(baseline_values)),
                    'std': float(np.std(baseline_values)),
                },
                'finetuned': {
                    'mean': float(np.mean(finetuned_values)),
                    'std': float(np.std(finetuned_values)),
                },
                'improvement': float(np.mean(finetuned_values) - np.array(baseline_values)),
                'improvement_percent': float(
                    ((np.mean(finetuned_values) - np.mean(baseline_values)) / 
                     (np.mean(baseline_values) + 1e-6)) * 100
                ),
            }
        
        # Print comparison
        logger.info(f"\n{'='*100}")
        logger.info(f"COMPARATIVE ANALYSIS: Baseline vs DPO Fine-tuned")
        logger.info(f"{'='*100}\n")
        
        for metric, stats in aggregate_comparison.items():
            logger.info(f"{metric.upper()}")
            logger.info(f"  Baseline:   {stats['baseline']['mean']:.4f} ± {stats['baseline']['std']:.4f}")
            logger.info(f"  Fine-tuned: {stats['finetuned']['mean']:.4f} ± {stats['finetuned']['std']:.4f}")
            logger.info(f"  Improvement: {stats['improvement']:.4f} ({stats['improvement_percent']:+.2f}%)\n")
        
        logger.info(f"\nIMPROVEMENT SUMMARY:")
        logger.info(f"  Examples with improvement: {improvements.get('bleu_improvement', 0)}/{len(results)}")
        logger.info(f"  Examples with regression: {improvements.get('bleu_regression', 0)}/{len(results)}")
        
        # Save results
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / "comparison_results.json", 'w') as f:
            json.dump({
                'aggregate_comparison': aggregate_comparison,
                'improvement_summary': dict(improvements),
                'examples': results[:100],
            }, f, indent=2)
        
        with open(output_dir / "detailed_comparison.jsonl", 'w') as f:
            for result in results:
                f.write(json.dumps(result) + '\n')
        
        logger.info(f"\nResults saved to {output_dir}")
        
        return {
            'aggregate_comparison': aggregate_comparison,
            'improvement_summary': improvements,
            'num_examples': len(results),
        }


def load_evaluation_data(filepath: Path) -> List[Dict]:
    """Load evaluation data."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Compare baseline and DPO fine-tuned models"
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        required=True,
        help="Path to baseline model"
    )
    parser.add_argument(
        "--finetuned",
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
        default=Path("comparative_results"),
        help="Output directory for results"
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=None,
        help="Number of samples to evaluate"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to use for inference"
    )
    
    args = parser.parse_args()
    
    try:
        # Load evaluation data
        eval_data = load_evaluation_data(args.eval_data)
        if args.num_samples:
            eval_data = eval_data[:args.num_samples]
        
        # Initialize evaluator
        evaluator = ModelComparison(
            args.baseline,
            args.finetuned,
            device=args.device,
        )
        
        # Run comparison
        results = evaluator.compare_models(eval_data, args.output_dir)
        
        return 0
        
    except Exception as e:
        logger.error(f"Comparison failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())

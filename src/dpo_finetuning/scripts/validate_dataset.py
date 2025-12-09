"""
Validate and analyze prepared DPO datasets.

This script:
1. Checks dataset integrity
2. Detects duplicates and anomalies
3. Provides quality metrics
4. Identifies potential data issues
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Set
import logging
from collections import Counter
import statistics


def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def load_jsonl(filepath: Path) -> List[Dict]:
    """Load JSONL file."""
    data = []
    if not filepath.exists():
        return data
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    logging.warning(f"Failed to parse line: {e}")
    return data


def validate_dataset(dataset_path: Path) -> Dict:
    """
    Validate a DPO dataset file.
    
    Returns:
        Dictionary with validation results
    """
    pairs = load_jsonl(dataset_path)
    
    if not pairs:
        logging.error(f"No data found in {dataset_path}")
        return {}
    
    results = {
        "total_pairs": len(pairs),
        "valid_pairs": 0,
        "issues": []
    }
    
    # Track issues
    missing_fields = Counter()
    duplicate_pairs = set()
    duplicate_prompts = Counter()
    identical_pairs = 0
    
    seen_pairs = set()
    
    for i, pair in enumerate(pairs):
        is_valid = True
        
        # Check required fields
        required_fields = ['prompt', 'chosen', 'rejected', 'question_id']
        for field in required_fields:
            if field not in pair or not pair[field]:
                missing_fields[field] += 1
                is_valid = False
        
        if is_valid:
            # Check for identical chosen and rejected
            if pair['chosen'].strip() == pair['rejected'].strip():
                identical_pairs += 1
                is_valid = False
                results["issues"].append({
                    "index": i,
                    "type": "identical_chosen_rejected",
                    "question_id": pair.get('question_id')
                })
            
            # Check for duplicate prompts
            prompt_key = pair['prompt'].strip().lower()
            duplicate_prompts[prompt_key] += 1
            
            # Check for duplicate pairs
            pair_key = (pair['prompt'].strip(), pair['chosen'].strip(), pair['rejected'].strip())
            if pair_key in seen_pairs:
                duplicate_pairs.add(pair.get('question_id'))
                results["issues"].append({
                    "index": i,
                    "type": "duplicate_pair",
                    "question_id": pair.get('question_id')
                })
            else:
                seen_pairs.add(pair_key)
        
        if is_valid:
            results["valid_pairs"] += 1
    
    # Add issue summary
    if missing_fields:
        results["issues"].append({
            "type": "missing_fields",
            "summary": dict(missing_fields)
        })
    
    if identical_pairs > 0:
        results["issues"].append({
            "type": "identical_pairs_count",
            "count": identical_pairs
        })
    
    if duplicate_pairs:
        results["issues"].append({
            "type": "duplicate_pairs_count",
            "count": len(duplicate_pairs)
        })
    
    # Check for highly duplicated prompts
    high_dup_prompts = [(k, v) for k, v in duplicate_prompts.items() if v > 3]
    if high_dup_prompts:
        results["issues"].append({
            "type": "highly_duplicated_prompts",
            "count": len(high_dup_prompts),
            "max_count": max(v for k, v in high_dup_prompts)
        })
    
    results["quality_score"] = (results["valid_pairs"] / results["total_pairs"]) * 100
    
    return results


def compare_datasets(train_path: Path, val_path: Path) -> Dict:
    """Compare training and validation datasets for data leakage."""
    train_pairs = load_jsonl(train_path)
    val_pairs = load_jsonl(val_path)
    
    results = {
        "train_pairs": len(train_pairs),
        "val_pairs": len(val_pairs),
        "leakage": {
            "prompt_overlap": 0,
            "question_id_overlap": 0,
            "pair_overlap": 0
        }
    }
    
    train_prompts = {p['prompt'].strip().lower() for p in train_pairs if 'prompt' in p}
    val_prompts = {p['prompt'].strip().lower() for p in val_pairs if 'prompt' in p}
    results["leakage"]["prompt_overlap"] = len(train_prompts & val_prompts)
    
    train_ids = {p.get('question_id') for p in train_pairs if 'question_id' in p}
    val_ids = {p.get('question_id') for p in val_pairs if 'question_id' in p}
    results["leakage"]["question_id_overlap"] = len(train_ids & val_ids)
    
    train_pairs_set = {(p['prompt'].strip(), p['chosen'].strip(), p['rejected'].strip()) 
                       for p in train_pairs if all(k in p for k in ['prompt', 'chosen', 'rejected'])}
    val_pairs_set = {(p['prompt'].strip(), p['chosen'].strip(), p['rejected'].strip()) 
                     for p in val_pairs if all(k in p for k in ['prompt', 'chosen', 'rejected'])}
    results["leakage"]["pair_overlap"] = len(train_pairs_set & val_pairs_set)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Validate DPO datasets")
    parser.add_argument(
        "--dataset",
        type=Path,
        help="Path to DPO dataset file to validate"
    )
    parser.add_argument(
        "--train",
        type=Path,
        help="Path to training dataset"
    )
    parser.add_argument(
        "--validation",
        type=Path,
        help="Path to validation dataset"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    args = parser.parse_args()
    setup_logging(args.log_level)
    
    if args.dataset:
        logging.info(f"Validating {args.dataset}")
        results = validate_dataset(args.dataset)
        
        logging.info(f"\n{'='*50}")
        logging.info(f"Dataset Validation Results")
        logging.info(f"{'='*50}")
        logging.info(f"Total pairs: {results['total_pairs']}")
        logging.info(f"Valid pairs: {results['valid_pairs']}")
        logging.info(f"Quality score: {results['quality_score']:.1f}%")
        
        if results['issues']:
            logging.info(f"\nIssues found ({len(results['issues'])}):")
            for issue in results['issues'][:10]:  # Show first 10
                logging.warning(f"  - {issue}")
            if len(results['issues']) > 10:
                logging.warning(f"  ... and {len(results['issues']) - 10} more issues")
    
    if args.train and args.validation:
        logging.info(f"\nChecking for data leakage between train and validation...")
        leakage = compare_datasets(args.train, args.validation)
        
        logging.info(f"\n{'='*50}")
        logging.info(f"Data Leakage Analysis")
        logging.info(f"{'='*50}")
        logging.info(f"Training pairs: {leakage['train_pairs']}")
        logging.info(f"Validation pairs: {leakage['val_pairs']}")
        logging.info(f"\nOverlap detected:")
        logging.info(f"  Prompt overlap: {leakage['leakage']['prompt_overlap']}")
        logging.info(f"  Question ID overlap: {leakage['leakage']['question_id_overlap']}")
        logging.info(f"  Pair overlap: {leakage['leakage']['pair_overlap']}")
        
        if leakage['leakage']['prompt_overlap'] > 0:
            logging.warning("⚠️  Data leakage detected! Prompts appear in both train and validation.")


if __name__ == "__main__":
    main()

"""
Prepare DPO (Direct Preference Optimization) dataset from collected errors and gold standard queries.

This script:
1. Matches few-shot errors with gold standard queries
2. Creates DPO pairs (prompt, chosen/gold, rejected/error)
3. Splits data into train/validation sets
4. Outputs JSONL format for DPO training
5. Validates data quality and generates statistics
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import random
import logging
from collections import Counter
import statistics


def load_jsonl(filepath: Path) -> List[Dict]:
    """Load JSONL file."""
    data = []
    if not filepath.exists():
        return data
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def save_jsonl(data: List[Dict], filepath: Path):
    """Save data as JSONL."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def validate_pair(pair: Dict) -> Tuple[bool, str]:
    """
    Validate a DPO pair for quality.
    
    Returns:
        (is_valid, error_message)
    """
    # Check required fields
    required_fields = ['prompt', 'chosen', 'rejected', 'question_id']
    for field in required_fields:
        if field not in pair or not pair[field]:
            return False, f"Missing or empty field: {field}"
    
    # Check that chosen and rejected are different
    if pair['chosen'].strip() == pair['rejected'].strip():
        return False, "Chosen and rejected queries are identical"
    
    # Check minimum lengths
    if len(pair['prompt'].strip()) < 10:
        return False, "Prompt too short"
    
    if len(pair['chosen'].strip()) < 20:
        return False, "Chosen query too short"
    
    if len(pair['rejected'].strip()) < 20:
        return False, "Rejected query too short"
    
    return True, ""


def create_dpo_pair(prompt: str, gold_query: str, error_query: str, 
                   question_id: str, error_type: str = "unknown") -> Dict:
    """Create a DPO pair from prompt and queries."""
    return {
        "prompt": prompt,
        "chosen": gold_query,
        "rejected": error_query,
        "question_id": question_id,
        "metadata": {
            "source": "few-shot-error",
            "error_type": error_type,
            "timestamp": datetime.now().isoformat()
        }
    }


def prepare_dpo_dataset(few_shot_errors_path: Path, gold_standard_path: Path, 
                       output_dir: Path, train_split: float = 0.8):
    """
    Prepare DPO dataset from errors and gold standard.
    
    Args:
        few_shot_errors_path: Path to few_shot_errors.jsonl
        gold_standard_path: Path to gold_standard.jsonl
        output_dir: Directory to save processed files
        train_split: Fraction for training set (rest goes to validation)
    """
    
    # Load data
    errors = load_jsonl(few_shot_errors_path)
    gold = load_jsonl(gold_standard_path)
    
    logging.info(f"Loaded {len(errors)} few-shot errors")
    logging.info(f"Loaded {len(gold)} gold standard queries")
    
    # Create mapping from question_id to gold query
    gold_map = {item.get('question_id'): item for item in gold}
    
    # Create DPO pairs
    dpo_pairs = []
    matched = 0
    unmatched = 0
    invalid = 0
    
    error_types_count = Counter()
    
    for error_item in errors:
        question_id = error_item.get('question_id')
        
        if question_id in gold_map:
            gold_item = gold_map[question_id]
            
            pair = create_dpo_pair(
                prompt=error_item.get('prompt') or gold_item.get('prompt'),
                gold_query=gold_item.get('query'),
                error_query=error_item.get('query'),
                question_id=question_id,
                error_type=error_item.get('error_type', 'unknown')
            )
            
            # Validate pair
            is_valid, error_msg = validate_pair(pair)
            if is_valid:
                dpo_pairs.append(pair)
                matched += 1
                error_type = pair['metadata']['error_type']
                error_types_count[error_type] += 1
            else:
                invalid += 1
                logging.debug(f"Invalid pair for {question_id}: {error_msg}")
        else:
            unmatched += 1
            logging.warning(f"No gold standard for question_id {question_id}")
    
    logging.info(f"\nPairing Results:")
    logging.info(f"  Matched and valid: {matched}")
    logging.info(f"  Unmatched: {unmatched}")
    logging.info(f"  Invalid format: {invalid}")
    
    logging.info(f"\nError Type Distribution:")
    for error_type, count in error_types_count.most_common():
        logging.info(f"  {error_type}: {count}")
    
    if not dpo_pairs:
        logging.error("No valid DPO pairs created!")
        return
    
    # Shuffle and split
    random.shuffle(dpo_pairs)
    split_idx = int(len(dpo_pairs) * train_split)
    
    train_pairs = dpo_pairs[:split_idx]
    val_pairs = dpo_pairs[split_idx:]
    
    # Save splits
    output_dir.mkdir(parents=True, exist_ok=True)
    
    save_jsonl(dpo_pairs, output_dir / "dpo_pairs.jsonl")
    save_jsonl(train_pairs, output_dir / "train_split.jsonl")
    save_jsonl(val_pairs, output_dir / "validation_split.jsonl")
    
    logging.info(f"\nDataset Statistics:")
    logging.info(f"  Total pairs: {len(dpo_pairs)}")
    logging.info(f"  Training: {len(train_pairs)} ({len(train_pairs)/len(dpo_pairs)*100:.1f}%)")
    logging.info(f"  Validation: {len(val_pairs)} ({len(val_pairs)/len(dpo_pairs)*100:.1f}%)")
    
    # Calculate average lengths
    prompt_lengths = [len(p['prompt'].split()) for p in dpo_pairs]
    chosen_lengths = [len(p['chosen'].split()) for p in dpo_pairs]
    rejected_lengths = [len(p['rejected'].split()) for p in dpo_pairs]
    
    logging.info(f"\nToken Statistics (by words):")
    logging.info(f"  Prompt - Mean: {statistics.mean(prompt_lengths):.0f}, Median: {statistics.median(prompt_lengths):.0f}")
    logging.info(f"  Chosen - Mean: {statistics.mean(chosen_lengths):.0f}, Median: {statistics.median(chosen_lengths):.0f}")
    logging.info(f"  Rejected - Mean: {statistics.mean(rejected_lengths):.0f}, Median: {statistics.median(rejected_lengths):.0f}")
    
    # Save statistics report
    stats = {
        "total_pairs": len(dpo_pairs),
        "train_pairs": len(train_pairs),
        "validation_pairs": len(val_pairs),
        "error_type_distribution": dict(error_types_count),
        "prompt_stats": {
            "mean": statistics.mean(prompt_lengths),
            "median": statistics.median(prompt_lengths),
            "min": min(prompt_lengths),
            "max": max(prompt_lengths)
        },
        "chosen_stats": {
            "mean": statistics.mean(chosen_lengths),
            "median": statistics.median(chosen_lengths),
            "min": min(chosen_lengths),
            "max": max(chosen_lengths)
        },
        "rejected_stats": {
            "mean": statistics.mean(rejected_lengths),
            "median": statistics.median(rejected_lengths),
            "min": min(rejected_lengths),
            "max": max(rejected_lengths)
        },
        "created_at": datetime.now().isoformat()
    }
    
    with open(output_dir / "dataset_stats.json", 'w') as f:
        json.dump(stats, f, indent=2)
    
    logging.info(f"\nSaved to {output_dir}")
    logging.info(f"Statistics saved to {output_dir / 'dataset_stats.json'}")


def main():
    parser = argparse.ArgumentParser(description="Prepare DPO dataset from errors and gold standard")
    parser.add_argument(
        "--errors",
        type=Path,
        default=Path(__file__).parent.parent / "datasets" / "raw" / "few_shot_errors.jsonl",
        help="Path to few_shot_errors.jsonl"
    )
    parser.add_argument(
        "--gold",
        type=Path,
        default=Path(__file__).parent.parent / "datasets" / "raw" / "gold_standard.jsonl",
        help="Path to gold_standard.jsonl"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "datasets" / "processed",
        help="Output directory for processed dataset"
    )
    parser.add_argument(
        "--train-split",
        type=float,
        default=0.8,
        help="Fraction of data to use for training (default: 0.8)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create output directory if it doesn't exist
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Run preparation
    try:
        prepare_dpo_dataset(
            args.errors,
            args.gold,
            args.output,
            args.train_split
        )
        logging.info("DPO dataset preparation completed successfully!")
    except Exception as e:
        logging.error(f"Error during DPO dataset preparation: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

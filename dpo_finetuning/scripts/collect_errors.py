"""
Collect few-shot generation errors and their metadata for DPO training.

This script:
1. Monitors decomposition pipeline for failed queries
2. Logs incorrect queries with their errors
3. Saves to few_shot_errors.jsonl for later pairing with gold standard
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import logging


def setup_logging(log_file: Optional[Path] = None):
    """Setup logging configuration."""
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def log_error_query(
    output_path: Path,
    question: str,
    generated_query: str,
    error_message: str,
    question_id: str,
    error_type: str = "unknown",
    metadata: Optional[Dict] = None
):
    """
    Log an incorrect query to the dataset file.
    
    Args:
        output_path: Path to few_shot_errors.jsonl
        question: Natural language question
        generated_query: The incorrectly generated SPARQL
        error_message: Error from executor/SPARQL endpoint
        question_id: Unique identifier for the question
        error_type: Category of error (syntax, semantic, limit_placement, etc.)
        metadata: Additional metadata
    """
    
    error_record = {
        "question_id": question_id,
        "prompt": question,
        "query": generated_query,
        "error": error_message,
        "error_type": error_type,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    # Append to JSONL file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'a') as f:
        f.write(json.dumps(error_record) + '\n')
    
    logging.info(f"Logged error for question {question_id}: {error_type}")


def log_gold_query(
    output_path: Path,
    question: str,
    correct_query: str,
    question_id: str,
    source: str = "manual",
    metadata: Optional[Dict] = None
):
    """
    Log a correct reference query (gold standard).
    
    Args:
        output_path: Path to gold_standard.jsonl
        question: Natural language question
        correct_query: The correct SPARQL query
        question_id: Unique identifier for the question
        source: Where this came from (manual, test_set, verified, etc.)
        metadata: Additional metadata
    """
    
    gold_record = {
        "question_id": question_id,
        "prompt": question,
        "query": correct_query,
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'a') as f:
        f.write(json.dumps(gold_record) + '\n')
    
    logging.info(f"Logged gold standard for question {question_id}")


def main():
    parser = argparse.ArgumentParser(description="Collect error queries for DPO training")
    parser.add_argument(
        "--errors-output",
        type=Path,
        default=Path(__file__).parent.parent / "datasets" / "raw" / "few_shot_errors.jsonl",
        help="Output file for error queries"
    )
    parser.add_argument(
        "--gold-output",
        type=Path,
        default=Path(__file__).parent.parent / "datasets" / "raw" / "gold_standard.jsonl",
        help="Output file for gold standard queries"
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Optional log file"
    )
    
    args = parser.parse_args()
    setup_logging(args.log_file)
    
    logging.info(f"Error queries will be saved to: {args.errors_output}")
    logging.info(f"Gold standard queries will be saved to: {args.gold_output}")
    logging.info("Ready to collect data. Use log_error_query() and log_gold_query() functions.")


if __name__ == "__main__":
    main()

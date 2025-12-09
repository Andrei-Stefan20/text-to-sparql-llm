"""
Sample and analyze DPO dataset examples.

This script:
1. Randomly samples pairs from the dataset
2. Shows examples in readable format
3. Analyzes query complexity and diversity
4. Generates example reports
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List
import random
import logging
from collections import Counter


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
                data.append(json.loads(line))
    return data


def analyze_query_complexity(query: str) -> Dict:
    """Analyze SPARQL query complexity metrics."""
    metrics = {
        "length": len(query),
        "word_count": len(query.split()),
        "has_filter": "FILTER" in query.upper(),
        "has_optional": "OPTIONAL" in query.upper(),
        "has_union": "UNION" in query.upper(),
        "has_service": "SERVICE" in query.upper(),
        "has_limit": "LIMIT" in query.upper(),
        "has_orderby": "ORDER BY" in query.upper(),
        "brace_count": query.count("{"),
    }
    return metrics


def print_pair(pair: Dict, index: int = None):
    """Pretty print a DPO pair."""
    if index is not None:
        print(f"\n{'='*80}")
        print(f"EXAMPLE {index}")
        print(f"{'='*80}")
    
    print(f"\nQuestion ID: {pair.get('question_id', 'N/A')}")
    print(f"Error Type: {pair.get('metadata', {}).get('error_type', 'N/A')}")
    
    print(f"\n📝 PROMPT:")
    print(f"   {pair.get('prompt', 'N/A')}")
    
    print(f"\n✅ CHOSEN (Gold Standard):")
    chosen_query = pair.get('chosen', 'N/A')
    # Pretty print SPARQL
    lines = chosen_query.split('\n')
    for line in lines:
        print(f"   {line}")
    
    chosen_metrics = analyze_query_complexity(chosen_query)
    print(f"   📊 Complexity: {chosen_metrics['word_count']} words, {chosen_metrics['length']} chars")
    
    print(f"\n❌ REJECTED (Error):")
    rejected_query = pair.get('rejected', 'N/A')
    lines = rejected_query.split('\n')
    for line in lines:
        print(f"   {line}")
    
    rejected_metrics = analyze_query_complexity(rejected_query)
    print(f"   📊 Complexity: {rejected_metrics['word_count']} words, {rejected_metrics['length']} chars")
    
    # Highlight differences
    print(f"\n🔍 DIFFERENCES:")
    if chosen_metrics['has_filter'] != rejected_metrics['has_filter']:
        print(f"   - FILTER clause: {rejected_metrics['has_filter']} → {chosen_metrics['has_filter']}")
    if chosen_metrics['has_optional'] != rejected_metrics['has_optional']:
        print(f"   - OPTIONAL clause: {rejected_metrics['has_optional']} → {chosen_metrics['has_optional']}")
    if chosen_metrics['has_limit'] != rejected_metrics['has_limit']:
        print(f"   - LIMIT clause: {rejected_metrics['has_limit']} → {chosen_metrics['has_limit']}")


def main():
    parser = argparse.ArgumentParser(description="Sample and analyze DPO dataset")
    parser.add_argument(
        "--dataset",
        type=Path,
        required=True,
        help="Path to DPO dataset file"
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=5,
        help="Number of samples to show (default: 5)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Save samples to a file"
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Only show statistics, don't display examples"
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
    
    # Load dataset
    pairs = load_jsonl(args.dataset)
    
    if not pairs:
        logging.error(f"No data found in {args.dataset}")
        return 1
    
    logging.info(f"Loaded {len(pairs)} pairs from {args.dataset}")
    
    # Calculate statistics
    error_types = Counter()
    has_filter = 0
    has_optional = 0
    has_limit = 0
    prompt_lengths = []
    chosen_lengths = []
    rejected_lengths = []
    
    for pair in pairs:
        if 'metadata' in pair:
            error_types[pair['metadata'].get('error_type', 'unknown')] += 1
        
        chosen_metrics = analyze_query_complexity(pair.get('chosen', ''))
        rejected_metrics = analyze_query_complexity(pair.get('rejected', ''))
        
        if chosen_metrics['has_filter']:
            has_filter += 1
        if chosen_metrics['has_optional']:
            has_optional += 1
        if chosen_metrics['has_limit']:
            has_limit += 1
        
        prompt_lengths.append(len(pair.get('prompt', '').split()))
        chosen_lengths.append(len(pair.get('chosen', '').split()))
        rejected_lengths.append(len(pair.get('rejected', '').split()))
    
    # Print statistics
    print(f"\n{'='*80}")
    print(f"DATASET STATISTICS")
    print(f"{'='*80}")
    print(f"Total pairs: {len(pairs)}")
    print(f"\nError Type Distribution:")
    for error_type, count in error_types.most_common():
        print(f"  {error_type}: {count} ({count/len(pairs)*100:.1f}%)")
    
    print(f"\nQuery Features:")
    print(f"  With FILTER: {has_filter} ({has_filter/len(pairs)*100:.1f}%)")
    print(f"  With OPTIONAL: {has_optional} ({has_optional/len(pairs)*100:.1f}%)")
    print(f"  With LIMIT: {has_limit} ({has_limit/len(pairs)*100:.1f}%)")
    
    print(f"\nAverage Length (words):")
    print(f"  Prompt: {sum(prompt_lengths)/len(prompt_lengths):.1f}")
    print(f"  Chosen: {sum(chosen_lengths)/len(chosen_lengths):.1f}")
    print(f"  Rejected: {sum(rejected_lengths)/len(rejected_lengths):.1f}")
    
    if not args.stats_only:
        # Sample pairs
        random.seed(args.seed)
        samples = random.sample(pairs, min(args.samples, len(pairs)))
        
        output_text = f"\nDPO Dataset Samples\n{'='*80}\n"
        
        for idx, sample in enumerate(samples, 1):
            print_pair(sample, idx)
            # Also collect for output file
            output_text += f"\n\nEXAMPLE {idx}\n"
            output_text += f"{'='*80}\n"
            output_text += f"Question ID: {sample.get('question_id', 'N/A')}\n"
            output_text += f"Error Type: {sample.get('metadata', {}).get('error_type', 'N/A')}\n\n"
            output_text += f"PROMPT:\n{sample.get('prompt', 'N/A')}\n\n"
            output_text += f"CHOSEN:\n{sample.get('chosen', 'N/A')}\n\n"
            output_text += f"REJECTED:\n{sample.get('rejected', 'N/A')}\n"
        
        # Save to file if requested
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w') as f:
                f.write(output_text)
            logging.info(f"\nSamples saved to {args.output}")
    
    return 0


if __name__ == "__main__":
    exit(main())

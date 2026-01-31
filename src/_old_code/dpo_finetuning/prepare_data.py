#!/usr/bin/env python3
import json
import argparse
import random
from pathlib import Path
from typing import List, Dict


def load_data(filepath: Path) -> List[Dict]:
    if filepath.suffix == ".jsonl":
        data = []
        with open(filepath, "r") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data
    else:
        with open(filepath, "r") as f:
            return json.load(f)


def validate_sample(sample: Dict) -> bool:
    return "question" in sample and "gold_query" in sample


def prepare_datasets(
    input_file: Path,
    output_dir: Path,
    train_ratio: float = 0.8,
    random_seed: int = 42,
) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {input_file}...")
    data = load_data(input_file)

    valid_samples = [s for s in data if validate_sample(s)]
    invalid = len(data) - len(valid_samples)

    if invalid > 0:
        print(f"Skipped {invalid} invalid samples")

    print(f"{len(valid_samples)} valid samples")

    for i, sample in enumerate(valid_samples):
        if "id" not in sample:
            sample["id"] = f"q_{i:06d}"

    random.seed(random_seed)
    random.shuffle(valid_samples)

    split_idx = int(len(valid_samples) * train_ratio)
    train_data = valid_samples[:split_idx]
    test_data = valid_samples[split_idx:]

    def save_jsonl(data, path):
        with open(path, "w") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")

    train_file = output_dir / "train.jsonl"
    test_file = output_dir / "test.jsonl"

    save_jsonl(train_data, train_file)
    save_jsonl(test_data, test_file)

    print(f"Train: {train_file} ({len(train_data)})")
    print(f"Test: {test_file} ({len(test_data)})")


def main():
    parser = argparse.ArgumentParser(description="Prepare datasets")
    parser.add_argument("--input", type=Path, required=True, help="Input file")
    parser.add_argument("--output", type=Path, required=True, help="Output dir")
    parser.add_argument("--train-ratio", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()
    prepare_datasets(args.input, args.output, args.train_ratio, args.seed)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path

from complete_finetuning_pipeline import DataHandler, run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="DPO fine-tuning pipeline for SPARQL")
    parser.add_argument("--model", type=str, required=True, help="Model name/path")
    parser.add_argument("--train", type=Path, required=True, help="Train JSONL")
    parser.add_argument("--test", type=Path, required=True, help="Test JSONL")
    parser.add_argument(
        "--output", type=Path, default=Path("./results"), help="Output dir"
    )
    parser.add_argument("--config", type=Path, help="Config JSON")
    parser.add_argument(
        "--finetuned-model", type=Path, help="Existing fine-tuned model"
    )
    parser.add_argument("--4bit", action="store_true", help="4-bit quantization")

    args = parser.parse_args()

    if not args.train.exists():
        logger.error(f"Train not found: {args.train}")
        return 1

    if not args.test.exists():
        logger.error(f"Test not found: {args.test}")
        return 1

    train_data = DataHandler.load_jsonl(args.train)
    test_data = DataHandler.load_jsonl(args.test)
    logger.info(f"Train: {len(train_data)}, Test: {len(test_data)}")

    config = {}
    if args.config and args.config.exists():
        import json

        with open(args.config) as f:
            config = json.load(f)
        logger.info(f"Config loaded: {args.config}")

    if args._4bit:
        config.setdefault("inference", {})["use_4bit"] = True

    try:
        run_pipeline(
            train_data=train_data,
            test_data=test_data,
            model_name=args.model,
            output_dir=args.output,
            config=config,
            finetuned_model=args.finetuned_model,
        )
        return 0
    except Exception as e:
        logger.error(f"Failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

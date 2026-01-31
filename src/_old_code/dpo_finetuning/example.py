#!/usr/bin/env python3
from pathlib import Path
from complete_finetuning_pipeline import DataHandler, run_pipeline


def example_1_basic():
    train_data = DataHandler.load_jsonl(Path("datasets/raw/train.jsonl"))
    test_data = DataHandler.load_jsonl(Path("datasets/raw/test.jsonl"))

    results = run_pipeline(
        train_data=train_data,
        test_data=test_data,
        model_name="meta-llama/Llama-2-7b-hf",
        output_dir=Path("results"),
    )

    print(f"Status: {results['status']}")


def example_2_with_config():
    train_data = DataHandler.load_jsonl(Path("datasets/raw/train.jsonl"))
    test_data = DataHandler.load_jsonl(Path("datasets/raw/test.jsonl"))

    config = {
        "inference": {"temperature": 0.5, "max_new_tokens": 256, "use_4bit": True},
        "finetuning": {"num_epochs": 5, "batch_size": 2, "learning_rate": 1e-4},
    }

    run_pipeline(
        train_data=train_data,
        test_data=test_data,
        model_name="meta-llama/Llama-2-7b-hf",
        output_dir=Path("results"),
        config=config,
    )


def example_3_eval_only():
    train_data = DataHandler.load_jsonl(Path("datasets/raw/train.jsonl"))
    test_data = DataHandler.load_jsonl(Path("datasets/raw/test.jsonl"))

    run_pipeline(
        train_data=train_data,
        test_data=test_data,
        model_name="meta-llama/Llama-2-7b-hf",
        output_dir=Path("results"),
        finetuned_model=None,
    )


if __name__ == "__main__":
    print("DPO Pipeline Examples")
    print("1. Basic: example_1_basic()")
    print("2. With config: example_2_with_config()")
    print("3. Eval only: example_3_eval_only()")

    print("Example 3: Skip fine-tuning")
    print(
        "  python -c 'from example import example_3_skip_finetuning; example_3_skip_finetuning()'\n"
    )

    print("Or use CLI:")
    print("  python run_pipeline.py --model meta-llama/Llama-2-7b-hf \\")
    print("    --train datasets/raw/train.jsonl \\")
    print("    --test datasets/raw/test.jsonl \\")
    print("    --output results")

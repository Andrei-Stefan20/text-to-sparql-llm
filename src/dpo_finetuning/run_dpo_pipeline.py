#!/usr/bin/env python3
"""
DPO Fine-Tuning Pipeline Orchestrator

Complete end-to-end orchestration for Direct Preference Optimization (DPO) fine-tuning
of language models for SPARQL query generation improvement.

Pipeline Steps:
    1. Prepare Dataset      - Convert raw error/gold pairs into DPO preference pairs
    2. Validate Dataset     - Quality assurance and integrity checks
    3. Analyze Dataset      - Statistical analysis and visualization
    4. Train DPO Model      - Fine-tune using DPO algorithm with quantization/LoRA
    5. Evaluate Model       - Assess performance using standard metrics
    6. Compare with Baseline - Comparative analysis against baseline model

Requirements:
    - torch>=2.0.0
    - transformers>=4.36.0
    - trl>=0.7.0
    - peft>=0.7.0
    - datasets
    - pyyaml
    - rouge-score
    - nltk

Environment Variables (Optional):
    CUDA_VISIBLE_DEVICES - GPU device selection
    PYTORCH_CUDA_ALLOC_CONF - CUDA memory configuration
    HF_HOME - HuggingFace cache directory

Author: Text-to-SPARQL Team
Version: 1.0.0
Date: December 2024
"""

import argparse
import sys
import logging
import os
from pathlib import Path
from typing import Optional, List
import subprocess
import json
from datetime import datetime


# Configure logging with ISO timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Utility Functions
# =============================================================================

def verify_environment() -> bool:
    """
    Verify that required packages are installed and accessible.
    
    Returns:
        bool: True if environment is properly configured, False otherwise
    """
    required_packages = {
        'torch': 'torch',
        'transformers': 'transformers',
        'trl': 'trl',
        'peft': 'peft',
        'datasets': 'datasets',
        'yaml': 'pyyaml',
        'rouge_score': 'rouge-score',
        'nltk': 'nltk',
    }
    
    missing_packages = []
    
    for import_name, pip_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.error(f"Install with: pip install {' '.join(missing_packages)}")
        return False
    
    logger.info("✓ All required packages are installed")
    return True


def verify_input_files(errors_file: Path, gold_file: Path, config_file: Path) -> bool:
    """
    Verify that all required input files exist and are readable.
    
    Args:
        errors_file: Path to error queries file
        gold_file: Path to gold standard queries file
        config_file: Path to DPO configuration file
    
    Returns:
        bool: True if all files exist and are readable, False otherwise
    """
    files_to_check = {
        'Error queries file': errors_file,
        'Gold standard file': gold_file,
        'Configuration file': config_file,
    }
    
    all_exist = True
    for name, filepath in files_to_check.items():
        if not filepath.exists():
            logger.error(f"{name} not found: {filepath}")
            all_exist = False
        elif not filepath.is_file():
            logger.error(f"{name} is not a file: {filepath}")
            all_exist = False
        else:
            logger.info(f"✓ {name} found: {filepath}")
    
    return all_exist


def create_output_directories(output_base: Path) -> bool:
    """
    Create required output directory structure.
    
    Args:
        output_base: Base output directory path
    
    Returns:
        bool: True if directories created successfully, False otherwise
    """
    required_dirs = [
        output_base / 'datasets' / 'processed',
        output_base / 'models',
        output_base / 'results' / 'evaluation',
        output_base / 'results' / 'comparison',
        output_base / 'logs',
    ]
    
    try:
        for directory in required_dirs:
            directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Output directory structure created: {output_base}")
        return True
    except Exception as e:
        logger.error(f"Failed to create output directories: {e}")
        return False


def log_pipeline_start(errors_file: Path, gold_file: Path, output_base: Path) -> None:
    """Log pipeline start information."""
    logger.info(f"\n{'='*80}")
    logger.info(f"{'DPO FINE-TUNING PIPELINE START':^80}")
    logger.info(f"{'='*80}")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"Error file: {errors_file.resolve()}")
    logger.info(f"Gold file: {gold_file.resolve()}")
    logger.info(f"Output directory: {output_base.resolve()}")
    logger.info(f"{'='*80}\n")


def run_command(cmd: List[str], description: str) -> bool:
    """
    Execute a shell command and monitor execution.
    
    Logs command execution, success/failure status, and error details.
    Returns without raising exceptions to allow pipeline continuation.
    
    Args:
        cmd: Command and arguments as list of strings
        description: Human-readable description of the command
    
    Returns:
        bool: True if command succeeded, False otherwise
    """
    logger.info(f"\n{'-'*80}")
    logger.info(f"STEP: {description}")
    logger.info(f"{'-'*80}")
    logger.info(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=False,
            text=True,
        )
        logger.info(f"✓ {description} completed successfully (exit code: {result.returncode})")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ {description} failed with exit code {e.returncode}")
        if e.stdout:
            logger.error(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            logger.error(f"STDERR:\n{e.stderr}")
        return False
        
    except FileNotFoundError as e:
        logger.error(f"✗ Command not found: {cmd[0]}")
        return False
        
    except Exception as e:
        logger.error(f"✗ {description} failed with exception: {type(e).__name__}: {e}")
        return False


def log_step_status(step_name: str, status: str, skipped: bool = False) -> None:
    """Log the status of a pipeline step."""
    if skipped:
        logger.info(f"⊘ {step_name}: SKIPPED")
    elif status == "success":
        logger.info(f"✓ {step_name}: SUCCESS")
    elif status == "warning":
        logger.info(f"⚠ {step_name}: WARNING - Continuing with caution")
    elif status == "error":
        logger.info(f"✗ {step_name}: FAILED")


# =============================================================================
# Pipeline Steps
# =============================================================================

def prepare_dataset(
    errors_file: Path,
    gold_file: Path,
    output_dir: Path,
    skip: bool = False
) -> bool:
    """
    Step 1: Prepare DPO dataset from raw error and gold standard queries.
    
    Converts raw JSONL files into DPO preference pairs with train/validation split.
    
    Args:
        errors_file: Path to file with error queries
        gold_file: Path to file with gold standard queries
        output_dir: Output directory for processed data
        skip: Whether to skip this step
    
    Returns:
        bool: True if step succeeded or was skipped, False if failed
    """
    if skip:
        log_step_status("Dataset Preparation", "success", skipped=True)
        return True
    
    cmd = [
        "python", "-m", "dpo_finetuning.scripts.prepare_dpo_dataset",
        "--errors", str(errors_file),
        "--gold", str(gold_file),
        "--output-dir", str(output_dir),
        "--train-split", "0.8",
    ]
    
    if run_command(cmd, "Prepare DPO Dataset"):
        log_step_status("Dataset Preparation", "success")
        return True
    else:
        log_step_status("Dataset Preparation", "error")
        logger.error("Dataset preparation failed. Subsequent steps may be affected.")
        return False


def validate_dataset(
    output_dir: Path,
    skip: bool = False
) -> bool:
    """
    Step 2: Validate dataset quality and integrity.
    
    Performs quality assurance checks including:
    - Missing field detection
    - Duplicate pair identification
    - Data leakage detection (train/val overlap)
    - Statistical quality metrics
    
    Args:
        output_dir: Directory containing processed dataset files
        skip: Whether to skip this step
    
    Returns:
        bool: True if step succeeded or was skipped
    """
    if skip:
        log_step_status("Dataset Validation", "success", skipped=True)
        return True
    
    train_file = output_dir / "train_split.jsonl"
    val_file = output_dir / "validation_split.jsonl"
    
    if not train_file.exists() or not val_file.exists():
        logger.warning("Dataset files not found. Skipping validation.")
        return True
    
    cmd = [
        "python", "-m", "dpo_finetuning.scripts.validate_dataset",
        "--train", str(train_file),
        "--validation", str(val_file),
        "--output-dir", str(output_dir),
    ]
    
    if run_command(cmd, "Validate Dataset Quality"):
        log_step_status("Dataset Validation", "success")
        return True
    else:
        log_step_status("Dataset Validation", "warning")
        return True  # Non-fatal, continue


def analyze_dataset(
    output_dir: Path,
    skip: bool = False
) -> bool:
    """
    Step 3: Analyze and visualize dataset characteristics.
    
    Generates statistics on:
    - Query complexity metrics
    - Token length distribution
    - Error type categorization
    - SPARQL feature frequency
    
    Args:
        output_dir: Directory containing processed dataset files
        skip: Whether to skip this step
    
    Returns:
        bool: True if step succeeded or was skipped
    """
    if skip:
        log_step_status("Dataset Analysis", "success", skipped=True)
        return True
    
    train_file = output_dir / "train_split.jsonl"
    
    if not train_file.exists():
        logger.warning("Training dataset not found. Skipping analysis.")
        return True
    
    cmd = [
        "python", "-m", "dpo_finetuning.scripts.sample_dataset",
        "--data", str(train_file),
        "--num-samples", "20",
        "--output", str(output_dir / "dataset_analysis.txt"),
    ]
    
    if run_command(cmd, "Analyze Dataset"):
        log_step_status("Dataset Analysis", "success")
        return True
    else:
        log_step_status("Dataset Analysis", "warning")
        return True  # Non-fatal, continue


def train_model(
    config_file: Path,
    models_dir: Path,
    logs_dir: Path,
    skip: bool = False
) -> bool:
    """
    Step 4: Train DPO fine-tuned model.
    
    Executes DPO training with:
    - Model quantization (4-bit/8-bit)
    - LoRA parameter-efficient adaptation
    - DPO loss optimization
    - Checkpoint management
    
    Args:
        config_file: Path to DPO training configuration
        models_dir: Directory for model output
        logs_dir: Directory for training logs
        skip: Whether to skip this step
    
    Returns:
        bool: True if step succeeded or was skipped, False if failed
    """
    if skip:
        log_step_status("Model Training", "success", skipped=True)
        return True
    
    models_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "python", "-m", "dpo_finetuning.scripts.train_dpo",
        "--config", str(config_file),
        "--output-dir", str(models_dir / "dpo_finetuned"),
        "--logging-dir", str(logs_dir),
    ]
    
    if run_command(cmd, "Train DPO Model"):
        log_step_status("Model Training", "success")
        return True
    else:
        log_step_status("Model Training", "error")
        logger.error("Model training failed. Cannot proceed without trained model.")
        return False


def evaluate_model(
    model_dir: Path,
    eval_data: Path,
    output_dir: Path,
    device: str = "cuda",
    num_samples: Optional[int] = None,
    skip: bool = False
) -> bool:
    """
    Step 5: Evaluate fine-tuned model performance.
    
    Computes evaluation metrics:
    - Exact Match (EM)
    - BLEU Score
    - ROUGE-1 and ROUGE-L
    - Keyword Overlap (SPARQL-specific)
    
    Args:
        model_dir: Path to trained model directory
        eval_data: Path to evaluation dataset (JSONL)
        output_dir: Output directory for evaluation results
        device: Device for inference (cuda/cpu)
        num_samples: Number of samples to evaluate (None = all)
        skip: Whether to skip this step
    
    Returns:
        bool: True if step succeeded or was skipped
    """
    if skip:
        log_step_status("Model Evaluation", "success", skipped=True)
        return True
    
    if not model_dir.exists():
        logger.warning(f"Model directory not found: {model_dir}")
        return True
    
    if not eval_data.exists():
        logger.warning(f"Evaluation data not found: {eval_data}")
        return True
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "python", "-m", "dpo_finetuning.scripts.evaluate_model",
        "--model", str(model_dir),
        "--eval-data", str(eval_data),
        "--output-dir", str(output_dir),
        "--device", device,
    ]
    
    if num_samples:
        cmd.extend(["--num-samples", str(num_samples)])
    
    if run_command(cmd, "Evaluate Fine-tuned Model"):
        log_step_status("Model Evaluation", "success")
        return True
    else:
        log_step_status("Model Evaluation", "warning")
        return True  # Non-fatal, continue


def compare_models(
    baseline_model: Optional[str],
    finetuned_model_dir: Path,
    eval_data: Path,
    output_dir: Path,
    device: str = "cuda",
    num_samples: Optional[int] = None,
    skip: bool = False
) -> bool:
    """
    Step 6: Compare fine-tuned model with baseline.
    
    Performs comparative analysis:
    - Side-by-side metric comparison
    - Improvement/regression identification
    - Per-example analysis
    - Aggregate statistics
    
    Args:
        baseline_model: Baseline model name/path for comparison
        finetuned_model_dir: Path to fine-tuned model
        eval_data: Path to evaluation dataset (JSONL)
        output_dir: Output directory for comparison results
        device: Device for inference (cuda/cpu)
        num_samples: Number of samples to evaluate (None = all)
        skip: Whether to skip this step
    
    Returns:
        bool: True if step succeeded, skipped, or baseline not provided
    """
    if skip:
        log_step_status("Model Comparison", "success", skipped=True)
        return True
    
    if not baseline_model:
        logger.info("Baseline model not specified. Skipping comparison.")
        return True
    
    if not finetuned_model_dir.exists():
        logger.warning(f"Fine-tuned model not found: {finetuned_model_dir}")
        return True
    
    if not eval_data.exists():
        logger.warning(f"Evaluation data not found: {eval_data}")
        return True
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "python", "-m", "dpo_finetuning.scripts.compare_models",
        "--baseline", str(baseline_model),
        "--finetuned", str(finetuned_model_dir),
        "--eval-data", str(eval_data),
        "--output-dir", str(output_dir),
        "--device", device,
    ]
    
    if num_samples:
        cmd.extend(["--num-samples", str(num_samples)])
    
    if run_command(cmd, "Compare with Baseline"):
        log_step_status("Model Comparison", "success")
        return True
    else:
        log_step_status("Model Comparison", "warning")
        return True  # Non-fatal, continue


# =============================================================================
# Main Pipeline Orchestration
# =============================================================================

def run_pipeline(
    errors_file: Path,
    gold_file: Path,
    output_base: Path,
    config_file: Path,
    baseline_model: Optional[str] = None,
    num_eval_samples: Optional[int] = None,
    skip_steps: Optional[List[str]] = None,
    device: str = "cuda",
) -> bool:
    """
    Execute the complete DPO fine-tuning pipeline with proper orchestration.
    
    Manages pipeline execution flow, error handling, and progress tracking.
    Each step is independent and can be skipped via configuration.
    
    Pipeline Sequence:
        1. Prepare Dataset (load raw data, create preference pairs)
        2. Validate Dataset (quality assurance checks)
        3. Analyze Dataset (statistics and visualization)
        4. Train Model (DPO fine-tuning with quantization/LoRA)
        5. Evaluate Model (performance metrics)
        6. Compare Models (baseline vs fine-tuned comparison)
    
    Args:
        errors_file: Path to error queries file (JSONL)
        gold_file: Path to gold standard queries file (JSONL)
        output_base: Base output directory for all results
        config_file: Path to DPO training configuration (YAML)
        baseline_model: Optional baseline model for comparison
        num_eval_samples: Optional limit on evaluation samples
        skip_steps: List of steps to skip (prepare, validate, analyze, train, evaluate, compare)
        device: Device for inference (cuda or cpu)
    
    Returns:
        bool: True if pipeline completed successfully, False otherwise
    """
    
    if skip_steps is None:
        skip_steps = []
    
    # =========================================================================
    # Pre-flight Checks
    # =========================================================================
    
    log_pipeline_start(errors_file, gold_file, output_base)
    
    # Verify environment
    if not verify_environment():
        logger.error("Environment verification failed. Please install required packages.")
        return False
    
    # Verify input files
    if not verify_input_files(errors_file, gold_file, config_file):
        logger.error("Input file verification failed.")
        return False
    
    # Create output directories
    if not create_output_directories(output_base):
        logger.error("Failed to create output directories.")
        return False
    
    # =========================================================================
    # Step 1: Prepare Dataset
    # =========================================================================
    
    processed_dir = output_base / "datasets" / "processed"
    if not prepare_dataset(
        errors_file,
        gold_file,
        processed_dir,
        skip="prepare" in skip_steps
    ):
        logger.error("Pipeline stopped: Dataset preparation failed")
        return False
    
    # =========================================================================
    # Step 2: Validate Dataset
    # =========================================================================
    
    validate_dataset(
        processed_dir,
        skip="validate" in skip_steps
    )
    
    # =========================================================================
    # Step 3: Analyze Dataset
    # =========================================================================
    
    analyze_dataset(
        processed_dir,
        skip="analyze" in skip_steps
    )
    
    # =========================================================================
    # Step 4: Train Model
    # =========================================================================
    
    models_dir = output_base / "models"
    logs_dir = output_base / "logs"
    
    if not train_model(
        config_file,
        models_dir,
        logs_dir,
        skip="train" in skip_steps
    ):
        logger.error("Pipeline stopped: Model training failed")
        return False
    
    # =========================================================================
    # Step 5: Evaluate Model
    # =========================================================================
    
    eval_results_dir = output_base / "results" / "evaluation"
    eval_data = processed_dir / "validation_split.jsonl"
    
    evaluate_model(
        models_dir / "dpo_finetuned",
        eval_data,
        eval_results_dir,
        device=device,
        num_samples=num_eval_samples,
        skip="evaluate" in skip_steps
    )
    
    # =========================================================================
    # Step 6: Compare with Baseline
    # =========================================================================
    
    comparison_results_dir = output_base / "results" / "comparison"
    
    compare_models(
        baseline_model,
        models_dir / "dpo_finetuned",
        eval_data,
        comparison_results_dir,
        device=device,
        num_samples=num_eval_samples,
        skip="compare" in skip_steps
    )
    
    # =========================================================================
    # Pipeline Completion
    # =========================================================================
    
    logger.info(f"\n{'='*80}")
    logger.info(f"{'PIPELINE COMPLETED SUCCESSFULLY':^80}")
    logger.info(f"{'='*80}")
    logger.info(f"Completion timestamp: {datetime.now().isoformat()}")
    logger.info(f"Results directory: {output_base.resolve()}")
    
    # Log results summary
    logger.info(f"\n{'Results Summary:':^80}")
    logger.info(f"  • Dataset: {(processed_dir / 'dpo_pairs.jsonl').resolve()}")
    logger.info(f"  • Model: {(models_dir / 'dpo_finetuned').resolve()}")
    logger.info(f"  • Evaluation: {eval_results_dir.resolve()}")
    if baseline_model:
        logger.info(f"  • Comparison: {comparison_results_dir.resolve()}")
    logger.info(f"{'='*80}\n")
    
    return True


# =============================================================================
# Command-Line Interface
# =============================================================================

def main() -> int:
    """
    Main entry point with command-line argument parsing.
    
    Returns:
        int: Exit code (0 = success, 1 = failure)
    """
    
    parser = argparse.ArgumentParser(
        prog="DPO Pipeline",
        description="Direct Preference Optimization (DPO) Fine-Tuning Pipeline for SPARQL Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:

  # Run complete pipeline with baseline comparison
  python run_dpo_pipeline.py \\
    --errors dpo_finetuning/datasets/raw/few_shot_errors.jsonl \\
    --gold dpo_finetuning/datasets/raw/gold_standard.jsonl \\
    --config dpo_finetuning/configs/dpo_config.yaml \\
    --baseline google/gemini-2.0-flash \\
    --output dpo_finetuning

  # Run pipeline skipping training (only data prep and validation)
  python run_dpo_pipeline.py \\
    --errors errors.jsonl \\
    --gold gold.jsonl \\
    --skip train evaluate compare

  # Evaluate an existing trained model
  python run_dpo_pipeline.py \\
    --errors errors.jsonl \\
    --gold gold.jsonl \\
    --skip prepare validate analyze train \\
    --output existing_results

  # CPU-only inference (no GPU)
  python run_dpo_pipeline.py \\
    --errors errors.jsonl \\
    --gold gold.jsonl \\
    --device cpu \\
    --skip train

ENVIRONMENT:
  CUDA_VISIBLE_DEVICES  - Specify GPU devices (e.g., "0,1")
  PYTORCH_CUDA_ALLOC_CONF - CUDA memory settings
  HF_HOME               - HuggingFace model cache location
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--errors",
        type=Path,
        required=True,
        help="Path to JSONL file with error queries"
    )
    parser.add_argument(
        "--gold",
        type=Path,
        required=True,
        help="Path to JSONL file with gold standard (reference) queries"
    )
    
    # Configuration arguments
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("dpo_finetuning/configs/dpo_config.yaml"),
        help="Path to DPO training configuration file (default: %(default)s)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dpo_finetuning"),
        help="Output directory for pipeline results (default: %(default)s)"
    )
    
    # Optional arguments
    parser.add_argument(
        "--baseline",
        type=str,
        default=None,
        help="Baseline model name/path for comparison (optional)"
    )
    parser.add_argument(
        "--num-eval-samples",
        type=int,
        default=None,
        help="Limit evaluation to N samples (default: all)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "cpu"],
        help="Device for inference (default: %(default)s)"
    )
    parser.add_argument(
        "--skip",
        nargs="+",
        default=[],
        choices=["prepare", "validate", "analyze", "train", "evaluate", "compare"],
        help="Pipeline steps to skip"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute pipeline
    try:
        success = run_pipeline(
            errors_file=args.errors,
            gold_file=args.gold,
            output_base=args.output,
            config_file=args.config,
            baseline_model=args.baseline,
            num_eval_samples=args.num_eval_samples,
            skip_steps=args.skip,
            device=args.device,
        )
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.warning("\nPipeline interrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"Unhandled exception in pipeline: {type(e).__name__}: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

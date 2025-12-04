"""
Command-line interface for Text-to-SPARQL evaluation pipeline.
Provides unified access to all evaluation modes and utilities.
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import config
from src.logging_config import get_logger
from src.validators import validate_file_exists

logger = get_logger(__name__)


def run_evaluation(args):
    """Execute standard evaluation based on selected model."""
    if args.model == "local":
        from src.evaluate import main
        logger.info("Running local model evaluation (HuggingFace Transformers)")
        main()
    elif args.model == "gemini":
        from src.evaluate_gemini import main
        logger.info("Running Gemini API evaluation")
        main()
    else:
        logger.error(f"Unknown model type: {args.model}")
        sys.exit(1)


def run_ace(args):
    """Execute ACE (Automated Correction Engine) evaluation."""
    from src.evaluate_ace_gemini import main
    logger.info("Running ACE Engine evaluation with Gemini")
    main()


def create_dataset(args):
    """Generate FAISS index and embeddings from training data."""
    from src.data.make_dataset import main
    logger.info("Creating dataset (FAISS index + embeddings)")
    main()


def validate_config(args):
    """Validate project configuration."""
    try:
        config.validate()
        logger.info("✓ Configuration is valid")
        logger.info(f"  Model: temperature={config.model.temperature}, max_retries={config.model.max_retries}")
        logger.info(f"  Retrieval: k_examples={config.retrieval.k_examples}, top_k={config.retrieval.top_k}")
        logger.info(f"  SPARQL: endpoint={config.sparql.endpoint}, timeout={config.sparql.timeout}s")
    except Exception as e:
        logger.error(f"✗ Configuration validation failed: {e}")
        sys.exit(1)


def check_dependencies(args):
    """Verify all required files and dependencies exist."""
    logger.info("Checking project dependencies...")
    
    # Check data files
    required_files = [
        (PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json", "Test dataset"),
        (PROJECT_ROOT / ".env", "Environment configuration"),
    ]
    
    optional_files = [
        (PROJECT_ROOT / "data/processed/train_index.faiss", "FAISS index"),
        (PROJECT_ROOT / "data/processed/train_metadata.pkl", "Metadata"),
        (PROJECT_ROOT / "playbook.json", "ACE Playbook"),
    ]
    
    errors = 0
    for path, name in required_files:
        try:
            validate_file_exists(path, name)
            logger.info(f"✓ {name}: {path}")
        except FileNotFoundError as e:
            logger.error(f"✗ {e}")
            errors += 1
    
    for path, name in optional_files:
        if path.exists():
            logger.info(f"✓ {name}: {path}")
        else:
            logger.warning(f"⚠ {name} not found: {path}")
    
    # Check Python packages
    try:
        import transformers
        import faiss
        import google.generativeai
        from sentence_transformers import SentenceTransformer
        logger.info("✓ All Python packages installed")
    except ImportError as e:
        logger.error(f"✗ Missing Python package: {e}")
        errors += 1
    
    if errors > 0:
        logger.error(f"Found {errors} critical errors")
        sys.exit(1)
    else:
        logger.info("✓ All dependencies satisfied")


def clean_playbook(args):
    """Clean and validate playbook.json."""
    import json
    playbook_path = PROJECT_ROOT / "playbook.json"
    
    try:
        validate_file_exists(playbook_path, "Playbook")
        with open(playbook_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            logger.error("Playbook must be a JSON array")
            sys.exit(1)
        
        # Remove duplicates
        unique_rules = []
        seen = set()
        for entry in data:
            rule = entry.get('rule', '')
            if rule and rule not in seen:
                unique_rules.append(entry)
                seen.add(rule)
        
        logger.info(f"Cleaned playbook: {len(data)} → {len(unique_rules)} unique strategies")
        
        if args.save:
            backup_path = playbook_path.with_suffix('.json.bak')
            playbook_path.rename(backup_path)
            with open(playbook_path, 'w', encoding='utf-8') as f:
                json.dump(unique_rules, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved cleaned playbook (backup: {backup_path})")
        
    except Exception as e:
        logger.error(f"Error cleaning playbook: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Text-to-SPARQL LLM Evaluation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create dataset (run first time)
  python cli.py dataset

  # Run evaluations
  python cli.py eval --model gemini
  python cli.py eval --model local
  python cli.py ace

  # Utilities
  python cli.py check
  python cli.py validate-config
  python cli.py clean-playbook --save
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Evaluation command
    eval_parser = subparsers.add_parser('eval', help='Run standard evaluation')
    eval_parser.add_argument(
        '--model', 
        choices=['local', 'gemini'], 
        required=True,
        help='Model type to evaluate'
    )
    
    # ACE command
    subparsers.add_parser('ace', help='Run ACE Engine evaluation')
    
    # Dataset creation
    subparsers.add_parser('dataset', help='Create FAISS index from training data')
    
    # Config validation
    subparsers.add_parser('validate-config', help='Validate configuration')
    
    # Dependency check
    subparsers.add_parser('check', help='Check all dependencies')
    
    # Playbook cleaning
    clean_parser = subparsers.add_parser('clean-playbook', help='Clean and deduplicate playbook')
    clean_parser.add_argument('--save', action='store_true', help='Save cleaned version')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Route to appropriate handler
    handlers = {
        'eval': run_evaluation,
        'ace': run_ace,
        'dataset': create_dataset,
        'validate-config': validate_config,
        'check': check_dependencies,
        'clean-playbook': clean_playbook,
    }
    
    handler = handlers.get(args.command)
    if handler:
        handler(args)
    else:
        logger.error(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

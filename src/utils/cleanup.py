#!/usr/bin/env python3
"""
Cleanup script to remove cache, temporary files, and generated outputs.
"""

import os
import shutil
import sys
from pathlib import Path


def cleanup_cache():
    """Remove HuggingFace cache and local models."""
    cache_dir = Path.home() / ".cache" / "huggingface"
    if cache_dir.exists():
        print(f"Removing HuggingFace cache: {cache_dir}")
        shutil.rmtree(cache_dir)
        print("✓ Cache removed")
    else:
        print("No HuggingFace cache found")
    
    project_root = Path(__file__).parent.parent.parent
    local_models = project_root / "models"
    if local_models.exists():
        print(f"Removing local models: {local_models}")
        shutil.rmtree(local_models)
        print("✓ Local models removed")
    else:
        print("No local models directory found")


def cleanup_pycache():
    """Remove __pycache__ and .pyc files."""
    project_root = Path(__file__).parent.parent.parent
    
    for pycache in project_root.rglob("__pycache__"):
        print(f"Removing: {pycache}")
        shutil.rmtree(pycache)
    
    for pyc in project_root.rglob("*.pyc"):
        print(f"Removing: {pyc}")
        pyc.unlink()
    
    print("✓ Python cache cleaned")


def cleanup_outputs():
    """Remove outputs directory."""
    outputs_dir = Path(__file__).parent.parent.parent / "outputs"
    if outputs_dir.exists():
        print(f"Removing outputs: {outputs_dir}")
        shutil.rmtree(outputs_dir)
        outputs_dir.mkdir(exist_ok=True)
        print("✓ Outputs cleaned (recreated empty)")
    else:
        print("No outputs directory found")


def cleanup_tmp():
    """Remove .DS_Store and other temp files."""
    project_root = Path(__file__).parent.parent.parent
    
    patterns = [".DS_Store", ".pytest_cache", "*.egg-info", ".eggs"]
    
    for pattern in patterns:
        for item in project_root.rglob(pattern):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                print(f"Removing: {item}")
            except Exception as e:
                print(f"Failed to remove {item}: {e}")
    
    print("✓ Temp files cleaned")


def main():
    """Run all cleanup operations."""
    print("=" * 60)
    print("CLEANUP SCRIPT")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        option = sys.argv[1].lower()
        
        if option == "--cache":
            cleanup_cache()
        elif option == "--pycache":
            cleanup_pycache()
        elif option == "--outputs":
            cleanup_outputs()
        elif option == "--tmp":
            cleanup_tmp()
        elif option == "--all":
            cleanup_cache()
            cleanup_pycache()
            cleanup_outputs()
            cleanup_tmp()
        else:
            print(f"Unknown option: {option}")
            print_help()
            sys.exit(1)
    else:
        print_help()


def print_help():
    """Print usage help."""
    print("\nUsage:")
    print("  python -m src.utils.cleanup [OPTION]")
    print("\nOptions:")
    print("  --cache      Remove HuggingFace cache and local models")
    print("  --pycache    Remove __pycache__ and .pyc files")
    print("  --outputs    Remove outputs directory")
    print("  --tmp        Remove temporary files (.DS_Store, etc)")
    print("  --all        Run all cleanup operations")
    print("\nExample:")
    print("  python -m src.utils.cleanup --all")
    print("  python -m src.utils.cleanup --cache")


if __name__ == "__main__":
    main()
    print("=" * 60)
    print("Cleanup complete!")
    print("=" * 60)

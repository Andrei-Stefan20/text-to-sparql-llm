#!/usr/bin/env python3
"""
MLflow UI Launcher
Starts the MLflow tracking UI to visualize evaluation results.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

def main():
    """Launch MLflow UI on localhost:5000."""
    print("=" * 60)
    print("Starting MLflow Tracking UI...")
    print("=" * 60)
    print()
    print("View your evaluation results at:")
    print("   http://localhost:5000")
    print()
    print("Features available:")
    print("  • Compare multiple runs")
    print("  • View metrics over time")
    print("  • Download artifacts (reports, visualizations)")
    print("  • Filter and search experiments")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        # Set MLflow tracking URI to local directory
        mlruns_dir = PROJECT_ROOT / "mlruns"
        mlruns_dir.mkdir(exist_ok=True)
        
        # Launch MLflow UI
        subprocess.run([
            sys.executable, "-m", "mlflow", "ui",
            "--port", "5000",
            "--host", "127.0.0.1"
        ], cwd=str(PROJECT_ROOT))
        
    except KeyboardInterrupt:
        print("\n\n✓ MLflow UI stopped")
    except Exception as e:
        print(f"\n✗ Error starting MLflow UI: {e}")
        print("\nTroubleshooting:")
        print("  1. Install MLflow: pip install mlflow")
        print("  2. Check if port 5000 is available")
        print("  3. Verify mlruns/ directory exists")
        sys.exit(1)

if __name__ == "__main__":
    main()

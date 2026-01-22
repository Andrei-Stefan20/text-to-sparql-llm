"""
Fine-Tuning Pipeline for SPARQL Query Generation

Main components:
- complete_finetuning_pipeline: Core pipeline implementation
- run_pipeline: CLI entry point
- prepare_data: Dataset preparation utility
"""

from complete_finetuning_pipeline import (
    InferenceEngine,
    DataHandler,
    QueryComparator,
    run_pipeline,
)

__version__ = "1.0.0"

__all__ = [
    'InferenceEngine',
    'DataHandler',
    'QueryComparator',
    'run_pipeline',
]

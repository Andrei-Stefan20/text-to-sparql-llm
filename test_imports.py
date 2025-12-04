#!/usr/bin/env python3
"""
Quick test to verify all imports and configuration work correctly.
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test all critical imports."""
    try:
        logger.info("Testing configuration...")
        from src.config import config
        logger.info("Configuration loaded")
        
        logger.info("Testing pipeline utilities...")
        from src.pipeline_utils import retry, timeout, SimpleCache, BatchProcessor
        logger.info("Pipeline utilities imported")
        
        logger.info("Testing SPARQL client...")
        from src.utils.sparql_client import SPARQLClient
        logger.info("SPARQL client imported")
        
        logger.info("Testing retriever...")
        from src.models.retriever import FewShotRetriever
        logger.info("Retriever imported")
        
        logger.info("Testing generator utilities...")
        from src.models.generator import build_prompt, build_ace_prompt
        logger.info("Generator utilities imported")
        
        logger.info("Testing evaluation modules...")
        from src.evaluate_gemini import GeminiGenerator as GG
        from src.evaluate import LocalLLMGenerator as LLG
        logger.info("Evaluation modules imported")
        
        logger.info("Testing MLflow reporter...")
        from src.evaluation.mlflow_reporter import MLflowReporter
        logger.info("MLflow reporter imported")
        
        logger.info("\n" + "="*50)
        logger.info("All imports successful!")
        logger.info("="*50)
        
        # Print configuration summary
        logger.info("\nConfiguration Summary:")
        logger.info(f"  Model: {config.model.gemini_model_id}")
        logger.info(f"  Max retries: {config.evaluation.max_retries}")
        logger.info(f"  K examples: {config.retrieval.k_examples}")
        logger.info(f"  SPARQL endpoint: {config.sparql.endpoint_url}")
        
        return True
        
    except Exception as e:
        logger.error(f"Import failed: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

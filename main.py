import hydra
import asyncio
import logging
import os
from omegaconf import DictConfig, OmegaConf
from dotenv import load_dotenv

from src.data.loader import DatasetLoader
from src.components.entity_linker import get_linker
from src.components.rag_retriever import RagRetriever
from src.components.schema_retriever import SchemaRetriever
from src.components.prompt_builder import PromptBuilder

from src.pipelines.batch_runner import BatchRunner
from src.utils.logging_utils import ExperimentLogger, generate_run_name

from src.clients.azure_client import AzureClient
from src.clients.openai_client import OpenAIClient

from src.evaluation.metrics import OfflineEvaluator

load_dotenv()

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_client_factory(cfg: DictConfig):
    """
    Method to instantiate the correct LLM Client based on the configuration.
    """
    platform = cfg.platform.lower()
    if platform == "azure":
        return AzureClient(cfg)
    elif platform == "openai":
        return OpenAIClient(cfg)
    else:
        raise ValueError(f"Unsupported platform: {platform}")

@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg: DictConfig):
    """
    Main entry point for the Text-to-SPARQL.
    
    Workflow:
    1. Initialize Experiment Logging (Artifacts).
    2. Load and filter the Dataset (QALD).
    3. Initialize Logic Components (Linker, Retriever, Schema).
    4. Execute the Async Batch Pipeline.
    5. Compute and Save Evaluation Metrics.
    """
    
    # 1. Experiment Setup
    run_id = generate_run_name(cfg)
    logger.info(f"Initializing Experiment Run: {run_id}")
    logger.info(f"Configuration Snapshot:\n{OmegaConf.to_yaml(cfg)}")

    exp_logger = ExperimentLogger(cfg)

    try:
        # 2. Data Loading
        logger.info("Loading dataset...")
        loader = DatasetLoader(
            dataset_name=cfg.dataset.name, 
            split=cfg.dataset.split, 
            language=cfg.dataset.language
        )
        full_dataset = loader.load()
        
        limit = cfg.dataset.get("limit")
        if limit is not None and limit > 0:
            logger.info(f"Dataset limit applied: processing first {limit} items only.")
            dataset = full_dataset[:limit]
        else:
            dataset = full_dataset

        if not dataset:
            logger.error("Dataset is empty after loading. Aborting execution.")
            return

        # 3. Component Initialization
        logger.info("Initializing system components...")
        
        # A. LLM Client
        client = get_client_factory(cfg.model)
        
        # B. Entity Linker 
        linker = get_linker(cfg.linking)
        
        # C. RAG Retriever (Fetches similar Q&A pairs for few-shot learning)
        retriever = RagRetriever(cfg.retrieval, cfg.rag)
        
        # D. Schema Retriever
        schema_retriever = SchemaRetriever(cfg.rag) 
        
        # E. Prompt Builder 
        prompt_builder = PromptBuilder(cfg.prompt)

        # 4. Pipeline Execution
        logger.info(f"Starting Batch Pipeline with concurrency limit: {cfg.model.concurrency}")
        
        # Initialize the runner with all dependencies
        runner = BatchRunner(
            client=client, 
            prompt_builder=prompt_builder, 
            concurrency=cfg.model.concurrency,
            schema_retriever=schema_retriever
        )
        
        # Execute the pipeline asynchronously
        results = asyncio.run(runner.run(dataset, linker, retriever))

        # 5. Evaluation & Reporting
        logger.info("Computing offline evaluation metrics...")
        
        # Compute proxy metrics (Syntax Validity, Exact Match)
        metrics = OfflineEvaluator.compute_metrics(results)
        logger.info(f"Final Metrics: {metrics}")
        
        # Prepare the final output object structure
        final_output = {
            "meta": {
                "run_id": run_id,
                "status": "completed",
                "dataset_size": len(dataset)
            },
            "configuration": OmegaConf.to_container(cfg, resolve=True),
            "metrics": metrics,
            "results": results
        }

        # 6. Artifact Persistence
        exp_logger.save_results(final_output)
        logger.info("Experiment completed successfully. All artifacts saved.")

    except Exception as e:
        logger.critical(f"Critical System Failure: {e}", exc_info=True)
        raise e

if __name__ == "__main__":
    main()
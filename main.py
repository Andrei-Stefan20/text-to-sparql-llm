import asyncio
import logging
import os

import hydra
from dotenv import load_dotenv
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf

from src.clients.azure_client import AzureClient
from src.clients.openai_client import OpenAIClient
from src.components.entity_linker import get_linker
from src.components.prompt_builder import PromptBuilder
from src.components.rag_retriever import RagRetriever
from src.components.schema_retriever import SchemaRetriever
from src.data.loader import DatasetLoader
from src.evaluation.metrics import OfflineEvaluator
from src.pipelines.batch_runner import BatchRunner
from src.utils.logging_utils import ExperimentLogger, generate_run_name

load_dotenv()

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
    """

    output_dir = HydraConfig.get().runtime.output_dir
    logger.info(f"Experiment started. Output directory: {output_dir}")

    # 1. Experiment Setup
    run_id = generate_run_name(cfg)
    logger.info(f"Initializing Experiment Run: {run_id}")
    logger.info(f"Configuration Snapshot:\n{OmegaConf.to_yaml(cfg)}")

    exp_logger = ExperimentLogger(cfg, output_dir=output_dir)

    try:
        # 2. Data Loading
        logger.info("Loading dataset...")
        loader = DatasetLoader(
            dataset_name=cfg.dataset.name,
            split=cfg.dataset.split,
            language=cfg.dataset.language,
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

        # B. Entity Linker(s)
        cache_dir = cfg.system.get("cache_dir")
        linker = get_linker(cfg.linking, cache_dir=cache_dir)
        
        # Optional: Use a second linker for hybrid approach
        linker2 = None
        if cfg.linking.get("use_dual_linkers", False):
            secondary_method = cfg.linking.get("secondary_method")
            if secondary_method:
                logger.info(f"Initializing secondary linker: {secondary_method}")
                from omegaconf import DictConfig as OmegaConfConfig
                secondary_config = OmegaConfConfig({"method": secondary_method})
                linker2 = get_linker(secondary_config, cache_dir=cache_dir)
                logger.info("✓ Dual linker mode enabled")

        # C. RAG Retriever (Fetches similar Q&A pairs for few-shot learning)
        retriever = RagRetriever(cfg.retrieval, cfg.rag)

        # D. Schema Retriever
        schema_retriever = SchemaRetriever(cfg.rag)

        # E. Prompt Builder
        prompt_builder = PromptBuilder(cfg.prompt)

        # 4. Pipeline Execution
        # Get validation and correction settings
        validation_cfg = cfg.get("validation", {})
        
        logger.info(
            f"Starting Batch Pipeline with concurrency limit: {cfg.model.concurrency}"
        )
        
        if validation_cfg.get("enable_correction", False):
            logger.info(
                f"Self-correction enabled: max_attempts={validation_cfg.get('max_attempts', 3)}, "
                f"self_consistency={validation_cfg.get('self_consistency_samples', 1)}"
            )

        runner = BatchRunner(
            client=client,
            prompt_builder=prompt_builder,
            concurrency=cfg.model.concurrency,
            schema_retriever=schema_retriever,
            linker2=linker2,
            # Validation & Correction settings
            enable_validation=validation_cfg.get("enable_validation", True),
            enable_correction=validation_cfg.get("enable_correction", False),
            max_correction_attempts=validation_cfg.get("max_attempts", 3),
            validate_execution=validation_cfg.get("validate_execution", False),
            # Self-consistency settings
            self_consistency_samples=validation_cfg.get("self_consistency_samples", 1),
            consistency_temperature=validation_cfg.get("consistency_temperature", 0.7),
        )

        results = asyncio.run(runner.run(dataset, linker, retriever))

        # 5. Evaluation & Reporting
        logger.info("Computing offline evaluation metrics...")

        metrics = OfflineEvaluator.compute_metrics(results)
        logger.info(f"Final Metrics: {metrics}")

        final_output = {
            "meta": {
                "run_id": run_id,
                "status": "completed",
                "dataset_size": len(dataset),
            },
            "configuration": OmegaConf.to_container(cfg, resolve=True),
            "metrics": metrics,
            "results": results,
        }

        # 6. Artifact Persistence
        exp_logger.save_results(final_output)
        logger.info(
            f"Experiment completed successfully. Artifacts saved in: {output_dir}"
        )

    except Exception as e:
        logger.critical(f"Critical System Failure: {e}", exc_info=True)
        raise e


if __name__ == "__main__":
    main()

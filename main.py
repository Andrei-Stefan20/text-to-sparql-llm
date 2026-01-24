import hydra
import asyncio
import logging
import os
from omegaconf import DictConfig, OmegaConf
from dotenv import load_dotenv

from src.data.loader import DatasetLoader
from src.components.entity_linker import get_linker
from src.components.rag_retriever import RagRetriever
from src.components.prompt_builder import PromptBuilder 
from src.components.schema_retriever import SchemaRetriever
from src.pipelines.batch_runner import BatchRunner
from src.utils.logging_utils import ExperimentLogger, generate_run_name
from src.clients.azure_client import AzureClient
from src.clients.openai_client import OpenAIClient


load_dotenv()
logger = logging.getLogger(__name__)

def get_client(cfg):
    if cfg.platform == "azure": return AzureClient(cfg)
    elif cfg.platform == "openai": return OpenAIClient(cfg)
    raise ValueError(f"Unknown platform: {cfg.platform}")

@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg: DictConfig):
    # 1. Genera nome esperimento dinamico
    run_id = generate_run_name(cfg)
    logger.info(f"INITIALIZING EXPERIMENT: {run_id}")
    

    exp_logger = ExperimentLogger(cfg)

    try:
        # 2. Load Data with Limit
        loader = DatasetLoader(
            dataset_name=cfg.dataset.name, 
            split=cfg.dataset.split, 
            language=cfg.dataset.language
        )
        full_dataset = loader.load()
        
        # Gestione parametrica del numero di dati
        if cfg.dataset.limit is not None and cfg.dataset.limit > 0:
            logger.warning(f"LIMITING DATASET to {cfg.dataset.limit} items.")
            dataset = full_dataset[:cfg.dataset.limit]
        else:
            dataset = full_dataset

        # 3. Components
        client = get_client(cfg.model)
        linker = get_linker(cfg.linking)
        retriever = RagRetriever(cfg.retrieval, cfg.rag)
        
        # 4. Prompt Strategy (NEW)
        prompt_builder = PromptBuilder(cfg.prompt)
        schema_retriever = SchemaRetriever(cfg.rag)

        # 5. Run Pipeline
        runner = BatchRunner(
            client=client, 
            prompt_builder=prompt_builder, 
            concurrency=cfg.model.concurrency,
            schema_retriever=schema_retriever
        )
        
        results = asyncio.run(runner.run(dataset, linker, retriever))

        exp_logger.save_results(results)

    except Exception as e:
        logger.critical(f"Failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()
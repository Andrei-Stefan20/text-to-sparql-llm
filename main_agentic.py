"""
main_agentic.py — Entry point for the Agentic Text-to-SPARQL pipeline.

Uses:
  conf/config.yaml          (base config, same as main.py)
  conf/prompt/agentic.yaml  (overrides prompt group)
  conf/model/*.yaml         (model selection)
  conf/linking/*.yaml       (entity linker)
  conf/retrieval/*.yaml     (RAG retrieval)

Run examples:
  # GPT-4o-mini, agentic mode, full test set
  python main_agentic.py model=azure_gpt4_mini

  # GPT-4o, limit 50 questions, REBEL linker
  python main_agentic.py model=azure_gpt4 dataset.limit=50 linking=rebel

  # Llama, 3-shot RAG, ReliK linker
  python main_agentic.py model=llama_33 retrieval=3shot linking=relik

  # Override agent loop settings
  python main_agentic.py model=azure_gpt4_mini prompt.max_steps=8

"""

import asyncio
import json
import logging
import os
from pathlib import Path

import hydra
from dotenv import load_dotenv
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf

from src.clients.azure_client import AzureClient
from src.clients.openai_client import OpenAIClient
from src.components.entity_linker import get_linker
from src.components.rag_retriever import RagRetriever
from src.components.schema_retriever import SchemaRetriever
from src.data.loader import DatasetLoader
from src.pipelines.agentic_pipeline import AgenticBatchRunner
from src.utils.logging_utils import ExperimentLogger

load_dotenv()
logger = logging.getLogger(__name__)


def get_client(cfg: DictConfig):
    """
    Method to instantiate the correct LLM Client based on the configuration.
    """
    platform = cfg.platform.lower()
    if platform == "azure":
        return AzureClient(cfg)
    elif platform == "openai":
        return OpenAIClient(cfg)
    raise ValueError(f"Unsupported platform: {platform}")


# ---------------------------------------------------------------------------
# Run-name generator (agentic flavour)
# ---------------------------------------------------------------------------


def _run_name(cfg: DictConfig) -> str:
    model = cfg.model.name.replace("-", "").replace(" ", "")
    linker = cfg.linking.method
    k = cfg.retrieval.k
    limit = cfg.dataset.get("limit")
    steps = cfg.prompt.get("max_steps", 6)
    lim_str = f"lim{limit}" if limit else "full"
    return f"agentic_{model}_{k}shot_{linker}_steps{steps}_{lim_str}"


# ---------------------------------------------------------------------------
# Compute summary stats from results
# ---------------------------------------------------------------------------


def _compute_stats(results: list) -> dict:
    total = len(results)
    if total == 0:
        return {}

    valid = sum(1 for r in results if r.get("is_valid", False))
    errors = sum(1 for r in results if r.get("error"))
    terminated_final = sum(
        1 for r in results if r.get("termination_reason") == "final_answer"
    )
    terminated_max = sum(
        1 for r in results if r.get("termination_reason") == "max_steps"
    )
    avg_steps = sum(r.get("total_steps", 0) for r in results) / total if total else 0

    return {
        "total": total,
        "valid_syntax_rate": round(valid / total, 4),
        "error_rate": round(errors / total, 4),
        "terminated_final_answer": terminated_final,
        "terminated_max_steps": terminated_max,
        "avg_steps_per_question": round(avg_steps, 2),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg: DictConfig):
    """Entry point for the agentic SPARQL generation pipeline."""

    output_dir = HydraConfig.get().runtime.output_dir
    logger.info(f"Output directory: {output_dir}")

    # Force agentic prompt (safety guard)
    if cfg.prompt.get("strategy", "") != "agentic":
        logger.warning(
            "prompt.strategy is not 'agentic'. "
            "This script requires conf/prompt/agentic.yaml. "
            "Run with: python main_agentic.py prompt=agentic ..."
        )

    run_id = _run_name(cfg)
    logger.info(f"Run ID: {run_id}")
    logger.info(f"Config:\n{OmegaConf.to_yaml(cfg)}")

    exp_logger = ExperimentLogger(cfg, output_dir=output_dir)

    try:
        #  1. Load dataset 
        logger.info("Loading dataset...")
        loader = DatasetLoader(
            dataset_name=cfg.dataset.name,
            split=cfg.dataset.split,
            language=cfg.dataset.language,
        )
        full_dataset = loader.load()

        limit = cfg.dataset.get("limit")
        dataset = full_dataset[:limit] if (limit and limit > 0) else full_dataset

        if not dataset:
            logger.error("Dataset is empty. Aborting.")
            return

        logger.info(f"Dataset size: {len(dataset)} questions")

        #  2. Initialise components 
        logger.info("Initialising components...")

        client = get_client(cfg.model)

        cache_dir = cfg.system.get("cache_dir")
        linker = get_linker(cfg.linking, cache_dir=cache_dir)
        linker2 = None  # extend here if needed

        retriever = RagRetriever(cfg.retrieval, cfg.rag)
        schema_retriever = SchemaRetriever(cfg.rag)

        # Agent settings from prompt config
        max_steps = cfg.prompt.get("max_steps", 6)
        step_delay = cfg.prompt.get("step_delay", 0.5)
        system_prompt = cfg.prompt.get(
            "system_message",
            "You are a Wikidata SPARQL agent. Follow the ReAct format strictly.",
        )

        # Agentic mode uses lower concurrency to respect Wikidata rate limits
        # Each agent step makes a real HTTP call, so we cap at 3 concurrent agents
        concurrency = min(cfg.model.concurrency, 3)
        logger.info(
            f"Agent config — max_steps={max_steps}, "
            f"step_delay={step_delay}s, concurrency={concurrency}"
        )

        #  3. Run pipeline 
        runner = AgenticBatchRunner(
            client=client,
            system_prompt=system_prompt,
            schema_retriever=schema_retriever,
            concurrency=concurrency,
            max_steps=max_steps,
            step_delay=step_delay,
            linker2=linker2,
        )

        results = asyncio.run(runner.run(dataset, linker, retriever))

        #  4. Stats (no Wikidata evaluation — use GERBIL externally) 
        stats = _compute_stats(results)
        logger.info(f"Pipeline stats: {stats}")

        #  5. Save artifacts 
        final_output = {
            "meta": {
                "run_id": run_id,
                "status": "completed",
                "dataset_size": len(dataset),
                "pipeline": "agentic",
            },
            "configuration": OmegaConf.to_container(cfg, resolve=True),
            "stats": stats,
            "results": results,
        }

        exp_logger.save_results(final_output)
        logger.info(f"Done. Results saved to {output_dir}/results_full.json")

    except Exception as exc:
        logger.critical(f"Critical failure: {exc}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

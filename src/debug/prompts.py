import logging
import os
import sys
import time
from typing import Any, List

import hydra
from dotenv import load_dotenv
from omegaconf import DictConfig, OmegaConf

sys.path.append(os.getcwd())

from src.components.entity_linker import get_linker
from src.components.prompt_builder import PromptBuilder
from src.components.rag_retriever import RagRetriever
from src.components.schema_retriever import SchemaRetriever

logger = logging.getLogger("PromptInspector")

load_dotenv()


def format_section(title: str, content: Any, active: bool = True) -> None:
    """
    Prints a structured section for debug output.
    """
    logger.info(f"--- {title.upper()} ---")

    if not active:
        logger.info("[SKIPPED] Feature disabled in configuration.")
        return

    if isinstance(content, list):
        if not content:
            logger.info("[EMPTY] No results found.")
        else:
            for i, item in enumerate(content, 1):
                logger.info(f"{i}. {item}")
    elif isinstance(content, str):
        if not content.strip():
            logger.info("[EMPTY] No content.")
        else:
            for line in content.split("\n"):
                logger.info(line)
    else:
        logger.info(str(content))


def measure_latency(func, *args):
    """Executes a function and returns (result, latency_ms)."""
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, (end - start) * 1000


@hydra.main(config_path="../../conf", config_name="config", version_base=None)
def run_inspection(cfg: DictConfig):
    logger.info("Initializing Semantic Query:")

    # 1. Configuration Audit
    logger.info("=== ACTIVE CONFIGURATION ===")
    logger.info(f"Model:          {cfg.model.name}")
    logger.info(f"Retrieval:      k={cfg.retrieval.k} shot")
    logger.info(f"Linking:        {cfg.linking.method}")
    logger.info(f"Prompt Config:")
    logger.info(f"  - Include Examples:      {cfg.prompt.include_examples}")
    logger.info(f"  - Include Entities:      {cfg.prompt.include_entities}")
    logger.info(f"  - Include Schema Hints:  {cfg.prompt.include_schema_hint}")
    logger.info(f"  - Custom Instruction:    {cfg.prompt.custom_instruction}")
    logger.info(f"Dataset:        {cfg.dataset.name} (split: {cfg.dataset.split})")
    logger.info(f"Limit:          {cfg.dataset.limit if cfg.dataset.limit else 'No limit'}")
    logger.info("============================")

    # 2. Component Initialization
    try:
        logger.info("Loading Entity Linker...")
        cache_dir = cfg.system.get("cache_dir")
        linker = get_linker(cfg.linking, cache_dir=cache_dir)

        logger.info("Loading RAG Retriever...")
        rag = RagRetriever(cfg.retrieval, cfg.rag)

        logger.info("Loading Schema Retriever...")
        schema_retriever = SchemaRetriever(cfg.rag)

        logger.info("Loading Prompt Builder...")
        builder = PromptBuilder(cfg.prompt)

    except Exception as e:
        logger.critical(f"Initialization failed: {e}")
        sys.exit(1)

    logger.info("System Ready. Starting Interactive Loop.")

    # 3. Interactive Testing Loop
    logger.info(
        "[INSTRUCTION] Enter a natural language question to analyze the pipeline."
    )
    logger.info("[INSTRUCTION] Type 'exit' or 'quit' to terminate the session.")

    print("\n" + "="*60)
    print("SYSTEM READY - DEBUG MODE")
    print("="*60)
    print("You can override parameters with Hydra syntax:")
    print("  python src/debug/prompts.py model=azure_gpt4_mini linking=relik")
    print("  python src/debug/prompts.py retrieval=1shot prompt.include_entities=false")
    print("  python src/debug/prompts.py prompt.custom_instruction='Your custom instruction'")
    print("="*60 + "\n")

    while True:
        try:
            question = input("USER_INPUT> ").strip()

            if not question:
                continue
            if question.lower() in ["exit", "quit"]:
                logger.info("Session terminated by user.")
                break

            logger.info(f"USER_INPUT> {question}")
            logger.info(f">>> PROCESSING QUERY: '{question}'")

            # A. Entity Linking
            linking_active = cfg.linking.method.lower() != "none"
            entities = []
            if linking_active:
                entities, lat = measure_latency(linker.extract, question)
                format_section(f"ENTITY LINKING ({lat:.2f}ms)", entities, active=True)
            else:
                format_section("ENTITY LINKING", None, active=False)

            # B. Schema Retrieval
            hints, lat = measure_latency(
                schema_retriever.retrieve_recommendations, question
            )
            format_section(
                f"SCHEMA RECOMMENDATIONS ({lat:.2f}ms)",
                hints,
                active=schema_retriever.enabled,
            )

            # C. Context Retrieval
            retrieval_active = cfg.retrieval.k > 0
            context = ""
            if retrieval_active:
                context, lat = measure_latency(rag.retrieve, question)
                # Preview only first 200 chars to avoid clutter
                display_context = (
                    context[:200] + " [...]" if len(context) > 200 else context
                )
                format_section(
                    f"CONTEXT RETRIEVAL ({lat:.2f}ms)", display_context, active=True
                )
            else:
                format_section("CONTEXT RETRIEVAL", None, active=False)

            # D. Prompt Assembly
            system_prompt = builder.build_system_prompt()
            final_prompt = builder.build_user_prompt(
                question=question,
                entities=entities,
                context_examples=context,
                schema_hints=hints,
            )

            # E. Display Prompts
            print("\n" + "="*70)
            print("SYSTEM PROMPT")
            print("="*70)
            print(system_prompt)
            print("\n" + "="*70)
            print("USER PROMPT")
            print("="*70)
            print(final_prompt)
            print("="*70 + "\n")

            logger.info("=== SYSTEM PROMPT ===")
            for line in system_prompt.split("\n"):
                logger.info(line)
            logger.info("=== USER PROMPT ===")
            for line in final_prompt.split("\n"):
                logger.info(line)
            logger.info("==========================================")

        except KeyboardInterrupt:
            logger.info("Operation cancelled by KeyboardInterrupt.")
            break
        except Exception as e:
            logger.error(f"Error processing input: {e}", exc_info=True)


if __name__ == "__main__":
    run_inspection()

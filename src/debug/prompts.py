import hydra
import logging
import sys
import os
import time
from typing import List, Any
from omegaconf import DictConfig, OmegaConf
from dotenv import load_dotenv

sys.path.append(os.getcwd())

from src.components.entity_linker import get_linker
from src.components.rag_retriever import RagRetriever
from src.components.schema_retriever import SchemaRetriever
from src.components.prompt_builder import PromptBuilder

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("PromptInspector")
logger.setLevel(logging.INFO)

load_dotenv()

def format_section(title: str, content: Any, active: bool = True) -> None:
    """
    Prints a structured section for debug output.
    """
    print(f"\n--- {title.upper()} ---")
    
    if not active:
        print("[SKIPPED] Feature disabled in configuration.")
        return

    if isinstance(content, list):
        if not content:
            print("[EMPTY] No results found.")
        else:
            for i, item in enumerate(content, 1):
                print(f"{i}. {item}")
    elif isinstance(content, str):
        if not content.strip():
            print("[EMPTY] No content.")
        else:
            print(content)
    else:
        print(str(content))

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
    print("\n=== ACTIVE CONFIGURATION ===")
    print(f"Model:      {cfg.model.name}")
    print(f"Retrieval:  k={cfg.retrieval.k}")
    print(f"Linking:    {cfg.linking.method}")
    print(f"Prompting:  Examples={cfg.prompt.include_examples}, Entities={cfg.prompt.include_entities}")
    print("============================")

    # 2. Component Initialization
    try:
        logger.info("Loading Entity Linker...")
        linker = get_linker(cfg.linking)

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
    print("\n[INSTRUCTION] Enter a natural language question to analyze the pipeline.")
    print("[INSTRUCTION] Type 'exit' or 'quit' to terminate the session.\n")

    while True:
        try:
            question = input("USER_INPUT> ").strip()
            
            if not question:
                continue
            if question.lower() in ['exit', 'quit']:
                logger.info("Session terminated by user.")
                break

            print(f"\n>>> PROCESSING QUERY: '{question}'")

            #A. Entity Linking
            linking_active = cfg.linking.method.lower() != "none"
            entities = []
            if linking_active:
                entities, lat = measure_latency(linker.extract, question)
                format_section(f"ENTITY LINKING ({lat:.2f}ms)", entities, active=True)
            else:
                format_section("ENTITY LINKING", None, active=False)

            #B. Schema Retrieval
            hints, lat = measure_latency(schema_retriever.retrieve_recommendations, question)
            format_section(f"SCHEMA RECOMMENDATIONS ({lat:.2f}ms)", hints, active=schema_retriever.enabled)

            #C. Context Retrieval
            retrieval_active = cfg.retrieval.k > 0
            context = ""
            if retrieval_active:
                context, lat = measure_latency(rag.retrieve, question)
                # Preview only first 200 chars to avoid clutter
                display_context = context[:200] + " [...]" if len(context) > 200 else context
                format_section(f"CONTEXT RETRIEVAL ({lat:.2f}ms)", display_context, active=True)
            else:
                format_section("CONTEXT RETRIEVAL", None, active=False)

            #D. Prompt Assembly
            final_prompt = builder.build_user_prompt(
                question=question, 
                entities=entities, 
                context_examples=context, 
                schema_hints=hints
            )
            
            print("\n=== FINAL GENERATED PROMPT ===")
            print(final_prompt)
            print("==========================================\n")

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            break
        except Exception as e:
            logger.error(f"Error processing input: {e}", exc_info=True)

if __name__ == "__main__":
    run_inspection()
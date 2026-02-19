import asyncio
import logging
from typing import Any, Dict, List, Optional

from tqdm.asyncio import tqdm

from src.clients.base import BaseClient
from src.components.entity_linker import BaseLinker, LinkedEntity
from src.components.prompt_builder import PromptBuilder
from src.components.rag_retriever import RagRetriever
from src.components.query_validator import (
    SPARQLValidator,
    SelfCorrectionLoop,
    CorrectionResult,
)

logger = logging.getLogger(__name__)


class BatchRunner:
    """
    Batch processing pipeline with optional validation and self-correction.

    Features:
    - Entity linking (single or dual linker), executed in a thread pool to avoid
      blocking the async event loop (critical for heavy models like ReLiK).
    - RAG retrieval for few-shot examples
    - Schema hints retrieval
    - Query validation (syntax + execution)
    - Self-correction with error feedback
    - Self-consistency with majority voting
    """

    def __init__(
        self,
        client,
        prompt_builder,
        concurrency,
        schema_retriever,
        linker2=None,
        # Validation & Correction settings
        enable_validation: bool = True,
        enable_correction: bool = True,
        max_correction_attempts: int = 3,
        validate_execution: bool = False,
        # Self-consistency settings
        self_consistency_samples: int = 1,
        consistency_temperature: float = 0.7,
    ):
        self.client = client
        self.prompt_builder = prompt_builder
        self.schema_retriever = schema_retriever
        self.semaphore = asyncio.Semaphore(concurrency)
        self.linker2 = linker2

        # Validation settings
        self.enable_validation = enable_validation
        self.enable_correction = enable_correction
        self.validate_execution = validate_execution

        # Initialize validator and correction loop
        if enable_validation or enable_correction:
            self.validator = SPARQLValidator(
                timeout=10,
                validate_execution=validate_execution,
            )

            if enable_correction or self_consistency_samples > 1:
                self.correction_loop = SelfCorrectionLoop(
                    client=client,
                    prompt_builder=prompt_builder,
                    validator=self.validator,
                    max_attempts=max_correction_attempts,
                    self_consistency_samples=self_consistency_samples,
                    temperature_for_consistency=consistency_temperature,
                )
            else:
                self.correction_loop = None
        else:
            self.validator = None
            self.correction_loop = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _merge_entities(
        self,
        entities1: List[LinkedEntity],
        entities2: List[LinkedEntity],
    ) -> List[LinkedEntity]:
        """
        Merges two entity lists, preferring entries with QIDs.
        Deduplicates by QID when available, otherwise by lowercased text.
        """
        merged: Dict[str, LinkedEntity] = {}

        for entity in entities1 + entities2:
            key = entity.qid if entity.qid else entity.text.lower()
            if key not in merged or (entity.qid and not merged[key].qid):
                merged[key] = entity

        return list(merged.values())

    async def _run_linker(self, linker: BaseLinker, question: str) -> List[LinkedEntity]:
        """
        Runs the entity linker in a thread pool executor so that CPU-bound /
        blocking models (e.g. ReLiK) do not stall the async event loop.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, linker.extract, question)


    async def _process_item(
        self,
        item: Dict[str, Any],
        linker: BaseLinker,
        retriever: RagRetriever,
    ) -> Dict[str, Any]:
        """
        Processes a single dataset item through the full pipeline.

        Always returns a dict — never None.  If an unrecoverable error occurs
        the dict will contain an "error" key and empty SPARQL fields so that
        downstream evaluation can handle it gracefully.
        """
        async with self.semaphore:
            try:
                question = item["question"]
                gold_sparql = item.get("gold_sparql", "")

                # 1. Entity Extraction — run in thread to avoid blocking event loop
                entities = await self._run_linker(linker, question)

                # Combine with second linker if provided
                if self.linker2:
                    try:
                        entities2 = await self._run_linker(self.linker2, question)
                        entities = self._merge_entities(entities, entities2)
                    except Exception as e:
                        logger.warning(
                            f"[ID {item.get('id')}] Secondary linker failed: {e}"
                        )

                # 2. Retrieval
                loop = asyncio.get_event_loop()
                context = await loop.run_in_executor(None, retriever.retrieve, question)

                static_hints = await loop.run_in_executor(
                    None, self.schema_retriever.retrieve_recommendations, question
                )

                # Dynamic hints disabled by default (uncomment to enable)
                dynamic_hints = ""
                # if hasattr(self.schema_retriever, "retrieve_dynamic_props"):
                #     dynamic_hints = self.schema_retriever.retrieve_dynamic_props(entities)

                schema_hints = (
                    f"Verified Properties for entities: {dynamic_hints}\n"
                    f"Other Semantic Matches: {static_hints}"
                )

                user_prompt = self.prompt_builder.build_user_prompt(
                    question, entities, context, schema_hints
                )

                # 3. Generation
                if self.correction_loop:
                    correction_result = await self.correction_loop.generate_with_correction(
                        question=question,
                        entities=entities,
                        context_examples=context,
                        schema_hints=schema_hints,
                        system_prompt=self.prompt_builder.build_system_prompt(),
                    )
                    sparql = correction_result.final_query
                    validation_info = {
                        "is_valid": correction_result.is_valid,
                        "total_attempts": correction_result.total_attempts,
                        "correction_method": correction_result.correction_method,
                        "attempts": [
                            {
                                "valid": a.validation.is_valid,
                                "error": a.validation.error_type,
                            }
                            for a in correction_result.attempts
                        ],
                    }
                    raw_response = None
                else:
                    raw_response = await self.client.generate(user_prompt)
                    sparql = self.prompt_builder.extract_sparql_from_response(
                        raw_response, validate_syntax=True
                    )
                    validation_info = None

                # 4. Clean output
                generated_sparql = sparql.replace("\\n", "\n") if sparql else ""
                gold_sparql_clean = gold_sparql.replace("\\n", "\n") if gold_sparql else ""

                return {
                    "id": item["id"],
                    "question": question,
                    "prompt": user_prompt,
                    "generated_sparql": generated_sparql,
                    "gold_sparql": gold_sparql_clean,
                    "hints_used": schema_hints,
                    "entities_linked": [
                        {"text": e.text, "qid": e.qid} for e in entities
                    ],
                    "validation": validation_info,
                    "raw_response": (
                        raw_response
                        if raw_response and raw_response != sparql
                        else None
                    ),
                    "error": None,
                }

            except Exception as e:
                logger.error(
                    f"[ID {item.get('id', '?')}] _process_item failed: {e}",
                    exc_info=True,
                )
                # Return a safe fallback dict — never return None
                return {
                    "id": item.get("id", "unknown"),
                    "question": item.get("question", ""),
                    "prompt": "",
                    "generated_sparql": "",
                    "gold_sparql": item.get("gold_sparql", ""),
                    "hints_used": "",
                    "entities_linked": [],
                    "validation": None,
                    "raw_response": None,
                    "error": str(e),
                }

    async def run(
        self,
        dataset: List[Dict],
        linker: BaseLinker,
        retriever: RagRetriever,
    ) -> List[Dict]:
        """
        Processes all items concurrently and returns a list of result dicts.
        Guarantees no None values in the returned list.
        """
        tasks = [self._process_item(item, linker, retriever) for item in dataset]
        results = await tqdm.gather(*tasks, desc="Processing")

        # Safety net: filter any residual None (should never happen after the fix)
        valid = [r for r in results if r is not None]
        if len(valid) < len(results):
            logger.warning(
                f"{len(results) - len(valid)} items returned None — "
                "this should not happen after the exception handler fix."
            )

        # Periodic partial save every 50 items
        import json, os
        os.makedirs("outputs", exist_ok=True)
        if len(valid) >= 50:
            with open(f"outputs/partial_{len(valid)}.json", "w") as f:
                json.dump(valid, f, indent=2)

        return valid
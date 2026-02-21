"""
Agentic Batch Pipeline.

Changes in this version:
  - schema_retriever.retrieve_recommendations() now receives both `question`
    AND `entities` for hybrid FAISS search (see schema_retriever.py).
  - top_k for schema hints is now 10 (configured in SchemaRetriever).
  - All other logic unchanged.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from tqdm.asyncio import tqdm

from src.clients.base import BaseClient
from src.components.agentic_runner import (AgenticSPARQLRunner, AgentResult,
                                           WikidataTool)
from src.components.entity_linker import BaseLinker, LinkedEntity
from src.components.rag_retriever import RagRetriever
from src.components.schema_retriever import SchemaRetriever

logger = logging.getLogger(__name__)


class AgenticBatchRunner:
    """
    Batch processing pipeline using the agentic ReAct loop.
    """

    def __init__(
        self,
        client: BaseClient,
        system_prompt: str,
        schema_retriever: SchemaRetriever,
        concurrency: int = 5,
        max_steps: int = 6,
        step_delay: float = 0.5,
        linker2: Optional[BaseLinker] = None,
    ):
        self.client = client
        self.system_prompt = system_prompt
        self.schema_retriever = schema_retriever
        self.semaphore = asyncio.Semaphore(concurrency)
        self.linker2 = linker2
        self.wikidata_tool = WikidataTool(timeout=8)
        self.max_steps = max_steps
        self.step_delay = step_delay

    def _merge_entities(
        self, e1: List[LinkedEntity], e2: List[LinkedEntity]
    ) -> List[LinkedEntity]:
        merged: Dict[str, LinkedEntity] = {}
        for e in e1 + e2:
            key = e.qid if e.qid else e.text.lower()
            if key not in merged or (e.qid and not merged[key].qid):
                merged[key] = e
        return list(merged.values())

    async def _run_linker(
        self, linker: BaseLinker, question: str
    ) -> List[LinkedEntity]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, linker.extract, question)

    def _serialize_steps(self, result: AgentResult) -> List[Dict]:
        return [
            {
                "step": s.step_number,
                "thought": s.thought,
                "action": s.action,
                "query": s.query,
                "observation": s.observation,
            }
            for s in result.steps
        ]

    async def _process_item(
        self,
        item: Dict[str, Any],
        linker: BaseLinker,
        retriever: RagRetriever,
    ) -> Dict[str, Any]:
        async with self.semaphore:
            try:
                question = item["question"]
                gold_sparql = item.get("gold_sparql", "")

                # 1. Entity linking
                entities = await self._run_linker(linker, question)
                if self.linker2:
                    try:
                        e2 = await self._run_linker(self.linker2, question)
                        entities = self._merge_entities(entities, e2)
                    except Exception as exc:
                        logger.warning(
                            f"[ID {item.get('id')}] Secondary linker failed: {exc}"
                        )

                # 2. RAG retrieval
                loop = asyncio.get_event_loop()
                context = await loop.run_in_executor(None, retriever.retrieve, question)

                # 3. Schema hints 
                #    Pass both `question` and `entities` so the retriever builds:
                #    "Question: {q}. Context: {entity_names}"
                schema_hints = await loop.run_in_executor(
                    None,
                    self.schema_retriever.retrieve_recommendations,
                    question,  # question for semantic matching
                    entities,  # entities for context enrichment
                )

                # 4. Agentic loop
                runner = AgenticSPARQLRunner(
                    client=self.client,
                    system_prompt=self.system_prompt,
                    wikidata_tool=self.wikidata_tool,
                    max_steps=self.max_steps,
                    step_delay=self.step_delay,
                )

                agent_result = await runner.run(
                    question=question,
                    entities=entities,
                    context_examples=context,
                    schema_hints=schema_hints,
                )

                # 5. Clean SPARQL
                final_sparql = (
                    agent_result.final_query.replace("\\n", "\n")
                    if agent_result.final_query
                    else ""
                )
                gold_clean = gold_sparql.replace("\\n", "\n") if gold_sparql else ""

                # 6. Execute final query
                execution_result = ""
                if agent_result.is_valid and final_sparql:
                    try:
                        execution_result = await loop.run_in_executor(
                            None, self.wikidata_tool.execute, final_sparql
                        )
                    except Exception as e:
                        execution_result = f"Error executing final query: {e}"

                logger.info(
                    f"[ID {item['id']}] Done — steps={agent_result.total_steps}, "
                    f"valid={agent_result.is_valid}, reason={agent_result.termination_reason}"
                )

                return {
                    "id": item["id"],
                    "question": question,
                    "generated_sparql": final_sparql,
                    "execution_result": execution_result,
                    "gold_sparql": gold_clean,
                    "is_valid": agent_result.is_valid,
                    "termination_reason": agent_result.termination_reason,
                    "total_steps": agent_result.total_steps,
                    "validation_error": agent_result.validation_error,
                    "agent_steps": self._serialize_steps(agent_result),
                    "entities_linked": [
                        {"text": e.text, "qid": e.qid} for e in entities
                    ],
                    "schema_hints": schema_hints,
                    "error": None,
                }

            except Exception as exc:
                logger.error(
                    f"[ID {item.get('id', '?')}] _process_item failed: {exc}",
                    exc_info=True,
                )
                return {
                    "id": item.get("id", "unknown"),
                    "question": item.get("question", ""),
                    "generated_sparql": "",
                    "execution_result": "",
                    "gold_sparql": item.get("gold_sparql", ""),
                    "is_valid": False,
                    "termination_reason": "error",
                    "total_steps": 0,
                    "validation_error": str(exc),
                    "agent_steps": [],
                    "entities_linked": [],
                    "schema_hints": "",
                    "error": str(exc),
                }

    async def run(
        self,
        dataset: List[Dict],
        linker: BaseLinker,
        retriever: RagRetriever,
    ) -> List[Dict]:
        tasks = [self._process_item(item, linker, retriever) for item in dataset]
        results = await tqdm.gather(*tasks, desc="Agentic Processing")
        return [r for r in results if r is not None]

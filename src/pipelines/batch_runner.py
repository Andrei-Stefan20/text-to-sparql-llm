import asyncio
import logging
from typing import Any, Dict, List, Optional

from tqdm.asyncio import tqdm

from src.clients.base import BaseClient
from src.components.entity_linker import BaseLinker
from src.components.prompt_builder import PromptBuilder
from src.components.rag_retriever import RagRetriever

logger = logging.getLogger(__name__)


class BatchRunner:
    def __init__(self, client, prompt_builder, concurrency, schema_retriever, linker2=None):
        self.client = client
        self.prompt_builder = prompt_builder
        self.schema_retriever = schema_retriever
        self.semaphore = asyncio.Semaphore(concurrency)
        self.linker2 = linker2  # Optional second linker

    async def _process_item(self, item, linker, retriever):
        async with self.semaphore:
            question = item["question"]
            gold_sparql = item.get("gold_sparql")

            # 1. Dynamic Steps - Extract entities using both linkers if available
            entities = linker.extract(question)
            
            # Combine with second linker if provided
            if self.linker2:
                try:
                    entities2 = self.linker2.extract(question)
                    # Merge: combine and deduplicate
                    entities = list(dict.fromkeys(entities + entities2))
                    logger.info(f"Combined entities from both linkers: {entities}")
                except Exception as e:
                    logger.warning(f"Second linker failed: {e}, using primary only")
            
            context = retriever.retrieve(question)

            # 2. Dynamic Schema Retrieval
            schema_hints = self.schema_retriever.retrieve_recommendations(question)

            # 3. Build Prompt
            user_prompt = self.prompt_builder.build_user_prompt(
                question, entities, context, schema_hints
            )

            # 4. Generate
            sparql = await self.client.generate(user_prompt)

            return {
                "id": item["id"],
                "question": question,
                "generated_sparql": sparql,
                "gold_sparql": item.get("gold_sparql"),
                "hints_used": schema_hints,
            }

    async def run(
        self, dataset: List[Dict], linker: BaseLinker, retriever: RagRetriever
    ) -> List[Dict]:

        tasks = [self._process_item(item, linker, retriever) for item in dataset]
        return await tqdm.gather(*tasks, desc="Processing Batch")

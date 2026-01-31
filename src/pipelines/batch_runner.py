import asyncio
import logging
from tqdm.asyncio import tqdm
from typing import List, Dict, Any
from src.clients.base import BaseClient
from src.components.entity_linker import BaseLinker
from src.components.rag_retriever import RagRetriever
from src.components.prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)


class BatchRunner:
    def __init__(self, client, prompt_builder, concurrency, schema_retriever):
        self.client = client
        self.prompt_builder = prompt_builder
        self.schema_retriever = schema_retriever
        self.semaphore = asyncio.Semaphore(concurrency)

    async def _process_item(self, item, linker, retriever):
        async with self.semaphore:
            question = item["question"]
            # --- MODIFICA: Recuperiamo la query Gold ---
            gold_sparql = item.get("gold_sparql")
            # -------------------------------------------

            # 1. Dynamic Steps
            entities = linker.extract(question)
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

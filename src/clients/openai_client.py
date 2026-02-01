import logging
import os

from omegaconf import DictConfig
from openai import OpenAI

from src.clients.base import BaseClient

logger = logging.getLogger(__name__)


class OpenAIClient(BaseClient):
    """
    Generic OpenAI Client that supports custom endpoints (Llama-3.3).
    """

    def __init__(self, config: DictConfig):
        is_llama = "llama" in config.name.lower()

        if is_llama:
            endpoint = os.getenv("LLAMA_ENDPOINT")
            api_key = os.getenv("LLAMA_API_KEY")
            if not endpoint or not api_key:
                raise ValueError(
                    "Missing LLAMA_ENDPOINT or LLAMA_API_KEY environment variables."
                )

            logger.info(f"Initializing Llama Client at: {endpoint}")
            self.client = OpenAI(base_url=f"{endpoint}", api_key=api_key)
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            self.client = OpenAI(api_key=api_key)

        self.model_name = config.model_name
        self.temperature = config.get("temperature", 0.7)

    async def generate(self, prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant expert in SPARQL. You will be responsible for translating natural language queries into a query for use on Wikidata.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=self.temperature,
            )
            return completion.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI/Llama Generation Error: {e}")
            return ""

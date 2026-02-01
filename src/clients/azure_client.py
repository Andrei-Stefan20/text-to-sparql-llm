import logging
import os

from omegaconf import DictConfig
from openai import AzureOpenAI

from src.clients.base import BaseClient

logger = logging.getLogger(__name__)


class AzureClient(BaseClient):
    """
    Client for Azure OpenAI models (GPT-4o, GPT-4o-mini).
    """

    def __init__(self, config: DictConfig):
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        if not endpoint or not api_key:
            raise ValueError(
                "Missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY environment variables."
            )

        self.deployment = config.deployment  # "gpt-4o" o "gpt-4o-mini" config yaml
        self.temperature = config.get("temperature", 1.0)
        self.top_p = config.get("top_p", 1.0)
        self.max_tokens = config.get("max_tokens", 4096)

        logger.info(
            f"Initializing AzureOpenAI Client for deployment: {self.deployment}"
        )

        self.client = AzureOpenAI(
            api_version="2024-12-01-preview",
            azure_endpoint=endpoint,
            api_key=api_key,
        )

    async def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
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
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                model=self.deployment,
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Azure Generation Error: {e}")
            return ""

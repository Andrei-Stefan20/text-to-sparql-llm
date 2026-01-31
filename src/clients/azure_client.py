import os
import tenacity
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from omegaconf import DictConfig
from .base import BaseClient

load_dotenv()


class AzureClient(BaseClient):
    """Client for Azure OpenAI Service."""

    def __init__(self, config: DictConfig):
        self.config = config
        api_key = os.getenv(config.env_var)
        if not api_key:
            raise ValueError(f"Environment variable {config.env_var} not found.")

        self.client = AsyncAzureOpenAI(
            api_version=config.connection.api_version,
            azure_endpoint=config.connection.endpoint,
            api_key=api_key,
            timeout=config.timeout,
        )

    @tenacity.retry(
        wait=tenacity.wait_exponential(min=2, max=15),
        stop=tenacity.stop_after_attempt(5),
        retry=tenacity.retry_if_exception_type(Exception),
    )
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})

        response = await self.client.chat.completions.create(
            model=self.config.connection.deployment,
            messages=messages,
            temperature=self.config.params.temperature,
            max_tokens=self.config.params.max_tokens,
        )
        return response.choices[0].message.content

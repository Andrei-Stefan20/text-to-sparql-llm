import os
import tenacity
from dotenv import load_dotenv
from openai import AsyncOpenAI
from omegaconf import DictConfig
from .base import BaseClient

load_dotenv()

class OpenAIClient(BaseClient):
    """Client for OpenAI-compatible APIs (e.g., Llama, Mistral)."""

    def __init__(self, config: DictConfig):
        self.config = config
        api_key = os.getenv(config.env_var)
        if not api_key:
            raise ValueError(f"Environment variable {config.env_var} not found.")

        self.client = AsyncOpenAI(
            base_url=config.connection.base_url,
            api_key=api_key,
            timeout=config.timeout
        )

    @tenacity.retry(
        wait=tenacity.wait_exponential(min=1, max=10),
        stop=tenacity.stop_after_attempt(5),
        retry=tenacity.retry_if_exception_type(Exception)
    )
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})

        response = await self.client.chat.completions.create(
            model=self.config.connection.model,
            messages=messages,
            temperature=self.config.params.temperature,
            max_tokens=self.config.params.max_tokens
        )
        return response.choices[0].message.content
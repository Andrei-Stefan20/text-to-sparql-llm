import logging
import os
from typing import AsyncIterator, Optional

from omegaconf import DictConfig, OmegaConf
from openai import AsyncOpenAI, APIError, RateLimitError, APITimeoutError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from src.clients.base import BaseClient

logger = logging.getLogger(__name__)

# Default system prompt for SPARQL generation
DEFAULT_SYSTEM_PROMPT = """You are a SPARQL expert for Wikidata.
Generate ONLY valid SPARQL query code.
Do NOT include explanations, comments, code blocks, or any text.
Output ONLY the query starting with SELECT or CONSTRUCT."""


class OpenAIClient(BaseClient):
    """
    Async OpenAI Client with retry logic and streaming support.
    Supports custom endpoints (Llama-3.3, vLLM, etc.).
    """

    def __init__(self, config: DictConfig):
        cfg_dict = OmegaConf.to_container(config, resolve=True)
        is_llama = "llama" in config.name.lower()

        if is_llama:
            endpoint = os.getenv("LLAMA_ENDPOINT")
            api_key = os.getenv("LLAMA_API_KEY")
            if not endpoint or not api_key:
                raise ValueError(
                    "Missing LLAMA_ENDPOINT or LLAMA_API_KEY environment variables."
                )

            logger.info(f"Initializing AsyncOpenAI (Llama) at: {endpoint}")
            self.client = AsyncOpenAI(base_url=endpoint, api_key=api_key)
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("Missing OPENAI_API_KEY environment variable.")

            logger.info("Initializing AsyncOpenAI Client")
            self.client = AsyncOpenAI(api_key=api_key)

        # Model parameters
        self.model_name = config.model_name
        self.temperature = cfg_dict.get("temperature", 0.7)
        self.max_tokens = cfg_dict.get("max_tokens", 4096)
        self.top_p = cfg_dict.get("top_p", 1.0)

        # Configurable system prompt
        self.default_system_prompt = cfg_dict.get(
            "system_prompt", DEFAULT_SYSTEM_PROMPT
        )

        # Retry configuration
        self.max_retries = cfg_dict.get("max_retries", 5)
        self.timeout = cfg_dict.get("timeout", 60)

    @retry(
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError)),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        stop=stop_after_attempt(5),
        before_sleep=lambda retry_state: logger.warning(
            f"Retry attempt {retry_state.attempt_number} after error: {retry_state.outcome.exception()}"
        ),
    )
    async def generate(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> str:
        """
        Generates text with automatic retry on transient errors.

        Args:
            prompt: The user prompt to send to the model.
            system_prompt: Optional system prompt override.

        Returns:
            The generated text response.
        """
        effective_system_prompt = system_prompt or self.default_system_prompt

        try:
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": effective_system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
            )
            return completion.choices[0].message.content or ""

        except (RateLimitError, APITimeoutError, APIError):
            # Let tenacity handle retry
            raise
        except Exception as e:
            logger.error(f"OpenAI Generation Error (non-retryable): {e}")
            return ""

    @retry(
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError)),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        stop=stop_after_attempt(5),
    )
    async def generate_stream(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """
        Generates text with streaming support.

        Args:
            prompt: The user prompt to send to the model.
            system_prompt: Optional system prompt override.

        Yields:
            Chunks of generated text as they become available.
        """
        effective_system_prompt = system_prompt or self.default_system_prompt

        try:
            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": effective_system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except (RateLimitError, APITimeoutError, APIError):
            raise
        except Exception as e:
            logger.error(f"OpenAI Streaming Error: {e}")
            return

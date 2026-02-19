"""
Azure OpenAI Client.

This module provides an asynchronous client for interacting with Azure OpenAI models, including retry logic and streaming support.

Features:
- Supports both standard and streaming generation.
- Implements retry logic for API errors, rate limits, and timeouts.
- Configurable via environment variables and Hydra configurations.

Implementation:
- Extends the `BaseClient` abstract class.
- Uses `tenacity` for robust retry mechanisms.
- Reads API keys and endpoints from environment variables.
"""

import logging
import os
from typing import AsyncIterator, Optional

from omegaconf import DictConfig, OmegaConf
from openai import APIError, APITimeoutError, AsyncAzureOpenAI, RateLimitError
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from src.clients.base import BaseClient

logger = logging.getLogger(__name__)

# Default system prompt for SPARQL generation
DEFAULT_SYSTEM_PROMPT = """You are a SPARQL expert for Wikidata.
Generate ONLY valid SPARQL query code.
Do NOT include explanations, comments, code blocks, or any text.
Output ONLY the query starting with SELECT or CONSTRUCT."""


class AzureClient(BaseClient):
    """
    Async client for Azure OpenAI models with retry logic and streaming support.
    """

    def __init__(self, config: DictConfig):
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        if not endpoint or not api_key:
            raise ValueError(
                "Missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY environment variables."
            )

        cfg_dict = OmegaConf.to_container(config, resolve=True)

        # Connection settings
        if "connection" in cfg_dict and "deployment" in cfg_dict["connection"]:
            self.deployment = cfg_dict["connection"]["deployment"]
        else:
            self.deployment = cfg_dict.get("deployment", "gpt-4o-mini")

        if "connection" in cfg_dict and "api_version" in cfg_dict["connection"]:
            self.api_version = cfg_dict["connection"]["api_version"]
        else:
            self.api_version = "2024-12-01-preview"

        # Model parameters
        params = cfg_dict.get("params", {})
        self.temperature = params.get("temperature", 0.0)
        self.top_p = params.get("top_p", 1.0)
        self.max_tokens = params.get("max_tokens", 4096)

        # Configurable system prompt
        self.default_system_prompt = cfg_dict.get(
            "system_prompt", DEFAULT_SYSTEM_PROMPT
        )

        # Retry configuration
        self.max_retries = cfg_dict.get("max_retries", 5)
        self.timeout = cfg_dict.get("timeout", 60)

        logger.info(
            f"Initializing AsyncAzureOpenAI Client for deployment: {self.deployment}"
        )

        self.client = AsyncAzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
            timeout=self.timeout,
        )

    @retry(
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError)),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        stop=stop_after_attempt(5),
        before_sleep=lambda retry_state: logger.warning(
            f"Retry attempt {retry_state.attempt_number} after error: {retry_state.outcome.exception()}"
        ),
    )
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
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
            response = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": effective_system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                model=self.deployment,
            )
            return response.choices[0].message.content or ""

        except (RateLimitError, APITimeoutError, APIError):
            # Let tenacity handle retry
            raise
        except Exception as e:
            logger.error(f"Azure Generation Error (non-retryable): {e}")
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
                messages=[
                    {"role": "system", "content": effective_system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                model=self.deployment,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except (RateLimitError, APITimeoutError, APIError):
            raise
        except Exception as e:
            logger.error(f"Azure Streaming Error: {e}")
            return

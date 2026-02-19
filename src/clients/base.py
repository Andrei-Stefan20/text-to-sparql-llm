"""
Base Client Interface.

This module defines the abstract interface for LLM clients, ensuring consistency across different implementations.

Features:
- Abstract methods for text generation and streaming generation.
- Provides a unified interface for all LLM clients.

Implementation:
- Defines `generate` for standard text generation.
- Defines `generate_stream` for streaming text generation.
- Serves as the base class for specific client implementations (e.g., Azure, OpenAI).
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional


class BaseClient(ABC):
    """Abstract interface for LLM clients."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generates text based on the provided prompts.
        
        Args:
            prompt: The user prompt to send to the model.
            system_prompt: Optional system prompt override. If None, uses default.
            
        Returns:
            The generated text response.
        """
        pass

    @abstractmethod
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
        pass

from abc import ABC, abstractmethod


class BaseClient(ABC):
    """Abstract interface for LLM clients."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generates text based on the provided prompts."""
        pass

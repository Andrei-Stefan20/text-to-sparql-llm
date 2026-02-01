import os
import logging
from openai import AzureOpenAI
from omegaconf import DictConfig, OmegaConf
from src.clients.base import BaseClient

logger = logging.getLogger(__name__)

class AzureClient(BaseClient):
    """
    Client for Azure OpenAI models.
    """
    def __init__(self, config: DictConfig):
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        if not endpoint or not api_key:
            raise ValueError("Missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY environment variables.")

        cfg_dict = OmegaConf.to_container(config, resolve=True)
        
        if "connection" in cfg_dict and "deployment" in cfg_dict["connection"]:
            self.deployment = cfg_dict["connection"]["deployment"]
        else:
            self.deployment = cfg_dict.get("deployment", "gpt-4o-mini")

        if "connection" in cfg_dict and "api_version" in cfg_dict["connection"]:
            self.api_version = cfg_dict["connection"]["api_version"]
        else:
            self.api_version = "2024-12-01-preview"

        params = cfg_dict.get("params", {})
        self.temperature = params.get("temperature", 0.0)
        self.top_p = params.get("top_p", 1.0)
        self.max_tokens = params.get("max_tokens", 4096)

        logger.info(f"Initializing AzureOpenAI Client for deployment: {self.deployment}")
        
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )

    async def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant expert in SPARQL.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                model=self.deployment
            )
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Azure Generation Error: {e}")
            return ""
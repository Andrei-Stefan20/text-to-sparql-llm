"""
Centralized configuration management for the Text-to-SPARQL project.
All constants, hyperparameters, and paths are defined here.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"


@dataclass
class ModelConfig:
    """LLM model configuration parameters."""

    temperature: float = 0.1
    max_new_tokens: int = 512
    top_p: float = 0.95
    top_k: int = 50

    # Model identifiers
    local_model_id: str = "Qwen/Qwen2.5-Coder-3B-Instruct"
    gemini_model_id: str = "models/gemini-2.0-flash"

    # Hardware optimization
    use_flash_attention: bool = True
    torch_compile: bool = True
    device_map: str = "auto"


@dataclass
class RetrievalConfig:
    """RAG and retrieval configuration."""

    k_examples: int = 3
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"
    faiss_index_path: Path = DATA_DIR / "processed" / "train_index.faiss"
    metadata_path: Path = DATA_DIR / "processed" / "train_metadata.pkl"
    chunk_size: int = 50  # For entity API calls


@dataclass
class EvaluationConfig:
    """Evaluation pipeline configuration."""

    max_retries: int = 3
    retry_with_error_feedback: bool = True
    test_sample_size: Optional[int] = 20  # None for full dataset
    test_data_path: Path = (
        DATA_DIR / "raw" / "QALD-10" / "data" / "qald_10" / "qald_10.json"
    )

    # ACE specific
    ace_max_retries: int = 3
    playbook_path: Path = PROJECT_ROOT / "playbook.json"


@dataclass
class SPARQLConfig:
    """SPARQL endpoint configuration."""

    endpoint_url: str = "https://query.wikidata.org/sparql"
    user_agent: str = "TextToSparqlBot/1.0"
    timeout: int = 60
    wikidata_api_url: str = "https://www.wikidata.org/w/api.php"
    api_delay: float = 0.1  # Seconds between API calls


@dataclass
class Config:
    """Main configuration container."""

    model: ModelConfig = field(default_factory=ModelConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    evaluation: EvaluationConfig = field(default_factory=EvaluationConfig)
    sparql: SPARQLConfig = field(default_factory=SPARQLConfig)

    # API Keys
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    def __post_init__(self):
        """Load environment variables and validate paths."""
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Create directories if they don't exist
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def validate(self) -> bool:
        """Validates critical configuration settings."""
        issues = []

        if not self.retrieval.faiss_index_path.exists():
            issues.append(f"FAISS index not found: {self.retrieval.faiss_index_path}")

        if not self.retrieval.metadata_path.exists():
            issues.append(f"Metadata not found: {self.retrieval.metadata_path}")

        if not self.evaluation.test_data_path.exists():
            issues.append(f"Test data not found: {self.evaluation.test_data_path}")

        if issues:
            print("⚠️  Configuration validation issues:")
            for issue in issues:
                print(f"  - {issue}")
            return False

        return True


# Global config instance
config = Config()


# Stop sequences for different models
STOP_SEQUENCES = {
    "default": ["User:", "```", "###", "Question:", "\n\n"],
    "gemini": ["User:", "###", "Question:"],
    "ace": ["### USER QUESTION", "User:"],
}

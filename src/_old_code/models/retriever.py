import faiss
import pickle
import logging
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Global model cache to avoid reloading
_MODEL_CACHE = {}


def _get_embedding_model(model_name: str = "sentence-transformers/all-mpnet-base-v2"):
    """Lazy load embedding model with caching."""
    if model_name not in _MODEL_CACHE:
        logger.info(f"Loading embedding model: {model_name}")
        try:
            _MODEL_CACHE[model_name] = SentenceTransformer(model_name)
            logger.info(f"✓ Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    return _MODEL_CACHE[model_name]


class ExampleRetriever:
    """Retrieves semantically similar examples using FAISS vector search with caching."""

    def __init__(
        self,
        index_path: Path,
        metadata_path: Path,
        embedding_cache: Optional[Dict] = None,
    ):
        """
        Initializes the retriever with precomputed index and examples.

        Args:
            index_path: Path to FAISS index file
            metadata_path: Path to pickled metadata containing example pairs
            embedding_cache: Optional dict to cache embeddings in memory
        """
        if not Path(index_path).exists():
            raise FileNotFoundError(f"FAISS index not found: {index_path}")
        if not Path(metadata_path).exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

        # Lazy load the embedding model
        self.model = _get_embedding_model()
        self.index = faiss.read_index(str(index_path))

        with open(metadata_path, "rb") as f:
            self.examples = pickle.load(f)

        self.embedding_cache = embedding_cache or {}
        logger.info(f"Loaded {len(self.examples)} examples from retriever")

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        """
        Retrieves k most similar examples for a given query.

        Args:
            query: Natural language question to match
            k: Number of examples to retrieve (default: 3)

        Returns:
            List of example dictionaries containing question-SPARQL pairs

        Raises:
            ValueError: If k is invalid or query is empty
        """
        if not query or not isinstance(query, str):
            logger.warning(f"Invalid query: {query!r}")
            return []

        if k <= 0 or k > len(self.examples):
            logger.warning(f"Invalid k={k}, adjusting to valid range")
            k = min(k, len(self.examples))

        try:
            # Check cache first
            cache_key = f"{query}:{k}"
            if cache_key in self.embedding_cache:
                return self.embedding_cache[cache_key]

            # Encode query
            query_vec = self.model.encode([query])

            # Search with some margin to filter duplicates
            fetch_k = min(k * 3, len(self.examples))
            distances, indices = self.index.search(query_vec, fetch_k)

            results = []
            query_norm = query.strip().lower()

            for idx in indices[0]:
                if idx >= len(self.examples):
                    continue

                example = self.examples[idx]
                ex_question = example.get("question", "").strip().lower()

                # Avoid returning the exact same query
                if ex_question == query_norm:
                    continue

                # Validate example structure
                if "sparql" not in example and "query" not in example:
                    logger.debug(f"Skipping malformed example at index {idx}")
                    continue

                results.append(example)

                if len(results) >= k:
                    break

            # Cache result
            self.embedding_cache[cache_key] = results

            if not results:
                logger.warning(
                    f"No valid examples retrieved for query: {query[:50]}..."
                )

            return results

        except Exception as e:
            logger.error(f"Retriever error: {e}")
            return []

"""
Retrieval-Augmented Generation (RAG) Module.

This module retrieves semantically similar examples from a FAISS index to enhance SPARQL generation.

Features:
- Semantic similarity search using Sentence Transformers.
- Efficient retrieval from pre-built FAISS indices.

Implementation:
- Loads FAISS index and metadata from specified paths.
- Retrieves top-k similar examples based on input embeddings.
- Integrates with the `sentence_transformers` library for encoding.
"""

import logging
import pickle
from pathlib import Path

import faiss
import numpy as np
from omegaconf import DictConfig
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class RagRetriever:
    """
    Retrieval-Augmented Generation.
    Retrieves semantically similar examples from a FAISS index.
    """

    def __init__(self, config: DictConfig, rag_config: DictConfig):
        self.k = config.k
        if self.k == 0:
            logger.info("Retrieval disabled.")
            return

        index_path = Path(rag_config.index_path)
        meta_path = Path(rag_config.metadata_path)
        model_name = rag_config.encoder_model

        # Validation
        if not index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found at {index_path}. Run the indexing script first."
            )
        if not meta_path.exists():
            raise FileNotFoundError(f"Metadata file not found at {meta_path}.")

        # Load resources
        logger.info(f"Loading FAISS index from {index_path}...")
        self.index = faiss.read_index(str(index_path))

        logger.info(f"Loading metadata from {meta_path}...")
        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)

        logger.info(f"Loading SentenceTransformer model '{model_name}'...")
        self.encoder = SentenceTransformer(model_name)

    def retrieve(self, query: str) -> str:
        """
        Retrieves the top-k similar examples and formats them as a string context.
        """
        if self.k == 0:
            return ""

        try:
            # 1. Encode the query
            query_vec = self.encoder.encode([query])
            query_vec = np.array(query_vec).astype("float32")

            # 2. Search in FAISS
            faiss.normalize_L2(query_vec)
            distances, indices = self.index.search(query_vec, self.k)

            # 3. Fetch and Format Results
            examples = []
            for idx in indices[0]:
                if idx != -1 and idx < len(self.metadata):
                    item = self.metadata[idx]

                    q_text = item.get("question", "")
                    if isinstance(q_text, dict):
                        q_text = q_text.get("en", str(q_text))

                    raw_sparql = item.get("sparql", "")
                    if isinstance(raw_sparql, dict):
                        s_text = raw_sparql.get("sparql", str(raw_sparql))
                    else:
                        s_text = str(raw_sparql)

                    if q_text and s_text:
                        examples.append(
                            f"Example Question: {q_text}\nExample SPARQL: {s_text}"
                        )

            return "\n\n".join(examples)

        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return ""

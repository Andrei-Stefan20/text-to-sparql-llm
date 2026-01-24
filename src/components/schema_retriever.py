import faiss
import pickle
import numpy as np
import logging
from pathlib import Path
from omegaconf import DictConfig
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class SchemaRetriever:
    """
    Dynamic Schema Retrieval, search for relevant Wikidata properties (P-ids)
    and classes (Q-ids) based on the input question semantics.
    """
    def __init__(self, config: DictConfig):
        self.k = config.get("k_properties", 5) 
        
        index_path = Path(config.get("schema_index_path", "data/processed/schema_index.faiss"))
        meta_path = Path(config.get("schema_metadata_path", "data/processed/schema_metadata.pkl"))
        
        if not index_path.exists():
            logger.warning(f"Schema Index not found at {index_path}. Dynamic hints disabled.")
            self.enabled = False
            return

        logger.info(f"Loading Schema Index from {index_path}...")
        self.index = faiss.read_index(str(index_path))
        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)
            
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.enabled = True

    def retrieve_recommendations(self, query: str) -> str:
        if not self.enabled:
            return ""

        query_vec = self.encoder.encode([query])
        faiss.normalize_L2(query_vec)
        
        distances, indices = self.index.search(query_vec, self.k)
        
        hints = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):
                item = self.metadata[idx]
                # Esempio output: "P19 (place of birth)"
                hints.append(f"{item['id']} ({item['label']})")
        
        return ", ".join(hints)
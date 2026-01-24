import faiss
import pickle
import numpy as np
import logging
from pathlib import Path
from omegaconf import DictConfig
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class RagRetriever:
    """
    Retrieval-Augmented Generation (RAG) component.
    Retrieves semantically similar examples (Question, SPARQL) from a FAISS index.
    """

    def __init__(self, config: DictConfig, rag_config: DictConfig):
        self.k = config.k
        if self.k == 0:
            logger.info("Retrieval disabled (k=0).")
            return

        index_path = Path(rag_config.index_path)
        meta_path = Path(rag_config.metadata_path)
        model_name = rag_config.encoder_model

        # Validation
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found at {index_path}. Please run the indexing script first.")
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
            
            # 2. Search in FAISS (assuming L2 normalized index for cosine similarity)
            faiss.normalize_L2(query_vec)
            distances, indices = self.index.search(query_vec, self.k)
            
            # 3. Fetch and Format Results
            examples = []
            for idx in indices[0]:
                if idx != -1 and idx < len(self.metadata):
                    item = self.metadata[idx]
                    
                    # Adapt these keys based on your specific metadata structure
                    q_text = item.get('question', '')
                    s_text = item.get('sparql', '')
                    
                    if q_text and s_text:
                        examples.append(f"Example Question: {q_text}\nExample SPARQL: {s_text}")
            
            return "\n\n".join(examples)
            
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return ""
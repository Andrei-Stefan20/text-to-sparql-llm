import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict

class FewShotRetriever:
    """Retrieves semantically similar examples using FAISS vector search."""
    
    def __init__(self, index_path: Path, metadata_path: Path):
        """
        Initializes the retriever with precomputed index and examples.
        
        Args:
            index_path: Path to FAISS index file
            metadata_path: Path to pickled metadata containing example pairs
        """
        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        self.index = faiss.read_index(str(index_path))
        
        with open(metadata_path, "rb") as f:
            self.examples = pickle.load(f)

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        """
        Retrieves k most similar examples for a given query.
        
        Args:
            query: Natural language question to match
            k: Number of examples to retrieve
            
        Returns:
            List of example dictionaries containing question-SPARQL pairs
        """
        query_vec = self.model.encode([query])
        fetch_k = k * 2
        distances, indices = self.index.search(query_vec, fetch_k)
        
        results = []
        query_norm = query.strip().lower()

        for idx in indices[0]:
            if idx < len(self.examples):
                example = self.examples[idx]
                ex_question = example['question'].strip().lower()
                
                if ex_question != query_norm:
                    results.append(example)
                
                if len(results) >= k:
                    break
                    
        return results
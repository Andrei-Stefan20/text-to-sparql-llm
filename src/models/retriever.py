"""
src/models/retriever.py
Handles semantic search to retrieve few-shot examples using FAISS and Sentence Transformers.
"""

import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict

class FewShotRetriever:
    def __init__(self, index_path: Path, metadata_path: Path):
        """
        Initializes the retriever by loading the FAISS index and metadata.
        
        Args:
            index_path: Path to the .faiss index file.
            metadata_path: Path to the .pkl metadata file (list of dicts).
        """
        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        
        # Load FAISS index
        self.index = faiss.read_index(str(index_path))
        
        # Load metadata (actual examples)
        with open(metadata_path, "rb") as f:
            self.examples = pickle.load(f)

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        """
        Retrieves top-k similar examples for a given query.
        
        Args:
            query: The user's natural language question.
            k: Number of examples to retrieve.
            
        Returns:
            A list of dictionaries containing the examples (question + sparql).
        """
        query_vec = self.model.encode([query])
        
        # Fetch more candidates initially to filter out exact duplicates if needed
        fetch_k = k * 2
        distances, indices = self.index.search(query_vec, fetch_k)
        
        results = []
        query_norm = query.strip().lower()

        for idx in indices[0]:
            if idx < len(self.examples):
                example = self.examples[idx]
                ex_question = example['question'].strip().lower()
                
                # Simple filter: don't include the exact same question in the few-shot
                if ex_question != query_norm:
                    results.append(example)
                
                if len(results) >= k:
                    break
                    
        return results
import faiss
import pickle
from sentence_transformers import SentenceTransformer

class FewShotRetriever:
    def __init__(self, index_path, metadata_path):
        """Initializes the retriever with a pre-built FAISS index."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.read_index(str(index_path))
        with open(metadata_path, "rb") as f:
            self.examples = pickle.load(f)

    def retrieve(self, query, k=3):
        """Retrieves k most similar examples for a given query."""
        query_vec = self.model.encode([query])
        distances, indices = self.index.search(query_vec, k)
        
        results = []
        for idx in indices[0]:
            if idx < len(self.examples):
                results.append(self.examples[idx])
        return results
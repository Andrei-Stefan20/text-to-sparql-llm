import faiss
import pickle
from sentence_transformers import SentenceTransformer

class FewShotRetriever:
    def __init__(self, index_path, metadata_path):
        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        
        self.index = faiss.read_index(str(index_path))
        with open(metadata_path, "rb") as f:
            self.examples = pickle.load(f)

    def retrieve(self, query, k=3):
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
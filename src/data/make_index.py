import os
import pickle
import logging
import faiss
import numpy as np
from pathlib import Path
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROCESSED_DIR = Path("data/processed")
MODEL_NAME = "all-MiniLM-L6-v2" 

def ensure_directory(path: Path):
    if not path.exists():
        path.mkdir(parents=True)

def build_index():
    ensure_directory(PROCESSED_DIR)
    
    logger.info("Loading training dataset...")
    try:
        dataset = load_dataset("casey-martin/qald_9_plus", split="train")
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        return

    logger.info(f"Loading encoder model: {MODEL_NAME}")
    encoder = SentenceTransformer(MODEL_NAME)

    questions = []
    metadata = []

    logger.info("Processing data...")
    for row in dataset:
        en_question = None
        raw_qs = row.get("question", [])
        
        if isinstance(raw_qs, list):
            for q in raw_qs:
                if q.get("language") == "en":
                    en_question = q.get("string")
                    break
        elif isinstance(raw_qs, str):
            en_question = raw_qs

        sparql = row.get("query", {}).get("sparql", "")
        
        if en_question and sparql:
            questions.append(en_question)
            metadata.append({
                "id": str(row.get("id")),
                "question": en_question,
                "sparql": sparql
            })

    if not questions:
        logger.error("No valid data found to index.")
        return

    logger.info(f"Encoding {len(questions)} items...")
    embeddings = encoder.encode(questions, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    faiss.normalize_L2(embeddings)

    logger.info("Building FAISS index:")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    index_path = PROCESSED_DIR / "train_index.faiss"
    meta_path = PROCESSED_DIR / "train_metadata.pkl"

    logger.info("Saving artifacts...")
    faiss.write_index(index, str(index_path))
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

    logger.info("Indexing completed successfully.")

if __name__ == "__main__":
    build_index()
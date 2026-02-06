import logging
import os
import json
import pickle
import ssl
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROCESSED_DIR = Path("data/processed")
MODEL_NAME = "all-MiniLM-L6-v2"
TRAIN_JSON_PATH = Path("data/raw/QALD-10/data/qald_9_plus/qald_9_plus_train_wikidata.json")
TARGET_LANGUAGE = "en"


def ensure_directory(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


def load_local_json(path: Path, language: str = "en"):
    """Load training data from local QALD JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    questions_list = raw_data.get("questions", [])
    logger.info(f"Parsed JSON. Found {len(questions_list)} questions total.")
    
    data = []
    for item in questions_list:
        question_text = None
        
        q_translations = item.get("question", [])
        if isinstance(q_translations, list):
            for q_obj in q_translations:
                if q_obj.get("language") == language:
                    question_text = q_obj.get("string")
                    break
        elif isinstance(q_translations, str):
            question_text = q_translations
        
        if not question_text:
            continue
            
        query_obj = item.get("query", {})
        sparql_query = None
        
        if isinstance(query_obj, dict):
            sparql_query = query_obj.get("sparql")
        elif isinstance(query_obj, str):
            sparql_query = query_obj
        
        if question_text and sparql_query:
            data.append({
                "id": str(item.get("id")),
                "question": question_text,
                "sparql": sparql_query
            })
    
    return data


def build_index():
    ensure_directory(PROCESSED_DIR)

    logger.info(f"Loading training dataset from {TRAIN_JSON_PATH}...")
    
    if not TRAIN_JSON_PATH.exists():
        logger.error(f"Training file not found at {TRAIN_JSON_PATH}")
        logger.error("Please download QALD-9-plus data to data/raw/QALD-10/")
        return
    
    training_data = load_local_json(TRAIN_JSON_PATH, language=TARGET_LANGUAGE)
    logger.info(f"Loaded {len(training_data)} English question-SPARQL pairs")

    logger.info(f"Loading encoder model: {MODEL_NAME}")
    encoder = SentenceTransformer(MODEL_NAME)

    questions = [item["question"] for item in training_data]
    metadata = training_data

    if not questions:
        logger.error("No valid data found to index.")
        return

    logger.info(f"Encoding {len(questions)} items...")
    embeddings = encoder.encode(questions, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    faiss.normalize_L2(embeddings)

    logger.info(f"Building FAISS index (dim={embeddings.shape[1]})...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    index_path = PROCESSED_DIR / "train_index.faiss"
    meta_path = PROCESSED_DIR / "train_metadata.pkl"

    logger.info("Saving artifacts...")
    faiss.write_index(index, str(index_path))
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

    logger.info(f"Indexing completed. {len(questions)} examples saved to {index_path}")


if __name__ == "__main__":
    build_index()

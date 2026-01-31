import os
import pickle
import logging
import faiss
import numpy as np
import ssl
import certifi
from pathlib import Path
from datasets import load_dataset
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

    logger.info(f"Dataset loaded. Rows: {len(dataset)}")

    logger.info(f"Loading encoder model: {MODEL_NAME}")
    encoder = SentenceTransformer(MODEL_NAME)

    questions = []
    metadata = []

    logger.info("Processing data...")
    for i, row in enumerate(dataset):
        raw_qs = row.get("question")
        question = None

        if isinstance(raw_qs, str):
            question = raw_qs
        elif isinstance(raw_qs, list) and len(raw_qs) > 0:
            question = raw_qs[0]

        sparql = row.get("query.sparql")
        if not sparql:
            sparql = row.get("sparql")

        if (
            question
            and sparql
            and isinstance(question, str)
            and isinstance(sparql, str)
        ):
            questions.append(question)
            metadata.append(
                {"id": str(row.get("id", i)), "question": question, "sparql": sparql}
            )

    if not questions:
        logger.error("No valid data found to index. Check dataset structure.")
        if len(dataset) > 0:
            logger.info(f"Sample row: {dataset[0]}")
        return

    logger.info(f"Encoding {len(questions)} items...")
    embeddings = encoder.encode(questions, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    faiss.normalize_L2(embeddings)

    logger.info(f"Building FAISS index {embeddings.shape[1]}...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    index_path = PROCESSED_DIR / "train_index.faiss"
    meta_path = PROCESSED_DIR / "train_metadata.pkl"

    logger.info("Saving artifacts...")
    faiss.write_index(index, str(index_path))
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

    logger.info(f"Indexing completed successfully. Saved to {index_path}")


if __name__ == "__main__":
    build_index()

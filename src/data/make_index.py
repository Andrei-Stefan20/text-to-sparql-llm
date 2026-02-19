import os
import platform
import pickle
import logging
from pathlib import Path

# Fix per crash su macOS
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import hydra
import faiss
import numpy as np
from omegaconf import DictConfig
from sentence_transformers import SentenceTransformer
from src.data.loader import DatasetLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@hydra.main(config_path="../../conf", config_name="config", version_base=None)
def make_index(cfg: DictConfig):
    output_path = Path("data/processed")
    output_path.mkdir(parents=True, exist_ok=True)
    
    index_file = output_path / "train_index.faiss"
    metadata_file = output_path / "train_metadata.pkl"

    logger.info(f"Loading dataset: {cfg.dataset.name}")
    loader = DatasetLoader(
        dataset_name=cfg.dataset.name,
        split="train",  
        language=cfg.dataset.language,
    )
    raw_data = loader.load() # Carica lo split di train
    
    logger.info("Filtering data (English only, no DBpedia)...")
    clean_data = []
    questions_text = []

    for item in raw_data:
        # 1. Filtro SPARQL (solo Wikidata)
        sparql = item.get('query', {}).get('sparql', '')
        if "dbpedia" in sparql or "dbo:" in sparql:
            continue

        # 2. Estrazione domanda inglese
        raw_q = item.get('question', [])
        en_q = ""
        if isinstance(raw_q, list):
            en_q = next((q['string'] for q in raw_q if q.get('language') == 'en'), "")
        elif isinstance(raw_q, str):
            en_q = raw_q

        # 3. Filtro Lingua (Russo/Cinese hanno caratteri Unicode > 1000)
        if not en_q or any(ord(c) >= 1000 for c in en_q):
            continue

        clean_data.append(item)
        questions_text.append(en_q)

    logger.info(f"Filtered: {len(raw_data)} -> {len(clean_data)} items")

    # 4. Generazione Embedding (Forza CPU su Mac per stabilità)
    device = "cpu" if platform.system() == "Darwin" else "cuda"
    model = SentenceTransformer(cfg.rag.encoder_model, device=device)
    
    logger.info("Generating embeddings...")
    embeddings = model.encode(questions_text, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)

    # 5. Creazione e salvataggio indice
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    logger.info(f"Saving index to {index_file}")
    faiss.write_index(index, str(index_file))
    with open(metadata_file, "wb") as f:
        pickle.dump(clean_data, f)

    logger.info("Index generation completed successfully!")

if __name__ == "__main__":
    make_index()
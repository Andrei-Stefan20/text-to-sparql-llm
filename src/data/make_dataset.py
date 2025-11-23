import click
import logging
import json
import pickle
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from dotenv import find_dotenv, load_dotenv

logger = logging.getLogger(__name__)

def load_qald_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pairs = []
    for q in data['questions']:
        en_question = next((item['string'] for item in q['question'] if item['language'] == 'en'), None)
        sparql = q['query'].get('sparql')
        if en_question and sparql:
            pairs.append({'question': en_question, 'sparql': sparql})
    return pairs

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
def main(input_filepath, output_dir):
    logger.info('Starting dataset processing...')
    
    # 1. Load Data
    train_pairs = load_qald_json(input_filepath)
    logger.info(f"Loaded {len(train_pairs)} training pairs.")

    # 2. Generate Embeddings
    logger.info("Generating embeddings (this may take time)...")
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    questions = [p['question'] for p in train_pairs]
    embeddings = model.encode(questions, show_progress_bar=True)

    # 3. Create FAISS Index
    logger.info("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # 4. Save Artifacts
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    faiss.write_index(index, str(out_path / "train_index.faiss"))
    with open(out_path / "train_metadata.pkl", "wb") as f:
        pickle.dump(train_pairs, f)
        
    logger.info(f"Processing complete. Artifacts saved to {output_dir}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    load_dotenv(find_dotenv())
    main()
import faiss
import pickle
import logging
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
# Richiede: pip install SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROCESSED_DIR = Path("data/processed")
MODEL_NAME = "all-MiniLM-L6-v2"

def fetch_top_properties():
    """Download top Wikidata properties by usage frequency."""
    logger.info("Fetching top properties from Wikidata SPARQL Endpoint...")
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    query = """
    SELECT ?property ?propertyLabel ?count WHERE {
        {
            SELECT ?property (COUNT(?item) as ?count) WHERE {
                ?item ?property ?value .
            } GROUP BY ?property ORDER BY DESC(?count) LIMIT 1000
        }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    properties = []
    for result in results["results"]["bindings"]:
        prop_url = result["property"]["value"]
        prop_id = prop_url.split("/")[-1] # es. P31
        label = result["propertyLabel"]["value"]
        properties.append({"id": prop_id, "label": label})
        
    return properties

def build_schema_index():
    if not PROCESSED_DIR.exists():
        PROCESSED_DIR.mkdir(parents=True)

    # 1. Fetch Properties
    properties = fetch_top_properties()
    logger.info(f"Fetched {len(properties)} properties.")

    # 2. Encode Properties
    encoder = SentenceTransformer(MODEL_NAME)
    texts = [f"{p['label']} {p['id']}" for p in properties]
    
    logger.info("Encoding properties...")
    embeddings = encoder.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    faiss.normalize_L2(embeddings)

    # 3. Indexing
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    # 4. Save
    faiss.write_index(index, str(PROCESSED_DIR / "schema_index.faiss"))
    with open(PROCESSED_DIR / "schema_metadata.pkl", "wb") as f:
        pickle.dump(properties, f)
        
    logger.info("Schema Index created successfully.")

if __name__ == "__main__":
    build_schema_index()
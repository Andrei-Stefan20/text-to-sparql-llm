import faiss
import pickle
import logging
import numpy as np
import ssl
from pathlib import Path
from sentence_transformers import SentenceTransformer
from SPARQLWrapper import SPARQLWrapper, JSON

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


def is_useful_property(label, pid):
    """
    deelete properties that are likely not useful based on heuristics
    """
    label = label.lower()

    blacklist = [
        "id",
        "identifier",
        "code",
        "kennis",
        "number",
        "filmportal",
        "allociné",
        "imdb",
        "freebase",
        "gnd",
    ]
    if any(x in label.split() for x in blacklist):
        return False

    if len(label) > 50:
        return False

    return True


def fetch_and_clean_properties():
    logger.info("Fetching raw properties from Wikidata...")
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.addCustomHttpHeader("User-Agent", "TextToSparqlApp/1.0")

    query = """
    SELECT DISTINCT ?property ?propertyLabel WHERE {
        ?property a wikibase:Property .
        MINUS { ?property a wikibase:ExternalId } .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 10000
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(60)

    try:
        results = sparql.query().convert()
    except Exception as e:
        logger.error(f"Wikidata Query Failed: {e}")
        return []

    candidates = []
    for result in results["results"]["bindings"]:
        prop_url = result["property"]["value"]
        prop_id = prop_url.split("/")[-1]  # es. P31
        label = result.get("propertyLabel", {}).get("value", prop_id)

        if label == prop_id:
            continue

        try:
            pid_num = int(prop_id[1:])
        except ValueError:
            continue

        if is_useful_property(label, prop_id):
            candidates.append({"id": prop_id, "label": label, "num": pid_num})
    candidates.sort(key=lambda x: x["num"])

    top_properties = candidates[:5000]

    return [{"id": x["id"], "label": x["label"]} for x in top_properties]


def build_schema_index():
    if not PROCESSED_DIR.exists():
        PROCESSED_DIR.mkdir(parents=True)

    # 1. Fetch and Clean
    properties = fetch_and_clean_properties()

    if not properties:
        logger.error("No properties fetched. Using emergency backup.")
        properties = [
            {"id": "P31", "label": "instance of"},
            {"id": "P57", "label": "director"},
            {"id": "P161", "label": "cast member"},
        ]

    logger.info(
        f"Indexing {len(properties)} high-quality properties (Top 5: {[p['label'] for p in properties[:5]]})"
    )

    # 2. Encode
    logger.info("Encoding properties...")
    encoder = SentenceTransformer(MODEL_NAME)
    texts = [f"{p['label']} {p['id']}" for p in properties]

    embeddings = encoder.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)

    # 3. Indexing
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    # 4. Save
    faiss.write_index(index, str(PROCESSED_DIR / "schema_index.faiss"))
    with open(PROCESSED_DIR / "schema_metadata.pkl", "wb") as f:
        pickle.dump(properties, f)


if __name__ == "__main__":
    build_schema_index()

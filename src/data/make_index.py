"""
Schema Index Creation Module — Enriched Version.

Improvements over v1:
  - Fetches aliases (skos:altLabel) and descriptions (schema:description) for each property.
  - Builds a `rich_text` string combining label + description + aliases before encoding.
    This gives FAISS a much richer semantic signal and makes retrieval significantly
    more accurate (e.g. "member of parliament" → P39 "position held").
  - Saves both the index and enriched metadata (with aliases/descriptions) for inspection.

Run:
    python -m src.data.make_schema_index
    
    or for mac

    python -c "
    import torch
    torch.backends.mps.is_available = lambda: False
    import runpy
    runpy.run_module('src.data.make_schema_index', run_name='__main__')
"
"""

import logging
import os
import pickle
import platform
import ssl
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from SPARQLWrapper import JSON, SPARQLWrapper

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROCESSED_DIR = Path("data/processed")
MODEL_NAME = "all-MiniLM-L6-v2"

# How many properties to index (sorted by P-number, so smaller P-IDs = more common)
TOP_N = 5000



# Heuristic filter



def is_useful_property(label: str, pid: str) -> bool:
    """Discard identifiers, external links, and very long labels."""
    label_l = label.lower()

    blacklist_words = {
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
    }
    if any(w in label_l.split() for w in blacklist_words):
        return False

    # External identifier properties (P-IDs often have "ID" in the label)
    if "id" in label_l and len(label_l) < 10:
        return False

    if len(label) > 60:
        return False

    return True



# Fetch properties WITH aliases and descriptions



def fetch_enriched_properties() -> list:
    """
    Returns a list of dicts:
      {
        "id":          "P39",
        "label":       "position held",
        "description": "subject currently or formerly holds the object position or public office",
        "aliases":     ["office", "member of parliament", "political office"],
        "num":         39
      }
    """
    logger.info(
        "Fetching enriched properties from Wikidata (label + description + aliases)..."
    )

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.addCustomHttpHeader("User-Agent", "TextToSparqlSchemaIndexer/2.0")
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(120)

    # Fetch label + description
    query_main = """
    SELECT DISTINCT ?property ?propertyLabel ?propertyDescription WHERE {
        ?property a wikibase:Property .
        MINUS { ?property wikibase:propertyType wikibase:ExternalId . }
        SERVICE wikibase:label {
            bd:serviceParam wikibase:language "en".
        }
    }
    LIMIT 8000
    """

    sparql.setQuery(query_main)
    try:
        results = sparql.query().convert()
    except Exception as e:
        logger.error(f"Main property query failed: {e}")
        return _backup()

    props_by_pid: dict = {}
    for r in results["results"]["bindings"]:
        prop_url = r["property"]["value"]
        pid = prop_url.split("/")[-1]
        label = r.get("propertyLabel", {}).get("value", pid)
        desc = r.get("propertyDescription", {}).get("value", "")

        # Skip if label == pid (no English label available)
        if label == pid:
            continue

        try:
            num = int(pid[1:])
        except ValueError:
            continue

        if is_useful_property(label, pid):
            props_by_pid[pid] = {
                "id": pid,
                "label": label,
                "description": desc,
                "aliases": [],
                "num": num,
            }

    logger.info(f"After filtering: {len(props_by_pid)} candidate properties")

    # Sort by P-number (lower = more fundamental/common), take top N
    sorted_props = sorted(props_by_pid.values(), key=lambda x: x["num"])[:TOP_N]

 
    # Enrich with aliases 
 
    logger.info("Fetching aliases (skos:altLabel) in batches...")
    pid_list = [p["id"] for p in sorted_props]

    CHUNK = 200
    for i in range(0, len(pid_list), CHUNK):
        chunk = pid_list[i : i + CHUNK]
        values_str = " ".join(f"wd:{pid}" for pid in chunk)

        alias_query = f"""
        SELECT ?property (GROUP_CONCAT(?alias; separator="|") AS ?aliases) WHERE {{
            VALUES ?property {{ {values_str} }}
            OPTIONAL {{ ?property skos:altLabel ?alias . FILTER(LANG(?alias) = "en") }}
        }}
        GROUP BY ?property
        """

        try:
            sparql.setQuery(alias_query)
            alias_results = sparql.query().convert()

            for row in alias_results["results"]["bindings"]:
                pid = row["property"]["value"].split("/")[-1]
                alias_str = row.get("aliases", {}).get("value", "")
                aliases = [a.strip() for a in alias_str.split("|") if a.strip()]

                if pid in props_by_pid:
                    props_by_pid[pid]["aliases"] = aliases[:8]  # cap at 8

        except Exception as e:
            logger.warning(f"Alias batch {i//CHUNK + 1} failed (non-fatal): {e}")

        logger.info(f"  Aliases: {i + len(chunk)}/{len(pid_list)} processed")

    # Re-fetch enriched data in sorted order
    enriched = [props_by_pid[p["id"]] for p in sorted_props if p["id"] in props_by_pid]
    logger.info(f"Final enriched property count: {len(enriched)}")
    return enriched


def _backup() -> list:
    """Returns a minimal property set if Wikidata is unreachable."""
    return [
        {
            "id": "P31",
            "label": "instance of",
            "description": "that class of which this subject is a particular example",
            "aliases": ["is a", "type"],
            "num": 31,
        },
        {
            "id": "P57",
            "label": "director",
            "description": "director(s) of film, TV-series, stageplay, video game or similar",
            "aliases": ["film director"],
            "num": 57,
        },
        {
            "id": "P50",
            "label": "author",
            "description": "main creator(s) of a written work",
            "aliases": ["writer", "written by"],
            "num": 50,
        },
        {
            "id": "P39",
            "label": "position held",
            "description": "subject currently or formerly holds the object position or public office",
            "aliases": ["member of parliament", "political office", "office"],
            "num": 39,
        },
        {
            "id": "P112",
            "label": "founded by",
            "description": "founder or co-founder of this organization, religion or place",
            "aliases": ["co-founder", "established by"],
            "num": 112,
        },
        {
            "id": "P138",
            "label": "named after",
            "description": "entity or event that inspired the subject's name",
            "aliases": ["namesake"],
            "num": 138,
        },
        {
            "id": "P451",
            "label": "unmarried partner",
            "description": "someone with whom the person is in a relationship without being married",
            "aliases": ["companion", "partner"],
            "num": 451,
        },
        {
            "id": "P710",
            "label": "participant",
            "description": "person, group of people or organization that actively takes part in the event",
            "aliases": ["participant of", "member"],
            "num": 710,
        },
        {
            "id": "P921",
            "label": "main subject",
            "description": "primary topic of a work",
            "aliases": ["subject", "topic", "about"],
            "num": 921,
        },
        {
            "id": "P800",
            "label": "notable work",
            "description": "notable scientific, artistic or literary work, or other work of significance among subject's works",
            "aliases": ["famous work", "known for"],
            "num": 800,
        },
    ]



# Build rich text for embedding



def build_rich_text(prop: dict) -> str:
    """
    Combines label + description + aliases into a single string for embedding.

    Example output for P39:
      "position held. office or post held by subject. Aliases: office, member of parliament, political office"

    This gives the SentenceTransformer full semantic context so FAISS can match
    questions like "who is a member of the National People's Congress?" to P39.
    """
    parts = [prop["label"]]

    if prop.get("description"):
        parts.append(prop["description"])

    if prop.get("aliases"):
        alias_str = ", ".join(prop["aliases"])
        parts.append(f"Aliases: {alias_str}")

    return ". ".join(parts)



# Main



def build_schema_index():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Fetch 
    properties = fetch_enriched_properties()

    if not properties:
        logger.error("No properties fetched. Using emergency backup.")
        properties = _backup()

    logger.info(f"Indexing {len(properties)} properties.")
    logger.info(f"Sample rich_text for first 3:")
    for p in properties[:3]:
        logger.info(f"  [{p['id']}] {build_rich_text(p)}")

    # 2. Build text for each property and encode
    device = "cpu" if platform.system() == "Darwin" else "cuda"
    logger.info(f"Encoding enriched property representations (device={device})...")
    encoder = SentenceTransformer(MODEL_NAME, device=device)
    texts = [build_rich_text(p) for p in properties]

    embeddings = encoder.encode(texts, show_progress_bar=True, batch_size=256)
    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)

    # 3. Build and save FAISS index
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    index_path = PROCESSED_DIR / "schema_index.faiss"
    meta_path = PROCESSED_DIR / "schema_metadata.pkl"

    faiss.write_index(index, str(index_path))
    with open(meta_path, "wb") as f:
        pickle.dump(properties, f)

    logger.info(f"Schema index saved: {index_path} ({len(properties)} entries)")
    logger.info(f"Metadata saved:     {meta_path}")
    logger.info("Done! Re-run this script whenever you want to refresh the schema.")


if __name__ == "__main__":
    build_schema_index()

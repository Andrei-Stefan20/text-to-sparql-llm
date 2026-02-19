"""
Dynamic Schema Retrieval Module.

This module dynamically retrieves relevant Wikidata properties (P-ids) and classes (Q-ids) based on input question semantics.

Features:
- Semantic search for schema hints.
- Integration with FAISS indices for efficient retrieval.

Implementation:
- Loads schema index and metadata from specified paths.
- Retrieves top-k relevant properties and classes based on input embeddings.
- Uses `sentence_transformers` for encoding and FAISS for similarity search.
"""

import logging
import pickle
import ssl
from pathlib import Path

import faiss
import numpy as np
from omegaconf import DictConfig
from sentence_transformers import SentenceTransformer
from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)


class SchemaRetriever:
    """
    Dynamic Schema Retrieval, search for relevant Wikidata properties (P-ids)
    and classes (Q-ids) based on the input question semantics.
    """

    def __init__(self, config: DictConfig):
        self.k = config.get("k_properties", 5)

        index_path = Path(
            config.get("schema_index_path", "data/processed/schema_index.faiss")
        )
        meta_path = Path(
            config.get("schema_metadata_path", "data/processed/schema_metadata.pkl")
        )

        if not index_path.exists():
            logger.warning(
                f"Schema Index not found at {index_path}. Dynamic hints disabled."
            )
            self.enabled = False
            return

        logger.info(f"Loading Schema Index from {index_path}...")
        self.index = faiss.read_index(str(index_path))
        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)

        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.enabled = True

    def retrieve_recommendations(self, query: str) -> str:
        if not self.enabled:
            return ""

        query_vec = self.encoder.encode([query])
        faiss.normalize_L2(query_vec)

        distances, indices = self.index.search(query_vec, self.k)

        hints = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):
                item = self.metadata[idx]
                # Esempio output: "P19 (place of birth)"
                hints.append(f"{item['id']} ({item['label']})")

        return ", ".join(hints)

    def retrieve_dynamic_props(self, entities: list, limit: int = 15) -> str:
        """
        Retrieves valid properties explicitly connected to the identified entities via live SPARQL.

        This reduces hallucinations by providing the LLM with a list of properties that
        actually exist for the specific entities in the question.

        Args:
            entities: List of LinkedEntity objects.
            limit: Maximum number of properties to retrieve.

        Returns:
            A string containing a comma-separated list of properties and their labels.
        """
        if not entities:
            return ""

        # Extract QIDs (e.g., ['Q76', 'Q30'])
        qids = [e.qid for e in entities if hasattr(e, "qid") and e.qid]
        if not qids:
            return ""

        # Format for SPARQL VALUES clause
        values_str = " ".join([f"wd:{qid}" for qid in qids])

        sparql_query = f"""
        SELECT DISTINCT ?p ?pLabel (COUNT(?o) AS ?usage) WHERE {{
          VALUES ?s {{ {values_str} }}
          ?s ?p ?o .
          ?prop wikibase:directClaim ?p .
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }} GROUP BY ?p ?pLabel ORDER BY DESC(?usage) LIMIT {limit}
        """

        try:
            # Setup a dedicated wrapper for schema retrieval
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
            sparql.setReturnFormat(JSON)
            sparql.setQuery(sparql_query)
            sparql.addCustomHttpHeader("User-Agent", "TextToSparqlSchema/1.0")
            sparql.setTimeout(5)  # Short timeout to ensure pipeline speed

            # Handle SSL context if necessary
            if hasattr(ssl, "_create_unverified_context"):
                ssl._create_default_https_context = ssl._create_unverified_context

            results = sparql.query().convert()
            bindings = results.get("results", {}).get("bindings", [])

            props = []
            for b in bindings:
                p_id = b.get("p", {}).get("value", "").split("/")[-1]
                p_label = b.get("pLabel", {}).get("value", "")
                props.append(f"{p_label} ({p_id})")

            return ", ".join(props)

        except Exception as e:
            logger.warning(f"Dynamic schema retrieval failed: {e}")
            return ""

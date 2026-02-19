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
from typing import List, Optional

import faiss
import numpy as np
from omegaconf import DictConfig
from sentence_transformers import SentenceTransformer
from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)


class SchemaRetriever:
    """
    Semantic + hybrid schema retrieval for Wikidata P-IDs.

    Hybrid search:
      query = "Question: {question}. Context: {entity_names}"

    This lets FAISS find properties based on the *meaning* of the user's
    question rather than just the entity surface form. For example:

      Question: "among the founders of Tencent, who has been member of the NPC?"
      Context:  "Tencent, National People's Congress"
      → FAISS retrieves P112 (founded by), P39 (position held), P102 (member of)

    Without the question context, a search on just "Tencent" would return
    generic corporate properties (P18, P154, etc.) that are not helpful.
    """

    # Default: 10
    DEFAULT_TOP_K = 10

    def __init__(self, config: DictConfig):
        # Allow override via config; fall back to DEFAULT_TOP_K
        self.k = config.get("k_properties", self.DEFAULT_TOP_K)

        index_path = Path(
            config.get("schema_index_path", "data/processed/schema_index.faiss")
        )
        meta_path = Path(
            config.get("schema_metadata_path", "data/processed/schema_metadata.pkl")
        )

        if not index_path.exists():
            logger.warning(
                f"Schema index not found at {index_path}. "
                "Dynamic schema hints disabled. "
                "Run: python -m src.data.make_schema_index"
            )
            self.enabled = False
            return

        logger.info(f"Loading Schema Index from {index_path}...")
        self.index = faiss.read_index(str(index_path))

        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)

        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.enabled = True

        logger.info(
            f"SchemaRetriever ready: {len(self.metadata)} properties indexed, "
            f"top_k={self.k}"
        )

    
    # Public API
    

    def retrieve_recommendations(
        self,
        question: str,
        entities: Optional[List] = None,
    ) -> str:
        """
        Returns a comma-separated list of relevant Wikidata properties.

        Args:
            question: The user's natural language question.
            entities: Optional list of LinkedEntity objects (or strings).
                      Their text/labels are appended to the search context
                      so FAISS can find properties specific to those entities.

        Returns:
            e.g. "P39 (position held), P112 (founded by), P710 (participant)"
        """
        if not self.enabled or not question:
            return ""

        search_query = self._build_search_query(question, entities)

        try:
            query_vec = self.encoder.encode([search_query])
            query_vec = np.array(query_vec).astype("float32")
            faiss.normalize_L2(query_vec)

            distances, indices = self.index.search(query_vec, self.k)

            hints = []
            for idx in indices[0]:
                if idx == -1 or idx >= len(self.metadata):
                    continue
                item = self.metadata[idx]
                hint = self._format_hint(item)
                if hint:
                    hints.append(hint)

            return ", ".join(hints)

        except Exception as e:
            logger.warning(f"Schema retrieval failed: {e}")
            return ""

    # Legacy alias — keeps compatibility with code that calls the old name
    def get_hints(
        self,
        question: str,
        entities: Optional[List] = None,
    ) -> str:
        return self.retrieve_recommendations(question, entities)

    
    # Dynamic live retrieval (entity-specific, via Wikidata SPARQL)
    

    def retrieve_dynamic_props(self, entities: list, limit: int = 15) -> str:
        """
        Retrieves valid properties explicitly connected to the given entities
        via a live SPARQL call to Wikidata.

        Used when static FAISS hints are not specific enough. Disabled by
        default in the pipeline for speed — uncomment to enable.
        """
        if not entities:
            return ""

        qids = [e.qid for e in entities if hasattr(e, "qid") and e.qid]
        if not qids:
            return ""

        values_str = " ".join(f"wd:{qid}" for qid in qids)

        sparql_query = f"""
        SELECT DISTINCT ?p ?pLabel (COUNT(?o) AS ?usage) WHERE {{
          VALUES ?s {{ {values_str} }}
          ?s ?p ?o .
          ?prop wikibase:directClaim ?p .
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }} GROUP BY ?p ?pLabel ORDER BY DESC(?usage) LIMIT {limit}
        """

        try:
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
            sparql.setReturnFormat(JSON)
            sparql.setQuery(sparql_query)
            sparql.addCustomHttpHeader("User-Agent", "TextToSparqlSchema/1.0")
            sparql.setTimeout(5)

            if hasattr(ssl, "_create_unverified_context"):
                ssl._create_default_https_context = ssl._create_unverified_context

            results = sparql.query().convert()
            bindings = results.get("results", {}).get("bindings", [])

            props = []
            for b in bindings:
                p_id = b.get("p", {}).get("value", "").split("/")[-1]
                p_label = b.get("pLabel", {}).get("value", "")
                if p_id and p_label:
                    props.append(f"{p_id} ({p_label})")

            return ", ".join(props)

        except Exception as e:
            logger.warning(f"Dynamic schema retrieval failed: {e}")
            return ""

    
    # Private helpers
    

    def _build_search_query(
        self,
        question: str,
        entities: Optional[List],
    ) -> str:
        """
        Builds a hybrid search string combining question + entity names.

        Example:
          question = "among the founders of Tencent, who has been member of NPC?"
          entities = [LinkedEntity("Tencent", "Q860580"), ...]

          → "Question: among the founders of Tencent, who has been member of NPC?
             Context: Tencent, National People's Congress"

        This dramatically improves retrieval for multi-hop questions where the
        property (P39 = position held) is implicit in the question text.
        """
        parts = [f"Question: {question}"]

        if entities:
            names = []
            for e in entities:
                if hasattr(e, "text") and e.text:
                    names.append(e.text)
                elif hasattr(e, "label") and e.label:
                    names.append(e.label)
                elif isinstance(e, str):
                    names.append(e)

            if names:
                parts.append(f"Context: {', '.join(names)}")

        return ". ".join(parts)

    def _format_hint(self, item: dict) -> str:
        """
        Formats a metadata item as a human-readable hint string.

        With enriched index (v2): "P39 (position held)"
        With aliases:             "P39 (position held)" — aliases shown in description
        """
        pid = item.get("id", "")
        label = item.get("label", "")

        if not pid or not label:
            return ""

        return f"{pid} ({label})"

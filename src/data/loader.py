import logging
from typing import Any, Dict, List

from datasets import load_dataset

logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Handles loading and normalization of QALD datasets.
    Specifically optimized for 'casey-martin/qald_9_plus'.
    """

    def __init__(self, dataset_name: str, split: str = "test", language: str = "en"):
        self.dataset_name = dataset_name
        self.split = split
        self.language = language

    def load(self) -> List[Dict[str, Any]]:
        """
        Loads the dataset from HuggingFace Hub and normalizes it.
        Returns: A list of dictionaries with 'id', 'question', 'gold_sparql'.
        """
        logger.info(
            f"Downloading dataset '{self.dataset_name}' (split: {self.split})..."
        )
        try:
            ds = load_dataset(self.dataset_name, split=self.split)
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            raise

        normalized_data = []
        logger.info(f"Filtering dataset for language '{self.language}'...")

        for row in ds:
            try:
                question_text = None

                # Handle QALD multilingual structure
                # The 'question' field can be a string or a list of dicts
                raw_question = row.get("question", [])

                if isinstance(raw_question, list):
                    # Search for the specific language
                    for q in raw_question:
                        if q.get("language") == self.language:
                            question_text = q.get("string")
                            break
                elif isinstance(raw_question, str):
                    question_text = raw_question

                # Get SPARQL query
                raw_query = row.get("query", {})
                sparql_text = ""
                if isinstance(raw_query, dict):
                    sparql_text = raw_query.get("sparql", "")
                else:
                    sparql_text = str(raw_query)

                if question_text:
                    normalized_data.append(
                        {
                            "id": str(row.get("id", "unknown")),
                            "question": question_text,
                            "gold_sparql": sparql_text,
                        }
                    )
            except Exception as e:
                # Log warning but continue processing other rows
                logger.debug(f"Skipping malformed row: {e}")
                continue

        logger.info(f"Successfully loaded {len(normalized_data)} items.")
        return normalized_data

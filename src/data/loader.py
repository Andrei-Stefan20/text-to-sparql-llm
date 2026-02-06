import logging
import json
import os
import pandas as pd
from datasets import load_dataset
from huggingface_hub import hf_hub_download
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DatasetLoader:
    def __init__(self, dataset_name: str, split: str = "train", language: str = "en"):
        self.dataset_name = dataset_name
        self.split = split
        self.language = language
        
        # Map split to local file paths
        self.local_paths = {
            "train": "data/raw/QALD-10/data/qald_9_plus/qald_9_plus_train_wikidata.json",
            "test": "data/raw/QALD-10/data/qald_10/qald_10.json"
        }

    def load(self) -> List[Dict[str, Any]]:
        """
        Carica il dataset dando priorità assoluta ai file locali JSON.
        """
        logger.info(f"Loading dataset '{self.dataset_name}' (split: {self.split})...")
        
        local_path = self.local_paths.get(self.split)
        
        if local_path and os.path.exists(local_path):
            logger.info(f"Found local file at '{local_path}'. Loading directly...")
            try:
                return self._load_local_json(local_path)
            except Exception as e:
                logger.error(f"Error loading local file: {e}. Falling back to standard download...")
        else:
            logger.warning(f"Local file not found at '{local_path}'.")
            logger.warning("Please ensure you have unpacked the QALD data in 'data/raw/'.")
            logger.warning("Attempting standard Hugging Face download as fallback...")

        try:
            # Download specific parquet file directly using huggingface_hub
            # This avoids the datasets library's schema casting issues
            parquet_file = f"data/wikidata_{self.language}_train.parquet"
            logger.info(f"Downloading {parquet_file} from HuggingFace Hub...")
            
            local_parquet = hf_hub_download(
                repo_id=self.dataset_name,
                filename=parquet_file,
                repo_type="dataset"
            )
            
            # Load with pandas
            df = pd.read_parquet(local_parquet)
            logger.info(f"Loaded {len(df)} rows from parquet file")
            
            data = []
            for _, row in df.iterrows():
                question = row.get('question')
                sparql = row.get('query.sparql') or row.get('sparql') or row.get('query')
                uid = row.get('id')
                
                if question and sparql:
                    data.append({
                        "id": str(uid),
                        "question": question,
                        "gold_sparql": sparql,
                        "language": row.get('language', 'en')
                    })
            
            logger.info(f"Processed {len(data)} valid question-SPARQL pairs")
            return data
            
        except Exception as e:
            logger.critical(f"🔥 All loading methods failed. Error: {e}")
            raise e

    def _load_local_json(self, path: str) -> List[Dict[str, Any]]:
        """
        Legge e processa il file JSON locale di QALD-9-plus.
        """
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        questions_list = raw_data.get("questions", [])
        logger.info(f"Parsed JSON. Found {len(questions_list)} questions total.")
        
        processed_data = []
        
        for item in questions_list:
            question_text = None
            
            q_translations = item.get("question", [])
            if isinstance(q_translations, list):
                for q_obj in q_translations:
                    if q_obj.get("language") == self.language:
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
                processed_data.append({
                    "id": str(item.get("id")),
                    "question": question_text,
                    "gold_sparql": sparql_query,
                    "language": self.language
                })
                
        logger.info(f"Successfully processed {len(processed_data)} items for language '{self.language}'.")
        return processed_data
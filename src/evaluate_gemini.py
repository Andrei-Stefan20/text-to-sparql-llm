"""
Evaluation pipeline for Google Gemini API with few-shot learning.
Executes Text-to-SPARQL translation with iterative self-correction.
"""

import json
import sys
import os
import time
import traceback
from pathlib import Path
from typing import List

FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from src.config import config
from src.exceptions import APIError, DataError
from src.validators import validate_file_exists, validate_json_file, validate_api_key
from src.logging_config import get_logger
from src.models.generator import build_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import FewShotRetriever
from src.utils.report_manager import ReportManager
from src.utils.sparql_client import SPARQLClient

logger = get_logger(__name__)

class GeminiGenerator:
    """API wrapper for Google Gemini models."""
    
    def __init__(self, model_id: str):
        self.model_id = model_id
        api_key = os.getenv("GEMINI_API_KEY")
        
        try:
            validate_api_key(api_key, "GEMINI_API_KEY")
        except ValueError as e:
            raise APIError(str(e)) from e
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_id)

    def generate_raw(self, prompt: str, stop: List[str] = None, max_new_tokens=1024) -> str:
        """Generates text completion from Gemini API."""
        if stop is None:
            stop = config.get_stop_sequences(self.model_id)
            
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_new_tokens,
            temperature=config.model.temperature,
            stop_sequences=stop
        )
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        try:
            response = self.model.generate_content(
                prompt, 
                generation_config=generation_config, 
                safety_settings=safety_settings
            )
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text.strip()
            return ""
        except Exception as e:
            raise APIError(f"Gemini API request failed: {e}") from e

def main():
    """Main evaluation pipeline for Gemini model."""
    logger.info(">>> STARTING STANDARD GEMINI EVALUATION FEW-SHOT...")
    
    # Validate configuration
    try:
        config.validate()
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return
    
    MODEL_ID = "models/gemini-2.0-flash"
    DATA_INDEX = PROJECT_ROOT / "data/processed/train_index.faiss"
    DATA_META = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    TEST_FILE = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"
    
    try:
        validate_file_exists(DATA_INDEX, "FAISS index")
        validate_file_exists(DATA_META, "Metadata file")
        test_data = validate_json_file(TEST_FILE)
        if 'questions' not in test_data:
            raise DataError(f"Missing 'questions' key in {TEST_FILE}")
    except (FileNotFoundError, DataError) as e:
        logger.error(f"Data validation error: {e}")
        return

    retriever = FewShotRetriever(DATA_INDEX, DATA_META)
    sparql_client = SPARQLClient()
    generator = GeminiGenerator(MODEL_ID)
    reporter = ReportManager(PROJECT_ROOT, MODEL_ID.replace("/", "_"), run_prefix="gemini_std")

    SAMPLES = test_data['questions'][:100]
    logger.info(f"Testing on {len(SAMPLES)} questions.")

    for i, q_obj in enumerate(SAMPLES):
        logger.info(f"--- Processing Question {i+1}/{len(SAMPLES)} ---")
        try:
            question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
            gold_sparql = q_obj['query'].get('sparql', '')
            if not question: continue

            gold_results, _ = sparql_client.execute_remote(gold_sparql)

            examples = retriever.retrieve(question, k=config.retrieval.k_examples)
            context = extract_gold_context(gold_sparql)
            prompt = build_prompt(question, examples, context)

            MAX_RETRIES = config.model.max_retries
            best_result = None

            for attempt in range(1, MAX_RETRIES + 2):
                raw_response = generator.generate_raw(prompt, stop=["User:", "###", "Question:"])
                gen_sparql = sparql_client.clean_query(raw_response)
                
                syntax_check = sparql_client.validate_syntax_local(gen_sparql)
                results, exec_error = None, None
                error_info = {}

                if syntax_check["valid"]:
                    results, exec_error = sparql_client.execute_remote(gen_sparql)
                    if exec_error:
                        syntax_check["valid"] = False
                        error_info = {"type": "Execution Error", "detail": exec_error}
                    else:
                        best_result = (gen_sparql, raw_response, True, {}, results, attempt)
                        break
                else:
                    error_info = {"type": syntax_check["type"], "detail": syntax_check["detail"]}
                
                if attempt <= MAX_RETRIES:
                    prompt += f"\n{gen_sparql}\n```\n\nSYSTEM: Invalid Query. {error_info.get('detail')}\nFix it.\nCorrected Query: ```sparql"
                else:
                    best_result = (gen_sparql, raw_response, False, error_info, None, attempt)

            gen_sparql, raw_resp, is_valid, error_info, gen_results, attempts = best_result
            
            f1 = 0.0
            if is_valid and gen_results:
                f1 = sparql_client.calculate_f1(gold_results, gen_results)
                if f1 < 1.0 and not error_info:
                    error_info = {"type": "Wrong Answer", "detail": f"F1 Score: {f1:.2f}"}

            reporter.log_entry(question, gold_sparql, gen_sparql, raw_resp, is_valid, error_info, f1, attempts, prompt, context, gold_results, gen_results)
            
        except Exception as e:
            logger.error(f"Error processing question {i+1}: {e}")
            traceback.print_exc()

    reporter.save_final_report()

if __name__ == "__main__":
    main()
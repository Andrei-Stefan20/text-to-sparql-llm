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
from typing import List, Optional, Tuple

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
from src.models.retriever import ExampleRetriever
from src.evaluation.metrics import (
    SPARQLSyntaxMetric,
    SPARQLExecutionMetric,
    SPARQLAnswerCorrectnessMetric,
    create_test_case
)
from src.utils.sparql_client import SPARQLClient
from src.pipeline_utils import timer, BatchProcessor

logger = get_logger(__name__)

class GeminiQueryGenerator:
    """API wrapper for Google Gemini models with error handling."""
    
    def __init__(self, model_id: str, max_retries: int = 2):
        """
        Initialize Gemini generator.
        
        Args:
            model_id: Model identifier (e.g., 'models/gemini-2.0-flash')
            max_retries: Max retries for API calls
        """
        self.model_id = model_id
        self.max_retries = max_retries
        self.last_request_time = 0
        self.min_request_interval = 5.0  # 5 seconds between requests (free tier: 15/min)
        
        api_key = os.getenv("GEMINI_API_KEY")
        
        try:
            validate_api_key(api_key, "GEMINI_API_KEY")
        except ValueError as e:
            raise APIError(str(e)) from e
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_id)
        logger.info(f"Initialized {model_id}")
    
    def _rate_limit(self):
        """Rate limiting between API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def generate_raw(self, prompt: str, stop: Optional[List[str]] = None, max_new_tokens: int = 1024) -> str:
        """
        Generates text completion from Gemini API with retry logic.
        
        Args:
            prompt: Input prompt
            stop: Stop sequences
            max_new_tokens: Max output tokens
            
        Returns:
            Generated text or empty string on failure
        """
        if not prompt:
            return ""
        
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
        
        for attempt in range(1, self.max_retries + 1):
            try:
                self._rate_limit()
                
                response = self.model.generate_content(
                    prompt, 
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )
                
                if response and response.candidates and response.candidates[0].content.parts:
                    return response.candidates[0].content.parts[0].text.strip()
                return ""
            
            except Exception as e:
                error_msg = str(e)
                # Check if it's a quota error
                if "429" in error_msg or "quota" in error_msg.lower():
                    logger.error(f"Quota exceeded: {error_msg[:200]}")
                    # For quota errors, wait longer
                    if attempt < self.max_retries:
                        wait_time = 30  # Wait 30 seconds on quota errors
                        logger.warning(f"Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                    else:
                        raise APIError(f"Gemini API quota exceeded: {e}") from e
                elif attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"API request failed (attempt {attempt}), retrying in {wait_time}s: {error_msg[:80]}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"API request failed after {self.max_retries} retries: {e}")
                    raise APIError(f"Gemini API failed: {e}") from e
        
        return ""

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
    
    # Validate files
    try:
        validate_file_exists(DATA_INDEX, "FAISS index")
        validate_file_exists(DATA_META, "Metadata file")
        test_data = validate_json_file(TEST_FILE)
        if 'questions' not in test_data:
            raise DataError(f"Missing 'questions' key in {TEST_FILE}")
    except (FileNotFoundError, DataError) as e:
        logger.error(f"Data validation error: {e}")
        return

    # Initialize components
    try:
        with timer("Component initialization"):
            retriever = ExampleRetriever(DATA_INDEX, DATA_META)
            sparql_client = SPARQLClient(timeout=30)
            generator = GeminiQueryGenerator(MODEL_ID, max_retries=2)
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        return
    
    # MLflow reporter removed
    
    # Initialize metrics
    syntax_metric = SPARQLSyntaxMetric()
    execution_metric = SPARQLExecutionMetric()
    answer_metric = SPARQLAnswerCorrectnessMetric(threshold=0.8)

    SAMPLES = test_data['questions'][:10]  
    logger.info(f"Testing on {len(SAMPLES)} questions.")
    
    # Process questions
    processor = BatchProcessor(SAMPLES, batch_size=10)
    
    def process_question(q_idx_tuple):
        i, q_obj = q_idx_tuple
        try:
            question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
            gold_sparql = q_obj['query'].get('sparql', '')
            
            if not question:
                logger.warning(f"No English question found for item {i+1}")
                return
            
            # Execute gold query
            gold_results, gold_error = sparql_client.execute_remote(gold_sparql)
            if gold_error:
                logger.warning(f"Q{i+1}: Gold query failed: {gold_error}")
                gold_results = []

            # Retrieve examples
            examples = retriever.retrieve(question, k=config.retrieval.k_examples)
            context = extract_gold_context(gold_sparql)
            prompt = build_prompt(question, examples, context)

            # Generation loop with self-correction
            MAX_RETRIES = config.evaluation.max_retries
            best_result = None

            for attempt in range(1, MAX_RETRIES + 2):
                try:
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
                    
                    # Self-correction prompt
                    if attempt <= MAX_RETRIES:
                        prompt += f"\n{gen_sparql}\n```\n\nSYSTEM: Invalid Query. {error_info.get('detail')}\nFix it.\nCorrected Query: ```sparql"
                    else:
                        best_result = (gen_sparql, raw_response, False, error_info, None, attempt)
                
                except APIError as e:
                    logger.error(f"Q{i+1}, Attempt {attempt}: API error: {e}")
                    best_result = ("", "", False, {"type": "API Error", "detail": str(e)[:100]}, None, attempt)
                    break
                except Exception as e:
                    logger.error(f"Q{i+1}, Attempt {attempt}: {e}")
                    best_result = ("", "", False, {"type": type(e).__name__, "detail": str(e)[:100]}, None, attempt)
                    break

            # Log result
            if not best_result:
                logger.error(f"Q{i+1}: No result generated")
                return
            
            gen_sparql, raw_resp, is_valid, error_info, gen_results, attempts = best_result
            
            f1 = 0.0
            if is_valid and gen_results:
                f1 = sparql_client.calculate_f1(gold_results, gen_results)
                if f1 < 1.0 and not error_info:
                    error_info = {"type": "Wrong Answer", "detail": f"F1: {f1:.2f}"}
            
            # DeepEval metrics
            test_case = create_test_case(question, gen_sparql, gold_sparql, examples)
            custom_metrics = {}
            
            try:
                custom_metrics = {
                    "syntax_validity": syntax_metric.measure(test_case),
                    "execution_success": execution_metric.measure(test_case),
                    "answer_correctness": answer_metric.measure(test_case)
                }
            except Exception as e:
                logger.debug(f"Q{i+1}: DeepEval metric error: {e}")
            
            # MLflow logging removed
            
        except Exception as e:
            logger.error(f"Error processing question {i+1}: {e}")
    
    # Process all questions
    for i, q_obj in enumerate(SAMPLES):
        process_question((i, q_obj))
    
    # MLflow finalize removed

if __name__ == "__main__":
    main()
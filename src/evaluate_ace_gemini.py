"""
ACE (Automated Correction Engine) evaluation pipeline for Gemini.
Implements iterative error learning and strategy accumulation.
"""

import logging
import json
import sys
import os
import time
import traceback
from pathlib import Path

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

from src.models.generator import build_ace_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import FewShotRetriever
from src.models.ace import ACEEngine
from src.utils.report_manager import ReportManager
from src.utils.sparql_client import SPARQLClient

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] ACE: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

class GeminiGenerator:
    """API wrapper for Google Gemini with ACE integration."""
    
    def __init__(self, model_id: str):
        self.model_id = model_id
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("ERROR: GEMINI_API_KEY not found.")
            sys.exit(1)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_id)

    def generate_raw(self, prompt: str, stop=None, max_new_tokens=1024) -> str:
        """Generates text completion with disabled safety filters."""
        config = genai.types.GenerationConfig(
            max_output_tokens=max_new_tokens, 
            temperature=0.0, 
            stop_sequences=stop
        )
        safety = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        try:
            response = self.model.generate_content(prompt, generation_config=config, safety_settings=safety)
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text.strip()
            return ""
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            time.sleep(1)
            return ""

def main():
    logger.info(">>> STARTING ACE ENGINE EVALUATION...")
    
    MODEL_ID = "models/gemini-2.0-flash"
    DATA_INDEX = PROJECT_ROOT / "data/processed/train_index.faiss"
    DATA_META = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    PLAYBOOK_PATH = PROJECT_ROOT / "playbook.json"
    TEST_FILE = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"

    if not DATA_INDEX.exists():
        logger.error("Data index not found. Please run make_dataset.py")
        return

    retriever = FewShotRetriever(DATA_INDEX, DATA_META)
    sparql_client = SPARQLClient()
    generator = GeminiGenerator(MODEL_ID)
    ace_engine = ACEEngine(generator, PLAYBOOK_PATH)
    reporter = ReportManager(PROJECT_ROOT, f"ACE_{MODEL_ID.replace('/', '_')}", run_prefix="ace")

    with open(TEST_FILE, 'r') as f:
        test_data = json.load(f)['questions']
    
    SAMPLES = test_data[:20]
    logger.info(f"Current Playbook Size: {len(ace_engine.playbook)} strategies.")

    for i, q_obj in enumerate(SAMPLES):
        logger.info(f"--- Processing Question {i+1}/{len(SAMPLES)} ---")
        try:
            question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
            gold_sparql = q_obj['query'].get('sparql', '')
            if not question: continue

            # 1. Execute Gold Query (Reference)
            gold_results, _ = sparql_client.execute_remote(gold_sparql)
            
            # 2. Build Context
            examples = retriever.retrieve(question, k=3)
            context_schema = extract_gold_context(gold_sparql)

            MAX_RETRIES = 3
            best_attempt_data = None 

            # 3. Retry Loop with ACE
            for attempt in range(MAX_RETRIES):
                # A. Retrieve Strategies from ACE Playbook
                playbook_ctx = ace_engine.get_context_block()
                
                # B. Build Prompt & Generate
                prompt = build_ace_prompt(question, examples, context_schema, playbook_ctx)
                # Ensure prompt allows natural completion
                prompt_chat = prompt.replace("```sparql", "").strip() + "\n\nOutput ONLY the SPARQL query inside a code block."
                
                raw_resp = generator.generate_raw(prompt_chat, stop=["### USER QUESTION"])
                gen_sparql = sparql_client.clean_query(raw_resp)
                
                # C. Validate & Execute
                is_valid = False
                exec_results = None
                error_msg = None
                
                syntax = sparql_client.validate_syntax_local(gen_sparql)
                if syntax["valid"]:
                    exec_results, exec_err = sparql_client.execute_remote(gen_sparql)
                    if exec_err:
                        error_msg = f"Execution Error: {exec_err}"
                    elif not exec_results and gold_results: 
                         error_msg = "Query returned 0 results."
                    else:
                        is_valid = True
                else:
                    error_msg = f"Syntax Error: {syntax['detail']}"

                f1 = sparql_client.calculate_f1(gold_results, exec_results)
                
                # Save state of this attempt
                best_attempt_data = (gen_sparql, raw_resp, is_valid, error_msg, f1, prompt, playbook_ctx, exec_results)

                # D. Check Success
                if is_valid and f1 > 0:
                    logger.info(f"   [SUCCESS] Resolved at attempt {attempt+1}")
                    break 
                
                # E. ACE Intervention
                if attempt < MAX_RETRIES - 1:
                    logger.info(f"   [FAILED Attempt {attempt+1}] {error_msg}")
                    prev_len = len(ace_engine.playbook)
                    
                    # Ask ACE to create a new strategy based on the failure
                    ace_engine.curate(question, gen_sparql, error_msg or "Wrong Answer")
                    
                    if len(ace_engine.playbook) > prev_len:
                        logger.info("   >>> ACE learned a new strategy, Retrying...")

            # Log Final Result
            gen, raw, valid, err, f1, prm, ctx, res = best_attempt_data
            err_info = {"type": "Error", "detail": err} if err else None
            if valid and f1 < 1.0 and not err:
                err_info = {"type": "Wrong Answer", "detail": f"F1: {f1:.2f}"}

            reporter.log_entry(question, gold_sparql, gen, raw, valid, err_info, f1, attempt+1, prm, ctx, gold_results, res)

        except Exception as e:
            logger.error(f"Error processing question {i+1}: {e}")
            traceback.print_exc()

    # Save artifacts
    ace_engine.save_playbook()
    reporter.save_final_report()

if __name__ == "__main__":
    main()
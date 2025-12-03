import logging
import json
import sys
import os
import time
import traceback
from pathlib import Path

# --- 1. Setup Percorsi ---
FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# --- 2. Carica Variabili d'Ambiente ---
try:
    from dotenv import load_dotenv
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

# --- 3. Import ---
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from src.models.generator import build_ace_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import FewShotRetriever
from src.models.ace import ACEEngine
from src.utils.report_manager import ReportManager
from src.utils.sparql_client import SPARQLClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] ACE: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class GeminiGenerator:
    """Wrapper per l'API di Google Gemini per ACE."""
    def __init__(self, model_id: str):
        self.model_id = model_id
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("CRITICAL: GEMINI_API_KEY non trovata.")
            sys.exit(1)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_id)

    def generate_raw(self, prompt: str, stop=None, max_new_tokens=1024) -> str:
        config = genai.types.GenerationConfig(max_output_tokens=max_new_tokens, temperature=0.1, stop_sequences=stop)
        safety = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        try:
            response = self.model.generate_content(prompt, generation_config=config, safety_settings=safety)
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text.strip()
            return ""
        except Exception as e:
            logger.error(f"Errore Gemini: {e}")
            time.sleep(1)
            return ""

def main():
    logger.info(">>> AVVIO VALUTAZIONE CON ACE ENGINE...")
    
    MODEL_ID = "models/gemini-2.0-flash"
    DATA_INDEX = PROJECT_ROOT / "data/processed/train_index.faiss"
    DATA_META = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    PLAYBOOK_PATH = PROJECT_ROOT / "playbook.json"
    TEST_FILE = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"

    if not DATA_INDEX.exists():
        logger.error("Dati non trovati. Esegui make_dataset.py")
        return

    retriever = FewShotRetriever(DATA_INDEX, DATA_META)
    sparql_client = SPARQLClient()
    generator = GeminiGenerator(MODEL_ID)
    
    # Inizializza ACE Engine
    ace_engine = ACEEngine(generator, PLAYBOOK_PATH)
    reporter = ReportManager(PROJECT_ROOT, f"ACE_{MODEL_ID.replace('/', '_')}", run_prefix="ace")

    with open(TEST_FILE, 'r') as f:
        test_data = json.load(f)['questions']
    
    SAMPLES = test_data[:20]
    logger.info(f"Playbook corrente: {len(ace_engine.playbook)} strategie.")

    for i, q_obj in enumerate(SAMPLES):
        logger.info(f"--- Domanda {i+1}/{len(SAMPLES)} ---")
        try:
            question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
            gold_sparql = q_obj['query'].get('sparql', '')
            if not question: continue

            gold_results, _ = sparql_client.execute_remote(gold_sparql)
            examples = retriever.retrieve(question, k=3)
            context_schema = extract_gold_context(gold_sparql)

            MAX_RETRIES = 3
            best_attempt_data = None 

            for attempt in range(MAX_RETRIES):
                # A. Recupera Strategie ACE
                playbook_ctx = ace_engine.get_context_block()
                
                # B. Genera
                prompt = build_ace_prompt(question, examples, context_schema, playbook_ctx)
                raw_resp = generator.generate_raw(prompt, stop=["### USER QUESTION", "```\n\n"])
                gen_sparql = sparql_client.clean_query(raw_resp)
                
                # C. Valida ed Esegui
                is_valid = False
                exec_results = None
                error_msg = None
                
                syntax = sparql_client.validate_syntax_local(gen_sparql)
                if syntax["valid"]:
                    exec_results, exec_err = sparql_client.execute_remote(gen_sparql)
                    if exec_err:
                        error_msg = f"Execution Error: {exec_err}"
                    elif not exec_results and gold_results: # Sospetto zero risultati
                         error_msg = "Query returned 0 results (Logic or ID mismatch)."
                    else:
                        is_valid = True
                else:
                    error_msg = f"Syntax Error: {syntax['detail']}"

                f1 = sparql_client.calculate_f1(gold_results, exec_results)
                
                best_attempt_data = (gen_sparql, raw_resp, is_valid, error_msg, f1, prompt, playbook_ctx, exec_results)

                # D. Controllo Successo
                if is_valid and f1 > 0:
                    break # Successo!
                
                # E. Intervento ACE (Impara dall'errore)
                if attempt < MAX_RETRIES - 1:
                    logger.info(f"   [FALLITO Tentativo {attempt+1}] {error_msg}")
                    prev_len = len(ace_engine.playbook)
                    ace_engine.curate(question, gen_sparql, error_msg or "Wrong Answer")
                    if len(ace_engine.playbook) > prev_len:
                        logger.info("   >>> ACE ha imparato una nuova strategia!")

            # Log Finale
            gen, raw, valid, err, f1, prm, ctx, res = best_attempt_data
            err_info = {"type": "Error", "detail": err} if err else None
            if valid and f1 < 1.0:
                err_info = {"type": "Wrong Answer", "detail": f"F1: {f1:.2f}"}

            reporter.log_entry(question, gold_sparql, gen, raw, valid, err_info, f1, attempt+1, prm, ctx, gold_results, res)

        except Exception as e:
            logger.error(f"Errore: {e}")
            traceback.print_exc()

    ace_engine.save_playbook()
    reporter.save_final_report()

if __name__ == "__main__":
    main()
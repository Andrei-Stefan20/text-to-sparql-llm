import sys
import logging
import json
from pathlib import Path
from tqdm import tqdm

FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.evaluate import SPARQLEvaluator, ReportManager, get_model_path
from src.models.retriever import FewShotRetriever
from src.models.entities import extract_gold_context
from src.models.ace import ACEEngine
from src.models.generator import build_ace_prompt

# Configurazione Logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] ACE: %(message)s',
    datefmt='%H:%M:%S'
)

def ace_loop():
    model_path = get_model_path()
    if not model_path.exists():
        logger.error(f"Model missing at {model_path}")
        return

    index_path = PROJECT_ROOT / "data/processed/train_index.faiss"
    meta_path = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    playbook_path = PROJECT_ROOT / "playbook.json"
    
    retriever = FewShotRetriever(index_path, meta_path)
    evaluator = SPARQLEvaluator(model_path, retriever)
    ace_engine = ACEEngine(evaluator.llm, playbook_path)
    
    reporter = ReportManager(PROJECT_ROOT, f"ACE-{evaluator.model_name}")

    test_file = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)['questions']
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        return

    SAMPLES = test_data[:20] 
    logger.info(f"Starting ACE Evaluation on {len(SAMPLES)} questions.")
    logger.info(f"Initial Playbook Strategies: {len(ace_engine.playbook)}")

    for i, q_obj in enumerate(tqdm(SAMPLES)):
        question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
        gold_sparql = q_obj['query'].get('sparql', '')
        
        if not question: continue

        examples = retriever.retrieve(question, k=3)
        context_schema = extract_gold_context(gold_sparql)
        gold_results, _ = evaluator.execute_remote(gold_sparql)

        MAX_RETRIES = 3
        best_attempt_data = None 
        
        for attempt in range(MAX_RETRIES):
            playbook_ctx = ace_engine.get_context_block()
            
            prompt = build_ace_prompt(question, examples, context_schema, playbook_ctx)
            
            gen_sparql = evaluator.generate(prompt)

            is_valid = False
            execution_results = None
            error_message = None
            
            syntax_check = evaluator.validate_syntax_local(gen_sparql)
            
            if syntax_check["valid"]:
                execution_results, exec_err = evaluator.execute_remote(gen_sparql)
                if exec_err:
                    error_message = f"Execution Error: {exec_err}"
                elif not execution_results:
                    error_message = "Query returned 0 results (Logic mismatch or ID error)."
                else:
                    is_valid = True
            else:
                error_message = f"Syntax Error: {syntax_check['detail']}"

            f1 = evaluator.calculate_f1(gold_results, execution_results)
            best_attempt_data = (gen_sparql, is_valid, error_message, f1, prompt, playbook_ctx, execution_results)

            if is_valid and f1 > 0:
                if attempt > 0:
                    logger.info(f"   [SUCCESS] Fixed Q{i+1} after {attempt} retries!")
                break 

            if attempt < MAX_RETRIES - 1:
                logger.info(f"  [Attempt {attempt+1}/{MAX_RETRIES} Failed] {error_message}")
                logger.info("   Invoking ACE Curator to update Playbook...")
                
                prev_len = len(ace_engine.playbook)
                ace_engine.curate(question, gen_sparql, error_message)
                new_len = len(ace_engine.playbook)
                
                if new_len > prev_len:
                    logger.info(f"Playbook updated! Retrying")
                else:
                    logger.info(f"Curator found no new strategy. Retrying")

        gen_sparql, is_valid, error_msg, f1, prompt, ctx, results = best_attempt_data
        
        attempts_used = attempt + 1
        
        reporter.log_entry(
            question, gold_sparql, gen_sparql, is_valid,
            {"type": "Error" if error_msg else "Success", "detail": error_msg},
            f1, attempts_used, prompt, ctx, gold_results, results
        )

    ace_engine.save_playbook()
    reporter.save_final_report()
    logger.info("ACE Loop Completed.")

if __name__ == "__main__":
    ace_loop()
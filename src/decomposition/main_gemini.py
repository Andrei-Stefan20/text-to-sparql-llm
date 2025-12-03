import logging
import json
import sys
import re
import traceback
import datetime
import os
import time
from pathlib import Path
from typing import Tuple, List, Dict, Optional

# --- Setup Percorsi e Variabili d'Ambiente ---
FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[2]  

# Aggiunge la root al path per gli import
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import per la gestione variabili d'ambiente
try:
    from dotenv import load_dotenv
    # Carica esplicitamente il file .env dalla root del progetto
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"Caricate variabili d'ambiente da: {env_path}")
    else:
        print(f"ATTENZIONE: File .env non trovato in: {env_path}")
except ImportError:
    print("ERRORE CRITICO: La libreria 'python-dotenv' non è installata.")
    print("Esegui: /opt/homebrew/bin/python3.14 -m pip install python-dotenv")
    sys.exit(1)

from SPARQLWrapper import SPARQLWrapper, JSON
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Import interni
from src.models.generator import build_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import FewShotRetriever

# Configurazione Logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ReportManager:
    """Gestisce la generazione di report JSON e Markdown."""
    def __init__(self, project_root: Path, model_name: str):
        self.model_name = model_name
        self.start_time = datetime.datetime.now()
        
        date_str = self.start_time.strftime("%Y-%m-%d")
        base_report_dir = project_root / "reports" / date_str
        base_report_dir.mkdir(parents=True, exist_ok=True)
        
        existing_runs = [d for d in base_report_dir.iterdir() if d.is_dir() and d.name.startswith("run_")]
        run_id = len(existing_runs) + 1
        
        time_str = self.start_time.strftime("%H%M%S")
        self.run_dir = base_report_dir / f"run_{run_id:03d}_{time_str}"
        self.run_dir.mkdir(exist_ok=True)
        
        self.stats = {
            "meta": {"date": date_str, "model": model_name, "run_id": run_id},
            "metrics": {
                "total": 0, 
                "valid_syntax": 0, 
                "correct_answer": 0, 
                "avg_f1": 0.0, 
                "retries_successful": 0
            },
            "results": []
        }
        logger.info(f"Report directory initialized at: {self.run_dir}")

    def _format_results(self, bindings: Optional[List[Dict]]) -> List[str]:
        if not bindings:
            return []
        formatted = []
        for row in bindings:
            values = [v['value'].split('/')[-1] for v in row.values()] 
            formatted.append("(" + ", ".join(values) + ")")
        return formatted

    def log_entry(self, question: str, gold_sparql: str, generated_sparql: str, 
                  raw_response: str, is_valid: bool, error_info: dict, 
                  f1_score: float, attempts: int, prompt: str, context: str, 
                  gold_results: Optional[List], gen_results: Optional[List]):
        
        fmt_gold = self._format_results(gold_results)
        fmt_gen = self._format_results(gen_results)

        entry = {
            "id": self.stats["metrics"]["total"] + 1,
            "question": question,
            "status": "VALID" if is_valid else "INVALID",
            "error_type": error_info.get("type") if error_info else None,
            "error_detail": error_info.get("detail") if error_info else None,
            "metrics": {"f1_score": f1_score, "attempts_needed": attempts},
            "queries": {
                "gold": gold_sparql, 
                "generated": generated_sparql,
                "raw_response": raw_response 
            },
            "execution": {
                "gold_count": len(fmt_gold),
                "gen_count": len(fmt_gen),
                "gold_data": fmt_gold,
                "gen_data": fmt_gen
            },
            "debug": {"prompt": prompt, "context": context}
        }
        self.stats["results"].append(entry)
        
        # Update metrics
        m = self.stats["metrics"]
        m["total"] += 1
        if is_valid: m["valid_syntax"] += 1
        if f1_score == 1.0: m["correct_answer"] += 1
        if attempts > 1 and is_valid: m["retries_successful"] += 1
        
        if m["total"] > 0:
            total_f1 = sum(r['metrics']['f1_score'] for r in self.stats['results'])
            m["avg_f1"] = round(total_f1 / m["total"], 4)
            
        self._flush_to_disk()

    def _flush_to_disk(self):
        try:
            with open(self.run_dir / "results.json", "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
            
            with open(self.run_dir / "report.md", "w", encoding="utf-8") as f:
                self._write_markdown(f)
        except Exception as e:
            logger.error(f"Failed to save report: {e}")

    def _write_markdown(self, f):
        m = self.stats['metrics']
        total = m['total']
        syn_acc = (m['valid_syntax'] / total * 100) if total > 0 else 0
        ans_acc = (m['correct_answer'] / total * 100) if total > 0 else 0
        
        f.write(f"# Text-to-SPARQL Evaluation Report (Gemini)\n\n")
        f.write(f"**Model:** `{self.model_name}`\n")
        f.write(f"**Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary Metrics\n")
        f.write(f"| Metric | Value |\n|---|---|\n")
        f.write(f"| Total Questions | {total} |\n")
        f.write(f"| Syntax Accuracy | {syn_acc:.2f}% |\n")
        f.write(f"| Answer Accuracy | {ans_acc:.2f}% |\n")
        f.write(f"| Average F1 Score | {m['avg_f1']:.4f} |\n")
        f.write(f"| Successful Retries | {m['retries_successful']} |\n\n")
        f.write("---\n\n")
        
        f.write("## Detailed Results\n\n")
        for item in reversed(self.stats["results"]):
            status_icon = "[PASS]" if item["metrics"]["f1_score"] == 1.0 else ("[FAIL]" if not item["status"] == "VALID" else "[PARTIAL]")
            f.write(f"### Q{item['id']}: {status_icon} {item['question']}\n\n")
            if item["error_type"]:
                f.write(f"**Error:** `{item['error_type']}: {item['error_detail']}`\n\n")
            f.write("#### 1. SPARQL Query Comparison\n")
            f.write(f"**Generated:**\n```sparql\n{item['queries']['generated']}\n```\n")
            f.write(f"**Gold:**\n```sparql\n{item['queries']['gold']}\n```\n\n")
            f.write(f"**F1 Score:** {item['metrics']['f1_score']:.2f} | **Attempts:** {item['metrics']['attempts_needed']}\n")
            f.write("---\n")

    def save_final_report(self):
        self._flush_to_disk()
        logger.info(f"Final report saved to {self.run_dir}")

class SPARQLEvaluator:
    def __init__(self, model_id: str, retriever: FewShotRetriever):
        self.retriever = retriever
        self.endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", "TextToSparqlBot/1.0 (GeminiEval)")
        self.endpoint.setTimeout(60)
        
        self.model_name = model_id
        
        # Configurazione Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY mancante! Controlla il file .env nella root del progetto.")
            sys.exit(1)
            
        genai.configure(api_key=api_key)
        logger.info(f"Initializing Gemini Model: {model_id}")
        self.model = genai.GenerativeModel(model_id)

    def _clean_query(self, query_text: str) -> str:
        q = query_text.strip()
        q = q.replace("```sparql", "").replace("```", "").strip()
        q = re.sub(r'PREF[A-Z]*\s', 'PREFIX ', q, flags=re.IGNORECASE)
        q = re.sub(r'wd:\?(\w+)', r'?\1', q)
        return q

    def generate_raw(self, prompt: str, stop: Optional[List[str]] = None, max_new_tokens=512) -> str:
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_new_tokens,
            temperature=0.1,
            stop_sequences=stop
        )
        # Disabilita filtri di sicurezza per evitare falsi positivi su codice
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
            if response.text:
                return response.text.strip()
            else:
                logger.warning("Gemini ha restituito una risposta vuota.")
                return ""
        except Exception as e:
            logger.error(f"Errore generazione Gemini: {e}")
            time.sleep(2)
            return ""

    def generate(self, prompt: str) -> Tuple[str, str]:
        raw = self.generate_raw(prompt, stop=["User:", "###", "Question:"])
        return self._clean_query(raw), raw

    def validate_syntax_local(self, query: str) -> dict:
        error_info = {"valid": True, "type": None, "detail": None}
        try:
            from rdflib.plugins.sparql.parser import parseQuery
            from pyparsing import ParseException
            parseQuery(query)
        except ImportError:
            pass
        except ParseException as e:
            error_info["valid"] = False
            error_info["type"] = "Syntax Error"
            error_info["detail"] = f"Line {e.lineno}, Col {e.col}: Expected {e.msg}"
        except Exception as e:
            error_info["valid"] = False
            error_info["type"] = "Parsing Error"
            error_info["detail"] = str(e)
        return error_info

    def execute_remote(self, query: str) -> Tuple[Optional[List], Optional[str]]:
        try:
            self.endpoint.setQuery(query)
            results = self.endpoint.query().convert()
            return results['results']['bindings'], None
        except Exception as e:
            return None, str(e).split('\n')[0]

    def calculate_f1(self, gold_results: List, gen_results: List) -> float:
        if not gold_results and not gen_results: return 1.0
        if not gold_results or not gen_results: return 0.0
        
        def get_vals(bindings):
            return {tuple(sorted(v['value'] for v in r.values())) for r in bindings}

        g_set = get_vals(gold_results)
        p_set = get_vals(gen_results)
        
        tp = len(g_set & p_set)
        if tp == 0: return 0.0
        precision = tp / len(p_set)
        recall = tp / len(g_set)
        return 2 * (precision * recall) / (precision + recall)

    def generate_smart(self, question: str, gold_sparql: str, max_retries=3):
        examples = self.retriever.retrieve(question, k=3)
        context = extract_gold_context(gold_sparql)
        prompt = build_prompt(question, examples, context)
        
        for attempt in range(1, max_retries + 2):
            if attempt > 1:
                logger.info(f"   Retry attempt {attempt-1}...")

            gen_sparql, raw_response = self.generate(prompt)
            syntax_check = self.validate_syntax_local(gen_sparql)
            
            results = None
            exec_error = None
            error_info = {}
            
            if syntax_check["valid"]:
                results, exec_error = self.execute_remote(gen_sparql)
                if exec_error:
                    syntax_check["valid"] = False
                    error_info = {"type": "Execution Error", "detail": exec_error}
                else:
                    return gen_sparql, raw_response, results, True, {}, attempt, prompt, context
            else:
                error_info = {"type": syntax_check["type"], "detail": syntax_check["detail"]}

            if attempt <= max_retries:
                prompt += f"\n{gen_sparql}\n```\n\nSYSTEM: Invalid Query. {error_info.get('detail')}\nFix it.\nCorrected Query: ```sparql"
            else:
                return gen_sparql, raw_response, None, False, error_info, attempt, prompt, context

def get_model_id():
    # Usa il nome corretto per l'API attuale
    return "models/gemini-2.0-flash"

def main():
    model_id = get_model_id()

    index_path = PROJECT_ROOT / "data/processed/train_index.faiss"
    meta_path = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    
    if not index_path.exists():
        logger.error(f"Index not found at {index_path}. Run 'make_dataset.py' first.")
        return

    retriever = FewShotRetriever(index_path, meta_path)
    evaluator = SPARQLEvaluator(model_id, retriever)
    reporter = ReportManager(PROJECT_ROOT, f"gemini_{model_id}")

    test_file = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)['questions']
    except Exception as e:
        logger.error(f"Failed to load test data: {e}")
        return

    SAMPLES = test_data[:20] 
    total_q = len(SAMPLES)
    
    logger.info(f"Starting evaluation on {total_q} questions using Gemini...")

    for i, q_obj in enumerate(SAMPLES):
        logger.info(f"Processing Question {i+1}/{total_q}")
        try:
            question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
            gold_sparql = q_obj['query'].get('sparql', '')
            if not question: continue
            
            gold_results, _ = evaluator.execute_remote(gold_sparql)
            gen_sparql, raw_resp, gen_results, is_valid, error_info, attempts, prompt, ctx = evaluator.generate_smart(question, gold_sparql, max_retries=3)
            
            f1 = 0.0
            if is_valid and gen_results:
                f1 = evaluator.calculate_f1(gold_results, gen_results)
                if f1 < 1.0:
                    error_info = {"type": "Wrong Answer", "detail": f"F1 Score: {f1:.2f}"}
            
            reporter.log_entry(question, gold_sparql, gen_sparql, raw_resp, is_valid, error_info, f1, attempts, prompt, ctx, gold_results, gen_results)
        except Exception as e:
            logger.error(f"Error processing question {i+1}: {e}")
            traceback.print_exc()
            continue

    reporter.save_final_report()

if __name__ == "__main__":
    main()
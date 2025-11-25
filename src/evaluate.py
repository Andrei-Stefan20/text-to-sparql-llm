import logging
import json
import sys
import re
import traceback
import pickle
import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Optional
from tqdm import tqdm

FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from SPARQLWrapper import SPARQLWrapper, JSON

try:
    from rdflib.plugins.sparql.parser import parseQuery
    from pyparsing import ParseException
    HAS_RDFLIB = True
except ImportError:
    HAS_RDFLIB = False

try:
    from llama_cpp import Llama, LlamaGrammar
except ImportError:
    Llama = None
    LlamaGrammar = None

# Import interni
from src.models.generator import build_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import FewShotRetriever

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)

class ReportManager:
    """
    - Cartelle: reports/YYYY-MM-DD/run_XXX/
    - File: results.json  e report.md 
    """
    def __init__(self, project_root: Path, model_name: str):
        self.model_name = model_name
        self.start_time = datetime.datetime.now()
        
        # Struttura cartelle: reports/DATA/run_ID
        date_str = self.start_time.strftime("%Y-%m-%d")
        base_report_dir = project_root / "reports" / date_str
        base_report_dir.mkdir(parents=True, exist_ok=True)
        
        existing_runs = [d for d in base_report_dir.iterdir() if d.is_dir() and d.name.startswith("run_")]
        run_id = len(existing_runs) + 1
        
        time_str = self.start_time.strftime("%H%M%S")
        self.run_dir = base_report_dir / f"run_{run_id:03d}_{time_str}"
        self.run_dir.mkdir(exist_ok=True)
        
        # Struttura Dati Originale
        self.stats = {
            "meta": {"date": date_str, "model": model_name, "run_id": run_id},
            "metrics": {
                "total": 0, "valid_syntax": 0, "correct_answer": 0, 
                "avg_f1": 0.0, "retries_successful": 0
            },
            "results": []
        }
        logger.info(f"Report directory initialized: {self.run_dir}")

    def format_results_preview(self, results: Optional[List[Dict]]) -> str:
        if not results: return "No results"
        flat_values = []
        for row in results:
            vals = [v['value'] for v in row.values()]
            flat_values.append(", ".join(vals))
        count = len(flat_values)
        preview = "; ".join(flat_values[:3])
        if count > 3: preview += f" ... ({count - 3} more)"
        return f"[{count} items] {preview}"

    def log_entry(self, question: str, gold_sparql: str, generated_sparql: str, 
                  is_valid: bool, error_info: dict, f1_score: float, 
                  attempts: int, history: str, context: str,
                  gold_results: Optional[List], gen_results: Optional[List]):
        
        gold_preview = self.format_results_preview(gold_results)
        gen_preview = self.format_results_preview(gen_results)

        entry = {
            "id": self.stats["metrics"]["total"] + 1,
            "question": question,
            "status": "VALID" if is_valid else "INVALID",
            "error_type": error_info.get("type") if error_info else None,
            "error_detail": error_info.get("detail") if error_info else None,
            "metrics": {"f1_score": f1_score, "attempts_needed": attempts},
            "queries": {"gold": gold_sparql, "generated": generated_sparql},
            "results_preview": {"gold": gold_preview, "generated": gen_preview},
            "debug": {"history": history, "context": context}
        }
        self.stats["results"].append(entry)
        
        # Aggiornamento Metriche
        m = self.stats["metrics"]
        m["total"] += 1
        if is_valid: m["valid_syntax"] += 1
        if f1_score == 1.0: m["correct_answer"] += 1
        if attempts > 1 and is_valid: m["retries_successful"] += 1
        
        total_f1 = sum(r['metrics']['f1_score'] for r in self.stats['results'])
        m["avg_f1"] = round(total_f1 / m["total"], 4)
            
        self._flush_to_disk()

    def _flush_to_disk(self):
        # Salva JSON
        with open(self.run_dir / "results.json", "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        # Salva Markdown
        with open(self.run_dir / "report.md", "w", encoding="utf-8") as f:
            self._write_markdown(f)

    def _write_markdown(self, f):
        m = self.stats['metrics']
        total = m['total']
        syn_acc = (m['valid_syntax'] / total * 100) if total > 0 else 0
        ans_acc = (m['correct_answer'] / total * 100) if total > 0 else 0
        
        f.write(f"# Text-to-SPARQL Report\n\n")
        f.write(f"**Model:** `{self.model_name}`\n")
        f.write(f"**Date:** {self.stats['meta']['date']}\n\n")
        f.write(f"| Metric | Value |\n|---|---|\n")
        f.write(f"| Syntax Accuracy | {syn_acc:.2f}% |\n")
        f.write(f"| Answer Accuracy | {ans_acc:.2f}% |\n")
        f.write(f"| Avg F1 Score | {m['avg_f1']:.4f} |\n")
        f.write(f"| Self-Corrections | {m['retries_successful']} |\n\n")
        f.write("---\n\n")
        
        for item in self.stats["results"]:
            status = "CORRECT" if item["metrics"]["f1_score"] == 1.0 else ("WRONG ANS" if item["status"] == "VALID" else "SYNTAX ERR")
            f.write(f"### Q{item['id']}: {status}\n")
            f.write(f"**Input:** {item['question']}\n\n")
            
            if item["error_type"]:
                f.write(f"> **Error:** `{item['error_type']}: {item['error_detail']}`\n\n")
            
            f.write("| Gold Query | Generated Query |\n|---|---|\n")
            g = item['queries']['gold'].replace('|', '\|').replace('\n', ' ')
            p = item['queries']['generated'].replace('|', '\|').replace('\n', ' ')
            f.write(f"| `{g}` | `{p}` |\n\n")
            
            f.write("#### Execution Results\n")
            f.write(f"- **Gold:** `{item['results_preview']['gold']}`\n")
            f.write(f"- **Gen:** `{item['results_preview']['generated']}`\n\n")
            
            f.write(f"**F1:** {item['metrics']['f1_score']:.2f} | **Attempts:** {item['metrics']['attempts_needed']}\n")
            
            f.write("<details><summary>Debug Info</summary>\n\n")
            f.write(f"**Context:**\n```text\n{item['debug']['context']}\n```\n\n")
            f.write(f"**History (Prompt):**\n````text\n{item['debug']['history']}\n````\n")
            f.write("</details>\n\n---\n")

    def save_final_report(self):
        # Alias per compatibilità, flusha un'ultima volta
        self._flush_to_disk()
        logger.info(f"Final report saved to {self.run_dir}")

class SPARQLEvaluator:
    def __init__(self, model_path: Path, retriever: FewShotRetriever):
        self.retriever = retriever
        self.endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", "TextToSparqlBot/1.0")
        self.endpoint.setTimeout(60)
        
        import torch
        n_gpu = -1 if torch.cuda.is_available() else 0
        
        self.grammar = None
        self.model_name = "MOCK_MODEL"
        
        if Llama and model_path.exists():
            logger.info(f"Loading Model: {model_path.name}")
            self.model_name = model_path.name
            try:
                grammar_path = PROJECT_ROOT / "sparql_grammar.gbnf"
                if grammar_path.exists():
                    logger.info(f"Loading Grammar from: {grammar_path}")
                    self.grammar = LlamaGrammar.from_file(str(grammar_path))
                else:
                    logger.warning(f"Grammar file not found at {grammar_path}. Unconstrained generation.")
            except Exception as e:
                logger.error(f"Error loading grammar: {e}")

            self.llm = Llama(
                model_path=str(model_path),
                n_ctx=4096,
                n_gpu_layers=n_gpu, 
                verbose=False
            )
        else:
            logger.warning("Model file not found or Llama package missing. Using MOCK mode.")
            self.llm = None

    def _clean_query(self, query_text: str) -> str:
        q = query_text.strip()
        q = q.replace("```sparql", "").replace("```", "").strip()
        q = re.sub(r'PREF[A-Z]*\s', 'PREFIX ', q, flags=re.IGNORECASE)
        q = re.sub(r'wd:\?(\w+)', r'?\1', q)
        return q

    def generate(self, prompt: str) -> str:
        if not self.llm: return ""
        try:
            output = self.llm(
                prompt, 
                grammar=self.grammar,
                max_tokens=256, 
                stop=["User:", "```", "###"],
                echo=False,
                temperature=0.1 
            )
            raw_text = output['choices'][0]['text']
            return self._clean_query(raw_text)
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return ""

    def validate_syntax_local(self, query: str) -> dict:
        error_info = {"valid": True, "type": None, "detail": None}
        if not HAS_RDFLIB: return error_info
        try:
            parseQuery(query)
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

    def generate_smart(self, question: str, gold_sparql: str, max_retries=5):
        # 1. Retrieval
        examples = self.retriever.retrieve(question, k=3)
        context = extract_gold_context(gold_sparql)
        
        # 2. Prompting (Usa la funzione esterna)
        prompt = build_prompt(question, examples, context)
        
        # 3. Generation Loop
        for attempt in range(1, max_retries + 2):
            gen_sparql = self.generate(prompt)
            
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
                    return gen_sparql, results, True, {}, attempt, prompt, context
            else:
                error_info = {"type": syntax_check["type"], "detail": syntax_check["detail"]}

            if attempt <= max_retries:
                logger.info(f"   -> Retry {attempt}: {error_info.get('type')}")
                prompt += f"\n{gen_sparql}\n```\n\n"
                prompt += f"SYSTEM: Invalid Query. {error_info.get('detail')}\nFix it.\n"
                prompt += f"Corrected Query: ```sparql"
            else:
                return gen_sparql, None, False, error_info, attempt, prompt, context

def get_model_path():
    REPO_FILE = "qwen2.5-coder-7b-instruct-q5_k_m.gguf"
    dest = Path.home() / "Desktop" / "models" / REPO_FILE
    return dest

def main():
    if not HAS_RDFLIB:
        logger.warning("rdflib missing. Install 'rdflib' for local syntax check.")

    model_path = get_model_path()
    if not model_path.exists():
        logger.error(f"MODEL NOT FOUND: {model_path}")
        logger.error("Please download the model or update get_model_path() in src/evaluate.py")
        return

    index_path = PROJECT_ROOT / "data/processed/train_index.faiss"
    meta_path = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    
    if not index_path.exists():
        logger.error(f"Index missing at {index_path}. Run 'python src/data/make_dataset.py ...'")
        return

    retriever = FewShotRetriever(index_path, meta_path)
    evaluator = SPARQLEvaluator(model_path, retriever)
    reporter = ReportManager(PROJECT_ROOT, evaluator.model_name)

    test_file = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)['questions']
    except Exception as e:
        logger.error(f"Failed to load test data: {e}")
        return

    SAMPLES = test_data[:20] 
    logger.info(f"Starting evaluation on {len(SAMPLES)} questions...")

    for q_obj in tqdm(SAMPLES):
        try:
            question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
            gold_sparql = q_obj['query'].get('sparql', '')
            
            if not question: continue
            
            gold_results, _ = evaluator.execute_remote(gold_sparql)
            gen_sparql, gen_results, is_valid, error_info, attempts, prompt, ctx = evaluator.generate_smart(question, gold_sparql, max_retries=5)
            
            f1 = 0.0
            if is_valid and gen_results:
                f1 = evaluator.calculate_f1(gold_results, gen_results)
                if f1 < 1.0:
                    error_info = {"type": "Wrong Answer", "detail": f"F1 Score: {f1:.2f}"}
            
            reporter.log_entry(question, gold_sparql, gen_sparql, is_valid, error_info, f1, attempts, prompt, ctx, gold_results, gen_results)
            
        except Exception as e:
            logger.error(f"Critical Loop Error: {e}")
            traceback.print_exc()
            continue

    reporter.save_final_report()

if __name__ == "__main__":
    main()
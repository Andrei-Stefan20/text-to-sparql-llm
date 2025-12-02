import logging
import json
import sys
import re
import traceback
import datetime
import torch
from pathlib import Path
from typing import Tuple, List, Dict, Optional

FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from SPARQLWrapper import SPARQLWrapper, JSON
from transformers import AutoModelForCausalLM, AutoTokenizer

# Internal imports
from src.models.generator import build_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import FewShotRetriever

# Configure Logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ReportManager:
    """
    Manages the generation of JSON and Markdown reports.
    """
    def __init__(self, project_root: Path, model_name: str):
        self.model_name = model_name
        self.start_time = datetime.datetime.now()
        
        # Directory structure: reports/YYYY-MM-DD/run_ID
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
        """Converts complex SPARQL bindings to a simple list of strings."""
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
        
        f.write(f"# Text-to-SPARQL Evaluation Report\n\n")
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
            
            # --- SPARQL Comparison ---
            f.write("#### 1. SPARQL Query Comparison\n")
            f.write(f"**Generated:**\n```sparql\n{item['queries']['generated']}\n```\n")
            f.write(f"**Gold:**\n```sparql\n{item['queries']['gold']}\n```\n\n")

            # --- Execution Results Comparison ---
            gold_count = item['execution']['gold_count']
            gen_count = item['execution']['gen_count']
            gold_preview = ", ".join(item['execution']['gold_data'][:5])
            gen_preview = ", ".join(item['execution']['gen_data'][:5])
            
            if len(item['execution']['gold_data']) > 5: gold_preview += "..."
            if len(item['execution']['gen_data']) > 5: gen_preview += "..."

            f.write("#### 2. Execution Data (Real-world results)\n")
            f.write("| Source | Count | Data Preview |\n|---|---|---|\n")
            f.write(f"| **Gold** | {gold_count} | `{gold_preview}` |\n")
            f.write(f"| **Gen** | {gen_count} | `{gen_preview}` |\n\n")
            
            # --- Expandable Details ---
            f.write("<details>\n<summary><b>View Full Prompt, Raw Response and Full Data</b></summary>\n\n")
            
            if gold_count > 5 or gen_count > 5:
                f.write("**Full Gold Results:**\n`" + str(item['execution']['gold_data']) + "`\n\n")
                f.write("**Full Gen Results:**\n`" + str(item['execution']['gen_data']) + "`\n\n")

            f.write("**Full Prompt Sent to Model:**\n```text\n")
            f.write(item['debug']['prompt'])
            f.write("\n```\n\n")
            
            f.write("**Raw Model Response (Uncleaned):**\n```text\n")
            f.write(item['queries']['raw_response'])
            f.write("\n```\n")
            f.write("</details>\n\n")
            
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
        self.endpoint.addCustomHttpHeader("User-Agent", "TextToSparqlBot/1.0")
        self.endpoint.setTimeout(60)
        
        self.model_name = model_id
        
        logger.info(f"Initializing Model: {model_id}")
        
        # Hardware Optimization for my RTX 4060
        attn_impl = "eager"
        try:
            import flash_attn
            attn_impl = "flash_attention_2"
            logger.info("Optimization: Flash Attention 2 enabled.")
        except ImportError:
            attn_impl = "sdpa" 
            logger.info("Optimization: Flash Attention 2 not found. Using SDPA.")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, 
                torch_dtype=torch.float16, 
                device_map="auto",
                attn_implementation=attn_impl
            )
            self.model.eval()
            
            if torch.cuda.is_available():
                logger.info("Compiling model with torch.compile (this may take a minute)...")
                try:
                    self.model = torch.compile(self.model)
                except Exception as e:
                    logger.warning(f"Compilation failed (continuing without it): {e}")
            
        except Exception as e:
            logger.error(f"Critical Error loading model: {e}")
            sys.exit(1)

    def _clean_query(self, query_text: str) -> str:
        q = query_text.strip()
        q = q.replace("```sparql", "").replace("```", "").strip()
        q = re.sub(r'PREF[A-Z]*\s', 'PREFIX ', q, flags=re.IGNORECASE)
        q = re.sub(r'wd:\?(\w+)', r'?\1', q)
        return q

    def generate_raw(self, prompt: str, stop: Optional[List[str]] = None, max_new_tokens=512) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if prompt in full_text:
            generated_text = full_text.split(prompt)[-1]
        else:
            generated_text = full_text[len(prompt):]
            
        if stop:
            for s in stop:
                if s in generated_text:
                    generated_text = generated_text.split(s)[0]
                    
        return generated_text.strip()

    def generate(self, prompt: str) -> Tuple[str, str]:
        raw = self.generate_raw(prompt, stop=["User:", "```", "###", "Question:"])
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
        last_raw_response = ""

        for attempt in range(1, max_retries + 2):
            if attempt > 1:
                logger.info(f"   Retry attempt {attempt-1}...")

            gen_sparql, raw_response = self.generate(prompt)
            last_raw_response = raw_response
            
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
                prompt += f"\n{gen_sparql}\n```\n\n"
                prompt += f"SYSTEM: Invalid Query. {error_info.get('detail')}\nFix it.\n"
                prompt += f"Corrected Query: ```sparql"
            else:
                return gen_sparql, raw_response, None, False, error_info, attempt, prompt, context

def get_model_id():
    return "Qwen/Qwen2.5-Coder-3B-Instruct"

def main():
    model_id = get_model_id()

    index_path = PROJECT_ROOT / "data/processed/train_index.faiss"
    meta_path = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    
    if not index_path.exists():
        logger.error(f"Index not found at {index_path}. Run 'make_dataset.py' first.")
        return

    retriever = FewShotRetriever(index_path, meta_path)
    evaluator = SPARQLEvaluator(model_id, retriever)
    reporter = ReportManager(PROJECT_ROOT, evaluator.model_name.replace("/", "_"))

    test_file = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)['questions']
    except Exception as e:
        logger.error(f"Failed to load test data: {e}")
        return

    SAMPLES = test_data[:20] 
    total_q = len(SAMPLES)
    
    logger.info(f"Starting evaluation on {total_q} questions...")

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
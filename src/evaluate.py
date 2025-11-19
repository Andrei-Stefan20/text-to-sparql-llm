import sys
import json
import logging
import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Optional
from tqdm import tqdm
from SPARQLWrapper import SPARQLWrapper, JSON
from huggingface_hub import hf_hub_download

# --- GESTIONE PERCORSI ---
FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.models.retriever import FewShotRetriever
from src.models.entities import extract_context

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("EVAL")

class ReportManager:
    def __init__(self, project_root: Path, model_name: str):
        self.start_time = datetime.datetime.now()
        self.model_name = model_name
        
        date_str = self.start_time.strftime("%Y-%m-%d")
        base_report_dir = project_root / "reports" / date_str
        base_report_dir.mkdir(parents=True, exist_ok=True)
        
        existing_runs = [d for d in base_report_dir.iterdir() if d.is_dir() and d.name.startswith("run_")]
        run_id = 1
        if existing_runs:
            try:
                ids = [int(d.name.split("_")[1]) for d in existing_runs]
                run_id = max(ids) + 1
            except ValueError: pass 

        time_str = self.start_time.strftime("%H%M%S")
        self.run_dir = base_report_dir / f"run_{run_id:03d}_{time_str}"
        self.run_dir.mkdir(exist_ok=True)
        
        self.stats = {
            "meta": {"date": date_str, "model": model_name, "run_id": run_id},
            "metrics": {"total": 0, "valid": 0, "accuracy": 0.0},
            "results": []
        }
        logger.info(f"Report directory: {self.run_dir}")

    def log_entry(self, question: str, gold: str, generated: str, is_valid: bool, error: str, context: str, examples: List[Dict], prompt: str):
        entry = {
            "id": self.stats["metrics"]["total"] + 1,
            "question": question,
            "status": "VALID" if is_valid else "INVALID",
            "sparql_gold": gold,
            "sparql_gen": generated,
            "error_message": error,
            "retrieved_context": context,
            "retrieved_examples": examples,
            "full_prompt": prompt
        }
        self.stats["results"].append(entry)
        self.stats["metrics"]["total"] += 1
        if is_valid:
            self.stats["metrics"]["valid"] += 1
        
        if self.stats["metrics"]["total"] > 0:
            self.stats["metrics"]["accuracy"] = round(self.stats["metrics"]["valid"] / self.stats["metrics"]["total"], 4)
            
        self._flush_to_disk()

    def _flush_to_disk(self):
        with open(self.run_dir / "results.json", "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        with open(self.run_dir / "report.md", "w", encoding="utf-8") as f:
            self._write_markdown(f)

    def _write_markdown(self, f):
        acc_perc = self.stats['metrics']['accuracy'] * 100
        f.write(f"# Text-to-SPARQL Evaluation Report\n\n")
        f.write(f"- **Model:** `{self.model_name}`\n")
        f.write(f"- **Accuracy:** **{acc_perc:.2f}%** ({self.stats['metrics']['valid']}/{self.stats['metrics']['total']})\n\n")
        f.write("---\n\n")
        
        for item in self.stats["results"]:
            icon = "[PASS]" if item["status"] == "VALID" else "[ERROR]"
            f.write(f"## {icon} Q{item['id']}: {item['question']}\n\n")
            
            f.write("| Type | Query |\n|---|---|\n")
            gold = item['sparql_gold'].replace('|', '\|').replace('\n', ' ')
            gen = item['sparql_gen'].replace('|', '\|').replace('\n', ' ')
            f.write(f"| **Gold** | `{gold}` |\n")
            f.write(f"| **Generated** | `{gen}` |\n\n")
            
            if item["error_message"]:
                f.write(f"> **Error:** `{item['error_message']}`\n\n")
            
            f.write("<details>\n<summary>Prompt & Retrieval Details</summary>\n\n")
            
            f.write(f"**Context Entities:**\n```text\n{item['retrieved_context']}\n```\n\n")
            
            f.write("**Few-Shot Examples Used:**\n")
            for i, ex in enumerate(item['retrieved_examples']):
                f.write(f"{i+1}. *{ex['question']}*\n")
            
            f.write(f"\n**Full Prompt Sent to LLM:**\n````text\n{item['full_prompt']}\n````\n")
            
            f.write("\n</details>\n\n---\n")

class SPARQLEvaluator:
    def __init__(self, model_path: Path, retriever: FewShotRetriever):
        self.retriever = retriever
        self.endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", "TextToSparqlBot/1.0")
        self.endpoint.setTimeout(10)
        
        if Llama and model_path.exists():
            logger.info("Loading LLM...")
            self.llm = Llama(model_path=str(model_path), n_ctx=4096, verbose=False)
            self.model_name = model_path.name
        else:
            logger.warning("Using MOCK mode.")
            self.llm = None
            self.model_name = "MOCK_MODEL"

    def prepare_input(self, question: str):
        examples = self.retriever.retrieve(question, k=3)
        context = extract_context(question)
        
        prompt = f"""You are a SPARQL expert for Wikidata. 
            Output ONLY the SPARQL query code inside a ```sparql block.

            ### Relevant Entities & Properties:
            {context}

            ### Examples:
            """
        for ex in examples:
            prompt += f"User: {ex['question']}\nQuery: ```sparql\n{ex['sparql']}\n```\n\n"
            
        prompt += f"User: {question}\nQuery: ```sparql"
        return prompt, context, examples

    def generate(self, prompt: str):
        if not self.llm: return "SELECT * WHERE { ?s ?p ?o } LIMIT 1"
        
        output = self.llm(
            prompt, 
            max_tokens=300, 
            stop=["User:", "```"],
            echo=False,
            temperature=0.1
        )
        return output['choices'][0]['text'].strip()

    def validate(self, query: str):
        try:
            self.endpoint.setQuery(query)
            self.endpoint.query()
            return True, None
        except Exception as e:
            return False, str(e).split("\n")[0]

def get_model_path():
    REPO = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
    FILE = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    dest = Path.home() / "Desktop" / "models" / FILE
    
    if not dest.exists():
        logger.info(f"Downloading model...")
        dest.parent.mkdir(parents=True, exist_ok=True)
        hf_hub_download(repo_id=REPO, filename=FILE, local_dir=dest.parent, local_dir_use_symlinks=False)
    return dest

def main():
    model_path = get_model_path()
    if not model_path: return

    index_path = PROJECT_ROOT / "data/processed/train_index.faiss"
    meta_path = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    
    if not index_path.exists():
        logger.error("Index missing. Run make_dataset.py")
        return

    retriever = FewShotRetriever(index_path, meta_path)
    evaluator = SPARQLEvaluator(model_path, retriever)
    reporter = ReportManager(PROJECT_ROOT, evaluator.model_name)

    test_file = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"
    with open(test_file, 'r') as f:
        test_data = json.load(f)['questions']

    SAMPLES = test_data[:50] 
    logger.info(f"Starting evaluation on {len(SAMPLES)} samples.")

    for q_obj in tqdm(SAMPLES):
        try:
            question = next((x['string'] for x in q_obj['question'] if x['language'] == 'en'), None)
            gold = q_obj['query'].get('sparql', '')
            if not question: continue
            
            prompt, ctx, exs = evaluator.prepare_input(question)
            gen = evaluator.generate(prompt)
            is_valid, err = evaluator.validate(gen)
            
            reporter.log_entry(question, gold, gen, is_valid, err, ctx, exs, prompt)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            continue

    logger.info(f"Finished. Final Accuracy: {reporter.stats['metrics']['accuracy']:.2%}")

if __name__ == "__main__":
    main()
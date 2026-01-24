import logging
import json
import sys
import re
import traceback
import os
import time
from pathlib import Path
from typing import Tuple, List, Dict, Optional
from datetime import datetime

FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    print("ERROR: python-dotenv not installed")
    sys.exit(1)

from SPARQLWrapper import SPARQLWrapper, JSON
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from src.models.generator import build_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import ExampleRetriever
from src.utils.report_manager import ReportManager
from src.utils.sparql_client import SPARQLClient
from src.decomposition.orchestrator import QueryProcessor
from src.decomposition.planner import QueryPlanner
from src.decomposition.orchestrator import QueryProcessor
from src.decomposition.planner import QueryPlanner

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class GeminiQueryModel:
    """Wrapper for Google Gemini."""
    
    def __init__(self, model_id: str):
        self.model_id = model_id
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY mancante! Controlla il file .env nella root del progetto.")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        logger.info(f"Initializing Gemini Model: {model_id}")
        self.model = genai.GenerativeModel(model_id)
    
    def generate(self, prompt: str, max_new_tokens: int = 512) -> str:
        """Generates text using Gemini."""
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_new_tokens,
            temperature=0.1,
            stop_sequences=["User:", "###", "Question:"]
        )
        # Disable safety content filters to prevent false positives when processing code.
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
                logger.warning("Gemini model returned empty response.")
                return ""
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            time.sleep(2)
            return ""
    
    def invoke(self, prompt: str) -> str:
        """Alias for compatibility."""
        return self.generate(prompt)

class WikidataClientGemini:
    """Tool for the Executor to run SPARQL queries against Wikidata."""
    
    def __init__(self):
        self.endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", "TextToSparqlBot/1.0 (GeminiDecomp)")
        self.endpoint.setTimeout(60)
    
    def run_sparql(self, query: str) -> Optional[List]:
        """Executes a SPARQL query and returns results."""
        try:
            # Remove markdown code fence markers that may be present in generated queries.
            clean_query = query.replace("```sparql", "").replace("```", "").strip()
            
            logger.info("Executing SPARQL query against Wikidata endpoint...")
            self.endpoint.setQuery(clean_query)
            results = self.endpoint.query().convert()
            
            bindings = results['results']['bindings']
            if not bindings:
                return []
            
            # Limit results to prevent context overflow
            return bindings[:100]
            
        except Exception as e:
            logger.error(f"SPARQL Execution Failed: {e}")
class SPARQLEvaluator:
    """Evaluator for non-decomposition queries."""
    
    def __init__(self, model_id: str, retriever: ExampleRetriever):
        self.retriever = retriever
        self.endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", "TextToSparqlBot/1.0 (GeminiEval)")
        self.endpoint.setTimeout(60)
        
        self.model_name = model_id
        
        # Retrieve API key from environment or exit gracefully with error message.
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found. Check environment configuration.")
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
        # Disable safety content filters to prevent false positives when processing code.
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
    return "models/gemini-2.0-flash"

def main():
    model_id = get_model_id()
    clean_model_name = model_id.replace('/', '-').replace(' ', '_')

    index_path = PROJECT_ROOT / "data/processed/train_index.faiss"
    meta_path = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    
    if not index_path.exists():
        logger.error(f"Index not found at {index_path}. Run 'make_dataset.py' first.")
        return

    # Initialize Gemini LLM and Wikidata client
    llm = GeminiQueryModel(model_id)
    kg_client = WikidataClientGemini()
    
    reporter = ReportManager(PROJECT_ROOT, clean_model_name, run_prefix="decomposition", mode="decomposition")
    
    orchestrator = QueryProcessor(
        llm=llm,
        generator=llm,
        retriever=kg_client,
        reporter=reporter  
    )

    # Test questions
    test_questions = [
        "Give me all books written by authors born in Germany between 1900 and 1950 with a rating higher than 4",
        "Find scientists born in France who won the Nobel Prize in Physics",
        "What are the tallest buildings in New York City completed after 2000?"
    ]
    
    logger.info(f"Starting decomposition-based evaluation on {len(test_questions)} questions using Gemini...")

    for i, question in enumerate(test_questions, 1):
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing Question {i}/{len(test_questions)}: {question}")
        logger.info(f"{'='*80}\n")
        
        try:
            final_answer = orchestrator.run(question, question_id=i)
            
            logger.info(f"\nFinal Answer: {final_answer}\n")
            
        except Exception as e:
            logger.error(f"Error processing question {i}: {e}")
            traceback.print_exc()
            continue

    reporter.save_final_report()

if __name__ == "__main__":
    main()
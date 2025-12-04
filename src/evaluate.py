"""
Evaluation pipeline for local LLM models using HuggingFace Transformers.
Executes Text-to-SPARQL translation with few-shot learning and self-correction.
"""

import json
import sys
import traceback
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv

FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

from src.config import config
from src.exceptions import ModelError, DataError
from src.validators import validate_file_exists, validate_json_file
from src.logging_config import get_logger
from src.models.generator import build_prompt
from src.models.entities import extract_gold_context
from src.models.retriever import FewShotRetriever
from src.utils.report_manager import ReportManager
from src.utils.sparql_client import SPARQLClient

logger = get_logger(__name__)

class LocalLLMGenerator:
    """Wrapper for HuggingFace Transformers models with hardware optimization."""
    
    def __init__(self, model_id: str):
        self.model_id = model_id
        logger.info(f"Initializing Local Model: {model_id}")
        
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
                logger.info("Attempting to compile model with torch.compile...")
                try:
                    self.model = torch.compile(self.model)
                except Exception as e:
                    logger.warning(f"Compilation failed (continuing without it): {e}")
            
        except Exception as e:
            raise ModelError(f"Failed to load model {model_id}") from e

    def generate_raw(self, prompt: str, stop: list = None, max_new_tokens=512) -> str:
        """
        Generates text completion from the model.
        
        Args:
            prompt: Input text to complete
            stop: List of stop sequences
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=config.model.temperature,
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

def get_model_id():
    return "Qwen/Qwen2.5-Coder-3B-Instruct"

def main():
    model_id = get_model_id()

    # Validate configuration
    try:
        config.validate()
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return

    # 1. Initialize Components
    index_path = PROJECT_ROOT / "data/processed/train_index.faiss"
    meta_path = PROJECT_ROOT / "data/processed/train_metadata.pkl"
    
    try:
        validate_file_exists(index_path, "FAISS index")
        validate_file_exists(meta_path, "Metadata file")
    except FileNotFoundError as e:
        logger.error(f"{e}. Run 'src/data/make_dataset.py' first.")
        return

    retriever = FewShotRetriever(index_path, meta_path)
    sparql_client = SPARQLClient()
    generator = LocalLLMGenerator(model_id)
    reporter = ReportManager(PROJECT_ROOT, model_id.replace("/", "_"), run_prefix="run_local")

    test_file = PROJECT_ROOT / "data/raw/QALD-10/data/qald_10/qald_10.json"
    try:
        validate_file_exists(test_file, "Test data")
        test_data = validate_json_file(test_file)
        if 'questions' not in test_data:
            raise DataError(f"Missing 'questions' key in {test_file}")
        test_data = test_data['questions']
    except (FileNotFoundError, DataError) as e:
        logger.error(f"Test data error: {e}")
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
            
            # --- Gold Execution ---
            gold_results, _ = sparql_client.execute_remote(gold_sparql)
            
            # --- Prompt Construction ---
            examples = retriever.retrieve(question, k=config.retrieval.k_examples)
            context = extract_gold_context(gold_sparql)
            prompt = build_prompt(question, examples, context)

            # --- Generation Loop (with simple retry) ---
            MAX_RETRIES = config.model.max_retries
            best_result = None

            for attempt in range(1, MAX_RETRIES + 2):
                raw_response = generator.generate_raw(prompt, stop=["User:", "```", "###", "Question:"])
                gen_sparql = sparql_client.clean_query(raw_response)
                
                syntax_check = sparql_client.validate_syntax_local(gen_sparql)
                results, exec_error = None, None
                
                if syntax_check["valid"]:
                    results, exec_error = sparql_client.execute_remote(gen_sparql)
                    if exec_error:
                        syntax_check["valid"] = False
                        error_info = {"type": "Execution Error", "detail": exec_error}
                    else:
                        # Success
                        best_result = (gen_sparql, raw_response, True, {}, results, attempt)
                        break
                else:
                    error_info = {"type": syntax_check["type"], "detail": syntax_check["detail"]}

                # Self-correction prompt for next retry
                if attempt <= MAX_RETRIES:
                    prompt += f"\n{gen_sparql}\n```\n\n"
                    prompt += f"SYSTEM: Invalid Query. {error_info.get('detail')}\nFix it.\n"
                    prompt += f"Corrected Query: ```sparql"
                else:
                    # Final failure
                    best_result = (gen_sparql, raw_response, False, error_info, None, attempt)
            
            # --- Logging ---
            gen_sparql, raw_resp, is_valid, error_info, gen_results, attempts = best_result
            
            f1 = 0.0
            if is_valid and gen_results:
                f1 = sparql_client.calculate_f1(gold_results, gen_results)
                if f1 < 1.0:
                    error_info = {"type": "Wrong Answer", "detail": f"F1 Score: {f1:.2f}"}
            
            reporter.log_entry(
                question, gold_sparql, gen_sparql, raw_resp, is_valid, 
                error_info, f1, attempts, prompt, context, gold_results, gen_results
            )
            
        except Exception as e:
            logger.error(f"Error processing question {i+1}: {e}")
            traceback.print_exc()
            continue

    reporter.save_final_report()

if __name__ == "__main__":
    main()
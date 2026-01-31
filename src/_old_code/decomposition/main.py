import sys
import logging
import torch
from pathlib import Path
from SPARQLWrapper import SPARQLWrapper, JSON
from transformers import AutoModelForCausalLM, AutoTokenizer

# Path Setup
FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Internal Imports
from src.decomposition.orchestrator import QueryProcessor
from src.models.retriever import ExampleRetriever

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class HuggingFaceLLM:
    def __init__(self, model_id):
        self.model_id = model_id
        logger.info(f"Initializing Model: {model_id}")

        # Hardware Optimization (Same as in evaluate.py)
        attn_impl = "eager"
        try:
            import flash_attn

            attn_impl = "flash_attention_2"
            logger.info("Optimization: Flash Attention 2 enabled.")
        except ImportError:
            attn_impl = "sdpa"
            logger.info("Optimization: Flash Attention 2 not found. Using SDPA.")

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto",
            attn_implementation=attn_impl,
        )
        self.model.eval()

    def generate(self, prompt, max_new_tokens=512):
        """Generates text based on the prompt."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Strip the input prompt from the response to get only the new text
        if prompt in full_text:
            response = full_text.split(prompt)[-1]
        else:
            response = full_text[len(prompt) :]

        return response.strip()

    # Alias for compatibility if your planner uses .invoke()
    def invoke(self, prompt):
        return self.generate(prompt)


class WikidataClient:
    """
    Executor to run SPARQL queries against Wikidata.
    """

    def __init__(self):
        self.endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", "TextToSparqlBot/1.0")
        self.endpoint.setTimeout(60)

    def run_sparql(self, query):
        """Executes a SPARQL query and returns formatted results."""
        try:
            # Cleanup markdown if present
            clean_query = query.replace("```sparql", "").replace("```", "").strip()

            logger.info(f"Executing SPARQL...")
            self.endpoint.setQuery(clean_query)
            results = self.endpoint.query().convert()

            bindings = results["results"]["bindings"]
            if not bindings:
                return []

            # Simple formatter for the context
            formatted_results = []
            for row in bindings:
                # Extract values (simplified for context injection)
                values = [v["value"].split("/")[-1] for v in row.values()]
                formatted_results.append("(" + ", ".join(values) + ")")

            # Limit results to avoid context overflow in next steps
            return formatted_results[:10]

        except Exception as e:
            logger.error(f"SPARQL Execution Failed: {e}")
            return None


def main():
    # 1. Configuration
    MODEL_ID = "Qwen/Qwen2.5-Coder-3B-Instruct"
    INDEX_PATH = PROJECT_ROOT / "data/processed/train_index.faiss"
    META_PATH = PROJECT_ROOT / "data/processed/train_metadata.pkl"

    # 2. Check Data
    if not INDEX_PATH.exists():
        logger.error(
            f"Index not found at {INDEX_PATH}. Please run make_dataset.py first."
        )
        return

    # 3. Initialize Components
    logger.info("--- Initializing Decomposition Pipeline ---")

    # A. The Brain (LLM)
    llm = HuggingFaceLLM(MODEL_ID)

    # B. The Knowledge
    # retriever = ExampleRetriever(INDEX_PATH, META_PATH)

    # C. The Tools (Wikidata Client)
    kg_client = WikidataClient()

    # 4. Initialize Orchestrator
    orchestrator = QueryProcessor(llm=llm, generator=llm, retriever=kg_client)

    # 5. Run Test
    question = "Give me all books written by authors born in Germany between 1900 and 1950 with a rating higher than 4"

    logger.info(f"\nUSER QUESTION: {question}\n")

    final_answer = orchestrator.run(question)

    logger.info("\n--- FINAL OUTPUT ---")
    print(final_answer)


if __name__ == "__main__":
    main()

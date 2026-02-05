# Text-to-SPARQL Pipeline

Translates natural language questions into SPARQL queries for Wikidata using retrieval-augmented generation with LLMs.

## Pipeline

```
Question → Entity Linking → Schema Retrieval → Few-shot Context → LLM Generation → Validation → SPARQL
```

- **Entity Linking**: REBEL/ReLiK maps mentions to Wikidata QIDs
- **Retrieval**: FAISS-based similar examples and schema hints
- **Generation**: GPT-4/Llama with configurable prompting strategies
- **Validation**: Syntax check + optional execution + multi-turn self-correction

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python src/data/make_schema_index.py && python src/data/make_index.py
```

`.env`:
```
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

## Usage

```bash
python main.py                                    # Default run
python main.py dataset.limit=10                   # Limit samples
python main.py prompt=cot                         # Chain-of-Thought reasoning
python main.py prompt=decomposition               # Query decomposition
python main.py validation.enable_correction=true  # Multi-turn self-correction
python main.py model=azure_gpt4 linking=relik     # Change model/linker
```

## Debug

Inspect generated prompts without API calls:
```bash
python src/debug/prompts.py prompt=cot linking=relik retrieval=3shot
```

## Configuration

| Parameter | Options | Default |
|-----------|---------|---------|
| `model` | `azure_gpt4_mini`, `azure_gpt4`, `llama_33` | `azure_gpt4_mini` |
| `prompt` | `standard`, `cot`, `decomposition` | `standard` |
| `linking` | `rebel`, `relik`, `all` | `rebel` |
| `retrieval` | `1shot`, `3shot` | `3shot` |
| `validation.enable_correction` | `true`, `false` | `false` |
| `validation.max_attempts` | `1-10` | `3` |
| `validation.validate_execution` | `true`, `false` | `false` |
| `dataset.limit` | `N` or `null` | `null` |

## Project Structure

```
conf/           # Hydra configuration files
src/
  clients/      # Async LLM clients with retry
  components/   # Entity linker, prompt builder, validator
  pipelines/    # Batch processing
  debug/        # Prompt inspector
data/processed/ # FAISS indices
outputs/        # Results
```

## Output

Results: `outputs/[experiment]/[timestamp]/results.json`

## License

MIT

# Text-to-SPARQL LLM Pipeline

A modular pipeline for translating natural language questions into SPARQL queries using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and iterative self-correction. Benchmarked on QALD-10 dataset with Wikidata.

## Features

- **Multi-Model Support**: HuggingFace Transformers (Qwen) + Google Gemini API
- **RAG with FAISS**: Few-shot learning with semantic retrieval
- **ACE Engine**: Automated Correction Engine with persistent error learning
- **Self-Correction**: Iterative query refinement with syntax/execution validation
- **Comprehensive Evaluation**: F1 scores, syntax accuracy, execution validation
- **Production-Ready**: Centralized config, custom exceptions, input validation, logging

## Architecture

```
src/
├── config.py              # Centralized configuration (ModelConfig, RetrievalConfig, etc.)
├── exceptions.py          # Custom exception hierarchy (APIError, SPARQLError, etc.)
├── validators.py          # Input validation utilities
├── logging_config.py      # Unified logging setup
├── evaluate.py            # Local model evaluation (HuggingFace)
├── evaluate_gemini.py     # Gemini API evaluation
├── evaluate_ace_gemini.py # ACE Engine evaluation
├── models/
│   ├── retriever.py       # FAISS-based RAG retriever
│   ├── generator.py       # Prompt construction
│   ├── ace.py             # Automated Correction Engine
│   ├── entities.py        # Schema extraction utilities
│   └── tools.py           # Wikidata API integration
├── utils/
│   ├── sparql_client.py   # SPARQL validation & execution
│   └── report_manager.py  # JSON/Markdown report generation
└── data/
    └── make_dataset.py    # FAISS index creation
```

## Quick Start

### 1. Installation

```bash
git clone <repo-url>
cd text-to-sparql-llm
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Setup

Create `.env` file in project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Verify Installation

```bash
python cli.py check           # Check all dependencies
python cli.py validate-config # Validate configuration
```

### 4. Create Dataset

Generate FAISS index and embeddings (first-time setup):

```bash
python cli.py dataset
# Or directly:
python src/data/make_dataset.py
```

This creates:
- `data/processed/train_index.faiss` (vector index)
- `data/processed/train_metadata.pkl` (question-query pairs)

### 5. Run Evaluation

**Option A: Gemini API (Recommended)**
```bash
python cli.py eval --model gemini
# Or directly:
python src/evaluate_gemini.py
```

**Option B: Local Model (HuggingFace)**
```bash
python cli.py eval --model local
# Or directly:
python src/evaluate.py
```

**Option C: ACE Engine (Advanced)**
```bash
python cli.py ace
# Or directly:
python src/evaluate_ace_gemini.py
```

## CLI Commands

```bash
# Evaluation
python cli.py eval --model gemini  # Run Gemini evaluation
python cli.py eval --model local   # Run local model evaluation
python cli.py ace                  # Run ACE Engine

# Dataset
python cli.py dataset              # Create FAISS index

# Utilities
python cli.py check                # Check dependencies
python cli.py validate-config      # Validate configuration
python cli.py clean-playbook --save # Clean ACE playbook
```

## Configuration

Edit `src/config.py` to customize:

```python
@dataclass
class ModelConfig:
    temperature: float = 0.1      # LLM sampling temperature
    max_retries: int = 3          # Self-correction attempts
    max_tokens: int = 512         # Max output tokens

@dataclass
class RetrievalConfig:
    k_examples: int = 3           # Few-shot examples count
    top_k: int = 10               # FAISS retrieval candidates
```

## Project Structure

```
├── cli.py                    # Command-line interface
├── playbook.json             # ACE learned strategies 
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── pytest.ini                # Test configuration
├── setup.py                  # Package metadata
├── data/
│   ├── raw/QALD-10/         # Test dataset
│   └── processed/           # FAISS index & metadata
├── reports/                 # Evaluation results (timestamped)
├── src/                     # Source code (see Architecture)
└── tests/                   # Unit tests
    ├── test_config.py
    ├── test_exceptions.py
    ├── test_validators.py
    └── test_sparql_client.py
```

## Evaluation Metrics

Results saved in `reports/YYYY-MM-DD/run_XXX_HHMMSS/`:

- **`results.json`**: Structured evaluation data
  - Total questions processed
  - Syntax accuracy (% valid SPARQL)
  - Answer accuracy (% correct results)
  - Average F1 score
  - Per-question details (query, errors, F1, attempts)

- **`report.md`**: Human-readable summary with:
  - Query comparison (generated vs. gold)
  - Error diagnostics
  - Execution results

### Metrics Explained

- **Syntax Accuracy**: Percentage of syntactically valid SPARQL queries
- **Answer Accuracy**: Percentage of queries returning correct results
- **F1 Score**: Harmonic mean of precision/recall on result bindings
- **Successful Retries**: Questions fixed through self-correction

## Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_sparql_client.py -v
```

## ACE Engine (Advanced)

The **Automated Correction Engine** learns from failures:

1. **Generation**: Create query with few-shot examples + learned strategies
2. **Validation**: Check syntax & execute against Wikidata
3. **Learning**: On failure, analyze error and create new strategy
4. **Persistence**: Save strategy to `playbook.json` for future queries

Current playbook: **26 curated strategies** (cleaned from 94 malformed entries)

## Troubleshooting

**FAISS index not found:**
```bash
python cli.py dataset
```

**Missing API key:**
```bash
# Add to .env:
GEMINI_API_KEY=your_key_here
```

**Import errors:**
```bash
pip install -r requirements.txt
```

**Test data missing:**
```bash
# Ensure QALD-10 dataset exists at:
data/raw/QALD-10/data/qald_10/qald_10.json
```

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run linters
black src/
flake8 src/

# Type checking
mypy src/
```

## License

See `LICENSE` file for details.


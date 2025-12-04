# Text-to-SPARQL LLM

Translate natural language questions into SPARQL queries using LLMs, RAG, and self-correction. Built on QALD-10 + Wikidata.

## Features

- **Multi-Model Support**: HuggingFace (Qwen) + Google Gemini
- **RAG with FAISS**: Few-shot semantic retrieval
- **ACE Engine**: Learn from errors, improve over time
- **Self-Correction**: Automatic query refinement
- **Experiment Tracking**: MLflow + custom metrics
- **Production Setup**: Config, error handling, validation, logging

## Structure

```
src/
├── config.py              # Settings (models, retrieval, etc.)
├── exceptions.py          # Custom errors
├── validators.py          # Input validation
├── logging_config.py      # Logging setup
├── evaluate.py            # HuggingFace evaluation
├── evaluate_gemini.py     # Gemini evaluation
├── evaluate_ace_gemini.py # ACE evaluation
├── evaluation/            # Experiment tracking
│   ├── metrics.py         # Custom metrics
│   ├── mlflow_reporter.py # MLflow integration
│   └── README.md          # Evaluation docs
├── models/
│   ├── retriever.py       # FAISS retrieval
│   ├── generator.py       # Prompt building
│   ├── ace.py             # Error learning
│   ├── entities.py        # Schema extraction
│   └── tools.py           # Wikidata API
├── utils/
│   └── sparql_client.py   # SPARQL validation
└── data/
    └── make_dataset.py    # Index creation
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

### 3. Check Setup

```bash
python cli.py check
python cli.py validate-config
```

### 4. Create Index

Generate FAISS embeddings (first time only):

```bash
python cli.py dataset
```

### 5. Run Evaluation

Gemini :
```bash
python cli.py eval --model gemini
```

Local model:
```bash
python cli.py eval --model local
```

With ACE learning:
```bash
python cli.py ace
```

## CLI Commands

```bash
# Evaluation
python cli.py eval --model gemini  # Run Gemini evaluation
python cli.py eval --model local   # Run local model evaluation
python cli.py ace                  # Run ACE Engine

# View Results (MLflow UI)
python cli.py view-results         # Launch interactive dashboard

# Dataset
python cli.py dataset              # Create FAISS index

# Utilities
python cli.py check                # Check dependencies
python cli.py validate-config      # Validate configuration
python cli.py clean-playbook --save # Clean ACE playbook
```

## View Results

Evaluations automatically log to MLflow:

```bash
python cli.py view-results
```

Opens at http://localhost:5000

## Configuration

Edit `src/config.py`:

```python
@dataclass
class ModelConfig:
    temperature: float = 0.1
    max_retries: int = 3
    max_tokens: int = 512

@dataclass
class RetrievalConfig:
    k_examples: int = 3
    top_k: int = 10
```

## Project Structure

```
├── cli.py                    # Commands
├── view_results.py           # MLflow UI
├── playbook.json             # ACE strategies (26 rules)
├── requirements.txt          # Dependencies
├── setup.py                  # Package info
├── EVALUATION_SYSTEM.md      # Evaluation docs
├── data/
│   ├── raw/QALD-10/         # Test data
│   └── processed/           # FAISS index
├── mlruns/                  # MLflow results
├── src/                     # Source code
│   └── evaluation/          # Tracking & metrics
└── tests/                   # Unit tests
```

## Metrics

MLflow tracks (view at http://localhost:5000):

### Charts:
- F1 score distribution
- Success rate by retry count
- Error frequency
- Performance trend

### Metrics:
- Syntax accuracy
- Answer accuracy
- F1 score
- Retry success rate
- Custom: syntax, execution, context

### Export:
- JSON, CSV, HTML, PNG

## Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_sparql_client.py -v
```

## ACE Engine

Learns from failures:

1. Generate query + learned strategies
2. Validate syntax & execution
3. On failure, analyze and create new strategy
4. Save to `playbook.json`

26 strategies in playbook

## Troubleshooting

Missing FAISS index:
```bash
python cli.py dataset
```

Missing API key - add to `.env`:
```env
GEMINI_API_KEY=your_key_here
```

Import errors:
```bash
pip install -r requirements.txt
```

## Development

```bash
pip install -r requirements-dev.txt
black src/
flake8 src/
mypy src/
```

## License

See `LICENSE` file for details.


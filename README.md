# Text-to-SPARQL with LLMs

### A modular research pipeline for translating natural-language questions into executable SPARQL queries over Wikidata

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Hydra](https://img.shields.io/badge/config-Hydra-89b8cd)](https://hydra.cc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-research%20prototype-yellow)](#project-status)

This repository explores what actually improves Text-to-SPARQL generation with large language models. It combines entity linking, example retrieval, schema information, prompting strategies, validation and agentic correction in one configurable experimental pipeline.

The project targets Wikidata and was designed for controlled experiments on the QALD benchmark.

## Why this project?

Generating valid SPARQL is only part of the problem. A model can produce syntactically correct queries while still selecting the wrong entity, property or graph pattern.

This pipeline separates those failure points so that each component can be tested independently. The main focus is understanding how entity linking, few-shot retrieval, schema hints and prompting strategies affect final query quality.

## Pipeline

```text
Natural-language question
        ↓
Entity linking
        ↓
Schema and example retrieval
        ↓
Prompt construction
        ↓
LLM generation
        ↓
Syntax and execution validation
        ↓
Optional self-correction
        ↓
SPARQL query
```

## Main components

| Component | Purpose |
| --- | --- |
| Entity linking | Maps textual mentions to Wikidata entities using REBEL or ReLiK |
| Example retrieval | Retrieves similar demonstrations with FAISS |
| Schema retrieval | Adds relevant Wikidata properties and structural hints |
| Prompting | Supports standard, chain-of-thought and decomposition strategies |
| Generation | Runs GPT-4-class or Llama models through configurable clients |
| Validation | Checks syntax and optionally executes generated queries |
| Self-correction | Feeds validation failures back to the model for another attempt |
| Evaluation | Compares generated answers and queries against benchmark references |

## Research findings

Experiments with this pipeline showed that entity linking is the most important component in the tested setting. Adding a linker produced a much larger improvement than simply increasing prompt complexity.

The strongest configurations reached roughly 24 to 25 percent macro F1 on the evaluated QALD-10 setup, while simpler baselines remained much lower. Decomposition worked best for GPT-4o, while self-consistency was more competitive for GPT-4o-mini and Llama 3.3 70B.

Few-shot retrieval without reliable entity linking often underperformed zero-shot prompting, and schema hints could become distracting when the linked entities were already available. These results suggest that grounding and disambiguation matter more than adding more prompt context.

## Quick start

```bash
git clone https://github.com/Andrei-Stefan20/text-to-sparql-llm.git
cd text-to-sparql-llm

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create the indexes:

```bash
python src/data/make_schema_index.py
python src/data/make_index.py
```

Create a `.env` file in the repository root:

```env
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""
LLAMA_ENDPOINT=""
LLAMA_API_KEY=""
SPARQL_ENDPOINT_URL="https://query.wikidata.org/sparql"
```

## Usage

Run the default configuration:

```bash
python main.py
```

Run a smaller experiment:

```bash
python main.py dataset.limit=10
```

Try a different prompting strategy:

```bash
python main.py prompt=decomposition
```

Enable iterative correction:

```bash
python main.py validation.enable_correction=true
```

Choose another model and linker:

```bash
python main.py model=azure_gpt4 linking=relik
```

Inspect generated prompts without making API calls:

```bash
python src/debug/prompts.py prompt=cot linking=relik retrieval=3shot
```

## Configuration

| Parameter | Options | Default |
| --- | --- | --- |
| `model` | `azure_gpt4_mini`, `azure_gpt4`, `llama_33` | `azure_gpt4_mini` |
| `prompt` | `standard`, `cot`, `decomposition` | `standard` |
| `linking` | `rebel`, `relik`, `all` | `rebel` |
| `retrieval` | `1shot`, `3shot` | `3shot` |
| `validation.enable_correction` | `true`, `false` | `false` |
| `validation.max_attempts` | `1-10` | `3` |
| `validation.validate_execution` | `true`, `false` | `false` |
| `dataset.limit` | integer or `null` | `null` |

Hydra keeps experiment settings separated from implementation code, making ablations reproducible and easy to compare.

## Project structure

```text
conf/                  Hydra experiment configurations
src/clients/           Async LLM clients and retry logic
src/components/        Entity linking, prompts and validation
src/data/              Dataset preparation and indexes
src/evaluation/        Benchmark and GERBIL evaluation utilities
src/pipelines/         Batch experiment pipelines
src/debug/             Prompt inspection tools
scripts/               Analysis and plotting utilities
data/processed/        Generated FAISS and schema indexes
outputs/               Experiment results
```

Results are stored under:

```text
outputs/<experiment>/<timestamp>/results.json
```

## Documentation

| Document | Content |
| --- | --- |
| [Research notes](docs/references/RESEARCH.md) | Papers, design notes and future work |
| [Test roadmap](docs/TEST_ROADMAP.md) | Planned experiments and result tracking |

## Project status

This is a research prototype developed for experimentation rather than a production query service. Model APIs, Wikidata availability and entity-linking dependencies may affect reproducibility.

The architecture is modular enough to test new linkers, prompting strategies, models and evaluation procedures without rewriting the full pipeline.

## License

Released under the [MIT License](LICENSE).

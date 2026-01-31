# Text-to-SPARQL Pipeline

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Config: Hydra](https://img.shields.io/badge/Config-Hydra-89b8cd)](https://hydra.cc/)
[![Search: FAISS](https://img.shields.io/badge/Search-FAISS-00d1ce)](https://github.com/facebookresearch/faiss)
[![Models: HuggingFace](https://img.shields.io/badge/Models-HuggingFace-ffcc00)](https://huggingface.co/)

Transform natural language questions into executable SPARQL queries for Wikidata.

This pipeline uses retrieval-augmented generation to convert plain English into valid SPARQL. It combines semantic search with entity linking to keep outputs grounded in actual schema data, cutting down on hallucinations.

## Why

SPARQL is powerful but not exactly user-friendly. Most people can't write it, and honestly, most people shouldn't have to. This project takes the question you'd ask a librarian and turns it into something a knowledge graph can answer.

The approach: pull in relevant schema elements and query examples, then let an LLM synthesize the final SPARQL with all that context in hand.

## How It Works

The pipeline runs through four stages:

**1. Entity Linking**  
First, we figure out what entities and relationships the question mentions. Uses models like REBEL or ReLiK to spot things like "Barack Obama" or "born in" and map them to actual Wikidata identifiers.

**2. Schema Retrieval**  
Next, we translate natural language into Wikidata's property vocabulary. When you say "actors," the system finds property `P161`. This happens through semantic search over a pre-built FAISS index of all relevant properties.

**3. Context Retrieval**  
The system pulls similar questions from the QALD-9-plus dataset. These examples show the LLM what good SPARQL queries look like for comparable questions.

**4. Generation**  
Finally, an LLM (GPT-4, Azure OpenAI, or Llama) writes the SPARQL query using everything we've gathered. The retrieved context keeps it honest and syntactically correct.

## Getting Started

### What You Need

- Python 3.10 or newer
- A virtual environment (just trust me on this one)

### Install

```bash
# Clone the repo
git clone https://github.com/yourusername/text-to-sparql-llm.git
cd text-to-sparql-llm

# Set up your environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure API Keys

Create a `.env` file at the project root:

```env
OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
```

### Build the Indices

Before you can run anything, you need to build the vector indices. This is a one-time thing:

```bash
# Download and index Wikidata properties
python src/data/make_schema_index.py

# Index the training examples
python src/data/make_index.py
```

You'll end up with `data/processed/schema_index.faiss` and `data/processed/train_index.faiss`.

## Running the Pipeline

### Basic Usage

Just run it:

```bash
python main.py
```

### Debug Mode

Want to see what's happening under the hood without burning API credits?

```bash
python src/debug/prompts.py linking.device=-1
```

This lets you inspect entity extraction and prompt construction before the LLM gets involved.

### Tweak Settings

The whole thing runs on [Hydra](https://hydra.cc/), so you can override configs from the command line:

```bash
# Switch to Azure GPT-4
python main.py model=azure_gpt4

# Try a different entity linker
python main.py linking=relik

# Turn off retrieval entirely (zero-shot mode)
python main.py retrieval.k=0
```

## Project Structure

```
text-to-sparql-llm/
├── conf/                   # Hydra configuration
│   ├── model/              # LLM configs (GPT-4, Llama, Azure)
│   └── linking/            # Entity linker configs (REBEL, ReLiK)
├── src/
│   ├── clients/            # LLM API wrappers
│   ├── components/         # Core modules (Linker, Retriever, Builder)
│   ├── data/               # Indexing scripts
│   └── debug/              # Development tools
├── data/
│   └── processed/          # FAISS indices and metadata
├── main.py                 # Entry point
└── requirements.txt
```

## License

MIT License — see [LICENSE](LICENSE) for the full text.

---
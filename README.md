text-to-sparql-llm
==============================
A pipeline for translating Natural Language (NL) queries into SPARQL using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and grammar-constrained decoding. The system is benchmarked on QALD-9 and QALD-10 datasets.

Architecture
------------


The project uses a modular architecture located in `src/models/`:

* **ACE Agent (`ace.py`, `agent.py`):** The main composer managing the request logic.
* **Retriever (`retriever.py`):** **FAISS**-based RAG module. It retrieves relevant few-shot examples or schemas from processed metadata (`data/processed/train_index.faiss`).
* **Generator (`generator.py`):** Interface for the Large Language Model.
* **Grammar Constraint (`sparql_grammar`):** Uses an EBNF grammar to force the LLM to generate valid SPARQL syntax during inference.


Setup
------------

1.  **Clone and create virtual environment:**

    ```bash
    git clone <repo-url>
    cd text-to-sparql-llm
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration:**
    Create a `.env` file in the root directory with necessary API keys (e.g., OpenAI API Key, SPARQL endpoint).

## Usage

### 1\. Data Preparation

Generate embeddings and FAISS indices for retrieval:

```bash
python src/data/make_dataset.py
```

### 2\. Execution & Evaluation

Run the evaluation pipeline using the ACE script. Parameters are controlled via `playbook.json`.

```bash
python src/evaluate_ace.py
```

Results are automatically saved in `reports/YYYY-MM-DD/run_ID/` containing:

  * `results.json`
  * `report.md`

## Metrics

The system evaluates performance by comparing the generated SPARQL query against the QALD ground truth, calculating metrics such as Precision, Recall, and F1-score on query execution (or syntactic match).

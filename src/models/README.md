# Models Layer

## Files
- `generator.py`: Prompt builders for standard and ACE flows. Adds Wikidata prefixes, few-shot examples, schema/context, and wraps output in ```sparql``` blocks.
- `ace.py`: ACE (adaptive correction). `CorrectionHandler` learns rules from failed queries and saves them to `playbook.json` so prompts can reuse them.
- `entities.py`: Pulls Wikidata IDs from a gold SPARQL query, fetches labels/descriptions, and formats them as context for prompts.
- `retriever.py`: FAISS-based semantic retriever. Loads embeddings/metadata, encodes a query, and returns similar question–SPARQL pairs with caching and sanity checks.
- `tools.py`: Placeholder for shared model utilities (empty for now).

## How it fits together
1. `ExampleRetriever.retrieve` returns few-shot examples for a user question.
2. `extract_gold_context` builds a labeled schema/context string from a reference query when available.
3. `build_prompt` or `build_ace_prompt` assembles the final prompt with prefixes, examples, and context.
4. An LLM generates SPARQL; downstream code cleans and runs it (evaluation/decomposition pipelines).
5. On failures, `CorrectionHandler.curate` learns a new rule and stores it for later runs.

## Key behaviors
- Standard prefixes are enforced; the ACE variant keeps the same set but markdown-friendly.
- Prompts end with an opening ```sparql fence to nudge code-only output.
- Retriever safeguards: adjusts invalid `k`, skips malformed examples, filters identical questions, caches by query+k.
- ACE expects a generator with `generate_raw`; it only keeps rules that look useful.

## Minimal usage sketch
```python
from src.models.generator import build_prompt
from src.models.retriever import ExampleRetriever
from src.models.entities import extract_gold_context

retriever = ExampleRetriever(index_path, metadata_path)
examples = retriever.retrieve(user_question, k=3)
context = extract_gold_context(gold_sparql)
prompt = build_prompt(user_question, examples, context)
# feed `prompt` to your LLM
```

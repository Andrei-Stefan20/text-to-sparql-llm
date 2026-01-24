# Decomposition Pipeline (Wikidata)

## What’s inside
- `main.py`: Minimal entrypoint for a local HuggingFace model. Sets up `HuggingFaceLLM`, wires it into `QueryProcessor`, sends a demo question, and prints the synthesized answer. Swap `MODEL_ID` to change the model; point the retriever to your FAISS artifacts if you want context examples.
- `main_gemini.py`: Gemini entrypoint. Builds `GeminiQueryModel`, `QueryPlanner`, and `StepRunner`; includes a legacy `SPARQLEvaluator` for non-decomposition trials and a `WikidataClientGemini` that trims markdown fences before hitting the endpoint. Requires `GEMINI_API_KEY` in `.env`.
- `planner.py`: `QueryPlanner` drives stepwise planning. It prompts the LLM for the next action (entity_search, filtering, join, aggregation), normalizes the JSON payload, and stores intermediate context. Multiple parsing fallbacks handle messy LLM outputs.
- `executor.py`: `StepRunner` generates SPARQL per step, cleans it, executes with retry/backoff, and tracks metadata (status, attempts, result count). It enforces dependency order, injects prior-step context, and applies query-type guidance (entity search, filtering, join, aggregation).
- `orchestrator.py`: `QueryProcessor` runs the end-to-end loop: plan → execute each step → synthesize. It logs per-step outcomes, preserves context, and asks the LLM to draft the final answer, with a structured fallback if synthesis fails.
- `__init__.py`: Package initializer.

## Execution flow
1. **Planning** (`QueryPlanner.create_plan_iterative`): the LLM proposes one step at a time, returning a JSON block with description, query_type, optional depends_on, and a needs_more_steps flag. Planning stops when the flag is false or the step cap is reached.
2. **Execution** (`StepRunner.execute_step`): for each step, the executor builds a SPARQL prompt that embeds prior-step context, generates a query, strips markdown, enforces `LIMIT`, runs it against Wikidata, and records status/result metadata. Dependency checks prevent out-of-order execution.
3. **Synthesis** (`QueryProcessor._combine_results`): successful step results are summarized and fed to the LLM to draft the final answer. If synthesis fails, a structured fallback returns the aggregated step outputs.

## How to run
Run from the repository root with the Python environment active.

### Local LLM (HuggingFace)
```bash
python -m src.decomposition.main
```
- Uses `HuggingFaceLLM` with `Qwen/Qwen2.5-Coder-3B-Instruct` by default (edit `MODEL_ID` in `main.py`).
- Expects FAISS artifacts in `data/processed/` (index and metadata) if you enable the example retriever.

### Gemini
```bash
python -m src.decomposition.main_gemini
```
- Requires `GEMINI_API_KEY` in `.env` (project root).
- Uses `GeminiQueryModel` for generation and `WikidataClientGemini` for SPARQL execution; removes code fences before calling the endpoint.

## Quick configuration
- **Wikidata endpoint**: fixed in `WikidataClient` / `WikidataClientGemini` with dedicated User-Agent.
- **Timeout**: 60s default on SPARQL endpoints.
- **LLM params**: temperature 0.1 and `max_new_tokens` 512/400 in generation methods (see `generate`).
- **Dependencies**: `SPARQLWrapper`, `transformers`, `google-generativeai`, `torch` (for `main.py`), plus `dotenv` to load keys.

## Operational tips
- Write questions with explicit constraints (dates, locations, numeric filters) so planning converges quickly.
- Check generated SPARQL in logs when you see empty results; the executor forces `LIMIT 100` to keep responses bounded.
- To support new step types, add a case in `_get_query_type_guidance` and teach the planner to emit that `query_type`.

# Test Plan & Experiments Log — Full Dataset (394)

Testing roadmap for the thesis project. Same structure as the 100-question plan but this is the real deal — full QALD-10 dataset.

**Started**: February 2026

---

## Models to Test

Every experiment below should be repeated for each model:

| Model ID | Config | Notes |
|----------|--------|-------|
| **M1** | `model=azure_gpt4_mini` | Cheapest, baseline |
| **M2** | `model=azure_gpt4` | More expensive, better? |
| **M3** | `model=llama_33` | Free, slower |

**Naming convention**: `exp{N}_{test}_{model}_394`
- Example: `exp1_cot_gpt4mini_394`, `exp1_cot_gpt4_394`, `exp1_cot_llama_394`

---

## Before Starting: Sanity Checks

Always run these first:

```bash
# Does the code even run?
python main.py dataset.limit=2 system.experiment_name=sanity_2q

# Can I see the prompts? (no API calls, safe to run)
python src/debug/prompts.py prompt=standard linking.device=-1
python src/debug/prompts.py prompt=cot linking.device=-1
```

If any of these fail, fix that first before running anything.

---

## test Tests (limit=10)

Run every new config on 10 questions before committing to a full 394 run. Not for comparing results — just to catch crashes.

```bash
# === GPT-4-mini test ===
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini prompt=standard system.experiment_name=test_standard_gpt4mini_10
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini prompt=cot system.experiment_name=test_cot_gpt4mini_10
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini prompt=decomposition system.experiment_name=test_decomp_gpt4mini_10
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini linking=rebel system.experiment_name=test_rebel_gpt4mini_10
python main.py dataset.limit=10 model=azure_gpt4_mini linking=relik system.experiment_name=test_relik_gpt4mini_10
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini linking=none system.experiment_name=test_nolink_gpt4mini_10
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini retrieval.k=0 system.experiment_name=test_0shot_gpt4mini_10
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini retrieval.k=5 system.experiment_name=test_5shot_gpt4mini_10
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini validation.enable_correction=true validation.max_attempts=3 system.experiment_name=test_3corr_gpt4mini_10
(ok) python main.py dataset.limit=10 model=azure_gpt4_mini validation.self_consistency_samples=3 system.experiment_name=test_3samples_gpt4mini_10

# === GPT-4 test ===
(ok) python main.py dataset.limit=10 model=azure_gpt4 prompt=standard system.experiment_name=test_standard_gpt4_10
(ok) python main.py dataset.limit=10 model=azure_gpt4 prompt=cot system.experiment_name=test_cot_gpt4_10

# === Llama test ===
(ok) python main.py dataset.limit=10 model=llama_33 prompt=standard system.experiment_name=test_standard_llama_10
(ok) python main.py dataset.limit=10 model=llama_33 prompt=cot system.experiment_name=test_cot_llama_10
```

| Config | Model | Crashed? | Notes |
| --- | --- | --- | --- |
| standard | GPT-4-mini | | |
| cot | GPT-4-mini | | |
| decomposition | GPT-4-mini | | |
| rebel | GPT-4-mini | | |
| relik | GPT-4-mini | | |
| no linker | GPT-4-mini | | |
| k=0 | GPT-4-mini | | |
| k=5 | GPT-4-mini | | |
| correction 3x | GPT-4-mini | | |
| 3 samples | GPT-4-mini | | |
| standard | GPT-4 | | |
| cot | GPT-4 | | |
| standard | Llama | | |
| cot | Llama | | |

---

## Research Questions

1. **Does Chain-of-Thought help?**
   - Hypothesis: CoT should help with complex multi-hop questions
   - But maybe it's overkill for simple questions?

2. **Which entity linker is better?**
   - REBEL is older but more stable
   - ReLiK is newer, supposedly more accurate
   - Using both together might be best but slower

3. **Is self-correction worth the extra API calls?**
   - Each retry costs money
   - But if it fixes 30% of errors, probably worth it?

4. **How many examples do I need?**
   - 0-shot: model uses only its training
   - 3-shot: more context but longer prompt
   - Trade-off between accuracy and token cost

5. **Does self-consistency help?**
   - Generate 3-5 queries, vote on best
   - 3-5x the cost — is the gain worth it?

6. **Do prompt rules actually reduce errors?**
   - Explicit rules for ASK, dates, no subqueries
   - Does adding negative examples help?

7. **Does the model matter more than the prompting strategy?**
   - Maybe GPT-4 with simple prompting beats GPT-4-mini with CoT?

8. **Tool Dependency vs. Internal Knowledge (Ablation)**
   - Do models actually need the Entity Linker, or do they know common QIDs?
   - Do they need Schema Retrieval, or do they know properties?

---

## Experiment 1: Prompting Strategies

**Question**: Which prompting strategy works best?

### Commands for each model:

```bash
# === GPT-4-mini ===
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini prompt=standard system.experiment_name=exp1_standard_gpt4mini_394
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini prompt=cot system.experiment_name=exp1_cot_gpt4mini_394
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini prompt=decomposition system.experiment_name=exp1_decomp_gpt4mini_394

# === GPT-4 ===
(ok) python main.py dataset.limit=394 model=azure_gpt4 prompt=standard system.experiment_name=exp1_standard_gpt4_394
(ok) python main.py dataset.limit=394 model=azure_gpt4 prompt=cot system.experiment_name=exp1_cot_gpt4_394
(ok) python main.py dataset.limit=394 model=azure_gpt4 prompt=decomposition system.experiment_name=exp1_decomp_gpt4_394

# === Llama 33 ===
(0k)python main.py dataset.limit=394 model=llama_33 prompt=standard system.experiment_name=exp1_standard_llama_394
(ok) python main.py dataset.limit=394 model=llama_33 prompt=cot system.experiment_name=exp1_cot_llama_394
(ok) python main.py dataset.limit=394 model=llama_33 prompt=decomposition system.experiment_name=exp1_decomp_llama_394
```

### Results Matrix:

| Strategy | GPT-4-mini | GPT-4 | Llama 33 |
| --- | --- | --- | --- |
| standard | ___/394 | ___/394 | ___/394 |
| cot | ___/394 | ___/394 | ___/394 |
| decomposition | ___/394 | ___/394 | ___/394 |

### Analysis:

* Best strategy for GPT-4-mini: ___
* Best strategy for GPT-4: ___
* Best strategy for Llama: ___
* Does CoT help more on complex multi-hop questions? ___
* Does strategy effect vary by model? ___

---

## Experiment 2: Entity Linking

**Question**: Does the entity linker actually matter? Which one is better?

### Commands for each model:

```bash
# === GPT-4-mini ===
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=rebel system.experiment_name=exp2_rebel_gpt4mini_394
python main.py dataset.limit=394 model=azure_gpt4_mini linking=relik system.experiment_name=exp2_relik_gpt4mini_394
python main.py dataset.limit=394 model=azure_gpt4_mini linking=all system.experiment_name=exp2_all_gpt4mini_394
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=none system.experiment_name=exp2_nolink_gpt4mini_394

# === GPT-4 ===
(ok) python main.py dataset.limit=394 model=azure_gpt4 linking=rebel system.experiment_name=exp2_rebel_gpt4_394
(ok) python main.py dataset.limit=394 model=azure_gpt4 linking=none system.experiment_name=exp2_nolink_gpt4_394

# === Llama 33 ===
(ok) python main.py dataset.limit=394 model=llama_33 linking=rebel system.experiment_name=exp2_rebel_llama_394
(ok) python main.py dataset.limit=394 model=llama_33 linking=none system.experiment_name=exp2_nolink_llama_394)
```

### Results Matrix:

| Linker | GPT-4-mini | GPT-4 | Llama 33 |
| --- | --- | --- | --- |
| REBEL | ___/394 | ___/394 | ___/394 |
| ReLiK | ___/394 | — | — |
| Both | ___/394 | — | — |
| None | ___/394 | ___/394 | ___/394 |

### Analysis:

* Does entity linking help more for weaker models? ___
* Best linker overall: ___
* If None >= REBEL: linker is introducing noise, check entity filter ___
* Does GPT-4 need the linker less than GPT-4-mini? ___

---

## Experiment 3: Self-Correction

**Question**: How many correction attempts are actually useful?

### Commands for each model:

```bash
# === GPT-4-mini ===
python main.py dataset.limit=394 model=azure_gpt4_mini validation.enable_correction=false system.experiment_name=exp3_nocorrect_gpt4mini_394
python main.py dataset.limit=394 model=azure_gpt4_mini validation.enable_correction=true validation.max_attempts=3 system.experiment_name=exp3_3attempts_gpt4mini_394
python main.py dataset.limit=394 model=azure_gpt4_mini validation.enable_correction=true validation.max_attempts=5 system.experiment_name=exp3_5attempts_gpt4mini_394

# === GPT-4 ===
python main.py dataset.limit=394 model=azure_gpt4 validation.enable_correction=false system.experiment_name=exp3_nocorrect_gpt4_394
python main.py dataset.limit=394 model=azure_gpt4 validation.enable_correction=true validation.max_attempts=3 system.experiment_name=exp3_3attempts_gpt4_394

# === Llama 33 ===
python main.py dataset.limit=394 model=llama_33 validation.enable_correction=false system.experiment_name=exp3_nocorrect_llama_394
python main.py dataset.limit=394 model=llama_33 validation.enable_correction=true validation.max_attempts=3 system.experiment_name=exp3_3attempts_llama_394
```

### Results Matrix:

| Correction | GPT-4-mini | GPT-4 | Llama 33 |
| --- | --- | --- | --- |
| None | ___/394 | ___/394 | ___/394 |
| 3 attempts | ___/394 | ___/394 | ___/394 |
| 5 attempts | ___/394 | — | — |

### Analysis:

* Which model benefits most from correction? ___
* Correction improvement by model:
  * GPT-4-mini: +___%
  * GPT-4: +___%
  * Llama: +___%
* Is 5 attempts better than 3? Or diminishing returns? ___

---

## Experiment 4: Few-Shot Retrieval

**Question**: How many examples should I retrieve?

### Commands for each model:

```bash
# === GPT-4-mini ===
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini retrieval.k=0 system.experiment_name=exp4_0shot_gpt4mini_394
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini retrieval.k=1 system.experiment_name=exp4_1shot_gpt4mini_394
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini retrieval.k=3 system.experiment_name=exp4_3shot_gpt4mini_394
(ok)python main.py dataset.limit=394 model=azure_gpt4_mini retrieval.k=5 system.experiment_name=exp4_5shot_gpt4mini_394

# === GPT-4 ===
(ok) python main.py dataset.limit=394 model=azure_gpt4 retrieval.k=0 system.experiment_name=exp4_0shot_gpt4_394
(ok) python main.py dataset.limit=394 model=azure_gpt4 retrieval.k=3 system.experiment_name=exp4_3shot_gpt4_394
(ok) python main.py dataset.limit=394 model=azure_gpt4 retrieval.k=5 system.experiment_name=exp4_5shot_gpt4_394

# === Llama 33 ===
(ok) python main.py dataset.limit=394 model=llama_33 retrieval.k=0 system.experiment_name=exp4_0shot_llama_394
(ok) python main.py dataset.limit=394 model=llama_33 retrieval.k=1 system.experiment_name=exp4_1shot_llama_394
(ok) python main.py dataset.limit=394 model=llama_33 retrieval.k=3 system.experiment_name=exp4_3shot_llama_394
(ok) python main.py dataset.limit=394 model=llama_33 retrieval.k=5 system.experiment_name=exp4_5shot_llama_394
```

### Results Matrix:

| Examples | GPT-4-mini | GPT-4 | Llama 33 |
| --- | --- | --- | --- |
| 0-shot | ___/394 | ___/394 | ___/394 |
| 1-shot | ___/394 | — | ___/394 |
| 3-shot | ___/394 | ___/394 | ___/394 |
| 5-shot | ___/394 | ___/394 | ___/394 |

### Analysis:

* Does Llama need more examples than GPT? ___
* Is there a saturation point (k=3 as good as k=5)? ___
* Optimal k per model:
  * GPT-4-mini: ___
  * GPT-4: ___
  * Llama: ___

---

## Experiment 5: Self-Consistency

**Question**: Does generating multiple samples and voting help accuracy? Is it worth 3-5x the cost?

### Commands for each model:

```bash
# === GPT-4-mini ===
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini validation.self_consistency_samples=1 system.experiment_name=exp5_1sample_gpt4mini_394
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini validation.self_consistency_samples=3 validation.consistency_temperature=0.7 system.experiment_name=exp5_3samples_gpt4mini_394
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini validation.self_consistency_samples=5 validation.consistency_temperature=0.7 system.experiment_name=exp5_5samples_gpt4mini_394

# === Llama 33 (free, so worth testing all) ===
(ok) python main.py dataset.limit=394 model=llama_33 validation.self_consistency_samples=1 system.experiment_name=exp5_1sample_llama_394
(ok) python main.py dataset.limit=394 model=llama_33 validation.self_consistency_samples=3 validation.consistency_temperature=0.7 system.experiment_name=exp5_3samples_llama_394
(ok) python main.py dataset.limit=394 model=llama_33 validation.self_consistency_samples=5 validation.consistency_temperature=0.7 system.experiment_name=exp5_5samples_llama_394
```

### Results Matrix:

| Samples | GPT-4-mini | Cost factor | Llama 33 | Cost factor |
| --- | --- | --- | --- | --- |
| 1 | ___/394 | 1x | ___/394 | 1x |
| 3 | ___/394 | 3x | ___/394 | 3x |
| 5 | ___/394 | 5x | ___/394 | 5x |

### Analysis:

* Is the gain from 1→3 samples worth 3x the cost? ___
* Does voting help more for GPT-4-mini (more errors to correct)? ___

---

## Experiment 6: Agent

**Question**: 

```bash
# Default (gpt-4o-mini, rebel, 3shot, 394 domande)
python main_agentic.py prompt=agentic dataset.limit=50 system.experiment_name=exp_agentic_mini

# GPT-4o, max 8 step per domanda
python main_agentic.py prompt=agentic model=azure_gpt4 prompt.max_steps=8 dataset.limit=50

# Llama
python main_agentic.py prompt=agentic model=llama_33 dataset.limit=50
```

### Results Matrix:

| Prompt Rules | GPT-4-mini | Llama 33 | Boolean errors | Syntax errors |
| --- | --- | --- | --- | --- |
| Minimal (no rules) | ___/394 | ___/394 | ___ | ___ |
| Standard (current) | ___/394 | ___/394 | ___ | ___ |
| Strict + negative examples | ___/394 | ___/394 | ___ | ___ |

### Analysis:

* Does adding the ASK rule actually reduce boolean errors? ___
* Does the no-subquery rule help? ___
* Is strict > standard, or does over-constraining hurt? ___

---

## Experiment 7: Ablation Study

**Question**: What actually matters in the pipeline? Which components can I remove?

This is the most important experiment for the thesis.

### Commands for each model:

```bash
# === GPT-4-mini (full ablation) ===

# 1. Pure LLM — no tools at all
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=none retrieval.k=0 prompt.include_schema_hint=false prompt.include_entities=false system.experiment_name=exp7_pure_gpt4mini_394

# 2. Linker only
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=rebel retrieval.k=0 prompt.include_schema_hint=false system.experiment_name=exp7_linker_only_gpt4mini_394

# 3. RAG only
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=none retrieval.k=3 prompt.include_schema_hint=false prompt.include_entities=false system.experiment_name=exp7_rag_only_gpt4mini_394

# 4. Schema hints only
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=none retrieval.k=0 prompt.include_schema_hint=true prompt.include_entities=false system.experiment_name=exp7_schema_only_gpt4mini_394

# 5. Linker + RAG (no schema)
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=rebel retrieval.k=3 prompt.include_schema_hint=false system.experiment_name=exp7_linker_rag_gpt4mini_394

# 6. Linker + Schema (no RAG)
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=rebel retrieval.k=0 prompt.include_schema_hint=true system.experiment_name=exp7_linker_schema_gpt4mini_394

# 7. RAG + Schema (no linker)
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=none retrieval.k=3 prompt.include_schema_hint=true prompt.include_entities=false system.experiment_name=exp7_rag_schema_gpt4mini_394

# 8. Full system (all tools)
(ok) python main.py dataset.limit=394 model=azure_gpt4_mini linking=rebel retrieval.k=3 prompt.include_schema_hint=true system.experiment_name=exp7_full_gpt4mini_394


# === GPT-4 (key configs only) ===

# 1. Pure LLM
(ok) python main.py dataset.limit=394 model=azure_gpt4 linking=none retrieval.k=0 prompt.include_schema_hint=false prompt.include_entities=false system.experiment_name=exp7_pure_gpt4_394

# 2. Full system
(ok) python main.py dataset.limit=394 model=azure_gpt4 linking=rebel retrieval.k=3 prompt.include_schema_hint=true system.experiment_name=exp7_full_gpt4_394


# === Llama 33 ===

# 1. Pure LLM
(ok) python main.py dataset.limit=394 model=llama_33 linking=none retrieval.k=0 prompt.include_schema_hint=false prompt.include_entities=false system.experiment_name=exp7_pure_llama_394

# 2. Linker only
(ok) python main.py dataset.limit=394 model=llama_33 linking=rebel retrieval.k=0 prompt.include_schema_hint=false system.experiment_name=exp7_linker_only_llama_394

# 3. RAG only
(ok) python main.py dataset.limit=394 model=llama_33 linking=none retrieval.k=3 prompt.include_schema_hint=false prompt.include_entities=false system.experiment_name=exp7_rag_only_llama_394

# 4. Full system
(ok) python main.py dataset.limit=394 model=llama_33 linking=rebel retrieval.k=3 prompt.include_schema_hint=true system.experiment_name=exp7_full_llama_394
```

### Results Matrix:

| Configuration | GPT-4-mini | GPT-4 | Llama 33 |
| --- | --- | --- | --- |
| **Pure LLM** (no tools) | ___/394 | ___/394 | ___/394 |
| **Linker only** | ___/394 | — | ___/394 |
| **RAG only** | ___/394 | — | ___/394 |
| **Schema only** | ___/394 | — | — |
| **Linker + RAG** | ___/394 | — | — |
| **Linker + Schema** | ___/394 | — | — |
| **RAG + Schema** | ___/394 | — | — |
| **Full system** | ___/394 | ___/394 | ___/394 |

### Analysis:

* **Hypothesis check**: If "Pure LLM" > "Linker Only" → Linker is introducing noise
* Most impactful single component: ___
* Least impactful (candidate for removal): ___
* Does GPT-4 need the linker less than GPT-4-mini? ___
* Does Llama benefit more from RAG? ___

---

## Best Configuration (per model)

**Question**: What's the optimal config for each model on the full dataset?

Based on previous experiments, fill in the best combination:

```bash
# === GPT-4-mini: Best config ===
python main.py dataset.limit=394 \
   model=azure_gpt4_mini \
   prompt=___ \
   linking=___ \
   retrieval.k=___ \
   validation.enable_correction=___ \
   system.experiment_name=FINAL_best_gpt4mini_394

# === GPT-4: Best config ===
python main.py dataset.limit=394 \
   model=azure_gpt4 \
   prompt=___ \
   linking=___ \
   retrieval.k=___ \
   validation.enable_correction=___ \
   system.experiment_name=FINAL_best_gpt4_394

# === Llama 33: Best config ===
python main.py dataset.limit=394 \
   model=llama_33 \
   prompt=___ \
   linking=___ \
   retrieval.k=___ \
   validation.enable_correction=___ \
   system.experiment_name=FINAL_best_llama_394
```

### Final Results:

| Model | Best Config | Score |
| --- | --- | --- |
| GPT-4-mini | | ___/394 |
| GPT-4 | | ___/394 |
| Llama 33 | | ___/394 |

---

## Master Results Table

All experiments summarized:

### By Model: GPT-4-mini

| Experiment | Config | Result | Notes |
| --- | --- | --- | --- |
| 1A | standard (394) | | |
| 1B | cot (394) | | |
| 1C | decomposition (394) | | |
| 2A | rebel (394) | | |
| 2B | relik (394) | | |
| 2C | both linkers (394) | | |
| 2D | no linker (394) | | |
| 3A | no correction (394) | | |
| 3B | 3 attempts (394) | | |
| 3C | 5 attempts (394) | | |
| 4A | 0-shot (394) | | |
| 4B | 1-shot (394) | | |
| 4C | 3-shot (394) | | |
| 4D | 5-shot (394) | | |
| 5A | 1 sample (394) | | |
| 5B | 3 samples (394) | | |
| 5C | 5 samples (394) | | |
| 6A | minimal rules (394) | | |
| 6B | strict rules (394) | | |
| 7A | Pure LLM (394) | | Ablation |
| 7B | Linker only (394) | | Ablation |
| 7C | RAG only (394) | | Ablation |
| 7D | Schema only (394) | | Ablation |
| 7E | Linker + RAG (394) | | Ablation |
| 7F | Linker + Schema (394) | | Ablation |
| 7G | RAG + Schema (394) | | Ablation |
| 7H | Full system (394) | | Ablation |
| FINAL | Best composite (394) | | Primary result |

### By Model: GPT-4

| Experiment | Config | Result | Notes |
| --- | --- | --- | --- |
| 1A | standard (394) | | |
| 1B | cot (394) | | |
| 1C | decomposition (394) | | |
| 2A | rebel (394) | | |
| 2D | no linker (394) | | |
| 3A | no correction (394) | | |
| 3B | 3 attempts (394) | | |
| 4A | 0-shot (394) | | |
| 4C | 3-shot (394) | | |
| 4D | 5-shot (394) | | |
| 7A | Pure LLM (394) | | Ablation |
| 7H | Full system (394) | | Ablation |
| FINAL | Best composite (394) | | Primary result |

### By Model: Llama 33

| Experiment | Config | Result | Notes |
| --- | --- | --- | --- |
| 1A | standard (394) | | |
| 1B | cot (394) | | |
| 1C | decomposition (394) | | |
| 2A | rebel (394) | | |
| 2D | no linker (394) | | |
| 3A | no correction (394) | | |
| 3B | 3 attempts (394) | | |
| 4A | 0-shot (394) | | |
| 4B | 1-shot (394) | | |
| 4C | 3-shot (394) | | |
| 4D | 5-shot (394) | | |
| 5A | 1 sample (394) | | |
| 5B | 3 samples (394) | | |
| 5C | 5 samples (394) | | |
| 6A | minimal rules (394) | | |
| 6B | strict rules (394) | | |
| 7A | Pure LLM (394) | | Ablation |
| 7B | Linker only (394) | | Ablation |
| 7C | RAG only (394) | | Ablation |
| 7H | Full system (394) | | Ablation |
| FINAL | Best composite (394) | | Primary result |

---

## Error Analysis

After running experiments, look at the failures:

### Common error patterns:

1. **Syntax errors**:
   - Missing braces `{}`
   - Wrong prefix usage
   - Examples: _______________

2. **Wrong entities**:
   - Entity not found or wrong QID selected
   - Examples: _______________

3. **Wrong properties**:
   - Used wrong Wikidata P-id
   - Examples: _______________

4. **Boolean errors**:
   - Used SELECT instead of ASK for yes/no questions
   - Examples: _______________

5. **Empty results**:
   - Query is valid but returns nothing
   - Usually wrong entity or property
   - Examples: _______________

### Failed queries to investigate:

| Question | What went wrong | Ideas to fix |
| --- | --- | --- |
| | | |
| | | |
| | | |

---

## My Conclusions

### Model comparison:

* Best overall: ___
* Best cost/performance: ___
* Llama vs GPT: ___

### What clearly helped (across all models):

1.
2.
3.

### What didn't help much:

1.
2.

### Recommended configuration:

**For production (cost-sensitive)**:

```bash
python main.py model=___ prompt=___ linking=___ retrieval.k=___
```

**For maximum accuracy (cost doesn't matter)**:

```bash
python main.py model=___ prompt=___ linking=___ validation.enable_correction=true validation.max_attempts=3
```

---

## Cost Tracking

| Date | Model | Experiment | API Calls | Est. Cost | Total |
| --- | --- | --- | --- | --- | --- |
| | GPT-4-mini | test (all, 10q x 10) | ~100 | ~$0.01 | |
| | GPT-4-mini | Exp 1 (3 runs x 394) | ~1,182 | ~$0.15 | |
| | GPT-4-mini | Exp 2 (4 runs x 394) | ~1,576 | ~$0.20 | |
| | GPT-4-mini | Exp 3 (3 runs x 394) | ~1,182 | ~$0.15 | |
| | GPT-4-mini | Exp 4 (4 runs x 394) | ~1,576 | ~$0.20 | |
| | GPT-4-mini | Exp 5 (3 runs x 394, up to 5x) | ~5,910 | ~$0.45 | |
| | GPT-4-mini | Exp 6 (3 runs x 394) | ~1,182 | ~$0.15 | |
| | GPT-4-mini | Exp 7 (8 runs x 394) | ~3,152 | ~$0.40 | |
| | GPT-4 | Selected runs (~2,000 calls) | ~2,000 | ~$12.00 | |
| | Llama 33 | All experiments | any | $0 | |
| **Total** | | | | | |

---

## Checklist

### Before any run:
* [ ] Sanity check passed (limit=2)
* [ ] test  passed for this config (limit=10)
* [ ] experiment_name is unique
* [ ] Azure credits available

### GPT-4-mini experiments:

* [ ] Exp 1: Prompting (standard, cot, decomp)
* [ ] Exp 2: Entity linking (rebel, relik, all, none)
* [ ] Exp 3: Correction (none, 3 attempts, 5 attempts)
* [ ] Exp 4: Retrieval (0, 1, 3, 5-shot)
* [ ] Exp 5: Self-consistency (1, 3, 5 samples)
* [ ] Exp 6: Prompt rules (minimal, strict)
* [ ] Exp 7: Ablation (all 8 configurations)
* [ ] FINAL: Best composite config

### GPT-4 experiments:

* [ ] Exp 1: Prompting (standard, cot, decomp)
* [ ] Exp 2: Entity linking (rebel, none)
* [ ] Exp 3: Correction (none, 3 attempts)
* [ ] Exp 4: Retrieval (0, 3, 5-shot)
* [ ] Exp 7: Ablation (pure LLM, full system)
* [ ] FINAL: Best composite config

### Llama 33 experiments:

* [ ] Exp 1: Prompting (standard, cot, decomp)
* [ ] Exp 2: Entity linking (rebel, none)
* [ ] Exp 3: Correction (none, 3 attempts)
* [ ] Exp 4: Retrieval (0, 1, 3, 5-shot)
* [ ] Exp 5: Self-consistency (1, 3, 5 samples)
* [ ] Exp 6: Prompt rules (minimal, strict)
* [ ] Exp 7: Ablation (pure LLM, linker only, RAG only, full)
* [ ] FINAL: Best composite config

### Final:

* [ ] Best config per model identified
* [ ] Error analysis done on best config outputs
* [ ] Results documented
* [ ] GERBIL evaluation submitted





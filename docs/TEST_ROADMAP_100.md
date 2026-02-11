# Test Plan & Experiments Log

Testing roadmap for the thesis project. I'll use this to track what I've tried, what worked, and what didn't.

**Started**: February 2026

---

## Models to Test

Every experiment below should be repeated for each model:

| Model ID | Config | Notes |
|----------|--------|-------|
| **M1** | `model=azure_gpt4_mini` | Cheapest, baseline |
| **M2** | `model=azure_gpt4` | More expensive, better? |
| **M3** | `model=llama_33` | More expensive, better?|

**Naming convention**: `exp{N}_{test}_{model}`
- Example: `exp1_cot_gpt4mini`, `exp1_cot_gpt4`, `exp1_cot_llama`

---

## Before Starting: Sanity Checks

I always run these first to make sure nothing is broken:

```bash
# Does the code even run?
python main.py dataset.limit=2

# Can I see the prompts? (no API calls, safe to run)
python src/debug/prompts.py prompt=cot linking.device=-1
```

If any of these fail, I need to fix that first before running experiments.

---

## Research Questions

These are the things I'm actually trying to figure out:

1. **Does Chain-of-Thought help?** 
   - Hypothesis: CoT should help with complex multi-hop questions
   - But maybe it's overkill for simple questions?

2. **Which entity linker is better?**
   - REBEL is older but more stable
   - ReLiK is newer, supposedly faster
   - Using both together might be best but slower

3. **Is self-correction worth the extra API calls?**
   - Each retry costs money
   - But if it fixes 30% of errors, probably worth it?

4. **How many examples do I need?**
   - 0-shot: model uses only its training
   - 3-shot: more context but longer prompt
   - Trade-off between accuracy and token cost

5. **Does the model matter more than the prompting strategy?**
   - Maybe GPT-4 with simple prompting beats GPT-4-mini with CoT?

---

## Experiment 1: Prompting Strategies (per model)

**Question**: Which prompting strategy works best for this task?

### Commands for each model:

```bash
# === GPT-4-mini ===
python main.py dataset.limit=100 model=azure_gpt4_mini prompt=standard system.experiment_name=exp1_standard_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini prompt=cot system.experiment_name=exp1_cot_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini prompt=decomposition system.experiment_name=exp1_decomp_gpt4mini_100

# === GPT-4 ===
python main.py dataset.limit=100 model=azure_gpt4 prompt=standard system.experiment_name=exp1_standard_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 prompt=cot system.experiment_name=exp1_cot_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 prompt=decomposition system.experiment_name=exp1_decomp_gpt4_100

# === Llama 33 ===
python main.py dataset.limit=100 model=llama_33 prompt=standard system.experiment_name=exp1_standard_llama_100
python main.py dataset.limit=100 model=llama_33 prompt=cot system.experiment_name=exp1_cot_llama_100
python main.py dataset.limit=100 model=llama_33 prompt=decomposition system.experiment_name=exp1_decomp_llama_100
```

### Results Matrix:

| Strategy | GPT-4-mini | GPT-4 | Llama 33 |
|----------|------------|-------|-----------|
| standard | ___/100 | ___/100 | ___/100 |
| cot | ___/100 | ___/100 | ___/100 |
| decomposition | ___/100 | ___/100 | ___/100 |

### Analysis:
- Best strategy for GPT-4-mini: ___
- Best strategy for GPT-4: ___
- Best strategy for Llama: ___
- Does strategy effect vary by model? ___

---

## Experiment 2: Entity Linking (per model)

**Question**: Does the entity linker actually matter? Which one finds more correct QIDs?

### Commands for each model:

```bash
# === GPT-4-mini ===
python main.py dataset.limit=100 model=azure_gpt4_mini linking=rebel system.experiment_name=exp2_rebel_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini linking=relik system.experiment_name=exp2_relik_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini linking=all system.experiment_name=exp2_all_gpt4mini_100

# === GPT-4 ===
python main.py dataset.limit=100 model=azure_gpt4 linking=rebel system.experiment_name=exp2_rebel_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 linking=relik system.experiment_name=exp2_relik_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 linking=all system.experiment_name=exp2_all_gpt4_100

# === Llama 33 ===
python main.py dataset.limit=100 model=llama_33 linking=rebel system.experiment_name=exp2_rebel_llama_100
python main.py dataset.limit=100 model=llama_33 linking=relik system.experiment_name=exp2_relik_llama_100
python main.py dataset.limit=100 model=llama_33 linking=all system.experiment_name=exp2_all_llama_100
```

### Results Matrix:

| Linker | GPT-4-mini | GPT-4 | Llama 33 |
|--------|------------|-------|-----------|
| REBEL | ___/100 | ___/100 | ___/100 |
| ReLiK | ___/100 | ___/100 | ___/100 |
| Both | ___/100 | ___/100 | ___/100 |

### Analysis:
- Does entity linking help more for weaker models? ___
- Best linker overall: ___

---

## Experiment 3: Self-Correction (per model)

**Question**: How many correction attempts are actually useful? Is there a point of diminishing returns?

### Commands for each model:

```bash
# === GPT-4-mini ===
python main.py dataset.limit=100 model=azure_gpt4_mini validation.enable_correction=false system.experiment_name=exp3_nocorrect_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini validation.enable_correction=true validation.max_attempts=3 system.experiment_name=exp3_3attempts_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini validation.enable_correction=true validation.max_attempts=5 system.experiment_name=exp3_5attempts_gpt4mini_100

# === GPT-4 ===
python main.py dataset.limit=100 model=azure_gpt4 validation.enable_correction=false system.experiment_name=exp3_nocorrect_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 validation.enable_correction=true validation.max_attempts=3 system.experiment_name=exp3_3attempts_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 validation.enable_correction=true validation.max_attempts=5 system.experiment_name=exp3_5attempts_gpt4_100

# === Llama 33 ===
python main.py dataset.limit=100 model=llama_33 validation.enable_correction=false system.experiment_name=exp3_nocorrect_llama_100
python main.py dataset.limit=100 model=llama_33 validation.enable_correction=true validation.max_attempts=3 system.experiment_name=exp3_3attempts_llama_100
python main.py dataset.limit=100 model=llama_33 validation.enable_correction=true validation.max_attempts=5 system.experiment_name=exp3_5attempts_llama_100
```

### Results Matrix:

| Correction | GPT-4-mini | GPT-4 | Llama 33 |
|------------|------------|-------|-----------|
| None | ___/100 | ___/100 | ___/100 |
| 3 attempts | ___/100 | ___/100 | ___/100 |
| 5 attempts | ___/100 | ___/100 | ___/100 |

### Analysis:
- Which model benefits most from correction? ___
- Correction improvement by model:
  - GPT-4-mini: +___% 
  - GPT-4: +___%
  - Llama: +___%

---

## Experiment 4: Few-Shot Retrieval (per model)

**Question**: How many examples should I retrieve? More = better? Or just more tokens?

### Commands for each model:

```bash
# === GPT-4-mini ===
python main.py dataset.limit=100 model=azure_gpt4_mini retrieval.k=0 system.experiment_name=exp4_0shot_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini retrieval=1shot system.experiment_name=exp4_1shot_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini retrieval=3shot system.experiment_name=exp4_3shot_gpt4mini_100

# === GPT-4 ===
python main.py dataset.limit=100 model=azure_gpt4 retrieval.k=0 system.experiment_name=exp4_0shot_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 retrieval=1shot system.experiment_name=exp4_1shot_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 retrieval=3shot system.experiment_name=exp4_3shot_gpt4_100

# === Llama 33 ===
python main.py dataset.limit=100 model=llama_33 retrieval.k=0 system.experiment_name=exp4_0shot_llama_100
python main.py dataset.limit=100 model=llama_33 retrieval=1shot system.experiment_name=exp4_1shot_llama_100
python main.py dataset.limit=100 model=llama_33 retrieval=3shot system.experiment_name=exp4_3shot_llama_100
```

### Results Matrix:

| Examples | GPT-4-mini | GPT-4 | Llama 33 |
|----------|------------|-------|-----------|
| 0-shot | ___/100 | ___/100 | ___/100 |
| 1-shot | ___/100 | ___/100 | ___/100 |
| 3-shot | ___/100 | ___/100 | ___/100 |

### Analysis:
- Does Llama need more examples than GPT? ___
- Optimal k per model:
  - GPT-4-mini: ___
  - GPT-4: ___
  - Llama: ___

---

## Experiment 5: Self-Consistency (per model)

**Question**: Does generating multiple samples and voting help accuracy? Is it worth 3-5x the cost?

### Commands for each model:

```bash
# === GPT-4-mini ===
python main.py dataset.limit=100 model=azure_gpt4_mini validation.self_consistency_samples=1 system.experiment_name=exp5_1sample_gpt4mini_100
python main.py dataset.limit=100 model=azure_gpt4_mini validation.self_consistency_samples=3 system.experiment_name=exp5_3samples_gpt4mini_100

# === GPT-4 ===
python main.py dataset.limit=100 model=azure_gpt4 validation.self_consistency_samples=1 system.experiment_name=exp5_1sample_gpt4_100
python main.py dataset.limit=100 model=azure_gpt4 validation.self_consistency_samples=3 system.experiment_name=exp5_3samples_gpt4_100

# === Llama 33 ===
python main.py dataset.limit=100 model=llama_33 validation.self_consistency_samples=1 system.experiment_name=exp5_1sample_llama_100
python main.py dataset.limit=100 model=llama_33 validation.self_consistency_samples=3 system.experiment_name=exp5_3samples_llama_100
```

### Results Matrix:

| Samples | GPT-4-mini | GPT-4 | Llama 33 |
|---------|------------|-------|-----------|
| 1 | ___/20 | ___/20 | ___/20 |
| 3 | ___/20 | ___/20 | ___/20 |

### Analysis:
- Self-consistency improvement by model: ___

---

## Experiment 6: Best Configuration (per model)

**Question**: What's the optimal config for each model?

Based on previous experiments, test the best combination for each:

```bash
# === GPT-4-mini: Best config ===
python main.py dataset.limit=100 \
   model=azure_gpt4_mini \
   prompt=___ \
   linking=___ \
   retrieval=___ \
   validation.enable_correction=___ \
   system.experiment_name=exp6_best_gpt4mini_100

# === GPT-4: Best config ===
python main.py dataset.limit=100 \
   model=azure_gpt4 \
   prompt=___ \
   linking=___ \
   retrieval=___ \
   validation.enable_correction=___ \
   system.experiment_name=exp6_best_gpt4_100

# === Llama 33: Best config ===
python main.py dataset.limit=100 \
   model=llama_33 \
   prompt=___ \
   linking=___ \
   retrieval=___ \
   validation.enable_correction=___ \
   system.experiment_name=exp6_best_llama_100
```

### Final Results:

| Model | Best Config | Accuracy |
|-------|-------------|----------|
| GPT-4-mini | | ___/50 |
| GPT-4 | | ___/50 |
| Llama 33 | | ___/50 |

---

## Master Results Table

All experiments summarized:

### By Model: GPT-4-mini

| Experiment | Config | Result | Notes |
|------------|--------|--------|-------|
| 1A | standard (100) | | |
| 1B | cot (100) | | |
| 1C | decomposition (100) | | |
| 2A | rebel (100) | | |
| 2B | relik (100) | | |
| 3A | no correction (100) | | |
| 3B | 3 attempts (100) | | |
| 4A | 0-shot (100) | | |
| 4C | 3-shot (100) | | |

### By Model: GPT-4

| Experiment | Config | Result | Notes |
|------------|--------|--------|-------|
| 1A | standard (100) | | |
| 1B | cot (100) | | |
| 1C | decomposition (100) | | |
| 2A | rebel (100) | | |
| 2B | relik (100) | | |
| 3A | no correction (100) | | |
| 3B | 3 attempts (100) | | |
| 4A | 0-shot (100) | | |
| 4C | 3-shot (100) | | |

### By Model: Llama 33

| Experiment | Config | Result | Notes |
|------------|--------|--------|-------|
| 1A | standard (100) | | |
| 1B | cot (100) | | |
| 1C | decomposition (100) | | |
| 2A | rebel (100) | | |
| 2B | relik (100) | | |
| 3A | no correction (100) | | |
| 3B | 3 attempts (100) | | |
| 4A | 0-shot (100) | | |
| 4C | 3-shot (100) | | |

---


## Error Analysis

After running experiments, I need to look at the failures:

### Common error patterns I've seen:

1. **Syntax errors**: 
   - Missing braces `{}`
   - Wrong prefix usage
   - Examples: _______________

2. **Wrong entities**:
   - Entity not found
   - Wrong QID selected
   - Examples: _______________

3. **Wrong properties**:
   - Used wrong Wikidata property
   - Property doesn't exist
   - Examples: _______________

4. **Empty results**:
   - Query is valid but returns nothing
   - Usually wrong entity or property
   - Examples: _______________

### Failed queries to investigate:

| Question | What went wrong | Ideas to fix |
|----------|-----------------|--------------|
| | | |
| | | |
| | | |

---

## My Conclusions

### Model comparison:
- Best overall: ___
- Best cost/performance: ___
- Llama vs GPT: ___

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
python main.py model=___ prompt=___ linking=___ retrieval=___
```

**For maximum accuracy (cost doesn't matter)**:
```bash
python main.py model=___ prompt=___ linking=___ validation.enable_correction=true
```

---

## Cost Tracking

| Date | Model | Experiment | API Calls | Est. Cost | Total |
|------|-------|------------|-----------|-----------|-------|
| | GPT-4-mini | | | | |
| | GPT-4 | | | | |
| | Llama | | | $0 | |
| **Total** | | | | | |

---

## Checklist

### GPT-4-mini experiments:
- [ ] Exp 1: Prompting (standard, cot, decomp)
- [ ] Exp 2: Entity linking (rebel, relik)
- [ ] Exp 3: Correction (none, 3 attempts)
- [ ] Exp 4: Retrieval (0-shot, 3-shot)
- [ ] Exp 5: Self-consistency

### GPT-4 experiments:
- [ ] Exp 1: Prompting
- [ ] Exp 2: Entity linking
- [ ] Exp 3: Correction
- [ ] Exp 4: Retrieval
- [ ] Exp 5: Self-consistency

### Llama 33 experiments:
- [ ] Exp 1: Prompting
- [ ] Exp 2: Entity linking
- [ ] Exp 3: Correction
- [ ] Exp 4: Retrieval
- [ ] Exp 5: Self-consistency

### Final:
- [ ] Best config per model identified
- [ ] Results documented
- [ ] Thesis section written

---

## Notes & Random Thoughts

**2026-02-__**:


**2026-02-__**:


**2026-02-__**:

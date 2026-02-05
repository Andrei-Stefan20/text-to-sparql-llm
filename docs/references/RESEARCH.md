# Research Notes & TODO

Personal notes for the Text-to-SPARQL project. Work in progress.

---

## Main Goal

Translate natural language → SPARQL for Wikidata with minimal errors.

**Key questions I'm exploring:**
- Which prompting strategy works best? (few-shot vs CoT vs decomposition)
- Does entity linking actually help?
- Can the model fix its own mistakes? (self-correction)
- RAG vs fine-tuning: what's more practical?

---

## Background Reading

### Text-to-SQL vs Text-to-SPARQL

Text-to-SQL has mature benchmarks (Spider, WikiSQL). SPARQL is harder because:
- Need to link entities to Wikidata IDs (millions of them)
- SPARQL syntax is more complex (OPTIONAL, FILTER, etc.)
- Schema is a knowledge graph, not a database

### Approaches I Found

| Approach | Notes |
|----------|-------|
| Fine-tuning | Best accuracy but needs data + compute |
| In-context learning | No training, but limited by context window |
| RAG + ICL | What I'm using - retrieve similar examples |
| Agentic | LLM uses tools, can self-correct - interesting but slow |

---

## Papers I've Read

### Chain-of-Thought (Wei et al., 2022)
[arXiv](https://arxiv.org/abs/2201.11903)

- "Let's think step by step" actually works
- Helps with complex reasoning
- **Implemented**: `prompt=cot`

### Self-Consistency (Wang et al., 2023)
[arXiv](https://arxiv.org/abs/2203.11171)

- Generate multiple answers, vote for best one
- Reduces random errors
- **Implemented**: `validation.self_consistency_samples`

### Self-Refine (Madaan et al., 2023)
[arXiv](https://arxiv.org/abs/2303.17651)

- LLM critiques and fixes its own output
- Works well for code generation
- **Implemented**: `validation.enable_correction`

### REBEL (Huguet Cabot & Navigli, 2021)
[arXiv](https://arxiv.org/abs/2104.07650)

- End-to-end relation extraction
- **Implemented**: `linking=rebel`

### ReLiK (Orlando et al., 2024)
[arXiv](https://arxiv.org/abs/2401.06394)

- Fast entity linking
- **Implemented**: `linking=relik`

### Decomposed Prompting (Khot et al., 2022)
[arXiv](https://arxiv.org/abs/2210.02406)

- Break complex tasks into subtasks
- **Implemented**: `prompt=decomposition`

### Self-Debugging (Chen et al., 2023)
[arXiv](https://arxiv.org/abs/2304.05128)

- Use execution results to fix code
- **TODO**: extend my correction loop with this

---

## TODO: Things to Try

### High Priority
- [ ] **Constrained decoding** - force valid SPARQL syntax at generation time
  - Check out [Outlines](https://github.com/outlines-dev/outlines) or [Guidance](https://github.com/guidance-ai/guidance)
- [ ] **Better entity linking** - mGENRE or BLINK might work better
- [ ] **Execution-guided correction** - use query results as feedback

### Medium Priority
- [ ] **LoRA fine-tuning** on Llama with QALD data
- [ ] **Plan-and-Solve prompting** - seems promising for complex queries
- [ ] **Tree-of-Thought** - multiple reasoning paths

### Low Priority / Future Work
- [ ] Agentic approach with tool use
- [ ] Multi-hop reasoning
- [ ] Multilingual support

---

## Progress

### Done
- [x] Basic RAG pipeline working
- [x] Entity linking with REBEL and ReLiK
- [x] Syntax validation with rdflib
- [x] Self-correction loop (up to N attempts)
- [x] Chain-of-Thought prompting
- [x] Query decomposition strategy
- [x] Self-consistency voting

### In Progress
- [ ] Testing different configurations systematically
- [ ] Improving extraction of SPARQL from LLM responses

### Blocked / Need Help
- [ ] Getting consistent Wikidata QIDs from entity linkers
- [ ] Handling queries that return empty results

---

## Datasets

| Dataset | Size | Notes |
|---------|------|-------|
| QALD-9 | 558 | Using this now |
| QALD-10 | 412 | Harder, more recent |
| LC-QuAD 2.0 | 30K | Much bigger, could use for fine-tuning |
| SimpleQuestions | 100K | Easy, single-hop only |

Links:
- [QALD](https://github.com/ag-sc/QALD)
- [LC-QuAD](https://github.com/AskNowQA/LC-QuAD2.0)

---

## Metrics I'm Tracking

| Metric | What it measures |
|--------|------------------|
| Syntax Valid % | Does the query parse? |
| Exact Match | Query = gold query? |
| Execution Accuracy | Same results as gold? |
| Correction Success % | Fixed after retries? |

---

## Useful Resources

**Wikidata**
- [SPARQL Endpoint](https://query.wikidata.org/) - test queries here
- [SPARQL Tutorial](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial)

**Entity Linking**
- [ReLiK repo](https://github.com/SapienzaNLP/relik)
- [REBEL repo](https://github.com/Babelscape/rebel)

**Tools I'm Using**
- [Hydra](https://hydra.cc/) - config management
- [FAISS](https://github.com/facebookresearch/faiss) - vector search
- [rdflib](https://rdflib.readthedocs.io/) - SPARQL parsing

---

## References

```bibtex
@article{wei2022chain,
  title={Chain-of-thought prompting elicits reasoning in large language models},
  author={Wei, Jason and others},
  journal={NeurIPS},
  year={2022}
}

@article{wang2023selfconsistency,
  title={Self-consistency improves chain of thought reasoning in language models},
  author={Wang, Xuezhi and others},
  journal={ICLR},
  year={2023}
}

@article{madaan2023selfrefine,
  title={Self-refine: Iterative refinement with self-feedback},
  author={Madaan, Aman and others},
  journal={NeurIPS},
  year={2023}
}

@article{huguet2021rebel,
  title={REBEL: Relation extraction by end-to-end language generation},
  author={Huguet Cabot, Pere-Lluis and Navigli, Roberto},
  journal={EMNLP},
  year={2021}
}

@article{orlando2024relik,
  title={Retrieve, Read and LinK: Fast and Accurate Entity Linking},
  author={Orlando, Riccardo and others},
  journal={arXiv},
  year={2024}
}
```

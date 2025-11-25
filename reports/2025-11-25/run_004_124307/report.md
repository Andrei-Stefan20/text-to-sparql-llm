# Text-to-SPARQL Report

**Model:** `ACE-deepseek-coder-6.7b-instruct.Q4_K_M.gguf`
**Date:** 2025-11-25

| Metric | Value |
|---|---|
| Syntax Accuracy | 50.00% |
| Answer Accuracy | 50.00% |
| Avg F1 Score | 0.5000 |
| Self-Corrections | 0 |

---

### Q1: CORRECT
**Input:** After whom is the Riemannian geometry named?

> **Error:** `Success: None`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q761383 wdt:P138 ?result. }` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?result WHERE {   wd:Q761383 wdt:P138 ?result. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q42299`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q42299`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
No specific strategies yet.
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
No specific strategies yet.

### STANDARD PREFIXES:
PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

### INSTRUCTIONS:
1. Use the Schema provided below.
2. Apply the strategies from the Playbook.
3. Output ONLY the SPARQL query inside a ```sparql``` block.

### FEW-SHOT EXAMPLES (Reference Only):
Q: What was Ada Lovelace’s noble title?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q7259 wdt:P97 ?result}
```

Q: Who founded the architectural firm who planned the Elbphilharmonie?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q673223 wdt:P84/wdt:P112 ?result}
```

Q: Who were the parents of Socrates ?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {{wd:Q913 wdt:P25 ?result} UNION {wd:Q913 wdt:P22 ?result}}
```

### SCHEMA CONTEXT:
- Riemannian geometry (Q761383): branch of differential geometry dealing with (generalized) Riemannian manifolds
- named after (P138): entity or event that inspired the subject's name, or namesake (in at least one language). Qualifier "applies to name" (P5168) can be used to indicate which one

### USER QUESTION:
After whom is the Riemannian geometry named?

### SOLUTION:
```sparql
````
</details>

---
### Q2: SYNTAX ERR
**Input:** Which animal participated in a military operation with the Australian Defence Force?

> **Error:** `Error: Syntax Error: Line 12, Col 66: Expected Expected SelectQuery`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  SELECT ?animal ?animalLabel WHERE {   ?operation wdt:P31 wd:Q645883; # instance of military operation             wdt:P1344 wd:Q625657. # participant is the Australian Defence Force   ?animal p:P31/ps:P31 ?operation. # animal is an instance of the` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q93208`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 3
<details><summary>Debug Info</summary>

**Context:**
```text
- Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.


### STANDARD PREFIXES:
PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

### INSTRUCTIONS:
1. Use the Schema provided below.
2. Apply the strategies from the Playbook.
3. Output ONLY the SPARQL query inside a ```sparql``` block.

### FEW-SHOT EXAMPLES (Reference Only):
Q: With how many countries does Australia share a border?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?country) AS ?result) WHERE {wd:Q408 wdt:P47 ?country. ?country p:P31/ps:P31 wd:Q6256}
```

Q: From which country are the beagles originally from?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q21102 wdt:P495 ?result}
```

Q: How many casualties were a result of the Troubles?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q815436 wdt:P1120 ?result}
```

### SCHEMA CONTEXT:
- instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- military operation (Q645883): coordinated military actions of a state or a non-state actor
- participant (P710): person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.
- Australian Defence Force (Q625657): combined military forces of Australia
- taxon (Q16521): group of one or more organism(s), which a taxonomist adjudges to be a unit

### USER QUESTION:
Which animal participated in a military operation with the Australian Defence Force?

### SOLUTION:
```sparql
````
</details>

---

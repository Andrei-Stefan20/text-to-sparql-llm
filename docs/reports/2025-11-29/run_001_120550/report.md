# Text-to-SPARQL Evaluation Report

**Model:** `Qwen_Qwen2.5-Coder-3B-Instruct`
**Timestamp:** 2025-11-29 12:19:44

## Summary Metrics
| Metric | Value |
|---|---|
| Total Questions | 20 |
| Syntax Accuracy | 85.00% |
| Answer Accuracy | 15.00% |
| Average F1 Score | 0.1750 |
| Successful Retries | 1 |

---

## Detailed Results

### Q20: [FAIL] Did Rawson Marshall Thurber, the director of Red Notice also direct Titanic?

**Error:** `Syntax Error: Line 1, Col 766: Expected Expected AskQuery`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q58815001 wdt:P57 wd:Q2745616. wd:Q44578 wdt:P57 wd:Q2745616. FILTER(?wd:Q58815001 != ?wd:Q44578)}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q58815001 wdt:P57 ?director. wd:Q44578 wdt:P57 ?director. FILTER(wd:Q2745616 = ?director)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: Tell me all the cast members of the film Red Notice directed by Rawson Marshall Thurber ?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q58815001 wdt:P57 wd:Q2745616; wdt:P161 ?result}
```

User: When the film Red Notice was released?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q58815001 wdt:P577 ?result}
```

User: Was Funny Games and its remake directed by different persons?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q696928 wdt:P57 ?dir. wd:Q951002 wdt:P57 ?dir2. FILTER(?dir != ?dir2)}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P57 (director) - director(s) of film, TV-series, stageplay, video game or similar

--- ENTITIES (Items/Objects) ---
wd:Q58815001 (Red Notice) - 2021 film directed by Rawson Marshall Thurber
wd:Q2745616 (Rawson Marshall Thurber) - American film director
wd:Q44578 (Titanic) - 1997 film by James Cameron

### User Question:
Did Rawson Marshall Thurber, the director of Red Notice also direct Titanic?

```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q58815001 wdt:P57 wd:Q2745616. wd:Q44578 wdt:P57 wd:Q2745616. FILTER(?wd:Q58815001 != ?wd:Q44578)}
```

SYSTEM: Invalid Query. Line 1, Col 766: Expected Expected AskQuery
Fix it.
Corrected Query: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q58815001 wdt:P57 wd:Q2745616. wd:Q44578 wdt:P57 wd:Q2745616. FILTER(?wd:Q58815001 != ?wd:Q44578)}
```

SYSTEM: Invalid Query. Line 1, Col 766: Expected Expected AskQuery
Fix it.
Corrected Query: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q58815001 wdt:P57 wd:Q2745616. wd:Q44578 wdt:P57 wd:Q2745616. FILTER(?wd:Q58815001 != ?wd:Q44578)}
```

SYSTEM: Invalid Query. Line 1, Col 766: Expected Expected AskQuery
Fix it.
Corrected Query: ```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q58815001 wdt:P57 wd:Q2745616. wd:Q44578 wdt:P57 wd:Q2745616. FILTER(?wd:Q58815001 != ?wd:Q44578)}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 4
---
### Q19: [FAIL] Did Kobe Bryant leave the Lakers when LeBron James joined that team?

**Error:** `Execution Error: EndPointInternalError: The endpoint returned the HTTP status code 500. `

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 wd:Q121783. wd:Q36159 wdt:P54 wd:Q121783. FILTER(wdt:P582(wd:Q25369) > wdt:P580(wd:Q36159))}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q25369 p:P54 ?teamStatement. ?teamStatement ps:P54 wd:Q121783; pq:P582 ?leave. wd:Q36159 p:P54 ?teamStatement2. ?teamStatement2 ps:P54 wd:Q121783; pq:P580 ?join. FILTER(?leave = ?join)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: Did Michael Jordan and Kobe Bryant play for the same team?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 ?team. wd:Q41421 wdt:P54 ?team.}
```

User: Was Shaquille O'Neal the teammate of Kobe Bryant in the year of 2000?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 p:P54 ?ps1. ?ps1 ps:P54 ?team; pq:P580 ?st1; pq:P582 ?et1. wd:Q169452 p:P54 ?ps2. ?ps2 ps:P54 ?team; pq:P580 ?st2; pq:P582 ?et2. FILTER(YEAR(?st1) <= 2000 && YEAR(?et1) >= 2000 && YEAR(?st2) <= 2000 && YEAR(?et2) >= 2000)}
```

User: How many positions did Kobe Bryant play in his team?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?pos) AS ?result) WHERE {wd:Q25369 wdt:P413 ?pos}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P580 (start time) - time an entity begins to exist or a statement starts being valid
wdt:P582 (end time) - moment when an entity ceases to exist and a statement stops being entirely valid or no longer be true
wdt:P54 (member of sports team) - sports teams or clubs that the subject represents or represented

--- ENTITIES (Items/Objects) ---
wd:Q121783 (Los Angeles Lakers) - American professional basketball team
wd:Q25369 (Kobe Bryant) - American basketball player (1978–2020)
wd:Q36159 (LeBron James) - American basketball player (born 1984)

### User Question:
Did Kobe Bryant leave the Lakers when LeBron James joined that team?

```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 wd:Q121783. wd:Q36159 wdt:P54 wd:Q121783. FILTER(wdt:P582(wd:Q25369) > wdt:P580(wd:Q36159))}
```

SYSTEM: Invalid Query. EndPointInternalError: The endpoint returned the HTTP status code 500. 
Fix it.
Corrected Query: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 wd:Q121783. wd:Q36159 wdt:P54 wd:Q121783. FILTER(wdt:P582(wd:Q25369) > wdt:P580(wd:Q36159))}
```

SYSTEM: Invalid Query. EndPointInternalError: The endpoint returned the HTTP status code 500. 
Fix it.
Corrected Query: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 wd:Q121783. wd:Q36159 wdt:P54 wd:Q121783. FILTER(wdt:P582(wd:Q25369) > wdt:P580(wd:Q36159))}
```

SYSTEM: Invalid Query. EndPointInternalError: The endpoint returned the HTTP status code 500. 
Fix it.
Corrected Query: ```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 wd:Q121783. wd:Q36159 wdt:P54 wd:Q121783. FILTER(wdt:P582(wd:Q25369) > wdt:P580(wd:Q36159))}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 4
---
### Q18: [PARTIAL] Did Haruki Murakami receive the Nobel Prize in Literature?

**Error:** `Wrong Answer: F1 Score: 0.00`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
SELECT (COUNT(DISTINCT ?winner) AS ?result) WHERE {wd:Q134798 wdt:P1346 wd:Q37922}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q37922 wdt:P1346 wd:Q134798}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 1 | `(0)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: How many Japanese writers received the Nobel Prize?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?writer) AS ?result) WHERE {?writer wdt:P166/wdt:P279 wd:Q7191. ?writer wdt:P27 wd:Q17; wdt:P106 wd:Q36180}
```

User: How many people have won the Nobel Prize in Literature since its inception?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?people) AS ?result) WHERE {?people wdt:P31 wd:Q5; wdt:P166 wd:Q37922}
```

User: How many people won the Nobel Prize in Literature or Physics since 2000?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?result) AS ?resultCnt) WHERE{?result wdt:P31 wd:Q5. ?result p:P166 ?ps. {?ps ps:P166 wd:Q37922} UNION {?ps ps:P166 wd:Q38104} ?ps pq:P585 ?time. FILTER(YEAR(?time) > 2000)}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P1346 (winner) - winner of a competition or similar event, not to be used for awards (instead use "award received" (P166) on awardee's item, possibly qualified with "for work" (P1686)) or for wars or battles

--- ENTITIES (Items/Objects) ---
wd:Q134798 (Haruki Murakami) - Japanese writer
wd:Q37922 (Nobel Prize in Literature) - one of five prizes established by Alfred Nobel

### User Question:
Did Haruki Murakami receive the Nobel Prize in Literature?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
SELECT (COUNT(DISTINCT ?winner) AS ?result) WHERE {wd:Q134798 wdt:P1346 wd:Q37922}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q17: [PARTIAL] Did the Chicago Bulls win at least two seasons of the NBA championship?

**Error:** `Wrong Answer: F1 Score: 0.00`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?season) AS ?result) WHERE {wd:Q128109 wdt:P3450 wd:Q155223; wdt:P1346 ?season.}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{{SELECT (COUNT (?season) AS ?count) WHERE {?season wdt:P3450 wd:Q155223. ?season wdt:P1346 wd:Q128109}} FILTER(?count >= 2)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 1 | `(0)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: Which NBA teams have won the most seasons?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {{SELECT DISTINCT (COUNT(DISTINCT ?season) AS ?max) WHERE {?season wdt:P31 wd:Q27020041; wdt:P3450 wd:Q155223; wdt:P1346 ?result. ?result wdt:P31 wd:Q13393265} GROUP BY ?result ORDER BY DESC (?max) LIMIT 1} ?season wdt:P31 wd:Q27020041; wdt:P3450 wd:Q155223; wdt:P1346 ?result. ?result wdt:P31 wd:Q13393265.} GROUP BY ?result HAVING ((COUNT(DISTINCT ?season)) = MAX(?max))
```

User: Did Michael Jordan and Kobe Bryant play for the same team?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 ?team. wd:Q41421 wdt:P54 ?team.}
```

User: How many All-NBA Team awards have Shaquille O'Neal and Kobe Bryant received in the same year?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?time) AS ?result) WHERE {wd:Q25369 p:P166 ?as. ?as ps:P166 wd:Q674359; pq:P585 ?time. wd:Q169452 p:P166 ?as2. ?as2 ps:P166 wd:Q674359; pq:P585 ?time}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P3450 (sports season of league or competition) - property that shows the competition of which the item is a season. Use P5138 for "season of club or team".
wdt:P1346 (winner) - winner of a competition or similar event, not to be used for awards (instead use "award received" (P166) on awardee's item, possibly qualified with "for work" (P1686)) or for wars or battles

--- ENTITIES (Items/Objects) ---
wd:Q128109 (Chicago Bulls) - American professional basketball team
wd:Q155223 (National Basketball Association) - North American professional basketball league

### User Question:
Did the Chicago Bulls win at least two seasons of the NBA championship?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?season) AS ?result) WHERE {wd:Q128109 wdt:P3450 wd:Q155223; wdt:P1346 ?season.}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q16: [PARTIAL] Did adam ondra win a medal in the 2020 summer olympics?

**Error:** `Wrong Answer: F1 Score: 0.00`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?medal) AS ?result) WHERE {wd:Q350568 p:P1344 ?ps. ?ps ps:P1344/wdt:P3450* wd:Q181278. ?ps ps:P1344/wdt:P166 ?medal.}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q350568 p:P1344 ?event. ?event ps:P1344 ?eventStatement. ?eventStatement wdt:P361* wd:Q181278. ?event pq:P1352 ?ranking. FILTER(?ranking <= 3)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 1 | `(0)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: has adam ondra been a winner of IFSC climbing world cup?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q350568 p:P1344 ?ps. ?ps ps:P1344/wdt:P3450* wd:Q1774251. {?ps pq:P1352 ?rank.} UNION {?ps pq:P166 ?gold.} FILTER(?rank = 1 || sameTerm(?gold,wd:Q406039))}
```

User: How many Olympic Games has Kobe Bryant taken part in?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?ol) AS ?result) WHERE {wd:Q25369 wdt:P1344 ?ol. ?ol wdt:P31/wdt:P279 wd:Q5389}
```

User: Did Udo Bölts participate in the Tour de France?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q66432 wdt:P1344/wdt:P31 wd:Q33881}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P1344 (participant in) - event in which a person, organization or creative work was/is a participant; inverse of P710 or P1923
wdt:P361 (part of) - object of which the subject is a part (if this subject is already part of object A which is a part of object B, then please only make the subject part of object A), inverse property of "has part" (P527, see also "has parts of the class" (P2670))
wdt:P1352 (ranking) - subject's ordinal position as qualitatively evaluated relative to other members of a group

--- ENTITIES (Items/Objects) ---
wd:Q350568 (Adam Ondra) - Czech rock climber
wd:Q181278 (2020 Summer Olympics) - games of the XXXII Olympiad, in Tokyo, Japan, held in 2021

### User Question:
Did adam ondra win a medal in the 2020 summer olympics?

```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q350568 p:P1344 ?ps. ?ps ps:P1344/wdt:P3450* wd:Q181278. {?ps pq:P1352 ?rank.} UNION {?ps pq:P166 ?gold.} FILTER(?rank = 1 || sameTerm(?gold,wd:Q406039))}
```

SYSTEM: Invalid Query. 'results'
Fix it.
Corrected Query: ```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?medal) AS ?result) WHERE {wd:Q350568 p:P1344 ?ps. ?ps ps:P1344/wdt:P3450* wd:Q181278. ?ps ps:P1344/wdt:P166 ?medal.}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 2
---
### Q15: [PARTIAL] How many different presidents of Russia have there been that took the position after 1990?

**Error:** `Wrong Answer: F1 Score: 0.00`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE {wd:Q218295 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. FILTER(?st > "1990-01-01T00:00:00Z"^^xsd:dateTime)}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE{?president p:P39 ?pos. ?pos ps:P39 wd:Q218295. ?pos pq:P580 ?start. FILTER((YEAR(?start)> 1990))}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(3)` |
| **Gen** | 1 | `(0)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: How many General Secretaries of the CPSU were there before Leonid Brezhnev?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT (COUNT(?gensec) as ?result) WHERE{wd:Q765165 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. ?gensec p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 < ?st)}
```

User: how many head of the state does iran have?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?hos) AS ?result) WHERE {wd:Q794 p:P35/ps:P35 ?hos.}
```

User: How many spouses do head of states have on average?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (AVG(?spouseCount) AS ?result) WHERE {{SELECT (COUNT(DISTINCT ?spouse) AS ?spouseCount) WHERE{?country wdt:P31 wd:Q6256. ?country p:P35/ps:P35 ?hos. OPTIONAL {?hos wdt:P26 ?spouse}} GROUP BY ?hos }}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P580 (start time) - time an entity begins to exist or a statement starts being valid
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q218295 (President of Russia) - head of state of the RSFSR (office established in 1991) and Russia

### User Question:
How many different presidents of Russia have there been that took the position after 1990?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE {wd:Q218295 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. FILTER(?st > "1990-01-01T00:00:00Z"^^xsd:dateTime)}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q14: [PARTIAL] How many General Secretaries of the CPSU were there before Leonid Brezhnev?

**Error:** `Wrong Answer: F1 Score: 0.00`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT (COUNT(DISTINCT ?genSec) AS ?result) WHERE {
  ?genSec wdt:P39 wd:Q1048744. 
  ?genSec wdt:P580 ?start. 
  ?genSec wdt:P580 ?end. 
  FILTER(?start < wd:Q765165)
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT (COUNT(?gensec) as ?result) WHERE{wd:Q765165 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. ?gensec p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 < ?st)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(2)` |
| **Gen** | 1 | `(0)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: How many different presidents of Russia have there been that took the position after 1990?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE{?president p:P39 ?pos. ?pos ps:P39 wd:Q218295. ?pos pq:P580 ?start. FILTER((YEAR(?start)> 1990))}
```

User: how many head of the state does iran have?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?hos) AS ?result) WHERE {wd:Q794 p:P35/ps:P35 ?hos.}
```

User: How many spouses do head of states have on average?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (AVG(?spouseCount) AS ?result) WHERE {{SELECT (COUNT(DISTINCT ?spouse) AS ?spouseCount) WHERE{?country wdt:P31 wd:Q6256. ?country p:P35/ps:P35 ?hos. OPTIONAL {?hos wdt:P26 ?spouse}} GROUP BY ?hos }}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P580 (start time) - time an entity begins to exist or a statement starts being valid
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q765165 (Leonid Brezhnev) - General Secretary of the Communist Party of the Soviet Union (1906–1982)
wd:Q1048744 (General Secretary of the Communist Party of the Soviet Union) - de facto head of state of the Soviet Union and dirigent of the Communist Party of the Soviet Union

### User Question:
How many General Secretaries of the CPSU were there before Leonid Brezhnev?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT (COUNT(DISTINCT ?genSec) AS ?result) WHERE {
  ?genSec wdt:P39 wd:Q1048744. 
  ?genSec wdt:P580 ?start. 
  ?genSec wdt:P580 ?end. 
  FILTER(?start < wd:Q765165)
}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q13: [PARTIAL] can i play don't starve on play station 4?

**Error:** `Wrong Answer: F1 Score: 0.00`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q3208174 wdt:P400 wd:Q5014725}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASk {wd:Q3208174 wdt:P400 wd:Q5014725.}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 1 | `()` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: What is the second game developed by Piranha Bytes?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{?result wdt:P178 wd:Q677273; wdt:P577 ?date} ORDER BY ASC(?date) OFFSET 1 LIMIT 1
```

User: How many other video games began the same year as Dead by Daylight?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?game) AS ?result) WHERE {?game wdt:P31/wdt:P279* wd:Q7889; wdt:P577 ?gameTime. wd:Q24514682 wdt:P577 ?dbdtime. FILTER((YEAR(?gameTime) = YEAR(?dbdtime)))}
```

User: How many people can play "Mensch ärgere dich nicht" at most?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q545129 wdt:P1873 ?result}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P400 (platform) - platform for which a work was developed or released, or the specific platform version of a software product

--- ENTITIES (Items/Objects) ---
wd:Q5014725 (PlayStation 4) - Sony's fourth home video game console, part of the eighth generation of consoles
wd:Q3208174 (Don't Starve) - 2013 video game developed by Klei Entertainment

### User Question:
can i play don't starve on play station 4?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q3208174 wdt:P400 wd:Q5014725}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q12: [PARTIAL] On which island is the Indonesian capital located?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q252 wdt:P36 ?result. wd:Q252 wdt:P706 wd:Q23442. }
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q252 wdt:P36 ?capital. ?capital wdt:P706 ?result. ?result wdt:P31 wd:Q23442}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q3757)` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: In which country is the Nanga Parbat located?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q130736 wdt:P17 ?result. }
```

User: Who is the founder of the capital of Vietnam?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q881 wdt:P36/wdt:P112 ?result}
```

User: What is the area of the capital of Spitsbergen?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q25231 wdt:P36/wdt:P2046 ?result}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P706 (located in/on physical feature) - located on the specified (geo)physical feature. Should not be used when the value is only political/administrative (P131) or a mountain range (P4552). Use P206 for things in/on bodies of water.
wdt:P36 (capital) - seat of government of a country, province, state or other type of administrative territorial entity
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain

--- ENTITIES (Items/Objects) ---
wd:Q23442 (island) - piece of sub-continental land completely surrounded by water
wd:Q252 (Indonesia) - island country in Southeast Asia and Oceania

### User Question:
On which island is the Indonesian capital located?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q252 wdt:P36 ?result. wd:Q252 wdt:P706 wd:Q23442. }
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q11: [PARTIAL] Which High School did Allen Ginsberg attend?

**Error:** `Wrong Answer: F1 Score: 0.50`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?school WHERE {wd:Q6711 wdt:P69 ?school}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q6711 wdt:P69 ?result. ?result wdt:P31 wd:Q9826}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q14705485)` |
| **Gen** | 3 | `(Q5018694), (Q14705485), (Q49088)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: When did Allen Ginsberg die?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q6711 wdt:P570 ?result}
```

User: Who was the partner of Allen Ginsberg?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q6711 wdt:P451 ?result}
```

User: How many poems did Allen Ginsberg published?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?poem) AS ?result) WHERE {?poem wdt:P31 wd:Q7725634; wdt:P50 wd:Q6711; wdt:P136/wdt:P279* wd:Q482}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
wdt:P69 (educated at) - educational institution attended by subject

--- ENTITIES (Items/Objects) ---
wd:Q6711 (Allen Ginsberg) - American poet and writer (1926–1997)
wd:Q9826 (high school) - institution which provides final part of secondary education

### User Question:
Which High School did Allen Ginsberg attend?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?school WHERE {wd:Q6711 wdt:P69 ?school}
```
</details>

**F1 Score:** 0.50 | **Attempts:** 1
---
### Q10: [PASS] At which school was Yayoi Kusama educated at?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q231121 wdt:P69 ?result }
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q231121 wdt:P69 ?result}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q749884)` |
| **Gen** | 1 | `(Q749884)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: When was Rumi born?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q43347 wdt:P569 ?result}
```

User: How many movies were directed by Akira Kurosawa ?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?film) AS ?result) WHERE {?film wdt:P31 wd:Q11424; wdt:P57 wd:Q8006}
```

User: Which High School did Allen Ginsberg attend?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q6711 wdt:P69 ?result. ?result wdt:P31 wd:Q9826}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P69 (educated at) - educational institution attended by subject

--- ENTITIES (Items/Objects) ---
wd:Q231121 (Yayoi Kusama) - Japanese painter, performance, and installation artist (born 1929)

### User Question:
At which school was Yayoi Kusama educated at?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q231121 wdt:P69 ?result }
```
</details>

**F1 Score:** 1.00 | **Attempts:** 1
---
### Q9: [PARTIAL] What is the boiling point of water?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?boilingPoint ?pressure WHERE {wd:Q283 wdt:P2102 ?boilingPoint ; pq:P2102 ?pressure }
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q283 wdt:P2102 ?result}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(99.9839)` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: How many different colors can water take?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?color) AS ?result) WHERE {wd:Q283 wdt:P462 ?color}
```

User: Is water colorless?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q283 wdt:P462 wd:Q11567495}
```

User: What is the highest point of Norway?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q20 wdt:P610 ?result}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P2102 (boiling point) - temperature at which a substance changes its phase from liquid to gas (indicate the corresponding pressure as qualifier)

--- ENTITIES (Items/Objects) ---
wd:Q283 (water) - chemical compound whose molecules are formed by two hydrogen atoms and one oxygen atom

### User Question:
What is the boiling point of water?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?boilingPoint ?pressure WHERE {wd:Q283 wdt:P2102 ?boilingPoint ; pq:P2102 ?pressure }
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q8: [PARTIAL] are brooke raboutou and colin duffy from same state of the usa?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?state WHERE {wd:Q2926117 wdt:P19 ?birthPlace. wd:Q87192979 wdt:P19 ?birthPlace2. ?birthPlace wdt:P31 wd:Q35657. ?birthPlace2 wdt:P31 wd:Q35657. FILTER(?birthPlace = ?birthPlace2)}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q2926117 wdt:P19 ?b1. wd:Q87192979 wdt:P19 ?b2. ?b1 wdt:P131* ?state. ?b2 wdt:P131* ?state. ?state wdt:P31 wd:Q35657 .}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: Were Angela Merkel and Tony Blair born in the same year?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q567 wdt:P569 ?da. wd:Q9545 wdt:P569 ?dt. FILTER(YEAR(?dt) = YEAR(?da))}
```

User: Is Axel Rose a member of Guns N' Roses?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q11885 wdt:P463 wd:Q11895}
```

User: which state inside USA is batman living in?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q2695156 wdt:P551/wdt:P131 ?result. ?result wdt:P31 wd:Q35657}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P131 (located in the administrative territorial entity) - the item is located on the territory of the following administrative entity. Use P276 for specifying locations that are non-administrative places and for items about events. Use P1382 if the item falls only partially into the administrative entity.
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
wdt:P19 (place of birth) - most specific known birth location of a person, animal or fictional character

--- ENTITIES (Items/Objects) ---
wd:Q2926117 (Brooke Raboutou) - American sport climber
wd:Q35657 (U.S. state) - constituent political entity of the United States of America
wd:Q87192979 (Colin Duffy) - Sport climber from the United States

### User Question:
are brooke raboutou and colin duffy from same state of the usa?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?state WHERE {wd:Q2926117 wdt:P19 ?birthPlace. wd:Q87192979 wdt:P19 ?birthPlace2. ?birthPlace wdt:P31 wd:Q35657. ?birthPlace2 wdt:P31 wd:Q35657. FILTER(?birthPlace = ?birthPlace2)}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q7: [PARTIAL] Apart from the book series the witcher, name all of the author’s notable work.

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?notableWork WHERE {wd:Q11835640 wdt:P800 ?notableWork}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P50 ?author. ?author wdt:P800 ?result. FILTER(?result != wd:Q11835640)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 5 | `(Q2045474), (Q2414756), (Q4080260), (Q4113386), (Q4240572)` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: How many literary works besides The Picture of Dorian Gray did its author write?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?novel) AS ?result) WHERE {wd:Q82464 wdt:P50 ?aut. ?novel wdt:P31 wd:Q7725634; wdt:P50 ?aut FILTER(?novel != wd:Q82464)}
```

User: How many literary works did Richard Bachman write?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?book) AS ?result) WHERE {?book wdt:P50 wd:Q39829; wdt:P31 wd:Q7725634}
```

User: How many notable works does Sarah J. Maas have?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?notableW) AS ?result) WHERE {wd:Q20640708 wdt:P800 ?notableW}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P800 (notable work) - notable scientific, artistic or literary work, or other work of significance among subject's works
wdt:P50 (author) - main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist

--- ENTITIES (Items/Objects) ---
wd:Q11835640 (The Witcher) - series of fantasy novels and short stories by Polish writer Andrzej Sapkowski

### User Question:
Apart from the book series the witcher, name all of the author’s notable work.

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?notableWork WHERE {wd:Q11835640 wdt:P800 ?notableWork}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q6: [PASS] On which stock exchanges are Siemens AG shares traded?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?exchange WHERE {wd:Q81230 wdt:P414 ?exchange.}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q81230 wdt:P414 ?result}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q151139)` |
| **Gen** | 1 | `(Q151139)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: How many international airports are located within the city of Hamburg ?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?ap) AS ?result) WHERE {?ap wdt:P31 wd:Q644371. ?ap wdt:P131* wd:Q1055}
```

User: In how many countries has IKEA been established?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?c) AS ?result) WHERE {wd:Q1769361 wdt:P527 ?c. ?c p:P31/ps:P31 wd:Q6256}
```

User: How many mountains are located in Germany?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?m) AS ?result) WHERE {?m wdt:P31 wd:Q8502; wdt:P17 wd:Q183}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P414 (stock exchange) - exchange on which this company is traded

--- ENTITIES (Items/Objects) ---
wd:Q81230 (Siemens) - German multinational conglomerate company

### User Question:
On which stock exchanges are Siemens AG shares traded?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?exchange WHERE {wd:Q81230 wdt:P414 ?exchange.}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 1
---
### Q5: [PARTIAL] among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?work WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P921 wd:Q16003532. ?author wdt:P800 ?work. FILTER(?work != wd:Q696071)}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P800 ?result. ?result wdt:P921 wd:Q16003532 FILTER(?result != wd:Q69071)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q18225473)` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: when was the magazine in which hunter x hunter is published established?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q696071 wdt:P1433 ?mag. ?mag wdt:P31/wdt:P279* wd:Q41298; wdt:P571 ?result}
```

User: is there female main character in hunter x hunter?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q696071 wdt:P674 ?char. ?char wdt:P21 wd:Q6581072}
```

User: what is the main subject of the manga "your lie in april": primary school, middle school or high school student?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11419997 wdt:P921 ?result. FILTER(?result IN (wd:Q16003605, wd:Q16003532, wd:Q15360275))}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P800 (notable work) - notable scientific, artistic or literary work, or other work of significance among subject's works
wdt:P921 (main subject) - primary topic of a work or act of communication
wdt:P50 (author) - main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist

--- ENTITIES (Items/Objects) ---
wd:Q69071 (Münchenbuchsee) - municipality in the canton of Bern in Switzerland
wd:Q696071 (Hunter × Hunter) - Japanese manga series
wd:Q16003532 (middle school student) - student in late primary or early secondary education

### User Question:
among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?work WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P921 wd:Q16003532. ?author wdt:P800 ?work. FILTER(?work != wd:Q696071)}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q4: [PARTIAL] among the founders of tencent company, who has been member of national people’s congress?

**Error:** `Wrong Answer: F1 Score: 0.00`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?founder. ?founder wdt:P39 ?result}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?result. ?result wdt:P39 wd:Q10891456.}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q1739008)` |
| **Gen** | 2 | `(Q484876), (Q10891456)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: Were at least two of the founders of tencent educated at the same university?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q860580 wdt:P112 ?founder. ?founder wdt:P69 ?uni. wd:Q860580 wdt:P112 ?founder2. ?founder2 wdt:P69 ?uni. FILTER(?founder != ?founder2)}
```

User: Who founded the Roland Corporation?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q848490 wdt:P112 ?result}
```

User: Which businesses are founded by the person in charge of Tesla?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q478214 wdt:P169 ?found. ?result wdt:P112 ?found; wdt:P31/wdt:P279* wd:Q4830453}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P112 (founded by) - founder or co-founder of this organization, religion, place or entity
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q10891456 (National People's Congress deputy) - member of Chinese National People's Congress
wd:Q860580 (Tencent) - Chinese multinational investment holding conglomerate

### User Question:
among the founders of tencent company, who has been member of national people’s congress?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?founder. ?founder wdt:P39 ?result}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q3: [FAIL] among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

**Error:** `Syntax Error: Line 1, Col 789: Expected Expected end of text`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result; wdt:P451 ?sp1; wdt:P451 ?sp2} FILTER (?sp1 != ?sp2)
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result. ?result wdt:P451 ?p1, ?p2. FILTER(?p1 != ?p2 &&(?result IN (wd:Q4205826, wd:Q4463198)))}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q4205826)` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: How many spouses had Rama V (one of the former Kings of Siam)?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?sp) AS ?result) WHERE {wd:Q158861 wdt:P26 ?sp}
```

User: Where was Goethe’s unmarried partner born ?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q5879 wdt:P451/wdt:P19 ?result}
```

User: which swordfighter in the lord of the rings marry a half-elven and belong to rangers of the north?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P106 wd:Q11397897; wdt:P26/wdt:P31 wd:Q2035494; wdt:P172 wd:Q2292830}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P451 (unmarried partner) - someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples
wdt:P674 (characters) - characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)

--- ENTITIES (Items/Objects) ---
wd:Q4205826 (Yennefer of Vengerberg) - fictional sorceress from the Witcher series
wd:Q11835640 (The Witcher) - series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
wd:Q4463198 (Triss Merigold) - fictional sorceress from the Witcher series

### User Question:
among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result; wdt:P451 ?sp1; wdt:P451 ?sp2} FILTER (?sp1 != ?sp2)
```

SYSTEM: Invalid Query. Line 1, Col 789: Expected Expected end of text
Fix it.
Corrected Query: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result; wdt:P451 ?sp1; wdt:P451 ?sp2} FILTER (?sp1 != ?sp2)
```

SYSTEM: Invalid Query. Line 1, Col 789: Expected Expected end of text
Fix it.
Corrected Query: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result; wdt:P451 ?sp1; wdt:P451 ?sp2} FILTER (?sp1 != ?sp2)
```

SYSTEM: Invalid Query. Line 1, Col 789: Expected Expected end of text
Fix it.
Corrected Query: ```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result; wdt:P451 ?sp1; wdt:P451 ?sp2} FILTER (?sp1 != ?sp2)
```
</details>

**F1 Score:** 0.00 | **Attempts:** 4
---
### Q2: [PARTIAL] Which animal participated in a military operation with the Australian Defence Force?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?animal WHERE {wd:Q625657 wdt:P710 ?animal. ?animal p:P31/ps:P31 wd:Q16521. ?animal p:P3831 wd:Q645883}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q93208)` |
| **Gen** | 0 | `` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: With how many countries does Australia share a border?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?country) AS ?result) WHERE {wd:Q408 wdt:P47 ?country. ?country p:P31/ps:P31 wd:Q6256}
```

User: From which country are the beagles originally from?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q21102 wdt:P495 ?result}
```

User: How many casualties were a result of the Troubles?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q815436 wdt:P1120 ?result}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
wdt:P710 (participant) - person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.

--- ENTITIES (Items/Objects) ---
wd:Q625657 (Australian Defence Force) - combined military forces of Australia
wd:Q16521 (taxon) - group of one or more organism(s), which a taxonomist adjudges to be a unit
wd:Q645883 (military operation) - coordinated military actions of a state or a non-state actor

### User Question:
Which animal participated in a military operation with the Australian Defence Force?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?animal WHERE {wd:Q625657 wdt:P710 ?animal. ?animal p:P31/ps:P31 wd:Q16521. ?animal p:P3831 wd:Q645883}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 1
---
### Q1: [PASS] After whom is the Riemannian geometry named?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q761383 wdt:P138 ?result}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q761383 wdt:P138 ?result. }
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q42299)` |
| **Gen** | 1 | `(Q42299)` |

<details>
<summary><b> View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    
### Few-Shot Examples:
User: What was Ada Lovelace’s noble title?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q7259 wdt:P97 ?result}
```

User: Who founded the architectural firm who planned the Elbphilharmonie?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q673223 wdt:P84/wdt:P112 ?result}
```

User: Who were the parents of Socrates ?
Query:
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {{wd:Q913 wdt:P25 ?result} UNION {wd:Q913 wdt:P22 ?result}}
```

### Context (Schema):
--- PROPERTIES (Relations) ---
wdt:P138 (named after) - entity or event that inspired the subject's name, or namesake (in at least one language). Qualifier "applies to name" (P5168) can be used to indicate which one

--- ENTITIES (Items/Objects) ---
wd:Q761383 (Riemannian geometry) - branch of differential geometry dealing with (generalized) Riemannian manifolds

### User Question:
After whom is the Riemannian geometry named?

```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q761383 wdt:P138 ?result}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 1
---

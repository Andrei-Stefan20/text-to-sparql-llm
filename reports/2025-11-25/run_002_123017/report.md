# Text-to-SPARQL Report

**Model:** `ACE-deepseek-coder-6.7b-instruct.Q4_K_M.gguf`
**Date:** 2025-11-25

| Metric | Value |
|---|---|
| Syntax Accuracy | 50.00% |
| Answer Accuracy | 33.33% |
| Avg F1 Score | 0.3333 |
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
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.

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

> **Error:** `Error: Syntax Error: Line 15, Col 31: Expected Expected SelectQuery`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX bd: <http://www.bigdata.com/rdf#>  SELECT DISTINCT ?animal ?animalLabel WHERE {   ?animal wdt:P31 wd:Q16521.   ?animal wdt:P710 ?operation.   ?operation wdt:P31 wd:Q64588` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q93208`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.

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
- participant (P710): person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.
- Australian Defence Force (Q625657): combined military forces of Australia
- taxon (Q16521): group of one or more organism(s), which a taxonomist adjudges to be a unit
- military operation (Q645883): coordinated military actions of a state or a non-state actor

### USER QUESTION:
Which animal participated in a military operation with the Australian Defence Force?

### SOLUTION:
```sparql
````
</details>

---
### Q3: SYNTAX ERR
**Input:** among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

> **Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result. ?result wdt:P451 ?p1, ?p2. FILTER(?p1 != ?p2 &&(?result IN (wd:Q4205826, wd:Q4463198)))}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?character ?characterLabel WHERE {   ?character wdt:P674 wd:Q11835640; # The Witcher             wdt:P451 ?partner1, ?partner2. # Unmarried partners   ?partner1 wdt:P31 wd:Q515; # Human            wdt:P26 wd:Q4205826. # Unmarried partner of Yennefer of Vengerberg   ?partner2 wdt:P31 wd:Q515; # Human            wdt:P26 wd:Q4463198. # Unmarried partner of Triss Merigold   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q4205826`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.

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
Q: How many spouses had Rama V (one of the former Kings of Siam)?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?sp) AS ?result) WHERE {wd:Q158861 wdt:P26 ?sp}
```

Q: Where was Goethe’s unmarried partner born ?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q5879 wdt:P451/wdt:P19 ?result}
```

Q: which swordfighter in the lord of the rings marry a half-elven and belong to rangers of the north?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P106 wd:Q11397897; wdt:P26/wdt:P31 wd:Q2035494; wdt:P172 wd:Q2292830}
```

### SCHEMA CONTEXT:
- characters (P674): characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)
- unmarried partner (P451): someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples
- The Witcher (Q11835640): series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
- Triss Merigold (Q4463198): fictional sorceress from the Witcher series
- Yennefer of Vengerberg (Q4205826): fictional sorceress from the Witcher series

### USER QUESTION:
among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

### SOLUTION:
```sparql
````
</details>

---
### Q4: WRONG ANS
**Input:** among the founders of tencent company, who has been member of national people’s congress?

> **Error:** `Success: None`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?result. ?result wdt:P39 wd:Q10891456.}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?founder ?founderLabel WHERE {   wd:Q860580 wdt:P112 ?founder.   ?founder wdt:P39 wd:Q10891456.   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q1739008`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q1739008, Ma Huateng`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.

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
Q: Were at least two of the founders of tencent educated at the same university?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q860580 wdt:P112 ?founder. ?founder wdt:P69 ?uni. wd:Q860580 wdt:P112 ?founder2. ?founder2 wdt:P69 ?uni. FILTER(?founder != ?founder2)}
```

Q: Who founded the Roland Corporation?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q848490 wdt:P112 ?result}
```

Q: Which businesses are founded by the person in charge of Tesla?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q478214 wdt:P169 ?found. ?result wdt:P112 ?found; wdt:P31/wdt:P279* wd:Q4830453}
```

### SCHEMA CONTEXT:
- National People's Congress deputy (Q10891456): member of Chinese National People's Congress
- founded by (P112): founder or co-founder of this organization, religion, place or entity
- Tencent (Q860580): Chinese multinational investment holding conglomerate
- position held (P39): subject currently or formerly holds the object position or public office

### USER QUESTION:
among the founders of tencent company, who has been member of national people’s congress?

### SOLUTION:
```sparql
````
</details>

---
### Q5: SYNTAX ERR
**Input:** among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

> **Error:** `Error: Syntax Error: Line 3, Col 1: Expected Expected SelectQuery`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P800 ?result. ?result wdt:P921 wd:Q16003532 FILTER(?result != wd:Q69071)}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdt:P921: <http://www.wikidata.org/prop/direct/P921> PREFIX wdt:P50: <http://www.wikidata.org/prop/direct/P50> PREFIX wdt:P1433: <http://www.wikidata.org/prop/direct/P1433>  SELECT ?representative_work WHERE {   wd:Q696071 wdt:P1433 ?magazine.   ?magazine wdt:P50 wd:Q481498.   ?magazine wdt:P921 ?representative_work.   ?representative_work wdt:P921 wd:Q16003532. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q18225473`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.

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
Q: when was the magazine in which hunter x hunter is published established?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q696071 wdt:P1433 ?mag. ?mag wdt:P31/wdt:P279* wd:Q41298; wdt:P571 ?result}
```

Q: is there female main character in hunter x hunter?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q696071 wdt:P674 ?char. ?char wdt:P21 wd:Q6581072}
```

Q: what is the main subject of the manga "your lie in april": primary school, middle school or high school student?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11419997 wdt:P921 ?result. FILTER(?result IN (wd:Q16003605, wd:Q16003532, wd:Q15360275))}
```

### SCHEMA CONTEXT:
- main subject (P921): primary topic of a work or act of communication
- notable work (P800): notable scientific, artistic or literary work, or other work of significance among subject's works
- Hunter × Hunter (Q696071): Japanese manga series
- author (P50): main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
- middle school student (Q16003532): student in late primary or early secondary education
- Münchenbuchsee (Q69071): municipality in the canton of Bern in Switzerland

### USER QUESTION:
among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

### SOLUTION:
```sparql
````
</details>

---
### Q6: CORRECT
**Input:** On which stock exchanges are Siemens AG shares traded?

> **Error:** `Success: None`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q81230 wdt:P414 ?result}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?exchange WHERE {   wd:Q81230 wdt:P414 ?exchange. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q151139`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q151139`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- For characters with two unmarried partners, use wdt:P451 twice in the query, once for each partner.

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
Q: How many international airports are located within the city of Hamburg ?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?ap) AS ?result) WHERE {?ap wdt:P31 wd:Q644371. ?ap wdt:P131* wd:Q1055}
```

Q: In how many countries has IKEA been established?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?c) AS ?result) WHERE {wd:Q1769361 wdt:P527 ?c. ?c p:P31/ps:P31 wd:Q6256}
```

Q: How many mountains are located in Germany?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?m) AS ?result) WHERE {?m wdt:P31 wd:Q8502; wdt:P17 wd:Q183}
```

### SCHEMA CONTEXT:
- Siemens (Q81230): German multinational conglomerate company
- stock exchange (P414): exchange on which this company is traded

### USER QUESTION:
On which stock exchanges are Siemens AG shares traded?

### SOLUTION:
```sparql
````
</details>

---

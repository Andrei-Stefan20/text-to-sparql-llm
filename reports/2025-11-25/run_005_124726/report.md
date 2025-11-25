# Text-to-SPARQL Report

**Model:** `ACE-deepseek-coder-6.7b-instruct.Q4_K_M.gguf`
**Date:** 2025-11-25

| Metric | Value |
|---|---|
| Syntax Accuracy | 33.33% |
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

> **Error:** `Error: Syntax Error: Line 3, Col 1: Expected Expected SelectQuery`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdt:P1344: <http://www.wikidata.org/prop/direct/P1344> PREFIX wdt:P134: <http://www.wikidata.org/prop/direct/P134> PREFIX wdt:P131: <http://www.wikidata.org/prop/direct/P131>  SELECT ?animal ?animalLabel WHERE {   ?animal wdt:P131* wd:Q16521.   ?animal wdt:P1344 ?militaryOperation.   ?militaryOperation wdt:P134 ?defenceForce.   ?defenceForce wdt:P17 wd:Q408.   SERVICE wikibase:label { bd:serviceParam wikibase:language "[` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q93208`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 3
<details><summary>Debug Info</summary>

**Context:**
```text
- Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.


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
- taxon (Q16521): group of one or more organism(s), which a taxonomist adjudges to be a unit
- Australian Defence Force (Q625657): combined military forces of Australia

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
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result. ?result wdt:P451 ?p1, ?p2. FILTER(?p1 != ?p2 &&(?result IN (wd:Q4205826, wd:Q4463198)))}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?character ?characterLabel ?partner1 ?partner1Label ?partner2 ?partner2Label WHERE {   ?character wdt:P674 wd:Q11835640; # characters in the Witcher series             wdt:P26 ?partner1; # first partner             wdt:P26 ?partner2. # second partner   ?partner1 wdt:P451 ?partner2. # second partner is the unmarried partner of the first partner   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q4205826`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 3
<details><summary>Debug Info</summary>

**Context:**
```text
- Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.

### ACE PLAYBOOK (STRATEGIC GUIDELINES):
The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
- Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.


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
- The Witcher (Q11835640): series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
- unmarried partner (P451): someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples
- characters (P674): characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)
- Triss Merigold (Q4463198): fictional sorceress from the Witcher series
- Yennefer of Vengerberg (Q4205826): fictional sorceress from the Witcher series

### USER QUESTION:
among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

### SOLUTION:
```sparql
````
</details>

---

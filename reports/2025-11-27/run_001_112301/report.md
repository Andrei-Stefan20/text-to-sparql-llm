# Text-to-SPARQL Report

**Model:** `deepseek-coder-6.7b-instruct.Q4_K_M.gguf`
**Date:** 2025-11-27

| Metric | Value |
|---|---|
| Syntax Accuracy | 76.47% |
| Answer Accuracy | 29.41% |
| Avg F1 Score | 0.3235 |
| Self-Corrections | 1 |

---

### Q1: CORRECT
**Input:** After whom is the Riemannian geometry named?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q761383 wdt:P138 ?result. }` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT ?namedAfter WHERE {   wd:Q761383 wdt:P138 ?namedAfter. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q42299`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q42299`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P138 (named after) - entity or event that inspired the subject's name, or namesake (in at least one language). Qualifier "applies to name" (P5168) can be used to indicate which one

--- ENTITIES (Items/Objects) ---
wd:Q761383 (Riemannian geometry) - branch of differential geometry dealing with (generalized) Riemannian manifolds
```

**History (Prompt):**
````text
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
````
</details>

---
### Q2: CORRECT
**Input:** Which animal participated in a military operation with the Australian Defence Force?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX bd: <http://www.bigdata.com/rdf#>  SELECT DISTINCT ?animal WHERE {   ?operation wdt:P31 wd:Q645883.   ?operation wdt:P710 ?animal.   ?animal wdt:P31 wd:Q16521. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q93208`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q93208`

**F1:** 1.00 | **Attempts:** 3
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P710 (participant) - person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain

--- ENTITIES (Items/Objects) ---
wd:Q645883 (military operation) - coordinated military actions of a state or a non-state actor
wd:Q16521 (taxon) - group of one or more organism(s), which a taxonomist adjudges to be a unit
wd:Q625657 (Australian Defence Force) - combined military forces of Australia
```

**History (Prompt):**
````text
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
wdt:P710 (participant) - person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain

--- ENTITIES (Items/Objects) ---
wd:Q645883 (military operation) - coordinated military actions of a state or a non-state actor
wd:Q16521 (taxon) - group of one or more organism(s), which a taxonomist adjudges to be a unit
wd:Q625657 (Australian Defence Force) - combined military forces of Australia

### User Question:
Which animal participated in a military operation with the Australian Defence Force?

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT DISTINCT ?animal WHERE {
  ?operation wdt:P31 wd:Q645883.
  ?operation wdt:P710 ?animal.
  ?animal wdt:P31 wd:Q16521.
  ?an
```

SYSTEM: Invalid Query. Line 14, Col 3: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
````
</details>

---
### Q3: SYNTAX ERR
**Input:** among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

> **Error:** `Syntax Error: Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result. ?result wdt:P451 ?p1, ?p2. FILTER(?p1 != ?p2 &&(?result IN (wd:Q4205826, wd:Q4463198)))}` | `PREFIX wdt:` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q4205826`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 6
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P674 (characters) - characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)
wdt:P451 (unmarried partner) - someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples

--- ENTITIES (Items/Objects) ---
wd:Q4205826 (Yennefer of Vengerberg) - fictional sorceress from the Witcher series
wd:Q11835640 (The Witcher) - series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
wd:Q4463198 (Triss Merigold) - fictional sorceress from the Witcher series
```

**History (Prompt):**
````text
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
wdt:P674 (characters) - characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)
wdt:P451 (unmarried partner) - someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples

--- ENTITIES (Items/Objects) ---
wd:Q4205826 (Yennefer of Vengerberg) - fictional sorceress from the Witcher series
wd:Q11835640 (The Witcher) - series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
wd:Q4463198 (Triss Merigold) - fictional sorceress from the Witcher series

### User Question:
among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>

SELECT ?item ?itemLabel WHERE {
  ?item wdt:P674 wd:Q11835640;  # The Witcher
        wdt:P451 ?partner1;  # Unmarried partner 1
        wdt:P451 ?partner2.  # Unmarried partner 2
  VALUES ?partner1 ?partner2 { wd:Q4205826 wd:Q4463198 }  # Yennefer of Vengerberg and Triss Merigold
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

SYSTEM: Invalid Query. Line 8, Col 3: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wdt:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>

SELECT ?item ?itemLabel WHERE {
  ?item wdt:P674 wd:Q11835640;
        wdt:P451 ?partner1;
        wdt:P451 ?partner2.
  VALUES ?partner1 ?partner2 { wd:Q4205826 wd:Q4463198 }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

SYSTEM: Invalid Query. Line 8, Col 3: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wdt:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
PREFIX wdt:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
````
</details>

---
### Q4: WRONG ANS
**Input:** among the founders of tencent company, who has been member of national people’s congress?

> **Error:** `Wrong Answer: F1 Score: 0.00`

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
--- PROPERTIES (Relations) ---
wdt:P112 (founded by) - founder or co-founder of this organization, religion, place or entity
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q10891456 (National People's Congress deputy) - member of Chinese National People's Congress
wd:Q860580 (Tencent) - Chinese multinational investment holding conglomerate
```

**History (Prompt):**
````text
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
````
</details>

---
### Q5: WRONG ANS
**Input:** among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P800 ?result. ?result wdt:P921 wd:Q16003532 FILTER(?result != wd:Q69071)}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?work WHERE {   ?work wdt:P50 wd:Q696071;  # author of the work is Hunter x Hunter         wdt:P921 wd:Q16003532.  # main subject of the work is middle school student }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q18225473`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P50 (author) - main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
wdt:P800 (notable work) - notable scientific, artistic or literary work, or other work of significance among subject's works
wdt:P921 (main subject) - primary topic of a work or act of communication

--- ENTITIES (Items/Objects) ---
wd:Q16003532 (middle school student) - student in late primary or early secondary education
wd:Q696071 (Hunter × Hunter) - Japanese manga series
wd:Q69071 (Münchenbuchsee) - municipality in the canton of Bern in Switzerland
```

**History (Prompt):**
````text
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
wdt:P50 (author) - main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
wdt:P800 (notable work) - notable scientific, artistic or literary work, or other work of significance among subject's works
wdt:P921 (main subject) - primary topic of a work or act of communication

--- ENTITIES (Items/Objects) ---
wd:Q16003532 (middle school student) - student in late primary or early secondary education
wd:Q696071 (Hunter × Hunter) - Japanese manga series
wd:Q69071 (Münchenbuchsee) - municipality in the canton of Bern in Switzerland

### User Question:
among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

```sparql
````
</details>

---
### Q6: CORRECT
**Input:** On which stock exchanges are Siemens AG shares traded?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q81230 wdt:P414 ?result}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/>  SELECT ?exchange WHERE {   wd:Q81230 wdt:P414 ?exchange. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q151139`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q151139`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P414 (stock exchange) - exchange on which this company is traded

--- ENTITIES (Items/Objects) ---
wd:Q81230 (Siemens) - German multinational conglomerate company
```

**History (Prompt):**
````text
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
````
</details>

---
### Q7: WRONG ANS
**Input:** Apart from the book series the witcher, name all of the author’s notable work.

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P50 ?author. ?author wdt:P800 ?result. FILTER(?result != wd:Q11835640)}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT ?notableWork ?notableWorkLabel WHERE {   wd:Q11835640 wdt:P800 ?notableWork.   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } }` |

#### Execution Results
- **Gold:** `[5 items] http://www.wikidata.org/entity/Q2045474; http://www.wikidata.org/entity/Q2414756; http://www.wikidata.org/entity/Q4080260 ... (2 more)`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P50 (author) - main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
wdt:P800 (notable work) - notable scientific, artistic or literary work, or other work of significance among subject's works

--- ENTITIES (Items/Objects) ---
wd:Q11835640 (The Witcher) - series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
```

**History (Prompt):**
````text
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
wdt:P50 (author) - main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
wdt:P800 (notable work) - notable scientific, artistic or literary work, or other work of significance among subject's works

--- ENTITIES (Items/Objects) ---
wd:Q11835640 (The Witcher) - series of fantasy novels and short stories by Polish writer Andrzej Sapkowski

### User Question:
Apart from the book series the witcher, name all of the author’s notable work.

```sparql
````
</details>

---
### Q8: WRONG ANS
**Input:** are brooke raboutou and colin duffy from same state of the usa?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q2926117 wdt:P19 ?b1. wd:Q87192979 wdt:P19 ?b2. ?b1 wdt:P131* ?state. ?b2 wdt:P131* ?state. ?state wdt:P31 wd:Q35657 .}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?state WHERE {   wd:Q35657 wdt:P131 ?state.   {wd:Q87192979 wdt:P19 ?state.}   UNION   {wd:Q2926117 wdt:P19 ?state.} }` |

#### Execution Results
- **Gold:** `No results`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P131 (located in the administrative territorial entity) - the item is located on the territory of the following administrative entity. Use P276 for specifying locations that are non-administrative places and for items about events. Use P1382 if the item falls only partially into the administrative entity.
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
wdt:P19 (place of birth) - most specific known birth location of a person, animal or fictional character

--- ENTITIES (Items/Objects) ---
wd:Q87192979 (Colin Duffy) - Sport climber from the United States
wd:Q35657 (U.S. state) - constituent political entity of the United States of America
wd:Q2926117 (Brooke Raboutou) - American sport climber
```

**History (Prompt):**
````text
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
wd:Q87192979 (Colin Duffy) - Sport climber from the United States
wd:Q35657 (U.S. state) - constituent political entity of the United States of America
wd:Q2926117 (Brooke Raboutou) - American sport climber

### User Question:
are brooke raboutou and colin duffy from same state of the usa?

```sparql
````
</details>

---
### Q9: CORRECT
**Input:** What is the boiling point of water?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q283 wdt:P2102 ?result}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?boilingPoint WHERE {   wd:Q283 wdt:P2102 ?boilingPoint. }` |

#### Execution Results
- **Gold:** `[1 items] 99.9839`
- **Gen:** `[1 items] 99.9839`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P2102 (boiling point) - temperature at which a substance changes its phase from liquid to gas (indicate the corresponding pressure as qualifier)

--- ENTITIES (Items/Objects) ---
wd:Q283 (water) - chemical compound whose molecules are formed by two hydrogen atoms and one oxygen atom
```

**History (Prompt):**
````text
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
````
</details>

---
### Q10: CORRECT
**Input:** At which school was Yayoi Kusama educated at?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q231121 wdt:P69 ?result}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?result WHERE {   wd:Q231121 wdt:P69 ?result. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q749884`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q749884`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P69 (educated at) - educational institution attended by subject

--- ENTITIES (Items/Objects) ---
wd:Q231121 (Yayoi Kusama) - Japanese painter, performance, and installation artist (born 1929)
```

**History (Prompt):**
````text
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
````
</details>

---
### Q11: WRONG ANS
**Input:** Which High School did Allen Ginsberg attend?

> **Error:** `Wrong Answer: F1 Score: 0.50`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q6711 wdt:P69 ?result. ?result wdt:P31 wd:Q9826}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?result WHERE {   wd:Q6711 wdt:P69 ?result. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q14705485`
- **Gen:** `[3 items] http://www.wikidata.org/entity/Q49088; http://www.wikidata.org/entity/Q5018694; http://www.wikidata.org/entity/Q14705485`

**F1:** 0.50 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
wdt:P69 (educated at) - educational institution attended by subject

--- ENTITIES (Items/Objects) ---
wd:Q6711 (Allen Ginsberg) - American poet and writer (1926–1997)
wd:Q9826 (high school) - institution which provides final part of secondary education
```

**History (Prompt):**
````text
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
````
</details>

---
### Q12: WRONG ANS
**Input:** On which island is the Indonesian capital located?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q252 wdt:P36 ?capital. ?capital wdt:P706 ?result. ?result wdt:P31 wd:Q23442}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?island WHERE {   wd:Q624 wdt:P36 wd:Q13442.   ?island wdt:P706 wd:Q13442. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q3757`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
wdt:P706 (located in/on physical feature) - located on the specified (geo)physical feature. Should not be used when the value is only political/administrative (P131) or a mountain range (P4552). Use P206 for things in/on bodies of water.
wdt:P36 (capital) - seat of government of a country, province, state or other type of administrative territorial entity

--- ENTITIES (Items/Objects) ---
wd:Q252 (Indonesia) - island country in Southeast Asia and Oceania
wd:Q23442 (island) - piece of sub-continental land completely surrounded by water
```

**History (Prompt):**
````text
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
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
wdt:P706 (located in/on physical feature) - located on the specified (geo)physical feature. Should not be used when the value is only political/administrative (P131) or a mountain range (P4552). Use P206 for things in/on bodies of water.
wdt:P36 (capital) - seat of government of a country, province, state or other type of administrative territorial entity

--- ENTITIES (Items/Objects) ---
wd:Q252 (Indonesia) - island country in Southeast Asia and Oceania
wd:Q23442 (island) - piece of sub-continental land completely surrounded by water

### User Question:
On which island is the Indonesian capital located?

```sparql
````
</details>

---
### Q13: WRONG ANS
**Input:** can i play don't starve on play station 4?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASk {wd:Q3208174 wdt:P400 wd:Q5014725.}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT ?game WHERE {   ?game wdt:P400 wd:Q5014725.   ?game wdt:P178 wd:Q3208174. }` |

#### Execution Results
- **Gold:** `No results`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P400 (platform) - platform for which a work was developed or released, or the specific platform version of a software product

--- ENTITIES (Items/Objects) ---
wd:Q5014725 (PlayStation 4) - Sony's fourth home video game console, part of the eighth generation of consoles
wd:Q3208174 (Don't Starve) - 2013 video game developed by Klei Entertainment
```

**History (Prompt):**
````text
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
````
</details>

---
### Q14: SYNTAX ERR
**Input:** How many General Secretaries of the CPSU were there before Leonid Brezhnev?

> **Error:** `Syntax Error: Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT (COUNT(?gensec) as ?result) WHERE{wd:Q765165 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. ?gensec p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 < ?st)}` | `PREFIX wd:` |

#### Execution Results
- **Gold:** `[1 items] 2`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 6
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P580 (start time) - time an entity begins to exist or a statement starts being valid
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q1048744 (General Secretary of the Communist Party of the Soviet Union) - de facto head of state of the Soviet Union and dirigent of the Communist Party of the Soviet Union
wd:Q765165 (Leonid Brezhnev) - General Secretary of the Communist Party of the Soviet Union (1906–1982)
```

**History (Prompt):**
````text
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
wd:Q1048744 (General Secretary of the Communist Party of the Soviet Union) - de facto head of state of the Soviet Union and dirigent of the Communist Party of the Soviet Union
wd:Q765165 (Leonid Brezhnev) - General Secretary of the Communist Party of the Soviet Union (1906–1982)

### User Question:
How many General Secretaries of the CPSU were there before Leonid Brezhnev?

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (COUNT(DISTINCT ?president) AS ?result)
WHERE {
  ?president p:P39 ?pos .
  ?pos ps:P39 wd:Q218295 . # position held is General Secretary of the Communist Party of the Soviet Union
  ?pos pq:P580 ?start . # start
```

SYSTEM: Invalid Query. Line 13, Col 32: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (COUNT(DISTINCT ?president) AS ?result)
WHERE {
  ?president p:P39 ?pos .
  ?pos ps:P39 wd:Q218295 .
  ?pos pq:P580 ?start .
  FILTER(?start < "1990-01-
```

SYSTEM: Invalid Query. Line 14, Col 3: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT  (COUNT(DISTINCT ?president) AS ?result)
WHERE  {
   ?president p:P39 ?pos .
   ?pos ps:P39 wd:Q218295 .
   ?pos pq:P580 ?start .
  FILTER(?start < "1
```

SYSTEM: Invalid Query. Line 14, Col 3: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT  (COUNT(DISTINCT ?president) AS ?result)
WHERE   {
    ?president p:P39  ?pos  .
    ?pos ps:P39 wd:Q218295  .
    ?pos pq:P580 ?start  .
  FILTER(?
```

SYSTEM: Invalid Query. Line 14, Col 3: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
````
</details>

---
### Q15: SYNTAX ERR
**Input:** How many different presidents of Russia have there been that took the position after 1990?

> **Error:** `Syntax Error: Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE{?president p:P39 ?pos. ?pos ps:P39 wd:Q218295. ?pos pq:P580 ?start. FILTER((YEAR(?start)> 1990))}` | `PREFIX wd:` |

#### Execution Results
- **Gold:** `[1 items] 3`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 6
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P580 (start time) - time an entity begins to exist or a statement starts being valid
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q218295 (President of Russia) - head of state of the RSFSR (office established in 1991) and Russia
```

**History (Prompt):**
````text
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
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (COUNT(DISTINCT ?president) AS ?count)
WHERE {
  ?president wdt:P31 wd:Q218295;
             p:P39 ?position.
  ?position ps:P39 wd:Q218295;
            pq:P580 ?start_time.
```

SYSTEM: Invalid Query. Line 14, Col 33: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT  (COUNT(DISTINCT ?president) AS ?count)
WHERE  {
   ?president wdt:P31 wd:Q218295;
             p:P39 ?position.
   ?position ps:P39 wd:Q218295;
            pq:P580 ?start_
```

SYSTEM: Invalid Query. Line 14, Col 28: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
PREFIX wd:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
````
</details>

---
### Q16: SYNTAX ERR
**Input:** Did adam ondra win a medal in the 2020 summer olympics?

> **Error:** `Execution Error: 'results'`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q350568 p:P1344 ?event. ?event ps:P1344 ?eventStatement. ?eventStatement wdt:P361* wd:Q181278. ?event pq:P1352 ?ranking. FILTER(?ranking <= 3)}` | `PREFIX wd:  <http://www.wikidata.org/entity/> PREFIX wdt:  <http://www.wikidata.org/prop/direct/> PREFIX p:  <http://www.wikidata.org/prop/> PREFIX ps:  <http://www.wikidata.org/prop/statement/> PREFIX pq:  <http://www.wikidata.org/prop/qualifier/>  ASK  {   wd:Q350568 p:P1344  ?event.    ?event ps:P1344 wd:Q181278;           pq:P1352  ?rank.   FILTER(?rank < 3) }` |

#### Execution Results
- **Gold:** `No results`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 6
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P361 (part of) - object of which the subject is a part (if this subject is already part of object A which is a part of object B, then please only make the subject part of object A), inverse property of "has part" (P527, see also "has parts of the class" (P2670))
wdt:P1352 (ranking) - subject's ordinal position as qualitatively evaluated relative to other members of a group
wdt:P1344 (participant in) - event in which a person, organization or creative work was/is a participant; inverse of P710 or P1923

--- ENTITIES (Items/Objects) ---
wd:Q350568 (Adam Ondra) - Czech rock climber
wd:Q181278 (2020 Summer Olympics) - games of the XXXII Olympiad, in Tokyo, Japan, held in 2021
```

**History (Prompt):**
````text
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
wdt:P361 (part of) - object of which the subject is a part (if this subject is already part of object A which is a part of object B, then please only make the subject part of object A), inverse property of "has part" (P527, see also "has parts of the class" (P2670))
wdt:P1352 (ranking) - subject's ordinal position as qualitatively evaluated relative to other members of a group
wdt:P1344 (participant in) - event in which a person, organization or creative work was/is a participant; inverse of P710 or P1923

--- ENTITIES (Items/Objects) ---
wd:Q350568 (Adam Ondra) - Czech rock climber
wd:Q181278 (2020 Summer Olympics) - games of the XXXII Olympiad, in Tokyo, Japan, held in 2021

### User Question:
Did adam ondra win a medal in the 2020 summer olympics?

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>

ASK {
  wd:Q350568 p:P1344 ?event.
  ?event ps:P1344 wd:Q181278;
          pq:P1352 ?rank.
  FILTER(?rank < 3)
}
```

SYSTEM: Invalid Query. 'results'
Fix it.
Corrected Query: ```sparql
PREFIX wd: 
<http://www.wikidata.org/entity/>
PREFIX wdt: 
<http://www.wikidata.org/prop/direct/>
PREFIX p: 
<http://www.wikidata.org/prop/>
PREFIX ps: 
<http://www.wikidata.org/prop/statement/>
PREFIX pq: 
<http://www.wikidata.org/prop/qualifier/>

ASK 
{
  wd:Q350568 p:P1344 ?event.
  ?event ps:P1344 wd:Q181278;
          pq:P1352 ?rank.
  FILTER(?rank < 3)
}
```

SYSTEM: Invalid Query. 'results'
Fix it.
Corrected Query: ```sparql
PREFIX wd: 
<http://www.wikidata.org/entity/>
PREFIX wdt: 
<http://www.wikidata.org/prop/direct/>
PREFIX p: 
<http://www.wikidata.org/prop/>
PREFIX ps: 
<http://www.wikidata.org/prop/statement/>
PREFIX pq: 
<http://www.wikidata.org/prop/qualifier/>

ASK 
{
  wd:Q350568 p:P1344  ?event.
   ?event ps:P1344 wd:Q181278;
          pq:P1352 ?rank.
  FILTER(?rank < 3)
}
```

SYSTEM: Invalid Query. 'results'
Fix it.
Corrected Query: ```sparql
PREFIX wd: 
<http://www.wikidata.org/entity/>
PREFIX wdt: 
<http://www.wikidata.org/prop/direct/>
PREFIX p: 
<http://www.wikidata.org/prop/>
PREFIX ps: 
<http://www.wikidata.org/prop/statement/>
PREFIX pq: 
<http://www.wikidata.org/prop/qualifier/>

ASK 
{
  wd:Q350568 p:P1344 ?event.
  ?event ps:P1344 wd:Q181278;
          pq:P1352 ?rank.
  FILTER(?rank < 3)
}
```

SYSTEM: Invalid Query. 'results'
Fix it.
Corrected Query: ```sparql
PREFIX wd: 
<http://www.wikidata.org/entity/>
PREFIX wdt: 
<http://www.wikidata.org/prop/direct/>
PREFIX p: 
<http://www.wikidata.org/prop/>
PREFIX ps: 
<http://www.wikidata.org/prop/statement/>
PREFIX pq: 
<http://www.wikidata.org/prop/qualifier/>

ASK 
{
  wd:Q350568 p:P1344  ?event.
    ?event ps:P1344 wd:Q181278;
          pq:P1352  ?rank.
  FILTER(?rank < 3)
}
```

SYSTEM: Invalid Query. 'results'
Fix it.
Corrected Query: ```sparql
````
</details>

---
### Q17: WRONG ANS
**Input:** Did the Chicago Bulls win at least two seasons of the NBA championship?

> **Error:** `Wrong Answer: F1 Score: 0.00`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{{SELECT (COUNT (?season) AS ?count) WHERE {?season wdt:P3450 wd:Q155223. ?season wdt:P1346 wd:Q128109}} FILTER(?count >= 2)}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT (COUNT(?season) AS ?count) WHERE {   ?season wdt:P31 wd:Q27020041; # instance of season          wdt:P3450 wd:Q155223; # NBA season          wdt:P1346 wd:Q128109. # winner of the season } HAVING (?count >= 2)` |

#### Execution Results
- **Gold:** `No results`
- **Gen:** `[1 items] 6`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
--- PROPERTIES (Relations) ---
wdt:P1346 (winner) - winner of a competition or similar event, not to be used for awards (instead use "award received" (P166) on awardee's item, possibly qualified with "for work" (P1686)) or for wars or battles
wdt:P3450 (sports season of league or competition) - property that shows the competition of which the item is a season. Use P5138 for "season of club or team".

--- ENTITIES (Items/Objects) ---
wd:Q128109 (Chicago Bulls) - American professional basketball team
wd:Q155223 (National Basketball Association) - North American professional basketball league
```

**History (Prompt):**
````text
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
wdt:P1346 (winner) - winner of a competition or similar event, not to be used for awards (instead use "award received" (P166) on awardee's item, possibly qualified with "for work" (P1686)) or for wars or battles
wdt:P3450 (sports season of league or competition) - property that shows the competition of which the item is a season. Use P5138 for "season of club or team".

--- ENTITIES (Items/Objects) ---
wd:Q128109 (Chicago Bulls) - American professional basketball team
wd:Q155223 (National Basketball Association) - North American professional basketball league

### User Question:
Did the Chicago Bulls win at least two seasons of the NBA championship?

```sparql
````
</details>

---

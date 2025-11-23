# Text-to-SPARQL Report

**Model:** `deepseek-coder-6.7b-instruct.Q4_K_M.gguf`
**Date:** 2025-11-23

| Metric | Value |
|---|---|
| Syntax Accuracy | 60.00% |
| Answer Accuracy | 20.00% |
| Avg F1 Score | 0.2000 |
| Self-Corrections | 0 |

---

### Q1: CORRECT
**Input:** After whom is the Riemannian geometry named?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q761383 wdt:P138 ?result. }` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?result WHERE {   wd:Q761383 wdt:P138 ?result. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q42299`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q42299`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- Riemannian geometry (Q761383): branch of differential geometry dealing with (generalized) Riemannian manifolds
- named after (P138): entity or event that inspired the subject's name, or namesake (in at least one language). Qualifier "applies to name" (P5168) can be used to indicate which one
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.
Follow the schema guidelines and use the provided examples.

### Guidelines:
1. Use the provided Schema/Entities.
2. Think step-by-step: first identify the main entity, then the relation.
3. Output ONLY the SPARQL query inside a ```sparql``` code block.

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
- Riemannian geometry (Q761383): branch of differential geometry dealing with (generalized) Riemannian manifolds
- named after (P138): entity or event that inspired the subject's name, or namesake (in at least one language). Qualifier "applies to name" (P5168) can be used to indicate which one

### User Question:
After whom is the Riemannian geometry named?

### Solution:
```sparql
````
</details>

---
### Q2: SYNTAX ERR
**Input:** Which animal participated in a military operation with the Australian Defence Force?

> **Error:** `Syntax Error: Line 2, Col 1: Expected Expected SelectQuery`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt:` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q93208`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 6
<details><summary>Debug Info</summary>

**Context:**
```text
- instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- military operation (Q645883): coordinated military actions of a state or a non-state actor
- Australian Defence Force (Q625657): combined military forces of Australia
- taxon (Q16521): group of one or more organism(s), which a taxonomist adjudges to be a unit
- participant (P710): person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.
Follow the schema guidelines and use the provided examples.

### Guidelines:
1. Use the provided Schema/Entities.
2. Think step-by-step: first identify the main entity, then the relation.
3. Output ONLY the SPARQL query inside a ```sparql``` code block.

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
- instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- military operation (Q645883): coordinated military actions of a state or a non-state actor
- Australian Defence Force (Q625657): combined military forces of Australia
- taxon (Q16521): group of one or more organism(s), which a taxonomist adjudges to be a unit
- participant (P710): person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.

### User Question:
Which animal participated in a military operation with the Australian Defence Force?

### Solution:
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT DISTINCT ?animal ?animalLabel
WHERE 
{
  ?operation wdt:P31 wd:Q645883. # instance of military operation
  ?operation wdt:P710 ?actor. # participant
  ?actor wdt:P171* wd:Q625657. # Australian Defence Force
  ?actor p:
```

SYSTEM: Invalid Query. Line 15, Col 3: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT DISTINCT ?animal ?animalLabel
WHERE 
{
   ?operation wdt:P31 wd:Q645883. # instance of military operation
   ?operation wdt:P710 ?actor. # participant
   ?actor wdt:P171* wd:Q625657. # Australian Defence Force
   ?actor p
```

SYSTEM: Invalid Query. Line 15, Col 4: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT DISTINCT ?animal ?animalLabel
WHERE 
{
    ?operation wdt:P31 wd:Q645883. # instance of military operation
    ?operation wdt:P710 ?actor. # participant
    ?actor wdt:P171* wd:Q625657. # Australian Defence Force
    ?actor p
```

SYSTEM: Invalid Query. Line 15, Col 5: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT DISTINCT ?animal ?animalLabel
WHERE 
{
    ?operation wdt:P31 wd:Q645883.  # instance of military operation
    ?operation wdt:P710 ?actor.  # participant
    ?actor wdt:P171* wd:Q625657.  # Australian Def
```

SYSTEM: Invalid Query. Line 14, Col 51: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT DISTINCT ?animal ?animalLabel
WHERE 
{
    ?operation wdt:P31 wd:Q645883.  # instance of military operation
    ?operation wdt:P710 ?actor.  # participant
    ?actor wdt:P171* wd:Q625657.  #
```

SYSTEM: Invalid Query. Line 14, Col 36: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
````
</details>

---
### Q3: WRONG ANS
**Input:** among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result. ?result wdt:P451 ?p1, ?p2. FILTER(?p1 != ?p2 &&(?result IN (wd:Q4205826, wd:Q4463198)))}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/>  SELECT ?character ?characterLabel ?partner1 ?partner1Label ?partner2 ?partner2Label WHERE {   ?character wdt:P674 wd:Q11835640; # characters in the Witcher series             wdt:P451 ?partnerStatement. # unmarried partner   ?partnerStatement ps:P26 ?partner. # spouse   ?partner wdt:P31 wd:Q515. # instance of human   OPTIONAL {     ?character wdt:P451 ?partnerStatement2. # second unmarried partner     ?partnerStatement2 ps:P26 ?partner2. # second spouse     ?partner2 wdt:P31 wd:Q515. # second instance of human   }   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q4205826`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- The Witcher (Q11835640): series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
- unmarried partner (P451): someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples
- characters (P674): characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)
- Triss Merigold (Q4463198): fictional sorceress from the Witcher series
- Yennefer of Vengerberg (Q4205826): fictional sorceress from the Witcher series
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.
Follow the schema guidelines and use the provided examples.

### Guidelines:
1. Use the provided Schema/Entities.
2. Think step-by-step: first identify the main entity, then the relation.
3. Output ONLY the SPARQL query inside a ```sparql``` code block.

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
- The Witcher (Q11835640): series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
- unmarried partner (P451): someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples
- characters (P674): characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)
- Triss Merigold (Q4463198): fictional sorceress from the Witcher series
- Yennefer of Vengerberg (Q4205826): fictional sorceress from the Witcher series

### User Question:
among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

### Solution:
```sparql
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
- founded by (P112): founder or co-founder of this organization, religion, place or entity
- position held (P39): subject currently or formerly holds the object position or public office
- National People's Congress deputy (Q10891456): member of Chinese National People's Congress
- Tencent (Q860580): Chinese multinational investment holding conglomerate
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.
Follow the schema guidelines and use the provided examples.

### Guidelines:
1. Use the provided Schema/Entities.
2. Think step-by-step: first identify the main entity, then the relation.
3. Output ONLY the SPARQL query inside a ```sparql``` code block.

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
- founded by (P112): founder or co-founder of this organization, religion, place or entity
- position held (P39): subject currently or formerly holds the object position or public office
- National People's Congress deputy (Q10891456): member of Chinese National People's Congress
- Tencent (Q860580): Chinese multinational investment holding conglomerate

### User Question:
among the founders of tencent company, who has been member of national people’s congress?

### Solution:
```sparql
````
</details>

---
### Q5: SYNTAX ERR
**Input:** among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

> **Error:** `Syntax Error: Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P800 ?result. ?result wdt:P921 wd:Q16003532 FILTER(?result != wd:Q69071)}` | `PREFIX wd:` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q18225473`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 6
<details><summary>Debug Info</summary>

**Context:**
```text
- Hunter × Hunter (Q696071): Japanese manga series
- Münchenbuchsee (Q69071): municipality in the canton of Bern in Switzerland
- main subject (P921): primary topic of a work or act of communication
- author (P50): main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
- middle school student (Q16003532): student in late primary or early secondary education
- notable work (P800): notable scientific, artistic or literary work, or other work of significance among subject's works
```

**History (Prompt):**
````text
You are an expert SPARQL developer for Wikidata.
Your task is to translate a natural language question into a valid SPARQL query.
Follow the schema guidelines and use the provided examples.

### Guidelines:
1. Use the provided Schema/Entities.
2. Think step-by-step: first identify the main entity, then the relation.
3. Output ONLY the SPARQL query inside a ```sparql``` code block.

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
- Hunter × Hunter (Q696071): Japanese manga series
- Münchenbuchsee (Q69071): municipality in the canton of Bern in Switzerland
- main subject (P921): primary topic of a work or act of communication
- author (P50): main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
- middle school student (Q16003532): student in late primary or early secondary education
- notable work (P800): notable scientific, artistic or literary work, or other work of significance among subject's works

### User Question:
among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

### Solution:
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wdt:P50: <http://www.wikidata.org/prop/direct/P50>
PREFIX wdt:P800: <http://www.wikidata.org/prop/direct/P800>
PREFIX wdt:P921: <http://www.wikidata.org/prop/direct/P921>

SELECT ?work WHERE {
  wd:Q696071 wdt:P50 ?author.
  ?work wdt:P800 ?author; wdt:P921 wd:Q16003532.
}
```

SYSTEM: Invalid Query. Line 3, Col 1: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt:
```

SYSTEM: Invalid Query. Line 2, Col 1: Expected Expected SelectQuery
Fix it.
Corrected Query: ```sparql
PREFIX wd:
```

SYSTEM: Invalid Query. Line 1, Col 1: Expected Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}
Fix it.
Corrected Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wdt:P50: <http://www.wikidata.org/prop/direct/P50>
PREFIX wdt:P800: <http://www.wikidata.org/prop/direct/P800>
PREFIX wdt:P921: <http://www.wikidata.org/prop/direct/P921>

SELECT ?work WHERE {
  wd:Q696071 wdt:P50 ?author.
  ?work wdt:P800 ?author; wdt:P921 wd:Q16003532.
}
```

SYSTEM: Invalid Query. Line 3, Col 1: Expected Expected SelectQuery
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

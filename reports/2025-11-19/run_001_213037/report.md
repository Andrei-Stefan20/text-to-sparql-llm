# Text-to-SPARQL Report

**Model:** `deepseek-coder-6.7b-instruct.Q4_K_M.gguf`
**Date:** 2025-11-19

| Metric | Value |
|---|---|
| Syntax Accuracy | 100.00% |
| Answer Accuracy | 25.00% |
| Avg F1 Score | 0.2500 |
| Self-Corrections | 0 |

---

### Q1: CORRECT
**Input:** After whom is the Riemannian geometry named?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q761383 wdt:P138 ?result. }` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?res WHERE { wd:Q761383 wdt:P138 ?res. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q42299`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q42299`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- named after (P138): entity or event that inspired the subject's name, or namesake (in at least one language). Qualifier "applies to name" (P5168) can be used to indicate which one
- Riemannian geometry (Q761383): branch of differential geometry dealing with (generalized) Riemannian manifolds
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - named after (P138): entity or event that inspired the subject's name, or namesake (in at least one language). Qualifier "applies to name" (P5168) can be used to indicate which one
- Riemannian geometry (Q761383): branch of differential geometry dealing with (generalized) Riemannian manifolds

            ### Examples:
            User: Where is the birthplace of Goethe?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?res WHERE { wd:Q5879 wdt:P19 ?res . } 
```

User: What is the highest mountain in Italy?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P31 wd:Q8502 ; wdt:P17 wd:Q38 ; wdt:P2044 ?elevation . } ORDER BY DESC(?elevation) LIMIT 1
```

User: What is the birth name of Adele?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?name WHERE { wd:Q23215 wdt:P1477 ?name. }
```

User: After whom is the Riemannian geometry named?
Query: ```sparql
````
</details>

---
### Q2: WRONG ANS
**Input:** Which animal participated in a military operation with the Australian Defence Force?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P31 wd:Q16521; wdt:P136 wd:Q625657. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q93208`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- participant (P710): person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.
- taxon (Q16521): group of one or more organism(s), which a taxonomist adjudges to be a unit
- Australian Defence Force (Q625657): combined military forces of Australia
- military operation (Q645883): coordinated military actions of a state or a non-state actor
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- participant (P710): person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.
- taxon (Q16521): group of one or more organism(s), which a taxonomist adjudges to be a unit
- Australian Defence Force (Q625657): combined military forces of Australia
- military operation (Q645883): coordinated military actions of a state or a non-state actor

            ### Examples:
            User: Which animals are critically endangered?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P141 wd:Q219127 }
```

User: Give me all Australian metalcore bands.
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P31 wd:Q215380 ; wdt:P495 wd:Q408 ; wdt:P136 wd:Q183862 . }
```

User: What is the largest city in Australia?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P31/wdt:P279* wd:Q515 ; wdt:P17 wd:Q408 ; wdt:P1082 ?population . } ORDER BY DESC(?population) LIMIT 1
```

User: Which animal participated in a military operation with the Australian Defence Force?
Query: ```sparql
````
</details>

---
### Q3: WRONG ANS
**Input:** among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result. ?result wdt:P451 ?p1, ?p2. FILTER(?p1 != ?p2 &&(?result IN (wd:Q4205826, wd:Q4463198)))}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?item ?itemLabel WHERE {   ?item wdt:P674 wd:Q11835640;         wdt:P451 ?partner1, ?partner2.   FILTER (?partner1 != ?partner2).   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q4205826`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- characters (P674): characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)
- Triss Merigold (Q4463198): fictional sorceress from the Witcher series
- Yennefer of Vengerberg (Q4205826): fictional sorceress from the Witcher series
- The Witcher (Q11835640): series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
- unmarried partner (P451): someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - characters (P674): characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)
- Triss Merigold (Q4463198): fictional sorceress from the Witcher series
- Yennefer of Vengerberg (Q4205826): fictional sorceress from the Witcher series
- The Witcher (Q11835640): series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
- unmarried partner (P451): someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples

            ### Examples:
            User: Which monarchs were married to a German?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P106 wd:Q116 ; wdt:P26 ?spouse . ?spouse wdt:P27 wd:Q183 . }
```

User: Who has Tom Cruise been married to?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?o1 WHERE { wd:Q37079 wdt:P26 ?o1 . }
```

User: Who was Tom Hanks married to?
Query: ```sparql
SELECT ?o1 WHERE { <http://www.wikidata.org/entity/Q2263>  <http://www.wikidata.org/prop/direct/P26>  ?o1 .  }
```

User: among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?
Query: ```sparql
````
</details>

---
### Q4: WRONG ANS
**Input:** among the founders of tencent company, who has been member of national people’s congress?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?result. ?result wdt:P39 wd:Q10891456.}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?founder WHERE { ?founder wdt:P112 wd:Q860580. ?founder wdt:P39 wd:Q10891456. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q1739008`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- Tencent (Q860580): Chinese multinational investment holding conglomerate
- founded by (P112): founder or co-founder of this organization, religion, place or entity
- position held (P39): subject currently or formerly holds the object position or public office
- National People's Congress deputy (Q10891456): member of Chinese National People's Congress
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - Tencent (Q860580): Chinese multinational investment holding conglomerate
- founded by (P112): founder or co-founder of this organization, religion, place or entity
- position held (P39): subject currently or formerly holds the object position or public office
- National People's Congress deputy (Q10891456): member of Chinese National People's Congress

            ### Examples:
            User: How many companies were founded by the founder of Facebook?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ( COUNT( DISTINCT ?uri ) AS ?c ) WHERE { ?uri wdt:P112 wd:Q36215 . ?uri wdt:P31/wdt:P279* wd:Q783794 . } 
```

User: Who owns Aldi?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?uri WHERE { wd:Q125054 wdt:P355 ?uri }
```

User: Which organizations were founded in 1930?
Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT * WHERE { ?sub wdt:P571 ?year . ?sub wdt:P31/wdt:P131* wd:Q43229 . FILTER(year(?year) = 1930) . } 
```

User: among the founders of tencent company, who has been member of national people’s congress?
Query: ```sparql
````
</details>

---
### Q5: WRONG ANS
**Input:** among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P800 ?result. ?result wdt:P921 wd:Q16003532 FILTER(?result != wd:Q69071)}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P31 wd:Q16003532 . }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q18225473`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- notable work (P800): notable scientific, artistic or literary work, or other work of significance among subject's works
- Münchenbuchsee (Q69071): municipality in the canton of Bern in Switzerland
- middle school student (Q16003532): student in late primary or early secondary education
- Hunter × Hunter (Q696071): Japanese manga series
- author (P50): main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
- main subject (P921): primary topic of a work or act of communication
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - notable work (P800): notable scientific, artistic or literary work, or other work of significance among subject's works
- Münchenbuchsee (Q69071): municipality in the canton of Bern in Switzerland
- middle school student (Q16003532): student in late primary or early secondary education
- Hunter × Hunter (Q696071): Japanese manga series
- author (P50): main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
- main subject (P921): primary topic of a work or act of communication

            ### Examples:
            User: Who is the novelist of the work a song of ice and fire?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { wd:Q45875 ?p ?uri . ?uri wdt:P106 wd:Q6625963 . }
```

User: Which books were written by Danielle Steel?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P50 wd:Q72653 . ?uri wdt:P136 ?genre . ?genre wdt:P279* wd:Q571 . }
```

User: Who are the writers of the Wall album of Pink Floyd?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { wd:Q151114 wdt:P658 ?track . ?track wdt:P162 ?uri . }
```

User: among the other representative work of the author of hunter x hunter, which one is talking about middle school student?
Query: ```sparql
````
</details>

---
### Q6: CORRECT
**Input:** On which stock exchanges are Siemens AG shares traded?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q81230 wdt:P414 ?result}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?exchange WHERE { wd:Q81230 wdt:P414 ?exchange }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q151139`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q151139`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- stock exchange (P414): exchange on which this company is traded
- Siemens (Q81230): German multinational conglomerate company
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - stock exchange (P414): exchange on which this company is traded
- Siemens (Q81230): German multinational conglomerate company

            ### Examples:
            User: What is the revenue of IBM?
Query: ```sparql
 SELECT ?o1 WHERE { <http://www.wikidata.org/entity/Q37156>  <http://www.wikidata.org/prop/direct/P2139>  ?o1 .  }
```

User: Give me all companies in Munich.
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?type wdt:P279* wd:Q4830453 . ?uri wdt:P31 ?type ; wdt:P159 wd:Q1726 . }
```

User: Give me the homepage of Forbes.
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?uri WHERE { wd:Q25161472 wdt:P856 ?uri } 
```

User: On which stock exchanges are Siemens AG shares traded?
Query: ```sparql
````
</details>

---
### Q7: WRONG ANS
**Input:** Apart from the book series the witcher, name all of the author’s notable work.

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P50 ?author. ?author wdt:P800 ?result. FILTER(?result != wd:Q11835640)}` | `SELECT DISTINCT ?work WHERE {    <http://www.wikidata.org/entity/Q11835640> <http://www.wikidata.org/prop/direct/P800> ?work. }` |

#### Execution Results
- **Gold:** `[5 items] http://www.wikidata.org/entity/Q2045474; http://www.wikidata.org/entity/Q2414756; http://www.wikidata.org/entity/Q4080260 ... (2 more)`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- The Witcher (Q11835640): series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
- author (P50): main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
- notable work (P800): notable scientific, artistic or literary work, or other work of significance among subject's works
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - The Witcher (Q11835640): series of fantasy novels and short stories by Polish writer Andrzej Sapkowski
- author (P50): main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
- notable work (P800): notable scientific, artistic or literary work, or other work of significance among subject's works

            ### Examples:
            User: Who wrote Harry Potter?
Query: ```sparql
SELECT DISTINCT ?uri WHERE { <http://www.wikidata.org/entity/Q8337> <http://www.wikidata.org/prop/direct/P50> ?uri}
```

User: Which poet wrote the most books?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P106 wd:Q49757 . ?x wdt:P50 ?uri ; wdt:P31 wd:Q571 . } GROUP BY ?uri ORDER BY DESC(COUNT(?x)) LIMIT 1
```

User: Which poet wrote the most books?
Query: ```sparql
 SELECT DISTINCT ?s1 (COUNT(?s2) as ?c ) WHERE { ?s1  <http://www.wikidata.org/prop/direct/P106>  <http://www.wikidata.org/entity/Q49757> . ?s2  <http://www.wikidata.org/prop/direct/P50>  ?s1 . ?s2  <http://www.wikidata.org/prop/direct/P31>  <http://www.wikidata.org/entity/Q571> .  } GROUP BY ?s1 ORDER BY DESC(COUNT(?s2)) OFFSET 0 LIMIT 1
```

User: Apart from the book series the witcher, name all of the author’s notable work.
Query: ```sparql
````
</details>

---
### Q8: WRONG ANS
**Input:** are brooke raboutou and colin duffy from same state of the usa?

> **Error:** `Wrong Answer: Result mismatch (F1=0.00)`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q2926117 wdt:P19 ?b1. wd:Q87192979 wdt:P19 ?b2. ?b1 wdt:P131* ?state. ?b2 wdt:P131* ?state. ?state wdt:P31 wd:Q35657 .}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?brookeState ?colinState WHERE {   ?brookeUri wdt:P19 ?brookeState.   ?colinUri wdt:P19 ?colinState.   VALUES ?brookeUri {wd:Q2926117}   VALUES ?colinUri {wd:Q87192979} }` |

#### Execution Results
- **Gold:** `No results`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q192517, http://www.wikidata.org/entity/Q492819`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- Brooke Raboutou (Q2926117): American sport climber
- place of birth (P19): most specific known birth location of a person, animal or fictional character
- located in the administrative territorial entity (P131): the item is located on the territory of the following administrative entity. Use P276 for specifying locations that are non-administrative places and for items about events. Use P1382 if the item falls only partially into the administrative entity.
- U.S. state (Q35657): constituent political entity of the United States of America
- Colin Duffy (Q87192979): Sport climber from the United States
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- Brooke Raboutou (Q2926117): American sport climber
- place of birth (P19): most specific known birth location of a person, animal or fictional character
- located in the administrative territorial entity (P131): the item is located on the territory of the following administrative entity. Use P276 for specifying locations that are non-administrative places and for items about events. Use P1382 if the item falls only partially into the administrative entity.
- U.S. state (Q35657): constituent political entity of the United States of America
- Colin Duffy (Q87192979): Sport climber from the United States

            ### Examples:
            User: How many politicians graduated from Columbia University?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT (COUNT(DISTINCT ?uri) AS ?c) WHERE { ?uri wdt:P106 wd:Q82955 ; wdt:P69 wd:Q49088 . }
```

User: Who is the daughter of Robert Kennedy married to?
Query: ```sparql
SELECT DISTINCT ?uri WHERE { <http://www.wikidata.org/entity/Q25310> <http://www.wikidata.org/prop/direct/P40> ?daughter . ?daughter  <http://www.wikidata.org/prop/direct/P21> <http://www.wikidata.org/entity/Q6581072> . ?daughter  <http://www.wikidata.org/prop/direct/P26> ?uri .}
```

User: Who is the husband of Amanda Palmer?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?uri WHERE { ?uri wdt:P26 wd:Q240377 } 
```

User: are brooke raboutou and colin duffy from same state of the usa?
Query: ```sparql
````
</details>

---
### Q9: CORRECT
**Input:** What is the boiling point of water?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q283 wdt:P2102 ?result}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?boilingPoint WHERE { wd:Q283 wdt:P2102 ?boilingPoint }` |

#### Execution Results
- **Gold:** `[1 items] 99.9839`
- **Gen:** `[1 items] 99.9839`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- boiling point (P2102): temperature at which a substance changes its phase from liquid to gas (indicate the corresponding pressure as qualifier)
- water (Q283): chemical compound whose molecules are formed by two hydrogen atoms and one oxygen atom
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - boiling point (P2102): temperature at which a substance changes its phase from liquid to gas (indicate the corresponding pressure as qualifier)
- water (Q283): chemical compound whose molecules are formed by two hydrogen atoms and one oxygen atom

            ### Examples:
            User: How deep is Lake Chiemsee?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?n WHERE { wd:Q4138  wdt:P4511 ?n }
```

User: What is the highest mountain?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P31 wd:Q8502 ; wdt:P2044 ?elevation . } ORDER BY DESC(?elevation) LIMIT 1
```

User: What is the longest river in China?
Query: ```sparql
SELECT DISTINCT ?uri WHERE { ?uri <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q4022> . ?uri <http://www.wikidata.org/prop/direct/P17> <http://www.wikidata.org/entity/Q148> . ?uri <http://www.wikidata.org/prop/direct/P2043> ?length } ORDER BY DESC(?length) LIMIT 1
```

User: What is the boiling point of water?
Query: ```sparql
````
</details>

---
### Q10: CORRECT
**Input:** At which school was Yayoi Kusama educated at?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q231121 wdt:P69 ?result}` | `PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT DISTINCT ?uri WHERE { wd:Q231121 wdt:P69 ?uri }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q749884`
- **Gen:** `[1 items] http://www.wikidata.org/entity/Q749884`

**F1:** 1.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- Yayoi Kusama (Q231121): Japanese painter, performance, and installation artist (born 1929)
- educated at (P69): educational institution attended by subject
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - Yayoi Kusama (Q231121): Japanese painter, performance, and installation artist (born 1929)
- educated at (P69): educational institution attended by subject

            ### Examples:
            User: Which movies did Kurosawa direct?
Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT DISTINCT * WHERE { ?uri wdt:P57 wd:Q8006 . } 
```

User: Which university did Angela Merkel attend?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { VALUES ?types { wd:Q3918 wd:Q875538 } wd:Q567 wdt:P69 ?uri . ?uri wdt:P31 ?types . }
```

User: In which city did Nikos Kazantzakis die?
Query: ```sparql
SELECT DISTINCT ?uri WHERE { <http://www.wikidata.org/entity/Q214622> <http://www.wikidata.org/prop/direct/P20> ?uri }
```

User: At which school was Yayoi Kusama educated at?
Query: ```sparql
````
</details>

---
### Q11: WRONG ANS
**Input:** Which High School did Allen Ginsberg attend?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q6711 wdt:P69 ?result. ?result wdt:P31 wd:Q9826}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P106 wd:Q6711; wdt:P69 ?school. }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q14705485`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- high school (Q9826): institution which provides final part of secondary education
- Allen Ginsberg (Q6711): American poet and writer (1926–1997)
- educated at (P69): educational institution attended by subject
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- high school (Q9826): institution which provides final part of secondary education
- Allen Ginsberg (Q6711): American poet and writer (1926–1997)
- educated at (P69): educational institution attended by subject

            ### Examples:
            User: How many scientists graduated from an Ivy League university?
Query: ```sparql
PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT (COUNT(DISTINCT ?uri) AS ?c) WHERE { ?uri wdt:P106 wd:Q901 . ?uri wdt:P69 ?university. wd:Q49113  wdt:P527 ?university . }
```

User: Which university did Angela Merkel attend?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { VALUES ?types { wd:Q3918 wd:Q875538 } wd:Q567 wdt:P69 ?uri . ?uri wdt:P31 ?types . }
```

User: How many politicians graduated from Columbia University?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT (COUNT(DISTINCT ?uri) AS ?c) WHERE { ?uri wdt:P106 wd:Q82955 ; wdt:P69 wd:Q49088 . }
```

User: Which High School did Allen Ginsberg attend?
Query: ```sparql
````
</details>

---
### Q12: WRONG ANS
**Input:** On which island is the Indonesian capital located?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q252 wdt:P36 ?capital. ?capital wdt:P706 ?result. ?result wdt:P31 wd:Q23442}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?capital wdt:P36 wd:Q252 . ?capital wdt:P206 ?uri . }` |

#### Execution Results
- **Gold:** `[1 items] http://www.wikidata.org/entity/Q3757`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- located in/on physical feature (P706): located on the specified (geo)physical feature. Should not be used when the value is only political/administrative (P131) or a mountain range (P4552). Use P206 for things in/on bodies of water.
- capital (P36): seat of government of a country, province, state or other type of administrative territorial entity
- island (Q23442): piece of sub-continental land completely surrounded by water
- Indonesia (Q252): island country in Southeast Asia and Oceania
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - instance of (P31): type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain
- located in/on physical feature (P706): located on the specified (geo)physical feature. Should not be used when the value is only political/administrative (P131) or a mountain range (P4552). Use P206 for things in/on bodies of water.
- capital (P36): seat of government of a country, province, state or other type of administrative territorial entity
- island (Q23442): piece of sub-continental land completely surrounded by water
- Indonesia (Q252): island country in Southeast Asia and Oceania

            ### Examples:
            User: What is the capital of Cameroon?
Query: ```sparql
SELECT DISTINCT ?uri WHERE { <http://www.wikidata.org/entity/Q1009> <http://www.wikidata.org/prop/direct/P36> ?uri}
```

User: Who is the mayor of the capital of French Polynesia?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/>  PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { wd:Q30971 wdt:P36 ?capital . ?capital wdt:P6 ?uri . }
```

User: Give me all islands that belong to Japan.
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P31 wd:Q23442 ; wdt:P17 wd:Q17 . }
```

User: On which island is the Indonesian capital located?
Query: ```sparql
````
</details>

---
### Q13: WRONG ANS
**Input:** can i play don't starve on play station 4?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASk {wd:Q3208174 wdt:P400 wd:Q5014725.}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P1344 wd:Q3208174 . }` |

#### Execution Results
- **Gold:** `No results`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- platform (P400): platform for which a work was developed or released, or the specific platform version of a software product
- Don't Starve (Q3208174): 2013 video game developed by Klei Entertainment
- PlayStation 4 (Q5014725): Sony's fourth home video game console, part of the eighth generation of consoles
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - platform (P400): platform for which a work was developed or released, or the specific platform version of a software product
- Don't Starve (Q3208174): 2013 video game developed by Klei Entertainment
- PlayStation 4 (Q5014725): Sony's fourth home video game console, part of the eighth generation of consoles

            ### Examples:
            User: List all boardgames by GMT.
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?uri WHERE { ?uri wdt:P31 wd:Q131436 . }
```

User: List all games by GMT.
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P31/wdt:P279* wd:Q11410 ; wdt:P123 wd:Q928726 . }
```

User: Who wrote The Hunger Games?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { wd:Q11679 wdt:P50 ?uri . }
```

User: can i play don't starve on play station 4?
Query: ```sparql
````
</details>

---
### Q14: WRONG ANS
**Input:** How many General Secretaries of the CPSU were there before Leonid Brezhnev?

> **Error:** `Wrong Answer: Result mismatch (F1=0.00)`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT (COUNT(?gensec) as ?result) WHERE{wd:Q765165 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. ?gensec p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 < ?st)}` | `SELECT (COUNT(DISTINCT ?uri) as ?count) WHERE {   ?uri wdt:P39 wd:Q1048744;        p:P39/ps:P39 ?statement.   ?statement pq:P580 ?start_time.   FILTER(?start_time < "1906-01-01"^^xsd:date && ?start_time > "1899-12-31"^^xsd:date) }` |

#### Execution Results
- **Gold:** `[1 items] 2`
- **Gen:** `[1 items] 0`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- start time (P580): time an entity begins to exist or a statement starts being valid
- Leonid Brezhnev (Q765165): General Secretary of the Communist Party of the Soviet Union (1906–1982)
- position held (P39): subject currently or formerly holds the object position or public office
- General Secretary of the Communist Party of the Soviet Union (Q1048744): de facto head of state of the Soviet Union and dirigent of the Communist Party of the Soviet Union
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - start time (P580): time an entity begins to exist or a statement starts being valid
- Leonid Brezhnev (Q765165): General Secretary of the Communist Party of the Soviet Union (1906–1982)
- position held (P39): subject currently or formerly holds the object position or public office
- General Secretary of the Communist Party of the Soviet Union (Q1048744): de facto head of state of the Soviet Union and dirigent of the Communist Party of the Soviet Union

            ### Examples:
            User: How many politicians graduated from Columbia University?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT (COUNT(DISTINCT ?uri) AS ?c) WHERE { ?uri wdt:P106 wd:Q82955 ; wdt:P69 wd:Q49088 . }
```

User: How many emperors did China have?
Query: ```sparql
SELECT (COUNT(DISTINCT ?uri) as ?count) WHERE {  ?uri <http://www.wikidata.org/prop/direct/P39> <http://www.wikidata.org/entity/Q268218>}
```

User: Who is the mayor of Berlin?
Query: ```sparql
SELECT ?o1 WHERE { <http://www.wikidata.org/entity/Q64>  <http://www.wikidata.org/prop/direct/P6>  ?o1 .  }
```

User: How many General Secretaries of the CPSU were there before Leonid Brezhnev?
Query: ```sparql
````
</details>

---
### Q15: WRONG ANS
**Input:** How many different presidents of Russia have there been that took the position after 1990?

> **Error:** `Wrong Answer: Result mismatch (F1=0.00)`

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE{?president p:P39 ?pos. ?pos ps:P39 wd:Q218295. ?pos pq:P580 ?start. FILTER((YEAR(?start)> 1990))}` | `SELECT (COUNT(DISTINCT ?uri) as ?count) WHERE { ?uri <http://www.wikidata.org/prop/direct/P39>/<http://www.wikidata.org/prop/direct/P279>/<http://www.wikidata.org/prop/direct/P580> ?start . FILTER(year(?start) > 1990) }` |

#### Execution Results
- **Gold:** `[1 items] 3`
- **Gen:** `[1 items] 4554`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- start time (P580): time an entity begins to exist or a statement starts being valid
- position held (P39): subject currently or formerly holds the object position or public office
- President of Russia (Q218295): head of state of the RSFSR (office established in 1991) and Russia
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - start time (P580): time an entity begins to exist or a statement starts being valid
- position held (P39): subject currently or formerly holds the object position or public office
- President of Russia (Q218295): head of state of the RSFSR (office established in 1991) and Russia

            ### Examples:
            User: Which presidents were born in 1945?
Query: ```sparql
SELECT DISTINCT ?uri WHERE { ?uri <http://www.wikidata.org/prop/direct/P39>/<http://www.wikidata.org/prop/direct/P279> <http://www.wikidata.org/entity/Q30461> . ?uri <http://www.wikidata.org/prop/direct/P569> ?date . FILTER(year(?date)=1945) }
```

User: How many emperors did China have?
Query: ```sparql
SELECT (COUNT(DISTINCT ?uri) as ?count) WHERE {  ?uri <http://www.wikidata.org/prop/direct/P39> <http://www.wikidata.org/entity/Q268218>}
```

User: How many missions does the Soyuz programme have?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT (COUNT(DISTINCT ?uri) AS ?c) WHERE { ?uri wdt:P361 wd:Q207329 }
```

User: How many different presidents of Russia have there been that took the position after 1990?
Query: ```sparql
````
</details>

---
### Q16: WRONG ANS
**Input:** Did adam ondra win a medal in the 2020 summer olympics?

| Gold Query | Generated Query |
|---|---|
| `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q350568 p:P1344 ?event. ?event ps:P1344 ?eventStatement. ?eventStatement wdt:P361* wd:Q181278. ?event pq:P1352 ?ranking. FILTER(?ranking <= 3)}` | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?medal WHERE { wd:Q350568 wdt:P1352 ?medal . }` |

#### Execution Results
- **Gold:** `No results`
- **Gen:** `No results`

**F1:** 0.00 | **Attempts:** 1
<details><summary>Debug Info</summary>

**Context:**
```text
- participant in (P1344): event in which a person, organization or creative work was/is a participant; inverse of P710 or P1923
- part of (P361): object of which the subject is a part (if this subject is already part of object A which is a part of object B, then please only make the subject part of object A), inverse property of "has part" (P527, see also "has parts of the class" (P2670))
- Adam Ondra (Q350568): Czech rock climber
- 2020 Summer Olympics (Q181278): games of the XXXII Olympiad, in Tokyo, Japan, held in 2021
- ranking (P1352): subject's ordinal position as qualitatively evaluated relative to other members of a group
```

**History:**
````text
You are a SPARQL expert for Wikidata.
            Output ONLY the SPARQL code inside a ```sparql block.

            ### Schema Context (Use these IDs):
            - participant in (P1344): event in which a person, organization or creative work was/is a participant; inverse of P710 or P1923
- part of (P361): object of which the subject is a part (if this subject is already part of object A which is a part of object B, then please only make the subject part of object A), inverse property of "has part" (P527, see also "has parts of the class" (P2670))
- Adam Ondra (Q350568): Czech rock climber
- 2020 Summer Olympics (Q181278): games of the XXXII Olympiad, in Tokyo, Japan, held in 2021
- ranking (P1352): subject's ordinal position as qualitatively evaluated relative to other members of a group

            ### Examples:
            User: How tall is Michael Jordan?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?val WHERE { wd:Q41421 wdt:P2048 ?val . }
```

User: Who is the youngest Darts player?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P106 wd:Q18574233 ; wdt:P569 ?dateOfBirth . } ORDER BY DESC(?dateOfBirth) LIMIT 1
```

User: Who is the tallest basketball player?
Query: ```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { ?uri wdt:P106 wd:Q3665646 ; wdt:P2048 ?height . } ORDER BY DESC(?height) LIMIT 1
```

User: Did adam ondra win a medal in the 2020 summer olympics?
Query: ```sparql
````
</details>

---

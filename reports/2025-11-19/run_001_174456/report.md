# Text-to-SPARQL Evaluation Report

- **Model:** `mistral-7b-instruct-v0.2.Q4_K_M.gguf`
- **Accuracy:** **28.57%** (4/14)

---

## ❌ Q1: After whom is the Riemannian geometry named?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q761383 wdt:P138 ?result. }` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFX wd: <http://www.wikidata.org/entity/> SELECT ?name WHERE { wd:Q12732 wdt:P31 wd:Q11283 ; wdt:P147 ?name . }` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *Where is the birthplace of Goethe?*
2. *What is the highest mountain in Italy?*
3. *What is the birth name of Adele?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ✅ Q2: Which animal participated in a military operation with the Australian Defence Force?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?animal WHERE { ?animal wdt:P31 wd:Q18923 ; wdt:P180 wd:Q219127 ; wdt:P182 wd:Q12732 ; wdt:P18 wd:Q233554 . }` |

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *Which animals are critically endangered?*
2. *Give me all Australian metalcore bands.*
3. *What is the largest city in Australia?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q3: among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result. ?result wdt:P451 ?p1, ?p2. FILTER(?p1 != ?p2 &&(?result IN (wd:Q4205826, wd:Q4463198)))}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?character WHERE {   ?character wdt:P31 wd:Q17123 . # Witcher character   { ?character wdt:P147 ?partner1 . } # Partner 1   { ?character wdt:P147 ?partner2 . .} # Partner 2   FILTER(CONTAINS(STR(?partner1), "Yennefer") \|\| CONTAINS(STR(?partner1), "Vengerberg"))   FILTER(CONTAINS(STR(?partner2), "Triss") \|\| CONTAINS(STR(?partner2), "Merigold"))   FILTER(NOT EXISTS { ?character wdt:P26 ?_ . }) # Unmarried }` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *Which monarchs were married to a German?*
2. *Who has Tom Cruise been married to?*
3. *Who was Tom Hanks married to?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q4: among the founders of tencent company, who has been member of national people’s congress?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?result. ?result wdt:P39 wd:Q10891456.}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?person WHERE { wd:Q10421 wdt:P11 wd:?person ; wdt:P31 wdt:Q184235 ; wdt:P1512 wd:Q12582 . ?person wdt:P1512 ?member . ?member wdt:P31 wdt:Q1312377 . }  GROUP BY ?person HAVING (COUNT(?member) > 0)  ORDER BY DESC(COUNT(?member)) FILTER(lang(?person) = "en")` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *How many companies were founded by the founder of Facebook?*
2. *Who owns Aldi?*
3. *Which organizations were founded in 1930?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ✅ Q5: among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P800 ?result. ?result wdt:P921 wd:Q16003532 FILTER(?result != wd:Q69071)}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { wd:Q1225 wdt:P106 ?uri . ?uri wdt:P31 wd:Q1312 . ?uri wdt:P1828 ?age . FILTER(lang(str(?age)) = "en" && str(?age) = "middle school") }` |

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *Who is the novelist of the work a song of ice and fire?*
2. *Which books were written by Danielle Steel?*
3. *Who are the writers of the Wall album of Pink Floyd?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ✅ Q6: On which stock exchanges are Siemens AG shares traded?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q81230 wdt:P414 ?result}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?exchange WHERE { wd:Q11223 wdt:P159 wd:Q1275 . ?exchange wdt:P31 wd:Q13123 . wd:Q11223 wdt:P2139 ?stock . ?stock wdt:P159 ?exchange . }` |

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *What is the revenue of IBM?*
2. *Give me all companies in Munich.*
3. *Give me the homepage of Forbes.*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q7: Apart from the book series the witcher, name all of the author’s notable work.

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P50 ?author. ?author wdt:P800 ?result. FILTER(?result != wd:Q11835640)}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?uri WHERE { <http://www.wikidata.org/entity/Q12345> wdt:P106 ?uri ; wdt:P31 wd:Q104391256 . FILTER(lang(label(?uri, "en")) = "Andrzej Sapkowski") . FILTER NOT EXISTS { ?uri wdt:P1828 ?book . } }` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *Who wrote Harry Potter?*
2. *Which poet wrote the most books?*
3. *Which poet wrote the most books?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q8: are brooke raboutou and colin duffy from same state of the usa?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q2926117 wdt:P19 ?b1. wd:Q87192979 wdt:P19 ?b2. ?b1 wdt:P131* ?state. ?b2 wdt:P131* ?state. ?state wdt:P31 wd:Q35657 .}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT (BOOLEAN(SAMPLE(?state1, ?state2) = SAMPLE(?state3, ?state2))) AS ?same_state WHERE { wd:Q13143 wdt:P17 wd:Q112235 . wd:Q13143 wdt:P19 wd:Q12744 . ?state1 wdt:P31 wd:Q275432 . ?state2 wdt:P31 ?state3 . FILTER(lang(?state1) = "en" && lang(?state2) = "en" && lang(?state3) = "en") }` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *How many politicians graduated from Columbia University?*
2. *Who is the daughter of Robert Kennedy married to?*
3. *Who is the husband of Amanda Palmer?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q9: What is the boiling point of water?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q283 wdt:P2102 ?result}` |
| **Generated** | `SELECT DISTINCT ?value WHERE { wd:Q1012 wdt:P31 wd:Q11123 ; wdt:P17 ?instance . ?instance wdt:P34 ?value . FILTER(lang(label(?instance, "en") = "Water") && lang(label(?instance, "en") = "liquid")) }` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *How deep is Lake Chiemsee?*
2. *What is the highest mountain?*
3. *What is the longest river in China?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q10: At which school was Yayoi Kusama educated at?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q231121 wdt:P69 ?result}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?school WHERE { wd:Q1531 wdt:P20 ?education . ?education wdt:P431 ?school . FILTER(lang(label(?school, "en")) = "Seattle School of Art" \|\| lang(label(?school, "en")) = "Seattle Art Institute") }` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *Which movies did Kurosawa direct?*
2. *Which university did Angela Merkel attend?*
3. *In which city did Nikos Kazantzakis die?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q11: Which High School did Allen Ginsberg attend?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q6711 wdt:P69 ?result. ?result wdt:P31 wd:Q9826}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?school WHERE { wd:Q5731 wdt:P69 ?school . ?school wdt:P18 ?person . wdt:P31 ?person wds:label "Allen Ginsberg"@en . }` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *How many scientists graduated from an Ivy League university?*
2. *Which university did Angela Merkel attend?*
3. *How many politicians graduated from Columbia University?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ✅ Q12: On which island is the Indonesian capital located?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q252 wdt:P36 ?capital. ?capital wdt:P706 ?result. ?result wdt:P31 wd:Q23442}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?island WHERE { wd:Q17101 wdt:P31 wd:Q31113 . wd:Q31113 wdt:P17 ?island . }` |

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *What is the capital of Cameroon?*
2. *Who is the mayor of the capital of French Polynesia?*
3. *Give me all islands that belong to Japan.*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q13: can i play don't starve on play station 4?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASk {wd:Q3208174 wdt:P400 wd:Q5014725.}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT ?platform WHERE { wd:Q1223 wdt:P1828 ?platform . wdt:P1828 wd:Q31348 . }` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *List all boardgames by GMT.*
2. *List all games by GMT.*
3. *Who wrote The Hunger Games?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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
## ❌ Q14: How many General Secretaries of the CPSU were there before Leonid Brezhnev?

| Type | Query |
|---|---|
| **Gold** | `PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT (COUNT(?gensec) as ?result) WHERE{wd:Q765165 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. ?gensec p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 < ?st)}` |
| **Generated** | `PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT DISTINCT (COUNT(DISTINCT ?uri) AS ?c) WHERE { ?uri wdt:P106 wd:Q1233 ; wdt:P39 wdt:Q1234 ; wdt:P39 wdt:?x . FILTER(?x < wd:Q1235)}` |

> **Error:** `QueryBadFormed: A bad request has been sent to the endpoint: probably the SPARQL query is badly formed. `

<details>
<summary>🔍 Prompt & Retrieval Details (Click to expand)</summary>

**Context Entities:**
```text

```

**Few-Shot Examples Used:**
1. *How many politicians graduated from Columbia University?*
2. *How many emperors did China have?*
3. *Who is the mayor of Berlin?*

**Full Prompt Sent to LLM:**
````text
You are a SPARQL expert for Wikidata. 
Output ONLY the SPARQL query code inside a ```sparql block.

### Relevant Entities & Properties:


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

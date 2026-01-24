# Text-to-SPARQL Evaluation Report

**Model:** `ACE-Qwen_Qwen2.5-Coder-3B-Instruct`
**Timestamp:** 2025-11-29 12:56:47

## Summary Metrics
| Metric | Value |
|---|---|
| Total Questions | 20 |
| Syntax Accuracy | 30.00% |
| Answer Accuracy | 45.00% |
| Average F1 Score | 0.4750 |
| Successful Retries | 2 |

---

## Detailed Results

### Q20: [PASS] Did Rawson Marshall Thurber, the director of Red Notice also direct Titanic?

**Error:** `Error: Execution Error: 'results'`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q2745616 wdt:P57 wd:Q58815001. wd:Q2745616 wdt:P57 wd:Q44578.}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```json
{
  "strategy": "Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using w
- Ensure that the SELECT clause is properly formatted with parentheses around the count expression. ```
- Ensure that the property used for the position is correct for the type of entity being queried. In this case, for presidents of Russia, use wdt:P39 instead of wdt:P57. ```
- Ensure that the property used for filtering dates is consistent across all relevant statements. In this case, use `pq:P580` consistently for both the initial position and the subsequent positions. ```
- Ensure that the correct property is used for medals in the 2020 Summer Olympics. Use wdt:P1344 for medals won by athletes, not wdt:P3450. ```
- For medals in the 2020 Summer Olympics, use wdt:P1344 instead of wdt:P3450. ```
- Ensure that the correct property is used for counting seasons in the NBA championship. Use wdt:P3450 instead of wdt:P1346. ```
- Use wdt:P1346 instead of wdt:P3450 for counting championships won by a team. ```
- For checking if someone received a specific award, use wdt:P1344 instead of wdt:P166. ```
- When comparing properties like P413 (position), ensure that you are using the correct entity IDs for the subjects being compared. In this case, use wd:Q25369 for Kobe Bryant and wd:Q41421 for LeBron James. ```
- Ensure that the properties used in the query match the relationships between the entities being queried. In this case, use wdt:P57 for the relationship between Kobe Bryant and the Lakers, and wdt:P57 for the relationship between LeBron James and the Lakers. Adjust the query accordingly. ```
- For movie directors, use wdt:P57, not wdt:P50. To find the correct query, you should replace wdt:P50 with wdt:P57 in your query. Additionally, ensure that the properties used in your query are appropriate for the type of entity you are querying. In this case, since you are looking for movie directors, you should use wdt:P57 instead of wdt:P50. Here is the corrected query:
- For movie directors, use wdt:P57, not wdt:P50. To determine the correct strategy, let's analyze the user's question and the failed query:

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P57 (director) - director(s) of film, TV-series, stageplay, video game or similar

--- ENTITIES (Items/Objects) ---
wd:Q2745616 (Rawson Marshall Thurber) - American film director
wd:Q44578 (Titanic) - 1997 film by James Cameron
wd:Q58815001 (Red Notice) - 2021 film directed by Rawson Marshall Thurber

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: Tell me all the cast members of the film Red Notice directed by Rawson Marshall Thurber ?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q58815001 wdt:P57 wd:Q2745616; wdt:P161 ?result}
```

Q: When the film Red Notice was released?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q58815001 wdt:P577 ?result}
```

Q: Was Funny Games and its remake directed by different persons?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q696928 wdt:P57 ?dir. wd:Q951002 wdt:P57 ?dir2. FILTER(?dir != ?dir2)}
```

### USER QUESTION:
Did Rawson Marshall Thurber, the director of Red Notice also direct Titanic?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q2745616 wdt:P57 wd:Q58815001. wd:Q2745616 wdt:P57 wd:Q44578.}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 3
---
### Q19: [PASS] Did Kobe Bryant leave the Lakers when LeBron James joined that team?

**Error:** `Error: Execution Error: 'results'`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 wd:Q121783. wd:Q41421 wdt:P54 wd:Q121783. wd:Q25369 wdt:P580 ?st1. wd:Q41421 wdt:P580 ?st2. FILTER(?st1 > ?st2)}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```json
{
  "strategy": "Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using w
- Ensure that the SELECT clause is properly formatted with parentheses around the count expression. ```
- Ensure that the property used for the position is correct for the type of entity being queried. In this case, for presidents of Russia, use wdt:P39 instead of wdt:P57. ```
- Ensure that the property used for filtering dates is consistent across all relevant statements. In this case, use `pq:P580` consistently for both the initial position and the subsequent positions. ```
- Ensure that the correct property is used for medals in the 2020 Summer Olympics. Use wdt:P1344 for medals won by athletes, not wdt:P3450. ```
- For medals in the 2020 Summer Olympics, use wdt:P1344 instead of wdt:P3450. ```
- Ensure that the correct property is used for counting seasons in the NBA championship. Use wdt:P3450 instead of wdt:P1346. ```
- Use wdt:P1346 instead of wdt:P3450 for counting championships won by a team. ```
- For checking if someone received a specific award, use wdt:P1344 instead of wdt:P166. ```
- When comparing properties like P413 (position), ensure that you are using the correct entity IDs for the subjects being compared. In this case, use wd:Q25369 for Kobe Bryant and wd:Q41421 for LeBron James. ```
- Ensure that the properties used in the query match the relationships between the entities being queried. In this case, use wdt:P57 for the relationship between Kobe Bryant and the Lakers, and wdt:P57 for the relationship between LeBron James and the Lakers. Adjust the query accordingly. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P580 (start time) - time an entity begins to exist or a statement starts being valid
wdt:P582 (end time) - moment when an entity ceases to exist and a statement stops being entirely valid or no longer be true
wdt:P54 (member of sports team) - sports teams or clubs that the subject represents or represented

--- ENTITIES (Items/Objects) ---
wd:Q121783 (Los Angeles Lakers) - American professional basketball team
wd:Q25369 (Kobe Bryant) - American basketball player (1978–2020)
wd:Q36159 (LeBron James) - American basketball player (born 1984)

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: Did Michael Jordan and Kobe Bryant play for the same team?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 ?team. wd:Q41421 wdt:P54 ?team.}
```

Q: Was Shaquille O'Neal the teammate of Kobe Bryant in the year of 2000?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 p:P54 ?ps1. ?ps1 ps:P54 ?team; pq:P580 ?st1; pq:P582 ?et1. wd:Q169452 p:P54 ?ps2. ?ps2 ps:P54 ?team; pq:P580 ?st2; pq:P582 ?et2. FILTER(YEAR(?st1) <= 2000 && YEAR(?et1) >= 2000 && YEAR(?st2) <= 2000 && YEAR(?et2) >= 2000)}
```

Q: How many positions did Kobe Bryant play in his team?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?pos) AS ?result) WHERE {wd:Q25369 wdt:P413 ?pos}
```

### USER QUESTION:
Did Kobe Bryant leave the Lakers when LeBron James joined that team?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 wd:Q121783. wd:Q41421 wdt:P54 wd:Q121783. wd:Q25369 wdt:P580 ?st1. wd:Q41421 wdt:P580 ?st2. FILTER(?st1 > ?st2)}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 3
---
### Q18: [PARTIAL] Did Haruki Murakami receive the Nobel Prize in Literature?

**Error:** `Wrong Answer: F1 Score: 0.00 (Results mismatch)`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?result) AS ?resultCnt) WHERE { ?result wdt:P166 wd:Q37922. ?result wdt:P106 wd:Q134798 }
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```json
{
  "strategy": "Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using w
- Ensure that the SELECT clause is properly formatted with parentheses around the count expression. ```
- Ensure that the property used for the position is correct for the type of entity being queried. In this case, for presidents of Russia, use wdt:P39 instead of wdt:P57. ```
- Ensure that the property used for filtering dates is consistent across all relevant statements. In this case, use `pq:P580` consistently for both the initial position and the subsequent positions. ```
- Ensure that the correct property is used for medals in the 2020 Summer Olympics. Use wdt:P1344 for medals won by athletes, not wdt:P3450. ```
- For medals in the 2020 Summer Olympics, use wdt:P1344 instead of wdt:P3450. ```
- Ensure that the correct property is used for counting seasons in the NBA championship. Use wdt:P3450 instead of wdt:P1346. ```
- Use wdt:P1346 instead of wdt:P3450 for counting championships won by a team. ```
- For checking if someone received a specific award, use wdt:P1344 instead of wdt:P166. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P1346 (winner) - winner of a competition or similar event, not to be used for awards (instead use "award received" (P166) on awardee's item, possibly qualified with "for work" (P1686)) or for wars or battles

--- ENTITIES (Items/Objects) ---
wd:Q37922 (Nobel Prize in Literature) - one of five prizes established by Alfred Nobel
wd:Q134798 (Haruki Murakami) - Japanese writer

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: How many Japanese writers received the Nobel Prize?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?writer) AS ?result) WHERE {?writer wdt:P166/wdt:P279 wd:Q7191. ?writer wdt:P27 wd:Q17; wdt:P106 wd:Q36180}
```

Q: How many people have won the Nobel Prize in Literature since its inception?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?people) AS ?result) WHERE {?people wdt:P31 wd:Q5; wdt:P166 wd:Q37922}
```

Q: How many people won the Nobel Prize in Literature or Physics since 2000?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?result) AS ?resultCnt) WHERE{?result wdt:P31 wd:Q5. ?result p:P166 ?ps. {?ps ps:P166 wd:Q37922} UNION {?ps ps:P166 wd:Q38104} ?ps pq:P585 ?time. FILTER(YEAR(?time) > 2000)}
```

### USER QUESTION:
Did Haruki Murakami receive the Nobel Prize in Literature?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?result) AS ?resultCnt) WHERE { ?result wdt:P166 wd:Q37922. ?result wdt:P106 wd:Q134798 }
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q17: [PASS] Did the Chicago Bulls win at least two seasons of the NBA championship?

**Error:** `Error: Execution Error: 'results'`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q128109 wdt:P3450 wd:Q155223; wdt:P1346 ?result. FILTER(?result >= 2)}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{{SELECT (COUNT (?season) AS ?count) WHERE {?season wdt:P3450 wd:Q155223. ?season wdt:P1346 wd:Q128109}} FILTER(?count >= 2)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 0 | `` |

<details>
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```json
{
  "strategy": "Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using w
- Ensure that the SELECT clause is properly formatted with parentheses around the count expression. ```
- Ensure that the property used for the position is correct for the type of entity being queried. In this case, for presidents of Russia, use wdt:P39 instead of wdt:P57. ```
- Ensure that the property used for filtering dates is consistent across all relevant statements. In this case, use `pq:P580` consistently for both the initial position and the subsequent positions. ```
- Ensure that the correct property is used for medals in the 2020 Summer Olympics. Use wdt:P1344 for medals won by athletes, not wdt:P3450. ```
- For medals in the 2020 Summer Olympics, use wdt:P1344 instead of wdt:P3450. ```
- Ensure that the correct property is used for counting seasons in the NBA championship. Use wdt:P3450 instead of wdt:P1346. ```
- Use wdt:P1346 instead of wdt:P3450 for counting championships won by a team. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P1346 (winner) - winner of a competition or similar event, not to be used for awards (instead use "award received" (P166) on awardee's item, possibly qualified with "for work" (P1686)) or for wars or battles
wdt:P3450 (sports season of league or competition) - property that shows the competition of which the item is a season. Use P5138 for "season of club or team".

--- ENTITIES (Items/Objects) ---
wd:Q128109 (Chicago Bulls) - American professional basketball team
wd:Q155223 (National Basketball Association) - North American professional basketball league

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: Which NBA teams have won the most seasons?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {{SELECT DISTINCT (COUNT(DISTINCT ?season) AS ?max) WHERE {?season wdt:P31 wd:Q27020041; wdt:P3450 wd:Q155223; wdt:P1346 ?result. ?result wdt:P31 wd:Q13393265} GROUP BY ?result ORDER BY DESC (?max) LIMIT 1} ?season wdt:P31 wd:Q27020041; wdt:P3450 wd:Q155223; wdt:P1346 ?result. ?result wdt:P31 wd:Q13393265.} GROUP BY ?result HAVING ((COUNT(DISTINCT ?season)) = MAX(?max))
```

Q: Did Michael Jordan and Kobe Bryant play for the same team?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q25369 wdt:P54 ?team. wd:Q41421 wdt:P54 ?team.}
```

Q: How many All-NBA Team awards have Shaquille O'Neal and Kobe Bryant received in the same year?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?time) AS ?result) WHERE {wd:Q25369 p:P166 ?as. ?as ps:P166 wd:Q674359; pq:P585 ?time. wd:Q169452 p:P166 ?as2. ?as2 ps:P166 wd:Q674359; pq:P585 ?time}
```

### USER QUESTION:
Did the Chicago Bulls win at least two seasons of the NBA championship?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q128109 wdt:P3450 wd:Q155223; wdt:P1346 ?result. FILTER(?result >= 2)}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 3
---
### Q16: [PASS] Did adam ondra win a medal in the 2020 summer olympics?

**Error:** `Error: Execution Error: 'results'`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q350568 wdt:P1344 ?medal. ?medal wdt:P3450 wd:Q181278.}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q350568 p:P1344 ?event. ?event ps:P1344 ?eventStatement. ?eventStatement wdt:P361* wd:Q181278. ?event pq:P1352 ?ranking. FILTER(?ranking <= 3)}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 0 | `` |

<details>
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```json
{
  "strategy": "Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using w
- Ensure that the SELECT clause is properly formatted with parentheses around the count expression. ```
- Ensure that the property used for the position is correct for the type of entity being queried. In this case, for presidents of Russia, use wdt:P39 instead of wdt:P57. ```
- Ensure that the property used for filtering dates is consistent across all relevant statements. In this case, use `pq:P580` consistently for both the initial position and the subsequent positions. ```
- Ensure that the correct property is used for medals in the 2020 Summer Olympics. Use wdt:P1344 for medals won by athletes, not wdt:P3450. ```
- For medals in the 2020 Summer Olympics, use wdt:P1344 instead of wdt:P3450. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P361 (part of) - object of which the subject is a part (if this subject is already part of object A which is a part of object B, then please only make the subject part of object A), inverse property of "has part" (P527, see also "has parts of the class" (P2670))
wdt:P1344 (participant in) - event in which a person, organization or creative work was/is a participant; inverse of P710 or P1923
wdt:P1352 (ranking) - subject's ordinal position as qualitatively evaluated relative to other members of a group

--- ENTITIES (Items/Objects) ---
wd:Q350568 (Adam Ondra) - Czech rock climber
wd:Q181278 (2020 Summer Olympics) - games of the XXXII Olympiad, in Tokyo, Japan, held in 2021

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: has adam ondra been a winner of IFSC climbing world cup?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q350568 p:P1344 ?ps. ?ps ps:P1344/wdt:P3450* wd:Q1774251. {?ps pq:P1352 ?rank.} UNION {?ps pq:P166 ?gold.} FILTER(?rank = 1 || sameTerm(?gold,wd:Q406039))}
```

Q: How many Olympic Games has Kobe Bryant taken part in?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?ol) AS ?result) WHERE {wd:Q25369 wdt:P1344 ?ol. ?ol wdt:P31/wdt:P279 wd:Q5389}
```

Q: Did Udo Bölts participate in the Tour de France?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q66432 wdt:P1344/wdt:P31 wd:Q33881}
```

### USER QUESTION:
Did adam ondra win a medal in the 2020 summer olympics?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q350568 wdt:P1344 ?medal. ?medal wdt:P3450 wd:Q181278.}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 3
---
### Q15: [PARTIAL] How many different presidents of Russia have there been that took the position after 1990?

**Error:** `Wrong Answer: F1 Score: 0.00 (Results mismatch)`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE {wd:Q218295 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. FILTER(?st > 1990). ?president p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 > ?st)}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```json
{
  "strategy": "Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using w
- Ensure that the SELECT clause is properly formatted with parentheses around the count expression. ```
- Ensure that the property used for the position is correct for the type of entity being queried. In this case, for presidents of Russia, use wdt:P39 instead of wdt:P57. ```
- Ensure that the property used for filtering dates is consistent across all relevant statements. In this case, use `pq:P580` consistently for both the initial position and the subsequent positions. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P580 (start time) - time an entity begins to exist or a statement starts being valid
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q218295 (President of Russia) - head of state of the RSFSR (office established in 1991) and Russia

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: How many General Secretaries of the CPSU were there before Leonid Brezhnev?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT (COUNT(?gensec) as ?result) WHERE{wd:Q765165 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. ?gensec p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 < ?st)}
```

Q: how many head of the state does iran have?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?hos) AS ?result) WHERE {wd:Q794 p:P35/ps:P35 ?hos.}
```

Q: How many spouses do head of states have on average?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (AVG(?spouseCount) AS ?result) WHERE {{SELECT (COUNT(DISTINCT ?spouse) AS ?spouseCount) WHERE{?country wdt:P31 wd:Q6256. ?country p:P35/ps:P35 ?hos. OPTIONAL {?hos wdt:P26 ?spouse}} GROUP BY ?hos }}
```

### USER QUESTION:
How many different presidents of Russia have there been that took the position after 1990?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE {wd:Q218295 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. FILTER(?st > 1990). ?president p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 > ?st)}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q14: [FAIL] How many General Secretaries of the CPSU were there before Leonid Brezhnev?

**Error:** `Error: Syntax Error: Line 13, Col 3: Expected Expected SelectQuery`

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

SELECT (COUNT(DISTINCT ?secretary) AS ?result) WHERE {
  ?secretary wdt:P39 wd:Q1048744. 
  ?secretary wdt:P580 ?start. 
  FILTER(?start < wdt:P580 wd:Q765165)
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
| **Gen** | 0 | `` |

<details>
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```json
{
  "strategy": "Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using w
- Ensure that the SELECT clause is properly formatted with parentheses around the count expression. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P580 (start time) - time an entity begins to exist or a statement starts being valid
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q765165 (Leonid Brezhnev) - General Secretary of the Communist Party of the Soviet Union (1906–1982)
wd:Q1048744 (General Secretary of the Communist Party of the Soviet Union) - de facto head of state of the Soviet Union and dirigent of the Communist Party of the Soviet Union

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: How many different presidents of Russia have there been that took the position after 1990?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE{?president p:P39 ?pos. ?pos ps:P39 wd:Q218295. ?pos pq:P580 ?start. FILTER((YEAR(?start)> 1990))}
```

Q: how many head of the state does iran have?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?hos) AS ?result) WHERE {wd:Q794 p:P35/ps:P35 ?hos.}
```

Q: How many spouses do head of states have on average?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (AVG(?spouseCount) AS ?result) WHERE {{SELECT (COUNT(DISTINCT ?spouse) AS ?spouseCount) WHERE{?country wdt:P31 wd:Q6256. ?country p:P35/ps:P35 ?hos. OPTIONAL {?hos wdt:P26 ?spouse}} GROUP BY ?hos }}
```

### USER QUESTION:
How many General Secretaries of the CPSU were there before Leonid Brezhnev?

### SOLUTION:
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

SELECT (COUNT(DISTINCT ?secretary) AS ?result) WHERE {
  ?secretary wdt:P39 wd:Q1048744. 
  ?secretary wdt:P580 ?start. 
  FILTER(?start < wdt:P580 wd:Q765165)
}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q13: [PASS] can i play don't starve on play station 4?

**Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
SELECT ?game ?platform WHERE {
  ?game wdt:P178 wd:Q5014725 .
  ?game wdt:P31 wd:Q7889 .
  ?platform wdt:P178 wd:Q5014725 .
  ?platform wdt:P31 wd:Q3208174 .
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASk {wd:Q3208174 wdt:P400 wd:Q5014725.}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 0 | `` |
| **Gen** | 0 | `` |

<details>
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```
- Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using wdt:P1344. Adjust the query accordingly. ```json
{
  "strategy": "Ensure that the properties used in the query match the data types of the entities being queried. In this case, use wdt:P178 for games and wdt:P31 for categories. Also, ensure that the platform entity is correctly identified using w

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P400 (platform) - platform for which a work was developed or released, or the specific platform version of a software product

--- ENTITIES (Items/Objects) ---
wd:Q5014725 (PlayStation 4) - Sony's fourth home video game console, part of the eighth generation of consoles
wd:Q3208174 (Don't Starve) - 2013 video game developed by Klei Entertainment

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: What is the second game developed by Piranha Bytes?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{?result wdt:P178 wd:Q677273; wdt:P577 ?date} ORDER BY ASC(?date) OFFSET 1 LIMIT 1
```

Q: How many other video games began the same year as Dead by Daylight?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?game) AS ?result) WHERE {?game wdt:P31/wdt:P279* wd:Q7889; wdt:P577 ?gameTime. wd:Q24514682 wdt:P577 ?dbdtime. FILTER((YEAR(?gameTime) = YEAR(?dbdtime)))}
```

Q: How many people can play "Mensch ärgere dich nicht" at most?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q545129 wdt:P1873 ?result}
```

### USER QUESTION:
can i play don't starve on play station 4?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
SELECT ?game ?platform WHERE {
  ?game wdt:P178 wd:Q5014725 .
  ?game wdt:P31 wd:Q7889 .
  ?platform wdt:P178 wd:Q5014725 .
  ?platform wdt:P31 wd:Q3208174 .
}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 3
---
### Q12: [FAIL] On which island is the Indonesian capital located?

**Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT ?island WHERE {
  wd:Q252 wdt:P36 wd:Q130736 .
  wd:Q130736 wdt:P17 ?island .
  ?island wdt:P31 wd:Q23442 .
}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```
- For questions about locations, use wdt:P625 instead of wdt:P17. ```
- For questions about locations, use wdt:P31 instead of wdt:P17. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P706 (located in/on physical feature) - located on the specified (geo)physical feature. Should not be used when the value is only political/administrative (P131) or a mountain range (P4552). Use P206 for things in/on bodies of water.
wdt:P36 (capital) - seat of government of a country, province, state or other type of administrative territorial entity
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain

--- ENTITIES (Items/Objects) ---
wd:Q23442 (island) - piece of sub-continental land completely surrounded by water
wd:Q252 (Indonesia) - island country in Southeast Asia and Oceania

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: In which country is the Nanga Parbat located?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q130736 wdt:P17 ?result. }
```

Q: Who is the founder of the capital of Vietnam?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q881 wdt:P36/wdt:P112 ?result}
```

Q: What is the area of the capital of Spitsbergen?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q25231 wdt:P36/wdt:P2046 ?result}
```

### USER QUESTION:
On which island is the Indonesian capital located?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT ?island WHERE {
  wd:Q252 wdt:P36 wd:Q130736 .
  wd:Q130736 wdt:P17 ?island .
  ?island wdt:P31 wd:Q23442 .
}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q11: [PARTIAL] Which High School did Allen Ginsberg attend?

**Error:** `Wrong Answer: F1 Score: 0.50 (Results mismatch)`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q6711 wdt:P69 ?result}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P69 (educated at) - educational institution attended by subject
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain

--- ENTITIES (Items/Objects) ---
wd:Q6711 (Allen Ginsberg) - American poet and writer (1926–1997)
wd:Q9826 (high school) - institution which provides final part of secondary education

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: When did Allen Ginsberg die?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q6711 wdt:P570 ?result}
```

Q: Who was the partner of Allen Ginsberg?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q6711 wdt:P451 ?result}
```

Q: How many poems did Allen Ginsberg published?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?poem) AS ?result) WHERE {?poem wdt:P31 wd:Q7725634; wdt:P50 wd:Q6711; wdt:P136/wdt:P279* wd:Q482}
```

### USER QUESTION:
Which High School did Allen Ginsberg attend?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q6711 wdt:P69 ?result}
```
</details>

**F1 Score:** 0.50 | **Attempts:** 1
---
### Q10: [PASS] At which school was Yayoi Kusama educated at?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
SELECT ?school WHERE {
  wd:Q231121 wdt:P69 ?school .
}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P69 (educated at) - educational institution attended by subject

--- ENTITIES (Items/Objects) ---
wd:Q231121 (Yayoi Kusama) - Japanese painter, performance, and installation artist (born 1929)

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: When was Rumi born?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q43347 wdt:P569 ?result}
```

Q: How many movies were directed by Akira Kurosawa ?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?film) AS ?result) WHERE {?film wdt:P31 wd:Q11424; wdt:P57 wd:Q8006}
```

Q: Which High School did Allen Ginsberg attend?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q6711 wdt:P69 ?result. ?result wdt:P31 wd:Q9826}
```

### USER QUESTION:
At which school was Yayoi Kusama educated at?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
SELECT ?school WHERE {
  wd:Q231121 wdt:P69 ?school .
}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 1
---
### Q9: [FAIL] What is the boiling point of water?

**Error:** `Error: Syntax Error: Line 3, Col 3: Expected Expected SelectQuery`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
SELECT ?boilingPoint ?pressure WHERE {
  wd:Q283 wdt:P2102 ?boilingPoint .
  OPTIONAL { wd:Q283 wdt:P2102 ?boilingPoint pq:P103 ?pressure }
}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```
- Ensure that the property used in the query matches the type of information being queried. In this case, use wdt:P2102 for boiling point instead of wdt:P50. ```python
# This is a placeholder for the Python code that would be generated based on the rule.
# The actual implementation would depend on the specific requirements and constraints of the task.
```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P2102 (boiling point) - temperature at which a substance changes its phase from liquid to gas (indicate the corresponding pressure as qualifier)

--- ENTITIES (Items/Objects) ---
wd:Q283 (water) - chemical compound whose molecules are formed by two hydrogen atoms and one oxygen atom

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: How many different colors can water take?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?color) AS ?result) WHERE {wd:Q283 wdt:P462 ?color}
```

Q: Is water colorless?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q283 wdt:P462 wd:Q11567495}
```

Q: What is the highest point of Norway?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q20 wdt:P610 ?result}
```

### USER QUESTION:
What is the boiling point of water?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
SELECT ?boilingPoint ?pressure WHERE {
  wd:Q283 wdt:P2102 ?boilingPoint .
  OPTIONAL { wd:Q283 wdt:P2102 ?boilingPoint pq:P103 ?pressure }
}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q8: [PASS] are brooke raboutou and colin duffy from same state of the usa?

**Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?state WHERE {wd:Q2926117 wdt:P131 ?state. wd:Q87192979 wdt:P131 ?state.}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P19 for birth place instead of wdt:P50 for director. ```
- Ensure that the properties used in the query match the data types and relationships expected for the entities being queried. In this case, use wdt:P131 for states instead of wdt:P50 for directors. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P19 (place of birth) - most specific known birth location of a person, animal or fictional character
wdt:P131 (located in the administrative territorial entity) - the item is located on the territory of the following administrative entity. Use P276 for specifying locations that are non-administrative places and for items about events. Use P1382 if the item falls only partially into the administrative entity.
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain

--- ENTITIES (Items/Objects) ---
wd:Q2926117 (Brooke Raboutou) - American sport climber
wd:Q87192979 (Colin Duffy) - Sport climber from the United States
wd:Q35657 (U.S. state) - constituent political entity of the United States of America

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: Were Angela Merkel and Tony Blair born in the same year?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q567 wdt:P569 ?da. wd:Q9545 wdt:P569 ?dt. FILTER(YEAR(?dt) = YEAR(?da))}
```

Q: Is Axel Rose a member of Guns N' Roses?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q11885 wdt:P463 wd:Q11895}
```

Q: which state inside USA is batman living in?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q2695156 wdt:P551/wdt:P131 ?result. ?result wdt:P31 wd:Q35657}
```

### USER QUESTION:
are brooke raboutou and colin duffy from same state of the usa?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?state WHERE {wd:Q2926117 wdt:P131 ?state. wd:Q87192979 wdt:P131 ?state.}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 3
---
### Q7: [FAIL] Apart from the book series the witcher, name all of the author’s notable work.

**Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
SELECT DISTINCT ?work WHERE {
  wd:Q11835640 wdt:P800 ?work
}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```
- For book series, use wdt:P800, not wdt:P50. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P50 (author) - main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
wdt:P800 (notable work) - notable scientific, artistic or literary work, or other work of significance among subject's works

--- ENTITIES (Items/Objects) ---
wd:Q11835640 (The Witcher) - series of fantasy novels and short stories by Polish writer Andrzej Sapkowski

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    
### FEW-SHOT EXAMPLES (Reference Only):
Q: How many literary works besides The Picture of Dorian Gray did its author write?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT (DISTINCT ?novel) AS ?result) WHERE {wd:Q82464 wdt:P50 ?aut. ?novel wdt:P31 wd:Q7725634; wdt:P50 ?aut FILTER(?novel != wd:Q82464)}
```

Q: How many literary works did Richard Bachman write?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?book) AS ?result) WHERE {?book wdt:P50 wd:Q39829; wdt:P31 wd:Q7725634}
```

Q: How many notable works does Sarah J. Maas have?
A: ```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?notableW) AS ?result) WHERE {wd:Q20640708 wdt:P800 ?notableW}
```

### USER QUESTION:
Apart from the book series the witcher, name all of the author’s notable work.

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
SELECT DISTINCT ?work WHERE {
  wd:Q11835640 wdt:P800 ?work
}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q6: [PASS] On which stock exchanges are Siemens AG shares traded?

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
SELECT DISTINCT ?exchange WHERE {
  wd:Q81230 wdt:P414 ?exchange .
}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P414 (stock exchange) - exchange on which this company is traded

--- ENTITIES (Items/Objects) ---
wd:Q81230 (Siemens) - German multinational conglomerate company

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
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

### USER QUESTION:
On which stock exchanges are Siemens AG shares traded?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
SELECT DISTINCT ?exchange WHERE {
  wd:Q81230 wdt:P414 ?exchange .
}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 1
---
### Q5: [FAIL] among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

**Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?work WHERE {wd:Q696071 wdt:P921 ?work. ?work wdt:P50 wd:Q16003532}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```
- Ensure that the property used for the author's works is appropriate for the type of work being queried. For middle school students, use wdt:P1477 instead of wdt:P50. ```
- Ensure that the property used for the author's work is appropriate for the type of work being described. For middle school students, use wdt:P921 instead of wdt:P451. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P921 (main subject) - primary topic of a work or act of communication
wdt:P50 (author) - main creator(s) of a written work (use on works, not humans); use P2093 (author name string) when Wikidata item is unknown or does not exist
wdt:P800 (notable work) - notable scientific, artistic or literary work, or other work of significance among subject's works

--- ENTITIES (Items/Objects) ---
wd:Q696071 (Hunter × Hunter) - Japanese manga series
wd:Q16003532 (middle school student) - student in late primary or early secondary education
wd:Q69071 (Münchenbuchsee) - municipality in the canton of Bern in Switzerland

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
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

### USER QUESTION:
among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?work WHERE {wd:Q696071 wdt:P921 ?work. ?work wdt:P50 wd:Q16003532}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q4: [FAIL] among the founders of tencent company, who has been member of national people’s congress?

**Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?founder. ?founder wdt:P106 wd:Q10891456}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?result. ?result wdt:P39 wd:Q10891456.}
```

#### 2. Execution Data (Real-world results)
| Source | Count | Data Preview |
|---|---|---|
| **Gold** | 1 | `(Q1739008)` |
| **Gen** | 0 | `` |

<details>
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```
- When querying for members of the National People's Congress, use wdt:P106 instead of wdt:P39. ```
- Ensure that the property used for nationality is correct for the entity type being queried. For individuals, use wdt:P27 for nationality. For organizations, use wdt:P106 for nationality. Adjust the query accordingly. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P112 (founded by) - founder or co-founder of this organization, religion, place or entity
wdt:P39 (position held) - subject currently or formerly holds the object position or public office

--- ENTITIES (Items/Objects) ---
wd:Q10891456 (National People's Congress deputy) - member of Chinese National People's Congress
wd:Q860580 (Tencent) - Chinese multinational investment holding conglomerate

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
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

### USER QUESTION:
among the founders of tencent company, who has been member of national people’s congress?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?founder. ?founder wdt:P106 wd:Q10891456}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q3: [FAIL] among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

**Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
SELECT ?character ?partner1 ?partner2
WHERE {
  ?character wdt:P674 wd:Q11835640 .
  ?character wdt:P451 ?partner1 .
  ?character wdt:P451 ?partner2 .
  FILTER (?partner1 != ?partner2)
}
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```
- Ensure that the properties used for partners are consistent and correctly identified for the specific entity type being queried. In this case, for characters in the Witcher, use wdt:P451 for partners instead of wdt:P674. Adjust the query accordingly. ```
- Ensure that the property used for partners is correct for the entity type being queried. For characters, use wdt:P451 instead of wdt:P674. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P451 (unmarried partner) - someone with whom the person is in a relationship without being married. Use "spouse" (P26) for married couples
wdt:P674 (characters) - characters which appear in this item (like plays, operas, operettas, books, comics, films, TV series, video games)

--- ENTITIES (Items/Objects) ---
wd:Q4463198 (Triss Merigold) - fictional sorceress from the Witcher series
wd:Q4205826 (Yennefer of Vengerberg) - fictional sorceress from the Witcher series
wd:Q11835640 (The Witcher) - series of fantasy novels and short stories by Polish writer Andrzej Sapkowski

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
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

### USER QUESTION:
among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
SELECT ?character ?partner1 ?partner2
WHERE {
  ?character wdt:P674 wd:Q11835640 .
  ?character wdt:P451 ?partner1 .
  ?character wdt:P451 ?partner2 .
  FILTER (?partner1 != ?partner2)
}
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
---
### Q2: [FAIL] Which animal participated in a military operation with the Australian Defence Force?

**Error:** `Error: Query returned 0 results (Logic mismatch or ID error).`

#### 1. SPARQL Query Comparison
**Generated:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?animal WHERE { wd:Q645883 wdt:P1344 wd:Q408 . wd:Q645883 wdt:P1344 ?operation . ?operation wdt:P131 ?animal . }
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    - Use wdt:P1344 instead of wdt:P134.

- Use wdt:P1340 instead of wdt:P1344 for the military operation.

- Use wdt:P131 to find the instance of an animal.
- Use wdt:P1344 instead of wdt:P1340 for the military operation.

- Use wdt:P26 to get the partners of a character in the Witcher series.
- For characters in the Witcher series, use wdt:P674, not wdt:P161.

- For military operations, use wdt:P1344 instead of wdt:P1344.
- For military operations involving the Australian Defence Force, use wdt:P1344 instead of wdt:P131. ```

    ### STANDARD PREFIXES:
    PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P710 (participant) - person, group of people or organization (object) that actively takes/took part in an event or process (subject). Preferably qualify with "object has role" (P3831). Use P1923 for participants that are teams.
wdt:P31 (instance of) - type to which this subject corresponds/belongs. Different from P279 (subclass of); for example: K2 is an instance of mountain; volcano is a subclass of mountain

--- ENTITIES (Items/Objects) ---
wd:Q645883 (military operation) - coordinated military actions of a state or a non-state actor
wd:Q625657 (Australian Defence Force) - combined military forces of Australia
wd:Q16521 (taxon) - group of one or more organism(s), which a taxonomist adjudges to be a unit

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
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

### USER QUESTION:
Which animal participated in a military operation with the Australian Defence Force?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?animal WHERE { wd:Q645883 wdt:P1344 wd:Q408 . wd:Q645883 wdt:P1344 ?operation . ?operation wdt:P131 ?animal . }
```
</details>

**F1 Score:** 0.00 | **Attempts:** 3
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
<summary><b>🔎 View Full Prompt, Raw Response & Full Data</b></summary>

**Full Prompt Sent to Model:**
```text
You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

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

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    --- PROPERTIES (Relations) ---
wdt:P138 (named after) - entity or event that inspired the subject's name, or namesake (in at least one language). Qualifier "applies to name" (P5168) can be used to indicate which one

--- ENTITIES (Items/Objects) ---
wd:Q761383 (Riemannian geometry) - branch of differential geometry dealing with (generalized) Riemannian manifolds

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
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

### USER QUESTION:
After whom is the Riemannian geometry named?

### SOLUTION:
```sparql
```

**Raw Model Response (Uncleaned):**
```text
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q761383 wdt:P138 ?result}
```
</details>

**F1 Score:** 1.00 | **Attempts:** 1
---

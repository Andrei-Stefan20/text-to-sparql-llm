# Text-to-SPARQL Report (Gemini)

**Model:** `gemini_models_gemini-2.0-flash`

| Total | Syntax Acc | Answer Acc | Avg F1 |
|---|---|---|---|
| 20 | 60.00% | 40.00% | 0.4000 |

### Q20: [FAIL] Did Rawson Marshall Thurber, the director of Red Notice also direct Titanic?

**Error:** `Empty Output: Il modello non ha generato nulla.`

**Gen:**
```sparql

```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q58815001 wdt:P57 ?director. wd:Q44578 wdt:P57 ?director. FILTER(wd:Q2745616 = ?director)}
```
---
### Q19: [FAIL] Did Kobe Bryant leave the Lakers when LeBron James joined that team?

**Error:** `Execution Error: 'results'`

**Gen:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>

ASK {
  wd:Q25369 p:P54 ?kobe_team_membership .
  ?kobe_team_membership ps:P54 wd:Q121783 .
  OPTIONAL { ?kobe_team_membership pq:P582 ?kobe_end_time . }

  wd:Q36159 p:P54 ?lebron_team_membership .
  ?lebron_team_membership ps:P54 wd:Q121783 .
  ?lebron_team_membership pq:P580 ?lebron_start_time .

  FILTER (BOUND(?kobe_end_time) && ?kobe_end_time <= ?lebron_start_time)
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q25369 p:P54 ?teamStatement. ?teamStatement ps:P54 wd:Q121783; pq:P582 ?leave. wd:Q36159 p:P54 ?teamStatement2. ?teamStatement2 ps:P54 wd:Q121783; pq:P580 ?join. FILTER(?leave = ?join)}
```
---
### Q18: [FAIL] Did Haruki Murakami receive the Nobel Prize in Literature?

**Error:** `Execution Error: 'results'`

**Gen:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

ASK {
  wd:Q134798 wdt:P166 wd:Q37922.
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q37922 wdt:P1346 wd:Q134798}
```
---
### Q17: [FAIL] Did the Chicago Bulls win at least two seasons of the NBA championship?

**Error:** `Execution Error: 'results'`

**Gen:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

ASK {
  {
    SELECT (COUNT(DISTINCT ?season) AS ?count)
    WHERE {
      ?season wdt:P1346 wd:Q128109.
      ?season wdt:P3450 wd:Q155223.
    }
  }
  FILTER (?count >= 2)
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{{SELECT (COUNT (?season) AS ?count) WHERE {?season wdt:P3450 wd:Q155223. ?season wdt:P1346 wd:Q128109}} FILTER(?count >= 2)}
```
---
### Q16: [FAIL] Did adam ondra win a medal in the 2020 summer olympics?

**Error:** `Execution Error: 'results'`

**Gen:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
ASK {
  wd:Q350568 wdt:P1344 ?event .
  ?event wdt:P361* wd:Q181278 .
  ?event wdt:P1344 wd:Q350568 .
  {?event p:P1352 ?rankStatement .
   ?rankStatement ps:P1352 ?rank .
   FILTER (?rank <= 3)} UNION {?event p:P166 ?medal .}
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK{wd:Q350568 p:P1344 ?event. ?event ps:P1344 ?eventStatement. ?eventStatement wdt:P361* wd:Q181278. ?event pq:P1352 ?ranking. FILTER(?ranking <= 3)}
```
---
### Q15: [FAIL] How many different presidents of Russia have there been that took the position after 1990?

**Error:** `Empty Output: Il modello non ha generato nulla.`

**Gen:**
```sparql

```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?president) AS ?result) WHERE{?president p:P39 ?pos. ?pos ps:P39 wd:Q218295. ?pos pq:P580 ?start. FILTER((YEAR(?start)> 1990))}
```
---
### Q14: [FAIL] How many General Secretaries of the CPSU were there before Leonid Brezhnev?

**Error:** `Empty Output: Il modello non ha generato nulla.`

**Gen:**
```sparql

```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT (COUNT(?gensec) as ?result) WHERE{wd:Q765165 p:P39 ?pos. ?pos ps:P39 wd:Q1048744; pq:P580 ?st. ?gensec p:P39 ?pos2. ?pos2 ps:P39 wd:Q1048744; pq:P580 ?st2. FILTER(?st2 < ?st)}
```
---
### Q13: [FAIL] can i play don't starve on play station 4?

**Error:** `Wrong Answer: F1 Score: 0.00`

**Gen:**
```sparql
SELECT (COUNT(*) as ?result) WHERE {
  wd:Q3208174 wdt:P400 wd:Q5014725.
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASk {wd:Q3208174 wdt:P400 wd:Q5014725.}
```
---
### Q12: [PASS] On which island is the Indonesian capital located?

**Gen:**
```sparql
SELECT DISTINCT ?result WHERE {
  wd:Q252 wdt:P36/wdt:P706 ?result.
  ?result wdt:P31 wd:Q23442.
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q252 wdt:P36 ?capital. ?capital wdt:P706 ?result. ?result wdt:P31 wd:Q23442}
```
---
### Q11: [PASS] Which High School did Allen Ginsberg attend?

**Gen:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?result WHERE {
  wd:Q6711 wdt:P69 ?result .
  ?result wdt:P31 wd:Q9826 .
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q6711 wdt:P69 ?result. ?result wdt:P31 wd:Q9826}
```
---
### Q10: [PASS] At which school was Yayoi Kusama educated at?

**Gen:**
```sparql
SELECT DISTINCT ?result WHERE { wd:Q231121 wdt:P69 ?result. }
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result {wd:Q231121 wdt:P69 ?result}
```
---
### Q9: [PASS] What is the boiling point of water?

**Gen:**
```sparql
SELECT ?boilingPoint WHERE { wd:Q283 wdt:P2102 ?boilingPoint. }
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE{wd:Q283 wdt:P2102 ?result}
```
---
### Q8: [FAIL] are brooke raboutou and colin duffy from same state of the usa?

**Error:** `Execution Error: 'results'`

**Gen:**
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

ASK {
  wd:Q2926117 wdt:P19 ?place1 .
  ?place1 wdt:P131 ?state1 .
  wd:Q87192979 wdt:P19 ?place2 .
  ?place2 wdt:P131 ?state2 .
  FILTER (?state1 = ?state2)
  ?state1 wdt:P31 wd:Q35657
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ASK {wd:Q2926117 wdt:P19 ?b1. wd:Q87192979 wdt:P19 ?b2. ?b1 wdt:P131* ?state. ?b2 wdt:P131* ?state. ?state wdt:P31 wd:Q35657 .}
```
---
### Q7: [FAIL] Apart from the book series the witcher, name all of the author’s notable work.

**Error:** `Wrong Answer: F1 Score: 0.00`

**Gen:**
```sparql
SELECT DISTINCT ?work WHERE {
  ?author wdt:P800 ?work.
  ?work wdt:P50 ?author.
  FILTER (?work != wd:Q11835640)
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P50 ?author. ?author wdt:P800 ?result. FILTER(?result != wd:Q11835640)}
```
---
### Q6: [FAIL] On which stock exchanges are Siemens AG shares traded?

**Error:** `Wrong Answer: F1 Score: 0.00`

**Gen:**
```sparql
SELECT ?item ?itemLabel WHERE {
  wd:Q81230 wdt:P414 ?item.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q81230 wdt:P414 ?result}
```
---
### Q5: [PASS] among the other representative work of the author of hunter x hunter, which one is talking about middle school student?

**Gen:**
```sparql
SELECT DISTINCT ?other_work WHERE {
  wd:Q696071 wdt:P50 ?author .
  ?other_work wdt:P50 ?author .
  ?other_work wdt:P921 wd:Q16003532 .
  FILTER (?other_work != wd:Q696071)
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q696071 wdt:P50 ?author. ?author wdt:P800 ?result. ?result wdt:P921 wd:Q16003532 FILTER(?result != wd:Q69071)}
```
---
### Q4: [PASS] among the founders of tencent company, who has been member of national people’s congress?

**Gen:**
```sparql
SELECT DISTINCT ?person WHERE {
  wd:Q860580 wdt:P112 ?person.
  ?person wdt:P39 wd:Q10891456.
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q860580 wdt:P112 ?result. ?result wdt:P39 wd:Q10891456.}
```
---
### Q3: [FAIL] among the characters in the witcher, who has two unmarried partners, Yennefer of Vengerberg and Triss Merigold?

**Gen:**
```sparql
SELECT ?character WHERE {
  ?character wdt:P674 wd:Q11835640 .
  ?character wdt:P451 wd:Q4205826 .
  ?character wdt:P451 wd:Q4463198 .
  FILTER NOT EXISTS {
    ?character wdt:P451 ?otherPartner .
    FILTER (?otherPartner != wd:Q4205826 && ?otherPartner != wd:Q4463198)
  }
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {wd:Q11835640 wdt:P674 ?result. ?result wdt:P451 ?p1, ?p2. FILTER(?p1 != ?p2 &&(?result IN (wd:Q4205826, wd:Q4463198)))}
```
---
### Q2: [PASS] Which animal participated in a military operation with the Australian Defence Force?

**Gen:**
```sparql
SELECT DISTINCT ?animal WHERE {
  ?military_operation wdt:P31 wd:Q645883.
  ?military_operation wdt:P710 wd:Q625657.
  ?military_operation wdt:P710 ?animal.
  ?animal wdt:P31 wd:Q16521.
}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE {?result wdt:P31 wd:Q16521. ?mop wdt:P31 wd:Q645883; wdt:P710 ?result, wd:Q625657.}
```
---
### Q1: [PASS] After whom is the Riemannian geometry named?

**Gen:**
```sparql
SELECT DISTINCT ?result WHERE {wd:Q761383 wdt:P138 ?result}
```
**Gold:**
```sparql
PREFIX bd: <http://www.bigdata.com/rdf#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> PREFIX p: <http://www.wikidata.org/prop/> PREFIX pq: <http://www.wikidata.org/prop/qualifier/> PREFIX ps: <http://www.wikidata.org/prop/statement/> PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wds: <http://www.wikidata.org/entity/statement/> PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wdv: <http://www.wikidata.org/value/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?result WHERE { wd:Q761383 wdt:P138 ?result. }
```
---

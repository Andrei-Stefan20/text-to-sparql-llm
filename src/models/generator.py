STANDARD_PREFIXES = """PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>"""

def build_prompt(user_question, similar_examples, candidate_entities):
    """
    Costruisce il prompt per il LLM includendo esempi few-shot e il contesto dello schema.
    """
    prompt = f"""You are an expert SPARQL developer for Wikidata.
    Your task is to translate a natural language question into a valid SPARQL query.

    ### Guidelines:
    1. Use the provided Schema/Entities.
    2. Use ONLY these standard prefixes (do not define your own):
    {STANDARD_PREFIXES}
    3. Do NOT explain the query, output ONLY the code.
    4. Output the SPARQL query inside a ```sparql``` code block.
    """

    prompt += "\n### Few-Shot Examples:\n"
    for ex in similar_examples:
        sparql_code = ex.get('sparql', ex.get('query', ''))
        sparql_code = sparql_code.strip()
        prompt += f"User: {ex['question']}\nQuery:\n```sparql\n{sparql_code}\n```\n\n"

    prompt += f"### Context (Schema):\n{candidate_entities}\n\n"
    prompt += f"### User Question:\n{user_question}\n\n"
    
    prompt += "```sparql" 
    
    return prompt
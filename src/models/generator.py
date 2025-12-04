
STANDARD_PREFIXES = """PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>"""

STANDARD_PREFIXES_ACE = """PREFIX wd: [http://www.wikidata.org/entity/](http://www.wikidata.org/entity/)
PREFIX wdt: [http://www.wikidata.org/prop/direct/](http://www.wikidata.org/prop/direct/)
PREFIX wikibase: [http://wikiba.se/ontology#](http://wikiba.se/ontology#)
PREFIX p: [http://www.wikidata.org/prop/](http://www.wikidata.org/prop/)
PREFIX ps: [http://www.wikidata.org/prop/statement/](http://www.wikidata.org/prop/statement/)
PREFIX pq: [http://www.wikidata.org/prop/qualifier/](http://www.wikidata.org/prop/qualifier/)
PREFIX rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)
PREFIX bd: [http://www.bigdata.com/rdf#](http://www.bigdata.com/rdf#)"""

def build_prompt(user_question: str, similar_examples: list, candidate_entities: str) -> str:
    """
    Constructs a few-shot learning prompt for SPARQL generation.
    
    Args:
        user_question: Natural language query to translate
        similar_examples: Retrieved examples containing question-SPARQL pairs
        candidate_entities: Formatted schema context with entity/property IDs
        
    Returns:
        Formatted prompt string ready for LLM inference
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

def build_ace_prompt(user_question: str, similar_examples: list, candidate_entities: str, playbook_context: str) -> str:
    """
    Constructs an ACE-enhanced prompt with learned strategies.
    
    Args:
        user_question: Natural language query to translate
        similar_examples: Retrieved examples containing question-SPARQL pairs
        candidate_entities: Formatted schema context with entity/property IDs
        playbook_context: Formatted string of learned corrective strategies
        
    Returns:
        ACE-enhanced prompt with strategic guidelines
    """
    prompt = f"""You are an expert SPARQL developer for Wikidata.
    Translate the user question into a valid SPARQL query.

    ### ACE PLAYBOOK (STRATEGIC GUIDELINES):
    The following strategies have been learned from previous errors. FOLLOW THEM STRICTLY:
    {playbook_context}

    ### STANDARD PREFIXES:
    {STANDARD_PREFIXES_ACE}

    ### SCHEMA CONTEXT (REQUIRED MAPPING):
    Use ONLY the IDs listed below for the corresponding concepts.
    - Use 'wdt:P...' for properties/predicates.
    - Use 'wd:Q...' for entities/items.
    
    {candidate_entities}

    ### INSTRUCTIONS:
    1. Analyze the Question and map terms to the IDs in the SCHEMA CONTEXT.
    2. Apply the strategies from the Playbook.
    3. Output ONLY the SPARQL query inside a ```sparql``` block.
    """

    prompt += "\n### FEW-SHOT EXAMPLES (Reference Only):\n"
    for ex in similar_examples:
        sparql_code = ex.get('sparql', ex.get('query', '')).strip()
        prompt += f"Q: {ex['question']}\nA: ```sparql\n{sparql_code}\n```\n\n"

    prompt += f"### USER QUESTION:\n{user_question}\n\n"
    prompt += "### SOLUTION:\n```sparql"
    
    return prompt
def build_prompt(user_question, similar_examples, candidate_entities):

    prompt = """You are a SPARQL expert for Wikidata.
        Your task is to translate a natural language question into a valid SPARQL query.
        Use the provided schema elements and examples.

        """
    
    # 1. Aggiungi esempi simili (Dynamic Few-Shot)
    prompt += "### Examples:\n"
    for ex in similar_examples:
        prompt += f"Question: {ex['question']}\nSPARQL: {ex['query']}\n\n"

    # 2. Iniezione Entità 
    prompt += f"### Context (Candidate Entities/Relations):\n{candidate_entities}\n\n"

    # 3. Domanda Target
    prompt += f"### Task:\nQuestion: {user_question}\nSPARQL:"
    
    return prompt
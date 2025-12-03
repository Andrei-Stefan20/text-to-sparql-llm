class StepExecutor:
    def __init__(self, generator_model, retriever_tool):
        self.generator = generator_model
        self.retriever = retriever_tool 

    def execute_step(self, current_step, context_history):
        """
        Executes a single step taking into account what was discovered previously.
        """
        
        # Build a prompt that includes the accumulated context 
        prompt_context = "\n".join([f"Result of previous steps: {k}: {v}" for k, v in context_history.items()])
        
        full_prompt = f"""
        Accumulated Context:
        {prompt_context}
        
        Current Task: {current_step}
        
        Generate the SPARQL query (or perform the action) necessary EXCLUSIVELY for this specific task.
        Use entity IDs found in the context if necessary.
        """
        
    
        # 1. SPARQL Generation
        sparql_query = self.generator.generate(full_prompt)
        
        # 2. Execution (Simulating KG call)
        results = self.retriever.run_sparql(sparql_query)
        
        return results
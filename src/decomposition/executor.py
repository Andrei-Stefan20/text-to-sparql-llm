class StepExecutor:
    """Executes individual decomposition steps with contextual awareness."""
    
    def __init__(self, generator_model, retriever_tool):
        self.generator = generator_model
        self.retriever = retriever_tool

    def execute_step(self, current_step, context_history):
        """
        Executes a decomposition step using accumulated context from previous steps.
        
        Args:
            current_step: Current task description to execute
            context_history: Dictionary of results from previous steps
            
        Returns:
            Query execution results from the knowledge graph
        """
        prompt_context = "\n".join([f"Result of previous steps: {k}: {v}" for k, v in context_history.items()])
        
        full_prompt = f"""
        Accumulated Context:
        {prompt_context}
        
        Current Task: {current_step}
        
        Generate the SPARQL query (or perform the action) necessary EXCLUSIVELY for this specific task.
        Use entity IDs found in the context if necessary.
        """
        
        sparql_query = self.generator.generate(full_prompt)
        results = self.retriever.run_sparql(sparql_query)
        
        return results
from .planner import QueryDecomposer
from .executor import StepExecutor

class DecompositionOrchestrator:
    """Coordinates query decomposition and sequential execution of sub-tasks."""
    
    def __init__(self, llm, generator, retriever):
        self.planner = QueryDecomposer(llm)
        self.executor = StepExecutor(generator, retriever)
        
    def run(self, user_question):
        """
        Orchestrates the complete decomposition pipeline.
        
        Args:
            user_question: Natural language query to process
            
        Returns:
            Final synthesized answer from all execution steps
        """
        print(f"Analyzing question: {user_question}")
        plan = self.planner.create_plan(user_question)
        print(f"Generated plan: {plan}")
        
        context = {}
        
        for i, step in enumerate(plan):
            print(f"--- Executing Step {i+1}: {step} ---")
            
            try:
                result = self.executor.execute_step(step, context)
                
                if not result:
                    print("No result. Attempting reformulation or relaxing constraints...")
                    continue
                
                context[f"step_{i+1}"] = result
                
            except Exception as e:
                print(f"Error in step {i+1}: {e}")
                break
        
        return self._synthesize_answer(user_question, context)

    def _synthesize_answer(self, question, context):
        """Combines execution results into a final answer."""
        return "Final answer based on..." 
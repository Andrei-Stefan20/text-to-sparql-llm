from .planner import QueryDecomposer
from .executor import StepExecutor

class DecompositionOrchestrator:
    def __init__(self, llm, generator, retriever):
        self.planner = QueryDecomposer(llm)
        self.executor = StepExecutor(generator, retriever)
        
    def run(self, user_question):
        # PHASE 1: Decomposition 
        print(f"Analyzing question: {user_question}")
        plan = self.planner.create_plan(user_question)
        print(f"Generated plan: {plan}")
        
        context = {}
        
        # PHASE 2: Sequential Execution 
        for i, step in enumerate(plan):
            print(f"--- Executing Step {i+1}: {step} ---")
            
            try:
                result = self.executor.execute_step(step, context)
                
                if not result:
                    print("No result. Attempting reformulation or relaxing constraints...")
                    continue
                
                # Save result to context for subsequent steps
                context[f"step_{i+1}"] = result
                
            except Exception as e:
                print(f"Error in step {i+1}: {e}")
                break
        
        # PHASE 3: Final Synthesis, combine results into natural language
        return self._synthesize_answer(user_question, context)

    def _synthesize_answer(self, question, context):
        return "Final answer based on..." 
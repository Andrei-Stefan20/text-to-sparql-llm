import logging
from typing import Dict, List, Any
from .planner import QueryPlanner
from .executor import StepRunner

logger = logging.getLogger(__name__)

class QueryProcessor:
    """Coordinates query decomposition with iterative refinement and synthesis."""
    
    def __init__(self, llm, generator, retriever):
        self.llm = llm
        self.planner = QueryPlanner(llm)
        self.executor = StepRunner(generator, retriever)
        self.execution_log = []
        
    def run(self, user_question: str) -> str:
        """
        Runs the complete decomposition pipeline with iterative refinement.
        
        Args:
            user_question: Natural language query to process
            
        Returns:
            Final synthesized answer from all execution steps
        """
        logger.info(f"{'='*80}")
        logger.info(f"ANALYZING QUESTION: {user_question}")
        logger.info(f"{'='*80}")
        
        # Phase 1: Generate iterative decomposition plan
        steps_plan = self.planner.create_plan_iterative(user_question, max_steps=10)
        
        if not steps_plan:
            logger.warning("No decomposition plan generated.")
            return "Could not decompose the question into actionable steps."
        
        logger.info(f"Generated {len(steps_plan)} steps for decomposition")
        
        # Phase 2: Execute steps with context accumulation
        execution_results = {}
        execution_context = {}
        
        for step_idx, step in enumerate(steps_plan, 1):
            step_id = f"step_{step_idx}"
            logger.info(f"\n--- EXECUTING STEP {step_idx}/{len(steps_plan)} ---")
            logger.info(f"Description: {step.get('description', 'N/A')[:100]}")
            
            try:
                # Execute the step
                results, metadata = self.executor.execute_step(step, execution_context)
                
                # Store results and metadata
                execution_results[step_id] = results
                step['results'] = results
                step['metadata'] = metadata
                execution_context[step_idx] = results
                
                # Log execution
                self.execution_log.append({
                    'step': step_idx,
                    'description': step.get('description'),
                    'status': metadata.get('status'),
                    'result_count': metadata.get('result_count', 0)
                })
                
                if metadata.get('status') == 'failed':
                    logger.warning(f"Step {step_idx} failed: {metadata.get('reason')}")
                    # Continue to next step - don't break
                else:
                    logger.info(f"Step {step_idx} completed successfully. Results: {metadata.get('result_count', 0)} items")
                
            except Exception as e:
                logger.error(f"Unexpected error in step {step_idx}: {e}")
                self.execution_log.append({
                    'step': step_idx,
                    'description': step.get('description'),
                    'status': 'error',
                    'error': str(e)
                })
                continue
        
        # Phase 3: Synthesize final answer from all results
        final_answer = self._combine_results(user_question, steps_plan, execution_results)
        
        logger.info(f"\n{'='*80}")
        logger.info("FINAL ANSWER")
        logger.info(f"{'='*80}")
        logger.info(final_answer)
        
        return final_answer
    
    def _combine_results(self, question: str, steps: List[Dict], results: Dict[str, Any]) -> str:
        """
        Combines and synthesizes final answer from all step results.
        """
        # Filter successful results
        successful_results = {
            k: v for k, v in results.items() 
            if v is not None and isinstance(v, list) and len(v) > 0
        }
        
        if not successful_results:
            return "No results found. The question could not be answered with the available data."
        
        # Aggregate results based on question type
        logger.info(f"Synthesizing results from {len(successful_results)} successful steps")
        
        # Build synthesis prompt
        synthesis_prompt = self._build_result_prompt(question, steps, successful_results)
        
        try:
            # Use LLM to synthesize natural language answer
            synthesis_response = self.llm.generate(synthesis_prompt, max_new_tokens=256)
            return synthesis_response
        except Exception as e:
            logger.error(f"Error during synthesis: {e}")
            # Fallback: return structured results
            return self._fallback_synthesis(successful_results)
    
    def _build_result_prompt(self, question: str, steps: List[Dict], results: Dict) -> str:
        """
        Builds prompt for final answer combination.
        """
        results_summary = "\n".join([
            f"Step {i+1} ({step.get('description', 'N/A')[:50]}): {len(results.get(f'step_{i+1}', []))} results"
            for i, step in enumerate(steps)
        ])
        
        # Sample some results for context
        sample_results = {}
        for step_idx, (key, vals) in enumerate(list(results.items())[:3], 1):
            if vals and isinstance(vals, list):
                sample_results[f"step_{step_idx}"] = vals[:3]
        
        prompt = f"""Based on the decomposed query execution results, provide a natural language answer.

Original Question: {question}

Execution Results Summary:
{results_summary}

Sample Results:
{str(sample_results)}

Provide a clear, concise answer to the original question based on these results:"""
        
        return prompt
    
    def _fallback_synthesis(self, results: Dict[str, List]) -> str:
        """
        Fallback synthesis without LLM.
        """
        total_items = sum(len(v) if v else 0 for v in results.values())
        total_steps = len(results)
        
        return f"Query executed successfully across {total_steps} steps, retrieving {total_items} total items. Results available in execution log." 
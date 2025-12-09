import logging
from typing import Dict, List, Any, Optional
from .planner import QueryPlanner
from .executor import StepRunner

logger = logging.getLogger(__name__)

class QueryProcessor:
    """Coordinates query decomposition with iterative refinement and synthesis.
    
    Unified reporting: All execution details are logged through ReportManager
    for consistent, centralized tracking across the pipeline.
    """
    
    def __init__(self, llm, generator, retriever, reporter=None):
        """
        Initialize query processor.
        
        Args:
            llm: Language model for planning and synthesis
            generator: Model for SPARQL generation (can be same as llm)
            retriever: Tool for SPARQL execution against knowledge base
            reporter: Optional ReportManager instance for unified logging
        """
        self.llm = llm
        self.planner = QueryPlanner(llm)
        self.executor = StepRunner(generator, retriever)
        self.reporter = reporter
        self.execution_log = []
        
    def run(self, user_question: str, question_id: int = 1) -> str:
        """
        Runs the complete decomposition pipeline with iterative refinement.
        
        All execution details are logged through ReportManager (if provided)
        for unified, consistent reporting.
        
        Args:
            user_question: Natural language query to process
            question_id: Identifier for this question in the report
            
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
        
        for step_idx, step in enumerate(steps_plan):  # 0-based enumeration
            step_num = step_idx + 1  # For user-facing messages (1-based)
            step_id = f"step_{step_num}"
            logger.info(f"\n--- EXECUTING STEP {step_num}/{len(steps_plan)} ---")
            logger.info(f"Description: {step.get('description', 'N/A')[:100]}")
            
            try:
                # Execute the step (pass 0-based index in context_history)
                results, metadata = self.executor.execute_step(step, execution_context, step_idx)
                
                # Store results and metadata
                execution_results[step_id] = results
                step['results'] = results
                step['metadata'] = metadata
                execution_context[step_idx] = results  # Store with 0-based index
                
                # Log execution (uniform reporting)
                step_log_entry = {
                    'step': step_num,
                    'description': step.get('description'),
                    'status': metadata.get('status'),
                    'result_count': metadata.get('result_count', 0),
                    'query_type': step.get('query_type'),
                    'depends_on': step.get('depends_on_step'),
                    'query': metadata.get('query'),
                    'error': metadata.get('reason') if metadata.get('status') == 'failed' else None
                }
                self.execution_log.append(step_log_entry)
                
                # Log to ReportManager if available
                if self.reporter:
                    self.reporter.log_decomposition_step(
                        question_id=question_id,
                        step_num=step_num,
                        step_description=step.get('description', 'N/A'),
                        query_type=step.get('query_type', 'unknown'),
                        status=metadata.get('status', 'unknown'),
                        result_count=metadata.get('result_count', 0),
                        query=metadata.get('query'),
                        error=metadata.get('reason') if metadata.get('status') == 'failed' else None,
                        depends_on=step.get('depends_on_step')
                    )
                
                if metadata.get('status') == 'failed':
                    logger.warning(f"Step {step_num} failed: {metadata.get('reason')}")
                    # Continue to next step - don't break
                else:
                    logger.info(f"Step {step_num} completed successfully. Results: {metadata.get('result_count', 0)} items")
                
            except Exception as e:
                logger.error(f"Unexpected error in step {step_num}: {e}")
                error_log = {
                    'step': step_num,
                    'description': step.get('description'),
                    'status': 'error',
                    'error': str(e)
                }
                self.execution_log.append(error_log)
                
                # Log error to ReportManager
                if self.reporter:
                    self.reporter.log_decomposition_step(
                        question_id=question_id,
                        step_num=step_num,
                        step_description=step.get('description', 'N/A'),
                        query_type=step.get('query_type', 'unknown'),
                        status='error',
                        result_count=0,
                        error=str(e),
                        depends_on=step.get('depends_on_step')
                    )
                continue
        
        # Phase 3: Synthesize final answer from all results
        final_answer = self._combine_results(user_question, steps_plan, execution_results)
        
        # Log complete decomposition to ReportManager
        if self.reporter:
            self.reporter.log_decomposition(
                question=user_question,
                decomposition_steps=steps_plan,
                execution_results=execution_results,
                final_answer=final_answer,
                execution_log=self.execution_log
            )
        
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
        Builds comprehensive prompt for final answer synthesis.
        Includes complete result sets and explicit instructions for combining multi-step results.
        """
        # Build detailed results summary with counts and descriptions
        results_summary = []
        for i, step in enumerate(steps):
            step_key = f"step_{i+1}"
            result_list = results.get(step_key, [])
            result_count = len(result_list) if result_list else 0
            results_summary.append(f"Step {i+1} ({step.get('description', 'N/A')[:70]}): {result_count} items found")
        
        # Build detailed result sections showing actual data from each step
        detailed_results = []
        for i, step in enumerate(steps):
            step_key = f"step_{i+1}"
            result_list = results.get(step_key, [])
            
            if result_list and isinstance(result_list, list):
                detailed_results.append(f"\n[Step {i+1} Results - {step.get('description', '')[:50]}]")
                # Show structured results preserving key-value relationships
                for idx, item in enumerate(result_list[:5], 1):  # Show first 5 results per step
                    if isinstance(item, dict):
                        item_pairs = ", ".join([f"{k}: {v.get('value', v) if isinstance(v, dict) else v}" 
                                               for k, v in list(item.items())[:4]])
                        detailed_results.append(f"  {idx}. {item_pairs}")
                    else:
                        detailed_results.append(f"  {idx}. {str(item)[:100]}")
                
                if len(result_list) > 5:
                    detailed_results.append(f"  ... and {len(result_list) - 5} more items")
        
        # Determine aggregation type based on question and steps
        aggregation_hint = self._determine_aggregation_type(question, steps)
        
        prompt = f"""Based on the decomposed query execution results, synthesize a natural language answer.

Original Question: {question}

Execution Results Summary:
{chr(10).join(results_summary)}

Complete Step Results:
{chr(10).join(detailed_results) if detailed_results else "(No results from any step)"}

Result Combination Strategy: {aggregation_hint}

Task: Synthesize all results above into a clear, complete answer to the original question.
Instructions:
1. If steps retrieved DIFFERENT ENTITY TYPES: Combine/filter them meaningfully (e.g., authors AND their books)
2. If steps have DEPENDENCIES: Use earlier step results to interpret later steps (e.g., "these books by those authors")
3. If aggregation was done: Summarize the key numbers/rankings (e.g., "Top 3 tallest buildings")
4. Remove duplicates if combining similar results
5. Provide structured answer (e.g., numbered list for multiple items)

Answer:"""
        
        return prompt
    
    def _determine_aggregation_type(self, question: str, steps: List[Dict]) -> str:
        """
        Determines what type of result combination is needed based on question and steps.
        """
        question_lower = question.lower()
        
        # Check for aggregation keywords
        if any(word in question_lower for word in ['count', 'how many', 'total', 'number of', 'sum', 'average']):
            return "AGGREGATION (count/sum results across steps)"
        
        # Check for ranking/selection keywords
        if any(word in question_lower for word in ['top', 'tallest', 'highest', 'largest', 'most', 'best', 'ranked']):
            return "RANKING (select top items from results)"
        
        # Check for filtering keywords
        if any(word in question_lower for word in ['between', 'after', 'before', 'greater than', 'less than', 'filter']):
            return "FILTERING (apply constraints to narrow results)"
        
        # Default: multi-entity join
        step_types = [s.get('query_type', '').lower() for s in steps]
        if len(set(step_types)) > 1:
            return "JOINING (combine results from different entity searches)"
        
        return "CONSOLIDATION (merge all results into comprehensive answer)"
    
    def _fallback_synthesis(self, results: Dict[str, List]) -> str:
        """
        Fallback synthesis without LLM.
        """
        total_items = sum(len(v) if v else 0 for v in results.values())
        total_steps = len(results)
        
        return f"Query executed successfully across {total_steps} steps, retrieving {total_items} total items. Results available in execution log." 
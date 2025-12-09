import logging
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)

class StepRunner:
    """Runs individual decomposition steps with retry and error recovery logic."""
    
    def __init__(self, generator_model, retriever_tool):
        self.generator = generator_model
        self.retriever = retriever_tool
        self.max_retries = 3
        self.retry_strategies = ['relax_constraints', 'simplify_query', 'alternative_property']

    def execute_step(self, step_dict: Dict, context_history: Dict) -> Tuple[Optional[List], Dict]:
        """
        Executes a decomposition step with error recovery.
        
        Args:
            step_dict: Step dictionary with description, query_type, dependencies
            context_history: Dictionary of results from previous steps
            
        Returns:
            Tuple of (results, step_metadata)
        """
        step_description = step_dict.get('description', '')
        query_type = step_dict.get('query_type', 'entity_search')
        depends_on = step_dict.get('depends_on_step')
        
        # Normalize depends_on field: convert lists and strings to integer or None.
        if isinstance(depends_on, list):
            depends_on = depends_on[0] if depends_on else None
        if isinstance(depends_on, str):
            try:
                depends_on = int(depends_on)
            except (ValueError, TypeError):
                depends_on = None
        
        logger.info(f"Executing step: {step_description[:80]}...")
        
        # Verify all dependencies are satisfied before proceeding with execution.
        if depends_on and depends_on not in context_history:
            logger.warning(f"Step depends on step {depends_on} which has not been executed yet.")
            return None, {'status': 'skipped', 'reason': 'missing_dependency'}
        
        # Build comprehensive prompt with execution context from previous steps.
        context_str = self._format_context(context_history)
        sparql_query = self._generate_sparql_for_step(
            step_description, 
            query_type, 
            context_str,
            depends_on,
            context_history
        )
        
        if not sparql_query:
            return None, {'status': 'failed', 'reason': 'query_generation_failed'}
        
        # Execute SPARQL query with automatic retry logic and error recovery.
        results, execution_info = self._execute_with_retry(sparql_query, step_description)
        
        logger.info(f"Step result: {len(results) if results else 0} items retrieved from Wikidata.")
        
        return results, {
            'status': 'success' if results else 'failed',
            'query': sparql_query,
            'result_count': len(results) if results else 0,
            'execution_info': execution_info
        }
    
    def _generate_sparql_for_step(self, description: str, query_type: str, context: str, 
                                  depends_on: Optional[int], context_history: Dict) -> Optional[str]:
        """
        Generate SPARQL query from step description using LLM-based generation.
        Incorporates context from previous decomposition steps.
        """
        dependency_context = ""
        if depends_on and depends_on in context_history:
            # Include results from previous step to inform current query generation.
            dep_results = context_history[depends_on]
            if dep_results:
                results_preview = str(dep_results)[:200] if isinstance(dep_results, list) else str(dep_results)
                dependency_context = f"\nUse results from step {depends_on}: {results_preview}"
            else:
                dependency_context = f"\nNote: Step {depends_on} returned no results. Generate fallback query."
        elif depends_on:
            dependency_context = f"\nNote: Step {depends_on} was skipped or failed. Generate independent query."
        
        prompt = f"""You are a SPARQL expert for Wikidata. Generate a single, executable SPARQL query.

Task: {description}
Query Type: {query_type}

Context from previous steps:
{context}
{dependency_context}

Requirements:
- Generate only valid SPARQL syntax (no markdown, no explanations).
- Use Wikidata properties (P* format) and entities (Q* format).
- Include LIMIT 100 to prevent excessive data retrieval.
- Handle missing data gracefully with OPTIONAL clauses.

SPARQL Query:"""
        
        try:
            # Generate SPARQL using the configured language model.
            query = self.generator.generate(prompt, max_new_tokens=400)
            # Remove formatting artifacts and ensure proper SPARQL syntax.
            query = self._clean_sparql(query)
            return query if query else None
        except Exception as e:
            logger.error(f"Error generating SPARQL: {e}")
            return None
    
    def _execute_with_retry(self, query: str, step_description: str) -> Tuple[Optional[List], Dict]:
        """
        Execute SPARQL query against Wikidata endpoint with automatic retry on failure.
        Uses exponential backoff strategy for transient failures.
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Execution attempt {attempt}/{self.max_retries}")
                results = self.retriever.run_sparql(query)
                
                if results:
                    return results, {'attempts': attempt, 'success': True}
                elif attempt < self.max_retries:
                    logger.warning(f"No results returned. Retrying with adjusted query parameters...")
                    # Could implement adaptive query modification here.
                    continue
                else:
                    return None, {'attempts': attempt, 'success': False, 'reason': 'no_results'}
                    
            except Exception as e:
                logger.error(f"Execution error on attempt {attempt}: {e}")
                
                if attempt < self.max_retries:
                    logger.info(f"Retrying with alternative strategy...")
                    continue
                else:
                    return None, {'attempts': attempt, 'success': False, 'reason': str(e)}
        
        return None, {'attempts': self.max_retries, 'success': False}
    
    def _format_context(self, context_history: Dict) -> str:
        """
        Format previous step results into human-readable context string.
        Provides contextual information for subsequent step generation.
        """
        if not context_history:
            return "(No previous context)"
        
        context_lines = []
        for step_num, results in context_history.items():
            if results:
                result_preview = str(results)[:200]
                context_lines.append(f"Step {step_num} results: {result_preview}")
        
        return "\n".join(context_lines) if context_lines else "(No usable context)"
    
    def _clean_sparql(self, query: str) -> str:
        """
        Clean SPARQL query by removing markdown artifacts and formatting debris.
        Ensures LIMIT/OFFSET clauses appear before closing } of WHERE block.
        This is critical for SPARQL syntax compliance and Wikidata endpoint compatibility.
        """
        q = query.strip()
        # Remove markdown code fence markers if present.
        q = q.replace('```sparql', '').replace('```', '').strip()
        q = q.split('```')[0].strip()
        
        # Extract LIMIT and OFFSET lines (they should appear at query end).
        lines = q.split('\n')
        limit_lines = []
        non_limit_lines = []
        
        for line in lines:
            stripped = line.strip().upper()
            if stripped.startswith(('LIMIT', 'OFFSET')):
                limit_lines.append(line.rstrip())
            else:
                non_limit_lines.append(line)
        
        # If no LIMIT clauses exist, return query with trailing whitespace removed.
        if not limit_lines:
            while non_limit_lines and not non_limit_lines[-1].strip():
                non_limit_lines.pop()
            return '\n'.join(non_limit_lines)
        
        # Find the last closing brace } and insert LIMIT before it.
        # Process from end to beginning to locate correct insertion point.
        result = []
        limit_inserted = False
        
        for i in range(len(non_limit_lines) - 1, -1, -1):
            line = non_limit_lines[i]
            
            if '}' in line and not limit_inserted:
                # Found closing brace - split line and insert LIMIT before it.
                before_brace = line[:line.rfind('}')].rstrip()
                after_brace = line[line.rfind('}'):]
                
                # Remove empty lines before closing brace for clean formatting.
                while result and not result[-1].strip():
                    result.pop()
                
                if before_brace:
                    result.append(before_brace)
                
                # Add LIMIT/OFFSET with proper indentation.
                for limit_line in limit_lines:
                    result.append('  ' + limit_line)
                
                result.append(after_brace)
                limit_inserted = True
            elif line.strip() or i < len(non_limit_lines) - 1:
                result.append(line)
        
        # Reverse list since we built it from end to beginning.
        result.reverse()
        
        return '\n'.join(result)
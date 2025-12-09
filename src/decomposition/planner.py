import logging
import re
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)

class QueryPlanner:
    """Decomposes complex queries into structured steps with iterative refinement."""
    
    def __init__(self, llm):
        self.llm = llm
        self.max_iterations = 5
        self.context_window = {}
        
    def create_plan_iterative(self, user_question: str, max_steps: int = 10) -> List[Dict]:
        """
        Generates and refines decomposition plan iteratively.
        The LLM generates one step at a time, deciding if more steps are needed.
        
        Args:
            user_question: Natural language question to decompose
            max_steps: Maximum number of steps to generate
            
        Returns:
            List of step dictionaries with task descriptions and dependencies
        """
        steps = []
        step_count = 0
        
        # Start iterative decomposition of the user question into structured steps.
        logger.info(f"Starting iterative decomposition for: {user_question}")
        
        while step_count < max_steps:
            step_count += 1
            
            # Build context string from results of previously completed steps.
            context_str = self._build_context_str(steps)
            
            # Request LLM to generate the next decomposition step.
            next_step, needs_more_steps = self._plan_next_step(
                user_question, 
                step_count, 
                context_str,
                steps
            )
            
            if not next_step:
                logger.info("No more steps needed.")
                break
                
            steps.append(next_step)
            logger.info(f"Step {step_count}: {next_step['description'][:100]}...")
            
            if not needs_more_steps:
                logger.info("Decomposition plan complete.")
                break
        
        # Store completed steps in context window for orchestrator access.
        self.context_window['last_steps'] = steps
        return steps
    
    def _plan_next_step(self, question: str, step_num: int, context: str, prev_steps: List) -> Tuple[Optional[Dict], bool]:
        """
        Plans the next step using the language model.
        """
        prev_steps_text = "\n".join([f"  {i+1}. {s.get('description', 'N/A')}" for i, s in enumerate(prev_steps)])
        
        prompt = f"""You are a SPARQL query decomposition expert for Wikidata.

Original Question: {question}

Previous Steps Planned:
{prev_steps_text if prev_steps_text else "(None - this is the first step)"}

Current Context Available:
{context if context else "(No results yet)"}

Task: Generate EXACTLY ONE next step needed to answer the question.
Consider:
- Is this step independent or does it depend on previous results?
- What specific entity/property should this step query?
- Is this a filtering/aggregation step or a data retrieval step?

IMPORTANT: Respond ONLY with valid JSON, no other text.
Response format:
{{"step_description": "Clear description of what this step should do", "query_type": "entity_search|property_search|aggregation|filtering|join", "depends_on_step": null, "needs_more_steps": true, "reasoning": "Why this step is needed"}}"""
        
        try:
            response = self.llm.generate(prompt, max_new_tokens=300)
            step_data = self._parse_json_response(response)
            
            if step_data:
                # Normalize field names: convert 'step_description' to 'description' if needed.
                if 'step_description' in step_data and 'description' not in step_data:
                    step_data['description'] = step_data.pop('step_description')
                
                # Ensure all required keys have default values for safety.
                step_data.setdefault('description', f'Step {step_num}')
                step_data.setdefault('query_type', 'entity_search')
                step_data.setdefault('depends_on_step', None)
                step_data.setdefault('needs_more_steps', True)
                
                return step_data, step_data.get('needs_more_steps', True)
        except Exception as e:
            logger.error(f"Error generating step {step_num}: {e}")
        
        return None, False
    
    def _parse_json_response(self, response: str) -> Optional[Dict]:
        """
        Safely parse JSON from LLM response using multiple fallback strategies.
        Handles various formatting issues and markdown artifacts.
        """
        import json
        
        if not response or not response.strip():
            logger.warning("Empty response received from LLM.")
            return None
        
        # Strategy 1: Try direct JSON parsing.
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Extract JSON object from response (may contain extra text).
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse extracted JSON: {response[:100]}")
        
        # Strategy 3: Clean common formatting issues and retry parsing.
        try:
            # Remove markdown code fence markers.
            cleaned = response.replace('```json', '').replace('```', '').strip()
            # Extract just the JSON object.
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                # Fix common JSON formatting issues.
                json_str = json_str.replace("'", '"')  # Single quotes to double quotes.
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed after cleanup attempt: {e}")
        
        # All parsing strategies failed, return None.
        logger.warning(f"Could not parse JSON response: {response[:200]}")
        return None
    
    def _build_context_str(self, steps: List[Dict]) -> str:
        """
        Build context string from results of completed decomposition steps.
        Summarizes findings to inform subsequent step generation.
        """
        if not steps:
            return ""
        
        context_lines = []
        for i, step in enumerate(steps):
            context_lines.append(f"Step {i+1}: {step.get('description', '')}")
            if step.get('results'):
                # Summarize results from this step.
                results = step['results']
                if isinstance(results, list):
                    context_lines.append(f"  Results: {len(results)} items found")
                    if results:
                        context_lines.append(f"  Sample: {results[:2]}")
        
        return "\n".join(context_lines)
    
    def create_plan(self, user_question: str) -> List[str]:
        """
        Legacy method for backwards compatibility.
        Returns simplified list of step descriptions.
        """
        steps = self.create_plan_iterative(user_question)
        return [step['description'] for step in steps]
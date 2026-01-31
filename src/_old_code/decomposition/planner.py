import logging
import re
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)


class QueryPlanner:

    def __init__(self, llm):
        """Initialize QueryPlanner.

        Args:
            llm: Language model for step generation and planning
        """
        self.llm = llm
        self.max_iterations = 5
        self.context_window = {}

    def create_plan_iterative(
        self, user_question: str, max_steps: int = 10
    ) -> List[Dict]:
        """
        The planner iteratively asks the LLM to generate one execution step at a time,
        using results from previous steps to inform subsequent steps.

        Args:
            user_question: Natural language question to decompose
            max_steps: Maximum number of steps to generate (prevents infinite loops)

        Returns:
            List of step dictionaries, each containing:
                - description: Step description
                - query_type: Type of operation (entity_search, filtering)
                - depends_on_step: Step number
                - needs_more_steps: Whether additional steps are needed
                - reasoning: Why this step is necessary
        """
        steps = []
        step_count = 0

        logger.info(f"Starting iterative decomposition for: {user_question}")

        while step_count < max_steps:
            step_count += 1

            context_str = self._build_context_str(steps)

            next_step, needs_more_steps = self._plan_next_step(
                user_question, step_count, context_str, steps
            )

            if not next_step:
                logger.info("No more steps needed.")
                break

            steps.append(next_step)
            logger.info(f"Step {step_count}: {next_step['description'][:100]}...")

            if not needs_more_steps:
                logger.info("Decomposition plan complete.")
                break

        self.context_window["last_steps"] = steps
        return steps

    def _plan_next_step(
        self, question: str, step_num: int, context: str, prev_steps: List
    ) -> Tuple[Optional[Dict], bool]:
        """
        Plans the next step using the language model.
        """
        prev_steps_text = "\n".join(
            [
                f"  {i+1}. {s.get('description', 'N/A')}"
                for i, s in enumerate(prev_steps)
            ]
        )

        prompt = f"""You are a SPARQL query decomposition expert for Wikidata.

Original Question: {question}

Previous Steps Planned:
{prev_steps_text if prev_steps_text else "(None - this is the first step)"}

Current Context Available:
{context if context else "(No results yet)"}

Task: Generate EXACTLY ONE next step needed to answer the question.

Decision Logic:
1. DATA RETRIEVAL (entity_search, property_search): Start by finding base entities or properties matching the question
2. FILTERING: Apply constraints (dates, regions, numeric ranges) to narrow results
3. JOIN: Combine results from previous steps (e.g., linking entities through relationships)
4. AGGREGATION: Count, group, or summarize results
5. SYNTHESIS: Final step to prepare answer format

Guidelines:
- Step 1 should be INDEPENDENT (no dependencies) to kickstart the pipeline
- Each step builds on previous ones for multi-hop queries (e.g., "authors from Germany" -> "their books" -> "filter by rating")
- Avoid redundant steps - don't repeat queries from previous steps
- For multi-entity queries ("authors AND books"), decompose into separate retrieval steps
- Keep step scope focused: one entity type or one constraint per step

Examples of good decomposition:
Q: "Books by German authors born after 1900 with rating > 4"
Step 1: Find authors born in Germany after 1900 (entity_search, independent)
Step 2: Get books written by these authors (entity_search, depends_on_step: 1)
Step 3: Filter books by rating > 4 (filtering, depends_on_step: 2)

Q: "Tallest buildings in New York completed after 2000"
Step 1: Find buildings in New York (entity_search, independent)
Step 2: Filter by completion year > 2000 (filtering, depends_on_step: 1)
Step 3: Sort by height and get top results (aggregation, depends_on_step: 2)

IMPORTANT: Respond ONLY with valid JSON, no other text. Step numbers in depends_on_step are 1-based (1, 2, 3, etc).
Response format:
{{"step_description": "Clear description of what this step should do", "query_type": "entity_search|property_search|aggregation|filtering|join", "depends_on_step": null, "needs_more_steps": true, "reasoning": "Why this step is needed"}}"""

        try:
            response = self.llm.generate(prompt, max_new_tokens=300)
            step_data = self._parse_json_response(response)

            if step_data:
                if "step_description" in step_data and "description" not in step_data:
                    step_data["description"] = step_data.pop("step_description")

                step_data.setdefault("description", f"Step {step_num}")
                step_data.setdefault("query_type", "entity_search")
                step_data.setdefault("depends_on_step", None)
                step_data.setdefault("needs_more_steps", True)

                return step_data, step_data.get("needs_more_steps", True)
        except Exception as e:
            logger.error(f"Error generating step {step_num}: {e}")

        return None, False

    def _parse_json_response(self, response: str) -> Optional[Dict]:
        """
        Parse JSON from LLM response using multiple fallback strategies.
        Handles various formatting issues and markdown artifacts.
        """
        import json

        if not response or not response.strip():
            logger.warning("Empty response received from LLM.")
            return None

        # Strategy 1: Try direct JSON parsing.
        try:
            parsed = json.loads(response)
            if not isinstance(parsed, dict):
                logger.warning(f"Expected dict, got {type(parsed).__name__}")
                return None
            return parsed
        except json.JSONDecodeError as e:
            logger.debug(f"Direct JSON parse failed: {e}")

        # Strategy 2: Extract JSON object from response.
        try:
            json_match = re.search(
                r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response, re.DOTALL
            )
            if json_match:
                json_str = json_match.group(0)
                parsed = json.loads(json_str)
                if isinstance(parsed, dict):
                    return parsed
                logger.warning(
                    f"Extracted content is {type(parsed).__name__}, not dict"
                )
        except json.JSONDecodeError as e:
            logger.debug(f"Failed to parse extracted JSON: {e}")

        # Strategy 3: Clean common formatting issues and retry parsing.
        try:
            # Remove markdown code fence markers.
            cleaned = response.replace("```json", "").replace("```", "").strip()
            # Extract just the JSON object.
            json_match = re.search(
                r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", cleaned, re.DOTALL
            )
            if json_match:
                json_str = json_match.group(0)
                # Fix common JSON formatting issues.
                json_str = json_str.replace("'", '"')
                json_str = json_str.replace("\n", "\\n")
                parsed = json.loads(json_str)
                if isinstance(parsed, dict):
                    return parsed
        except Exception as e:
            logger.debug(f"Failed after cleanup attempt: {e}")

        # All parsing strategies failed, return None with detailed error logging.
        logger.error(
            f"Could not parse JSON response from LLM. Response (first 500 chars): {response[:500]}"
        )
        logger.error(f"Full response available for debugging in step generation log")
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
            if step.get("results"):
                # Summarize results from this step.
                results = step["results"]
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
        return [step["description"] for step in steps]

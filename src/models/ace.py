import json
import logging
from pathlib import Path
from typing import List, Any

logger = logging.getLogger(__name__)

CURATOR_SYSTEM_PROMPT = """You are a helpful Strategy Curator for Wikidata SPARQL.
Your goal is to help the user write better queries by creating a general rule based on their mistake.

TASK:
1. Analyze the User Question, the Failed Query, and the Error.
2. Write ONE simple, general rule to prevent this error.
3. The rule must start with "STRATEGY: ".

EXAMPLE:
Error: Property P50 used for a movie director.
Response: STRATEGY: For movie directors, use wdt:P57, not wdt:P50.
"""

class ACEEngine:
    """Automated Correction Engine that learns from SPARQL query errors."""
    
    def __init__(self, generator_interface: Any, playbook_path: Path):
        """
        Initializes the ACE engine with a generator and playbook storage.
        
        Args:
            generator_interface: Object with .generate_raw(prompt, stop=...) method
            playbook_path: Path to JSON file containing learned strategies
        """
        self.generator = generator_interface
        self.playbook_path = playbook_path
        self.playbook: List[str] = []
        self.load_playbook()

    def load_playbook(self):
        """Loads existing strategies from persistent storage."""
        if self.playbook_path.exists():
            try:
                with open(self.playbook_path, 'r', encoding='utf-8') as f:
                    self.playbook = json.load(f)
            except Exception:
                self.playbook = []

    def save_playbook(self):
        """Persists current strategies to disk."""
        with open(self.playbook_path, 'w', encoding='utf-8') as f:
            json.dump(self.playbook, f, indent=2)

    def get_context_block(self) -> str:
        """Formats playbook strategies for prompt injection."""
        if not self.playbook:
            return "No specific strategies yet."
        return "\n".join([f"- {rule}" for rule in self.playbook])

    def curate(self, question: str, wrong_sparql: str, error_msg: str):
        """
        Analyzes query failures and generates corrective strategies.
        
        Args:
            question: Original natural language question
            wrong_sparql: Failed SPARQL query
            error_msg: Error description from execution or validation
        """
        prompt = f"{CURATOR_SYSTEM_PROMPT}\n\n"
        prompt += f"User Question: {question}\n"
        prompt += f"Failed Query: {wrong_sparql}\n"
        prompt += f"Error Message: {error_msg}\n\n"
        prompt += "Write the corrective rule (start with 'STRATEGY:'):"

        try:
            text = self.generator.generate_raw(
                prompt,
                max_new_tokens=128,
                stop=["\n\n", "User Question:"]
            )
            
            strategy = text.strip()
            
            if "STRATEGY:" in text:
                strategy = text.split("STRATEGY:")[1].strip()
            elif len(text) > 5 and "STRATEGY" not in text:
                strategy = text
                
            strategy = strategy.strip('"').strip("'")

            is_valid_rule = len(strategy) > 10 and any(x in strategy for x in ["P", "Q", "FILTER", "SELECT", "use", "Use"])
            
            if is_valid_rule:
                if strategy not in self.playbook:
                    self.playbook.append(strategy)
                    logger.info(f"ACE LEARNED: {strategy}")
                    self.save_playbook()
                else:
                    logger.info("ACE: Strategy already known.")
            else:
                logger.warning(f"ACE Ignored invalid/empty strategy: '{text}'")

        except Exception as e:
            logger.error(f"ACE Curation failed: {e}")
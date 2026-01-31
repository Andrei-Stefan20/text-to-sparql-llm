from typing import List, Optional

from omegaconf import DictConfig


class PromptBuilder:
    def __init__(self, config: DictConfig):
        self.cfg = config

    def build_system_prompt(self) -> str:
        return self.cfg.get("system_message", "You are a SPARQL expert.")

    def build_user_prompt(
        self,
        question: str,
        entities: List[str],
        context_examples: str,
        schema_hints: str,
    ) -> str:
        parts = []

        # 1. Task Definition
        parts.append("Task: Generate a valid SPARQL query for Wikidata.")

        # 2. Schema Hints
        if schema_hints:
            parts.append(
                f"### Relevant Properties (Hints):\nConsider using: {schema_hints}"
            )

        # 3. Entity Linking
        if entities:
            parts.append(f"### Identified Entities:\n{', '.join(entities)}")

        # 4. Few-Shot Examples (RAG)
        if context_examples:
            parts.append(f"### Similar Examples:\n{context_examples}")

        # 5. Question
        parts.append(f"### Question:\n{question}")
        parts.append("### SPARQL Query:")

        return "\n\n".join(parts)

from typing import List, Optional

from omegaconf import DictConfig


class PromptBuilder:
    def __init__(self, config: DictConfig):
        self.cfg = config

    def build_system_prompt(self) -> str:
        system_msg = self.cfg.get(
            "system_message",
            "You are a SPARQL expert. Generate ONLY valid SPARQL query code. "
            "Do NOT include explanations, comments, or markdown formatting. "
            "Output ONLY the query, starting with SELECT or CONSTRUCT."
        )
        return system_msg

    def build_user_prompt(
        self,
        question: str,
        entities: List[str],
        context_examples: str,
        schema_hints: str,
    ) -> str:
        parts = []

        # 1. Schema Hints (most specific info first)
        if schema_hints and self.cfg.get("include_schema_hint", False):
            parts.append(f"Relevant Properties: {schema_hints}")

        # 2. Entity Linking
        if entities and self.cfg.get("include_entities", False):
            parts.append(f"Entities: {', '.join(entities)}")

        # 3. Few-Shot Examples (RAG)
        if context_examples and self.cfg.get("include_examples", False):
            parts.append(f"Examples of similar queries:\n{context_examples}")

        # 4. Question
        parts.append(f"Question: {question}")
        
        # 5. Explicit instruction for clean output
        custom_instruction = self.cfg.get("custom_instruction", "")
        if custom_instruction:
            parts.append(f"\n{custom_instruction}")
        else:
            parts.append("\nOutput ONLY the SPARQL query (no markdown, no explanation):")

        return "\n".join(parts)

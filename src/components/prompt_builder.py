from typing import List, Optional, Union
from enum import Enum
import logging

from omegaconf import DictConfig

logger = logging.getLogger(__name__)

# Import LinkedEntity for type hints (avoid circular import)
try:
    from src.components.entity_linker import LinkedEntity
except ImportError:
    LinkedEntity = None


class PromptStrategy(str, Enum):
    """Available prompting strategies."""
    BASE = "base"           # Standard few-shot prompting
    COT = "cot"             # Chain-of-Thought reasoning
    DECOMPOSITION = "decomposition"  # Query decomposition into sub-queries


class PromptBuilder:
    """
    Builds prompts for SPARQL generation with multiple strategy support.
    
    Strategies:
    - base: Standard few-shot prompting with examples
    - cot: Chain-of-Thought - step-by-step reasoning before generating
    - decomposition: Breaks complex queries into sub-queries
    """
    
    def __init__(self, config: DictConfig):
        self.cfg = config
        self.strategy = PromptStrategy(
            config.get("strategy", "base").lower()
        )

    def build_system_prompt(self) -> str:
        """Builds the system prompt based on strategy."""
        
        if self.strategy == PromptStrategy.COT:
            return self._get_cot_system_prompt()
        elif self.strategy == PromptStrategy.DECOMPOSITION:
            return self._get_decomposition_system_prompt()
        else:
            return self._get_base_system_prompt()
    
    def _get_base_system_prompt(self) -> str:
        """Standard system prompt for few-shot generation."""
        return self.cfg.get(
            "system_message",
            """You are a SPARQL expert for Wikidata.
Generate ONLY valid SPARQL query code.
Do NOT include explanations, comments, code blocks, or any text.
Output ONLY the query starting with SELECT or CONSTRUCT."""
        )
    
    def _get_cot_system_prompt(self) -> str:
        """Chain-of-Thought system prompt."""
        return self.cfg.get(
            "system_message",
            """You are a SPARQL expert for Wikidata.
Your task is to translate natural language questions into SPARQL queries.

You must think step-by-step before writing the query:
1. Identify what the question is asking for (the target variable)
2. Identify the entities mentioned and their Wikidata IDs
3. Identify the relationships/properties needed
4. Consider any filters, aggregations, or special conditions
5. Write the SPARQL query

Always show your reasoning, then output the final query."""
        )
    
    def _get_decomposition_system_prompt(self) -> str:
        """Decomposition strategy system prompt."""
        return self.cfg.get(
            "system_message",
            """You are a SPARQL expert for Wikidata specializing in complex queries.

For complex questions, you will:
1. Analyze the question complexity
2. If complex, break it into simpler sub-questions
3. Write a sub-query for each sub-question
4. Combine sub-queries into the final SPARQL query

Use this approach for questions involving:
- Multiple conditions (AND, OR)
- Aggregations (COUNT, MAX, MIN, AVG)
- Nested relationships
- Temporal constraints
- Comparisons between entities"""
        )

    def _format_entities(self, entities: List) -> str:
        """
        Formats entities for the prompt.
        
        Handles both LinkedEntity objects and plain strings for backward compatibility.
        LinkedEntity format: "Obama (wd:Q76)"
        String format: "Obama"
        """
        formatted = []
        for entity in entities:
            if hasattr(entity, 'to_sparql_format'):
                # LinkedEntity object
                formatted.append(entity.to_sparql_format())
            elif isinstance(entity, dict) and entity.get('qid'):
                # Dict with qid
                formatted.append(f"{entity.get('text', str(entity))} (wd:{entity['qid']})")
            else:
                # Plain string
                formatted.append(str(entity))
        return ', '.join(formatted)

    def build_user_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
    ) -> str:
        """
        Builds the user prompt based on the selected strategy.
        """
        if self.strategy == PromptStrategy.COT:
            return self._build_cot_prompt(question, entities, context_examples, schema_hints)
        elif self.strategy == PromptStrategy.DECOMPOSITION:
            return self._build_decomposition_prompt(question, entities, context_examples, schema_hints)
        else:
            return self._build_base_prompt(question, entities, context_examples, schema_hints)

    def _build_base_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
    ) -> str:
        """Standard few-shot prompt."""
        parts = []

        # 1. Schema Hints (most specific info first)
        if schema_hints and self.cfg.get("include_schema_hint", False):
            parts.append(f"Relevant Properties: {schema_hints}")

        # 2. Entity Linking with QIDs
        if entities and self.cfg.get("include_entities", False):
            formatted_entities = self._format_entities(entities)
            parts.append(f"Entities: {formatted_entities}")

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

    def _build_cot_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
    ) -> str:
        """
        Chain-of-Thought prompt that guides the model through reasoning steps.
        """
        parts = []
        
        # 1. Context Section
        parts.append("=== CONTEXT ===")
        
        if schema_hints and self.cfg.get("include_schema_hint", False):
            parts.append(f"Available Properties: {schema_hints}")

        if entities and self.cfg.get("include_entities", False):
            formatted_entities = self._format_entities(entities)
            parts.append(f"Identified Entities: {formatted_entities}")

        # 2. Few-Shot Examples with reasoning (if available)
        if context_examples and self.cfg.get("include_examples", False):
            parts.append("\n=== SIMILAR EXAMPLES ===")
            parts.append(context_examples)

        # 3. Question
        parts.append("\n=== YOUR TASK ===")
        parts.append(f"Question: {question}")
        
        # 4. CoT Reasoning Template
        parts.append("\n=== REASONING (Think step-by-step) ===")
        parts.append("1. Target: What does the question ask for?")
        parts.append("2. Entities: Which Wikidata entities are involved?")
        parts.append("3. Properties: Which properties connect them?")
        parts.append("4. Constraints: Any filters, sorting, or aggregations?")
        parts.append("5. Query Pattern: What SPARQL pattern fits?")
        
        # 5. Output instruction
        parts.append("\n=== SOLUTION ===")
        parts.append("Reasoning:")
        
        return "\n".join(parts)

    def _build_decomposition_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
    ) -> str:
        """
        Decomposition prompt that breaks complex queries into sub-queries.
        """
        parts = []
        
        # 1. Context Section
        parts.append("=== AVAILABLE CONTEXT ===")
        
        if schema_hints and self.cfg.get("include_schema_hint", False):
            parts.append(f"Properties: {schema_hints}")

        if entities and self.cfg.get("include_entities", False):
            formatted_entities = self._format_entities(entities)
            parts.append(f"Entities: {formatted_entities}")

        # 2. Examples
        if context_examples and self.cfg.get("include_examples", False):
            parts.append("\n=== REFERENCE EXAMPLES ===")
            parts.append(context_examples)

        # 3. Question
        parts.append("\n=== QUESTION TO SOLVE ===")
        parts.append(f"{question}")
        
        # 4. Decomposition Template
        parts.append("\n=== DECOMPOSITION ANALYSIS ===")
        parts.append("""
Analyze the question complexity:
- Is this a SIMPLE query (single relationship)? → Write directly
- Is this a COMPLEX query? → Decompose first

If COMPLEX, follow this structure:

**Sub-question 1**: [First part of the question]
```sparql
# Sub-query 1
SELECT ?x WHERE { ... }
```

**Sub-question 2**: [Second part, may use results from above]
```sparql
# Sub-query 2 
SELECT ?y WHERE { ... }
```

**Final Combined Query**:
```sparql
# Combines all sub-queries
SELECT ... WHERE {
  # Integration of sub-patterns
}
```
""")
        
        # 5. Output instruction
        parts.append("=== YOUR SOLUTION ===")
        parts.append("Complexity Assessment:")
        
        return "\n".join(parts)

    def extract_sparql_from_response(self, response: str, validate_syntax: bool = True) -> str:
        """
        Extracts the final SPARQL query from model response with robust multi-pattern matching.
        Handles different response formats based on strategy.
        
        For CoT/Decomposition: extracts the last/final query from reasoning
        For Base: returns as-is or strips markdown
        
        Args:
            response: Raw LLM response
            validate_syntax: If True, validates extracted SPARQL and tries fallbacks
        
        Returns:
            Extracted SPARQL query (best effort)
        """
        import re
        
        if not response:
            return ""
        
        # Try multiple extraction methods in priority order
        extraction_attempts = [
            self._extract_from_code_blocks,
            self._extract_from_final_query_marker,
            self._extract_from_bare_statement,
            self._extract_from_query_keyword,
            self._extract_last_valid_block,
        ]
        
        for extractor in extraction_attempts:
            try:
                query = extractor(response)
                if query:
                    # Clean extracted query
                    query = self._clean_sparql(query)
                    # Replace '\n' with actual newlines
                    query = query.replace("\\n", "\n")
                    # Optionally validate syntax
                    if validate_syntax and self._is_valid_sparql_syntax(query):
                        return query
                    elif not validate_syntax:
                        return query
            except Exception as e:
                logger.debug(f"Extraction method {extractor.__name__} failed: {e}")
                continue
        
        # Final fallback: aggressive cleaning
        fallback_query = self._clean_sparql(response)
        fallback_query = fallback_query.replace("\\n", "\n")
        return fallback_query
    
    def _extract_from_code_blocks(self, response: str) -> Optional[str]:
        """Extracts SPARQL from markdown code blocks."""
        import re
        
        # Pattern for ```sparql ... ``` or ``` ... ```
        pattern = r'```(?:sparql)?\s*((?:PREFIX|SELECT|CONSTRUCT|ASK|DESCRIBE)[\s\S]*?)```'
        matches = re.findall(pattern, response, re.IGNORECASE)
        
        if matches:
            # Return the last code block (final query in decomposition)
            return matches[-1].strip()
        
        return None
    
    def _extract_from_final_query_marker(self, response: str) -> Optional[str]:
        """Extracts query after markers like 'Final Query:', 'SPARQL:', etc."""
        import re
        
        markers = [
            r'Final\s+(?:Combined\s+)?Query[:\s]+',
            r'SPARQL[:\s]+',
            r'Final\s+SPARQL[:\s]+',
            r'Corrected\s+Query[:\s]+',
            r'===\s*YOUR\s+SOLUTION\s*===[\s\S]*?',
        ]
        
        for marker in markers:
            pattern = marker + r'[\s\n]*```?(?:sparql)?[\s\n]*((?:PREFIX|SELECT|CONSTRUCT|ASK|DESCRIBE)[\s\S]+?)(?:```|$)'
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_from_bare_statement(self, response: str) -> Optional[str]:
        """Extracts bare SELECT/CONSTRUCT statements with proper bracket matching."""
        import re
        
        # Find all SPARQL keywords
        pattern = r'((?:PREFIX[^\n]+\n)*\s*(?:SELECT|CONSTRUCT|ASK|DESCRIBE)\s+[\s\S]+?)(?=\n\n|\nFinal|\n===|$)'
        matches = re.findall(pattern, response, re.IGNORECASE)
        
        if matches:
            # Find the one with balanced braces
            for match in reversed(matches):  # Try last first
                if self._has_balanced_braces(match):
                    return match.strip()
            
            # If none balanced, return last anyway
            return matches[-1].strip()
        
        return None
    
    def _extract_from_query_keyword(self, response: str) -> Optional[str]:
        """Extracts from first occurrence of SELECT/CONSTRUCT to end of balanced braces."""
        import re
        
        for keyword in ['SELECT', 'CONSTRUCT', 'ASK', 'DESCRIBE']:
            pattern = re.compile(rf'({keyword}\s+[\s\S]+)', re.IGNORECASE)
            match = pattern.search(response)
            if match:
                candidate = match.group(1)
                # Try to find balanced end
                return self._extract_until_balanced_braces(candidate)
        
        return None
    
    def _extract_last_valid_block(self, response: str) -> Optional[str]:
        """Attempts to find any text block that looks like SPARQL."""
        import re
        
        # Split by major markers
        blocks = re.split(r'\n\n+|\n===', response)
        
        for block in reversed(blocks):
            if any(kw in block.upper() for kw in ['SELECT', 'WHERE', 'PREFIX']):
                return block.strip()
        
        return None
    
    def _clean_sparql(self, query: str) -> str:
        """Cleans SPARQL query from common artifacts."""
        import re
        
        if not query:
            return ""
        
        # Remove markdown code block markers
        query = re.sub(r'^```(?:sparql)?\s*', '', query, flags=re.IGNORECASE)
        query = re.sub(r'\s*```$', '', query)
        
        # Remove common prefixes from text
        query = re.sub(r'^(?:SPARQL|Query|Final Query|Corrected Query)[:\s]+', '', query, flags=re.IGNORECASE)
        
        # Remove trailing ellipsis or incomplete markers
        query = re.sub(r'\.{3,}$', '', query)
        
        # Normalize whitespace
        query = '\n'.join(line.rstrip() for line in query.split('\n'))
        
        return query.strip()
    
    def _has_balanced_braces(self, text: str) -> bool:
        """Checks if text has balanced curly braces."""
        count = 0
        for char in text:
            if char == '{':
                count += 1
            elif char == '}':
                count -= 1
            if count < 0:
                return False
        return count == 0
    
    def _extract_until_balanced_braces(self, text: str) -> str:
        """Extracts text until curly braces are balanced."""
        count = 0
        for i, char in enumerate(text):
            if char == '{':
                count += 1
            elif char == '}':
                count -= 1
            if count == 0 and '}' in text[:i+1]:
                return text[:i+1]
        return text
    
    def _is_valid_sparql_syntax(self, query: str) -> bool:
        """Quick validation of SPARQL syntax without full parsing."""
        if not query:
            return False
        
        # Must start with PREFIX or SPARQL keyword
        query_stripped = query.strip().upper()
        valid_starts = ['PREFIX', 'SELECT', 'CONSTRUCT', 'ASK', 'DESCRIBE']
        if not any(query_stripped.startswith(start) for start in valid_starts):
            return False
        
        # Must have balanced braces
        if not self._has_balanced_braces(query):
            return False
        
        # Must contain WHERE clause for SELECT/CONSTRUCT
        if query_stripped.startswith(('SELECT', 'CONSTRUCT')):
            if 'WHERE' not in query_stripped:
                return False
        
        return True

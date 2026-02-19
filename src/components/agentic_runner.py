"""
Agentic SPARQL Generation using ReAct (Reason + Act) pattern.

The agent loop:
  1. Receives: question + entities + context examples + schema hints
  2. Generates: THOUGHT + ACTION (exploratory SPARQL) OR FINAL_ANSWER
  3. If ACTION: executes query on Wikidata → OBSERVATION → continues
  4. If FINAL_ANSWER: validates + returns

Response format the LLM must follow:
─────────────────────────────────────────
THOUGHT: <reasoning about what to do next>
ACTION: EXECUTE_SPARQL
```sparql
<exploratory query>
```
─────────────────────────────────────────
OR (final step):
─────────────────────────────────────────
THOUGHT: <I have all I need>
FINAL_ANSWER:
```sparql
<complete answer query>
```
─────────────────────────────────────────
"""

import asyncio
import logging
import re
import ssl
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class AgentStep:
    """Records a single reasoning + action step."""
    step_number: int
    thought: str
    action: str                    # "EXECUTE_SPARQL" | "FINAL_ANSWER"
    query: str                     # The SPARQL issued in this step
    observation: Optional[str]     # Result returned by Wikidata (None for FINAL_ANSWER)
    raw_llm_response: str


@dataclass
class AgentResult:
    """Final result of the agentic run."""
    final_query: str
    is_valid: bool
    steps: List[AgentStep] = field(default_factory=list)
    total_steps: int = 0
    termination_reason: str = ""   # "final_answer" | "max_steps" | "error"
    validation_error: Optional[str] = None


# ---------------------------------------------------------------------------
# Wikidata tool executor
# ---------------------------------------------------------------------------

class WikidataTool:
    """
    Executes exploratory SPARQL queries against Wikidata.
    Used by the agent as a tool to verify QIDs, PIDs, and schema.
    """

    ENDPOINT = "https://query.wikidata.org/sparql"
    STANDARD_PREFIXES = (
        "PREFIX wd: <http://www.wikidata.org/entity/>\n"
        "PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n"
        "PREFIX wikibase: <http://wikiba.se/ontology#>\n"
        "PREFIX p: <http://www.wikidata.org/prop/>\n"
        "PREFIX ps: <http://www.wikidata.org/prop/statement/>\n"
        "PREFIX pq: <http://www.wikidata.org/prop/qualifier/>\n"
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
        "PREFIX bd: <http://www.bigdata.com/rdf#>\n"
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
    )
    MAX_ROWS_IN_OBSERVATION = 10   # Truncate results to keep context small

    def __init__(self, timeout: int = 8):
        self.timeout = timeout
        self.sparql = SPARQLWrapper(self.ENDPOINT)
        self.sparql.setReturnFormat(JSON)
        self.sparql.addCustomHttpHeader("User-Agent", "AgenticSPARQLBot/1.0")
        self.sparql.setTimeout(timeout)

        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context

    def execute(self, query: str) -> str:
        """
        Runs a SPARQL query and returns a concise, human-readable observation
        string that can be appended to the LLM context.

        Returns a string like:
          "Results (3 rows): [['Q76', 'Barack Obama'], ['Q47', ...]]"
          "ASK result: true"
          "Error: <message>"
          "No results returned."
        """
        if not query or not query.strip():
            return "Error: empty query."

        # Inject prefixes if missing
        full_query = query if "PREFIX" in query.upper() else self.STANDARD_PREFIXES + query

        try:
            self.sparql.setQuery(full_query)
            raw = self.sparql.query().convert()
            return self._format_results(raw)

        except Exception as exc:
            err = str(exc)
            # Trim stack traces / long messages
            err = err.split("\n")[0][:200]
            return f"Error executing query: {err}"

    def _format_results(self, raw: Dict) -> str:
        """Converts SPARQLWrapper JSON output to a readable string."""

        # ASK query
        if "boolean" in raw:
            return f"ASK result: {str(raw['boolean']).lower()}"

        bindings = raw.get("results", {}).get("bindings", [])
        if not bindings:
            return "No results returned."

        vars_list = raw.get("head", {}).get("vars", [])
        rows = []
        for b in bindings[: self.MAX_ROWS_IN_OBSERVATION]:
            row = []
            for v in vars_list:
                val = b.get(v, {}).get("value", "")
                # Strip full Wikidata URI for readability
                val = val.replace("http://www.wikidata.org/entity/", "wd:")
                val = val.replace("http://www.wikidata.org/prop/direct/", "wdt:")
                row.append(val)
            rows.append(row)

        total = len(bindings)
        shown = len(rows)
        header = f"Results ({total} row{'s' if total != 1 else ''}"
        if total > self.MAX_ROWS_IN_OBSERVATION:
            header += f", showing first {shown}"
        header += "):"

        # Format as simple table
        col_labels = " | ".join(vars_list)
        separator = "-+-".join(["-" * max(len(v), 8) for v in vars_list])
        data_lines = [" | ".join(str(c) for c in r) for r in rows]

        return "\n".join([header, col_labels, separator] + data_lines)


# ---------------------------------------------------------------------------
# Response parser
# ---------------------------------------------------------------------------

class AgentResponseParser:
    """
    Parses LLM responses that follow the ReAct format.

    Handles:
    - THOUGHT + ACTION: EXECUTE_SPARQL + ```sparql...```
    - THOUGHT + FINAL_ANSWER: + ```sparql...```
    - Gracefully falls back when format is not perfectly followed
    """

    # Patterns (case-insensitive, flexible whitespace)
    _THOUGHT_RE = re.compile(r"THOUGHT\s*[:]\s*(.*?)(?=\nACTION|\nFINAL_ANSWER|$)", re.IGNORECASE | re.DOTALL)
    _ACTION_RE = re.compile(r"ACTION\s*[:]\s*EXECUTE_SPARQL", re.IGNORECASE)
    _FINAL_RE = re.compile(r"FINAL_ANSWER\s*[:]?", re.IGNORECASE)
    _SPARQL_BLOCK_RE = re.compile(r"```(?:sparql)?\s*([\s\S]*?)```", re.IGNORECASE)

    def parse(self, response: str) -> Tuple[str, str, str]:
        """
        Returns (thought, action, query) where:
          action = "EXECUTE_SPARQL" | "FINAL_ANSWER" | "UNKNOWN"
          query  = extracted SPARQL (may be empty on UNKNOWN)
        """
        thought = self._extract_thought(response)
        query = self._extract_last_sparql_block(response)

        if self._FINAL_RE.search(response):
            return thought, "FINAL_ANSWER", query

        if self._ACTION_RE.search(response):
            return thought, "EXECUTE_SPARQL", query

        # Fallback: if we found a SPARQL block with no explicit marker,
        # treat as FINAL_ANSWER (common with weaker models)
        if query:
            logger.debug("No explicit action found; treating SPARQL block as FINAL_ANSWER.")
            return thought, "FINAL_ANSWER", query

        return thought, "UNKNOWN", ""

    def _extract_thought(self, text: str) -> str:
        m = self._THOUGHT_RE.search(text)
        if m:
            return m.group(1).strip()
        return ""

    def _extract_last_sparql_block(self, text: str) -> str:
        """Returns the last ```sparql ... ``` block (covers multi-step decomp)."""
        matches = self._SPARQL_BLOCK_RE.findall(text)
        if matches:
            return matches[-1].strip()
        # No fenced block: try to find bare SELECT/ASK/CONSTRUCT
        bare = re.search(
            r"((?:PREFIX[^\n]+\n)*\s*(?:SELECT|ASK|CONSTRUCT|DESCRIBE)\s+[\s\S]+)",
            text, re.IGNORECASE
        )
        if bare:
            return bare.group(1).strip()
        return ""


# ---------------------------------------------------------------------------
# Core agent loop
# ---------------------------------------------------------------------------

class AgenticSPARQLRunner:
    """
    Orchestrates the ReAct loop for SPARQL generation.

    Args:
        client:          LLM client (AzureClient / OpenAIClient)
        wikidata_tool:   WikidataTool instance (injected for testability)
        system_prompt:   System prompt to use for every LLM call
        max_steps:       Max reasoning iterations before forced stop
        step_delay:      Seconds to wait between Wikidata calls (rate-limit protection)
    """

    def __init__(
        self,
        client,
        system_prompt: str,
        wikidata_tool: Optional[WikidataTool] = None,
        max_steps: int = 6,
        step_delay: float = 0.5,
    ):
        self.client = client
        self.system_prompt = system_prompt
        self.tool = wikidata_tool or WikidataTool(timeout=8)
        self.max_steps = max_steps
        self.step_delay = step_delay
        self.parser = AgentResponseParser()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
    ) -> AgentResult:
        """
        Runs the full ReAct loop for a single question.

        Returns AgentResult with final SPARQL and step history.
        """
        steps: List[AgentStep] = []
        conversation: List[str] = []  # Accumulated context sent to LLM each step

        # Build the opening prompt (shown only on step 1)
        opening = self._build_initial_prompt(
            question, entities, context_examples, schema_hints
        )
        conversation.append(opening)

        for step_num in range(1, self.max_steps + 1):
            logger.info(f"[Agent] Step {step_num}/{self.max_steps}")

            # --- LLM call --------------------------------------------------
            full_prompt = "\n\n".join(conversation)
            raw_response = await self.client.generate(full_prompt, self.system_prompt)

            # --- Parse response --------------------------------------------
            thought, action, query = self.parser.parse(raw_response)

            logger.info(f"[Agent] Thought: {thought[:120]}")
            logger.info(f"[Agent] Action : {action}")
            if query:
                logger.debug(f"[Agent] Query  : {query[:200]}")

            # --- FINAL_ANSWER branch ---------------------------------------
            if action == "FINAL_ANSWER":
                step = AgentStep(
                    step_number=step_num,
                    thought=thought,
                    action="FINAL_ANSWER",
                    query=query,
                    observation=None,
                    raw_llm_response=raw_response,
                )
                steps.append(step)

                valid, error = self._validate_final_query(query)
                return AgentResult(
                    final_query=query,
                    is_valid=valid,
                    steps=steps,
                    total_steps=step_num,
                    termination_reason="final_answer",
                    validation_error=error,
                )

            # --- EXECUTE_SPARQL branch -------------------------------------
            if action == "EXECUTE_SPARQL" and query:
                # Rate-limit protection
                if self.step_delay > 0:
                    await asyncio.sleep(self.step_delay)

                loop = asyncio.get_event_loop()
                observation = await loop.run_in_executor(
                    None, self.tool.execute, query
                )
                logger.info(f"[Agent] Observation: {observation[:200]}")

                step = AgentStep(
                    step_number=step_num,
                    thought=thought,
                    action="EXECUTE_SPARQL",
                    query=query,
                    observation=observation,
                    raw_llm_response=raw_response,
                )
                steps.append(step)

                # Append this exchange to conversation history
                conversation.append(
                    self._format_exchange(step_num, thought, action, query, observation)
                )
                continue

            # --- UNKNOWN / malformed response ------------------------------
            logger.warning(
                f"[Agent] Step {step_num}: could not parse action from response. "
                "Appending a correction hint."
            )
            step = AgentStep(
                step_number=step_num,
                thought=thought,
                action="UNKNOWN",
                query=query,
                observation=None,
                raw_llm_response=raw_response,
            )
            steps.append(step)

            # Give the model a nudge
            conversation.append(
                f"[SYSTEM] Step {step_num}: Your response did not follow the required format.\n"
                "You MUST respond with either:\n"
                "  THOUGHT: ...\n  ACTION: EXECUTE_SPARQL\n  ```sparql ... ```\n"
                "OR:\n"
                "  THOUGHT: ...\n  FINAL_ANSWER:\n  ```sparql ... ```"
            )

        # --- Max steps reached -------------------------------------------
        logger.warning("[Agent] Max steps reached. Returning best available query.")

        # Try to return the last query we found
        last_query = ""
        for s in reversed(steps):
            if s.query:
                last_query = s.query
                break

        valid, error = self._validate_final_query(last_query) if last_query else (False, "No query generated")

        return AgentResult(
            final_query=last_query,
            is_valid=valid,
            steps=steps,
            total_steps=self.max_steps,
            termination_reason="max_steps",
            validation_error=error,
        )

    # ------------------------------------------------------------------
    # Prompt builders
    # ------------------------------------------------------------------

    def _build_initial_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
    ) -> str:
        parts = []

        parts.append("=== TASK ===")
        parts.append(f"Question: {question}")

        if entities:
            ent_str = ", ".join(
                e.to_sparql_format() if hasattr(e, "to_sparql_format") else str(e)
                for e in entities
            )
            parts.append(f"\nIdentified Entities (may need verification): {ent_str}")

        if schema_hints and schema_hints.strip():
            parts.append(f"\nSchema Hints (candidate properties): {schema_hints}")

        if context_examples and context_examples.strip():
            parts.append("\n=== SIMILAR EXAMPLES ===")
            parts.append(context_examples)

        parts.append("\n=== BEGIN REASONING ===")
        parts.append(
            "Start by verifying entity QIDs and relevant properties using EXECUTE_SPARQL.\n"
            "When you are confident you have the correct IDs and structure, issue FINAL_ANSWER."
        )

        return "\n".join(parts)

    def _format_exchange(
        self,
        step: int,
        thought: str,
        action: str,
        query: str,
        observation: str,
    ) -> str:
        return (
            f"--- Step {step} ---\n"
            f"THOUGHT: {thought}\n"
            f"ACTION: {action}\n"
            f"```sparql\n{query}\n```\n"
            f"OBSERVATION:\n{observation}"
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_final_query(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Quick structural validation: balanced braces + correct start keyword.
        Does NOT execute against Wikidata (that is done by the evaluator).
        """
        if not query or not query.strip():
            return False, "Empty query"

        q = query.strip().upper()
        valid_starts = ("PREFIX", "SELECT", "ASK", "CONSTRUCT", "DESCRIBE")
        if not any(q.startswith(s) for s in valid_starts):
            return False, f"Query must start with one of {valid_starts}"

        # Balanced braces
        count = 0
        for ch in query:
            if ch == "{":
                count += 1
            elif ch == "}":
                count -= 1
            if count < 0:
                return False, "Unbalanced braces (extra closing brace)"
        if count != 0:
            return False, f"Unbalanced braces (open={count})"

        # SELECT/CONSTRUCT must have WHERE
        if q.startswith(("SELECT", "CONSTRUCT")) and "WHERE" not in q:
            return False, "SELECT/CONSTRUCT query missing WHERE clause"

        return True, None

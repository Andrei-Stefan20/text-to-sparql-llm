"""
Agentic SPARQL Generation using ReAct (Reason + Act) pattern.

The agent loop:
  1. Receives: question + entities + context examples + schema hints
  2. Generates: THOUGHT + ACTION (exploratory SPARQL) OR FINAL_ANSWER
  3. If ACTION: executes query on Wikidata → OBSERVATION → continues
  4. If FINAL_ANSWER: validates + returns

Response format the LLM must follow:
─────────────────────────────────────────
THOUGHT: <reasoning>
ACTION: EXECUTE_SPARQL
sparql_start
<exploratory query>
sparql_end
─────────────────────────────────────────
OR:
─────────────────────────────────────────
THOUGHT: <reasoning>
FINAL_ANSWER:
sparql_start
<complete answer query>
sparql_end
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
    action: str  # "EXECUTE_SPARQL" | "FINAL_ANSWER"
    query: str  # The SPARQL issued in this step
    observation: Optional[str]  # Result returned by Wikidata (None for FINAL_ANSWER)
    raw_llm_response: str


@dataclass
class AgentResult:
    """Final result of the agentic run."""

    final_query: str
    is_valid: bool
    steps: List[AgentStep] = field(default_factory=list)
    total_steps: int = 0
    termination_reason: str = ""  # "final_answer" | "max_steps" | "error"
    validation_error: Optional[str] = None


# ---------------------------------------------------------------------------
# Wikidata tool executor
# ---------------------------------------------------------------------------


class WikidataTool:
    """
    Executes exploratory SPARQL queries against Wikidata.
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
    MAX_ROWS_IN_OBSERVATION = 10

    def __init__(self, timeout: int = 8):
        self.timeout = timeout
        self.sparql = SPARQLWrapper(self.ENDPOINT)
        self.sparql.setReturnFormat(JSON)
        self.sparql.addCustomHttpHeader("User-Agent", "AgenticSPARQLBot/1.0")
        self.sparql.setTimeout(timeout)

        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context

    def execute(self, query: str) -> str:
        if not query or not query.strip():
            return "Error: empty query."

        full_query = (
            query if "PREFIX" in query.upper() else self.STANDARD_PREFIXES + query
        )

        try:
            self.sparql.setQuery(full_query)
            raw = self.sparql.query().convert()
            return self._format_results(raw)

        except Exception as exc:
            err = str(exc).split("\n")[0][:200]
            return f"Error executing query: {err}"

    def _format_results(self, raw: Dict) -> str:
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
    Supports both sparql_start/sparql_end markers and backtick blocks.
    """

    _THOUGHT_RE = re.compile(
        r"THOUGHT\s*[:]\s*(.*?)(?=\nACTION|\nFINAL_ANSWER|$)", re.IGNORECASE | re.DOTALL
    )
    _ACTION_RE = re.compile(r"ACTION\s*[:]\s*EXECUTE_SPARQL", re.IGNORECASE)
    _FINAL_RE = re.compile(r"FINAL_ANSWER\s*[:]?", re.IGNORECASE)

    # Supports sparql_start/sparql_end (primary) and backtick blocks (fallback)
    _SPARQL_MARKER_RE = re.compile(
        r"sparql_start\s*([\s\S]*?)\s*sparql_end", re.IGNORECASE
    )
    _SPARQL_BLOCK_RE = re.compile(r"```(?:sparql)?\s*([\s\S]*?)```", re.IGNORECASE)

    def parse(self, response: str) -> Tuple[str, str, str]:
        """
        Returns (thought, action, query).
        action = "EXECUTE_SPARQL" | "FINAL_ANSWER" | "UNKNOWN"
        """
        thought = self._extract_thought(response)
        query = self._extract_sparql(response)

        if self._FINAL_RE.search(response):
            return thought, "FINAL_ANSWER", query

        if self._ACTION_RE.search(response):
            return thought, "EXECUTE_SPARQL", query

        # Fallback: bare SPARQL block with no explicit marker
        if query:
            logger.debug(
                "No explicit action found; treating SPARQL block as FINAL_ANSWER."
            )
            return thought, "FINAL_ANSWER", query

        return thought, "UNKNOWN", ""

    def _extract_thought(self, text: str) -> str:
        m = self._THOUGHT_RE.search(text)
        return m.group(1).strip() if m else ""

    def _extract_sparql(self, text: str) -> str:
        """Try sparql_start/end first, then backtick blocks, then bare SELECT/ASK."""
        # 1. sparql_start / sparql_end markers
        matches = self._SPARQL_MARKER_RE.findall(text)
        if matches:
            return matches[-1].strip()

        # 2. Backtick fenced blocks
        matches = self._SPARQL_BLOCK_RE.findall(text)
        if matches:
            return matches[-1].strip()

        # 3. Bare SELECT/ASK/CONSTRUCT
        bare = re.search(
            r"((?:PREFIX[^\n]+\n)*\s*(?:SELECT|ASK|CONSTRUCT|DESCRIBE)\s+[\s\S]+)",
            text,
            re.IGNORECASE,
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

    The system prompt supports two runtime placeholders resolved before the
    first LLM call so the model always knows its budget:

      {max_steps}           → total steps allowed          (e.g. "5")
      {max_steps_minus_one} → max exploratory steps allowed (e.g. "4")

    At runtime the loop also:
      - Appends how many steps remain after each EXECUTE_SPARQL observation.
      - Injects a hard reminder on the last step so the model cannot emit
        another EXECUTE_SPARQL instead of FINAL_ANSWER.
      - Salvages the query if the model ignores the last-step reminder.
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
    # System prompt — inject runtime values once per run
    # ------------------------------------------------------------------

    def _resolve_system_prompt(self) -> str:
        """
        Replaces {max_steps} and {max_steps_minus_one} placeholders with the
        actual values for this run.

        Example with max_steps=5:
          "You have at most {max_steps} steps."
          → "You have at most 5 steps."
          "Use at most {max_steps_minus_one} exploratory steps."
          → "Use at most 4 exploratory steps."
        """
        return (
            self.system_prompt
            .replace("{max_steps}", str(self.max_steps))
            .replace("{max_steps_minus_one}", str(self.max_steps - 1))
        )

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    async def _check_semantic_correctness(self, generated_query: str, gold_query: str) -> bool:
        """ Executes both generated and gold queries on Wikidata and compares results."""
        try:
            gen_res_raw = self.executor.execute(generated_query)
            gold_res_raw = self.executor.execute(gold_query)
            
            def get_val_set(res):
                if not res or 'results' not in res: return set()
                return {str(row[v]['value']) for row in res['results']['bindings'] for v in row}

            gen_set = get_val_set(gen_res_raw)
            gold_set = get_val_set(gold_res_raw)

            if not gold_set and not gen_set: return True
            
            intersection = gen_set.intersection(gold_set)
            if not gold_set: return not gen_set
            
            recall = len(intersection) / len(gold_set)
            precision = len(intersection) / len(gen_set) if gen_set else 0
            
            return recall == 1.0 and precision == 1.0
        except Exception as e:
            logger.error(f"Error in semantic check: {e}")
            return False

    async def run(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        gold_sparql: Optional[str] = None,
    ) -> AgentResult:
        """Runs the full ReAct loop for a single question."""
        steps: List[AgentStep] = []
        conversation: List[str] = []

        # Resolve {max_steps} placeholders once — reused for every LLM call
        resolved_system_prompt = self._resolve_system_prompt()

        # Opening prompt: clean context only, no instruction-like text
        # (avoids Azure jailbreak filter)
        opening = self._build_initial_prompt(
            question, entities, context_examples, schema_hints
        )
        conversation.append(opening)

        for step_num in range(1, self.max_steps + 1):
            is_last_step = step_num == self.max_steps
            logger.info(
                f"[Agent] Step {step_num}/{self.max_steps}"
                + (" ← LAST STEP, must emit FINAL_ANSWER" if is_last_step else "")
            )

            # Inject a hard reminder on the last step so the model cannot
            # "forget" and waste it on another exploratory query.
            if is_last_step:
                conversation.append(
                    f"[Step budget exhausted: {step_num}/{self.max_steps}] "
                    "You have used all your exploratory steps. "
                    "You MUST now respond with FINAL_ANSWER using the best query "
                    "you have built so far. Do NOT use EXECUTE_SPARQL."
                )

            full_prompt = "\n\n".join(conversation)
            raw_response = await self.client.generate(
                full_prompt, resolved_system_prompt
            )

            thought, action, query = self.parser.parse(raw_response)

            logger.info(f"[Agent] Thought: {thought[:120]}")
            logger.info(f"[Agent] Action : {action}")
            if query:
                logger.debug(f"[Agent] Query  : {query[:200]}")

            # ----------------------------------------------------------
            # FINAL_ANSWER branch
            # ----------------------------------------------------------
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

                is_valid, error = self._validate_final_query(query)

                if is_valid and gold_sparql and step < self.max_steps:
                    is_correct = await self._check_semantic_correctness(query, gold_sparql)
                    
                    if not is_correct:
                        # Feedback all'agente: non uscire, correggi la query!
                        observation = (
                            "OBSERVATION: Pre-check failed. Your query is syntactically correct, "
                            "but the results DO NOT match the expected answer. "
                            f"You have {self.max_steps - step} steps left. "
                            "Please use FORMAT A to test alternative properties (P-IDs) or filters."
                        )
                        conversation.append(
                            self._format_exchange(step, thought, query, observation)
                        )
                        logger.info(f"[Agent] Step {step}: Semantic check failed, retrying...")
                        continue

                return AgentResult(
                    final_query=query,
                    is_valid=is_valid,
                    steps=steps,
                    total_steps=step_num,
                    termination_reason="final_answer",
                    validation_error=error,
                )

            # ----------------------------------------------------------
            # EXECUTE_SPARQL branch
            # ----------------------------------------------------------
            if action == "EXECUTE_SPARQL" and query:

                # Model ignored the last-step reminder — salvage the query
                if is_last_step:
                    logger.warning(
                        "[Agent] Model emitted EXECUTE_SPARQL on last step — "
                        "salvaging query as FINAL_ANSWER."
                    )
                    step = AgentStep(
                        step_number=step_num,
                        thought=thought,
                        action="FINAL_ANSWER",  # override
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
                        termination_reason="max_steps",
                        validation_error=error,
                    )

                # Normal exploratory step
                if self.step_delay > 0:
                    await asyncio.sleep(self.step_delay)

                loop = asyncio.get_event_loop()
                observation = await loop.run_in_executor(None, self.tool.execute, query)
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

                # Tell the model how many steps remain so it can plan ahead
                steps_remaining = self.max_steps - step_num
                remaining_note = (
                    f" ({steps_remaining} step{'s' if steps_remaining != 1 else ''} remaining"
                    + (", next MUST be FINAL_ANSWER" if steps_remaining == 1 else "")
                    + ")"
                )

                conversation.append(
                    self._format_exchange(
                        step_num, thought, query, observation, remaining_note
                    )
                )
                continue

            # ----------------------------------------------------------
            # UNKNOWN / malformed response
            # ----------------------------------------------------------
            logger.warning(f"[Agent] Step {step_num}: could not parse action.")
            step = AgentStep(
                step_number=step_num,
                thought=thought,
                action="UNKNOWN",
                query=query,
                observation=None,
                raw_llm_response=raw_response,
            )
            steps.append(step)

            steps_remaining = self.max_steps - step_num
            conversation.append(
                f"Step {step_num}: format not recognized "
                f"({steps_remaining} step{'s' if steps_remaining != 1 else ''} remaining). "
                "Respond with THOUGHT followed by either "
                "ACTION: EXECUTE_SPARQL with a sparql_start/sparql_end block, "
                "or FINAL_ANSWER: with a sparql_start/sparql_end block."
            )

   
        logger.warning(
            "[Agent] Max steps reached without FINAL_ANSWER. "
            "Returning best available query."
        )
        last_query = next((s.query for s in reversed(steps) if s.query), "")
        valid, error = (
            self._validate_final_query(last_query)
            if last_query
            else (False, "No query generated")
        )

        return AgentResult(
            final_query=last_query,
            is_valid=valid,
            steps=steps,
            total_steps=self.max_steps,
            termination_reason="max_steps",
            validation_error=error,
        )

    # ------------------------------------------------------------------
    # Prompt builders — CLEAN user turns to avoid Azure content filter
    # ------------------------------------------------------------------

    def _build_initial_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
    ) -> str:
        """
        Builds a CLEAN user prompt with just question + context.
        No instruction-like meta-text that could trigger Azure jailbreak filter.
        """
        parts = []

        if schema_hints and schema_hints.strip():
            parts.append(f"Relevant properties: {schema_hints}")

        if entities:
            ent_str = ", ".join(
                e.to_sparql_format() if hasattr(e, "to_sparql_format") else str(e)
                for e in entities
            )
            parts.append(f"Identified entities: {ent_str}")

        if context_examples and context_examples.strip():
            parts.append(f"Similar examples:\n{context_examples}")

        # Question always last
        parts.append(f"Question: {question}")

        return "\n\n".join(parts)

    def _format_exchange(
        self,
        step: int,
        thought: str,
        query: str,
        observation: str,
        remaining_note: str = "",
    ) -> str:
        """Formats a completed exploratory step for the conversation history."""
        return (
            f"Step {step} thought: {thought}\n"
            f"Ran query:\n{query}\n"
            f"Result{remaining_note}:\n{observation}"
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_final_query(self, query: str) -> Tuple[bool, Optional[str]]:
        if not query or not query.strip():
            return False, "Empty query"

        q = query.strip().upper()
        valid_starts = ("PREFIX", "SELECT", "ASK", "CONSTRUCT", "DESCRIBE")
        if not any(q.startswith(s) for s in valid_starts):
            return False, f"Query must start with one of {valid_starts}"

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

        if q.startswith(("SELECT", "CONSTRUCT")) and "WHERE" not in q:
            return False, "SELECT/CONSTRUCT query missing WHERE clause"

        return True, None
"""
Agentic SPARQL Generation using ReAct (Reason + Act) pattern.

System prompt placeholders resolved before the first LLM call:
  {max_steps}           → total step budget (e.g. "8")
  {max_steps_minus_one} → max exploratory steps (e.g. "7")

Runtime enforcement:
  - Steps remaining shown after every EXECUTE_SPARQL observation.
  - Hard reminder injected on the last step.
  - Last-step salvage: if model still emits EXECUTE_SPARQL, the query is
    returned as FINAL_ANSWER instead of being discarded.

"""

import asyncio
import logging
import re
import ssl
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)


# Data classes


@dataclass
class AgentStep:
    step_number: int
    thought: str
    action: str
    query: str
    observation: Optional[str]
    raw_llm_response: str


@dataclass
class AgentResult:
    final_query: str
    is_valid: bool
    steps: List[AgentStep] = field(default_factory=list)
    total_steps: int = 0
    termination_reason: str = ""
    validation_error: Optional[str] = None


# Wikidata tool executor


class WikidataTool:
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


# Response parser


class AgentResponseParser:
    _THOUGHT_RE = re.compile(
        r"THOUGHT\s*[:]\s*(.*?)(?=\nACTION|\nFINAL_ANSWER|$)", re.IGNORECASE | re.DOTALL
    )
    _ACTION_RE = re.compile(r"ACTION\s*[:]\s*EXECUTE_SPARQL", re.IGNORECASE)
    _FINAL_RE = re.compile(r"FINAL_ANSWER\s*[:]?", re.IGNORECASE)
    _SPARQL_MARK_RE = re.compile(
        r"sparql_start\s*([\s\S]*?)\s*sparql_end", re.IGNORECASE
    )
    _SPARQL_BLCK_RE = re.compile(r"```(?:sparql)?\s*([\s\S]*?)```", re.IGNORECASE)

    def parse(self, response: str) -> Tuple[str, str, str]:
        thought = self._extract_thought(response)
        query = self._extract_sparql(response)

        if self._FINAL_RE.search(response):
            return thought, "FINAL_ANSWER", query
        if self._ACTION_RE.search(response):
            return thought, "EXECUTE_SPARQL", query
        if query:
            return thought, "FINAL_ANSWER", query
        return thought, "UNKNOWN", ""

    def _extract_thought(self, text: str) -> str:
        m = self._THOUGHT_RE.search(text)
        return m.group(1).strip() if m else ""

    def _extract_sparql(self, text: str) -> str:
        matches = self._SPARQL_MARK_RE.findall(text)
        if matches:
            return matches[-1].strip()

        matches = self._SPARQL_BLCK_RE.findall(text)
        if matches:
            return matches[-1].strip()

        bare = re.search(
            r"((?:PREFIX[^\n]+\n)*\s*(?:SELECT|ASK|CONSTRUCT|DESCRIBE)\s+[\s\S]+)",
            text,
            re.IGNORECASE,
        )
        if bare:
            return bare.group(1).strip()

        return ""


# Core agent loop


class AgenticSPARQLRunner:
    """
    The ReAct loop for SPARQL generation.
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
        self.tool = wikidata_tool or WikidataTool(timeout=8)  # ← self.tool, always
        self.max_steps = max_steps
        self.step_delay = step_delay
        self.parser = AgentResponseParser()

    # System prompt, inject runtime values once per run

    def _resolve_system_prompt(self) -> str:
        return self.system_prompt.replace("{max_steps}", str(self.max_steps)).replace(
            "{max_steps_minus_one}", str(self.max_steps - 1)
        )

    # Optional semantic dry-run (uses self.tool, not self.executor)

    async def _check_semantic_correctness(
        self, generated_query: str, gold_query: str
    ) -> bool:
        """
        Executes both queries via self.tool and compares result sets.
        Returns True if both return the same values (F1 == 1.0).
        Only triggered when gold_sparql is explicitly passed to run().
        """
        try:
            loop = asyncio.get_event_loop()
            gen_obs = await loop.run_in_executor(
                None, self.tool.execute, generated_query
            )
            gold_obs = await loop.run_in_executor(None, self.tool.execute, gold_query)

            def _parse(obs: str) -> set:
                vals = set()
                for line in obs.splitlines():
                    if "Results (" in line or "---" in line or not line.strip():
                        continue
                    for part in line.split("|"):
                        part = part.strip()
                        if part:
                            vals.add(part)
                return vals

            gen_set = _parse(gen_obs)
            gold_set = _parse(gold_obs)

            if not gold_set and not gen_set:
                return True
            if not gold_set or not gen_set:
                return False

            intersection = gen_set & gold_set
            recall = len(intersection) / len(gold_set)
            precision = len(intersection) / len(gen_set)
            return recall == 1.0 and precision == 1.0

        except Exception as exc:
            logger.debug(f"[Agent] Semantic check error: {exc}")
            return False

    # Main loop

    async def run(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        gold_sparql: Optional[str] = None,
    ) -> AgentResult:
        steps: List[AgentStep] = []
        conversation: List[str] = []

        resolved_system_prompt = self._resolve_system_prompt()

        conversation.append(
            self._build_initial_prompt(
                question, entities, context_examples, schema_hints
            )
        )

        for step_num in range(1, self.max_steps + 1):
            is_last_step = step_num == self.max_steps
            logger.info(
                f"[Agent] Step {step_num}/{self.max_steps}"
                + (" ← LAST STEP, must emit FINAL_ANSWER" if is_last_step else "")
            )

            if is_last_step:
                conversation.append(
                    f"[Step budget exhausted: {step_num}/{self.max_steps}] "
                    "You have used all your exploratory steps. "
                    "You MUST now respond with FINAL_ANSWER. Do NOT use EXECUTE_SPARQL."
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

            # FINAL_ANSWER

            if action == "FINAL_ANSWER":
                step = AgentStep(
                    step_num, thought, "FINAL_ANSWER", query, None, raw_response
                )
                steps.append(step)

                is_valid, error = self._validate_final_query(query)

                # Optional semantic dry-run (only when gold_sparql supplied AND steps left)
                if is_valid and gold_sparql and step_num < self.max_steps:
                    correct = await self._check_semantic_correctness(query, gold_sparql)
                    if not correct:
                        steps_left = self.max_steps - step_num
                        conversation.append(
                            self._format_exchange(
                                step_num,
                                thought,
                                query,
                                f"OBSERVATION: Pre-check failed. Results don't match. "
                                f"{steps_left} step(s) remaining — try a different property.",
                            )
                        )
                        logger.info(
                            f"[Agent] Step {step_num}: semantic check failed, retrying."
                        )
                        steps.pop()
                        continue

                return AgentResult(
                    final_query=query,
                    is_valid=is_valid,
                    steps=steps,
                    total_steps=step_num,
                    termination_reason="final_answer",
                    validation_error=error,
                )

            # EXECUTE_SPARQL

            if action == "EXECUTE_SPARQL" and query:

                # Salvage on last step
                if is_last_step:
                    logger.warning(
                        "[Agent] EXECUTE_SPARQL on last step — salvaging as FINAL_ANSWER."
                    )
                    step = AgentStep(
                        step_num, thought, "FINAL_ANSWER", query, None, raw_response
                    )
                    steps.append(step)
                    valid, error = self._validate_final_query(query)
                    return AgentResult(
                        query, valid, steps, step_num, "max_steps", error
                    )

                if self.step_delay > 0:
                    await asyncio.sleep(self.step_delay)

                loop = asyncio.get_event_loop()
                observation = await loop.run_in_executor(None, self.tool.execute, query)
                logger.info(f"[Agent] Observation: {observation[:200]}")

                step = AgentStep(
                    step_num,
                    thought,
                    "EXECUTE_SPARQL",
                    query,
                    observation,
                    raw_response,
                )
                steps.append(step)

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

            # UNKNOWN

            logger.warning(f"[Agent] Step {step_num}: could not parse action.")
            step = AgentStep(step_num, thought, "UNKNOWN", query, None, raw_response)
            steps.append(step)

            steps_remaining = self.max_steps - step_num
            conversation.append(
                f"Step {step_num}: format not recognized "
                f"({steps_remaining} step{'s' if steps_remaining != 1 else ''} remaining). "
                "Use ACTION: EXECUTE_SPARQL or FINAL_ANSWER: with sparql_start/sparql_end."
            )

        # Safety net
        logger.warning("[Agent] Max steps reached. Returning best available query.")
        last_query = next((s.query for s in reversed(steps) if s.query), "")
        valid, error = (
            self._validate_final_query(last_query)
            if last_query
            else (False, "No query generated")
        )
        return AgentResult(last_query, valid, steps, self.max_steps, "max_steps", error)

    # Prompt builders

    def _build_initial_prompt(
        self, question: str, entities: List, context_examples: str, schema_hints: str
    ) -> str:
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
        return (
            f"Step {step} thought: {thought}\n"
            f"Ran query:\n{query}\n"
            f"Result{remaining_note}:\n{observation}"
        )

    # Validation

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

"""
SPARQL Validation and Self-Correction Module.

This module ensures the validity of SPARQL queries through:
- Syntax validation using `rdflib`.
- Execution validation against Wikidata.
- Self-correction loops with error feedback.
- Self-consistency checks using majority voting.

Implementation:
- Validates queries for syntax errors and execution correctness.
- Provides detailed error feedback for self-correction.
- Uses `ValidationResult` to encapsulate validation outcomes.
"""

import asyncio
import logging
import os
import re
import ssl
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper

# compare_results is a utility shared with the evaluation module
from src.evaluation.metrics import compare_results

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of SPARQL validation."""

    is_valid: bool
    error_type: Optional[str] = None  # "syntax", "execution", "timeout", "empty"
    error_message: Optional[str] = None
    results_count: Optional[int] = None

    def __bool__(self):
        return self.is_valid


@dataclass
class GenerationAttempt:
    """Records a single generation attempt."""

    query: str
    validation: ValidationResult
    attempt_number: int
    error_feedback_used: Optional[str] = None


@dataclass
class CorrectionResult:
    """Result of the self-correction process."""

    final_query: str
    is_valid: bool
    attempts: List[GenerationAttempt] = field(default_factory=list)
    total_attempts: int = 0
    correction_method: str = "none"  # "none", "self_correction", "self_consistency"


class SPARQLValidator:
    """
    Validates SPARQL queries syntactically and semantically.
    """

    WIKIDATA_ENDPOINT = os.getenv(
        "SPARQL_ENDPOINT_URL", "https://query.wikidata.org/sparql"
    )

    # Common Wikidata prefixes that should be auto-added if missing
    STANDARD_PREFIXES = """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """

    def __init__(self, timeout: int = 10, validate_execution: bool = True):
        self.timeout = timeout
        self.execution_enabled = validate_execution

        # Setup SPARQL wrapper
        self.sparql = SPARQLWrapper(self.WIKIDATA_ENDPOINT)
        self.sparql.setReturnFormat(JSON)
        self.sparql.addCustomHttpHeader("User-Agent", "TextToSparqlValidator/1.0")
        self.sparql.setTimeout(timeout)

        # Handle SSL issues
        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context

    def validate_syntax(self, query: str) -> ValidationResult:
        """
        Validates SPARQL syntax using rdflib.
        """
        if not query or not query.strip():
            return ValidationResult(
                is_valid=False, error_type="syntax", error_message="Empty query"
            )

        try:
            from rdflib import Namespace
            from rdflib.plugins.sparql import prepareQuery

            full_query = self._ensure_prefixes(query)

            namespaces = {
                "wd": Namespace("http://www.wikidata.org/entity/"),
                "wdt": Namespace("http://www.wikidata.org/prop/direct/"),
                "p": Namespace("http://www.wikidata.org/prop/"),
                "ps": Namespace("http://www.wikidata.org/prop/statement/"),
                "pq": Namespace("http://www.wikidata.org/prop/qualifier/"),
                "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
                "bd": Namespace("http://www.bigdata.com/rdf#"),
                "wikibase": Namespace("http://wikiba.se/ontology#"),
            }

            prepareQuery(full_query, initNs=namespaces)
            return ValidationResult(is_valid=True)

        except Exception as e:
            clean_error = self._clean_error_message(str(e))
            return ValidationResult(
                is_valid=False, error_type="syntax", error_message=clean_error
            )

    def validate_execution(self, query: str) -> ValidationResult:
        """
        Validates by actually executing the query against Wikidata.
        """
        if not query or not query.strip():
            return ValidationResult(
                is_valid=False, error_type="syntax", error_message="Empty query"
            )

        try:
            full_query = self._ensure_prefixes(query)
            self.sparql.setQuery(full_query)

            results = self.sparql.query().convert()
            bindings = results.get("results", {}).get("bindings", [])
            count = len(bindings)

            if count == 0:
                return ValidationResult(
                    is_valid=True,
                    error_type="empty",
                    error_message="Query returned no results",
                    results_count=0,
                )

            return ValidationResult(is_valid=True, results_count=count)

        except Exception as e:
            error_msg = str(e)

            if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                error_type = "timeout"
            elif "syntax" in error_msg.lower() or "parse" in error_msg.lower():
                error_type = "syntax"
            else:
                error_type = "execution"

            clean_error = self._clean_error_message(error_msg)
            return ValidationResult(
                is_valid=False, error_type=error_type, error_message=clean_error
            )

    def validate_semantic(self, generated_query: str, gold_query: str) -> bool:
        """
        Compares execution results of generated vs gold query.
        Uses SPARQLWrapper (no external requests dependency).
        Returns True if F1 == 1.0 (exact match on result sets).
        """

        def _get_results(q: str) -> list:
            try:
                wrapper = SPARQLWrapper(self.WIKIDATA_ENDPOINT)
                wrapper.setReturnFormat(JSON)
                wrapper.addCustomHttpHeader("User-Agent", "TextToSparqlValidator/1.0")
                wrapper.setTimeout(self.timeout)
                if hasattr(ssl, "_create_unverified_context"):
                    ssl._create_default_https_context = ssl._create_unverified_context
                wrapper.setQuery(self._ensure_prefixes(q))
                data = wrapper.query().convert()
                bindings = data.get("results", {}).get("bindings", [])
                return [row[v]["value"] for row in bindings for v in row]
            except Exception as ex:
                logger.debug(f"validate_semantic query error: {ex}")
                return []

        gen_res = _get_results(generated_query)
        gold_res = _get_results(gold_query)

        f1, _, _ = compare_results(gen_res, gold_res)
        return f1 == 1.0

    def validate(self, query: str, check_execution: bool = None) -> ValidationResult:
        """
        Full validation: syntax first, then optionally execution.
        """
        syntax_result = self.validate_syntax(query)
        if not syntax_result.is_valid:
            return syntax_result

        should_execute = (
            check_execution if check_execution is not None else self.execution_enabled
        )
        if should_execute:
            return self.validate_execution(query)

        return syntax_result

    def _ensure_prefixes(self, query: str) -> str:
        """Adds missing standard prefixes to query."""
        query_upper = query.upper()

        if "PREFIX" in query_upper:
            return query

        needs_prefixes = any(
            prefix in query
            for prefix in [
                "wd:",
                "wdt:",
                "p:",
                "ps:",
                "pq:",
                "rdfs:",
                "bd:",
                "wikibase:",
            ]
        )

        if needs_prefixes:
            return self.STANDARD_PREFIXES + "\n" + query

        return query

    def _clean_error_message(self, error: str) -> str:
        """Cleans error message for use as feedback."""
        if "Traceback" in error:
            error = error.split("Traceback")[0]

        error = re.sub(r"http://[^\s>]+", "<URI>", error)

        if len(error) > 300:
            error = error[:300] + "..."

        return error.strip()


class SelfCorrectionLoop:
    """
    Implements self-correction with error feedback and self-consistency.
    """

    def __init__(
        self,
        client,
        prompt_builder,
        validator: SPARQLValidator = None,
        max_attempts: int = 3,
        self_consistency_samples: int = 1,
        temperature_for_consistency: float = 0.7,
    ):
        self.client = client
        self.prompt_builder = prompt_builder
        self.validator = validator or SPARQLValidator()
        self.max_attempts = max_attempts
        self.self_consistency_samples = self_consistency_samples
        self.temperature_for_consistency = temperature_for_consistency

    async def generate_with_correction(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        system_prompt: str = None,
    ) -> CorrectionResult:
        if self.self_consistency_samples > 1:
            return await self._generate_with_self_consistency(
                question, entities, context_examples, schema_hints, system_prompt
            )

        return await self._generate_with_correction_loop(
            question, entities, context_examples, schema_hints, system_prompt
        )

    async def _generate_with_correction_loop(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        system_prompt: str = None,
        error_history: List[str] = None,
    ) -> CorrectionResult:
        attempts = []
        conversation_history = []

        for attempt_num in range(1, self.max_attempts + 1):
            if attempt_num == 1:
                user_prompt = self.prompt_builder.build_user_prompt(
                    question, entities, context_examples, schema_hints
                )
            else:
                user_prompt = self._build_multiturn_correction_prompt(
                    question,
                    entities,
                    context_examples,
                    schema_hints,
                    conversation_history,
                )

            raw_response = await self.client.generate(user_prompt, system_prompt)
            query = self.prompt_builder.extract_sparql_from_response(
                raw_response, validate_syntax=True
            )
            validation = self.validator.validate(query)

            turn = {
                "attempt": attempt_num,
                "query": query,
                "validation": validation,
                "raw_response": raw_response[:500],
            }
            conversation_history.append(turn)

            attempt = GenerationAttempt(
                query=query,
                validation=validation,
                attempt_number=attempt_num,
                error_feedback_used=(
                    validation.error_message if validation.error_message else None
                ),
            )
            attempts.append(attempt)

            should_stop, correction_method = self._should_stop_correction(
                validation, attempt_num, attempts
            )

            if should_stop:
                return CorrectionResult(
                    final_query=query,
                    is_valid=validation.is_valid,
                    attempts=attempts,
                    total_attempts=attempt_num,
                    correction_method=correction_method,
                )

            logger.info(
                f"Attempt {attempt_num}/{self.max_attempts}: "
                f"{validation.error_type or 'valid'} - "
                f"{'empty results' if validation.error_type == 'empty' else (validation.error_message[:80] if validation.error_message else 'success')}"
            )

            if (
                validation.is_valid
                and validation.error_type == "empty"
                and attempt_num < self.max_attempts
            ):
                logger.info(
                    "Query valid but returned no results. Attempting result-based refinement..."
                )

        best = self._select_best_attempt(attempts)
        return CorrectionResult(
            final_query=best.query,
            is_valid=best.validation.is_valid,
            attempts=attempts,
            total_attempts=len(attempts),
            correction_method="self_correction_multiturn",
        )

    async def _generate_with_self_consistency(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        system_prompt: str = None,
    ) -> CorrectionResult:
        all_attempts = []
        valid_queries = []

        tasks = [
            self._generate_single_sample(
                question, entities, context_examples, schema_hints, system_prompt, i
            )
            for i in range(self.self_consistency_samples)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Sample {i} failed with exception: {result}")
                continue

            query, validation = result
            attempt = GenerationAttempt(
                query=query, validation=validation, attempt_number=i + 1
            )
            all_attempts.append(attempt)

            if validation.is_valid:
                valid_queries.append(query)

        if valid_queries:
            normalized = [self._normalize_query(q) for q in valid_queries]
            counter = Counter(normalized)
            most_common_normalized, vote_count = counter.most_common(1)[0]

            winner = next(
                q
                for q in valid_queries
                if self._normalize_query(q) == most_common_normalized
            )

            logger.info(
                f"Self-consistency: {len(valid_queries)}/{self.self_consistency_samples} valid, "
                f"winner has {vote_count} votes"
            )

            return CorrectionResult(
                final_query=winner,
                is_valid=True,
                attempts=all_attempts,
                total_attempts=len(all_attempts),
                correction_method="self_consistency",
            )

        if all_attempts:
            correction_result = await self._generate_with_correction_loop(
                question, entities, context_examples, schema_hints, system_prompt
            )
            correction_result.correction_method = "self_consistency+correction"
            return correction_result

        return CorrectionResult(
            final_query="",
            is_valid=False,
            attempts=all_attempts,
            total_attempts=len(all_attempts),
            correction_method="self_consistency",
        )

    async def _generate_single_sample(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        system_prompt: str,
        sample_index: int,
    ) -> Tuple[str, ValidationResult]:
        user_prompt = self.prompt_builder.build_user_prompt(
            question, entities, context_examples, schema_hints
        )

        if sample_index > 0 and hasattr(self.client, "temperature"):
            original_temp = self.client.temperature
            self.client.temperature = self.temperature_for_consistency

        try:
            raw_response = await self.client.generate(user_prompt, system_prompt)
            query = self.prompt_builder.extract_sparql_from_response(
                raw_response, validate_syntax=True
            )
            validation = self.validator.validate(query)
            return query, validation
        finally:
            if sample_index > 0 and hasattr(self.client, "temperature"):
                self.client.temperature = original_temp

    def _build_multiturn_correction_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        conversation_history: List[Dict],
    ) -> str:
        parts = []

        if schema_hints:
            parts.append(f"Available Properties: {schema_hints}")

        if entities:
            formatted = self.prompt_builder._format_entities(entities)
            parts.append(f"Entities: {formatted}")

        if context_examples:
            parts.append(f"Examples:\n{context_examples}")

        parts.append(f"\nQuestion: {question}")
        parts.append("\n=== PREVIOUS ATTEMPTS (CONVERSATION HISTORY) ===")

        for turn in conversation_history:
            attempt_num = turn["attempt"]
            query = turn["query"]
            validation = turn["validation"]

            parts.append(f"\n--- Attempt {attempt_num} ---")
            parts.append(f"Query:\n```sparql\n{query}\n```")

            if validation.is_valid:
                if validation.error_type == "empty":
                    parts.append(f"Result: ✓ Valid but returned 0 results (empty)")
                    parts.append(
                        "Issue: Consider wrong QID/P-ID or overly restrictive constraints."
                    )
                else:
                    parts.append(
                        f"Result: ✓ Valid ({validation.results_count or 0} results)"
                    )
            else:
                parts.append(f"Result: ✗ {validation.error_type.upper()} ERROR")
                parts.append(f"Error: {validation.error_message}")

        parts.append(f"\n=== ATTEMPT {len(conversation_history) + 1} ===")
        parts.append("Generate a corrected SPARQL query based on the history above.")

        last_validation = conversation_history[-1]["validation"]
        if last_validation.error_type == "syntax":
            parts.append(
                "\nFocus on: SYNTAX — Check brackets, keywords, PREFIX declarations"
            )
        elif last_validation.error_type == "execution":
            parts.append(
                "\nFocus on: EXECUTION — Verify entity/property IDs exist in Wikidata"
            )
        elif last_validation.error_type == "empty":
            parts.append(
                "\nFocus on: RESULTS — Query is valid but too restrictive or uses wrong IDs"
            )
        elif last_validation.error_type == "timeout":
            parts.append(
                "\nFocus on: PERFORMANCE — Simplify query, add more specific constraints"
            )

        parts.append("\nOutput ONLY the corrected SPARQL query:")
        return "\n".join(parts)

    def _should_stop_correction(
        self,
        validation: ValidationResult,
        attempt_num: int,
        attempts: List[GenerationAttempt],
    ) -> Tuple[bool, str]:
        if validation.is_valid and validation.error_type != "empty":
            method = "self_correction" if attempt_num > 1 else "none"
            return True, method

        if attempt_num >= self.max_attempts:
            return True, "self_correction_exhausted"

        return False, ""

    def _select_best_attempt(
        self, attempts: List[GenerationAttempt]
    ) -> GenerationAttempt:
        perfect = [
            a
            for a in attempts
            if a.validation.is_valid and a.validation.error_type != "empty"
        ]
        if perfect:
            return perfect[-1]

        valid_empty = [
            a
            for a in attempts
            if a.validation.is_valid and a.validation.error_type == "empty"
        ]
        if valid_empty:
            return valid_empty[-1]

        return min(attempts, key=lambda a: self._error_severity(a.validation))

    def _normalize_query(self, query: str) -> str:
        if not query:
            return ""
        normalized = " ".join(query.split())
        normalized = normalized.lower()
        normalized = re.sub(r"#[^\n]*", "", normalized)
        return normalized.strip()

    def _error_severity(self, validation: ValidationResult) -> int:
        if validation.is_valid:
            return 1 if validation.error_type == "empty" else 0
        return {"timeout": 2, "execution": 3, "syntax": 4}.get(validation.error_type, 5)

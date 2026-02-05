"""
SPARQL Validation and Self-Correction Module.

Provides:
- Syntax validation using rdflib
- Execution validation against Wikidata
- Self-correction loop with error feedback
- Self-consistency with majority voting
"""

import asyncio
import logging
import re
import ssl
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper

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
    
    WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
    
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
        self.validate_execution = validate_execution
        
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
        
        Returns:
            ValidationResult with syntax check status
        """
        if not query or not query.strip():
            return ValidationResult(
                is_valid=False,
                error_type="syntax",
                error_message="Empty query"
            )
        
        try:
            from rdflib.plugins.sparql import prepareQuery
            from rdflib import Namespace
            
            # Add standard prefixes if missing
            full_query = self._ensure_prefixes(query)
            
            # Define namespaces for validation
            namespaces = {
                'wd': Namespace('http://www.wikidata.org/entity/'),
                'wdt': Namespace('http://www.wikidata.org/prop/direct/'),
                'p': Namespace('http://www.wikidata.org/prop/'),
                'ps': Namespace('http://www.wikidata.org/prop/statement/'),
                'pq': Namespace('http://www.wikidata.org/prop/qualifier/'),
                'rdfs': Namespace('http://www.w3.org/2000/01/rdf-schema#'),
                'bd': Namespace('http://www.bigdata.com/rdf#'),
                'wikibase': Namespace('http://wikiba.se/ontology#'),
            }
            
            prepareQuery(full_query, initNs=namespaces)
            return ValidationResult(is_valid=True)
            
        except Exception as e:
            error_msg = str(e)
            # Clean up error message for feedback
            clean_error = self._clean_error_message(error_msg)
            
            return ValidationResult(
                is_valid=False,
                error_type="syntax",
                error_message=clean_error
            )
    
    def validate_execution(self, query: str) -> ValidationResult:
        """
        Validates by actually executing the query against Wikidata.
        
        Returns:
            ValidationResult with execution status and result count
        """
        if not query or not query.strip():
            return ValidationResult(
                is_valid=False,
                error_type="syntax", 
                error_message="Empty query"
            )
        
        try:
            full_query = self._ensure_prefixes(query)
            self.sparql.setQuery(full_query)
            
            results = self.sparql.query().convert()
            
            # Count results
            bindings = results.get("results", {}).get("bindings", [])
            count = len(bindings)
            
            # Check for empty results (might indicate wrong query)
            if count == 0:
                return ValidationResult(
                    is_valid=True,  # Syntactically valid but no results
                    error_type="empty",
                    error_message="Query returned no results",
                    results_count=0
                )
            
            return ValidationResult(
                is_valid=True,
                results_count=count
            )
            
        except Exception as e:
            error_msg = str(e)
            
            # Categorize error type
            if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                error_type = "timeout"
            elif "syntax" in error_msg.lower() or "parse" in error_msg.lower():
                error_type = "syntax"
            else:
                error_type = "execution"
            
            clean_error = self._clean_error_message(error_msg)
            
            return ValidationResult(
                is_valid=False,
                error_type=error_type,
                error_message=clean_error
            )
    
    def validate(self, query: str, check_execution: bool = None) -> ValidationResult:
        """
        Full validation: syntax first, then optionally execution.
        
        Args:
            query: SPARQL query to validate
            check_execution: Override instance setting for execution check
            
        Returns:
            ValidationResult with full validation status
        """
        # First check syntax
        syntax_result = self.validate_syntax(query)
        if not syntax_result.is_valid:
            return syntax_result
        
        # Optionally check execution
        should_execute = check_execution if check_execution is not None else self.validate_execution
        if should_execute:
            return self.validate_execution(query)
        
        return syntax_result
    
    def _ensure_prefixes(self, query: str) -> str:
        """Adds missing standard prefixes to query."""
        query_upper = query.upper()
        
        # Check if query already has PREFIX declarations
        if "PREFIX" in query_upper:
            return query
        
        # Check if query uses common prefixes without declaring them
        needs_prefixes = any(
            prefix in query 
            for prefix in ["wd:", "wdt:", "p:", "ps:", "pq:", "rdfs:", "bd:", "wikibase:"]
        )
        
        if needs_prefixes:
            return self.STANDARD_PREFIXES + "\n" + query
        
        return query
    
    def _clean_error_message(self, error: str) -> str:
        """Cleans error message for use as feedback."""
        # Remove stack traces
        if "Traceback" in error:
            error = error.split("Traceback")[0]
        
        # Remove long URIs
        error = re.sub(r'http://[^\s>]+', '<URI>', error)
        
        # Truncate if too long
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
        """
        Args:
            client: LLM client for generation
            prompt_builder: PromptBuilder instance
            validator: SPARQLValidator instance (created if None)
            max_attempts: Maximum correction attempts per sample
            self_consistency_samples: Number of samples for self-consistency (1 = disabled)
            temperature_for_consistency: Temperature for generating diverse samples
        """
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
        """
        Generates SPARQL with validation and self-correction.
        
        Flow:
        1. Generate initial query
        2. Validate (syntax + optional execution)
        3. If invalid, retry with error feedback
        4. Repeat until valid or max_attempts reached
        5. If self_consistency_samples > 1, generate multiple and vote
        
        Returns:
            CorrectionResult with final query and attempt history
        """
        
        # Self-consistency mode: generate multiple samples
        if self.self_consistency_samples > 1:
            return await self._generate_with_self_consistency(
                question, entities, context_examples, schema_hints, system_prompt
            )
        
        # Single generation with correction loop
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
        """Single generation with multi-turn conversational correction."""
        
        attempts = []
        conversation_history = []  # Track all exchanges
        
        for attempt_num in range(1, self.max_attempts + 1):
            # Build prompt with full conversation history (multi-turn)
            if attempt_num == 1:
                # First attempt: standard prompt
                user_prompt = self.prompt_builder.build_user_prompt(
                    question, entities, context_examples, schema_hints
                )
            else:
                # Subsequent attempts: include all previous attempts in conversation
                user_prompt = self._build_multiturn_correction_prompt(
                    question, entities, context_examples, schema_hints,
                    conversation_history
                )
            
            # Generate
            raw_response = await self.client.generate(user_prompt, system_prompt)
            query = self.prompt_builder.extract_sparql_from_response(raw_response, validate_syntax=True)
            
            # Validate
            validation = self.validator.validate(query)
            
            # Record this turn in conversation history
            turn = {
                "attempt": attempt_num,
                "query": query,
                "validation": validation,
                "raw_response": raw_response[:500]  # Truncate for memory
            }
            conversation_history.append(turn)
            
            attempt = GenerationAttempt(
                query=query,
                validation=validation,
                attempt_number=attempt_num,
                error_feedback_used=validation.error_message if validation.error_message else None
            )
            attempts.append(attempt)
            
            # Check if we should continue or stop
            should_stop, correction_method = self._should_stop_correction(
                validation, attempt_num, attempts
            )
            
            if should_stop:
                return CorrectionResult(
                    final_query=query,
                    is_valid=validation.is_valid,
                    attempts=attempts,
                    total_attempts=attempt_num,
                    correction_method=correction_method
                )
            
            # Log progress
            logger.info(
                f"Attempt {attempt_num}/{self.max_attempts}: "
                f"{validation.error_type or 'valid'} - "
                f"{'empty results' if validation.error_type == 'empty' else validation.error_message[:80] if validation.error_message else 'success'}"
            )
            
            # Special case: if syntactically valid but empty results, try result-based refinement
            if validation.is_valid and validation.error_type == "empty" and attempt_num < self.max_attempts:
                logger.info("Query valid but returned no results. Attempting result-based refinement...")
        
        # All attempts exhausted, return best effort
        best = self._select_best_attempt(attempts)
        
        return CorrectionResult(
            final_query=best.query,
            is_valid=best.validation.is_valid,
            attempts=attempts,
            total_attempts=len(attempts),
            correction_method="self_correction_multiturn"
        )
    
    async def _generate_with_self_consistency(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        system_prompt: str = None,
    ) -> CorrectionResult:
        """
        Self-consistency: generate N samples, validate each, vote on best.
        """
        all_attempts = []
        valid_queries = []
        
        # Generate N samples concurrently
        tasks = []
        for i in range(self.self_consistency_samples):
            task = self._generate_single_sample(
                question, entities, context_examples, schema_hints, 
                system_prompt, sample_index=i
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Sample {i} failed with exception: {result}")
                continue
            
            query, validation = result
            attempt = GenerationAttempt(
                query=query,
                validation=validation,
                attempt_number=i + 1
            )
            all_attempts.append(attempt)
            
            if validation.is_valid:
                valid_queries.append(query)
        
        # Voting: select most common valid query
        if valid_queries:
            # Normalize queries for comparison
            normalized = [self._normalize_query(q) for q in valid_queries]
            counter = Counter(normalized)
            most_common_normalized, vote_count = counter.most_common(1)[0]
            
            # Find original query matching the normalized winner
            for q in valid_queries:
                if self._normalize_query(q) == most_common_normalized:
                    winner = q
                    break
            
            logger.info(
                f"Self-consistency: {len(valid_queries)}/{self.self_consistency_samples} valid, "
                f"winner has {vote_count} votes"
            )
            
            return CorrectionResult(
                final_query=winner,
                is_valid=True,
                attempts=all_attempts,
                total_attempts=len(all_attempts),
                correction_method="self_consistency"
            )
        
        # No valid queries, try correction on best attempt
        if all_attempts:
            # Pick the one with least severe error
            best = min(all_attempts, key=lambda a: self._error_severity(a.validation))
            
            # Try one correction loop on the best
            correction_result = await self._generate_with_correction_loop(
                question, entities, context_examples, schema_hints, system_prompt
            )
            correction_result.correction_method = "self_consistency+correction"
            return correction_result
        
        # Complete failure
        return CorrectionResult(
            final_query="",
            is_valid=False,
            attempts=all_attempts,
            total_attempts=len(all_attempts),
            correction_method="self_consistency"
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
        """Generates a single sample for self-consistency."""
        user_prompt = self.prompt_builder.build_user_prompt(
            question, entities, context_examples, schema_hints
        )
        
        # Use higher temperature for diversity (except first sample)
        if sample_index > 0 and hasattr(self.client, 'temperature'):
            original_temp = self.client.temperature
            self.client.temperature = self.temperature_for_consistency
        
        try:
            raw_response = await self.client.generate(user_prompt, system_prompt)
            query = self.prompt_builder.extract_sparql_from_response(raw_response, validate_syntax=True)
            validation = self.validator.validate(query)
            return query, validation
        finally:
            # Restore temperature
            if sample_index > 0 and hasattr(self.client, 'temperature'):
                self.client.temperature = original_temp
    
    def _build_correction_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        error_message: str,
        failed_query: str,
    ) -> str:
        """Builds a prompt with error feedback for correction (single attempt view)."""
        
        parts = []
        
        # Context
        if schema_hints:
            parts.append(f"Available Properties: {schema_hints}")
        
        if entities:
            formatted = self.prompt_builder._format_entities(entities)
            parts.append(f"Entities: {formatted}")
        
        if context_examples:
            parts.append(f"Examples:\n{context_examples}")
        
        # Question
        parts.append(f"\nQuestion: {question}")
        
        # Error feedback section
        parts.append("\n=== PREVIOUS ATTEMPT FAILED ===")
        parts.append(f"Failed Query:\n```sparql\n{failed_query}\n```")
        parts.append(f"\nError: {error_message}")
        parts.append("\n=== CORRECTION REQUIRED ===")
        parts.append("Fix the error and generate a correct SPARQL query.")
        parts.append("Output ONLY the corrected SPARQL query:")
        
        return "\n".join(parts)
    
    def _build_multiturn_correction_prompt(
        self,
        question: str,
        entities: List,
        context_examples: str,
        schema_hints: str,
        conversation_history: List[Dict],
    ) -> str:
        """Builds a multi-turn conversational prompt showing ALL previous attempts."""
        
        parts = []
        
        # Context (shown once at top)
        if schema_hints:
            parts.append(f"Available Properties: {schema_hints}")
        
        if entities:
            formatted = self.prompt_builder._format_entities(entities)
            parts.append(f"Entities: {formatted}")
        
        if context_examples:
            parts.append(f"Examples:\n{context_examples}")
        
        # Question
        parts.append(f"\nQuestion: {question}")
        
        # Conversation history - show all previous attempts
        parts.append("\n=== PREVIOUS ATTEMPTS (CONVERSATION HISTORY) ===")
        
        for turn in conversation_history:
            attempt_num = turn["attempt"]
            query = turn["query"]
            validation = turn["validation"]
            
            parts.append(f"\n--- Attempt {attempt_num} ---")
            parts.append(f"Query:\n```sparql\n{query}\n```")
            
            if validation.is_valid:
                if validation.error_type == "empty":
                    parts.append(f"Result: ✓ Syntactically valid but returned {validation.results_count or 0} results (empty)")
                    parts.append("Issue: Query is correct but returns no data. Consider:")
                    parts.append("  - Are entity IDs correct?")
                    parts.append("  - Are property IDs correct?")
                    parts.append("  - Is the query too restrictive?")
                    parts.append("  - Try using OPTIONAL for some constraints")
                else:
                    parts.append(f"Result: ✓ Valid ({validation.results_count or 0} results)")
            else:
                parts.append(f"Result: ✗ {validation.error_type.upper()} ERROR")
                parts.append(f"Error: {validation.error_message}")
        
        # Current attempt instruction
        parts.append(f"\n=== ATTEMPT {len(conversation_history) + 1} ===")
        parts.append("Based on the conversation history above, generate a corrected SPARQL query.")
        parts.append("Learn from ALL previous errors and results.")
        
        # Special guidance based on last error type
        last_turn = conversation_history[-1]
        last_validation = last_turn["validation"]
        
        if last_validation.error_type == "syntax":
            parts.append("\nFocus on: SYNTAX - Check brackets, keywords, PREFIX declarations")
        elif last_validation.error_type == "execution":
            parts.append("\nFocus on: EXECUTION - Verify entity/property IDs exist in Wikidata")
        elif last_validation.error_type == "empty":
            parts.append("\nFocus on: RESULTS - Query is valid but too restrictive or uses wrong IDs")
        elif last_validation.error_type == "timeout":
            parts.append("\nFocus on: PERFORMANCE - Simplify query, add more specific constraints")
        
        parts.append("\nOutput ONLY the corrected SPARQL query:")
        
        return "\n".join(parts)
    
    def _should_stop_correction(
        self,
        validation: ValidationResult,
        attempt_num: int,
        attempts: List[GenerationAttempt]
    ) -> Tuple[bool, str]:
        """Determines if correction loop should stop.
        
        Returns:
            (should_stop, correction_method)
        """
        # Stop if perfectly valid (not empty)
        if validation.is_valid and validation.error_type != "empty":
            method = "self_correction" if attempt_num > 1 else "none"
            return True, method
        
        # Stop if max attempts reached
        if attempt_num >= self.max_attempts:
            return True, "self_correction_exhausted"
        
        # Continue for all other cases (syntax error, execution error, empty results)
        return False, ""
    
    def _select_best_attempt(self, attempts: List[GenerationAttempt]) -> GenerationAttempt:
        """Selects the best attempt from all tried.
        
        Priority:
        1. Valid with results
        2. Valid with empty results (syntactically correct)
        3. Least severe error
        """
        # Try to find perfectly valid
        perfect = [a for a in attempts if a.validation.is_valid and a.validation.error_type != "empty"]
        if perfect:
            return perfect[-1]  # Return latest perfect
        
        # Try to find valid but empty
        valid_empty = [a for a in attempts if a.validation.is_valid and a.validation.error_type == "empty"]
        if valid_empty:
            return valid_empty[-1]
        
        # Return least severe error
        return min(attempts, key=lambda a: self._error_severity(a.validation))
    
    def _normalize_query(self, query: str) -> str:
        """Normalizes a query for comparison in voting."""
        if not query:
            return ""
        
        # Remove whitespace variations
        normalized = " ".join(query.split())
        
        # Lowercase (SPARQL keywords are case-insensitive)
        normalized = normalized.lower()
        
        # Remove comments
        normalized = re.sub(r'#[^\n]*', '', normalized)
        
        return normalized.strip()
    
    def _error_severity(self, validation: ValidationResult) -> int:
        """Returns severity score for error (lower = better)."""
        if validation.is_valid:
            if validation.error_type == "empty":
                return 1  # Valid but empty
            return 0  # Perfect
        
        severity_map = {
            "timeout": 2,
            "execution": 3,
            "syntax": 4,
        }
        return severity_map.get(validation.error_type, 5)

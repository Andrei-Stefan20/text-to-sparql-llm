import logging
import re
import time
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)


class SPARQLClient:
    """Handles SPARQL query validation and execution against Wikidata endpoint."""

    def __init__(
        self,
        endpoint_url: str = "https://query.wikidata.org/sparql",
        user_agent: str = "TextToSparqlBot/1.0",
        timeout: int = 60,
    ):
        self.endpoint = SPARQLWrapper(endpoint_url)
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", user_agent)
        self.endpoint.setTimeout(timeout)
        self.request_count = 0
        self.last_request_time = None
        self.min_request_interval = 0.5  # Rate limiting: min 0.5s between requests

    def _rate_limit(self) -> None:
        """Apply rate limiting to avoid overwhelming Wikidata."""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_request_interval:
                time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    @contextmanager
    def timed_query(self, query_type: str = "query"):
        """Context manager for query timing and monitoring."""
        start_time = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start_time
            logger.debug(f"{query_type} took {elapsed:.2f}s")
            self.request_count += 1

    def clean_query(self, query_text: str) -> str:
        """Extracts and normalizes SPARQL query from LLM output."""
        if not query_text:
            return ""

        q = query_text.strip()
        if "```" in q:
            pattern = r"```(?:sparql)?(.*?)```"
            match = re.search(pattern, q, re.DOTALL)
            if match:
                q = match.group(1)

        q = q.strip()
        q = re.sub(r"PREF[A-Z]*\s", "PREFIX ", q, flags=re.IGNORECASE)
        q = re.sub(r"wd:\?(\w+)", r"?\1", q)
        return q

    def validate_syntax_local(self, query: str) -> Dict[str, Any]:
        """Validates SPARQL syntax using local parser."""
        if not query:
            return {
                "valid": False,
                "type": "Empty Output",
                "detail": "No query generated",
            }

        if not isinstance(query, str):
            return {
                "valid": False,
                "type": "Type Error",
                "detail": f"Expected str, got {type(query).__name__}",
            }

        try:
            from pyparsing import ParseException
            from rdflib.plugins.sparql.parser import parseQuery

            parseQuery(query)
            return {"valid": True, "type": None, "detail": None}
        except ImportError:
            logger.warning("rdflib not available, skipping syntax check")
            return {"valid": True, "type": None, "detail": "Syntax validation skipped"}
        except ParseException as e:
            return {
                "valid": False,
                "type": "Syntax Error",
                "detail": f"Line {e.lineno}: {str(e)[:100]}",
            }
        except Exception as e:
            return {"valid": False, "type": type(e).__name__, "detail": str(e)[:100]}

    def execute_remote(
        self, query: str, timeout_override: Optional[int] = None
    ) -> Tuple[Optional[List], Optional[str]]:
        """
        Executes SPARQL query against remote endpoint with error handling.

        Args:
            query: SPARQL query string to execute
            timeout_override: Optional timeout override (seconds)

        Returns:
            Tuple of (results list, error message)
        """
        if not query or not isinstance(query, str):
            return None, "Invalid query: empty or wrong type"

        try:
            self._rate_limit()

            with self.timed_query("SPARQL execution"):
                if timeout_override:
                    self.endpoint.setTimeout(timeout_override)

                self.endpoint.setQuery(query)
                results = self.endpoint.query().convert()

            # Handle boolean queries
            if isinstance(results, dict) and "boolean" in results:
                val = "TRUE" if results.get("boolean") else "FALSE"
                return [{"ask_result": {"type": "literal", "value": val}}], None

            # Handle SELECT queries
            if isinstance(results, dict) and "results" in results:
                bindings = results["results"].get("bindings", [])
                if bindings:
                    return bindings, None
                return [], None

            return None, "Unexpected response format"

        except TimeoutError as e:
            return None, f"Query timeout: {str(e)[:80]}"
        except Exception as e:
            error_msg = str(e).split("\n")[0][:100]
            logger.warning(f"SPARQL execution failed: {error_msg}")
            return None, error_msg

    def calculate_f1(
        self, gold_results: Optional[List], gen_results: Optional[List]
    ) -> float:
        """
        Computes F1 score between reference and generated results.

        Args:
            gold_results: Gold standard results
            gen_results: Generated results

        Returns:
            F1 score between 0.0 and 1.0
        """
        # Handle edge cases
        if gold_results is None or gen_results is None:
            return 0.0

        if not gold_results and not gen_results:
            return 1.0  # Both empty = perfect match

        if not gold_results or not gen_results:
            return 0.0  # One empty, one not

        try:

            def extract_values(bindings):
                """Extract unique value tuples from bindings."""
                values = set()
                for row in bindings:
                    if not isinstance(row, dict):
                        continue
                    row_vals = []
                    for k, v in row.items():
                        if isinstance(v, dict) and "value" in v:
                            val = v["value"].split("/")[-1]
                            row_vals.append(val)
                    if row_vals:
                        values.add(tuple(sorted(row_vals)))
                return values

            gold_set = extract_values(gold_results)
            gen_set = extract_values(gen_results)

            if not gold_set or not gen_set:
                return 1.0 if not gold_set and not gen_set else 0.0

            tp = len(gold_set & gen_set)
            if tp == 0:
                return 0.0

            precision = tp / len(gen_set)
            recall = tp / len(gold_set)
            f1 = 2 * (precision * recall) / (precision + recall)

            return min(1.0, max(0.0, f1))  # Ensure 0 <= F1 <= 1

        except Exception as e:
            logger.warning(f"F1 calculation error: {e}")
            return 0.0

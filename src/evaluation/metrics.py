"""
Evaluation Metrics Module.

Computes Precision, Recall, and F1 for SPARQL query generation (QALD standard).
Executes queries against the live Wikidata endpoint with robust rate-limit handling.

Key fixes vs. original:
- Separate 429 retry logic with exponential backoff (up to 60s per retry, 6 attempts)
- Inter-item throttling: small sleep between evaluations to avoid hammering Wikidata
- Rate-limit errors tracked separately (not counted as syntax errors)
- Cleaner progress logging with rate-limit stats
"""

import json
import logging
import os
import ssl
import time
import urllib.error
from typing import Any, Dict, List, Optional, Set, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)


class OfflineEvaluator:
    """
    Computes standard QALD metrics (Precision, Recall, F1) by executing
    generated SPARQL queries against the live Wikidata endpoint.

    Robust handling for:
    - None / error items in the results list
    - 429 Too Many Requests: exponential backoff, up to RATE_LIMIT_MAX_RETRIES attempts
    - Timeout retries
    - Variable-agnostic result matching
    - URI normalisation
    - Inter-item throttling to prevent rate-limit cascades
    """

    ENDPOINT_URL = os.getenv("SPARQL_ENDPOINT_URL", "https://query.wikidata.org/sparql")

    #  Rate-limit tuning 
    # Delay between consecutive item evaluations (2 SPARQL calls per item).
    # 0.5s → ~1 call/s, well within Wikidata's soft limit of ~10 req/s for robots.
    INTER_ITEM_DELAY: float = 0.5

    RATE_LIMIT_MAX_RETRIES: int = 6

    # attempt 0 → 2s, 1 → 4s, 2 → 8s, 3 → 16s, 4 → 32s, 5 → 60s
    RATE_LIMIT_BASE: float = 2.0
    RATE_LIMIT_MAX_SLEEP: float = 60.0

    @staticmethod
    def compute_metrics(
        results: List[Optional[Dict[str, Any]]],
        inter_item_delay: float = None,
    ) -> Dict[str, float]:
        """
        Iterates over generated results, executes both Gold and Generated queries,
        and calculates the Macro F1 score.

        Args:
            results:          List of result dicts (may contain None or items with "error").
            inter_item_delay: Seconds to sleep between items. Defaults to
                              OfflineEvaluator.INTER_ITEM_DELAY (0.5s).
                              Set to 0 to disable (not recommended for large batches).
        """
        # Allow caller to override the default throttle
        delay = (
            inter_item_delay
            if inter_item_delay is not None
            else OfflineEvaluator.INTER_ITEM_DELAY
        )

        #  Filter None entries 
        raw_count = len(results)
        valid_results = [r for r in results if r is not None]

        skipped_none = raw_count - len(valid_results)
        if skipped_none > 0:
            logger.warning(
                f"Skipping {skipped_none} None item(s) in results — "
                "these correspond to pipeline failures in _process_item."
            )

        if not valid_results:
            logger.error("No valid results to evaluate.")
            return {"error": "No valid results to evaluate"}

        logger.info(
            f"Starting Evaluation on {len(valid_results)} items "
            f"(inter-item delay: {delay}s)..."
        )

        #  SPARQL wrapper 
        sparql = SPARQLWrapper(OfflineEvaluator.ENDPOINT_URL)
        sparql.setReturnFormat(JSON)
        sparql.addCustomHttpHeader("User-Agent", "TextToSparqlEvaluator/1.0")
        sparql.setTimeout(20)

        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context

        #  Counters 
        total_precision = 0.0
        total_recall = 0.0
        total_f1 = 0.0
        syntax_errors = 0  
        pipeline_errors = 0  
        rate_limit_skips = 0  
        count = 0
        exact_matches = 0

        for idx, item in enumerate(valid_results):

            # Sleep between items to respect Wikidata rate limits.
            # Skip the very first item (no previous call to rate-limit).
            if delay > 0 and idx > 0:
                time.sleep(delay)

            #  Pipeline errors (failed before we got a query) 
            if item.get("error"):
                logger.debug(
                    f"ID {item.get('id')}: Pipeline error — {item['error']}. "
                    "Counting as F1=0."
                )
                pipeline_errors += 1
                count += 1
                continue

            gold_query = item.get("gold_sparql")
            gen_query = item.get("generated_sparql")

            if not gen_query:
                logger.debug(f"ID {item.get('id')}: No generated query.")
                count += 1
                continue

            #  Execute gold 
            gold_results, gold_rate_limited = (
                OfflineEvaluator._execute_query_with_retry(sparql, gold_query)
            )

            #  Execute generated 
            gen_results, gen_rate_limited = OfflineEvaluator._execute_query_with_retry(
                sparql, gen_query
            )

            #  Handle rate-limit failures 
            # If either query was rate-limited beyond all retries, we cannot
            # evaluate this item fairly. Skip it and track separately.
            if gold_rate_limited or gen_rate_limited:
                rate_limit_skips += 1
                logger.warning(
                    f"ID {item.get('id')}: Skipped evaluation — "
                    f"persistent rate-limit (gold_limited={gold_rate_limited}, "
                    f"gen_limited={gen_rate_limited}). "
                    "Consider increasing INTER_ITEM_DELAY."
                )
                count += 1
                continue

            #  Track syntax/execution errors on generated query 
            if gen_results is None:
                syntax_errors += 1
                gen_results = set()

            # If gold fails we cannot evaluate this item fairly — skip it
            if gold_results is None:
                logger.warning(
                    f"ID {item.get('id')}: Gold query failed. Skipping metric."
                )
                count += 1
                continue

            #  Compute metrics 
            p, r, f1 = OfflineEvaluator._calculate_set_metrics(
                gold_results, gen_results
            )

            total_precision += p
            total_recall += r
            total_f1 += f1
            count += 1

            if f1 >= 0.99:
                exact_matches += 1

            item["evaluation"] = {
                "precision": p,
                "recall": r,
                "f1": f1,
                "gold_count": len(gold_results),
                "gen_count": len(gen_results),
            }

            # Progress log every 10 items
            if count % 10 == 0:
                evaluated_so_far = count - pipeline_errors - rate_limit_skips
                current_f1 = (
                    total_f1 / evaluated_so_far if evaluated_so_far > 0 else 0.0
                )
                logger.info(
                    f"Evaluated {count}/{len(valid_results)} | "
                    f"Macro F1: {current_f1:.4f} | "
                    f"SyntaxErr: {syntax_errors} | "
                    f"RateLimit skips: {rate_limit_skips}"
                )

        if count == 0:
            return {"error": "No items evaluated"}

        # Denominator for averages: items where we actually computed a score
        scored_count = count - pipeline_errors - rate_limit_skips
        if scored_count == 0:
            return {"error": "All items were either pipeline errors or rate-limited"}

        metrics = {
            "precision": round(total_precision / scored_count, 4),
            "recall": round(total_recall / scored_count, 4),
            "f1": round(total_f1 / scored_count, 4),
            "exact_match_rate": round(exact_matches / scored_count, 4),
            "syntax_error_rate": round(syntax_errors / len(valid_results), 4),
            "pipeline_error_rate": round(pipeline_errors / len(valid_results), 4),
            "rate_limit_skip_rate": round(rate_limit_skips / len(valid_results), 4),
            "evaluated_count": scored_count,
            "exact_matches": exact_matches,
            "skipped_none": skipped_none,
            "pipeline_errors": pipeline_errors,
            "syntax_errors": syntax_errors,
            "rate_limit_skips": rate_limit_skips,
        }

        logger.info("=== Evaluation Summary ===")
        logger.info(f"Macro F1:           {metrics['f1']}")
        logger.info(f"Precision:          {metrics['precision']}")
        logger.info(f"Recall:             {metrics['recall']}")
        logger.info(f"Exact Matches:      {exact_matches}/{scored_count}")
        logger.info(f"Syntax Errors:      {syntax_errors}")
        logger.info(f"Pipeline Errors:    {pipeline_errors}")
        logger.info(f"Rate-Limit Skips:   {rate_limit_skips}")
        if skipped_none:
            logger.warning(f"None items skipped: {skipped_none}")
        if rate_limit_skips > 0:
            logger.warning(
                f"{rate_limit_skips} items skipped due to persistent 429. "
                f"Try increasing INTER_ITEM_DELAY (currently {delay}s) "
                f"or run during off-peak hours."
            )

        return metrics

    @staticmethod
    def _execute_query_with_retry(
        sparql_wrapper: SPARQLWrapper,
        query: str,
        max_retries: int = 3,
    ) -> Tuple[Optional[Set[Tuple]], bool]:
        """
        Executes a SPARQL query with separate retry logic for:
          - Too Many Requests: exponential backoff, up to RATE_LIMIT_MAX_RETRIES attempts
          - Timeout: fixed 2s sleep, up to max_retries attempts
          - Other HTTP errors (400, 500…): immediate None (not retryable)

        Returns:
            (results_set_or_None, was_rate_limited)

            was_rate_limited=True means we exhausted all 429 retries — the
            caller should skip this item rather than counting it as a syntax error.
        """
        if not query or not query.strip():
            return None, False

        rate_limit_attempts = 0

        for attempt in range(max_retries):
            try:
                sparql_wrapper.setQuery(query)
                ret = sparql_wrapper.query().convert()
                return OfflineEvaluator._parse_results(ret), False

            except urllib.error.HTTPError as e:
                if e.code == 429:
                    rate_limit_attempts += 1
                    if rate_limit_attempts > OfflineEvaluator.RATE_LIMIT_MAX_RETRIES:
                        logger.error(
                            f"429 rate limit persists after "
                            f"{OfflineEvaluator.RATE_LIMIT_MAX_RETRIES} retries. "
                            "Giving up on this query."
                        )
                        return None, True  # Signal, rate-limited, not a real error

                    sleep_time = min(
                        OfflineEvaluator.RATE_LIMIT_BASE
                        * (2 ** (rate_limit_attempts - 1)),
                        OfflineEvaluator.RATE_LIMIT_MAX_SLEEP,
                    )
                    logger.warning(
                        f"429 Too Many Requests (attempt {rate_limit_attempts}/"
                        f"{OfflineEvaluator.RATE_LIMIT_MAX_RETRIES}). "
                        f"Sleeping {sleep_time:.0f}s before retry..."
                    )
                    time.sleep(sleep_time)
                    continue

                # Other HTTP errors (400 Bad Request = syntax error, 500, etc.)
                logger.debug(f"HTTP {e.code} error on query: {str(e)[:100]}")
                return None, False

            except Exception as e:
                error_msg = str(e).lower()
                if "time-out" in error_msg or "timed out" in error_msg:
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Timeout on attempt {attempt + 1}/{max_retries}. "
                            "Retrying in 2s..."
                        )
                        time.sleep(2)
                        continue
                    else:
                        logger.error(f"Query timed out after {max_retries} retries.")
                        return None, False

                # Non-timeout, non-HTTP error (parse error, network issue, etc.)
                logger.debug(f"Query execution error: {str(e)[:100]}")
                return None, False

        # Exhausted max_retries (only reached on repeated timeouts)
        return None, False

    @staticmethod
    def _parse_results(ret: Dict) -> Set[Any]:
        """
        Parses JSON SPARQLWrapper results into a canonical set of values.

        - ASK queries  → {"true"} or {"false"}
        - SELECT 1 var → flat set of values
        - SELECT N var → set of tuples
        - URIs normalised by stripping the Wikidata entity prefix
        """
        if "boolean" in ret:
            return {str(ret["boolean"]).lower()}

        if "results" not in ret or "bindings" not in ret["results"]:
            return set()

        vars_list = ret["head"]["vars"]
        results: Set[Any] = set()

        for binding in ret["results"]["bindings"]:
            row = []
            for v in vars_list:
                if v in binding:
                    val = binding[v]["value"]
                    val = val.replace("http://www.wikidata.org/entity/", "")
                    row.append(val)
                else:
                    row.append(None)

            if len(row) == 1:
                results.add(row[0])
            else:
                results.add(tuple(row))

        return results

    @staticmethod
    def _calculate_set_metrics(
        gold: Optional[Set],
        gen: Optional[Set],
    ) -> Tuple[float, float, float]:
        """
        Computes Precision, Recall, F1 from two result sets.
        """
        if gold is None:
            gold = set()
        if gen is None:
            gen = set()

        # Both empty → perfect match
        if not gold and not gen:
            return 1.0, 1.0, 1.0

        # One side empty → zero
        if not gold or not gen:
            return 0.0, 0.0, 0.0

        intersection = len(gold & gen)
        precision = intersection / len(gen)
        recall = intersection / len(gold)

        f1 = 0.0
        if (precision + recall) > 0:
            f1 = (2 * precision * recall) / (precision + recall)

        return precision, recall, f1


# 
# Utility function used by query_validator.py
# 
def compare_results(
    gen_results: list,
    gold_results: list,
) -> tuple:
    """
    Computes (F1, precision, recall) between two flat result lists.
    Used by SPARQLValidator.validate_semantic() for dry-run checks.
    """
    gen_set = set(str(v) for v in gen_results) if gen_results else set()
    gold_set = set(str(v) for v in gold_results) if gold_results else set()

    if not gold_set and not gen_set:
        return 1.0, 1.0, 1.0
    if not gold_set or not gen_set:
        return 0.0, 0.0, 0.0

    intersection = len(gen_set & gold_set)
    precision = intersection / len(gen_set)
    recall = intersection / len(gold_set)
    f1 = (
        (2 * precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    return f1, precision, recall

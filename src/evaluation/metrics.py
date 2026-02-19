"""
Evaluation Metrics Module.

This module computes evaluation metrics for SPARQL query generation tasks, focusing on QALD metrics.

Features:
- Calculates Precision, Recall, and F1 scores for generated queries.
- Executes queries against the live Wikidata endpoint.
- Handles errors and retries for evaluation.

Implementation:
- Uses `OfflineEvaluator` to process results and compute metrics.
- Supports variable-agnostic result matching and URI normalization.
- Provides detailed logging for debugging and analysis.
"""

import json
import logging
import ssl
import time
import urllib.error
from typing import Any, Dict, List, Optional, Set, Tuple
import os

from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)


class OfflineEvaluator:
    """
    Computes standard QALD metrics (Precision, Recall, F1) by executing
    generated SPARQL queries against the live Wikidata endpoint.

    Includes robust handling for:
    - None / error items in the results list (from failed _process_item calls)
    - Retries on timeout
    - Variable-agnostic result matching
    - URI normalisation
    """

    ENDPOINT_URL = os.getenv("SPARQL_ENDPOINT_URL", "https://query.wikidata.org/sparql")

    @staticmethod
    def compute_metrics(results: List[Optional[Dict[str, Any]]]) -> Dict[str, float]:
        """
        Iterates over generated results, executes both Gold and Generated queries,
        and calculates the Macro F1 score.

        Handles None items and items with an "error" key gracefully — they are
        counted as failures (F1=0) rather than crashing the evaluation.
        """
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

        logger.info(f"Starting Evaluation on {len(valid_results)} items...")

        # --- Setup SPARQL wrapper ---
        sparql = SPARQLWrapper(OfflineEvaluator.ENDPOINT_URL)
        sparql.setReturnFormat(JSON)
        sparql.addCustomHttpHeader("User-Agent", "TextToSparqlEvaluator/1.0")
        sparql.setTimeout(20)

        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context

        total_precision = 0.0
        total_recall = 0.0
        total_f1 = 0.0
        syntax_errors = 0
        pipeline_errors = 0
        count = 0
        exact_matches = 0

        for item in valid_results:
            # Items that failed in _process_item have an "error" key set
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

            # Execute Gold
            gold_results = OfflineEvaluator._execute_query_with_retry(
                sparql, gold_query
            )

            # Execute Generated
            gen_results = OfflineEvaluator._execute_query_with_retry(
                sparql, gen_query
            )

            # Track syntax/execution errors on the generated query
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

            if count % 10 == 0:
                logger.info(
                    f"Evaluated {count}/{len(valid_results)} queries. "
                    f"Current Macro F1: {total_f1 / count:.4f}"
                )

        if count == 0:
            return {"error": "No items evaluated"}

        metrics = {
            "precision": round(total_precision / count, 4),
            "recall": round(total_recall / count, 4),
            "f1": round(total_f1 / count, 4),
            "exact_match_rate": round(exact_matches / count, 4),
            "syntax_error_rate": round(syntax_errors / len(valid_results), 4),
            "pipeline_error_rate": round(pipeline_errors / len(valid_results), 4),
            "evaluated_count": count,
            "exact_matches": exact_matches,
            "skipped_none": skipped_none,
            "pipeline_errors": pipeline_errors,
        }

        logger.info("=== Evaluation Summary ===")
        logger.info(f"Macro F1:       {metrics['f1']}")
        logger.info(f"Exact Matches:  {exact_matches}/{count}")
        logger.info(f"Syntax Errors:  {syntax_errors}")
        logger.info(f"Pipeline Errors:{pipeline_errors}")
        if skipped_none:
            logger.warning(f"None items skipped: {skipped_none}")

        return metrics

    @staticmethod
    def _execute_query_with_retry(
        sparql_wrapper: SPARQLWrapper,
        query: str,
        max_retries: int = 3,
    ) -> Optional[Set[Tuple]]:
        """
        Executes a SPARQL query with retry logic for transient errors.
        Returns None on unrecoverable failure (syntax error, persistent timeout).
        """
        if not query or not query.strip():
            return None

        for attempt in range(max_retries):
            try:
                sparql_wrapper.setQuery(query)
                ret = sparql_wrapper.query().convert()
                return OfflineEvaluator._parse_results(ret)

            except urllib.error.HTTPError as e:
                if e.code == 429:  # Too Many Requests
                    time.sleep(2 * (attempt + 1))
                    continue
                return None  # e.g. 400 Bad Request = syntax error

            except Exception as e:
                error_msg = str(e).lower()
                if "time-out" in error_msg or "timed out" in error_msg:
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Timeout on attempt {attempt + 1}. Retrying..."
                        )
                        time.sleep(2)
                        continue
                    else:
                        logger.error(f"Query timed out after {max_retries} retries.")
                        return None
                # Non-timeout error — likely a logic/syntax issue
                return None

        return None

    @staticmethod
    def _parse_results(ret: Dict) -> Set[Any]:
        """
        Parses JSON SPARQLWrapper results into a canonical set of values.

        - ASK queries → {"true"} or {"false"}
        - SELECT queries with 1 variable → flat set of values
        - SELECT queries with N variables → set of tuples
        - URIs are normalised by stripping the Wikidata entity prefix
        """
        # ASK queries
        if "boolean" in ret:
            return {str(ret["boolean"]).lower()}

        # SELECT queries
        if "results" not in ret or "bindings" not in ret["results"]:
            return set()

        vars_list = ret["head"]["vars"]
        results: Set[Any] = set()

        for binding in ret["results"]["bindings"]:
            row = []
            for v in vars_list:
                if v in binding:
                    val = binding[v]["value"]
                    # Normalise Wikidata entity URIs
                    val = val.replace(
                        "http://www.wikidata.org/entity/", ""
                    )
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

        # One side empty → zero score
        if not gold or not gen:
            return 0.0, 0.0, 0.0

        intersection = len(gold & gen)

        precision = intersection / len(gen)
        recall = intersection / len(gold)

        if (precision + recall) == 0:
            f1 = 0.0
        else:
            f1 = (2 * precision * recall) / (precision + recall)

        return precision, recall, f1
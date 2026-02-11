import json
import logging
import ssl
import time
import urllib.error
from typing import Any, Dict, List, Set, Tuple
import os

from SPARQLWrapper import JSON, SPARQLWrapper

logger = logging.getLogger(__name__)

class OfflineEvaluator:
    """
    Computes standard QALD metrics (Precision, Recall, F1) by executing
    generated SPARQL queries against the live Wikidata endpoint.
    Includes robust handling for retries, variable naming, and URI normalization.
    """

    ENDPOINT_URL = os.getenv("SPARQL_ENDPOINT_URL", "https://query.wikidata.org/sparql")

    @staticmethod
    def compute_metrics(results: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Iterates over generated results, executes both Gold and Generated queries,
        and calculates the Macro F1 score.
        """
        total_precision = 0.0
        total_recall = 0.0
        total_f1 = 0.0
        syntax_errors = 0
        count = 0
        exact_matches = 0
        
        # Setup SPARQL Wrapper
        sparql = SPARQLWrapper(OfflineEvaluator.ENDPOINT_URL)
        sparql.setReturnFormat(JSON)
        sparql.addCustomHttpHeader("User-Agent", "TextToSparqlEvaluator/1.0")
        sparql.setTimeout(20) # Aumentato timeout a 20 secondi

        # Fix SSL context for Mac/local envs
        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context

        logger.info(f"Starting Evaluation on {len(results)} items...")

        for item in results:
            gold_query = item.get("gold_sparql")
            gen_query = item.get("generated_sparql")

            if not gen_query:
                logger.debug(f"ID {item.get('id')}: No generated query.")
                count += 1
                continue

            # Execute Gold
            gold_results = OfflineEvaluator._execute_query_with_retry(sparql, gold_query)
            
            # Execute Generated
            gen_results = OfflineEvaluator._execute_query_with_retry(sparql, gen_query)

            # Check for syntax/execution errors
            if gen_results is None:
                syntax_errors += 1
                gen_results = set() # Treat as empty result for metrics
            
            if gold_results is None:
                # If gold fails, we can't evaluate this item fairly. Skip or treat as 0?
                # Usually we skip to avoid penalizing the model for Wikidata issues.
                logger.warning(f"ID {item.get('id')}: Gold query failed. Skipping metric calculation for this item.")
                count += 1
                continue

            # Calculate Metrics
            p, r, f1 = OfflineEvaluator._calculate_set_metrics(gold_results, gen_results)
            
            total_precision += p
            total_recall += r
            total_f1 += f1
            count += 1
            
            if f1 >= 0.99: # Floating point tolerance
                exact_matches += 1

            # Update item with evaluation details (optional, for debugging)
            item["evaluation"] = {
                "precision": p,
                "recall": r,
                "f1": f1,
                "gold_count": len(gold_results),
                "gen_count": len(gen_results)
            }
            
            # Logging progress occasionally
            if count % 10 == 0:
                logger.info(f"Evaluated {count}/{len(results)} queries. Current Macro F1: {total_f1/count:.4f}")

        # Final Averages
        if count == 0:
            return {"error": "No items evaluated"}

        metrics = {
            "precision": round(total_precision / count, 4),
            "recall": round(total_recall / count, 4),
            "f1": round(total_f1 / count, 4),
            "exact_match_rate": round(exact_matches / count, 4),
            "syntax_error_rate": round(syntax_errors / len(results), 4),
            "evaluated_count": count,
            "exact_matches": exact_matches
        }
        
        logger.info("=== Evaluation Summary ===")
        logger.info(f"Macro F1: {metrics['f1']}")
        logger.info(f"Exact Matches: {exact_matches}/{count}")
        
        return metrics

    @staticmethod
    def _execute_query_with_retry(sparql_wrapper: SPARQLWrapper, query: str, max_retries: int = 3) -> Set[Tuple]:
        """
        Executes query with retry logic for timeouts.
        Normalizes results to handle URI prefixes and variable names.
        """
        for attempt in range(max_retries):
            try:
                sparql_wrapper.setQuery(query)
                ret = sparql_wrapper.query().convert()
                return OfflineEvaluator._parse_results(ret)
                
            except urllib.error.HTTPError as e:
                if e.code == 429: # Too Many Requests
                    time.sleep(2 * (attempt + 1))
                    continue
                return None # Other HTTP errors (e.g. 400 Syntax) -> Syntax Error
                
            except Exception as e:
                # If timeout, retry. If syntax error, stop.
                error_msg = str(e).lower()
                if "time-out" in error_msg or "timed out" in error_msg:
                    if attempt < max_retries - 1:
                        logger.warning(f"Timeout (attempt {attempt+1}). Retrying...")
                        time.sleep(2)
                        continue
                    else:
                        logger.error(f"Failed after {max_retries} retries due to timeout.")
                        return None
                
                # If it's not a timeout, it's likely a syntax error or logic error
                # logger.warning(f"SPARQL Execution Error: {e}") 
                return None
        return None

    @staticmethod
    def _parse_results(ret: Dict) -> Set[Any]:
        """
        Parses JSON results from SPARQLWrapper into a canonical set of values.
        - Handles variable-agnostic matching (if 1 var).
        - Normalizes URIs (removes http://www.wikidata.org/entity/).
        """
        results = set()
        
        # Handle ASK queries
        if "boolean" in ret:
            # Normalize boolean to string 'true'/'false' or keep python bool
            # Let's use string to match set logic easily
            return {str(ret["boolean"]).lower()}

        # Handle SELECT queries
        if "results" not in ret or "bindings" not in ret["results"]:
            return set()

        vars_list = ret["head"]["vars"]
        
        for binding in ret["results"]["bindings"]:
            row = []
            for v in vars_list:
                if v in binding:
                    val = binding[v]["value"]
                    # NORMALIZE: Strip Wikidata URI prefix for easier comparison
                    val = val.replace("http://www.wikidata.org/entity/", "")
                    row.append(val)
                else:
                    row.append(None)
            
            # Variable Agnostic Logic
            if len(row) == 1:
                results.add(row[0])
            else:
                results.add(tuple(row))
                
        return results

    @staticmethod
    def _calculate_set_metrics(gold: Set, gen: Set) -> Tuple[float, float, float]:
        """
        Calculates P, R, F1 by comparing two sets of results.
        """
        if gold is None: gold = set()
        if gen is None: gen = set()

        if not gold and not gen:
            return 1.0, 1.0, 1.0 # Both empty = Match
        if not gold and gen:
            return 0.0, 0.0, 0.0 # Gold empty but Gen has results = Error
        if gold and not gen:
            return 0.0, 0.0, 0.0 # Gen empty = Error

        intersection = len(gold.intersection(gen))
        
        precision = intersection / len(gen) if len(gen) > 0 else 0.0
        recall = intersection / len(gold) if len(gold) > 0 else 0.0
        
        if (precision + recall) == 0:
            f1 = 0.0
        else:
            f1 = (2 * precision * recall) / (precision + recall)
            
        return precision, recall, f1
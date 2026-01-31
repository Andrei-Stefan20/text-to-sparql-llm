import json
import logging
import ssl
import time
from typing import Any, Dict, List, Set, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper
from tqdm import tqdm

logger = logging.getLogger(__name__)


class OfflineEvaluator:
    """
    Computes standard QALD metrics (Precision, Recall, F1) by executing
    generated SPARQL queries against the live Wikidata endpoint.
    """

    ENDPOINT_URL = "https://query.wikidata.org/sparql"

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

        logger.info(f"Starting QALD Evaluation on {len(results)} items...")

        # Initialize SPARQL Wrapper
        sparql = SPARQLWrapper(OfflineEvaluator.ENDPOINT_URL)
        sparql.setReturnFormat(JSON)
        sparql.addCustomHttpHeader("User-Agent", "TextToSparql-Evaluator/1.0")
        sparql.setTimeout(10)

        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context

        for item in tqdm(results, desc="Evaluating Queries"):
            gen_query = item.get("generated_sparql", "").strip()
            gold_query = item.get("gold_sparql", "").strip()

            if not gold_query:
                continue

            count += 1

            # 1. Execute Gold Query, expected Answers
            gold_answers = OfflineEvaluator._execute_query(sparql, gold_query)

            # 2. Execute Generated Query, actual Answers
            gen_answers = None
            if gen_query:
                gen_answers = OfflineEvaluator._execute_query(sparql, gen_query)

            # 3. Calculate Metrics
            if gen_answers is None:
                # Execution failed or empty query
                if gen_query:
                    syntax_errors += 1
                p, r, f1 = 0.0, 0.0, 0.0
            else:
                # Standard QALD set comparison
                p, r, f1 = OfflineEvaluator._calculate_set_metrics(
                    gold_answers, gen_answers
                )

            total_precision += p
            total_recall += r
            total_f1 += f1

            # Delay to avoid overloading Wikidata
            time.sleep(0.5)

        if count == 0:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "error_rate": 0.0}

        # Calculate Macro-Average
        metrics = {
            "precision": round(total_precision / count, 4),
            "recall": round(total_recall / count, 4),
            "f1": round(total_f1 / count, 4),
            "syntax_error_rate": round(syntax_errors / count, 4),
            "evaluated_count": count,
        }

        return metrics

    @staticmethod
    def _execute_query(sparql_wrapper: SPARQLWrapper, query: str) -> Set[Tuple]:
        """
        Executes a SPARQL query and returns a set of canonical tuples.
        Returns None if execution fails (syntax error/timeout).
        """
        try:
            sparql_wrapper.setQuery(query)
            ret = sparql_wrapper.query().convert()

            results = set()
            vars_list = ret["head"]["vars"]

            for binding in ret["results"]["bindings"]:
                row = []
                for v in vars_list:
                    if v in binding:
                        row.append((v, binding[v]["value"]))
                results.add(tuple(sorted(row)))

            return results

        except Exception:
            return None

    @staticmethod
    def _calculate_set_metrics(gold: Set, gen: Set) -> Tuple[float, float, float]:
        """
        Calculates P, R, F1 by comparing two sets of results.
        """
        if gold is None:
            gold = set()
        if gen is None:
            gen = set()

        # Handle edge cases
        if not gold:
            return (1.0, 1.0, 1.0) if not gen else (0.0, 0.0, 0.0)

        if not gen:
            return 0.0, 0.0, 0.0

        # Intersection
        intersection = len(gold.intersection(gen))

        precision = intersection / len(gen) if len(gen) > 0 else 0.0
        recall = intersection / len(gold) if len(gold) > 0 else 0.0

        if (precision + recall) == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        return precision, recall, f1

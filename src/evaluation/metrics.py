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
        
        Also computes validation/correction statistics if available.
        MODIFIES results in-place to add execution details.
        """
        total_precision = 0.0
        total_recall = 0.0
        total_f1 = 0.0
        syntax_errors = 0
        count = 0
        exact_matches = 0
        
        # Validation/Correction statistics
        validation_stats = {
            "total_validated": 0,
            "valid_on_first_try": 0,
            "valid_after_correction": 0,
            "total_correction_attempts": 0,
            "self_consistency_used": 0,
            "correction_success": 0,
            "still_invalid": 0,
        }

        logger.info(f"Starting QALD Evaluation on {len(results)} items...")

        # Initialize SPARQL Wrapper
        sparql = SPARQLWrapper(OfflineEvaluator.ENDPOINT_URL)
        sparql.setReturnFormat(JSON)
        sparql.addCustomHttpHeader("User-Agent", "TextToSparql-Evaluator/1.0")
        sparql.setTimeout(30)

        if hasattr(ssl, "_create_unverified_context"):
            ssl._create_default_https_context = ssl._create_unverified_context

        for item in tqdm(results, desc="Evaluating Queries"):
            gen_query = item.get("generated_sparql", "").strip()
            gold_query = item.get("gold_sparql", "").strip()

            gen_query = gen_query.replace("\\n", "\n")
            gold_query = gold_query.replace("\\n", "\n")

            # Print queries to console for inspection
            print("\n--- EVALUATION ITEM ---")
            print(f"ID: {item.get('id')}")
            print("Gold Query:")
            print(gold_query)
            print("Generated Query:")
            print(gen_query)
            
            # Initialize evaluation details for this item
            item["evaluation"] = {
                "gold_results_count": 0,
                "generated_results_count": 0,
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "exact_match": False,
                "execution_error": None,
            }
            
            # Track validation statistics
            validation_info = item.get("validation")
            if validation_info:
                validation_stats["total_validated"] += 1
                
                if validation_info.get("is_valid"):
                    total_attempts = validation_info.get("total_attempts", 1)
                    correction_method = validation_info.get("correction_method", "none")
                    
                    if total_attempts == 1 and correction_method == "none":
                        validation_stats["valid_on_first_try"] += 1
                    else:
                        validation_stats["valid_after_correction"] += 1
                        validation_stats["correction_success"] += 1
                    
                    if correction_method == "self_consistency":
                        validation_stats["self_consistency_used"] += 1
                    
                    validation_stats["total_correction_attempts"] += total_attempts
                else:
                    validation_stats["still_invalid"] += 1
                    validation_stats["total_correction_attempts"] += validation_info.get("total_attempts", 1)

            if not gold_query:
                item["evaluation"]["execution_error"] = "No gold query available"
                continue

            count += 1

            # 1. Execute Gold Query
            gold_answers = OfflineEvaluator._execute_query(sparql, gold_query)
            print("Gold Query Results:")
            print(gold_answers)
            if gold_answers is not None:
                item["evaluation"]["gold_results_count"] = len(gold_answers)
                # Store actual gold answers for JSON
                item["evaluation"]["gold_bindings"] = [list(row) for row in gold_answers]
            else:
                item["evaluation"]["execution_error"] = "Gold query execution failed"

            # 2. Execute Generated Query
            gen_answers = None
            if gen_query:
                gen_answers = OfflineEvaluator._execute_query(sparql, gen_query)
                print("Generated Query Results:")
                print(gen_answers)
                if gen_answers is not None:
                    item["evaluation"]["generated_results_count"] = len(gen_answers)
                    # Store actual generated answers for JSON
                    item["evaluation"]["generated_bindings"] = [list(row) for row in gen_answers]
                else:
                    item["evaluation"]["execution_error"] = "Generated query execution failed"
                    syntax_errors += 1

            # 3. Calculate Metrics
            if gen_answers is None:
                p, r, f1 = 0.0, 0.0, 0.0
            else:
                p, r, f1 = OfflineEvaluator._calculate_set_metrics(
                    gold_answers, gen_answers
                )
                
            # Check for exact match
            is_exact = gold_answers == gen_answers if gold_answers is not None and gen_answers is not None else False
            if is_exact:
                exact_matches += 1
            
            # Store per-item metrics
            item["evaluation"]["precision"] = round(p, 4)
            item["evaluation"]["recall"] = round(r, 4)
            item["evaluation"]["f1"] = round(f1, 4)
            item["evaluation"]["exact_match"] = is_exact

            total_precision += p
            total_recall += r
            total_f1 += f1
            
            # Log progress for each item
            logger.debug(f"Q{item.get('id')}: P={p:.2f} R={r:.2f} F1={f1:.2f} | Gold={item['evaluation']['gold_results_count']} Gen={item['evaluation']['generated_results_count']}")

            # Delay to avoid overloading Wikidata
            time.sleep(0.5)

        if count == 0:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "error_rate": 0.0}

        # Calculate Macro-Average
        metrics = {
            "precision": round(total_precision / count, 4),
            "recall": round(total_recall / count, 4),
            "f1": round(total_f1 / count, 4),
            "exact_match_rate": round(exact_matches / count, 4),
            "syntax_error_rate": round(syntax_errors / count, 4),
            "evaluated_count": count,
            "exact_matches": exact_matches,
        }
        
        # Log summary
        logger.info(f"=== Evaluation Summary ===")
        logger.info(f"Total evaluated: {count}")
        logger.info(f"Exact matches: {exact_matches} ({metrics['exact_match_rate']*100:.1f}%)")
        logger.info(f"Macro Precision: {metrics['precision']:.4f}")
        logger.info(f"Macro Recall: {metrics['recall']:.4f}")
        logger.info(f"Macro F1: {metrics['f1']:.4f}")
        logger.info(f"Syntax errors: {syntax_errors} ({metrics['syntax_error_rate']*100:.1f}%)")
        
        # Add validation/correction statistics if any validation was done
        if validation_stats["total_validated"] > 0:
            total_val = validation_stats["total_validated"]
            metrics["validation"] = {
                "total_validated": total_val,
                "valid_first_try_rate": round(validation_stats["valid_on_first_try"] / total_val, 4),
                "correction_success_rate": round(validation_stats["correction_success"] / total_val, 4) if validation_stats["total_correction_attempts"] > total_val else 0.0,
                "avg_attempts": round(validation_stats["total_correction_attempts"] / total_val, 2),
                "still_invalid_rate": round(validation_stats["still_invalid"] / total_val, 4),
                "self_consistency_used": validation_stats["self_consistency_used"],
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

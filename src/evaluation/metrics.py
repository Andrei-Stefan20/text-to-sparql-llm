"""
Evaluation helpers.

The authoritative metric lives in ``evaluate_gerbil_vs_qald.py`` (GERBIL-style
answer-set comparison against the frozen QALD-10 gold). This module only keeps
the small ``compare_results`` helper used by ``query_validator`` for in-pipeline
dry-run checks.

(The former ``OfflineEvaluator`` — which re-executed both gold and generated
queries live and compared them with structural tuple matching — was removed: it
was dead code, only ever invoked from a commented-out line in main.py, and its
tuple semantics diverged from the pooled-set metric actually reported.)
"""


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

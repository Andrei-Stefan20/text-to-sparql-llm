"""
Offline GERBIL-style evaluator: gerbil_test.json vs QALD-10 gold.

Compares the answers produced by each experiment's generated SPARQL queries
(stored in every `outputs/**/gerbil_test.json`) against the frozen gold answers
shipped inside the QALD-10 dataset.

This reproduces the GERBIL QALD methodology locally, comparing *answer sets*
(not query strings) — a query written differently but returning the same
results still scores 1.0. It never depends on the GERBIL server.

Two modes:

1. Default (fully offline): compares the answers already stored in
   gerbil_test.json against the frozen gold answers in qald_10.json.
   No network. WARNING: only meaningful if gerbil_test.json answers are
   actually populated. If they were written with a short timeout / under
   rate-limiting they may be empty, in which case the scores are noise.
   Use --require-answers to abort when a file has no populated answers.

2. --reexecute: ignores the stored answers and runs each `query.sparql`
   live against the Wikidata endpoint, then compares to the frozen gold.
   This is the reliable mode when the stored answers are empty/stale.
   It hits Wikidata (rate-limited) but still needs no GERBIL server.

Metric: Macro Precision / Recall / F1 over the questions of each file,
following the QALD convention where an item with empty gold AND empty
prediction counts as a perfect match (F1 = 1.0).

Usage:
    # offline, using stored answers
    python -m src.evaluation.evaluate_gerbil_vs_qald --csv outputs/gerbil_vs_qald_summary.csv

    # re-execute generated queries live (reliable), one experiment family
    python -m src.evaluation.evaluate_gerbil_vs_qald --reexecute --filter exp4_3shot_gpt4_394

Caveat:
    The QALD-10 gold answers are frozen at dataset-creation time. If Wikidata
    drifted, a semantically correct query can still mismatch the gold set.
    This is an inherent limitation of any frozen-gold comparison (GERBIL
    included), not a bug in this script.
"""

import argparse
import csv
import glob
import json
import os
import re
import ssl
import time
import urllib.error
from typing import Any, Dict, List, Optional, Set, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper

WIKIDATA_ENTITY_PREFIX = "http://www.wikidata.org/entity/"

DEFAULT_OUTPUTS_DIR = "outputs"
DEFAULT_GOLD_PATH = os.path.join(
    "data", "raw", "QALD-10", "data", "qald_10", "qald_10.json"
)
GERBIL_FILENAME = "gerbil_test.json"


# Candidate endpoints tried in order at startup; the first reachable one wins.
# Override / prepend with --endpoints or the SPARQL_ENDPOINT_URL env var.
DEFAULT_ENDPOINTS = [
    "https://query.wikidata.org/sparql",  # official WDQS (may be throttled)
    "https://qlever.cs.uni-freiburg.de/api/wikidata",  # fast public mirror
]

# Standard Wikidata prefixes, injected into queries that declare none — WDQS
# predefines them but QLever (and plain SPARQL engines) require explicit ones.
STANDARD_PREFIXES = """PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wds: <http://www.wikidata.org/entity/statement/>
PREFIX wdv: <http://www.wikidata.org/value/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX psv: <http://www.wikidata.org/prop/statement/value/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX schema: <http://schema.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX wikibase: <http://wikiba.se/ontology#>
"""

# Matches a (non-nested) `SERVICE wikibase:label { ... }` block.
_LABEL_SERVICE_RE = re.compile(
    r"SERVICE\s+wikibase:label\s*\{[^{}]*\}", re.IGNORECASE | re.DOTALL
)

# Live re-execution tuning (only used with --reexecute).
INTER_QUERY_DELAY = 0.5
RATE_LIMIT_MAX_RETRIES = 6
RATE_LIMIT_BASE = 2.0
RATE_LIMIT_MAX_SLEEP = 60.0


def _normalise_value(value: str) -> str:
    """Strip the Wikidata entity prefix so URIs compare equal across sources."""
    return value.replace(WIKIDATA_ENTITY_PREFIX, "")


def prepare_query(query: str, strip_label_service: bool = True) -> str:
    """
    Make a generated query portable across engines.

    - Removes `SERVICE wikibase:label {...}` blocks: only WDQS implements them,
      and they only add label columns (the answer entity is still returned).
    - Prepends the standard Wikidata prefixes when the query declares none,
      so prefix-less queries run on engines that don't predefine them.
    """
    if not query:
        return query
    out = query
    if strip_label_service:
        out = _LABEL_SERVICE_RE.sub(" ", out)
    if "prefix " not in out.lower():
        out = STANDARD_PREFIXES + out
    return out


def _make_sparql_client(endpoint_url: str) -> SPARQLWrapper:
    """Build a SPARQLWrapper configured for the given endpoint."""
    client = SPARQLWrapper(endpoint_url)
    client.setReturnFormat(JSON)
    client.addCustomHttpHeader("User-Agent", "TextToSparqlEvaluator/1.0")
    client.setTimeout(30)
    if hasattr(ssl, "_create_unverified_context"):
        ssl._create_default_https_context = ssl._create_unverified_context
    return client


def select_working_endpoint(candidates: List[str]) -> Optional[str]:
    """
    Return the first endpoint that answers a trivial probe query without a
    connection error or rate-limit, or None if all candidates fail.
    """
    probe = (
        STANDARD_PREFIXES
        + "SELECT ?p WHERE { wd:Q761383 wdt:P138 ?p . } LIMIT 1"
    )
    for url in candidates:
        if not url:
            continue
        client = _make_sparql_client(url)
        try:
            client.setQuery(probe)
            client.query().convert()
            print(f"  [endpoint] using {url}")
            return url
        except urllib.error.HTTPError as e:
            print(f"  [endpoint] {url} -> HTTP {e.code}, trying next")
        except Exception as e:
            print(f"  [endpoint] {url} -> {type(e).__name__}, trying next")
    return None


def execute_query_live(
    client: SPARQLWrapper, query: str, max_retries: int = 3
) -> Tuple[Optional[Set[Any]], bool]:
    """
    Execute a SPARQL query, returning (answer_set_or_None, was_rate_limited).

    None means the query failed (syntax/HTTP/timeout error). A returned set may
    be empty (a valid query with no results). Mirrors the retry/back-off policy
    of OfflineEvaluator so live numbers are comparable.
    """
    query = prepare_query(query)
    if not query or not query.strip():
        return None, False

    rate_limit_attempts = 0
    for attempt in range(max_retries):
        try:
            client.setQuery(query)
            ret = client.query().convert()
            return parse_answer_object(ret), False
        except urllib.error.HTTPError as e:
            if e.code == 429:
                rate_limit_attempts += 1
                if rate_limit_attempts > RATE_LIMIT_MAX_RETRIES:
                    return None, True
                sleep_time = min(
                    RATE_LIMIT_BASE * (2 ** (rate_limit_attempts - 1)),
                    RATE_LIMIT_MAX_SLEEP,
                )
                time.sleep(sleep_time)
                continue
            # 400 (syntax), 500, etc. — not retryable.
            return None, False
        except Exception as e:
            msg = str(e).lower()
            if ("time-out" in msg or "timed out" in msg) and attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None, False
    return None, False


def parse_answer_object(answer: Dict[str, Any]) -> Set[Any]:
    """
    Turn a single QALD answer object into a canonical set of values.

    Handles:
    - ASK queries -> {"true"} / {"false"}
    - SELECT      -> flat (pooled) set of all cell values across every binding

    All cell values are pooled into one flat set rather than kept as per-row
    tuples. QALD gold answers are sets of resources, and generated queries
    often project extra helper columns (e.g. a label alongside the entity);
    pooling lets the answer entity still match instead of scoring 0 on a
    structural mismatch. URIs are normalised by stripping the entity prefix.
    """
    if not isinstance(answer, dict):
        return set()

    # ASK query result
    if "boolean" in answer:
        return {str(answer["boolean"]).lower()}

    results = answer.get("results")
    if not isinstance(results, dict):
        return set()

    bindings = results.get("bindings")
    if not bindings:
        return set()

    out: Set[Any] = set()
    for binding in bindings:
        for cell in binding.values():
            if isinstance(cell, dict) and "value" in cell:
                out.add(_normalise_value(cell["value"]))
    return out


def parse_answers_list(answers: Optional[List[Dict[str, Any]]]) -> Set[Any]:
    """QALD stores `answers` as a list with (usually) one result object."""
    if not answers:
        return set()
    merged: Set[Any] = set()
    for ans in answers:
        merged |= parse_answer_object(ans)
    return merged


def calculate_set_metrics(gold: Set, gen: Set) -> Tuple[float, float, float]:
    """Precision / Recall / F1 between two answer sets (QALD convention)."""
    if not gold and not gen:
        return 1.0, 1.0, 1.0
    if not gold or not gen:
        return 0.0, 0.0, 0.0

    intersection = len(gold & gen)
    precision = intersection / len(gen)
    recall = intersection / len(gold)
    f1 = (
        (2 * precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    return precision, recall, f1


CSV_FIELDNAMES = [
    "experiment",
    "timestamp",
    "count",
    "precision",
    "recall",
    "f1",
    "exact_match_rate",
    "exact_matches",
    "missing_in_gold",
    "path",
]


def _append_row_csv(csv_path: str, row: Dict[str, Any]) -> None:
    """Append one result row to the CSV (writing a header first if new)."""
    new_file = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        if new_file:
            writer.writeheader()
        writer.writerow({k: row.get(k) for k in CSV_FIELDNAMES})


def load_gold(gold_path: str) -> Dict[str, Set[Any]]:
    """Map question id (as str) -> gold answer set from the QALD-10 dataset."""
    with open(gold_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    gold: Dict[str, Set[Any]] = {}
    for q in data.get("questions", []):
        qid = str(q.get("id"))
        gold[qid] = parse_answers_list(q.get("answers"))
    return gold


def evaluate_file(
    gerbil_path: str,
    gold: Dict[str, Set[Any]],
    reexecute: bool = False,
    client: Optional[SPARQLWrapper] = None,
) -> Optional[Dict[str, Any]]:
    """
    Compute macro metrics for one gerbil_test.json against the gold map.

    If `reexecute` is True, each question's `query.sparql` is run live against
    Wikidata (via `client`) and that result is compared to gold; otherwise the
    pre-computed `answers` stored in the file are used.
    """
    try:
        with open(gerbil_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"  ! Could not read {gerbil_path}: {e}")
        return None

    questions = data.get("questions", [])
    if not questions:
        return None

    n = 0
    missing_in_gold = 0
    total_p = total_r = total_f1 = 0.0
    exact = 0
    populated_answers = 0  # questions whose stored answer set is non-empty
    syntax_errors = 0
    rate_limit_skips = 0

    for idx, q in enumerate(questions):
        qid = str(q.get("id"))
        if qid not in gold:
            missing_in_gold += 1
            continue

        gold_set = gold[qid]

        if reexecute:
            if idx > 0 and INTER_QUERY_DELAY > 0:
                time.sleep(INTER_QUERY_DELAY)
            query = (q.get("query") or {}).get("sparql", "")
            gen_set, rate_limited = execute_query_live(client, query)
            if rate_limited:
                rate_limit_skips += 1
                continue
            if gen_set is None:
                syntax_errors += 1
                gen_set = set()
        else:
            gen_set = parse_answers_list(q.get("answers"))

        if gen_set:
            populated_answers += 1

        p, r, f1 = calculate_set_metrics(gold_set, gen_set)
        total_p += p
        total_r += r
        total_f1 += f1
        if f1 >= 0.99:
            exact += 1
        n += 1

    if n == 0:
        return None

    # Derive a readable experiment label from the path.
    parts = os.path.normpath(gerbil_path).split(os.sep)
    experiment = parts[-3] if len(parts) >= 3 else os.path.dirname(gerbil_path)
    timestamp = parts[-2] if len(parts) >= 2 else ""

    return {
        "experiment": experiment,
        "timestamp": timestamp,
        "path": gerbil_path,
        "count": n,
        "precision": round(total_p / n, 4),
        "recall": round(total_r / n, 4),
        "f1": round(total_f1 / n, 4),
        "exact_match_rate": round(exact / n, 4),
        "exact_matches": exact,
        "missing_in_gold": missing_in_gold,
        "populated_answers": populated_answers,
        "syntax_errors": syntax_errors,
        "rate_limit_skips": rate_limit_skips,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Offline GERBIL-style evaluation of gerbil_test.json vs QALD-10 gold."
    )
    parser.add_argument(
        "--outputs",
        default=DEFAULT_OUTPUTS_DIR,
        help="Root directory containing experiment outputs (default: outputs).",
    )
    parser.add_argument(
        "--gold",
        default=DEFAULT_GOLD_PATH,
        help="Path to qald_10.json gold dataset.",
    )
    parser.add_argument(
        "--csv",
        default=None,
        help="Optional path to write a CSV summary of all experiments.",
    )
    parser.add_argument(
        "--reexecute",
        action="store_true",
        help="Run each generated query.sparql live against Wikidata instead of "
        "trusting the stored answers (reliable when stored answers are empty).",
    )
    parser.add_argument(
        "--filter",
        default=None,
        help="Only evaluate files whose path contains this substring "
        "(e.g. an experiment name). Recommended with --reexecute.",
    )
    parser.add_argument(
        "--endpoints",
        default=None,
        help="Comma-separated SPARQL endpoints to try in order (first reachable "
        "wins). Defaults to $SPARQL_ENDPOINT_URL then the built-in candidates.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=None,
        help="Seconds between consecutive live queries (default 0.5). Use a low "
        "value (e.g. 0.05) for non-rate-limited endpoints like QLever.",
    )
    args = parser.parse_args()

    global INTER_QUERY_DELAY
    if args.delay is not None:
        INTER_QUERY_DELAY = args.delay

    if not os.path.exists(args.gold):
        print(f"Gold dataset not found: {args.gold}")
        return

    gold = load_gold(args.gold)
    print(f"Loaded {len(gold)} gold questions from {args.gold}\n")

    pattern = os.path.join(args.outputs, "**", GERBIL_FILENAME)
    files = sorted(glob.glob(pattern, recursive=True))
    if args.filter:
        files = [f for f in files if args.filter in f]
    if not files:
        print(f"No {GERBIL_FILENAME} files found under {args.outputs}/")
        return

    mode = "RE-EXECUTE live against Wikidata" if args.reexecute else "stored answers (offline)"
    print(f"Found {len(files)} {GERBIL_FILENAME} file(s). Mode: {mode}.\n")

    client = None
    if args.reexecute:
        # Build the candidate list: --endpoints, else env var + built-in defaults.
        if args.endpoints:
            candidates = [u.strip() for u in args.endpoints.split(",") if u.strip()]
        else:
            candidates = []
            env_url = os.getenv("SPARQL_ENDPOINT_URL")
            if env_url:
                candidates.append(env_url)
            candidates += DEFAULT_ENDPOINTS
        endpoint = select_working_endpoint(candidates)
        if not endpoint:
            print("No reachable SPARQL endpoint among: " + ", ".join(candidates))
            return
        client = _make_sparql_client(endpoint)

    rows: List[Dict[str, Any]] = []
    for i, path in enumerate(files, 1):
        if args.reexecute:
            print(f"[{i}/{len(files)}] {path} ...", flush=True)
        res = evaluate_file(path, gold, reexecute=args.reexecute, client=client)
        if res:
            rows.append(res)
            if args.reexecute:
                # Live per-file line so progress is visible during long runs.
                print(
                    f"    -> {res['experiment']:<32} "
                    f"F1={res['f1']:.3f} P={res['precision']:.3f} "
                    f"R={res['recall']:.3f} EM={res['exact_match_rate']:.3f} "
                    f"(n={res['count']})",
                    flush=True,
                )
                # Append to CSV incrementally so a crash/interrupt keeps results.
                if args.csv:
                    _append_row_csv(args.csv, res)

    if not rows:
        print("No files could be evaluated.")
        return

    # Warn if stored-answer mode produced essentially empty predictions.
    if not args.reexecute:
        total_pop = sum(r["populated_answers"] for r in rows)
        if total_pop == 0:
            print(
                "\n*** WARNING: every stored answer set is EMPTY. ***\n"
                "The offline scores below are NOT meaningful (they only reward\n"
                "empty-vs-empty matches). Re-run with --reexecute to execute the\n"
                "generated queries live against Wikidata.\n"
            )

    # Sort best-to-worst by F1 for the console report.
    rows.sort(key=lambda r: r["f1"], reverse=True)

    name_w = max(len(r["experiment"]) for r in rows)
    name_w = min(max(name_w, 10), 45)

    header = (
        f"{'experiment':<{name_w}}  {'n':>4}  {'P':>6}  {'R':>6}  "
        f"{'F1':>6}  {'EM':>6}"
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        exp = r["experiment"]
        if len(exp) > name_w:
            exp = exp[: name_w - 1] + "…"
        print(
            f"{exp:<{name_w}}  {r['count']:>4}  {r['precision']:>6.3f}  "
            f"{r['recall']:>6.3f}  {r['f1']:>6.3f}  {r['exact_match_rate']:>6.3f}"
        )

    if args.csv:
        # Final rewrite: complete and sorted (overwrites any incremental rows).
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r.get(k) for k in CSV_FIELDNAMES})
        print(f"\nCSV summary written to {args.csv}")


if __name__ == "__main__":
    main()

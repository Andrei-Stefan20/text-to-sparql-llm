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
import threading
import time
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Set, Tuple

from rich.table import Table
from SPARQLWrapper import JSON, SPARQLWrapper

from src.utils.progress import console, make_progress

WIKIDATA_ENTITY_PREFIX = "http://www.wikidata.org/entity/"

DEFAULT_OUTPUTS_DIR = "outputs"
DEFAULT_GOLD_PATH = os.path.join(
    "data", "raw", "QALD-10", "data", "qald_10", "qald_10.json"
)
GERBIL_FILENAME = "gerbil_test.json"


# Candidate endpoints probed at startup; every reachable one is kept and the
# evaluator rotates across them (round-robin, with fail-over). Override /
# prepend with --endpoints or the SPARQL_ENDPOINT_URL env var.
DEFAULT_ENDPOINTS = [
    "https://query.wikidata.org/sparql",  # official WDQS (may be throttled)
    "https://qlever.cs.uni-freiburg.de/api/wikidata",  # fast public mirror
    "https://wikidata.demo.openlinksw.com/sparql",  # OpenLink Virtuoso mirror
]
# Unreachable / data-partial candidates are dropped at the startup probe, so it
# is safe to list extras here. NOT included: query-main / query-scholarly
# (Wikidata's graph-split endpoints) — each holds only part of the graph, so
# they would return incomplete answer sets for the other half of the queries.

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

# Matches a `SERVICE wikibase:label { ... }` block, tolerating one level of
# nested braces inside it (e.g. inline blank-node syntax).
_LABEL_SERVICE_RE = re.compile(
    r"SERVICE\s+wikibase:label\s*\{(?:[^{}]|\{[^{}]*\})*\}",
    re.IGNORECASE | re.DOTALL,
)

# Prefix declarations present in a query, e.g. `PREFIX wdt:` -> "wdt".
_PREFIX_DECL_RE = re.compile(r"(?i)\bPREFIX\s+([A-Za-z][\w.-]*)\s*:")

# name -> full declaration line, derived from STANDARD_PREFIXES.
_STANDARD_PREFIX_LINES = {
    line.split()[1].rstrip(":"): line
    for line in STANDARD_PREFIXES.strip().splitlines()
}

# Live re-execution tuning (only used with --reexecute). The delay applies
# per worker thread, so the aggregate rate is roughly workers / delay.
INTER_QUERY_DELAY = 0.5
RATE_LIMIT_MAX_RETRIES = 6
RATE_LIMIT_BASE = 2.0
RATE_LIMIT_MAX_SLEEP = 60.0

# Endpoint rotation tuning.
# When a mirror returns a rate-limit it is "exhausted": pulled out of the
# rotation for this many seconds so traffic shifts to the healthy mirror(s).
ENDPOINT_COOLDOWN = 30.0
# After the main pass, queries still rate-limited / transient are retried in a
# few extra rounds (cooldowns expire, flaky endpoints recover) before being
# left for the next run.
RETRY_ROUNDS = 2


def _normalise_value(value: str) -> str:
    """Strip the Wikidata entity prefix so URIs compare equal across sources."""
    return value.replace(WIKIDATA_ENTITY_PREFIX, "")


def prepare_query(query: str, strip_label_service: bool = True) -> str:
    """
    Make a generated query portable across engines.

    - Removes `SERVICE wikibase:label {...}` blocks: only WDQS implements them,
      and they only add label columns (the answer entity is still returned).
    - Prepends the standard Wikidata prefixes the query does not declare
      itself, so partially-prefixed queries also run on engines that don't
      predefine them. Idempotent: a second call adds nothing.
    """
    if not query:
        return query
    out = query
    if strip_label_service:
        out = _LABEL_SERVICE_RE.sub(" ", out)
    declared = {m.group(1) for m in _PREFIX_DECL_RE.finditer(out)}
    missing = [
        line for name, line in _STANDARD_PREFIX_LINES.items() if name not in declared
    ]
    if missing:
        out = "\n".join(missing) + "\n" + out
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


def select_working_endpoints(candidates: List[str]) -> List[str]:
    """
    Probe every candidate and return all endpoints that answer a trivial probe
    query without a connection error or rate-limit, preserving input order.

    The evaluator rotates across the returned list (round-robin, with fail-over
    to the next mirror on a rate-limit or transient error), so spreading the
    load over several endpoints raises throughput and reduces 429s.
    """
    probe = (
        STANDARD_PREFIXES
        + "SELECT ?p WHERE { wd:Q761383 wdt:P138 ?p . } LIMIT 1"
    )
    working: List[str] = []
    for url in candidates:
        if not url:
            continue
        client = _make_sparql_client(url)
        try:
            client.setQuery(probe)
            client.query().convert()
            print(f"  [endpoint] OK   {url}")
            working.append(url)
        except urllib.error.HTTPError as e:
            print(f"  [endpoint] skip {url} -> HTTP {e.code}")
        except Exception as e:
            print(f"  [endpoint] skip {url} -> {type(e).__name__}")
    return working


def execute_query_live(
    client: SPARQLWrapper, query: str, max_retries: int = 3
) -> Tuple[Optional[Set[Any]], str]:
    """
    Execute a SPARQL query, returning (answer_set_or_None, status).

    status is one of:
      "ok"        — executed; the set may be empty (valid query, no results).
      "error"     — definitive failure (HTTP 400, i.e. a syntax error):
                    safe to cache permanently.
      "rl"        — persistent rate-limit after all back-off retries.
      "transient" — timeout / 5xx / network error: retryable on the next run,
                    must NOT be cached as a permanent failure.
    """
    query = prepare_query(query)
    if not query or not query.strip():
        return None, "error"

    rate_limit_attempts = 0
    for attempt in range(max_retries):
        try:
            client.setQuery(query)
            ret = client.query().convert()
            return parse_answer_object(ret), "ok"
        except urllib.error.HTTPError as e:
            if e.code == 429:
                rate_limit_attempts += 1
                if rate_limit_attempts > RATE_LIMIT_MAX_RETRIES:
                    return None, "rl"
                sleep_time = min(
                    RATE_LIMIT_BASE * (2 ** (rate_limit_attempts - 1)),
                    RATE_LIMIT_MAX_SLEEP,
                )
                time.sleep(sleep_time)
                continue
            if e.code == 400:
                # Malformed query: deterministic, cacheable.
                return None, "error"
            # 403/5xx etc. — endpoint trouble, not the query's fault.
            return None, "transient"
        except Exception as e:
            msg = str(e).lower()
            if ("time-out" in msg or "timed out" in msg) and attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None, "transient"
    return None, "transient"


# Matches an existing LIMIT clause so the safety cap is only added when absent.
_LIMIT_RE = re.compile(r"\bLIMIT\s+\d+", re.IGNORECASE)


class LiveExecutor:
    """
    Executes prepared queries against one or more endpoints with a persistent
    disk cache and optional thread parallelism.

    When several endpoints are given they are used in round-robin (a per-query
    atomic counter picks the starting mirror); a query that hits a rate-limit
    or transient failure on one endpoint is retried on the next before being
    recorded as skipped. A definitive (syntax) error is only recorded when
    *every* endpoint rejects the query, so a query valid on at least one mirror
    is never lost to another mirror's stricter parser.

    The cache maps the *prepared* query string (without the safety LIMIT cap)
    to an entry:
      {"v": [...], "cap": N, "ep": url}  — success (cap/endpoint it ran with)
      {"err": true, "ep": url}           — definitive failure (syntax error)
    Rate-limited and transient failures (timeout/5xx/network) are never
    cached, so they are retried automatically on the next run. Legacy cache
    entries (cap baked into the key, no metadata) are migrated on lookup;
    legacy error entries are re-executed once, since the old format could not
    distinguish a syntax error from a transient timeout.
    """

    def __init__(
        self,
        endpoints: List[str],
        cache_path: Optional[str] = None,
        workers: int = 1,
        limit_cap: int = 0,
        cooldown: float = ENDPOINT_COOLDOWN,
        retry_rounds: int = RETRY_ROUNDS,
    ):
        # Accept a bare string for convenience, but normalise to a list.
        self.endpoints = [endpoints] if isinstance(endpoints, str) else list(endpoints)
        if not self.endpoints:
            raise ValueError("LiveExecutor requires at least one endpoint")
        self.cache_path = cache_path
        self.workers = max(1, workers)
        self.limit_cap = limit_cap
        self.cooldown = cooldown
        self.retry_rounds = max(0, retry_rounds)
        self._local = threading.local()
        self._lock = threading.Lock()
        self._rr_lock = threading.Lock()
        self._rr_index = 0
        # endpoint -> epoch time until which it is "exhausted" (skipped).
        self._ep_lock = threading.Lock()
        self._cooldown_until: Dict[str, float] = {ep: 0.0 for ep in self.endpoints}
        # Live counters for the current pass, shown in the progress bar.
        self._stats: Dict[str, int] = {"ok": 0, "err": 0, "rl": 0, "tr": 0}
        self._label = ""
        self._transient: Dict[str, Dict[str, Any]] = {}
        self._progress: Optional[Any] = None
        self._task_id: Optional[Any] = None
        self.cache: Dict[str, Dict[str, Any]] = {}
        if cache_path and os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                print(f"  [cache] loaded {len(self.cache)} cached queries from {cache_path}")
            except (OSError, json.JSONDecodeError):
                self.cache = {}

    def _client(self, endpoint: str) -> SPARQLWrapper:
        """Thread-local SPARQLWrapper, one per endpoint, created on first use."""
        clients = getattr(self._local, "clients", None)
        if clients is None:
            clients = self._local.clients = {}
        client = clients.get(endpoint)
        if client is None:
            client = clients[endpoint] = _make_sparql_client(endpoint)
        return client

    def _next_index(self) -> int:
        """Round-robin starting index for the next query, advanced atomically."""
        with self._rr_lock:
            idx = self._rr_index
            self._rr_index += 1
            return idx

    def _endpoint_order(self, start: int) -> List[str]:
        """
        Endpoints to attempt for one query, best first: healthy mirrors (in
        round-robin order from `start`) before any in cooldown. Cooling mirrors
        are kept as a last resort so a query is never stranded when every
        endpoint is briefly exhausted.
        """
        n = len(self.endpoints)
        rotated = [self.endpoints[(start + i) % n] for i in range(n)]
        now = time.time()
        with self._ep_lock:
            healthy = [e for e in rotated if self._cooldown_until[e] <= now]
            cooling = [e for e in rotated if self._cooldown_until[e] > now]
        return healthy + cooling

    def _mark_exhausted(self, endpoint: str) -> None:
        """Pull a rate-limited endpoint out of rotation for the cooldown window."""
        with self._ep_lock:
            self._cooldown_until[endpoint] = time.time() + self.cooldown

    def _status_text(self) -> str:
        """Live progress description: current pass label + outcome counters."""
        s = self._stats
        return (
            f"{self._label}  [green]ok {s['ok']}[/] [red]err {s['err']}[/] "
            f"[yellow]rl {s['rl']}[/] [dim]tr {s['tr']}[/]"
        )

    def prepare(self, query: str) -> str:
        """Canonical (cache-key) form: portable query, without the safety cap."""
        return prepare_query(query)

    def _capped(self, prepared: str) -> str:
        """Execution form: adds `LIMIT N` to SELECTs lacking one (if cap > 0)."""
        if (
            self.limit_cap > 0
            and prepared
            and "select" in prepared.lower()
            and not _LIMIT_RE.search(prepared)
        ):
            return prepared.rstrip() + f"\nLIMIT {self.limit_cap}"
        return prepared

    def _usable(self, entry: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Decide whether a cache entry is reusable under the current settings.

        Success entries are valid if produced without a cap, with the same cap,
        or if the result was not truncated (len < cap, so any cap would have
        returned the same set). Error entries are valid only in the new format
        ("ep" present): legacy errors may actually have been timeouts.
        """
        if entry is None or entry.get("rl") or entry.get("tr"):
            return None
        if entry.get("err"):
            return entry if "ep" in entry else None
        cap = entry.get("cap", 0)
        if cap == 0 or cap == self.limit_cap or len(entry.get("v", [])) < cap:
            return entry
        return None

    def _cached(self, prepared: str) -> Optional[Dict[str, Any]]:
        """Look up a usable entry, migrating legacy capped-key entries."""
        entry = self._usable(self.cache.get(prepared))
        if entry is not None:
            return entry
        # Legacy format: the safety cap used to be baked into the key.
        if self.limit_cap > 0:
            legacy_key = prepared.rstrip() + f"\nLIMIT {self.limit_cap}"
            legacy = self.cache.pop(legacy_key, None)
            if legacy is not None:
                migrated = dict(legacy)
                migrated.setdefault("cap", self.limit_cap)
                self.cache[prepared] = migrated
                return self._usable(migrated)
        return None

    def save_cache(self) -> None:
        if not self.cache_path:
            return
        with self._lock:
            tmp = self.cache_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.cache, f)
            os.replace(tmp, self.cache_path)

    def _execute_uncached(self, prepared: str) -> None:
        if INTER_QUERY_DELAY > 0:
            time.sleep(INTER_QUERY_DELAY)
        capped = self._capped(prepared)
        # Try the endpoints best-first (healthy before cooling, round-robin from
        # a per-query offset). Stop on the first "ok"; on a rate-limit pull that
        # mirror out of rotation and fall over to the next. Only call it a
        # definitive error if *every* endpoint rejected it (a single mirror's
        # stricter parser must not lose a query another mirror would answer).
        order = self._endpoint_order(self._next_index())
        gen_set: Optional[Set[Any]] = None
        seen: List[str] = []
        used_ep = order[0]
        status = "transient"
        for ep in order:
            used_ep = ep
            gen_set, status = execute_query_live(self._client(ep), capped)
            if status == "rl":
                self._mark_exhausted(ep)
            if status == "ok":
                break
            seen.append(status)
        if status != "ok":
            if seen and all(s == "error" for s in seen):
                status = "error"
            elif "rl" in seen:
                status = "rl"
            else:
                status = "transient"
        entry: Dict[str, Any]
        if status == "ok":
            entry = {
                "v": sorted(str(x) for x in gen_set),
                "cap": self.limit_cap,
                "ep": used_ep,
            }
        elif status == "error":
            entry = {"err": True, "ep": used_ep}
        elif status == "rl":
            entry = {"rl": True}
        else:
            # Transient (timeout/5xx/network): never cached, retried next run.
            entry = {"tr": True}
        stat_key = {"ok": "ok", "error": "err", "rl": "rl", "transient": "tr"}[status]
        with self._lock:
            if status in ("ok", "error"):
                self.cache[prepared] = entry
            self._transient[prepared] = entry
            self._stats[stat_key] += 1
            if self._progress is not None:
                self._progress.update(
                    self._task_id, description=self._status_text()
                )
                self._progress.advance(self._task_id)

    def _pending(self, queries: List[str]) -> List[str]:
        """Queries left rate-limited / transient (retryable) after a pass."""
        return sorted(
            pq
            for pq in queries
            if (self._transient.get(pq) or {}).get("rl")
            or (self._transient.get(pq) or {}).get("tr")
        )

    def _run_pool(self, label: str, queries: List[str]) -> None:
        """Execute `queries` in a worker pool under a fresh progress bar."""
        self._label = label
        self._stats = {"ok": 0, "err": 0, "rl": 0, "tr": 0}
        with make_progress() as progress:
            self._progress = progress
            self._task_id = progress.add_task(self._status_text(), total=len(queries))
            try:
                with ThreadPoolExecutor(max_workers=self.workers) as pool:
                    list(pool.map(self._execute_uncached, queries))
            finally:
                self._progress = None
                self._task_id = None

    def run_many(self, queries: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Execute every distinct query (via cache when possible).

        Returns a map from the *original* query string to a result entry:
        {"v": [...]} on success, {"err": True} on definitive failure,
        {"rl": True} / {"tr": True} when skipped (rate-limit / transient).
        """
        prepared_by_query = {q: self.prepare(q) for q in set(queries)}
        self._transient: Dict[str, Dict[str, Any]] = {}
        todo = sorted(
            {
                pq
                for pq in prepared_by_query.values()
                if pq and self._cached(pq) is None
            }
        )
        cached_hits = len({pq for pq in prepared_by_query.values() if pq}) - len(todo)
        if todo:
            if cached_hits:
                console.print(f"    [dim]\\[cache] {cached_hits} query riusate dalla cache[/]")
            self._run_pool("Esecuzione query", todo)
            # Extra passes for queries still rate-limited / transient: endpoint
            # cooldowns expire and flaky mirrors recover, so a couple of rounds
            # reclaim most of them without re-running the whole experiment.
            for round_num in range(1, self.retry_rounds + 1):
                pending = self._pending(todo)
                if not pending:
                    break
                wait = min(RATE_LIMIT_MAX_SLEEP, 5.0 * round_num)
                console.print(
                    f"    [yellow]\\[retry {round_num}/{self.retry_rounds}] "
                    f"{len(pending)} query da riprovare fra {wait:.0f}s[/]"
                )
                time.sleep(wait)
                self._run_pool(f"Retry {round_num}/{self.retry_rounds}", pending)
            leftover = self._pending(todo)
            if leftover:
                console.print(
                    f"    [yellow]! {len(leftover)} query ancora irrisolte "
                    f"(rate-limit/transient) — verranno riprovate al prossimo run[/]"
                )
        else:
            console.print(
                f"    [dim]\\[cache] tutte le {cached_hits} query riusate dalla cache[/]"
            )
        # Always persist: lookups may have migrated legacy entries in place.
        self.save_cache()
        out: Dict[str, Dict[str, Any]] = {}
        for q, pq in prepared_by_query.items():
            if not pq:
                out[q] = {"err": True}
            else:
                out[q] = self._transient.get(pq) or self._cached(pq) or {"rl": True}
        return out


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


def _write_csv_merged(csv_path: str, rows: List[Dict[str, Any]]) -> None:
    """
    Rewrite the CSV merging this run's rows with any pre-existing ones.

    Rows are keyed by `path`: the current run overwrites its own experiments
    (including the incremental rows appended during the run) but never erases
    results of experiments evaluated in previous runs with other --filter.
    """
    merged: Dict[str, Dict[str, Any]] = {}
    if os.path.exists(csv_path):
        try:
            with open(csv_path, "r", newline="", encoding="utf-8") as f:
                for old in csv.DictReader(f):
                    if old.get("path"):
                        merged[old["path"]] = {
                            k: old.get(k) for k in CSV_FIELDNAMES
                        }
        except (OSError, csv.Error):
            pass
    for r in rows:
        merged[r["path"]] = {k: r.get(k) for k in CSV_FIELDNAMES}

    def _f1(row: Dict[str, Any]) -> float:
        try:
            return float(row.get("f1") or 0.0)
        except (TypeError, ValueError):
            return 0.0

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for row in sorted(merged.values(), key=_f1, reverse=True):
            writer.writerow(row)


def load_gold(gold_path: str) -> Tuple[Dict[str, Set[Any]], Dict[str, str]]:
    """
    Load the QALD-10 gold, returning two maps keyed by question id (as str):

    - answers:  the frozen gold answer set shipped with the dataset.
    - queries:  the gold `query.sparql`, used as a fallback to recompute the
                answers live for any question whose stored answer set is empty
                (e.g. answers absent from the dataset, or gold that drifted to
                empty), so evaluation never scores against a missing gold.
    """
    with open(gold_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    gold: Dict[str, Set[Any]] = {}
    gold_queries: Dict[str, str] = {}
    for q in data.get("questions", []):
        qid = str(q.get("id"))
        gold[qid] = parse_answers_list(q.get("answers"))
        sparql = (q.get("query") or {}).get("sparql", "")
        if sparql:
            gold_queries[qid] = sparql
    return gold, gold_queries


def evaluate_file(
    gerbil_path: str,
    gold: Dict[str, Set[Any]],
    reexecute: bool = False,
    executor: Optional["LiveExecutor"] = None,
) -> Optional[Dict[str, Any]]:
    """
    Compute macro metrics for one gerbil_test.json against the gold map.

    If `reexecute` is True, each question's `query.sparql` is run live against
    Wikidata (via `executor`, cached and possibly parallel) and that result is
    compared to gold; otherwise the pre-computed `answers` stored in the file
    are used.
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

    live_results: Dict[str, Dict[str, Any]] = {}
    if reexecute:
        all_queries = [
            (q.get("query") or {}).get("sparql", "")
            for q in questions
            if str(q.get("id")) in gold
        ]
        live_results = executor.run_many(all_queries)

    for q in questions:
        qid = str(q.get("id"))
        if qid not in gold:
            missing_in_gold += 1
            continue

        gold_set = gold[qid]

        if reexecute:
            query = (q.get("query") or {}).get("sparql", "")
            entry = live_results.get(query, {"err": True})
            if entry.get("rl") or entry.get("tr"):
                # Rate-limited or transient endpoint failure: cannot be scored
                # fairly, excluded from n and retried on the next run.
                rate_limit_skips += 1
                continue
            if entry.get("err"):
                syntax_errors += 1
                gen_set: Set[Any] = set()
            else:
                gen_set = set(entry.get("v", []))
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
        help="Comma-separated SPARQL endpoints. Every reachable one is kept and "
        "queries are rotated across them (round-robin + fail-over). Defaults to "
        "$SPARQL_ENDPOINT_URL then the built-in candidates.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=None,
        help="Seconds between consecutive live queries (default 0.5). Use a low "
        "value (e.g. 0.05) for non-rate-limited endpoints like QLever.",
    )
    parser.add_argument(
        "--cache",
        default=None,
        help="Path to a persistent JSON query-result cache. Identical generated "
        "queries across runs are executed only once.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Parallel query workers (default 1). Use 4-8 with QLever.",
    )
    parser.add_argument(
        "--limit-cap",
        type=int,
        default=0,
        help="Append `LIMIT N` to SELECT queries lacking one, to prevent "
        "runaway/timeout queries (0 = off). Gold answers are small, so a "
        "generous cap (e.g. 5000) does not change the metrics.",
    )
    parser.add_argument(
        "--cooldown",
        type=float,
        default=ENDPOINT_COOLDOWN,
        help=f"Seconds a rate-limited endpoint is pulled out of rotation before "
        f"being retried (default {ENDPOINT_COOLDOWN:.0f}). Only relevant with "
        f"multiple endpoints.",
    )
    parser.add_argument(
        "--retry-rounds",
        type=int,
        default=RETRY_ROUNDS,
        help=f"Extra passes to retry queries still rate-limited/transient after "
        f"the main run, before leaving them for the next run "
        f"(default {RETRY_ROUNDS}; 0 = off).",
    )
    args = parser.parse_args()

    global INTER_QUERY_DELAY
    if args.delay is not None:
        INTER_QUERY_DELAY = args.delay

    if not os.path.exists(args.gold):
        print(f"Gold dataset not found: {args.gold}")
        return

    gold, gold_queries = load_gold(args.gold)
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

    executor = None
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
        endpoints = select_working_endpoints(candidates)
        if not endpoints:
            print("No reachable SPARQL endpoint among: " + ", ".join(candidates))
            return
        if len(endpoints) > 1:
            print(f"  [endpoint] rotating across {len(endpoints)} endpoints")
        executor = LiveExecutor(
            endpoints,
            cache_path=args.cache,
            workers=args.workers,
            limit_cap=args.limit_cap,
            cooldown=args.cooldown,
            retry_rounds=args.retry_rounds,
        )

        # Hybrid gold: trust the dataset's frozen answers, but for any question
        # whose stored answer set is empty, recompute it by executing the gold
        # query live — so a generated query is never compared to a missing gold.
        unresolved = [qid for qid, ans in gold.items() if not ans and qid in gold_queries]
        if unresolved:
            console.print(
                f"  [gold] {len(unresolved)} risposta/e gold assenti nel dataset: "
                f"eseguo le query gold dal vivo"
            )
            gold_res = executor.run_many([gold_queries[qid] for qid in unresolved])
            filled = 0
            for qid in unresolved:
                entry = gold_res.get(gold_queries[qid], {})
                if entry.get("v"):
                    gold[qid] = set(entry["v"])
                    filled += 1
            console.print(f"  [gold] risolte {filled}/{len(unresolved)} dal vivo")

    rows: List[Dict[str, Any]] = []
    for i, path in enumerate(files, 1):
        if args.reexecute:
            console.print(f"[bold]\\[{i}/{len(files)}][/] {path} ...")
        res = evaluate_file(path, gold, reexecute=args.reexecute, executor=executor)
        if res:
            rows.append(res)
            if args.reexecute:
                # Live per-file line so progress is visible during long runs.
                console.print(
                    f"    -> [bold]{res['experiment']:<32}[/] "
                    f"F1=[green]{res['f1']:.3f}[/] P={res['precision']:.3f} "
                    f"R={res['recall']:.3f} EM={res['exact_match_rate']:.3f} "
                    f"(n={res['count']})"
                )
                # Append to CSV incrementally so a crash/interrupt keeps results.
                if args.csv:
                    _append_row_csv(args.csv, res)
            else:
                # Offline mode: per-file sanity check on the stored answers.
                pop, n = res["populated_answers"], res["count"]
                if pop == 0:
                    console.print(
                        f"    [yellow]! {res['experiment']}: tutte le risposte "
                        f"salvate sono vuote — punteggio non significativo, "
                        f"usa --reexecute[/]"
                    )
                elif pop < n / 2:
                    console.print(
                        f"    [yellow]! {res['experiment']}: solo {pop}/{n} "
                        f"risposte salvate non vuote — punteggio probabilmente "
                        f"sottostimato (timeout durante la generazione?)[/]"
                    )

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

    table = Table(title="GERBIL-style evaluation vs QALD-10 gold")
    table.add_column("experiment", style="bold", max_width=45, no_wrap=True)
    table.add_column("n", justify="right")
    table.add_column("P", justify="right")
    table.add_column("R", justify="right")
    table.add_column("F1", justify="right", style="green")
    table.add_column("EM", justify="right")
    for r in rows:
        table.add_row(
            r["experiment"],
            str(r["count"]),
            f"{r['precision']:.3f}",
            f"{r['recall']:.3f}",
            f"{r['f1']:.3f}",
            f"{r['exact_match_rate']:.3f}",
        )
    console.print(table)

    if args.csv:
        # Final rewrite: merges with existing rows (previous runs with other
        # --filter are preserved; this run's rows overwrite their duplicates).
        _write_csv_merged(args.csv, rows)
        console.print(f"\nCSV summary written to [bold]{args.csv}[/]")


if __name__ == "__main__":
    main()

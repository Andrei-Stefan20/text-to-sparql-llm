"""
GERBIL File Generator.

This script converts SPARQL query results into GERBIL-compatible QALD format for evaluation.

Features:
- Executes SPARQL queries against the Wikidata endpoint.
- Converts `results_full.json` files into GERBIL-compatible JSON.
- Supports batch processing of multiple result files.

Implementation:
- Uses `SPARQLWrapper` for query execution.
- Processes files recursively from the `outputs` directory.
- Handles query errors gracefully and provides default empty results.
"""

import glob
import json
import logging
import os
import re
import time
import urllib.error

from SPARQLWrapper import JSON, SPARQLWrapper

from src.evaluation.evaluate_gerbil_vs_qald import prepare_query
from src.utils.progress import console, make_progress

logger = logging.getLogger(__name__)

#  CONFIGURATION
ROOT_DIR = "outputs"
INPUT_FILENAME = "results_full.json"
OUTPUT_FILENAME = "gerbil_test.json"
WIKIDATA_ENDPOINT = os.getenv(
    "SPARQL_ENDPOINT_URL", "https://query.wikidata.org/sparql"
)
QUERY_TIMEOUT = 30
INTER_QUERY_DELAY = 0.1
RATE_LIMIT_RETRIES = 4
RATE_LIMIT_BASE_SLEEP = 2.0

EMPTY_SELECT = {"head": {"vars": []}, "results": {"bindings": []}}
EMPTY_ASK = {"head": {}, "boolean": False}

# Word-boundary matches so e.g. a variable named ?task is not mistaken for ASK.
_ASK_RE = re.compile(r"\bASK\b", re.IGNORECASE)
_SELECT_RE = re.compile(r"\bSELECT\b", re.IGNORECASE)

# SPARQL Client Configuration
sparql_client = SPARQLWrapper(WIKIDATA_ENDPOINT)
sparql_client.setReturnFormat(JSON)
sparql_client.setTimeout(QUERY_TIMEOUT)
sparql_client.addCustomHttpHeader("User-Agent", "TextToSparqlEvaluator/1.0")


def execute_sparql(query):
    """
    Executes the query on Wikidata to get the actual bindings required by GERBIL.

    Handles both SELECT queries (returning variable bindings) and ASK queries
    (returning a boolean), as QALD/GERBIL evaluates the two answer types
    differently. Retries with exponential back-off on HTTP 429; on any other
    failure returns the type-appropriate empty result.
    """
    if not query:
        return EMPTY_SELECT

    is_ask = bool(_ASK_RE.search(query)) and not _SELECT_RE.search(query)
    if not is_ask and not _SELECT_RE.search(query):
        return EMPTY_SELECT

    prepared = prepare_query(query)
    for attempt in range(RATE_LIMIT_RETRIES + 1):
        try:
            sparql_client.setQuery(prepared)
            return sparql_client.queryAndConvert()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < RATE_LIMIT_RETRIES:
                time.sleep(RATE_LIMIT_BASE_SLEEP * (2**attempt))
                continue
            logger.debug("Query failed (HTTP %s): %.120s", e.code, prepared)
            break
        except Exception as e:
            logger.debug("Query failed (%s): %.120s", type(e).__name__, prepared)
            break

    return EMPTY_ASK if is_ask else EMPTY_SELECT


def convert_single_file(file_path):
    """
    Converts a single results_full.json file into GERBIL format (QALD).
    """
    # Extract info from path (outputs/EXP_NAME/DATE_TIME/results_full.json)
    path_parts = os.path.normpath(file_path).split(os.sep)
    exp_name = path_parts[-3]
    timestamp = path_parts[-2]

    console.print(f"\n[bold]>>> Processing:[/] \\[{exp_name}] - {timestamp}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle different formats (direct list or object with "results" key)
        if isinstance(data, dict) and "results" in data:
            items = data["results"]
        elif isinstance(data, list):
            items = data
        else:
            console.print(f"[yellow]>>> Unrecognized format in {file_path}, skipping.[/]")
            return

        qald_questions = []

        with make_progress() as progress:
            bar = progress.add_task(f"Querying Wikidata ({timestamp})", total=len(items))
            for item in items:
                q_id = str(item.get("id", "0"))
                question_text = item.get("question", "")
                generated_sparql = item.get("generated_sparql", "")

                # Execute query to get real answers
                answers = execute_sparql(generated_sparql)
                time.sleep(INTER_QUERY_DELAY)

                # Construct QALD object
                qald_entry = {
                    "id": q_id,
                    "question": [{"string": question_text, "language": "en"}],
                    "query": {"sparql": generated_sparql},
                    "answers": [answers],  # GERBIL expects a list of result objects
                }
                qald_questions.append(qald_entry)
                progress.advance(bar)

        # Final structure
        final_json = {"questions": qald_questions}

        # Save in the same folder as the original file
        output_path = os.path.join(os.path.dirname(file_path), OUTPUT_FILENAME)

        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(final_json, out_f, indent=2)

        console.print(f"[green]Created:[/] {output_path}")

    except Exception as e:
        console.print(f"[red]Error processing {file_path}: {e}[/]")


def main():
    # Find all results_full.json files recursively
    search_pattern = os.path.join(ROOT_DIR, "*", "*", INPUT_FILENAME)
    found_files = glob.glob(search_pattern)

    if not found_files:
        console.print("No files found. Check that the 'outputs' folder exists.")
        return

    console.print(f"Found [bold]{len(found_files)}[/] experiments to process.")

    for file_path in found_files:
        convert_single_file(file_path)


if __name__ == "__main__":
    main()

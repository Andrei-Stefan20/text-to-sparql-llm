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
import os
import time
from datetime import datetime

from SPARQLWrapper import JSON, SPARQLWrapper
from tqdm import tqdm

# --- CONFIGURATION ---
ROOT_DIR = "outputs"
INPUT_FILENAME = "results_full.json"
OUTPUT_FILENAME = "gerbil_test.json"
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
WIKIDATA_ENDPOINT = os.getenv("SPARQL_ENDPOINT_URL", WIKIDATA_ENDPOINT)

# SPARQL Client Configuration
sparql_client = SPARQLWrapper(WIKIDATA_ENDPOINT)
sparql_client.setReturnFormat(JSON)
sparql_client.setTimeout(5)

sparql_client.addCustomHttpHeader(
    "User-Agent", "PhD-Thesis-Bot/1.0 (contact: your_email@example.com)"
)


def execute_sparql(query):
    """
    Executes the query on Wikidata to get the actual bindings required by GERBIL.
    """
    if not query or "SELECT" not in query.upper():
        return {"head": {"vars": []}, "results": {"bindings": []}}

    try:
        sparql_client.setQuery(query)
        return sparql_client.queryAndConvert()
    except Exception as e:
        return {"head": {"vars": []}, "results": {"bindings": []}}


def convert_single_file(file_path):
    """
    Converts a single results_full.json file into GERBIL format (QALD).
    """
    # Extract info from path (outputs/EXP_NAME/DATE_TIME/results_full.json)
    path_parts = os.path.normpath(file_path).split(os.sep)
    exp_name = path_parts[-3]
    timestamp = path_parts[-2]

    print(f"\n>>> Processing: [{exp_name}] - {timestamp}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle different formats (direct list or object with "results" key)
        if isinstance(data, dict) and "results" in data:
            items = data["results"]
        elif isinstance(data, list):
            items = data
        else:
            print(f">>> Unrecognized format in {file_path}, skipping.")
            return

        qald_questions = []

        # Progress bar for queries in this file
        for item in tqdm(items, desc=f"Querying Wikidata for {timestamp}", unit="q"):
            q_id = str(item.get("id", "0"))
            question_text = item.get("question", "")
            generated_sparql = item.get("generated_sparql", "")

            # Execute query to get real answers
            answers = execute_sparql(generated_sparql)
            time.sleep(0.1)  # Riduciamo un po' l'attesa visto che abbiamo il timeout

            # Construct QALD object
            qald_entry = {
                "id": q_id,
                "question": [{"string": question_text, "language": "en"}],
                "query": {"sparql": generated_sparql},
                "answers": [answers],  # GERBIL expects a list of result objects
            }
            qald_questions.append(qald_entry)

        # Final structure
        final_json = {"questions": qald_questions}

        # Save in the same folder as the original file
        output_path = os.path.join(os.path.dirname(file_path), OUTPUT_FILENAME)

        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(final_json, out_f, indent=2)

        print(f"Created: {output_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def main():
    # Find all results_full.json files recursively
    search_pattern = os.path.join(ROOT_DIR, "*", "*", INPUT_FILENAME)
    found_files = glob.glob(search_pattern)

    if not found_files:
        print("No files found. Check that the 'outputs' folder exists.")
        return

    print(f"Found {len(found_files)} experiments to process.")

    for file_path in found_files:
        convert_single_file(file_path)


if __name__ == "__main__":
    main()

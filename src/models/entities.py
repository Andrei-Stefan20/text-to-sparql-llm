import requests
import time
import logging
import re
from typing import List

logger = logging.getLogger(__name__)

ID_PATTERN = re.compile(r'\b([QP]\d+)\b')

def get_labels_for_ids(ids_list: List[str]) -> List[str]:
    """
    Retrieves labels for Q-IDs and P-IDs and formats them,
    separating Properties (predicates) and Entities (objects/subjects).
    """
    if not ids_list:
        return []
    
    ids = list(set(ids_list))
    chunk_size = 50
    
    items = []      # Q-ids
    properties = [] # P-ids
    
    headers = {"User-Agent": "TextToSparqlBot/1.0"}
    
    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i+chunk_size]
        ids_str = "|".join(chunk)
        
        params = {
            "action": "wbgetentities",
            "ids": ids_str,
            "format": "json",
            "props": "labels|descriptions",
            "languages": "en"
        }
        
        try:
            response = requests.get(
                "https://www.wikidata.org/w/api.php", 
                params=params, 
                headers=headers, 
                timeout=5
            )
            data = response.json()
            
            if "entities" in data:
                for qid, info in data["entities"].items():
                    label = info.get("labels", {}).get("en", {}).get("value", "No Label")
                    desc = info.get("descriptions", {}).get("en", {}).get("value", "No description")
                    
                    if qid.startswith("P"):
                        line = f"wdt:{qid} ({label}) - {desc}"
                        properties.append(line)
                    else:
                        line = f"wd:{qid} ({label}) - {desc}"
                        items.append(line)
            
            time.sleep(0.1) 
            
        except Exception as e:
            logger.warning(f"Wikidata API error for chunk {chunk}: {e}")
            
    output_lines = []
    
    if properties:
        output_lines.append("--- PROPERTIES (Relations) ---")
        output_lines.extend(properties)
        
    if items:
        output_lines.append("\n--- ENTITIES (Items/Objects) ---")
        output_lines.extend(items)
            
    return output_lines

def extract_gold_context(sparql_query: str) -> str:
    """
    Extracts entities and properties directly from the correct (gold) SPARQL query.
    Useful for creating the schema context in prompts.
    """
    if not sparql_query:
        return "No gold query available."
        
    found_ids = ID_PATTERN.findall(sparql_query)
    if not found_ids:
        return "No entities found in gold query."
        
    context_lines = get_labels_for_ids(found_ids)
    return "\n".join(context_lines)
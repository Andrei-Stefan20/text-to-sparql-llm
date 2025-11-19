import requests
import time
import logging

logger = logging.getLogger(__name__)

def search_wikidata_entities(keyword, limit=2):
    """Queries Wikidata API for entity candidates."""
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "language": "en",
        "format": "json",
        "search": keyword,
        "limit": limit
    }
    try:
        time.sleep(0.1) 
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        results = []
        for item in data.get('search', []):
            label = item.get('label', 'No Label')
            desc = item.get('description', '')
            qid = item.get('id')
            results.append(f"- {label} (ID: {qid}): {desc}")
        return results
    except Exception:
        return []

def extract_context(question):
    """Extracts potential entities from the question text."""
    keywords = [w for w in question.split() if len(w) > 3]
    keywords = keywords[:3] 
    
    context_lines = []
    for kw in keywords:
        candidates = search_wikidata_entities(kw)
        if candidates:
            context_lines.extend(candidates)
    
    return "\n".join(list(set(context_lines)))
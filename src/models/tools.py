import requests

def search_entity(query: str, type_filter: str = None) -> str:
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": query
    }
    if type_filter == "property":
        params["type"] = "property"
        
    try:
        data = requests.get(url, params=params).json()
        if data['search']:
            results = []
            for item in data['search'][:2]:
                results.append(f"{item['id']} ({item.get('label', 'No label')} - {item.get('description', 'No desc')})")
            return "Found: " + ", ".join(results)
        else:
            return "No results found."
    except Exception as e:
        return f"Error connecting to Wikidata: {e}"

def search_property(query: str) -> str:
    return search_entity(query, type_filter="property")
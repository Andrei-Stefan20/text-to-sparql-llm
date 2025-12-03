import re
import logging
from typing import Tuple, List, Optional, Dict
from SPARQLWrapper import SPARQLWrapper, JSON

logger = logging.getLogger(__name__)

class SPARQLClient:
    """
    Handles interactions with the Wikidata SPARQL Endpoint, 
    syntax validation, and metric calculation (F1).
    """
    def __init__(self, endpoint_url: str = "https://query.wikidata.org/sparql", user_agent: str = "TextToSparqlBot/1.0"):
        self.endpoint = SPARQLWrapper(endpoint_url)
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", user_agent)
        self.endpoint.setTimeout(60)

    def clean_query(self, query_text: str) -> str:
        """Cleans the LLM output to extract just the SPARQL query."""
        if not query_text: return ""
        q = query_text.strip()
        q = q.replace("```sparql", "").replace("```", "").strip()
        q = re.sub(r'PREF[A-Z]*\s', 'PREFIX ', q, flags=re.IGNORECASE)
        # Ensure 'wd:?variable' is fixed to '?variable' if model hallucinates
        q = re.sub(r'wd:\?(\w+)', r'?\1', q)
        return q

    def validate_syntax_local(self, query: str) -> Dict[str, Any]:
        """Validates SPARQL syntax locally using rdflib (if available)."""
        error_info = {"valid": True, "type": None, "detail": None}
        if not query:
            return {"valid": False, "type": "Empty Output", "detail": "The model generated no output."}
            
        try:
            from rdflib.plugins.sparql.parser import parseQuery
            from pyparsing import ParseException
            parseQuery(query)
        except ImportError:
            logger.warning("rdflib not installed. Skipping local syntax validation.")
        except ParseException as e:
            error_info["valid"] = False
            error_info["type"] = "Syntax Error"
            error_info["detail"] = f"Line {e.lineno}, Col {e.col}: Expected {e.msg}"
        except Exception as e:
            error_info["valid"] = False
            error_info["type"] = "Parsing Error"
            error_info["detail"] = str(e)
        return error_info

    def execute_remote(self, query: str) -> Tuple[Optional[List], Optional[str]]:
        """Executes the query against the remote endpoint."""
        try:
            self.endpoint.setQuery(query)
            results = self.endpoint.query().convert()
            return results['results']['bindings'], None
        except Exception as e:
            # Return None for results and the error message string
            return None, str(e).split('\n')[0]

    def calculate_f1(self, gold_results: List, gen_results: List) -> float:
        """Calculates F1 Score based on result sets."""
        if not gold_results and not gen_results: return 1.0 # Both empty = Match
        if not gold_results or not gen_results: return 0.0  # One empty = Mismatch
        
        def get_vals(bindings):
            # Create a set of tuples containing sorted values for each row
            return {tuple(sorted(v['value'] for v in r.values())) for r in bindings}

        g_set = get_vals(gold_results)
        p_set = get_vals(gen_results)
        
        tp = len(g_set & p_set)
        if tp == 0: return 0.0
        
        precision = tp / len(p_set)
        recall = tp / len(g_set)
        return 2 * (precision * recall) / (precision + recall)
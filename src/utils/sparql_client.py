import re
import logging
from typing import Tuple, List, Optional, Dict, Any
from SPARQLWrapper import SPARQLWrapper, JSON

logger = logging.getLogger(__name__)

class SPARQLClient:
    """Handles SPARQL query validation and execution against Wikidata endpoint."""
    
    def __init__(self, endpoint_url: str = "[https://query.wikidata.org/sparql](https://query.wikidata.org/sparql)", user_agent: str = "TextToSparqlBot/1.0"):
        self.endpoint = SPARQLWrapper(endpoint_url)
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.addCustomHttpHeader("User-Agent", user_agent)
        self.endpoint.setTimeout(60)

    def clean_query(self, query_text: str) -> str:
        """Extracts and normalizes SPARQL query from LLM output."""
        if not query_text: return ""
        
        q = query_text.strip()
        if "```" in q:
            pattern = r"```(?:sparql)?(.*?)```"
            match = re.search(pattern, q, re.DOTALL)
            if match:
                q = match.group(1)
        
        q = q.strip()
        q = re.sub(r'PREF[A-Z]*\s', 'PREFIX ', q, flags=re.IGNORECASE)
        q = re.sub(r'wd:\?(\w+)', r'?\1', q)
        return q

    def validate_syntax_local(self, query: str) -> Dict[str, Any]:
        """Validates SPARQL syntax using local parser."""
        error_info = {"valid": True, "type": None, "detail": None}
        if not query:
            return {"valid": False, "type": "Empty Output", "detail": "The model generated no output."}
            
        try:
            from rdflib.plugins.sparql.parser import parseQuery
            from pyparsing import ParseException
            parseQuery(query)
        except ImportError:
            pass
        except ParseException as e:
            error_info["valid"] = False
            error_info["type"] = "Syntax Error"
            error_info["detail"] = f"Line {e.lineno}, Col {e.col}: {e.msg}"
        except Exception as e:
            error_info["valid"] = False
            error_info["type"] = "Parsing Error"
            error_info["detail"] = str(e)
        return error_info

    def execute_remote(self, query: str) -> Tuple[Optional[List], Optional[str]]:
        """
        Executes SPARQL query against remote endpoint.
        
        Args:
            query: SPARQL query string to execute
            
        Returns:
            Tuple of (results list, error message)
        """
        try:
            self.endpoint.setQuery(query)
            results = self.endpoint.query().convert()
            
            if 'boolean' in results:
                val = "TRUE" if results['boolean'] else "FALSE"
                return [{'ask_result': {'type': 'literal', 'value': val}}], None
                
            if 'results' in results and 'bindings' in results['results']:
                return results['results']['bindings'], None
                
            return [], "No bindings or boolean found in response"

        except Exception as e:
            return None, str(e).split('\n')[0]

    def calculate_f1(self, gold_results: List, gen_results: List) -> float:
        """Computes F1 score between reference and generated results."""
        if not gold_results and not gen_results: return 1.0
        if gold_results is None or gen_results is None: return 0.0
        if not gold_results or not gen_results: return 0.0
        
        def get_vals(bindings):
            out = set()
            for row in bindings:
                row_vals = []
                for k, v in row.items():
                    val = v['value'].split('/')[-1]
                    row_vals.append(val)
                out.add(tuple(sorted(row_vals)))
            return out

        g_set = get_vals(gold_results)
        p_set = get_vals(gen_results)
        
        tp = len(g_set & p_set)
        if tp == 0: return 0.0
        
        precision = tp / len(p_set)
        recall = tp / len(g_set)
        return 2 * (precision * recall) / (precision + recall)
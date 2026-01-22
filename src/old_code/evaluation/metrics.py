"""
Custom evaluation metrics for SPARQL generation using DeepEval.
"""

from typing import List, Dict, Any, Optional
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

from src.utils.sparql_client import SPARQLClient
from src.logging_config import get_logger

logger = get_logger(__name__)


class SPARQLSyntaxMetric(BaseMetric):
    """
    Evaluates syntactic correctness of generated SPARQL queries.
    Uses rdflib parser for validation.
    """
    
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.client = SPARQLClient()
    
    def measure(self, test_case: LLMTestCase) -> float:
        """
        Measure syntax validity (binary: 1.0 or 0.0).
        
        Args:
            test_case: Contains actual_output (generated SPARQL)
            
        Returns:
            1.0 if syntactically valid, 0.0 otherwise
        """
        query = test_case.actual_output
        result = self.client.validate_syntax_local(query)
        
        self.success = result["valid"]
        self.score = 1.0 if self.success else 0.0
        self.reason = result.get("detail", "Valid SPARQL syntax")
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.score >= self.threshold
    
    @property
    def __name__(self):
        return "SPARQL Syntax Validity"


class SPARQLExecutionMetric(BaseMetric):
    """
    Evaluates if generated SPARQL executes without errors on Wikidata.
    """
    
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.client = SPARQLClient()
    
    def measure(self, test_case: LLMTestCase) -> float:
        """
        Measure execution success (binary: 1.0 or 0.0).
        
        Args:
            test_case: Contains actual_output (generated SPARQL)
            
        Returns:
            1.0 if executes successfully, 0.0 on error
        """
        query = test_case.actual_output
        
        # First check syntax
        syntax = self.client.validate_syntax_local(query)
        if not syntax["valid"]:
            self.success = False
            self.score = 0.0
            self.reason = f"Syntax Error: {syntax['detail']}"
            return self.score
        
        # Try execution
        results, error = self.client.execute_remote(query)
        
        self.success = (error is None)
        self.score = 1.0 if self.success else 0.0
        self.reason = error or "Query executed successfully"
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.score >= self.threshold
    
    @property
    def __name__(self):
        return "SPARQL Execution Success"


class SPARQLAnswerCorrectnessMetric(BaseMetric):
    """
    Evaluates semantic correctness by comparing result bindings.
    Uses F1 score between gold and generated query results.
    """
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.client = SPARQLClient()
    
    def measure(self, test_case: LLMTestCase) -> float:
        """
        Measure answer correctness using F1 score.
        
        Args:
            test_case: Contains:
                - actual_output: generated SPARQL
                - expected_output: gold SPARQL
            
        Returns:
            F1 score between 0.0 and 1.0
        """
        gen_query = test_case.actual_output
        gold_query = test_case.expected_output
        
        # Execute both queries
        gen_results, gen_error = self.client.execute_remote(gen_query)
        gold_results, gold_error = self.client.execute_remote(gold_query)
        
        if gen_error or gold_error:
            self.success = False
            self.score = 0.0
            self.reason = f"Execution failed: {gen_error or gold_error}"
            return self.score
        
        # Calculate F1
        self.score = self.client.calculate_f1(gold_results, gen_results)
        self.success = self.score >= self.threshold
        self.reason = f"F1 Score: {self.score:.3f}"
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.score >= self.threshold
    
    @property
    def __name__(self):
        return "SPARQL Answer Correctness (F1)"


class ContextRelevanceMetric(BaseMetric):
    """
    Evaluates if retrieved few-shot examples are relevant to the question.
    Uses semantic similarity between question and examples.
    """
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
    
    def measure(self, test_case: LLMTestCase) -> float:
        """
        Measure context relevance based on retrieval context.
        
        Args:
            test_case: Contains:
                - input: question
                - retrieval_context: list of retrieved examples
            
        Returns:
            Average relevance score (0.0 to 1.0)
        """
        if not test_case.retrieval_context:
            self.success = False
            self.score = 0.0
            self.reason = "No retrieval context provided"
            return self.score
        
        # Simple heuristic: check if examples contain question keywords
        question = test_case.input.lower()
        keywords = set(question.split())
        
        relevance_scores = []
        for example in test_case.retrieval_context:
            example_lower = example.lower()
            matches = sum(1 for kw in keywords if kw in example_lower)
            relevance_scores.append(matches / len(keywords) if keywords else 0.0)
        
        self.score = sum(relevance_scores) / len(relevance_scores)
        self.success = self.score >= self.threshold
        self.reason = f"Average keyword overlap: {self.score:.3f}"
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.score >= self.threshold
    
    @property
    def __name__(self):
        return "Context Relevance"


def create_test_case(
    question: str,
    generated_sparql: str,
    gold_sparql: str,
    examples: Optional[List] = None
) -> LLMTestCase:
    """
    Factory function to create DeepEval test case from evaluation data.
    
    Args:
        question: Natural language question
        generated_sparql: LLM-generated SPARQL query
        gold_sparql: Ground truth SPARQL query
        examples: Retrieved few-shot examples (list of dicts or strings)
        
    Returns:
        LLMTestCase ready for metric evaluation
    """
    # Convert examples to list of strings if needed
    retrieval_context = []
    if examples:
        for ex in examples:
            if isinstance(ex, dict):
                # Extract question from dict
                retrieval_context.append(ex.get('question', str(ex)))
            elif isinstance(ex, str):
                retrieval_context.append(ex)
            else:
                retrieval_context.append(str(ex))
    
    return LLMTestCase(
        input=question,
        actual_output=generated_sparql,
        expected_output=gold_sparql,
        retrieval_context=retrieval_context
    )

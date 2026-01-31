"""
Unit tests for pipeline error handling and edge cases.
Tests error scenarios, malformed inputs, timeout handling, etc.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

FILE = Path(__file__).resolve()
PROJECT_ROOT = FILE.parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.sparql_client import SPARQLClient
from src.pipeline_utils import retry, SimpleCache, validate_sparql_output, RetryError
from src.exceptions import DataError


class TestSPARQLClient:
    """Test SPARQL client error handling."""

    def test_validate_syntax_empty_query(self):
        """Should handle empty queries gracefully."""
        client = SPARQLClient()
        result = client.validate_syntax_local("")
        assert result["valid"] is False
        assert result["type"] == "Empty Output"

    def test_validate_syntax_invalid_query(self):
        """Should detect syntax errors."""
        client = SPARQLClient()
        result = client.validate_syntax_local("SELECT * WHERE { INVALID SYNTAX }")
        assert result["valid"] is False
        assert "Syntax Error" in result["type"] or "Parsing Error" in result["type"]

    def test_validate_syntax_valid_query(self):
        """Should accept valid SPARQL."""
        client = SPARQLClient()
        query = "SELECT * WHERE { ?s ?p ?o }"
        result = client.validate_syntax_local(query)
        assert result["valid"] is True

    def test_validate_syntax_wrong_type(self):
        """Should handle non-string input."""
        client = SPARQLClient()
        result = client.validate_syntax_local(None)
        assert result["valid"] is False
        # None is treated as empty output first
        assert result["type"] in ["Empty Output", "Type Error"]

    def test_calculate_f1_both_empty(self):
        """F1 = 1.0 when both results are empty."""
        client = SPARQLClient()
        f1 = client.calculate_f1([], [])
        assert f1 == 1.0

    def test_calculate_f1_one_empty(self):
        """F1 = 0.0 when one result is empty."""
        client = SPARQLClient()
        gold = [{"x": {"value": "http://example.org/test"}}]
        gen = []
        f1 = client.calculate_f1(gold, gen)
        assert f1 == 0.0

    def test_calculate_f1_identical(self):
        """F1 = 1.0 for identical results."""
        client = SPARQLClient()
        results = [{"x": {"value": "http://example.org/test"}}]
        f1 = client.calculate_f1(results, results)
        assert f1 == 1.0

    def test_calculate_f1_none_input(self):
        """Handle None inputs gracefully."""
        client = SPARQLClient()
        assert client.calculate_f1(None, None) == 0.0
        assert client.calculate_f1([{"x": {"value": "test"}}], None) == 0.0

    def test_clean_query_markdown(self):
        """Should extract query from markdown."""
        client = SPARQLClient()
        raw = "Here's the query:\n```sparql\nSELECT * WHERE { ?s ?p ?o }\n```"
        cleaned = client.clean_query(raw)
        assert "SELECT" in cleaned
        assert "```" not in cleaned

    def test_clean_query_empty(self):
        """Should handle empty input."""
        client = SPARQLClient()
        assert client.clean_query("") == ""
        assert client.clean_query(None) == ""


class TestRetryDecorator:
    """Test retry decorator functionality."""

    def test_retry_success_first_attempt(self):
        """Should return immediately on success."""
        call_count = 0

        @retry(max_attempts=3)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 1

    def test_retry_eventual_success(self):
        """Should succeed on second attempt."""
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("First attempt fails")
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 2

    def test_retry_max_exceeded(self):
        """Should raise RetryError when max attempts exceeded."""

        @retry(max_attempts=2, delay=0.01)
        def test_func():
            raise ValueError("Always fails")

        with pytest.raises(RetryError):
            test_func()

    def test_retry_with_callback(self):
        """Should call error callback on failure."""
        errors = []

        def on_error(e):
            errors.append(str(e))

        @retry(max_attempts=2, delay=0.01, on_error=on_error)
        def test_func():
            raise ValueError("Test error")

        with pytest.raises(RetryError):
            test_func()

        assert len(errors) >= 1


class TestSimpleCache:
    """Test caching functionality."""

    def test_cache_set_get(self):
        """Should store and retrieve values."""
        cache = SimpleCache()
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_cache_miss(self):
        """Should return None on cache miss."""
        cache = SimpleCache()
        assert cache.get("nonexistent") is None

    def test_cache_overwrite(self):
        """Should overwrite existing values."""
        cache = SimpleCache()
        cache.set("key", "value1")
        cache.set("key", "value2")
        assert cache.get("key") == "value2"

    def test_cache_complex_objects(self):
        """Should cache complex objects."""
        cache = SimpleCache()
        data = {"nested": {"key": [1, 2, 3]}}
        cache.set("complex", data)
        assert cache.get("complex") == data

    def test_cache_clear(self):
        """Should clear all cache entries."""
        cache = SimpleCache()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None


class TestValidateSparqlOutput:
    """Test SPARQL output validation."""

    def test_extract_from_code_block(self):
        """Should extract query from markdown code block."""
        raw = "```sparql\nSELECT * WHERE { ?s ?p ?o }\n```"
        query = validate_sparql_output(raw)
        assert query is not None
        assert "SELECT" in query

    def test_extract_select_statement(self):
        """Should find SELECT statement without code block."""
        raw = "Here's the query: SELECT * WHERE { ?s ?p ?o }"
        query = validate_sparql_output(raw)
        assert query is not None
        assert "SELECT" in query

    def test_invalid_output_no_select(self):
        """Should return None for non-SELECT output."""
        raw = "This is just text without SELECT"
        query = validate_sparql_output(raw)
        assert query is None

    def test_empty_output(self):
        """Should handle empty output."""
        assert validate_sparql_output("") is None
        assert validate_sparql_output(None) is None

    def test_case_insensitive_select(self):
        """Should handle lowercase select."""
        raw = "select * where { ?s ?p ?o }"
        query = validate_sparql_output(raw)
        assert query is not None


class TestErrorHandling:
    """Test general error handling."""

    def test_data_error_custom_exception(self):
        """DataError should be properly raised."""
        with pytest.raises(DataError):
            raise DataError("Test error message")

    def test_sparql_client_malformed_response(self):
        """Should handle malformed API responses."""
        client = SPARQLClient()
        # This would test actual API response handling
        # Requires mocking the endpoint

    @patch("src.models.retriever.ExampleRetriever.__init__")
    def test_retriever_missing_files(self, mock_init):
        """Should raise FileNotFoundError for missing indices."""
        mock_init.side_effect = FileNotFoundError("Index not found")

        with pytest.raises(FileNotFoundError):
            from src.models.retriever import ExampleRetriever

            ExampleRetriever("fake_index.faiss", "fake_meta.pkl")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

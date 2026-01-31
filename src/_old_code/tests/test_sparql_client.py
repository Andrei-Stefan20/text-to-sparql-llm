"""
Unit tests for SPARQL client functionality.
"""

import pytest
from src.utils.sparql_client import SPARQLClient
from src.exceptions import SPARQLError


@pytest.fixture
def client():
    """Create a SPARQLClient instance."""
    return SPARQLClient()


def test_sparql_client_initialization(client):
    """Test SPARQL client initializes correctly."""
    assert client.endpoint is not None


def test_clean_query_with_markdown(client):
    """Test query cleaning removes markdown code blocks."""
    query_with_markdown = "```sparql\nSELECT * WHERE { ?s ?p ?o }\n```"
    cleaned = client.clean_query(query_with_markdown)
    assert "```" not in cleaned
    assert "SELECT" in cleaned


def test_clean_query_plain(client):
    """Test query cleaning with plain SPARQL."""
    query = "SELECT * WHERE { ?s ?p ?o }"
    cleaned = client.clean_query(query)
    assert cleaned == query


def test_clean_query_empty(client):
    """Test query cleaning with empty input."""
    cleaned = client.clean_query("")
    assert cleaned == ""


def test_validate_syntax_local_valid(client):
    """Test local syntax validation with valid query."""
    query = "SELECT ?s WHERE { ?s ?p ?o }"
    result = client.validate_syntax_local(query)
    assert result["valid"] is True


def test_validate_syntax_local_empty(client):
    """Test local syntax validation with empty query."""
    result = client.validate_syntax_local("")
    assert result["valid"] is False
    assert result["type"] == "Empty Output"


def test_calculate_f1_identical(client):
    """Test F1 calculation with identical results."""
    results1 = [{"var": {"value": "http://example.org/Q123"}}]
    results2 = [{"var": {"value": "http://example.org/Q123"}}]

    f1 = client.calculate_f1(results1, results2)
    assert f1 == 1.0


def test_calculate_f1_empty_both(client):
    """Test F1 calculation with both results empty."""
    f1 = client.calculate_f1([], [])
    assert f1 == 1.0


def test_calculate_f1_no_overlap(client):
    """Test F1 calculation with no overlap."""
    results1 = [{"var": {"value": "http://example.org/Q123"}}]
    results2 = [{"var": {"value": "http://example.org/Q456"}}]

    f1 = client.calculate_f1(results1, results2)
    assert f1 == 0.0


def test_calculate_f1_partial_overlap(client):
    """Test F1 calculation with partial overlap."""
    results1 = [
        {"var": {"value": "http://example.org/Q123"}},
        {"var": {"value": "http://example.org/Q456"}},
    ]
    results2 = [
        {"var": {"value": "http://example.org/Q123"}},
        {"var": {"value": "http://example.org/Q789"}},
    ]

    f1 = client.calculate_f1(results1, results2)
    assert 0 < f1 < 1.0

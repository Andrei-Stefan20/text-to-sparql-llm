"""
Unit tests for input validation utilities.
"""

import json
import tempfile
from pathlib import Path

import pytest
from src.exceptions import DataError, ValidationError
from src.validators import (validate_api_key, validate_directory_exists,
                            validate_file_exists, validate_json_file,
                            validate_qald_data, validate_sparql_query)


def test_validate_file_exists_success(tmp_path):
    """Test file validation with existing file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    validate_file_exists(test_file)  # Should not raise


def test_validate_file_exists_missing():
    """Test file validation with missing file."""
    with pytest.raises(ValidationError, match="not found"):
        validate_file_exists(Path("/nonexistent/file.txt"))


def test_validate_file_exists_directory(tmp_path):
    """Test file validation with directory instead of file."""
    with pytest.raises(ValidationError, match="not a file"):
        validate_file_exists(tmp_path)


def test_validate_directory_exists_success(tmp_path):
    """Test directory validation with existing directory."""
    validate_directory_exists(tmp_path)  # Should not raise


def test_validate_directory_exists_missing():
    """Test directory validation with missing directory."""
    with pytest.raises(ValidationError, match="not found"):
        validate_directory_exists(Path("/nonexistent/dir"))


def test_validate_json_file_success(tmp_path):
    """Test JSON file validation with valid file."""
    test_file = tmp_path / "test.json"
    test_data = {"key": "value"}
    test_file.write_text(json.dumps(test_data))

    result = validate_json_file(test_file)
    assert result == test_data


def test_validate_json_file_invalid(tmp_path):
    """Test JSON file validation with invalid JSON."""
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{ invalid json }")

    with pytest.raises(DataError, match="Invalid JSON"):
        validate_json_file(test_file)


def test_validate_qald_data_success():
    """Test QALD data validation with valid structure."""
    valid_data = {
        "questions": [
            {
                "question": [{"language": "en", "string": "Test question"}],
                "query": {"sparql": "SELECT * WHERE { ?s ?p ?o }"},
            }
        ]
    }

    result = validate_qald_data(valid_data)
    assert len(result) == 1


def test_validate_qald_data_missing_questions():
    """Test QALD validation with missing questions field."""
    with pytest.raises(ValidationError, match="missing 'questions'"):
        validate_qald_data({})


def test_validate_qald_data_empty():
    """Test QALD validation with empty questions list."""
    with pytest.raises(ValidationError, match="No questions found"):
        validate_qald_data({"questions": []})


def test_validate_sparql_query_valid():
    """Test SPARQL validation with valid query."""
    query = "SELECT ?s WHERE { ?s ?p ?o }"
    validate_sparql_query(query)  # Should not raise


def test_validate_sparql_query_empty():
    """Test SPARQL validation with empty query."""
    with pytest.raises(ValidationError, match="empty"):
        validate_sparql_query("")


def test_validate_sparql_query_invalid():
    """Test SPARQL validation without query type."""
    with pytest.raises(ValidationError, match="valid SPARQL query type"):
        validate_sparql_query("INVALID QUERY")


def test_validate_api_key_valid():
    """Test API key validation with valid key."""
    result = validate_api_key("test_key_123", "TestService")
    assert result == "test_key_123"


def test_validate_api_key_empty():
    """Test API key validation with empty key."""
    with pytest.raises(ValidationError, match="API key not found"):
        validate_api_key("", "TestService")


def test_validate_api_key_none():
    """Test API key validation with None."""
    with pytest.raises(ValidationError, match="API key not found"):
        validate_api_key(None, "TestService")

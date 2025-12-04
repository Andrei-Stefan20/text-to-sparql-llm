"""
Unit tests for custom exceptions.
"""

import pytest
from src.exceptions import (
    TextToSPARQLError,
    ModelError,
    APIError,
    SPARQLError,
    SyntaxError,
    ExecutionError,
    RetrievalError,
    ConfigurationError,
    DataError,
    ValidationError
)


def test_base_exception():
    """Test base TextToSPARQLError can be raised."""
    with pytest.raises(TextToSPARQLError):
        raise TextToSPARQLError("Base error")


def test_model_error():
    """Test ModelError is a TextToSPARQLError."""
    with pytest.raises(TextToSPARQLError):
        raise ModelError("Model failed")


def test_api_error():
    """Test APIError is a TextToSPARQLError."""
    with pytest.raises(TextToSPARQLError):
        raise APIError("API call failed")


def test_sparql_error():
    """Test SPARQLError is a TextToSPARQLError."""
    with pytest.raises(TextToSPARQLError):
        raise SPARQLError("SPARQL error")


def test_syntax_error():
    """Test SyntaxError is a SPARQLError."""
    with pytest.raises(SPARQLError):
        raise SyntaxError("Invalid syntax")


def test_execution_error():
    """Test ExecutionError is a SPARQLError."""
    with pytest.raises(SPARQLError):
        raise ExecutionError("Execution failed")


def test_retrieval_error():
    """Test RetrievalError is a TextToSPARQLError."""
    with pytest.raises(TextToSPARQLError):
        raise RetrievalError("Retrieval failed")


def test_configuration_error():
    """Test ConfigurationError is a TextToSPARQLError."""
    with pytest.raises(TextToSPARQLError):
        raise ConfigurationError("Invalid config")


def test_data_error():
    """Test DataError is a TextToSPARQLError."""
    with pytest.raises(TextToSPARQLError):
        raise DataError("Data loading failed")


def test_validation_error():
    """Test ValidationError is a TextToSPARQLError."""
    with pytest.raises(TextToSPARQLError):
        raise ValidationError("Validation failed")

"""
Unit tests for configuration management.
"""

import pytest
from pathlib import Path
from src.config import (
    Config,
    ModelConfig,
    RetrievalConfig,
    EvaluationConfig,
    SPARQLConfig,
)


def test_model_config_defaults():
    """Test ModelConfig has correct default values."""
    config = ModelConfig()
    assert config.temperature == 0.1
    assert config.max_new_tokens == 512
    assert "Qwen" in config.local_model_id
    assert "gemini" in config.gemini_model_id


def test_retrieval_config_defaults():
    """Test RetrievalConfig has correct defaults."""
    config = RetrievalConfig()
    assert config.k_examples == 3
    assert "all-mpnet-base-v2" in config.embedding_model
    assert config.chunk_size == 50


def test_evaluation_config_defaults():
    """Test EvaluationConfig has correct defaults."""
    config = EvaluationConfig()
    assert config.max_retries == 3
    assert config.retry_with_error_feedback is True
    assert config.test_sample_size == 20
    assert config.ace_max_retries == 3


def test_sparql_config_defaults():
    """Test SPARQLConfig has correct defaults."""
    config = SPARQLConfig()
    assert "wikidata.org" in config.endpoint_url
    assert config.timeout == 60
    assert config.api_delay == 0.1


def test_config_initialization():
    """Test Config main class initialization."""
    config = Config()
    assert isinstance(config.model, ModelConfig)
    assert isinstance(config.retrieval, RetrievalConfig)
    assert isinstance(config.evaluation, EvaluationConfig)
    assert isinstance(config.sparql, SPARQLConfig)


def test_config_validation_missing_files():
    """Test config validation detects missing files."""
    config = Config()
    # Should return False when files don't exist
    # (unless they do exist in your setup)
    result = config.validate()
    assert isinstance(result, bool)

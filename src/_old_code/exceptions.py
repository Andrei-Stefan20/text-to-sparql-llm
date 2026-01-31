"""
Custom exceptions for the Text-to-SPARQL project.
Provides specific error types for better error handling and debugging.
"""


class TextToSPARQLError(Exception):
    """Base exception for all project-specific errors."""

    pass


class ModelError(TextToSPARQLError):
    """Raised when LLM model initialization or inference fails."""

    pass


class APIError(TextToSPARQLError):
    """Raised when external API calls fail (Gemini, Wikidata, etc.)."""

    pass


class SPARQLError(TextToSPARQLError):
    """Raised when SPARQL query validation or execution fails."""

    pass


class SyntaxError(SPARQLError):
    """Raised when generated SPARQL has syntax errors."""

    pass


class ExecutionError(SPARQLError):
    """Raised when SPARQL query execution fails on the endpoint."""

    pass


class RetrievalError(TextToSPARQLError):
    """Raised when FAISS retrieval or embedding generation fails."""

    pass


class ConfigurationError(TextToSPARQLError):
    """Raised when configuration is invalid or incomplete."""

    pass


class DataError(TextToSPARQLError):
    """Raised when data loading or processing fails."""

    pass


class ValidationError(TextToSPARQLError):
    """Raised when input validation fails."""

    pass

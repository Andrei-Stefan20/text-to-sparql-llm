"""
Input validation utilities for the Text-to-SPARQL project.
Ensures data integrity before processing.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.exceptions import DataError, ValidationError


def validate_file_exists(file_path: Path, description: str = "File") -> None:
    """
    Validates that a file exists.

    Args:
        file_path: Path to validate
        description: Human-readable description for error messages

    Raises:
        ValidationError: If file does not exist
    """
    if not file_path.exists():
        raise ValidationError(f"{description} not found: {file_path}")

    if not file_path.is_file():
        raise ValidationError(f"{description} is not a file: {file_path}")


def validate_directory_exists(dir_path: Path, description: str = "Directory") -> None:
    """
    Validates that a directory exists.

    Args:
        dir_path: Directory path to validate
        description: Human-readable description for error messages

    Raises:
        ValidationError: If directory does not exist
    """
    if not dir_path.exists():
        raise ValidationError(f"{description} not found: {dir_path}")

    if not dir_path.is_dir():
        raise ValidationError(f"{description} is not a directory: {dir_path}")


def validate_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Validates and loads a JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        ValidationError: If file doesn't exist
        DataError: If JSON parsing fails
    """
    validate_file_exists(file_path, "JSON file")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise DataError(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise DataError(f"Failed to read {file_path}: {e}")


def validate_qald_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Validates QALD dataset structure.

    Args:
        data: Loaded QALD JSON data

    Returns:
        List of valid question objects

    Raises:
        ValidationError: If data structure is invalid
    """
    if "questions" not in data:
        raise ValidationError("QALD data missing 'questions' field")

    questions = data["questions"]
    if not isinstance(questions, list):
        raise ValidationError("'questions' field must be a list")

    if len(questions) == 0:
        raise ValidationError("No questions found in QALD data")

    # Validate first question structure
    sample = questions[0]
    required_fields = ["question", "query"]
    for field in required_fields:
        if field not in sample:
            raise ValidationError(f"Question missing required field: {field}")

    return questions


def validate_sparql_query(query: str) -> None:
    """
    Basic SPARQL query validation.

    Args:
        query: SPARQL query string

    Raises:
        ValidationError: If query is invalid
    """
    if not query or not query.strip():
        raise ValidationError("SPARQL query is empty")

    query_upper = query.upper()

    # Check for basic SPARQL keywords
    if not any(
        keyword in query_upper for keyword in ["SELECT", "ASK", "CONSTRUCT", "DESCRIBE"]
    ):
        raise ValidationError(
            "Query must contain a valid SPARQL query type (SELECT, ASK, CONSTRUCT, DESCRIBE)"
        )


def validate_api_key(key: Optional[str], service: str) -> str:
    """
    Validates that an API key is present.

    Args:
        key: API key to validate
        service: Service name for error messages

    Returns:
        The validated API key

    Raises:
        ValidationError: If key is missing or empty
    """
    if not key or not key.strip():
        raise ValidationError(
            f"{service} API key not found. " f"Please set it in your .env file."
        )
    return key.strip()

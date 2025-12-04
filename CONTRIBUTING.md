# Contributing to Text-to-SPARQL LLM

Thank you for your interest in contributing! This document provides guidelines and standards for contributing to the project.

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/text-to-sparql-llm.git
cd text-to-sparql-llm
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (testing, linting, type checking)
pip install -r requirements-dev.txt
```

### 4. Verify Installation

```bash
python cli.py check
pytest
```

## Code Standards

### Python Style Guide

We follow **PEP 8** with these tools:

- **Black** (code formatting): Line length 100
- **flake8** (linting): Enforces PEP 8 compliance
- **mypy** (type checking): Ensures type safety

### Running Code Quality Tools

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/ --max-line-length=100

# Type checking
mypy src/ --ignore-missing-imports
```

### Pre-Commit Checklist

Before committing code:

1. Run `black` to format code
2. Run `flake8` and fix all errors
3. Run `mypy` and address type issues
4. Run `pytest` and ensure all tests pass
5. Add tests for new functionality
6. Update documentation if needed

## Project Architecture

### Core Modules

```
src/
├── config.py           # Centralized configuration (DO NOT hardcode values)
├── exceptions.py       # Custom exceptions (use instead of generic Exception)
├── validators.py       # Input validation (validate all external data)
├── logging_config.py   # Logging setup (use get_logger(__name__))
├── models/             # Core ML/NLP components
├── utils/              # Shared utilities
└── data/               # Data processing
```

### Design Principles

1. **Configuration Centralization**: Use `src.config.config` for all parameters
2. **Custom Exceptions**: Raise specific exceptions from `src.exceptions`
3. **Input Validation**: Validate all external data using `src.validators`
4. **Logging**: Use `get_logger(__name__)` instead of `logging.basicConfig()`
5. **Type Hints**: Add type annotations to all functions
6. **Docstrings**: Document all public functions with Google-style docstrings

### Example: Proper Function Structure

```python
from typing import List, Optional
from src.config import config
from src.exceptions import ValidationError
from src.validators import validate_file_exists
from src.logging_config import get_logger

logger = get_logger(__name__)


def process_query(
    question: str, 
    examples: List[str], 
    max_retries: Optional[int] = None
) -> str:
    """
    Process a natural language question into a SPARQL query.
    
    Args:
        question: User's natural language question
        examples: Few-shot learning examples
        max_retries: Maximum retry attempts (defaults to config value)
        
    Returns:
        Generated SPARQL query string
        
    Raises:
        ValidationError: If question is empty or examples are invalid
        APIError: If LLM API request fails
    """
    if not question or not question.strip():
        raise ValidationError("Question cannot be empty")
    
    retries = max_retries or config.model.max_retries
    logger.info(f"Processing question with {len(examples)} examples")
    
    # Implementation here
    ...
```

## Testing

### Writing Tests

- Use `pytest` framework
- Place tests in `tests/` directory
- Follow naming: `test_<module_name>.py`
- Test functions: `test_<function_name>_<scenario>`

### Test Structure

```python
import pytest
from src.validators import validate_sparql_query
from src.exceptions import SPARQLSyntaxError


def test_validate_sparql_query_valid():
    """Test validation accepts valid SPARQL query."""
    query = "SELECT ?s WHERE { ?s ?p ?o }"
    assert validate_sparql_query(query) is True


def test_validate_sparql_query_invalid():
    """Test validation rejects malformed query."""
    query = "SELECT ?s WHERE"
    with pytest.raises(SPARQLSyntaxError):
        validate_sparql_query(query)


@pytest.mark.parametrize("query,expected", [
    ("SELECT * WHERE { ?s ?p ?o }", True),
    ("ASK { ?s ?p ?o }", True),
    ("INVALID SYNTAX", False),
])
def test_validate_sparql_query_multiple(query, expected):
    """Test validation across multiple query types."""
    result = validate_sparql_query(query, raise_on_error=False)
    assert result == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_validators.py -v

# Run tests matching pattern
pytest -k "test_sparql" -v
```

### Coverage Requirements

- Minimum coverage: **90%**
- Critical modules (`config.py`, `validators.py`, `sparql_client.py`): **95%+**

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# Or for bug fixes:
git checkout -b fix/bug-description
```

### 2. Make Changes

- Follow code standards
- Add tests for new functionality
- Update documentation

### 3. Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(retriever): add semantic caching for FAISS queries
fix(sparql): handle timeout errors in remote execution
docs(readme): update installation instructions
test(validators): add parametrized tests for URL validation
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- **Title**: Clear, descriptive summary
- **Description**: 
  - What changed and why
  - Related issue numbers (e.g., "Fixes #123")
  - Testing performed
  - Screenshots (if UI changes)

### 5. Code Review

- Address reviewer comments
- Keep PR focused (one feature/fix per PR)
- Update branch if conflicts arise

### 6. Merge

Once approved, PR will be merged using **squash and merge** strategy.

## Common Tasks

### Adding a New Model

1. Create model class in `src/models/`
2. Implement `generate_raw(prompt, stop, max_tokens)` method
3. Add configuration to `src/config.py`
4. Create evaluation script in `src/evaluate_<model>.py`
5. Update CLI in `cli.py`
6. Add tests in `tests/test_<model>.py`
7. Update README.md

### Adding a New Validator

1. Add function to `src/validators.py`
2. Raise specific exception from `src/exceptions.py`
3. Add docstring with examples
4. Create tests in `tests/test_validators.py`
5. Use validator in relevant modules

### Adding Configuration Parameter

1. Add to appropriate dataclass in `src/config.py`
2. Update `validate()` method if needed
3. Document in README.md
4. Use `config.<section>.<param>` instead of hardcoding

## Reporting Issues

### Bug Reports

Include:
- **Description**: What happened vs. expected behavior
- **Steps to Reproduce**: Minimal example
- **Environment**: Python version, OS, dependencies
- **Logs**: Relevant error messages
- **Screenshots**: If applicable

### Feature Requests

Include:
- **Use Case**: Why is this needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other approaches considered
- **Examples**: Similar features in other projects

## Questions?

- Open a GitHub Discussion for questions
- Check existing issues before creating new ones
- Refer to README.md for usage documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing! 🎉

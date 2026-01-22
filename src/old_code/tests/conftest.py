"""
Pytest configuration and fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def project_root():
    """Provides the project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def data_dir(project_root):
    """Provides the data directory."""
    return project_root / "data"


@pytest.fixture(scope="session")
def test_data_dir(project_root):
    """Provides the test data directory."""
    return project_root / "data" / "raw" / "QALD-10"

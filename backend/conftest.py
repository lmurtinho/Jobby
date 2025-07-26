"""
Pytest configuration for AI Job Tracker tests.

This file contains pytest fixtures and configuration shared across test modules.
"""

import pytest
from app.tests.fixtures.test_database import create_test_database, drop_test_database


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "ml: Machine learning model tests")
    config.addinivalue_line("markers", "slow: Slow running tests (> 1 second)")
    config.addinivalue_line("markers", "external: Tests that require external services")
    config.addinivalue_line("markers", "auth: Authentication related tests")
    config.addinivalue_line("markers", "database: Database related tests")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "scraping: Web scraping tests")
    config.addinivalue_line("markers", "background: Background task tests")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up test database before running any tests."""
    print("Setting up test database...")
    create_test_database()
    yield
    print("Cleaning up test database...")
    drop_test_database()


# Removed autouse database reset to avoid conflicts with test-specific fixtures

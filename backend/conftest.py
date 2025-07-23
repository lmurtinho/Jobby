"""
Pytest configuration for AI Job Tracker tests.

This file contains pytest fixtures and configuration shared across test modules.
"""

import pytest


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

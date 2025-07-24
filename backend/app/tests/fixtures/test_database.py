"""
Test database fixtures for AI Job Tracker.

This module provides test database configuration and utilities for integration tests.
Follows FastAPI testing patterns with separate test database.
"""

import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

from app.database import Base


# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

# Alternative: Use temporary file database for debugging
# TEST_DATABASE_URL = f"sqlite:///{tempfile.mkdtemp()}/test.db"

# Create test engine with specific configuration for SQLite
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False  # Set to True for SQL debugging in tests
)

# Test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def create_test_database():
    """Create all database tables for testing."""
    # Import models to ensure they're registered with SQLAlchemy
    from app.models import user  # Import to register models
    Base.metadata.create_all(bind=test_engine)


def drop_test_database():
    """Drop all database tables after testing."""
    Base.metadata.drop_all(bind=test_engine)


def override_get_db() -> Generator[Session, None, None]:
    """
    Override database dependency for testing.
    
    This function replaces the normal get_db dependency in FastAPI
    during integration tests to use the test database instead.
    
    Yields:
        Session: Test database session
    """
    # Ensure test database exists
    create_test_database()
    
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_test_db_session() -> Session:
    """
    Get a test database session for direct use in tests.
    
    Returns:
        Session: Test database session
    """
    create_test_database()
    return TestSessionLocal()


def reset_test_database():
    """
    Reset the test database by dropping and recreating all tables.
    
    Useful for ensuring clean state between test runs.
    """
    drop_test_database()
    create_test_database()


class TestDatabaseManager:
    """
    Context manager for test database lifecycle.
    
    Ensures proper setup and cleanup of test database.
    """
    
    def __enter__(self):
        """Set up test database."""
        create_test_database()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up test database."""
        drop_test_database()
    
    def get_session(self) -> Session:
        """Get a database session within the context."""
        return TestSessionLocal()


# Export commonly used test database utilities
__all__ = [
    "TestSessionLocal",
    "override_get_db", 
    "create_test_database",
    "drop_test_database",
    "get_test_db_session",
    "reset_test_database",
    "TestDatabaseManager"
]

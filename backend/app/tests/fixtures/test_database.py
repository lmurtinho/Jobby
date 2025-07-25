"""
Test database configuration and fixtures.

This module provides test database setup, session management, and utilities
for testing database operations in isolation.
"""

import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.database import Base

# Create a temporary database for testing
TEST_DATABASE_URL = "sqlite:///./test_jobby.db"

# Test database engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL debugging during tests
)

# Test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db() -> Generator[Session, None, None]:
    """
    Override database dependency for testing.
    
    Yields:
        Session: Test database session
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_test_database() -> None:
    """
    Create all database tables for testing.
    
    This function creates all tables defined by models that inherit from Base.
    """
    Base.metadata.create_all(bind=test_engine)


def drop_test_database() -> None:
    """
    Drop all database tables after testing.
    
    This function drops all tables to ensure clean test state.
    """
    Base.metadata.drop_all(bind=test_engine)


def get_test_db_session() -> Session:
    """
    Get a test database session.
    
    Returns:
        Session: Test database session
    """
    return TestSessionLocal()


def reset_test_database() -> None:
    """
    Reset the test database by dropping and recreating all tables.
    
    Useful between test runs to ensure clean state.
    """
    drop_test_database()
    create_test_database()
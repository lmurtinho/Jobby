"""
Database configuration for AI Job Tracker.

This module provides SQLAlchemy database setup, session management,
and dependency injection for the FastAPI application.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Generator


# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobby.db")

# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False  # Set to True for SQL debugging
)


# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """
    Create all database tables.
    
    This function creates all tables defined by models that inherit from Base.
    """
    Base.metadata.create_all(bind=engine)


def get_database_url() -> str:
    """
    Get the configured database URL.
    
    Returns:
        str: The database URL
    """
    return DATABASE_URL


def get_engine():
    """
    Get the SQLAlchemy engine.
    
    Returns:
        Engine: The SQLAlchemy engine instance
    """
    return engine


def get_session_factory():
    """
    Get the session factory.
    
    Returns:
        sessionmaker: The SQLAlchemy session factory
    """
    return SessionLocal

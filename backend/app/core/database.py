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

# Fix PostgreSQL URL format if needed (Railway compatibility)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLAlchemy engine with proper PostgreSQL configuration
engine_kwargs = {
    "echo": False,  # Set to True for SQL debugging
}

# Add connection args based on database type
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
elif DATABASE_URL.startswith("postgresql"):
    # PostgreSQL-specific configuration for production
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20
    engine_kwargs["pool_pre_ping"] = True  # Validate connections before use
    engine_kwargs["pool_recycle"] = 300   # Recycle connections every 5 minutes

engine = create_engine(DATABASE_URL, **engine_kwargs)


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
    # Import models to register them with Base
    from app.models.user import User  # noqa: F401
    
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

"""
Unit tests for the core database module.

Following Outside-In TDD approach - these tests verify what app.core.database should provide.
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine


class TestDatabaseModule:
    """Test suite for the core database module."""
    
    def test_get_db_function_exists(self):
        """Test that get_db function can be imported."""
        from app.core.database import get_db
        
        assert get_db is not None
        assert callable(get_db)
    
    def test_get_db_returns_session_generator(self):
        """Test that get_db returns a database session generator."""
        from app.core.database import get_db
        
        # get_db should be a generator function for FastAPI dependency injection
        db_generator = get_db()
        
        # Should be a generator
        assert hasattr(db_generator, '__next__')
        assert hasattr(db_generator, '__iter__')
    
    @patch('app.core.database.SessionLocal')
    def test_get_db_yields_database_session(self, mock_session_local):
        """Test that get_db yields a database session."""
        from app.core.database import get_db
        
        # Mock the session
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        # Get the database session
        db_generator = get_db()
        db_session = next(db_generator)
        
        # Should yield the session
        assert db_session == mock_session
        mock_session_local.assert_called_once()
    
    @patch('app.core.database.SessionLocal')
    def test_get_db_closes_session_after_use(self, mock_session_local):
        """Test that get_db properly closes the session after use."""
        from app.core.database import get_db
        
        # Mock the session
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        # Use the database session
        db_generator = get_db()
        db_session = next(db_generator)
        
        # Simulate the end of request (generator cleanup)
        try:
            next(db_generator)
        except StopIteration:
            pass
        
        # Session should be closed
        mock_session.close.assert_called_once()


class TestDatabaseConfiguration:
    """Test suite for database configuration and engine setup."""
    
    def test_database_url_configuration(self):
        """Test that database URL is properly configured."""
        from app.core.database import DATABASE_URL
        
        assert DATABASE_URL is not None
        assert isinstance(DATABASE_URL, str)
        assert len(DATABASE_URL) > 0
    
    def test_engine_creation(self):
        """Test that database engine is created."""
        from app.core.database import engine
        
        assert engine is not None
        assert isinstance(engine, Engine)
    
    def test_sessionlocal_creation(self):
        """Test that SessionLocal is properly created."""
        from app.core.database import SessionLocal
        
        assert SessionLocal is not None
        
        # Should be a sessionmaker class - check for callable and basic attributes
        assert callable(SessionLocal)
        assert hasattr(SessionLocal, 'configure')  # sessionmaker has configure method
        assert hasattr(SessionLocal, 'class_')    # sessionmaker has class_ attribute
    
    def test_sessionlocal_configuration(self):
        """Test that SessionLocal has proper configuration."""
        from app.core.database import SessionLocal
        
        # Create a session instance to test configuration
        session = SessionLocal()
        try:
            # Check that session is properly configured
            assert session is not None
            assert hasattr(session, 'bind')  # Session should have bind attribute
            assert hasattr(session, 'execute')  # Session should have execute method
            
            # Check session configuration via session info
            session_info = session.get_bind()
            assert session_info is not None
        finally:
            session.close()


class TestDatabaseIntegration:
    """Integration tests for database functionality."""
    
    @pytest.mark.integration
    def test_database_connection_works(self):
        """Test that database connection can be established."""
        from app.core.database import engine
        
        # Should be able to connect to database
        with engine.connect() as connection:
            assert connection is not None
    
    @pytest.mark.integration
    def test_session_creation_works(self):
        """Test that database sessions can be created."""
        from app.core.database import SessionLocal
        
        # Should be able to create a session
        session = SessionLocal()
        assert session is not None
        
        # Clean up
        session.close()
    
    @pytest.mark.integration
    def test_get_db_dependency_integration(self):
        """Test that get_db works as FastAPI dependency."""
        from app.core.database import get_db
        
        # Should work in FastAPI dependency injection context
        db_generator = get_db()
        
        try:
            db_session = next(db_generator)
            assert db_session is not None
            assert isinstance(db_session, Session)
        finally:
            # Ensure cleanup happens
            try:
                next(db_generator)
            except StopIteration:
                pass  # Expected behavior

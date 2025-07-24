"""
Unit tests for test database fixtures.

Following Outside-In TDD approach - these tests ensure our test database
fixtures work correctly for integration testing.
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import text

from app.tests.fixtures.test_database import (
    TestSessionLocal,
    override_get_db,
    create_test_database,
    drop_test_database,
    get_test_db_session,
    reset_test_database,
    TestDatabaseManager as FixturesDatabaseManager,
    test_engine
)


class TestDatabaseFixtures:
    """Test suite for test database fixture functionality."""
    
    def test_test_session_local_exists(self):
        """Test that TestSessionLocal is properly configured."""
        assert TestSessionLocal is not None
        assert hasattr(TestSessionLocal, '__call__')
        
        # Should be able to create a session
        session = TestSessionLocal()
        assert isinstance(session, Session)
        session.close()
    
    def test_test_engine_configuration(self):
        """Test that test engine is properly configured."""
        assert test_engine is not None
        assert isinstance(test_engine, Engine)
        
        # Should be SQLite in-memory or file
        assert "sqlite" in str(test_engine.url)
    
    def test_override_get_db_function(self):
        """Test that override_get_db returns a database session generator."""
        db_generator = override_get_db()
        
        # Should be a generator
        assert hasattr(db_generator, '__next__')
        assert hasattr(db_generator, '__iter__')
        
        # Should yield a database session
        db_session = next(db_generator)
        assert isinstance(db_session, Session)
        
        # Clean up the generator
        try:
            next(db_generator)
        except StopIteration:
            pass  # Expected behavior
    
    def test_create_test_database(self):
        """Test that create_test_database creates tables without error."""
        # This should not raise an exception
        create_test_database()
        
        # Should be able to connect to the database
        with test_engine.connect() as connection:
            assert connection is not None
    
    def test_drop_test_database(self):
        """Test that drop_test_database removes tables without error."""
        # First create the database
        create_test_database()
        
        # Then drop it - should not raise an exception
        drop_test_database()
    
    def test_get_test_db_session(self):
        """Test that get_test_db_session returns a working session."""
        session = get_test_db_session()
        
        assert isinstance(session, Session)
        assert session is not None
        
        # Should be able to execute a simple query
        result = session.execute(text("SELECT 1")).fetchone()
        assert result is not None
        assert result[0] == 1
        
        session.close()
    
    def test_reset_test_database(self):
        """Test that reset_test_database properly resets the database."""
        # Create database first
        create_test_database()
        
        # Reset should not raise an exception
        reset_test_database()
        
        # Should still be able to connect after reset
        session = get_test_db_session()
        assert isinstance(session, Session)
        session.close()


class TestDatabaseManagerTests:
    """Test suite for TestDatabaseManager context manager."""
    
    def test_database_manager_context(self):
        """Test that TestDatabaseManager works as a context manager."""
        with FixturesDatabaseManager() as db_manager:
            assert db_manager is not None
            
            # Should be able to get a session
            session = db_manager.get_session()
            assert isinstance(session, Session)
            session.close()
    
    def test_database_manager_cleanup(self):
        """Test that TestDatabaseManager properly cleans up."""
        db_manager = FixturesDatabaseManager()
        
        # Enter context
        db_manager.__enter__()
        
        # Should be able to get session
        session = db_manager.get_session()
        assert isinstance(session, Session)
        session.close()
        
        # Exit context - should not raise exception
        db_manager.__exit__(None, None, None)


class TestFixturesIntegration:
    """Integration tests for test fixtures with actual database operations."""
    
    @pytest.mark.integration
    def test_fixtures_work_with_fastapi_dependency_override(self):
        """Test that fixtures work properly with FastAPI dependency injection."""
        from app.core.database import get_db
        
        # Test that override_get_db can replace get_db
        original_db_gen = get_db()
        override_db_gen = override_get_db()
        
        # Both should be generators
        assert hasattr(original_db_gen, '__next__')
        assert hasattr(override_db_gen, '__next__')
        
        # Both should yield database sessions
        original_session = next(original_db_gen)
        override_session = next(override_db_gen)
        
        assert isinstance(original_session, Session)
        assert isinstance(override_session, Session)
        
        # They should be different sessions (different databases)
        assert original_session is not override_session
        
        # Clean up generators
        for gen in [original_db_gen, override_db_gen]:
            try:
                next(gen)
            except StopIteration:
                pass
    
    @pytest.mark.integration  
    def test_test_database_isolation(self):
        """Test that test database is isolated from main database."""
        from app.core.database import get_db, DATABASE_URL
        from app.tests.fixtures.test_database import TEST_DATABASE_URL
        
        # Test database should be different from main database
        assert TEST_DATABASE_URL != DATABASE_URL
        assert "memory" in TEST_DATABASE_URL or "test" in TEST_DATABASE_URL
        
        # Sessions should use different engines
        main_db_gen = get_db()
        test_db_gen = override_get_db()
        
        main_session = next(main_db_gen)
        test_session = next(test_db_gen)
        
        # Different engines
        assert main_session.bind != test_session.bind
        
        # Clean up
        for gen in [main_db_gen, test_db_gen]:
            try:
                next(gen)
            except StopIteration:
                pass

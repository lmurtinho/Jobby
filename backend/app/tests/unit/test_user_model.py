"""
Unit tests for User model - Issue #19.

Following Outside-In TDD approach - these tests verify the User model
implementation meets the requirements from the integration test.
"""

import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import Base
from app.tests.fixtures.test_database import (
    TestSessionLocal, test_engine, create_test_database, drop_test_database
)


class TestUserModel:
    """Test suite for User model functionality."""
    
    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        # Create tables for testing
        create_test_database()
        
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()
            # Clean up tables after test
            drop_test_database()
    
    def test_user_model_creation(self, db_session: Session):
        """Test that User model can be created with required fields."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "hashed_password": "hashed_password_123"
        }
        
        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Assert
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.hashed_password == "hashed_password_123"
        assert user.is_active is True  # Default value
        assert user.is_verified is False  # Default value
        assert user.currency == "USD"  # Default value
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
    
    def test_user_model_with_profile_fields(self, db_session: Session):
        """Test User model with all profile fields from integration test."""
        # Arrange - Data matching the integration test expectations
        user_data = {
            "email": "maria.silva@example.com",
            "name": "Maria Silva",
            "hashed_password": "hashed_password_123",
            "location": "São Paulo, Brazil",
            "timezone": "America/Sao_Paulo",
            "experience_level": "mid",
            "salary_min": 8000,
            "salary_max": 15000,
            "currency": "USD",
            "preferred_languages": ["Portuguese", "English"]
        }
        
        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Assert
        assert user.location == "São Paulo, Brazil"
        assert user.timezone == "America/Sao_Paulo"
        assert user.experience_level == "mid"
        assert user.salary_min == 8000
        assert user.salary_max == 15000
        assert user.currency == "USD"
        assert user.preferred_languages == ["Portuguese", "English"]
    
    def test_user_model_with_skills_data(self, db_session: Session):
        """Test User model with skills and resume data."""
        # Arrange
        skills_data = ["Python", "Machine Learning", "SQL", "TensorFlow"]
        user_data = {
            "email": "developer@example.com",
            "name": "Developer User",
            "hashed_password": "hashed_password_123",
            "skills": skills_data,
            "resume_text": "Sample resume text content",
            "resume_filename": "resume.pdf"
        }
        
        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Assert
        assert user.skills == ["Python", "Machine Learning", "SQL", "TensorFlow"]
        assert user.resume_text == "Sample resume text content"
        assert user.resume_filename == "resume.pdf"
    
    def test_user_email_uniqueness(self, db_session: Session):
        """Test that user emails must be unique."""
        # Arrange
        user1_data = {
            "email": "duplicate@example.com",
            "name": "User One",
            "hashed_password": "password1"
        }
        user2_data = {
            "email": "duplicate@example.com",
            "name": "User Two", 
            "hashed_password": "password2"
        }
        
        # Act & Assert
        user1 = User(**user1_data)
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(**user2_data)
        db_session.add(user2)
        
        with pytest.raises(Exception):  # Database integrity error
            db_session.commit()
    
    def test_user_str_representation(self, db_session: Session):
        """Test User model string representation."""
        # Arrange
        user = User(
            email="repr@example.com",
            name="Repr User",
            hashed_password="password"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Act
        user_str = str(user)
        
        # Assert
        assert "User" in user_str
        assert str(user.id) in user_str
        assert "repr@example.com" in user_str
        assert "Repr User" in user_str
    
    def test_user_is_authenticated_property(self, db_session: Session):
        """Test User is_authenticated property."""
        # Arrange
        active_user = User(
            email="active@example.com",
            name="Active User",
            hashed_password="password",
            is_active=True
        )
        inactive_user = User(
            email="inactive@example.com", 
            name="Inactive User",
            hashed_password="password",
            is_active=False
        )
        
        # Act & Assert
        assert active_user.is_authenticated is True
        assert inactive_user.is_authenticated is False
    
    def test_user_to_dict_method(self, db_session: Session):
        """Test User to_dict method for JSON serialization."""
        # Arrange
        user_data = {
            "email": "dict@example.com",
            "name": "Dict User",
            "hashed_password": "password",
            "location": "Test City",
            "experience_level": "senior",
            "skills": ["Python", "SQL"]
        }
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Act
        user_dict = user.to_dict()
        
        # Assert
        assert "id" in user_dict
        assert user_dict["email"] == "dict@example.com"
        assert user_dict["name"] == "Dict User"
        assert "hashed_password" not in user_dict  # Should not expose password
        assert user_dict["location"] == "Test City"
        assert user_dict["experience_level"] == "senior"
        assert user_dict["skills"] == ["Python", "SQL"]
        assert "created_at" in user_dict
        assert "updated_at" in user_dict
    
    def test_user_optional_fields_defaults(self, db_session: Session):
        """Test User model with minimal data and optional field defaults."""
        # Arrange - Only required fields
        user = User(
            email="minimal@example.com",
            name="Minimal User",
            hashed_password="password"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Assert optional fields have proper defaults/None values
        assert user.location is None
        assert user.timezone is None
        assert user.experience_level is None
        assert user.salary_min is None
        assert user.salary_max is None
        assert user.currency == "USD"  # Default value
        assert user.preferred_languages is None
        assert user.skills is None
        assert user.resume_text is None
        assert user.resume_filename is None
    
    def test_user_updated_at_timestamp_changes(self, db_session: Session):
        """Test that updated_at timestamp changes when user is modified."""
        # Arrange
        user = User(
            email="timestamp@example.com",
            name="Timestamp User",
            hashed_password="password"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        original_updated_at = user.updated_at
        
        # Act - Modify user
        user.name = "Updated Name"
        db_session.commit()
        db_session.refresh(user)
        
        # Assert
        assert user.updated_at > original_updated_at
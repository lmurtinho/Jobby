"""
Unit tests for Authentication Service - Issue #20.

Following Outside-In TDD approach - these tests verify the authentication service
implementation meets the requirements from the integration test.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.services.auth import AuthService, auth_service
from app.models.user import User
from app.schemas.user import UserRegistrationRequest, UserLoginRequest
from app.tests.fixtures.test_database import (
    TestSessionLocal, create_test_database, drop_test_database
)


class TestAuthService:
    """Test suite for AuthService functionality."""
    
    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        create_test_database()
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()
            drop_test_database()
    
    @pytest.fixture
    def auth_service_instance(self):
        """Create AuthService instance for testing."""
        return AuthService()
    
    @pytest.fixture
    def sample_user_registration(self):
        """Sample user registration data matching integration test."""
        return UserRegistrationRequest(
            email="maria.silva@example.com",
            password="SecurePassword123!",
            name="Maria Silva",
            location="São Paulo, Brazil",
            timezone="America/Sao_Paulo",
            experience_level="mid",
            salary_min=8000,
            salary_max=15000,
            currency="USD",
            preferred_languages=["Portuguese", "English"]
        )
    
    @pytest.fixture
    def sample_user_login(self):
        """Sample user login data."""
        return UserLoginRequest(
            email="maria.silva@example.com",
            password="SecurePassword123!"
        )
    
    def test_auth_service_initialization(self, auth_service_instance):
        """Test AuthService initializes properly."""
        assert auth_service_instance.pwd_context is not None
        assert auth_service_instance.secret_key is not None
        assert auth_service_instance.algorithm == "HS256"
        assert auth_service_instance.access_token_expire_minutes > 0
    
    def test_hash_password(self, auth_service_instance):
        """Test password hashing functionality."""
        # Arrange
        plain_password = "SecurePassword123!"
        
        # Act
        hashed = auth_service_instance.hash_password(plain_password)
        
        # Assert
        assert hashed is not None
        assert hashed != plain_password
        assert len(hashed) > 50  # Bcrypt hashes are long
        assert hashed.startswith("$2b$")  # Bcrypt format
    
    def test_verify_password_success(self, auth_service_instance):
        """Test password verification with correct password."""
        # Arrange
        plain_password = "SecurePassword123!"
        hashed_password = auth_service_instance.hash_password(plain_password)
        
        # Act
        is_valid = auth_service_instance.verify_password(plain_password, hashed_password)
        
        # Assert
        assert is_valid is True
    
    def test_verify_password_failure(self, auth_service_instance):
        """Test password verification with incorrect password."""
        # Arrange
        plain_password = "SecurePassword123!"
        wrong_password = "WrongPassword456!"
        hashed_password = auth_service_instance.hash_password(plain_password)
        
        # Act
        is_valid = auth_service_instance.verify_password(wrong_password, hashed_password)
        
        # Assert
        assert is_valid is False
    
    def test_create_access_token(self, auth_service_instance):
        """Test JWT access token creation."""
        # Arrange
        test_data = {"sub": "123", "email": "test@example.com"}
        
        # Act
        token = auth_service_instance.create_access_token(test_data)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 100  # JWTs are long strings
        
        # Verify token can be decoded
        decoded = jwt.decode(token, auth_service_instance.secret_key, algorithms=[auth_service_instance.algorithm])
        assert decoded["sub"] == "123"
        assert decoded["email"] == "test@example.com"
        assert "exp" in decoded
    
    def test_create_access_token_with_custom_expiry(self, auth_service_instance):
        """Test JWT token creation with custom expiration time."""
        # Arrange
        test_data = {"sub": "123"}
        custom_delta = timedelta(minutes=60)
        start_time = datetime.utcnow()
        
        # Act
        token = auth_service_instance.create_access_token(test_data, custom_delta)
        
        # Assert
        decoded = jwt.decode(token, auth_service_instance.secret_key, algorithms=[auth_service_instance.algorithm])
        exp_time = datetime.utcfromtimestamp(decoded["exp"])  # Use utcfromtimestamp
        expected_time = start_time + custom_delta
        
        # Allow 10 second tolerance for test execution time
        assert abs((exp_time - expected_time).total_seconds()) < 10
    
    def test_verify_token_success(self, auth_service_instance):
        """Test JWT token verification with valid token."""
        # Arrange
        test_data = {"sub": "123", "email": "test@example.com"}
        token = auth_service_instance.create_access_token(test_data)
        
        # Act
        payload = auth_service_instance.verify_token(token)
        
        # Assert
        assert payload is not None
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"
    
    def test_verify_token_invalid(self, auth_service_instance):
        """Test JWT token verification with invalid token."""
        # Arrange
        invalid_token = "invalid.jwt.token"
        
        # Act
        payload = auth_service_instance.verify_token(invalid_token)
        
        # Assert
        assert payload is None
    
    def test_get_user_by_email(self, auth_service_instance, db_session: Session):
        """Test getting user by email address."""
        # Arrange
        user = User(
            email="test@example.com",
            name="Test User",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        db_session.commit()
        
        # Act
        found_user = auth_service_instance.get_user_by_email(db_session, "test@example.com")
        
        # Assert
        assert found_user is not None
        assert found_user.email == "test@example.com"
        assert found_user.name == "Test User"
    
    def test_get_user_by_email_not_found(self, auth_service_instance, db_session: Session):
        """Test getting user by email when user doesn't exist."""
        # Act
        found_user = auth_service_instance.get_user_by_email(db_session, "nonexistent@example.com")
        
        # Assert
        assert found_user is None
    
    def test_get_user_by_id(self, auth_service_instance, db_session: Session):
        """Test getting user by ID."""
        # Arrange
        user = User(
            email="test@example.com",
            name="Test User",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Act
        found_user = auth_service_instance.get_user_by_id(db_session, user.id)
        
        # Assert
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == "test@example.com"
    
    def test_create_user_success(self, auth_service_instance, db_session: Session, sample_user_registration):
        """Test successful user creation."""
        # Act
        created_user = auth_service_instance.create_user(db_session, sample_user_registration)
        
        # Assert
        assert created_user is not None
        assert created_user.id is not None
        assert created_user.email == "maria.silva@example.com"
        assert created_user.name == "Maria Silva"
        assert created_user.location == "São Paulo, Brazil"
        assert created_user.experience_level == "mid"
        assert created_user.is_active is True
        assert created_user.is_verified is False
        
        # Verify password was hashed
        assert created_user.hashed_password != "SecurePassword123!"
        assert auth_service_instance.verify_password("SecurePassword123!", created_user.hashed_password)
    
    def test_create_user_duplicate_email(self, auth_service_instance, db_session: Session, sample_user_registration):
        """Test user creation with duplicate email fails."""
        # Arrange - Create first user
        auth_service_instance.create_user(db_session, sample_user_registration)
        
        # Act & Assert - Try to create duplicate
        with pytest.raises(HTTPException) as exc_info:
            auth_service_instance.create_user(db_session, sample_user_registration)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in str(exc_info.value.detail)
    
    def test_authenticate_user_success(self, auth_service_instance, db_session: Session, sample_user_registration, sample_user_login):
        """Test successful user authentication."""
        # Arrange - Create user first
        created_user = auth_service_instance.create_user(db_session, sample_user_registration)
        
        # Act
        authenticated_user = auth_service_instance.authenticate_user(db_session, sample_user_login)
        
        # Assert
        assert authenticated_user is not None
        assert authenticated_user.id == created_user.id
        assert authenticated_user.email == "maria.silva@example.com"
    
    def test_authenticate_user_wrong_email(self, auth_service_instance, db_session: Session):
        """Test authentication with non-existent email."""
        # Arrange
        login_data = UserLoginRequest(email="nonexistent@example.com", password="password")
        
        # Act
        authenticated_user = auth_service_instance.authenticate_user(db_session, login_data)
        
        # Assert
        assert authenticated_user is None
    
    def test_authenticate_user_wrong_password(self, auth_service_instance, db_session: Session, sample_user_registration):
        """Test authentication with wrong password."""
        # Arrange - Create user first
        auth_service_instance.create_user(db_session, sample_user_registration)
        
        wrong_login = UserLoginRequest(email="maria.silva@example.com", password="WrongPassword!")
        
        # Act
        authenticated_user = auth_service_instance.authenticate_user(db_session, wrong_login)
        
        # Assert
        assert authenticated_user is None
    
    def test_authenticate_user_inactive_account(self, auth_service_instance, db_session: Session, sample_user_registration, sample_user_login):
        """Test authentication with inactive account."""
        # Arrange - Create user and deactivate
        created_user = auth_service_instance.create_user(db_session, sample_user_registration)
        created_user.is_active = False
        db_session.commit()
        
        # Act
        authenticated_user = auth_service_instance.authenticate_user(db_session, sample_user_login)
        
        # Assert
        assert authenticated_user is None
    
    def test_generate_user_token(self, auth_service_instance, db_session: Session):
        """Test JWT token generation for user."""
        # Arrange
        user = User(
            id=123,
            email="test@example.com",
            name="Test User",
            hashed_password="hashed_password"
        )
        
        # Act
        token = auth_service_instance.generate_user_token(user)
        
        # Assert
        assert token is not None
        
        # Verify token contains user data
        decoded = jwt.decode(token, auth_service_instance.secret_key, algorithms=[auth_service_instance.algorithm])
        assert decoded["sub"] == "123"
        assert decoded["email"] == "test@example.com"
        assert decoded["name"] == "Test User"
    
    def test_global_auth_service_instance(self):
        """Test that global auth_service instance is available."""
        # Assert
        assert auth_service is not None
        assert isinstance(auth_service, AuthService)
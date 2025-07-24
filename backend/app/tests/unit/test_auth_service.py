"""
Unit tests for authentication service.

This module tests the AuthService class methods including password hashing,
JWT token generation/validation, and user authentication logic.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.services.auth import AuthService
from app.models.user import User
from app.schemas.user import UserCreate, TokenData
from fastapi import HTTPException


class TestAuthService:
    """Test suite for AuthService class."""
    
    @pytest.fixture
    def auth_service(self):
        """Create AuthService instance for testing."""
        return AuthService(secret_key="test_secret_key_for_testing_only")
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock(spec=Session)
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return UserCreate(
            email="test@example.com",
            password="SecurePassword123!",
            name="Test User",
            location="São Paulo, Brazil",
            timezone="America/Sao_Paulo",
            experience_level="mid",
            salary_min=5000,
            salary_max=10000,
            currency="USD",
            preferred_languages=["Portuguese", "English"]
        )
    
    @pytest.fixture
    def mock_user(self):
        """Mock User model instance."""
        user = Mock(spec=User)
        user.id = 1
        user.email = "test@example.com"
        user.password_hash = "$2b$12$test_hash"
        user.name = "Test User"
        user.is_active = True
        return user

    def test_hash_password(self, auth_service):
        """Test password hashing functionality."""
        password = "SecurePassword123!"
        hashed = auth_service.hash_password(password)
        
        # Check that hash is generated
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 20  # bcrypt hashes are long
        assert hashed != password  # Hash should be different from original
        
        # Check that same password produces different hashes (salt)
        hashed2 = auth_service.hash_password(password)
        assert hashed != hashed2

    def test_verify_password_success(self, auth_service):
        """Test password verification with correct password."""
        password = "SecurePassword123!"
        hashed = auth_service.hash_password(password)
        
        # Correct password should verify
        assert auth_service.verify_password(password, hashed) is True

    def test_verify_password_failure(self, auth_service):
        """Test password verification with incorrect password."""
        password = "SecurePassword123!"
        wrong_password = "WrongPassword456!"
        hashed = auth_service.hash_password(password)
        
        # Wrong password should not verify
        assert auth_service.verify_password(wrong_password, hashed) is False

    def test_create_access_token(self, auth_service):
        """Test JWT token creation."""
        data = {"sub": "1", "email": "test@example.com"}
        token = auth_service.create_access_token(data)
        
        # Check token is created
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50  # JWT tokens are long
        
        # Check token parts (header.payload.signature)
        parts = token.split(".")
        assert len(parts) == 3

    def test_create_access_token_with_expiry(self, auth_service):
        """Test JWT token creation with custom expiry."""
        data = {"sub": "1", "email": "test@example.com"}
        expires_delta = timedelta(minutes=60)
        token = auth_service.create_access_token(data, expires_delta)
        
        assert token is not None
        assert isinstance(token, str)

    def test_verify_token_success(self, auth_service):
        """Test JWT token verification with valid token."""
        data = {"sub": "1", "email": "test@example.com"}
        token = auth_service.create_access_token(data)
        
        # Verify token
        token_data = auth_service.verify_token(token)
        
        assert isinstance(token_data, TokenData)
        assert token_data.user_id == 1
        assert token_data.email == "test@example.com"

    def test_verify_token_invalid(self, auth_service):
        """Test JWT token verification with invalid token."""
        invalid_token = "invalid.jwt.token"
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            auth_service.verify_token(invalid_token)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in str(exc_info.value.detail)

    def test_verify_token_expired(self, auth_service):
        """Test JWT token verification with expired token."""
        data = {"sub": "1", "email": "test@example.com"}
        # Create token that expires immediately
        expires_delta = timedelta(seconds=-1)
        expired_token = auth_service.create_access_token(data, expires_delta)
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            auth_service.verify_token(expired_token)
        
        assert exc_info.value.status_code == 401

    def test_authenticate_user_success(self, auth_service, mock_db, mock_user):
        """Test user authentication with correct credentials."""
        # Setup mock
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Mock password verification to return True
        with patch.object(auth_service, 'verify_password', return_value=True):
            user = auth_service.authenticate_user(mock_db, "test@example.com", "password")
        
        assert user == mock_user
        mock_db.query.assert_called_once()

    def test_authenticate_user_not_found(self, auth_service, mock_db):
        """Test user authentication when user doesn't exist."""
        # Setup mock to return None (user not found)
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        user = auth_service.authenticate_user(mock_db, "nonexistent@example.com", "password")
        
        assert user is None

    def test_authenticate_user_wrong_password(self, auth_service, mock_db, mock_user):
        """Test user authentication with wrong password."""
        # Setup mock
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Mock password verification to return False
        with patch.object(auth_service, 'verify_password', return_value=False):
            user = auth_service.authenticate_user(mock_db, "test@example.com", "wrong_password")
        
        assert user is None

    def test_create_user_success(self, auth_service, mock_db, sample_user_data):
        """Test user creation with valid data."""
        # Setup mock - no existing user
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Mock the created user
        created_user = Mock(spec=User)
        created_user.id = 1
        created_user.email = sample_user_data.email
        
        user = auth_service.create_user(mock_db, sample_user_data)
        
        # Verify database operations
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_create_user_email_exists(self, auth_service, mock_db, sample_user_data, mock_user):
        """Test user creation when email already exists."""
        # Setup mock - existing user found
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            auth_service.create_user(mock_db, sample_user_data)
        
        assert exc_info.value.status_code == 400
        assert "Email already registered" in str(exc_info.value.detail)

    def test_get_current_user_success(self, auth_service, mock_db, mock_user):
        """Test getting current user with valid token."""
        # Create a valid token
        data = {"sub": "1", "email": "test@example.com"}
        token = auth_service.create_access_token(data)
        
        # Setup mock
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        user = auth_service.get_current_user(mock_db, token)
        
        assert user == mock_user

    def test_get_current_user_not_found(self, auth_service, mock_db):
        """Test getting current user when user doesn't exist in database."""
        # Create a valid token
        data = {"sub": "999", "email": "nonexistent@example.com"}
        token = auth_service.create_access_token(data)
        
        # Setup mock - user not found
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            auth_service.get_current_user(mock_db, token)
        
        assert exc_info.value.status_code == 401
        assert "User not found" in str(exc_info.value.detail)

    def test_get_current_user_invalid_token(self, auth_service, mock_db):
        """Test getting current user with invalid token."""
        invalid_token = "invalid.jwt.token"
        
        # Should raise HTTPException from verify_token
        with pytest.raises(HTTPException) as exc_info:
            auth_service.get_current_user(mock_db, invalid_token)
        
        assert exc_info.value.status_code == 401

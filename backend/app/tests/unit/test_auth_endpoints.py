"""
Unit tests for Authentication Endpoints - Issue #20.

Following Outside-In TDD approach - these tests verify the authentication router
endpoints meet the requirements from the integration test.
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserRegistrationRequest, UserLoginRequest
from app.tests.fixtures.test_database import (
    TestSessionLocal, create_test_database, drop_test_database, override_get_db
)


class TestAuthenticationEndpoints:
    """Test suite for authentication router endpoints."""
    
    @pytest.fixture(autouse=True)
    def setup_test_db(self):
        """Set up test database for each test."""
        create_test_database()
        # Override database dependency
        app.dependency_overrides[get_db] = override_get_db
        yield
        drop_test_database()
        # Clean up dependency override
        app.dependency_overrides.clear()
    
    @pytest.fixture
    def client(self):
        """FastAPI test client."""
        return TestClient(app)
    
    @pytest.fixture
    def sample_registration_data(self):
        """Sample user registration data matching integration test."""
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        return {
            "email": f"maria.silva.{unique_id}@example.com",
            "password": "SecurePassword123!",
            "name": "Maria Silva",
            "location": "São Paulo, Brazil",
            "timezone": "America/Sao_Paulo",
            "experience_level": "mid",
            "salary_min": 8000,
            "salary_max": 15000,
            "currency": "USD",
            "preferred_languages": ["Portuguese", "English"]
        }
    
    @pytest.fixture
    def sample_login_data(self, sample_registration_data):
        """Sample user login data."""
        return {
            "email": sample_registration_data["email"],
            "password": "SecurePassword123!"
        }
    
    def test_register_endpoint_success(self, client: TestClient, sample_registration_data):
        """Test successful user registration endpoint - matches integration test expectation."""
        # Act
        response = client.post("/api/v1/auth/register", json=sample_registration_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        response_data = response.json()
        assert "id" in response_data
        assert "access_token" in response_data
        assert response_data["email"] == sample_registration_data["email"]
        assert response_data["name"] == "Maria Silva"
        assert response_data["token_type"] == "bearer"
        
        # Verify access token is a valid JWT string
        assert isinstance(response_data["access_token"], str)
        assert len(response_data["access_token"]) > 100
    
    def test_register_endpoint_duplicate_email(self, client: TestClient, sample_registration_data):
        """Test registration with duplicate email fails."""
        # Arrange - Register first user
        client.post("/api/v1/auth/register", json=sample_registration_data)
        
        # Act - Try to register duplicate
        response = client.post("/api/v1/auth/register", json=sample_registration_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_endpoint_invalid_email(self, client: TestClient, sample_registration_data):
        """Test registration with invalid email format."""
        # Arrange
        sample_registration_data["email"] = "invalid-email"
        
        # Act
        response = client.post("/api/v1/auth/register", json=sample_registration_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_endpoint_weak_password(self, client: TestClient, sample_registration_data):
        """Test registration with weak password."""
        # Arrange
        sample_registration_data["password"] = "123"  # Too short
        
        # Act
        response = client.post("/api/v1/auth/register", json=sample_registration_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_endpoint_missing_required_fields(self, client: TestClient):
        """Test registration with missing required fields."""
        # Arrange
        incomplete_data = {
            "email": "test@example.com"
            # Missing password and name
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=incomplete_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_endpoint_invalid_experience_level(self, client: TestClient, sample_registration_data):
        """Test registration with invalid experience level.""" 
        # Arrange
        sample_registration_data["experience_level"] = "invalid_level"
        
        # Act
        response = client.post("/api/v1/auth/register", json=sample_registration_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_endpoint_invalid_salary_range(self, client: TestClient, sample_registration_data):
        """Test registration with invalid salary range (max < min)."""
        # Arrange
        sample_registration_data["salary_min"] = 15000
        sample_registration_data["salary_max"] = 8000  # Less than min
        
        # Act
        response = client.post("/api/v1/auth/register", json=sample_registration_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_endpoint_success(self, client: TestClient, sample_registration_data, sample_login_data):
        """Test successful user login endpoint."""
        # Arrange - Register user first
        client.post("/api/v1/auth/register", json=sample_registration_data)
        
        # Act
        response = client.post("/api/v1/auth/login", json=sample_login_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert "id" in response_data
        assert "access_token" in response_data
        assert response_data["email"] == sample_registration_data["email"]
        assert response_data["name"] == "Maria Silva"
        assert response_data["token_type"] == "bearer"
    
    def test_login_endpoint_wrong_email(self, client: TestClient, sample_registration_data):
        """Test login with non-existent email."""
        # Arrange - Register user first
        client.post("/api/v1/auth/register", json=sample_registration_data)
        
        wrong_login = {
            "email": "nonexistent@example.com",
            "password": "SecurePassword123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=wrong_login)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_endpoint_wrong_password(self, client: TestClient, sample_registration_data):
        """Test login with wrong password."""
        # Arrange - Register user first
        client.post("/api/v1/auth/register", json=sample_registration_data)
        
        wrong_login = {
            "email": "maria.silva@example.com",
            "password": "WrongPassword!"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=wrong_login)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_endpoint_invalid_email_format(self, client: TestClient):
        """Test login with invalid email format."""
        # Arrange
        invalid_login = {
            "email": "invalid-email",
            "password": "password"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=invalid_login)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_endpoint_missing_fields(self, client: TestClient):
        """Test login with missing required fields."""
        # Arrange
        incomplete_login = {
            "email": "test@example.com"
            # Missing password
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=incomplete_login)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_user_profile_endpoint_success(self, client: TestClient, sample_registration_data):
        """Test getting user profile with valid token."""
        # Arrange - Register user and get token
        register_response = client.post("/api/v1/auth/register", json=sample_registration_data)
        access_token = register_response.json()["access_token"]
        user_id = register_response.json()["id"]
        
        auth_headers = {"Authorization": f"Bearer {access_token}"}
        
        # Act
        response = client.get(f"/api/v1/users/{user_id}/profile", headers=auth_headers)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        profile_data = response.json()
        assert profile_data["email"] == sample_registration_data["email"]
        assert profile_data["name"] == "Maria Silva"
        assert profile_data["location"] == "São Paulo, Brazil"
        assert profile_data["experience_level"] == "mid"
        assert profile_data["salary_min"] == 8000
        assert profile_data["salary_max"] == 15000
    
    def test_user_profile_endpoint_no_token(self, client: TestClient, sample_registration_data):
        """Test getting user profile without authentication token."""
        # Arrange - Register user
        register_response = client.post("/api/v1/auth/register", json=sample_registration_data)
        user_id = register_response.json()["id"]
        
        # Act - Request without auth header
        response = client.get(f"/api/v1/users/{user_id}/profile")
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_user_profile_endpoint_invalid_token(self, client: TestClient, sample_registration_data):
        """Test getting user profile with invalid token."""
        # Arrange - Register user
        register_response = client.post("/api/v1/auth/register", json=sample_registration_data)
        user_id = register_response.json()["id"]
        
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        
        # Act
        response = client.get(f"/api/v1/users/{user_id}/profile", headers=invalid_headers)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_authentication_flow_integration(self, client: TestClient, sample_registration_data, sample_login_data):
        """Test complete authentication flow: register � login � access protected endpoint."""
        # Step 1: Register user
        register_response = client.post("/api/v1/auth/register", json=sample_registration_data)
        assert register_response.status_code == status.HTTP_201_CREATED
        
        register_data = register_response.json()
        user_id = register_data["id"]
        register_token = register_data["access_token"]
        
        # Step 2: Login with same credentials
        login_response = client.post("/api/v1/auth/login", json=sample_login_data)
        assert login_response.status_code == status.HTTP_200_OK
        
        login_data = login_response.json()
        login_token = login_data["access_token"]
        
        # Step 3: Access protected endpoint with both tokens
        register_headers = {"Authorization": f"Bearer {register_token}"}
        login_headers = {"Authorization": f"Bearer {login_token}"}
        
        # Both tokens should work for protected endpoints
        profile_response_1 = client.get(f"/api/v1/users/{user_id}/profile", headers=register_headers)
        profile_response_2 = client.get(f"/api/v1/users/{user_id}/profile", headers=login_headers)
        
        assert profile_response_1.status_code == status.HTTP_200_OK
        assert profile_response_2.status_code == status.HTTP_200_OK
        
        # Profile data should be identical
        assert profile_response_1.json() == profile_response_2.json()


class TestAuthenticationEndpointsErrorHandling:
    """Test suite for authentication endpoint error handling."""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client."""
        return TestClient(app)
    
    def test_register_endpoint_malformed_json(self, client: TestClient):
        """Test registration endpoint with malformed JSON."""
        # Act
        response = client.post(
            "/api/v1/auth/register", 
            data="malformed json",
            headers={"Content-Type": "application/json"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_endpoint_malformed_json(self, client: TestClient):
        """Test login endpoint with malformed JSON."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            data="malformed json", 
            headers={"Content-Type": "application/json"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_endpoints_with_wrong_http_method(self, client: TestClient):
        """Test authentication endpoints with wrong HTTP methods."""
        # Test GET on POST endpoints
        register_response = client.get("/api/v1/auth/register")
        login_response = client.get("/api/v1/auth/login")
        
        assert register_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert login_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
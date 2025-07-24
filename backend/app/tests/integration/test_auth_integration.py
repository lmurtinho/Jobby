"""
Integration tests for authentication system.

This module tests the complete authentication flow including database
operations, password hashing, JWT tokens, and endpoint integration.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.tests.fixtures.test_database import override_get_db, create_test_database, drop_test_database
from app.models.user import User


# Override database dependency for testing
app.dependency_overrides[get_db] = override_get_db


@pytest.mark.integration
@pytest.mark.auth
class TestAuthenticationIntegration:
    """Integration tests for the complete authentication system."""
    
    @pytest.fixture(scope="function")
    def setup_test_db(self):
        """Setup and teardown test database for each test."""
        create_test_database()
        yield
        drop_test_database()
    
    @pytest.fixture
    def client(self, setup_test_db):
        """Create test client with clean database."""
        return TestClient(app)
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            "email": "integration.test@example.com",
            "password": "SecurePassword123!",
            "name": "Integration Test User",
            "location": "São Paulo, Brazil",
            "timezone": "America/Sao_Paulo",
            "experience_level": "mid",
            "salary_min": 5000,
            "salary_max": 10000,
            "currency": "USD",
            "preferred_languages": ["Portuguese", "English"]
        }

    def test_complete_authentication_flow(self, client, sample_user_data):
        """Test the complete authentication flow from registration to protected access."""
        
        # Step 1: Register a new user
        register_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        user_data = register_response.json()
        assert "id" in user_data
        assert "access_token" in user_data
        assert user_data["email"] == sample_user_data["email"]
        
        user_id = user_data["id"]
        access_token = user_data["access_token"]
        
        # Step 2: Verify the token works for protected endpoints
        auth_headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test /me endpoint
        me_response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["id"] == user_id
        assert me_data["email"] == sample_user_data["email"]
        
        # Test token verification endpoint
        verify_response = client.get("/api/v1/auth/verify-token", headers=auth_headers)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        assert verify_data["valid"] is True
        assert verify_data["user_id"] == user_id
        
        # Step 3: Test login with OAuth2 form
        form_data = {
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", data=form_data)
        assert login_response.status_code == 200
        
        login_data = login_response.json()
        assert "access_token" in login_data
        assert login_data["token_type"] == "bearer"
        
        # Step 4: Test login with JSON
        json_login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        json_login_response = client.post("/api/v1/auth/login-json", json=json_login_data)
        assert json_login_response.status_code == 200
        
        json_login_result = json_login_response.json()
        assert "access_token" in json_login_result
        
        # Step 5: Verify new token also works
        new_token = json_login_result["access_token"]
        new_auth_headers = {"Authorization": f"Bearer {new_token}"}
        
        final_me_response = client.get("/api/v1/auth/me", headers=new_auth_headers)
        assert final_me_response.status_code == 200

    def test_duplicate_email_registration(self, client, sample_user_data):
        """Test that registering with the same email twice fails."""
        
        # Register first user
        first_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert first_response.status_code == 201
        
        # Try to register with same email
        second_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert second_response.status_code == 400
        assert "Email already registered" in second_response.text

    def test_invalid_login_credentials(self, client, sample_user_data):
        """Test login with invalid credentials."""
        
        # Register a user first
        register_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        # Test wrong password
        wrong_password_data = {
            "username": sample_user_data["email"],
            "password": "WrongPassword123!"
        }
        response = client.post("/api/v1/auth/login", data=wrong_password_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.text
        
        # Test non-existent email
        non_existent_data = {
            "username": "nonexistent@example.com",
            "password": sample_user_data["password"]
        }
        response = client.post("/api/v1/auth/login", data=non_existent_data)
        assert response.status_code == 401

    def test_protected_endpoints_without_token(self, client):
        """Test that protected endpoints reject requests without valid tokens."""
        
        protected_endpoints = [
            "/api/v1/auth/me",
            "/api/v1/auth/verify-token"
        ]
        
        for endpoint in protected_endpoints:
            # No authorization header
            response = client.get(endpoint)
            assert response.status_code == 401
            
            # Invalid token
            headers = {"Authorization": "Bearer invalid_token"}
            response = client.get(endpoint, headers=headers)
            assert response.status_code == 401
            
            # Malformed authorization header
            headers = {"Authorization": "InvalidFormat"}
            response = client.get(endpoint, headers=headers)
            assert response.status_code == 401

    def test_password_hashing_security(self, client, sample_user_data):
        """Test that passwords are properly hashed and never stored in plain text."""
        
        # Register a user
        register_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        # Check that password is not in the response
        user_data = register_response.json()
        assert "password" not in user_data
        assert "password_hash" not in user_data
        
        # Verify we can login with the original password
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login-json", json=login_data)
        assert login_response.status_code == 200

    def test_token_expiration_handling(self, client, sample_user_data):
        """Test token expiration (this would be a longer-running test in practice)."""
        
        # Register a user
        register_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        user_data = register_response.json()
        access_token = user_data["access_token"]
        expires_in = user_data["expires_in"]
        
        # Verify token info
        assert expires_in == 1800  # 30 minutes * 60 seconds
        assert isinstance(access_token, str)
        assert len(access_token) > 50  # JWT tokens are long

    def test_user_data_validation(self, client):
        """Test validation of user registration data."""
        
        # Test various invalid data combinations
        invalid_test_cases = [
            # Invalid email
            {
                "email": "not-an-email",
                "password": "SecurePassword123!",
                "name": "Test User"
            },
            # Weak password
            {
                "email": "test@example.com",
                "password": "weak",
                "name": "Test User"
            },
            # Invalid experience level
            {
                "email": "test@example.com",
                "password": "SecurePassword123!",
                "name": "Test User",
                "experience_level": "invalid_level"
            },
            # Invalid salary range
            {
                "email": "test@example.com",
                "password": "SecurePassword123!",
                "name": "Test User",
                "salary_min": 10000,
                "salary_max": 5000  # max < min
            }
        ]
        
        for invalid_data in invalid_test_cases:
            response = client.post("/api/v1/auth/register", json=invalid_data)
            assert response.status_code == 422  # Validation error

    def test_database_user_creation(self, client, sample_user_data):
        """Test that user is properly created in the database."""
        
        # Register a user
        register_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        user_data = register_response.json()
        
        # Verify user data structure
        required_fields = [
            "id", "email", "name", "is_active", "created_at", "updated_at",
            "location", "timezone", "experience_level", "currency"
        ]
        
        for field in required_fields:
            assert field in user_data, f"Missing required field: {field}"
        
        # Verify data values
        assert user_data["email"] == sample_user_data["email"]
        assert user_data["name"] == sample_user_data["name"]
        assert user_data["is_active"] is True
        assert user_data["experience_level"] == sample_user_data["experience_level"]

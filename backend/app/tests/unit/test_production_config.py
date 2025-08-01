"""
Unit tests for production configuration functionality.

Generated from failing integration test following outside-in TDD methodology.
These tests will drive implementation of production config endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestProductionConfig:
    """Unit tests for production configuration - will FAIL initially and drive implementation."""
    
    def test_config_status_endpoint_exists(self):
        """Test that config status endpoint exists."""
        response = client.get("/api/v1/config/status")
        # Should not be 404 (endpoint exists)
        assert response.status_code != 404, "Config status endpoint must exist"
        # Should be 200 (successful response)
        assert response.status_code == 200, "Config status endpoint must respond with 200"
    
    def test_config_status_response_format(self):
        """Test config status endpoint returns proper JSON format."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        data = response.json()
        
        # Required configuration status fields
        required_fields = [
            "environment",
            "claude_api_configured", 
            "database_configured",
            "frontend_url_configured",
            "secret_key_configured"
        ]
        
        for field in required_fields:
            assert field in data, f"Config status missing required field: {field}"
    
    def test_config_status_boolean_values(self):
        """Test config status returns proper boolean values."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        data = response.json()
        
        # Configuration status fields should be boolean
        boolean_fields = [
            "claude_api_configured",
            "database_configured", 
            "frontend_url_configured",
            "secret_key_configured"
        ]
        
        for field in boolean_fields:
            assert isinstance(data[field], bool), f"Config field {field} should be boolean"
    
    def test_config_status_environment_detection(self):
        """Test config status properly detects environment."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        data = response.json()
        
        # Environment should be valid value
        valid_environments = ["development", "testing", "production"]
        assert data["environment"] in valid_environments, f"Invalid environment: {data['environment']}"
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    def test_config_status_claude_api_detection(self):
        """Test config status detects Claude API configuration."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["claude_api_configured"] is True, "Should detect Claude API key when present"
    
    @patch.dict('os.environ', {}, clear=True)
    def test_config_status_missing_claude_api(self):
        """Test config status detects missing Claude API configuration."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["claude_api_configured"] is False, "Should detect missing Claude API key"
    
    @patch.dict('os.environ', {'DATABASE_URL': 'postgresql://user:pass@host/db'})
    def test_config_status_database_detection(self):
        """Test config status detects database configuration."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["database_configured"] is True, "Should detect database URL when present"
    
    @patch.dict('os.environ', {'FRONTEND_URL': 'https://app.vercel.app'})
    def test_config_status_frontend_url_detection(self):
        """Test config status detects frontend URL configuration."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["frontend_url_configured"] is True, "Should detect frontend URL when present"
    
    @patch.dict('os.environ', {'SECRET_KEY': 'production-secret'})
    def test_config_status_secret_key_detection(self):
        """Test config status detects secret key configuration."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["secret_key_configured"] is True, "Should detect secret key when present"
    
    def test_config_status_production_requirements(self):
        """Test config status validates production requirements."""
        with patch.dict('os.environ', {
            'ENVIRONMENT': 'production',
            'DATABASE_URL': 'postgresql://user:pass@host/db',
            'ANTHROPIC_API_KEY': 'claude-key',
            'FRONTEND_URL': 'https://app.vercel.app',
            'SECRET_KEY': 'production-secret'
        }):
            response = client.get("/api/v1/config/status")
            assert response.status_code == 200
            
            data = response.json()
            
            # In production, all configs should be present
            assert data["environment"] == "production"
            assert data["claude_api_configured"] is True
            assert data["database_configured"] is True  
            assert data["frontend_url_configured"] is True
            assert data["secret_key_configured"] is True
    
    def test_config_status_does_not_expose_secrets(self):
        """Test config status doesn't expose actual secret values."""
        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://user:secret@host/db',
            'ANTHROPIC_API_KEY': 'sk-ant-secret-key',
            'SECRET_KEY': 'super-secret-key'
        }):
            response = client.get("/api/v1/config/status")
            assert response.status_code == 200
            
            response_text = response.text
            
            # Should not expose actual secret values
            assert "secret" not in response_text.lower(), "Should not expose secret values"
            assert "sk-ant-" not in response_text, "Should not expose API keys"
            assert "postgresql://user:secret" not in response_text, "Should not expose DB credentials"
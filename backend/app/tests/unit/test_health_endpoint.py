"""
Unit tests for health endpoint functionality.

Generated from failing integration test following outside-in TDD methodology.
These tests will drive implementation of the health endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Unit tests for health endpoint - will FAIL initially and drive implementation."""
    
    def test_health_endpoint_exists(self):
        """Test that health endpoint exists and responds."""
        response = client.get("/health")
        # Should not be 404 (endpoint exists)
        assert response.status_code != 404, "Health endpoint must exist"
        # Should be 200 (healthy response)  
        assert response.status_code == 200, "Health endpoint must respond with 200"
    
    def test_health_endpoint_response_format(self):
        """Test health endpoint returns proper JSON format."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        
        # Required fields for production health checks
        required_fields = ["status", "database", "timestamp"]
        for field in required_fields:
            assert field in data, f"Health response missing required field: {field}"
    
    def test_health_endpoint_status_values(self):
        """Test health endpoint returns valid status values."""
        response = client.get("/health")  
        assert response.status_code == 200
        
        data = response.json()
        
        # Status should be valid value
        assert data["status"] in ["healthy", "unhealthy"], "Invalid health status value"
        assert data["database"] in ["connected", "disconnected"], "Invalid database status value"
    
    def test_health_endpoint_database_connection_check(self):
        """Test health endpoint checks actual database connection."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        
        # Should include database status
        assert "database" in data, "Health response must include database status"
        assert data["database"] == "connected", "Database should be connected in healthy state"
    
    def test_health_endpoint_includes_environment_info(self):
        """Test health endpoint includes environment information."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        
        # Should include environment and version info
        assert "environment" in data, "Health response should include environment"
        assert "version" in data, "Health response should include version"
    
    def test_health_endpoint_includes_database_url_info(self):
        """Test health endpoint includes database URL information (for production validation)."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        
        # Should include database URL info (masked for security)
        assert "database_url" in data, "Health response should include database URL info"
        
        # Should not expose full database URL for security
        db_url = data["database_url"]
        assert "password" not in db_url.lower(), "Database URL should not expose password"
    
    @patch('app.core.database.get_database_status')
    def test_health_endpoint_handles_database_failure(self, mock_db_status):
        """Test health endpoint handles database connection failures gracefully."""
        # Mock database connection failure
        mock_db_status.return_value = {"status": "disconnected", "error": "Connection failed"}
        
        response = client.get("/health")
        
        # Should still respond (not crash)
        assert response.status_code == 200, "Health endpoint should handle DB failures gracefully"
        
        data = response.json()
        assert data["status"] == "unhealthy", "Should report unhealthy when DB disconnected"
        assert data["database"] == "disconnected", "Should report database disconnected"
    
    def test_health_endpoint_performance(self):
        """Test health endpoint responds quickly."""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0, f"Health endpoint too slow: {response_time:.2f}s (should be <1s)"
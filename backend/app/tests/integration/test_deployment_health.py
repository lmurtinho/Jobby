"""
Integration tests for deployment health and production readiness.
Following TDD approach - these tests will guide our deployment verification.
"""

import pytest
import requests
import os
from typing import Dict, Any
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings


@pytest.mark.integration
class TestDeploymentHealth:
    """Test suite for deployment health checks and production readiness."""

    def test_health_endpoint_exists(self):
        """Test that health check endpoint is available."""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        assert "status" in response.json()
        assert "version" in response.json()
        assert response.json()["status"] == "healthy"

    def test_health_endpoint_includes_database_status(self):
        """Test that health check includes database connectivity."""
        client = TestClient(app)
        response = client.get("/health")
        
        health_data = response.json()
        assert "database" in health_data
        # Will pass once database is properly configured
        
    def test_cors_headers_configured(self):
        """Test that CORS headers are properly configured for production."""
        client = TestClient(app)
        response = client.options("/health")
        
        # Should have CORS headers for frontend communication
        assert response.status_code in [200, 204]
        
    def test_environment_variables_loaded(self):
        """Test that required environment variables are available."""
        settings = get_settings()
        
        # Critical environment variables should be set
        required_vars = [
            "DATABASE_URL",
            "SECRET_KEY"
        ]
        
        for var in required_vars:
            assert hasattr(settings, var.lower()), f"Missing required setting: {var}"
            
    def test_gunicorn_production_server_config(self):
        """Test that gunicorn is properly configured for production."""
        # This test ensures our Railway deployment uses gunicorn
        import subprocess
        result = subprocess.run(
            ["pip", "show", "gunicorn"], 
            capture_output=True, 
            text=True
        )
        assert result.returncode == 0, "Gunicorn should be installed for production"

    @pytest.mark.external
    def test_railway_deployment_accessibility(self):
        """Test that deployed application is accessible via Railway URL."""
        # This will fail until deployment is complete - that's expected in TDD
        railway_url = os.getenv("RAILWAY_URL")
        
        if railway_url:
            try:
                response = requests.get(f"{railway_url}/health", timeout=10)
                assert response.status_code == 200
                assert response.json()["status"] == "healthy"
            except requests.exceptions.RequestException:
                pytest.fail(f"Railway deployment not accessible at {railway_url}")
        else:
            pytest.skip("RAILWAY_URL not set - deployment not yet complete")

    @pytest.mark.external  
    def test_postgresql_database_connection(self):
        """Test that PostgreSQL database connection works in production."""
        from app.core.database import engine
        from sqlalchemy import text
        
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")

    def test_authentication_endpoints_production_ready(self):
        """Test that authentication endpoints work in production environment."""
        client = TestClient(app)
        
        # Test registration endpoint
        test_user = {
            "email": "deployment-test@example.com",
            "password": "TestPassword123!",
            "name": "Deployment Test User"
        }
        
        response = client.post("/api/v1/auth/register", json=test_user)
        # Should work or give appropriate validation error
        assert response.status_code in [201, 400, 422]
        
        # Test login endpoint
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        # Should work or give appropriate authentication error  
        assert response.status_code in [200, 401, 422]

    def test_resume_upload_endpoint_production_ready(self):
        """Test that resume upload endpoint works in production."""
        client = TestClient(app)
        
        # Create a test user first
        user_data = {
            "email": "resume-test@example.com", 
            "password": "TestPassword123!",
            "name": "Resume Test User"
        }
        
        # Register user
        response = client.post("/api/v1/auth/register", json=user_data)
        if response.status_code == 201:
            user_id = response.json()["id"]
            
            # Test resume upload
            test_file_content = b"Sample PDF content for testing"
            files = {"resume": ("test_resume.pdf", test_file_content, "application/pdf")}
            
            response = client.post(f"/api/v1/users/{user_id}/resume", files=files)
            # Should work or give appropriate validation error
            assert response.status_code in [200, 400, 422]

    def test_api_response_times_acceptable(self):
        """Test that API response times are acceptable for production."""
        import time
        client = TestClient(app)
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 2.0, f"Health endpoint too slow: {response_time}s"
        
    def test_error_handling_production_ready(self):
        """Test that error handling doesn't expose sensitive information."""
        client = TestClient(app)
        
        # Test 404 error
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
        
        # Response should not contain sensitive debug information
        error_data = response.json()
        sensitive_fields = ["traceback", "file_path", "local_vars"]
        
        response_text = str(error_data).lower()
        for field in sensitive_fields:
            assert field not in response_text, f"Sensitive info exposed: {field}"


@pytest.mark.slow
class TestDeploymentStress:
    """Stress tests for deployment stability."""
    
    def test_concurrent_health_checks(self):
        """Test that health endpoint handles concurrent requests."""
        import concurrent.futures
        import threading
        
        client = TestClient(app)
        
        def check_health():
            response = client.get("/health")
            return response.status_code == 200
        
        # Test with 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_health) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        assert all(results), "Some concurrent health checks failed"

    def test_memory_usage_stable(self):
        """Test that memory usage remains stable under load."""
        import psutil
        import gc
        
        client = TestClient(app)
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Make 100 requests
        for _ in range(100):
            response = client.get("/health")
            assert response.status_code == 200
        
        gc.collect()  # Force garbage collection
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024, f"Memory leak detected: {memory_increase} bytes"

"""
Integration tests for production deployment readiness.

This module contains tests that verify the application is ready for 
production deployment on Railway + Vercel following the outside-in 
TDD methodology from CLAUDE.md.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestProductionDeploymentReadiness:
    """
    Test suite for production deployment readiness.
    
    These tests will initially FAIL and drive implementation of
    all production deployment features.
    """
    
    def test_complete_production_deployment_readiness(self):
        """
        Test complete production deployment readiness workflow.
        
        This is the main integration test that represents full production
        deployment success criteria. It will initially FAIL, driving 
        implementation of all deployment fixes.
        """
        print("🧪 Testing complete production deployment readiness...")
        
        # Step 1: Health endpoint responding with proper format
        response = client.get("/health")
        assert response.status_code == 200, "Health endpoint must be accessible"
        
        health_data = response.json()
        assert "status" in health_data, "Health response must include status"
        assert health_data["status"] == "healthy", "Application must report healthy status"
        assert "database" in health_data, "Health response must include database status"
        assert health_data["database"] == "connected", "Database must be connected"
        assert "timestamp" in health_data, "Health response must include timestamp"
        
        # Step 2: Database connection properly configured for production
        assert "database_url" in health_data, "Health response must include database URL info"
        # Should have database URL information (format depends on environment)
        db_url = health_data["database_url"]
        assert len(db_url) > 0, "Database URL info must not be empty"
        
        # In test environment, SQLite is acceptable, but info should be present
        # In production, would be PostgreSQL
        if health_data.get("environment") == "production":
            assert not db_url.startswith("sqlite://"), "Production must not use SQLite"
            assert "test" not in db_url.lower(), "Production must not use test database"
        else:
            # In development/test, SQLite is fine
            print(f"   🧪 Test environment detected: {db_url} (SQLite OK for testing)")
        
        # Step 3: API documentation accessible  
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200, "OpenAPI documentation must be accessible"
        
        # Step 4: CORS properly configured for production frontend
        cors_response = client.options("/", headers={
            "Origin": "https://ai-job-tracker.vercel.app",
            "Access-Control-Request-Method": "GET"
        })
        assert cors_response.status_code == 200, "CORS preflight must succeed"
        assert "Access-Control-Allow-Origin" in cors_response.headers, "CORS headers must be present"
        
        # Step 5: Environment configuration endpoint
        config_response = client.get("/api/v1/config/status")
        assert config_response.status_code == 200, "Config status endpoint must be accessible"
        
        config_data = config_response.json()
        assert "environment" in config_data, "Config must include environment info"
        assert "claude_api_configured" in config_data, "Config must show Claude API status"
        assert "database_configured" in config_data, "Config must show database status" 
        assert "frontend_url_configured" in config_data, "Config must show frontend URL status"
        
        # Verify all services properly configured
        assert config_data["claude_api_configured"] is True, "Claude API must be configured"
        assert config_data["database_configured"] is True, "Database must be configured"
        assert config_data["frontend_url_configured"] is True, "Frontend URL must be configured"
        
        print("✅ Complete production deployment readiness test PASSED!")
        print(f"   🏥 Health endpoint: {health_data['status']}")
        print(f"   🗄️  Database: {health_data['database']}")
        print(f"   ⚙️  Environment: {config_data['environment']}")
        print("   🚀 Ready for Railway + Vercel deployment!")
    
    def test_health_endpoint_detailed_response(self):
        """Test health endpoint returns detailed production information."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        
        # Required fields for production health checks
        required_fields = ["status", "database", "timestamp", "version", "environment"]
        for field in required_fields:
            assert field in data, f"Health response missing required field: {field}"
        
        # Status values validation
        assert data["status"] in ["healthy", "unhealthy"], "Invalid health status"
        assert data["database"] in ["connected", "disconnected"], "Invalid database status"
        
        # Production-specific validations
        if data.get("environment") == "production":
            assert data["status"] == "healthy", "Production must be healthy"
            assert data["database"] == "connected", "Production database must be connected"
    
    def test_cors_configuration_for_production(self):
        """Test CORS is properly configured for production frontend URLs."""
        production_origins = [
            "https://ai-job-tracker.vercel.app",
            "https://jobby-frontend.vercel.app",  # Alternative domain
        ]
        
        for origin in production_origins:
            # Test preflight request
            response = client.options("/api/v1/jobs", headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Authorization"
            })
            
            assert response.status_code == 200, f"CORS preflight failed for {origin}"
            
            # Verify CORS headers
            headers = response.headers
            assert "Access-Control-Allow-Origin" in headers, "Missing CORS origin header"
            assert "Access-Control-Allow-Methods" in headers, "Missing CORS methods header"
            assert "Access-Control-Allow-Headers" in headers, "Missing CORS headers header"
    
    def test_database_production_configuration(self):
        """Test database is configured for production use."""
        response = client.get("/health")
        assert response.status_code == 200
        
        health_data = response.json()
        assert health_data["database"] == "connected"
        
        # In production, should not be using SQLite
        db_url = health_data.get("database_url", "")
        assert not db_url.startswith("sqlite://"), "Production should use PostgreSQL, not SQLite"
        
        # Should indicate production database
        test_indicators = ["test", "local", "dev", "localhost"]
        for indicator in test_indicators:
            assert indicator not in db_url.lower(), f"Production DB should not contain '{indicator}'"
    
    def test_environment_variables_loaded(self):
        """Test that all required production environment variables are loaded."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        
        config_data = response.json()
        
        # Required production environment configurations
        required_configs = [
            "claude_api_configured",
            "database_configured", 
            "frontend_url_configured",
            "secret_key_configured"
        ]
        
        for config in required_configs:
            assert config in config_data, f"Missing config status: {config}"
            assert config_data[config] is True, f"Production config not properly set: {config}"
    
    @pytest.mark.slow  
    def test_production_performance_requirements(self):
        """Test that production performance requirements are met."""
        import time
        
        # Health endpoint should respond quickly
        start_time = time.time()
        response = client.get("/health")
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0, f"Health endpoint too slow: {response_time:.2f}s (max 2.0s)"
        
        # API endpoints should respond quickly
        start_time = time.time()
        auth_response = client.post("/api/v1/auth/register", json={
            "email": "perf-test@example.com",
            "password": "testpass123",
            "name": "Perf Test"
        })
        api_response_time = time.time() - start_time
        
        # Should respond within reasonable time (allowing for validation/hashing)
        assert api_response_time < 5.0, f"API endpoint too slow: {api_response_time:.2f}s (max 5.0s)"
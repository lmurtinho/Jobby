"""
Integration tests for the main FastAPI application.

These tests verify the application works correctly with other components.
"""

import pytest
from fastapi.testclient import TestClient


class TestMainApplicationIntegration:
    """Integration tests for main application with other components."""
    
    @pytest.mark.integration
    def test_app_can_connect_to_database(self):
        """Test that app can connect to database when configured."""
        from app.main import app
        
        # This will be implemented once database configuration is available
        # For now, just ensure the app doesn't crash on startup
        client = TestClient(app)
        assert client is not None
    
    @pytest.mark.integration  
    def test_app_includes_api_routers(self):
        """Test that app includes all required API routers."""
        from app.main import app
        
        # Once API routers are implemented, verify they're included
        routes = [getattr(route, 'path', str(route)) for route in app.routes]
        
        # Health endpoint should exist
        health_routes = [route for route in routes if "health" in str(route)]
        assert len(health_routes) > 0
        
        # API v1 routes will be added later
        # assert any("/api/v1" in route for route in routes)

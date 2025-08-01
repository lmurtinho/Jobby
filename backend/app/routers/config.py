"""
Configuration status router for production deployment monitoring.

This module provides endpoints to check the configuration status of
various services and environment variables required for production deployment.
"""

import os
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/config", tags=["Configuration"])


@router.get("/status")
async def get_config_status() -> Dict[str, Any]:
    """
    Get configuration status for production deployment validation.
    
    Returns configuration status for all critical services and environment
    variables required for production deployment.
    
    Returns:
        Dict[str, Any]: Configuration status information
    """
    
    # Check environment variables
    claude_api_key = os.getenv("ANTHROPIC_API_KEY")
    database_url = os.getenv("DATABASE_URL")
    frontend_url = os.getenv("FRONTEND_URL")
    secret_key = os.getenv("SECRET_KEY")
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    environment = os.getenv("ENVIRONMENT", "development")
    
    return {
        "environment": environment,
        "claude_api_configured": bool(claude_api_key and len(claude_api_key.strip()) > 0),
        "database_configured": bool(database_url and len(database_url.strip()) > 0),
        "frontend_url_configured": bool(frontend_url and len(frontend_url.strip()) > 0),
        "secret_key_configured": bool(secret_key and len(secret_key.strip()) > 0),
        "jwt_secret_configured": bool(jwt_secret and len(jwt_secret.strip()) > 0),
        "production_ready": all([
            claude_api_key and len(claude_api_key.strip()) > 0,
            database_url and len(database_url.strip()) > 0,
            frontend_url and len(frontend_url.strip()) > 0,
            secret_key and len(secret_key.strip()) > 0,
            jwt_secret and len(jwt_secret.strip()) > 0
        ])
    }
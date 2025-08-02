"""
Main FastAPI application for AI Job Tracker.

This module creates and configures the FastAPI application instance
following the project architecture and coding standards defined in CLAUDE.md.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, AsyncGenerator

from app.core.database import create_tables
from app.routers import auth, users, jobs, config

@app.on_event("startup")
async def create_tables():
    from app.core.database import create_tables
    create_tables()
    
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for startup and shutdown events.
    
    Args:
        app: FastAPI application instance
        
    Yields:
        None: Control during application lifetime
    """
    # Startup
    print("🚀 AI Job Tracker API starting up...")
    # Initialize database tables
    create_tables()
    print("✅ Database tables initialized")
    
    yield
    
    # Shutdown
    print("🛑 AI Job Tracker API shutting down...")
    # TODO: Add cleanup tasks
    # TODO: Close database connections
    # TODO: Save any pending data


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    # Create FastAPI application with basic configuration
    application = FastAPI(
        title="AI Job Tracker API",
        description="A comprehensive job tracking application that automatically finds, scores, and manages AI/ML/Data Science job opportunities for remote workers in Brazil and Latin America",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,  # Use modern lifespan approach
    )
    
    # Configure CORS middleware for frontend integration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    application.include_router(auth.router)
    application.include_router(users.router)
    application.include_router(jobs.router)
    application.include_router(config.router)
    
    # Add health check endpoint
    @application.get("/health", tags=["Health"])
    async def health_check() -> Dict[str, Any]:
        """
        Health check endpoint for monitoring and load balancer.
        
        Returns:
            Dict[str, Any]: Health status information
        """
        from app.core.database import engine
        from sqlalchemy import text
        from datetime import datetime
        import os
        
        # Check database connectivity
        db_status = "connected"
        db_url_info = "sqlite://test"  # Default fallback
        overall_status = "healthy"
        
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
                
                # Get database URL info (masked for security)
                db_url = os.getenv("DATABASE_URL", str(engine.url))
                if "postgresql://" in db_url:
                    db_url_info = "postgresql://production"
                elif "sqlite://" in db_url:
                    db_url_info = "sqlite://development"
                else:
                    db_url_info = "unknown://configured"
                    
        except Exception as e:
            db_status = "disconnected"
            overall_status = "unhealthy"
            print(f"Database health check failed: {e}")
        
        return {
            "status": overall_status,
            "database": db_status,  # Changed from nested object to string
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "database_url": db_url_info  # Masked URL info
        }
    
    @application.options("/health", tags=["Health"])
    async def health_check_options() -> Dict[str, Any]:
        """
        CORS preflight handler for health check endpoint.
        
        Returns:
            Dict[str, Any]: Empty response for CORS preflight
        """
        return {}
    
    return application


# Create the application instance
app = create_application()

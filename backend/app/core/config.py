"""
Configuration management for AI Job Tracker.

This module provides centralized configuration management with 
environment variable support and validation.
"""

import os
from typing import Optional
from functools import lru_cache


class Settings:
    """
    Application settings with environment variable support.
    
    Provides centralized configuration management for the application
    with support for different environments and validation.
    """
    
    def __init__(self):
        """Initialize settings with environment variables and defaults."""
        
        # Database Configuration
        self.database_url: str = os.getenv(
            'DATABASE_URL', 
            'postgresql://user:password@localhost/jobby_dev'
        )
        
        # Security Configuration
        self.secret_key: str = os.getenv(
            'SECRET_KEY', 
            'dev-secret-key-change-in-production-minimum-32-characters'
        )
        self.algorithm: str = os.getenv('ALGORITHM', 'HS256')
        self.access_token_expire_minutes: int = int(os.getenv(
            'ACCESS_TOKEN_EXPIRE_MINUTES', 
            '60' if os.getenv('ENVIRONMENT') == 'production' else '1440'  # 1 hour prod, 24 hours dev
        ))
        
        # Environment Detection
        self.environment: str = os.getenv('ENVIRONMENT', 'development')
        
        # API Configuration
        self.api_v1_str: str = os.getenv('API_V1_STR', '/api/v1')
        
        # Claude API Configuration (for future Day 4 enhancement)
        self.claude_api_key: Optional[str] = os.getenv('CLAUDE_API_KEY', None)
        self.claude_api_base_url: str = os.getenv(
            'CLAUDE_API_BASE_URL', 
            'https://api.anthropic.com'
        )
        
        # Logging Configuration
        self.log_level: str = os.getenv('LOG_LEVEL', 'INFO')
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self) -> None:
        """Validate that all required settings are properly configured."""
        
        # Ensure secret key is not empty
        if not self.secret_key or self.secret_key.strip() == '':
            self.secret_key = 'dev-secret-key-change-in-production-minimum-32-characters'
        
        # Ensure database URL is not empty
        if not self.database_url or self.database_url.strip() == '':
            self.database_url = 'postgresql://user:password@localhost/jobby_dev'
        
        # Validate environment
        if self.environment not in ['development', 'production', 'testing']:
            self.environment = 'development'
        
        # Validate log level
        if self.log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            self.log_level = 'INFO'
        
        # Ensure minimum security in production
        if self.environment == 'production':
            if self.access_token_expire_minutes > 60:
                self.access_token_expire_minutes = 60  # Max 1 hour in production
            
            # Ensure secret key is strong enough for production
            if self.secret_key == 'dev-secret-key-change-in-production-minimum-32-characters':
                raise ValueError(
                    "SECRET_KEY environment variable must be set for production environment"
                )


# Global settings instance - implements singleton pattern for performance
_settings_instance: Optional[Settings] = None


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (singleton pattern).
    
    Returns the same Settings instance on subsequent calls for performance.
    Uses lru_cache to ensure singleton behavior.
    
    Returns:
        Settings: The application settings object
    """
    return Settings()


def clear_settings_cache() -> None:
    """
    Clear the settings cache.
    
    This function is primarily used for testing to ensure that
    environment variable changes are picked up in new settings instances.
    """
    global _settings_instance
    _settings_instance = None
    get_settings.cache_clear()
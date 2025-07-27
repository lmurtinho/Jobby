"""
Unit tests for app.core.config module.

Following TDD approach - these tests will guide the implementation
of the configuration management system.
"""

import pytest
import os
from unittest.mock import patch
from typing import Dict, Any


class TestCoreConfigModule:
    """Test suite for core configuration module."""
    
    def test_config_module_can_be_imported(self):
        """Test that app.core.config module can be imported."""
        try:
            from app.core.config import get_settings
            assert get_settings is not None
        except ImportError:
            pytest.fail("app.core.config module should be importable")
    
    def test_get_settings_function_exists(self):
        """Test that get_settings function exists and is callable."""
        from app.core.config import get_settings
        assert callable(get_settings)
    
    def test_get_settings_returns_settings_object(self):
        """Test that get_settings returns a settings object."""
        from app.core.config import get_settings
        settings = get_settings()
        assert settings is not None
        assert hasattr(settings, '__dict__')  # Should be an object with attributes


class TestSettingsObject:
    """Test suite for the Settings object returned by get_settings."""
    
    def test_settings_has_database_configuration(self):
        """Test that settings object has database configuration."""
        from app.core.config import get_settings
        settings = get_settings()
        
        # Should have database URL configuration
        assert hasattr(settings, 'database_url')
        assert isinstance(settings.database_url, str)
    
    def test_settings_has_security_configuration(self):
        """Test that settings object has security configuration."""
        from app.core.config import get_settings
        settings = get_settings()
        
        # Should have JWT configuration
        assert hasattr(settings, 'secret_key')
        assert hasattr(settings, 'algorithm')
        assert hasattr(settings, 'access_token_expire_minutes')
        
        assert isinstance(settings.secret_key, str)
        assert isinstance(settings.algorithm, str)
        assert isinstance(settings.access_token_expire_minutes, int)
    
    def test_settings_has_environment_detection(self):
        """Test that settings object can detect environment."""
        from app.core.config import get_settings
        settings = get_settings()
        
        assert hasattr(settings, 'environment')
        assert settings.environment in ['development', 'production', 'testing']
    
    def test_settings_has_api_configuration(self):
        """Test that settings object has API configuration."""
        from app.core.config import get_settings
        settings = get_settings()
        
        assert hasattr(settings, 'api_v1_str')
        assert isinstance(settings.api_v1_str, str)
        assert settings.api_v1_str.startswith('/api/')


class TestEnvironmentVariableHandling:
    """Test suite for environment variable configuration."""
    
    @patch.dict(os.environ, {
        'DATABASE_URL': 'postgresql://test:test@localhost/test_db',
        'SECRET_KEY': 'test-secret-key-123',
        'ENVIRONMENT': 'testing'
    })
    def test_settings_reads_from_environment_variables(self):
        """Test that settings are properly read from environment variables."""
        from app.core.config import get_settings, clear_settings_cache
        clear_settings_cache()  # Clear cache to ensure fresh settings
        settings = get_settings()
        
        assert settings.database_url == 'postgresql://test:test@localhost/test_db'
        assert settings.secret_key == 'test-secret-key-123'
        assert settings.environment == 'testing'
    
    def test_settings_has_default_values(self):
        """Test that settings have reasonable defaults when env vars not set."""
        with patch.dict(os.environ, {}, clear=True):
            from app.core.config import get_settings, clear_settings_cache
            clear_settings_cache()  # Clear cache to ensure fresh settings
            settings = get_settings()
            
            # Should have defaults for required settings
            assert settings.database_url is not None
            assert settings.secret_key is not None
            assert settings.algorithm == 'HS256'
            assert settings.access_token_expire_minutes > 0
            assert settings.environment == 'development'  # Default environment
    
    @patch.dict(os.environ, {'SECRET_KEY': ''})
    def test_settings_handles_empty_environment_variables(self):
        """Test that settings handle empty environment variables gracefully."""
        from app.core.config import get_settings
        settings = get_settings()
        
        # Should not use empty string, should fall back to default
        assert settings.secret_key != ''
        assert len(settings.secret_key) > 0


class TestSettingsValidation:
    """Test suite for settings validation and error handling."""
    
    def test_settings_validates_required_fields(self):
        """Test that settings validation catches missing required fields."""
        from app.core.config import get_settings
        settings = get_settings()
        
        # These fields should never be None or empty
        assert settings.secret_key
        assert settings.database_url
        assert settings.algorithm
        assert settings.access_token_expire_minutes > 0
    
    def test_settings_singleton_behavior(self):
        """Test that get_settings returns the same instance (singleton pattern)."""
        from app.core.config import get_settings
        
        settings1 = get_settings()
        settings2 = get_settings()
        
        # Should be the same instance for performance
        assert settings1 is settings2


class TestClaudeAPIConfiguration:
    """Test suite for Claude API configuration (for Day 4 integration)."""
    
    def test_settings_has_claude_api_configuration(self):
        """Test that settings object has Claude API configuration."""
        from app.core.config import get_settings
        settings = get_settings()
        
        # Should have Claude API configuration for future enhancement
        assert hasattr(settings, 'claude_api_key')
        assert hasattr(settings, 'claude_api_base_url')
    
    @patch.dict(os.environ, {'CLAUDE_API_KEY': 'test-claude-key'})
    def test_claude_api_key_from_environment(self):
        """Test that Claude API key is read from environment."""
        from app.core.config import get_settings, clear_settings_cache
        clear_settings_cache()  # Clear cache to ensure fresh settings
        settings = get_settings()
        
        assert settings.claude_api_key == 'test-claude-key'


class TestLoggingConfiguration:
    """Test suite for logging configuration."""
    
    def test_settings_has_logging_configuration(self):
        """Test that settings object has logging configuration."""
        from app.core.config import get_settings
        settings = get_settings()
        
        assert hasattr(settings, 'log_level')
        assert settings.log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    
    @patch.dict(os.environ, {'LOG_LEVEL': 'DEBUG'})
    def test_log_level_from_environment(self):
        """Test that log level is read from environment."""
        from app.core.config import get_settings, clear_settings_cache
        clear_settings_cache()  # Clear cache to ensure fresh settings
        settings = get_settings()
        
        assert settings.log_level == 'DEBUG'


class TestProductionConfiguration:
    """Test suite for production-specific configuration."""
    
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'production',
        'SECRET_KEY': 'production-secret-key-at-least-32-characters-long-12345'
    })
    def test_production_environment_settings(self):
        """Test that production environment has appropriate settings."""
        from app.core.config import get_settings, clear_settings_cache
        clear_settings_cache()  # Clear cache to ensure fresh settings
        settings = get_settings()
        
        assert settings.environment == 'production'
        # In production, should have stricter security defaults
        assert settings.access_token_expire_minutes <= 60  # Shorter token expiry
    
    @patch.dict(os.environ, {'ENVIRONMENT': 'development'})
    def test_development_environment_settings(self):
        """Test that development environment has appropriate settings."""
        from app.core.config import get_settings, clear_settings_cache
        clear_settings_cache()  # Clear cache to ensure fresh settings  
        settings = get_settings()
        
        assert settings.environment == 'development'
        # In development, can have longer token expiry for convenience
        assert settings.access_token_expire_minutes >= 30
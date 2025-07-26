"""
Unit tests for resume upload endpoint.

Tests for Issue #26 - Add missing resume upload endpoint placeholder.
These tests validate the POST /api/v1/users/{user_id}/resume endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status, UploadFile
from unittest.mock import Mock
from io import BytesIO
from datetime import datetime

from app.main import app
from app.core.database import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserResponse


class TestResumeUploadEndpoint:
    """Unit tests for resume upload endpoint."""
    
    def setup_method(self):
        """Set up test dependencies."""
        self.client = TestClient(app)
        
        # Mock database dependency
        def mock_get_db():
            return Mock()
        
        # Mock current user
        self.mock_user = UserResponse(
            id=1,
            email="test@example.com",
            name="Test User",
            is_active=True,
            is_verified=True,
            created_at=datetime(2024, 1, 1),
            updated_at=datetime(2024, 1, 1),
            location=None,
            timezone=None,
            experience_level=None,
            salary_min=None,
            salary_max=None,
            currency="USD",
            preferred_languages=None,
            skills=None,
            resume_filename=None
        )
        
        def mock_get_current_user():
            return self.mock_user
        
        # Override dependencies
        app.dependency_overrides[get_db] = mock_get_db
        app.dependency_overrides[get_current_user] = mock_get_current_user
    
    def teardown_method(self):
        """Clean up after tests."""
        app.dependency_overrides = {}
    
    def test_upload_resume_success(self):
        """Test successful resume upload."""
        # Arrange
        user_id = 1
        pdf_content = b"%PDF-1.4 fake pdf content"
        files = {"resume": ("test_resume.pdf", BytesIO(pdf_content), "application/pdf")}
        
        # Act
        response = self.client.post(f"/api/v1/users/{user_id}/resume", files=files)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "filename" in data
        assert "parsing_result" in data
        assert "skills_extracted" in data
        assert data["filename"] == "test_resume.pdf"
        assert data["parsing_result"]["status"] == "placeholder"
        assert isinstance(data["skills_extracted"], list)
        assert len(data["skills_extracted"]) > 0
    
    def test_upload_resume_wrong_user(self):
        """Test resume upload for different user (should fail)."""
        # Arrange
        user_id = 2  # Different from mock user ID (1)
        pdf_content = b"%PDF-1.4 fake pdf content"
        files = {"resume": ("test_resume.pdf", BytesIO(pdf_content), "application/pdf")}
        
        # Act
        response = self.client.post(f"/api/v1/users/{user_id}/resume", files=files)
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Access denied" in response.json()["detail"]
    
    def test_upload_resume_invalid_file_type(self):
        """Test resume upload with non-PDF file."""
        # Arrange
        user_id = 1
        txt_content = b"This is a text file, not a PDF"
        files = {"resume": ("test_resume.txt", BytesIO(txt_content), "text/plain")}
        
        # Act
        response = self.client.post(f"/api/v1/users/{user_id}/resume", files=files)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Only PDF files are supported" in response.json()["detail"]
    
    def test_upload_resume_no_filename(self):
        """Test that upload fails when file has no filename."""
        # Create file without filename
        file_content = b"%PDF-1.4 test content"
        file = UploadFile(filename=None, file=BytesIO(file_content))
        
        response = self.client.post(
            f"/api/v1/users/{self.mock_user.id}/resume",
            files={"file": ("", file_content, "application/pdf")}
        )
        
        # FastAPI returns 422 for validation errors
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_upload_resume_missing_file(self):
        """Test resume upload without file."""
        # Arrange
        user_id = 1
        
        # Act - No files parameter
        response = self.client.post(f"/api/v1/users/{user_id}/resume")
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_upload_resume_response_structure(self):
        """Test that response has correct structure for Day 2+ integration."""
        # Arrange
        user_id = 1
        pdf_content = b"%PDF-1.4 fake pdf content"
        files = {"resume": ("resume.pdf", BytesIO(pdf_content), "application/pdf")}
        
        # Act
        response = self.client.post(f"/api/v1/users/{user_id}/resume", files=files)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Validate response structure matches ResumeUploadResponse schema
        assert isinstance(data["filename"], str)
        assert isinstance(data["parsing_result"], dict)
        assert isinstance(data["skills_extracted"], list)
        
        # Validate placeholder content
        parsing_result = data["parsing_result"]
        assert "status" in parsing_result
        assert "message" in parsing_result
        assert "Day 2" in parsing_result["message"]
        
        # Validate placeholder skills
        skills = data["skills_extracted"]
        expected_skills = ["Python", "SQL", "Machine Learning"]
        assert all(skill in skills for skill in expected_skills)


@pytest.mark.integration
class TestResumeUploadIntegration:
    """Integration tests for resume upload with real authentication."""
    
    def test_resume_upload_requires_authentication(self):
        """Test that unauthenticated requests are rejected."""
        # Don't set up authentication dependency override
        client = TestClient(app)
        
        file_content = b"%PDF-1.4 test content"
        response = client.post(
            "/api/v1/users/1/resume",
            files={"file": ("test.pdf", file_content, "application/pdf")}
        )
        
        # FastAPI returns 403 for authentication failures
        assert response.status_code == status.HTTP_403_FORBIDDEN

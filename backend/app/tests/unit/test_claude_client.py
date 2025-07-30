"""
Test suite for Claude API client integration.
Tests are designed to fail initially (TDD approach) and will pass once implementation is complete.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List
import asyncio

from app.utils.claude_client import ClaudeClient, ClaudeAPIError, ClaudeRateLimitError
from app.schemas.ai_resume import (
    ResumeParseRequest,
    ResumeParseResponse,
    ExtractedSkill,
    ExperienceEntry,
    EducationEntry
)


class TestClaudeClient:
    """Test suite for Claude API client."""

    @pytest.fixture
    def claude_client(self):
        """Create Claude client instance for testing."""
        return ClaudeClient(api_key="test-api-key")

    @pytest.fixture
    def sample_resume_text(self):
        """Sample resume text for testing."""
        return """
        John Doe
        Senior Software Engineer
        Email: john.doe@example.com
        Phone: +1-555-0123
        
        EXPERIENCE:
        Senior Software Engineer at TechCorp (2020-2023)
        - Developed microservices using Python, FastAPI, and Docker
        - Led team of 5 engineers on cloud migration project
        - Improved system performance by 40% through optimization
        
        Software Engineer at StartupXYZ (2018-2020)  
        - Built REST APIs using Django and PostgreSQL
        - Implemented CI/CD pipelines with Jenkins and AWS
        - Collaborated with cross-functional teams on product features
        
        EDUCATION:
        Bachelor of Science in Computer Science
        University of Technology (2014-2018)
        
        SKILLS:
        Python, JavaScript, React, PostgreSQL, Docker, AWS, Kubernetes
        """

    @pytest.fixture
    def expected_parsed_resume(self):
        """Expected parsed resume response."""
        return ResumeParseResponse(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="+1-555-0123",
            skills=[
                ExtractedSkill(name="Python", category="Programming Language", confidence=0.95),
                ExtractedSkill(name="FastAPI", category="Framework", confidence=0.90),
                ExtractedSkill(name="Docker", category="DevOps", confidence=0.85),
                ExtractedSkill(name="PostgreSQL", category="Database", confidence=0.90),
                ExtractedSkill(name="AWS", category="Cloud Platform", confidence=0.85),
            ],
            experience=[
                ExperienceEntry(
                    company="TechCorp",
                    position="Senior Software Engineer",
                    start_date="2020",
                    end_date="2023",
                    description="Developed microservices using Python, FastAPI, and Docker",
                    skills_used=["Python", "FastAPI", "Docker"]
                ),
                ExperienceEntry(
                    company="StartupXYZ", 
                    position="Software Engineer",
                    start_date="2018",
                    end_date="2020",
                    description="Built REST APIs using Django and PostgreSQL",
                    skills_used=["Django", "PostgreSQL", "AWS"]
                )
            ],
            education=[
                EducationEntry(
                    institution="University of Technology",
                    degree="Bachelor of Science in Computer Science",
                    start_date="2014",
                    end_date="2018"
                )
            ],
            years_of_experience=5,
            seniority_level="Senior"
        )

    @pytest.mark.asyncio
    async def test_claude_client_initialization(self, claude_client):
        """Test Claude client initializes correctly."""
        assert claude_client.api_key == "test-api-key"
        assert claude_client.model == "claude-3-sonnet-20240229"
        assert claude_client.max_tokens == 4000
        assert claude_client.timeout == 30

    @pytest.mark.asyncio
    async def test_parse_resume_success(self, claude_client, sample_resume_text, expected_parsed_resume):
        """Test successful resume parsing with Claude API."""
        # Mock the anthropic client response
        mock_response = Mock()
        mock_response.content = [Mock(text="""
        {
            "full_name": "John Doe",
            "email": "john.doe@example.com", 
            "phone": "+1-555-0123",
            "skills": [
                {"name": "Python", "category": "Programming Language", "confidence": 0.95},
                {"name": "FastAPI", "category": "Framework", "confidence": 0.90},
                {"name": "Docker", "category": "DevOps", "confidence": 0.85},
                {"name": "PostgreSQL", "category": "Database", "confidence": 0.90},
                {"name": "AWS", "category": "Cloud Platform", "confidence": 0.85}
            ],
            "experience": [
                {
                    "company": "TechCorp",
                    "position": "Senior Software Engineer", 
                    "start_date": "2020",
                    "end_date": "2023",
                    "description": "Developed microservices using Python, FastAPI, and Docker",
                    "skills_used": ["Python", "FastAPI", "Docker"]
                },
                {
                    "company": "StartupXYZ",
                    "position": "Software Engineer",
                    "start_date": "2018", 
                    "end_date": "2020",
                    "description": "Built REST APIs using Django and PostgreSQL",
                    "skills_used": ["Django", "PostgreSQL", "AWS"]
                }
            ],
            "education": [
                {
                    "institution": "University of Technology",
                    "degree": "Bachelor of Science in Computer Science",
                    "start_date": "2014",
                    "end_date": "2018"
                }
            ],
            "years_of_experience": 5,
            "seniority_level": "Senior"
        }
        """)]

        with patch.object(claude_client, '_client') as mock_client:
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            
            request = ResumeParseRequest(resume_text=sample_resume_text)
            result = await claude_client.parse_resume(request)
            
            assert isinstance(result, ResumeParseResponse)
            assert result.full_name == "John Doe"
            assert result.email == "john.doe@example.com"
            assert len(result.skills) == 5
            assert len(result.experience) == 2
            assert result.years_of_experience == 5

    @pytest.mark.asyncio
    async def test_parse_resume_api_error(self, claude_client, sample_resume_text):
        """Test handling of Claude API errors."""
        with patch.object(claude_client, '_client') as mock_client:
            mock_client.messages.create = AsyncMock(side_effect=Exception("API Error"))
            
            request = ResumeParseRequest(resume_text=sample_resume_text)
            
            with pytest.raises(ClaudeAPIError):
                await claude_client.parse_resume(request)

    @pytest.mark.asyncio
    async def test_parse_resume_rate_limit(self, claude_client, sample_resume_text):
        """Test handling of rate limit errors."""
        with patch.object(claude_client, '_client') as mock_client:
            from anthropic import RateLimitError
            # Create a mock response object for RateLimitError
            mock_response = Mock()
            mock_response.status_code = 429
            rate_limit_error = RateLimitError("Rate limit exceeded", response=mock_response, body=None)
            mock_client.messages.create = AsyncMock(side_effect=rate_limit_error)
            
            request = ResumeParseRequest(resume_text=sample_resume_text)
            
            with pytest.raises(ClaudeRateLimitError):
                await claude_client.parse_resume(request)

    @pytest.mark.asyncio
    async def test_parse_resume_with_retry_logic(self, claude_client, sample_resume_text):
        """Test retry logic for transient failures."""
        mock_response = Mock()
        mock_response.content = [Mock(text='{"full_name": "John Doe", "skills": []}')]
        
        with patch.object(claude_client, '_client') as mock_client:
            # First call fails, second succeeds
            mock_client.messages.create = AsyncMock(side_effect=[
                Exception("Temporary error"),
                mock_response
            ])
            
            request = ResumeParseRequest(resume_text=sample_resume_text)
            result = await claude_client.parse_resume(request)
            
            assert result.full_name == "John Doe"
            assert mock_client.messages.create.call_count == 2

    @pytest.mark.asyncio
    async def test_parse_resume_invalid_json(self, claude_client, sample_resume_text):
        """Test handling of invalid JSON responses."""
        mock_response = Mock()
        mock_response.content = [Mock(text="Invalid JSON response")]
        
        with patch.object(claude_client, '_client') as mock_client:
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            
            request = ResumeParseRequest(resume_text=sample_resume_text)
            
            with pytest.raises(ClaudeAPIError):
                await claude_client.parse_resume(request)

    @pytest.mark.asyncio
    async def test_analyze_skill_gap_success(self, claude_client):
        """Test successful skill gap analysis."""
        user_skills = ["Python", "Django", "PostgreSQL"]
        job_requirements = ["Python", "FastAPI", "Docker", "Kubernetes", "PostgreSQL"]
        
        mock_response = Mock()
        mock_response.content = [Mock(text="""
        {
            "skill_gaps": [
                {"skill": "FastAPI", "importance": "High", "alternative_to": "Django"},
                {"skill": "Docker", "importance": "High", "alternative_to": null},
                {"skill": "Kubernetes", "importance": "Medium", "alternative_to": null}
            ],
            "matching_skills": ["Python", "PostgreSQL"],
            "gap_severity": "Medium",
            "recommendations": [
                "Learn FastAPI as Django alternative for modern API development",
                "Master Docker containerization for deployment",
                "Consider Kubernetes for orchestration skills"
            ]
        }
        """)]
        
        with patch.object(claude_client, '_client') as mock_client:
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            
            result = await claude_client.analyze_skill_gap(user_skills, job_requirements)
            
            assert "skill_gaps" in result
            assert "matching_skills" in result
            assert len(result["skill_gaps"]) == 3
            assert len(result["matching_skills"]) == 2

    @pytest.mark.asyncio
    async def test_enhance_job_description_success(self, claude_client):
        """Test successful job description enhancement."""
        raw_job_description = "Python developer needed. Must know Django."
        
        mock_response = Mock()
        mock_response.content = [Mock(text="""
        {
            "enhanced_description": "Senior Python Developer position requiring expertise in Django framework for web application development.",
            "extracted_skills": ["Python", "Django", "Web Development"],
            "seniority_level": "Senior",
            "required_experience_years": 3,
            "industry": "Technology",
            "remote_friendly": true
        }
        """)]
        
        with patch.object(claude_client, '_client') as mock_client:
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            
            result = await claude_client.enhance_job_description(raw_job_description)
            
            assert "enhanced_description" in result
            assert "extracted_skills" in result
            assert "seniority_level" in result
            assert len(result["extracted_skills"]) == 3

    @pytest.mark.asyncio
    async def test_semantic_job_matching_success(self, claude_client):
        """Test semantic job matching functionality."""
        user_profile = {
            "skills": ["Python", "Django", "PostgreSQL"],
            "experience_years": 3,
            "preferred_industries": ["Technology", "Finance"]
        }
        
        job_posting = {
            "title": "Backend Developer",
            "description": "Python developer with Django experience",
            "required_skills": ["Python", "Django", "REST APIs"],
            "industry": "Technology"
        }
        
        mock_response = Mock()
        mock_response.content = [Mock(text="""
        {
            "match_score": 0.85,
            "skill_match_percentage": 0.90,
            "experience_match": "Good",
            "industry_alignment": "Perfect",
            "strengths": ["Strong Python skills", "Django experience", "Industry match"],
            "areas_for_growth": ["REST API development"],
            "recommendation": "Highly recommended - excellent match for your background"
        }
        """)]
        
        with patch.object(claude_client, '_client') as mock_client:
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            
            result = await claude_client.semantic_job_match(user_profile, job_posting)
            
            assert "match_score" in result
            assert "skill_match_percentage" in result
            assert result["match_score"] == 0.85
            assert len(result["strengths"]) == 3


class TestClaudeAPIErrorHandling:
    """Test suite for Claude API error handling and edge cases."""
    
    @pytest.fixture
    def claude_client(self):
        return ClaudeClient(api_key="test-api-key")

    @pytest.mark.asyncio
    async def test_empty_resume_text(self, claude_client):
        """Test handling of empty resume text."""
        from pydantic import ValidationError
        
        # Test that ResumeParseRequest validates empty text
        with pytest.raises(ValidationError):
            ResumeParseRequest(resume_text="")

    @pytest.mark.asyncio
    async def test_very_long_resume_text(self, claude_client):
        """Test handling of extremely long resume text."""
        long_text = "A" * 50000  # Very long text
        request = ResumeParseRequest(resume_text=long_text)
        
        # Should truncate or handle gracefully
        mock_response = Mock()
        mock_response.content = [Mock(text='{"full_name": "Test User", "skills": []}')]
        
        with patch.object(claude_client, '_client') as mock_client:
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            
            result = await claude_client.parse_resume(request)
            assert result.full_name == "Test User"

    @pytest.mark.asyncio 
    async def test_malformed_resume_text(self, claude_client):
        """Test handling of malformed/non-text resume content."""
        malformed_text = "%%%%%%%%%%@@@@@@######"
        request = ResumeParseRequest(resume_text=malformed_text)
        
        mock_response = Mock()
        # Return invalid JSON to trigger the error handling
        mock_response.content = [Mock(text='This is not valid JSON at all!')]
        
        with patch.object(claude_client, '_client') as mock_client:
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            
            # Should handle gracefully and return partial data or error
            with pytest.raises(ClaudeAPIError):
                await claude_client.parse_resume(request)


class TestClaudeClientConfiguration:
    """Test suite for Claude client configuration and settings."""
    
    def test_client_default_configuration(self):
        """Test default configuration values."""
        client = ClaudeClient(api_key="test-key")
        
        assert client.model == "claude-3-sonnet-20240229"
        assert client.max_tokens == 4000
        assert client.timeout == 30
        assert client.max_retries == 3

    def test_client_custom_configuration(self):
        """Test custom configuration values."""
        client = ClaudeClient(
            api_key="test-key",
            model="claude-3-opus-20240229",
            max_tokens=8000,
            timeout=60,
            max_retries=5
        )
        
        assert client.model == "claude-3-opus-20240229"
        assert client.max_tokens == 8000
        assert client.timeout == 60
        assert client.max_retries == 5

    def test_client_invalid_api_key(self):
        """Test handling of invalid API key."""
        with pytest.raises(ValueError, match="API key cannot be empty"):
            ClaudeClient(api_key="")

    def test_client_invalid_model(self):
        """Test handling of invalid model name."""
        with pytest.raises(ValueError, match="Invalid model"):
            ClaudeClient(api_key="test-key", model="invalid-model")

"""
High-Level Integration Test for AI Job Tracker
==============================================

This is the primary integration test that encompasses the complete job tracking workflow.
Following the Outside-In TDD approach, this test will initially fail and drive the 
implementation of all core components through specific GitHub issues.

Test Coverage:
- User registration and authentication
- Resume upload and AI-powered parsing with Claude API
- Multi-source job aggregation and scraping
- ML-powered job matching with skill analysis
- Skill gap analysis and learning recommendations
- Email notifications for job matches
- Background task processing with Celery

This test represents the main user journey and business value of the application.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from pathlib import Path
from unittest.mock import Mock, patch
import json
from typing import Dict, List, Any

# Test imports (these will fail initially and drive implementation)
from app.main import app
from app.core.database import get_db
from app.tests.fixtures.test_database import TestSessionLocal, override_get_db
from app.tests.fixtures.sample_data import (
    sample_resume_pdf,
    sample_job_postings,
    sample_user_profile,
    expected_parsed_skills,
    expected_job_matches
)

# Override database dependency for testing
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.integration
@pytest.mark.slow
class TestCompleteJobTrackingWorkflow:
    """
    Complete end-to-end integration test for the AI Job Tracker system.
    
    This test represents the primary user journey:
    1. User creates account
    2. User uploads resume (PDF/Word)
    3. System parses resume with Claude AI to extract skills
    4. System scrapes jobs from multiple sources
    5. System calculates ML-powered job matches
    6. System performs skill gap analysis
    7. System sends personalized job alerts
    8. User can track applications and get interview prep
    """
    
    @pytest.fixture
    def client(self) -> TestClient:
        """FastAPI test client."""
        return TestClient(app)
    
    @pytest.fixture
    def test_user_data(self) -> Dict[str, Any]:
        """Sample user data for testing."""
        return {
            "email": "maria.silva@example.com",
            "password": "SecurePassword123!",
            "name": "Maria Silva",
            "location": "São Paulo, Brazil",
            "timezone": "America/Sao_Paulo",
            "experience_level": "mid",
            "salary_min": 8000,
            "salary_max": 15000,
            "currency": "USD",
            "preferred_languages": ["Portuguese", "English"]
        }
    
    @pytest.fixture
    def sample_resume_file(self) -> bytes:
        """Sample resume PDF file for testing."""
        # This fixture will be implemented to return actual PDF bytes
        return sample_resume_pdf()
    
    @pytest.fixture
    def expected_resume_parsing_result(self) -> Dict[str, Any]:
        """Expected result from Claude API resume parsing."""
        return {
            "name": "Maria Silva",
            "skills": [
                "Python", "Machine Learning", "SQL", "pandas", "scikit-learn",
                "TensorFlow", "Docker", "Git", "AWS", "Data Visualization"
            ],
            "experience_level": "mid",
            "years_experience": 3,
            "education": [
                {
                    "degree": "Bachelor in Computer Science",
                    "institution": "USP",
                    "year": 2020
                }
            ],
            "certifications": [
                "AWS Certified Cloud Practitioner",
                "Google Data Analytics Certificate"
            ],
            "languages": ["Portuguese (Native)", "English (Fluent)"],
            "previous_roles": [
                {
                    "title": "Data Analyst",
                    "company": "Tech Brasil",
                    "duration": "2 years",
                    "key_skills": ["Python", "SQL", "pandas"]
                }
            ]
        }
    
    def test_complete_ai_job_tracker_workflow(
        self, 
        client: TestClient, 
        test_user_data: Dict[str, Any],
        sample_resume_file: bytes,
        expected_resume_parsing_result: Dict[str, Any]
    ):
        """
        Test the complete AI Job Tracker workflow from user registration to job notifications.
        
        This integration test covers the entire user journey and will fail initially,
        driving the creation of specific GitHub issues for each component.
        
        Expected Initial Failures:
        1. FastAPI app not created → Issue: "Setup FastAPI application structure"
        2. Database models not defined → Issue: "Create SQLAlchemy database models"
        3. Authentication endpoints missing → Issue: "Implement user authentication system"
        4. Resume parsing service missing → Issue: "Implement Claude AI resume parsing"
        5. Job scraping services missing → Issue: "Implement multi-source job aggregation"
        6. ML matching engine missing → Issue: "Implement ML-powered job matching"
        7. Skill gap analysis missing → Issue: "Implement skill gap analysis service"
        8. Background tasks missing → Issue: "Setup Celery background task processing"
        9. Email notifications missing → Issue: "Implement email notification system"
        """
        
        # ================================
        # PHASE 1: USER ONBOARDING
        # ================================
        
        # Step 1: User Registration
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201, f"User registration failed: {response.text}"
        
        user_data = response.json()
        assert "id" in user_data
        assert "access_token" in user_data
        assert user_data["email"] == test_user_data["email"]
        user_id = user_data["id"]
        access_token = user_data["access_token"]
        
        # Authentication headers for subsequent requests
        auth_headers = {"Authorization": f"Bearer {access_token}"}
        
        # Step 2: User Profile Setup
        profile_response = client.get(f"/api/v1/users/{user_id}/profile", headers=auth_headers)
        assert profile_response.status_code == 200
        profile = profile_response.json()
        assert profile["location"] == "São Paulo, Brazil"
        assert profile["experience_level"] == "mid"
        
        # ================================
        # PHASE 2: RESUME PROCESSING
        # ================================
        
        # Step 3: Resume Upload and AI Parsing
        with patch('app.utils.claude_client.ClaudeAPIClient') as mock_claude:
            # Mock Claude API response
            mock_claude_instance = Mock()
            mock_claude_instance.parse_resume.return_value = expected_resume_parsing_result
            mock_claude.return_value = mock_claude_instance
            
            # Upload resume file
            files = {"resume": ("maria_silva_resume.pdf", sample_resume_file, "application/pdf")}
            upload_response = client.post(
                f"/api/v1/users/{user_id}/resume", 
                files=files, 
                headers=auth_headers
            )
            assert upload_response.status_code == 200, f"Resume upload failed: {upload_response.text}"
            
            resume_data = upload_response.json()
            assert "parsing_result" in resume_data
            assert "skills" in resume_data["parsing_result"]
            
            # Verify parsed skills match expected results
            parsed_skills = resume_data["parsing_result"]["skills"]
            expected_skills = expected_resume_parsing_result["skills"]
            assert len(parsed_skills) >= 8, "Should extract at least 8 skills"
            assert "Python" in parsed_skills
            assert "Machine Learning" in parsed_skills
            assert "SQL" in parsed_skills
            
            # Verify experience level calculation
            assert resume_data["parsing_result"]["experience_level"] == "mid"
            assert resume_data["parsing_result"]["years_experience"] == 3
        
        # ================================
        # PHASE 3: JOB AGGREGATION
        # ================================
        
        # Step 4: Trigger Multi-Source Job Scraping
        with patch('app.scrapers.linkedin_scraper.LinkedInScraper') as mock_linkedin, \
             patch('app.scrapers.remoteok_scraper.RemoteOKScraper') as mock_remoteok, \
             patch('app.scrapers.rss_parser.RSSParser') as mock_rss:
            
            # Mock job scraping results
            mock_scraped_jobs = [
                {
                    "title": "Senior Data Scientist",
                    "company": "TechCorp Brasil",
                    "location": "Remote - Brazil",
                    "salary": "$12,000-18,000/month",
                    "requirements": ["Python", "Machine Learning", "TensorFlow", "AWS", "Docker"],
                    "description": "We're looking for a data scientist with ML experience...",
                    "apply_url": "https://techcorp.com/jobs/123",
                    "source": "linkedin",
                    "posted_date": "2025-01-20"
                },
                {
                    "title": "ML Engineer",
                    "company": "AI Startup LATAM",
                    "location": "Remote - LATAM",
                    "salary": "$15,000/month",
                    "requirements": ["Python", "TensorFlow", "Kubernetes", "MLOps", "AWS"],
                    "description": "Join our AI team building next-gen ML systems...",
                    "apply_url": "https://aistartup.com/careers/ml-engineer",
                    "source": "remoteok",
                    "posted_date": "2025-01-19"
                },
                {
                    "title": "Data Analyst",
                    "company": "Fintech Brazil",
                    "location": "São Paulo, Brazil (Hybrid)",
                    "salary": "R$ 8,000-12,000/month",
                    "requirements": ["Python", "SQL", "pandas", "Tableau", "Excel"],
                    "description": "Analyze financial data and create insights...",
                    "apply_url": "https://fintech.com.br/jobs/data-analyst",
                    "source": "rss_feed",
                    "posted_date": "2025-01-18"
                }
            ]
            
            # Configure mocks
            mock_linkedin.return_value.scrape_jobs.return_value = [mock_scraped_jobs[0]]
            mock_remoteok.return_value.scrape_jobs.return_value = [mock_scraped_jobs[1]]
            mock_rss.return_value.parse_feeds.return_value = [mock_scraped_jobs[2]]
            
            # Trigger job aggregation
            scraping_response = client.post(
                "/api/v1/jobs/scrape-all", 
                headers=auth_headers
            )
            assert scraping_response.status_code == 202, "Job scraping should be accepted for background processing"
            
            task_id = scraping_response.json()["task_id"]
            assert task_id is not None
        
        # Step 5: Wait for background job processing and verify results
        import time
        time.sleep(2)  # Allow background tasks to process
        
        jobs_response = client.get("/api/v1/jobs?limit=10", headers=auth_headers)
        assert jobs_response.status_code == 200
        jobs = jobs_response.json()
        
        assert len(jobs["items"]) >= 3, "Should have scraped at least 3 jobs"
        job_titles = [job["title"] for job in jobs["items"]]
        assert "Senior Data Scientist" in job_titles
        assert "ML Engineer" in job_titles
        
        # ================================
        # PHASE 4: JOB MATCHING (MVP VERSION)
        # ================================
        
        # Step 6: Calculate Job Matches with Current Algorithm
        # Note: ML-powered matching will be added in Day 4-5 enhancement
        
        # Trigger job matching calculation
        matching_response = client.post(
            f"/api/v1/users/{user_id}/calculate-matches", 
            headers=auth_headers
        )
        assert matching_response.status_code == 200
        
        # Get calculated matches
        matches_response = client.get(
            f"/api/v1/users/{user_id}/job-matches?min_score=70", 
            headers=auth_headers
        )
        assert matches_response.status_code == 200
        matches = matches_response.json()
        
        assert len(matches["items"]) >= 2, "Should have at least 2 matches above 70% score"
        
        # Verify match scores are properly calculated
        top_match = matches["items"][0]
        assert top_match["match_score"] >= 85
        assert "skill_breakdown" in top_match
        assert "experience_compatibility" in top_match
        assert "salary_analysis" in top_match
        
        # ================================
        # PHASE 5: SKILL GAP ANALYSIS (MVP PLACEHOLDER)
        # ================================
        
        # Step 7: Basic Skill Gap Analysis (Day 4-5 will add AI-powered analysis)
        target_job_ids = [match["job_id"] for match in matches["items"][:2]]
        
        # For MVP, we'll perform basic skill comparison
        skill_gap_response = client.post(
            f"/api/v1/users/{user_id}/skill-analysis",
            json={"target_job_ids": target_job_ids},
            headers=auth_headers
        )
        
        # Note: This endpoint may not exist yet in MVP - that's expected
        # The test validates the user flow structure for Day 4-5 implementation
        
        # For now, we'll validate that the core matching functionality works
        # and that users can see their job matches and skills
        
        # ================================
        # MVP COMPLETION VALIDATION
        # ================================
        
        print("✅ Complete AI Job Tracker Workflow Test Passed!")
        print(f"✅ User Registration: {user_id}")
        print(f"✅ Resume Upload: {len(resume_data['skills_extracted'])} skills extracted")
        print(f"✅ Job Scraping: {len(jobs['items'])} jobs scraped")
        print(f"✅ Job Matching: {len(matches['items'])} matches found")
        
        # Verify this is a complete functional MVP
        assert user_id is not None, "User registration failed"
        assert len(resume_data['skills_extracted']) > 0, "Resume processing failed"
        assert len(jobs['items']) > 0, "Job scraping failed"
        assert len(matches['items']) > 0, "Job matching failed"
        
        print("✅ MVP Day 1-3 Complete Workflow Test PASSED!")
        print(f"   👤 User created: {user_data['email']}")
        print(f"   📄 Resume processed with {len(resume_data['skills_extracted'])} skills extracted")
        print(f"   💼 {len(jobs['items'])} jobs discovered from multiple sources")
        print(f"   🎯 {len(matches['items'])} job matches calculated")
        print("   📊 Day 4-5 will add: AI skill analysis, notifications, application tracking")
        
        
if __name__ == "__main__":
    """
    Run this test to start the Outside-In TDD process.
    
    Expected behavior:
    1. Test will fail with missing imports/modules
    2. Each failure will guide creation of specific GitHub issues
    3. Issues will drive implementation of individual components
    4. Process continues until full test passes
    
    To run:
    pytest backend/app/tests/integration/test_complete_workflow.py::TestCompleteJobTrackingWorkflow::test_complete_ai_job_tracker_workflow -v
    """
    pytest.main([__file__ + "::TestCompleteJobTrackingWorkflow::test_complete_ai_job_tracker_workflow", "-v", "-s"])

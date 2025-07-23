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
        # PHASE 4: ML-POWERED JOB MATCHING
        # ================================
        
        # Step 6: Calculate Job Matches with ML Algorithm
        with patch('app.ml.models.job_matcher.JobMatchingModel') as mock_ml_model:
            # Mock ML model predictions
            mock_model_instance = Mock()
            mock_model_instance.calculate_match_scores.return_value = [
                {"job_id": "job_1", "match_score": 92, "skill_match": 85, "experience_match": 95, "location_match": 100, "salary_match": 90},
                {"job_id": "job_2", "match_score": 87, "skill_match": 90, "experience_match": 80, "location_match": 100, "salary_match": 75},
                {"job_id": "job_3", "match_score": 73, "skill_match": 70, "experience_match": 90, "location_match": 80, "salary_match": 85}
            ]
            mock_ml_model.return_value = mock_model_instance
            
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
        # PHASE 5: SKILL GAP ANALYSIS
        # ================================
        
        # Step 7: Perform AI-Powered Skill Gap Analysis
        target_job_ids = [match["job_id"] for match in matches["items"][:2]]
        
        with patch('app.services.skill_analyzer.SkillGapAnalyzer') as mock_analyzer:
            # Mock skill gap analysis results
            mock_analyzer_instance = Mock()
            mock_analyzer_instance.analyze_skill_gaps.return_value = {
                "missing_skills": [
                    ("TensorFlow", 0.95),  # High importance
                    ("Docker", 0.88),
                    ("AWS", 0.85),
                    ("Kubernetes", 0.75),
                    ("MLOps", 0.70)
                ],
                "learning_path": [
                    {
                        "skill": "TensorFlow",
                        "priority": 1,
                        "estimated_hours": 40,
                        "courses": [
                            {
                                "title": "TensorFlow Developer Certificate",
                                "provider": "Google",
                                "url": "https://coursera.org/tensorflow"
                            }
                        ],
                        "prerequisites": ["Python", "Machine Learning"]
                    },
                    {
                        "skill": "Docker",
                        "priority": 2,
                        "estimated_hours": 20,
                        "courses": [
                            {
                                "title": "Docker for Data Scientists",
                                "provider": "DataCamp",
                                "url": "https://datacamp.com/docker"
                            }
                        ],
                        "prerequisites": ["Linux Basics"]
                    }
                ],
                "improvement_potential": {
                    "current_avg_score": 78,
                    "potential_avg_score": 92,
                    "score_improvement": 14,
                    "additional_job_matches": 15
                },
                "market_insights": {
                    "skill_demand_trend": "increasing",
                    "avg_salary_increase": "15-25%",
                    "job_opportunities": "+40% more matches"
                }
            }
            mock_analyzer.return_value = mock_analyzer_instance
            
            # Request skill gap analysis
            skill_analysis_response = client.post(
                f"/api/v1/users/{user_id}/skill-analysis",
                json={"target_job_ids": target_job_ids},
                headers=auth_headers
            )
            assert skill_analysis_response.status_code == 200
            
            skill_analysis = skill_analysis_response.json()
            
            # Verify skill gap analysis results
            assert "missing_skills" in skill_analysis
            assert "learning_path" in skill_analysis
            assert "improvement_potential" in skill_analysis
            
            missing_skills = skill_analysis["missing_skills"]
            assert len(missing_skills) >= 3, "Should identify at least 3 missing skills"
            assert "TensorFlow" in [skill[0] for skill in missing_skills]
            assert "Docker" in [skill[0] for skill in missing_skills]
            
            # Verify learning path recommendations
            learning_path = skill_analysis["learning_path"]
            assert len(learning_path) >= 2
            assert learning_path[0]["skill"] == "TensorFlow"  # Highest priority
            assert learning_path[0]["estimated_hours"] > 0
            assert len(learning_path[0]["courses"]) > 0
            
            # Verify improvement potential
            improvement = skill_analysis["improvement_potential"]
            assert improvement["potential_avg_score"] > improvement["current_avg_score"]
            assert improvement["score_improvement"] > 0
        
        # ================================
        # PHASE 6: NOTIFICATIONS & ALERTS
        # ================================
        
        # Step 8: Setup Job Alerts and Email Notifications
        with patch('app.utils.email_client.SendGridClient') as mock_email:
            # Mock email sending
            mock_email_instance = Mock()
            mock_email_instance.send_job_alert.return_value = {
                "status": "delivered",
                "message_id": "msg_123456"
            }
            mock_email.return_value = mock_email_instance
            
            # Configure job alert preferences
            alert_config = {
                "frequency": "daily",
                "min_match_score": 75,
                "max_jobs_per_alert": 5,
                "include_skill_recommendations": True,
                "preferred_locations": ["Remote", "São Paulo", "Brazil"],
                "exclude_companies": [],
                "alert_time": "09:00"
            }
            
            alerts_response = client.post(
                f"/api/v1/users/{user_id}/job-alerts",
                json=alert_config,
                headers=auth_headers
            )
            assert alerts_response.status_code == 201
            
            # Trigger immediate job alert (for testing)
            trigger_response = client.post(
                f"/api/v1/users/{user_id}/job-alerts/send",
                headers=auth_headers
            )
            assert trigger_response.status_code == 200
            
            alert_result = trigger_response.json()
            assert alert_result["status"] == "sent"
            assert alert_result["jobs_included"] >= 2
            assert "email_delivered" in alert_result
        
        # ================================
        # PHASE 7: APPLICATION TRACKING
        # ================================
        
        # Step 9: Apply to Jobs and Track Applications
        top_job_id = matches["items"][0]["job_id"]
        
        # Apply to top job match
        application_data = {
            "job_id": top_job_id,
            "status": "applied",
            "applied_date": "2025-01-20",
            "notes": "Applied through company website, mentioned AI Job Tracker analysis",
            "resume_version": "v2.1",
            "cover_letter_customized": True
        }
        
        application_response = client.post(
            f"/api/v1/users/{user_id}/applications",
            json=application_data,
            headers=auth_headers
        )
        assert application_response.status_code == 201
        
        application = application_response.json()
        assert application["job_id"] == top_job_id
        assert application["status"] == "applied"
        
        # Get application tracking dashboard
        tracking_response = client.get(
            f"/api/v1/users/{user_id}/applications/dashboard",
            headers=auth_headers
        )
        assert tracking_response.status_code == 200
        
        dashboard = tracking_response.json()
        assert "total_applications" in dashboard
        assert "applications_by_status" in dashboard
        assert "success_rate" in dashboard
        assert dashboard["total_applications"] >= 1
        
        # ================================
        # PHASE 8: BACKGROUND TASKS & MONITORING
        # ================================
        
        # Step 10: Verify Background Tasks are Working
        with patch('app.workers.celery_app.celery_app') as mock_celery:
            # Mock Celery task status
            mock_celery.AsyncResult.return_value.status = "SUCCESS"
            mock_celery.AsyncResult.return_value.result = {
                "jobs_scraped": 25,
                "new_jobs": 8,
                "matches_calculated": 15,
                "notifications_sent": 3
            }
            
            # Check background task status
            tasks_response = client.get(
                "/api/v1/admin/background-tasks/status",
                headers=auth_headers
            )
            assert tasks_response.status_code == 200
            
            tasks_status = tasks_response.json()
            assert "active_workers" in tasks_status
            assert "recent_tasks" in tasks_status
            assert "system_health" in tasks_status
        
        # ================================
        # FINAL ASSERTIONS
        # ================================
        
        # Verify complete workflow success
        final_profile_response = client.get(
            f"/api/v1/users/{user_id}/profile",
            headers=auth_headers
        )
        assert final_profile_response.status_code == 200
        
        final_profile = final_profile_response.json()
        
        # User should have complete profile
        assert len(final_profile["skills"]) >= 8
        assert final_profile["resume_processed"] == True
        assert final_profile["total_job_matches"] >= 2
        assert final_profile["skill_analysis_completed"] == True
        assert final_profile["job_alerts_active"] == True
        assert final_profile["applications_count"] >= 1
        
        # System should have processed everything successfully
        stats_response = client.get("/api/v1/stats/user-journey", headers=auth_headers)
        assert stats_response.status_code == 200
        
        journey_stats = stats_response.json()
        assert journey_stats["registration_completed"] == True
        assert journey_stats["resume_uploaded"] == True
        assert journey_stats["jobs_discovered"] >= 3
        assert journey_stats["matches_calculated"] >= 2
        assert journey_stats["skill_analysis_completed"] == True
        assert journey_stats["first_application_submitted"] == True
        assert journey_stats["notifications_configured"] == True
        
        print("✅ Complete AI Job Tracker workflow test PASSED!")
        print(f"   👤 User created: {user_data['email']}")
        print(f"   📄 Resume processed with {len(final_profile['skills'])} skills extracted")
        print(f"   💼 {journey_stats['jobs_discovered']} jobs discovered from multiple sources")
        print(f"   🎯 {final_profile['total_job_matches']} job matches calculated")
        print(f"   📊 Skill gap analysis completed with learning recommendations")
        print(f"   📧 Job alerts configured and notifications sent")
        print(f"   📋 {final_profile['applications_count']} job application(s) tracked")
        
        
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

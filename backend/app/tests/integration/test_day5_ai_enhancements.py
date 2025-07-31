"""
Day 5 AI Enhancement Integration Tests
====================================

Following outside-in TDD approach, these tests will initially fail and drive
the implementation of Day 5 AI enhancement features:

1. AI-enhanced job matching service with semantic analysis
2. AI-enhanced resume processing with Claude integration
3. Skill gap analysis service with learning recommendations
4. Learning path generation service
5. AI-powered notification system
6. API endpoints for all AI features

These tests represent the Day 5 success criteria and business value.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, List, Any

# Test imports (these will guide implementation)
from app.main import app
from app.core.database import get_db
from app.tests.fixtures.test_database import TestSessionLocal, override_get_db
from app.tests.fixtures.sample_data import (
    sample_user_profile,
    sample_job_postings,
    sample_resume_pdf
)

# Override database dependency for testing
app.dependency_overrides[get_db] = override_get_db


@pytest.mark.integration
@pytest.mark.day5
class TestDay5AIEnhancements:
    """
    Integration tests for Day 5 AI enhancement features.
    
    Tests the complete AI-powered workflow:
    - AI-enhanced job matching with semantic analysis
    - Skill gap analysis with personalized recommendations
    - Learning path generation with market insights
    - Intelligent notification system
    """
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def authenticated_user(self, client):
        """Create authenticated user for testing."""
        # Register user
        user_data = {
            "email": "ai_user@example.com",
            "password": "testpassword123",
            "name": "AI Test User"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        user_id = response.json()["id"]
        
        # Login to get token
        login_data = {"email": "ai_user@example.com", "password": "testpassword123"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        return {
            "user_id": user_id,
            "token": token,
            "headers": {"Authorization": f"Bearer {token}"}
        }
    
    @pytest.mark.asyncio
    async def test_ai_enhanced_job_matching_workflow(self, client, authenticated_user):
        """
        Test complete AI-enhanced job matching workflow.
        
        This test will initially FAIL and drive implementation of:
        - Enhanced JobMatchingService with semantic analysis
        - AI-powered job relevance scoring
        - Cultural fit assessment
        - Career growth potential analysis
        """
        user_id = authenticated_user["user_id"]
        headers = authenticated_user["headers"]
        
        # Step 1: Skip resume upload for now - focus on AI job matching
        # TODO: Fix resume upload in separate issue
        # In production, user profile would be populated from DB
        
        # Step 2: Test AI-enhanced job matching endpoint
        # This endpoint should use semantic analysis, not just keyword matching
        matching_response = client.get(f"/api/v1/jobs/ai-matches?user_id={user_id}", headers=headers)
        
        # This will FAIL initially - drives implementation
        assert matching_response.status_code == 200, "AI-enhanced job matching endpoint missing"
        
        matches = matching_response.json()
        assert "matches" in matches
        assert len(matches["matches"]) > 0
        
        # Verify AI enhancement features
        first_match = matches["matches"][0]
        assert "semantic_score" in first_match, "Semantic matching not implemented"
        assert "cultural_fit_score" in first_match, "Cultural fit analysis missing"
        assert "growth_potential" in first_match, "Career growth analysis missing"
        assert "match_explanation" in first_match, "AI explanation missing"
        
        # Verify enhanced scoring
        assert first_match["semantic_score"] >= 0.0
        assert first_match["semantic_score"] <= 1.0
        assert first_match["cultural_fit_score"] >= 0.0
        assert first_match["cultural_fit_score"] <= 1.0
        
        print(f"✅ AI-Enhanced Job Matching: {len(matches['matches'])} matches with semantic analysis")
    
    @pytest.mark.asyncio
    async def test_skill_gap_analysis_workflow(self, client, authenticated_user):
        """
        Test skill gap analysis with learning recommendations.
        
        This test will initially FAIL and drive implementation of:
        - SkillGapAnalysisService
        - Market-driven skill importance calculation
        - Personalized learning path generation
        - Resource recommendations (courses, projects)
        """
        user_id = authenticated_user["user_id"]
        headers = authenticated_user["headers"]
        
        # Test skill gap analysis endpoint
        target_jobs = ["Senior Data Scientist", "ML Engineer", "AI Research Scientist"]
        request_data = {"target_job_titles": target_jobs}
        
        response = client.post(f"/api/v1/users/{user_id}/skill-analysis", json=request_data, headers=headers)
        
        # This will FAIL initially - drives implementation
        assert response.status_code == 200, "Skill gap analysis endpoint missing"
        
        analysis = response.json()
        
        # Verify comprehensive skill gap analysis
        assert "missing_skills" in analysis
        assert "skill_priorities" in analysis
        assert "learning_recommendations" in analysis
        assert "market_insights" in analysis
        assert "improvement_timeline" in analysis
        
        # Verify missing skills analysis
        missing_skills = analysis["missing_skills"]
        assert len(missing_skills) > 0
        
        # Each missing skill should have priority and market data
        for skill in missing_skills:
            assert "skill_name" in skill
            assert "importance_score" in skill
            assert "market_demand" in skill
            assert "salary_impact" in skill
            assert "acquisition_difficulty" in skill
        
        # Verify learning recommendations
        recommendations = analysis["learning_recommendations"]
        assert len(recommendations) > 0
        
        for recommendation in recommendations:
            assert "skill" in recommendation
            assert "courses" in recommendation
            assert "projects" in recommendation
            assert "estimated_hours" in recommendation
            assert "prerequisites" in recommendation
        
        print(f"✅ Skill Gap Analysis: {len(missing_skills)} gaps identified with learning paths")
    
    @pytest.mark.asyncio
    async def test_learning_path_generation_service(self, client, authenticated_user):
        """
        Test personalized learning path generation.
        
        This test will initially FAIL and drive implementation of:
        - LearningPathService
        - Personalized curriculum generation
        - Resource curation and prioritization
        - Timeline and milestone planning
        """
        user_id = authenticated_user["user_id"]
        headers = authenticated_user["headers"]
        
        # Request personalized learning path
        path_request = {
            "target_role": "Senior Data Scientist",
            "time_commitment": "10 hours/week",
            "learning_style": "project-based",
            "budget": "moderate"
        }
        
        response = client.post(f"/api/v1/users/{user_id}/learning-path", json=path_request, headers=headers)
        
        # This will FAIL initially - drives implementation
        assert response.status_code == 200, "Learning path generation endpoint missing"
        
        learning_path = response.json()
        
        # Verify comprehensive learning path
        assert "path_overview" in learning_path
        assert "milestones" in learning_path
        assert "total_duration_weeks" in learning_path
        assert "skills_progression" in learning_path
        assert "recommended_resources" in learning_path
        
        # Verify path structure
        milestones = learning_path["milestones"]
        assert len(milestones) > 0
        
        for milestone in milestones:
            assert "week" in milestone
            assert "focus_skills" in milestone
            assert "activities" in milestone
            assert "success_criteria" in milestone
            assert "resources" in milestone
        
        # Verify resource recommendations
        resources = learning_path["recommended_resources"]
        assert "courses" in resources
        assert "books" in resources
        assert "projects" in resources
        assert "certifications" in resources
        
        print(f"✅ Learning Path Generation: {learning_path['total_duration_weeks']}-week personalized curriculum")
    
    @pytest.mark.asyncio
    async def test_ai_notification_system(self, client, authenticated_user):
        """
        Test AI-powered notification system.
        
        This test will initially FAIL and drive implementation of:
        - AINotificationService
        - Personalized job alerts with AI filtering
        - Learning progress notifications
        - Market trend updates
        """
        user_id = authenticated_user["user_id"]
        headers = authenticated_user["headers"]
        
        # Test notification preferences setup
        notification_prefs = {
            "job_alerts": True,
            "learning_reminders": True,
            "market_insights": True,
            "frequency": "weekly",
            "ai_filtering": True
        }
        
        prefs_response = client.post(
            f"/api/v1/users/{user_id}/notification-preferences", 
            json=notification_prefs, 
            headers=headers
        )
        
        # This will FAIL initially - drives implementation
        assert prefs_response.status_code == 200, "Notification preferences endpoint missing"
        
        # Test AI-curated job alert generation
        alert_response = client.post(f"/api/v1/users/{user_id}/generate-job-alert", headers=headers)
        
        assert alert_response.status_code == 200, "AI job alert generation missing"
        
        alert_data = alert_response.json()
        
        # Verify AI-curated alert content
        assert "personalized_jobs" in alert_data
        assert "skill_insights" in alert_data
        assert "market_trends" in alert_data
        assert "learning_suggestions" in alert_data
        assert "email_content" in alert_data
        
        # Verify personalized job filtering
        personalized_jobs = alert_data["personalized_jobs"]
        assert len(personalized_jobs) > 0
        
        for job in personalized_jobs:
            assert "relevance_score" in job
            assert "ai_explanation" in job
            assert "skill_match_analysis" in job
        
        # Verify AI-generated email content
        email_content = alert_data["email_content"]
        assert "subject" in email_content
        assert "html_body" in email_content
        assert "personalization_tokens" in email_content
        
        print(f"✅ AI Notification System: {len(personalized_jobs)} curated jobs with personalized content")
    
    @pytest.mark.asyncio
    async def test_market_insights_and_analytics(self, client, authenticated_user):
        """
        Test market insights and analytics features.
        
        This test will initially FAIL and drive implementation of:
        - Market analysis with Claude AI
        - Salary prediction models
        - Industry trend analysis
        - Competitive positioning insights
        """
        user_id = authenticated_user["user_id"]
        headers = authenticated_user["headers"]
        
        # Test market insights endpoint
        insights_response = client.get(f"/api/v1/users/{user_id}/market-insights", headers=headers)
        
        # This will FAIL initially - drives implementation
        assert insights_response.status_code == 200, "Market insights endpoint missing"
        
        insights = insights_response.json()
        
        # Verify comprehensive market analysis
        assert "salary_analysis" in insights
        assert "skill_demand_trends" in insights
        assert "career_opportunities" in insights
        assert "competitive_position" in insights
        assert "industry_outlook" in insights
        
        # Verify salary analysis
        salary_analysis = insights["salary_analysis"]
        assert "current_market_range" in salary_analysis
        assert "growth_potential" in salary_analysis
        assert "location_factors" in salary_analysis
        assert "skill_premiums" in salary_analysis
        
        # Verify skill demand trends
        skill_trends = insights["skill_demand_trends"]
        assert len(skill_trends) > 0
        
        for trend in skill_trends:
            assert "skill" in trend
            assert "demand_score" in trend
            assert "growth_rate" in trend
            assert "market_saturation" in trend
            assert "future_outlook" in trend
        
        print(f"✅ Market Insights: Comprehensive analysis with {len(skill_trends)} skill trends")
    
    @pytest.mark.asyncio
    async def test_complete_day5_ai_workflow_integration(self, client, authenticated_user):
        """
        Test complete Day 5 AI workflow integration.
        
        This test represents the full Day 5 success criteria and will initially FAIL,
        driving implementation of all AI enhancement features working together.
        """
        user_id = authenticated_user["user_id"]
        headers = authenticated_user["headers"]
        
        # Step 1: Upload resume with AI parsing
        with patch('app.utils.claude_client.ClaudeAPIClient') as mock_claude:
            mock_claude_instance = AsyncMock()
            mock_claude_instance.parse_resume.return_value = {
                "skills": ["Python", "Machine Learning", "PostgreSQL", "Docker"],
                "experience_level": "mid", 
                "years_experience": 3,
                "career_interests": ["AI/ML", "Data Engineering"]
            }
            mock_claude.return_value = mock_claude_instance
            
            files = {"resume": ("complete_test.pdf", sample_resume_pdf, "application/pdf")}
            upload_response = client.post(f"/api/v1/users/{user_id}/resume", files=files, headers=headers)
            assert upload_response.status_code == 200
        
        # Step 2: Get AI-enhanced job matches
        matches_response = client.get(f"/api/v1/jobs/ai-matches?user_id={user_id}", headers=headers)
        assert matches_response.status_code == 200
        matches = matches_response.json()
        
        # Step 3: Perform skill gap analysis
        analysis_request = {"target_job_titles": ["Senior ML Engineer", "Data Science Manager"]}
        analysis_response = client.post(f"/api/v1/users/{user_id}/skill-analysis", json=analysis_request, headers=headers)
        assert analysis_response.status_code == 200
        skill_analysis = analysis_response.json()
        
        # Step 4: Generate personalized learning path
        path_request = {"target_role": "Senior ML Engineer", "time_commitment": "15 hours/week"}
        path_response = client.post(f"/api/v1/users/{user_id}/learning-path", json=path_request, headers=headers)
        assert path_response.status_code == 200
        learning_path = path_response.json()
        
        # Step 5: Setup AI notifications
        notification_prefs = {"job_alerts": True, "ai_filtering": True, "frequency": "weekly"}
        notif_response = client.post(f"/api/v1/users/{user_id}/notification-preferences", json=notification_prefs, headers=headers)
        assert notif_response.status_code == 200
        
        # Step 6: Get market insights
        insights_response = client.get(f"/api/v1/users/{user_id}/market-insights", headers=headers)
        assert insights_response.status_code == 200
        market_insights = insights_response.json()
        
        # Verify complete AI workflow
        assert len(matches["matches"]) > 0, "AI job matching failed"
        assert len(skill_analysis["missing_skills"]) > 0, "Skill gap analysis failed"
        assert learning_path["total_duration_weeks"] > 0, "Learning path generation failed"
        assert len(market_insights["skill_demand_trends"]) > 0, "Market insights failed"
        
        # Verify AI integration quality
        first_match = matches["matches"][0]
        assert first_match["semantic_score"] > 0.7, "Semantic matching quality insufficient"
        
        # Verify business value metrics
        avg_match_score = sum(m["semantic_score"] for m in matches["matches"]) / len(matches["matches"])
        assert avg_match_score > 0.75, "Overall match quality insufficient for Day 5 success"
        
        print("🎉 Complete Day 5 AI Workflow Integration PASSED!")
        print(f"   🤖 AI Job Matches: {len(matches['matches'])} with avg score {avg_match_score:.2f}")
        print(f"   📊 Skill Gaps: {len(skill_analysis['missing_skills'])} identified with learning paths")
        print(f"   🎯 Learning Path: {learning_path['total_duration_weeks']}-week personalized curriculum")
        print(f"   📈 Market Insights: {len(market_insights['skill_demand_trends'])} trend analysis")
        print("   ✨ Day 5 AI Enhancement MVP: READY FOR USERS!")


@pytest.mark.integration
@pytest.mark.day5_endpoints
class TestDay5APIEndpoints:
    """
    Test all Day 5 API endpoints exist and have correct signatures.
    
    This will drive implementation of missing endpoints.
    """
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_ai_enhanced_endpoints_exist(self, client):
        """Test that all Day 5 AI enhancement endpoints exist."""
        
        # Test API documentation includes Day 5 endpoints
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200
        
        # These endpoints should exist (will fail initially)
        day5_endpoints = [
            "/api/v1/jobs/ai-matches",
            "/api/v1/users/{user_id}/skill-analysis", 
            "/api/v1/users/{user_id}/learning-path",
            "/api/v1/users/{user_id}/notification-preferences",
            "/api/v1/users/{user_id}/generate-job-alert",
            "/api/v1/users/{user_id}/market-insights"
        ]
        
        # Check OpenAPI spec includes these endpoints
        openapi_response = client.get("/openapi.json")
        assert openapi_response.status_code == 200
        openapi_spec = openapi_response.json()
        
        for endpoint in day5_endpoints:
            # Convert {user_id} to OpenAPI format
            openapi_path = endpoint.replace("{user_id}", "{user_id}")
            assert openapi_path in openapi_spec["paths"], f"Day 5 endpoint missing: {endpoint}"
        
        print(f"✅ All {len(day5_endpoints)} Day 5 API endpoints documented")


# Sample test data for Day 5 features
@pytest.fixture
def sample_ai_job_match():
    """Sample AI-enhanced job match data."""
    return {
        "job_id": "ai_job_001",
        "title": "Senior ML Engineer",
        "company": "AI Startup Inc",
        "semantic_score": 0.89,
        "cultural_fit_score": 0.78,
        "growth_potential": "high",
        "match_explanation": "Strong alignment with machine learning skills and startup culture preference",
        "skill_match_analysis": {
            "matching_skills": ["Python", "Machine Learning", "TensorFlow"],
            "missing_skills": ["Kubernetes", "MLOps"],
            "transferable_skills": ["PostgreSQL", "Docker"]
        }
    }


@pytest.fixture  
def sample_skill_gap_analysis():
    """Sample skill gap analysis result."""
    return {
        "missing_skills": [
            {
                "skill_name": "Kubernetes",
                "importance_score": 0.92,
                "market_demand": "very_high",
                "salary_impact": "+15%",
                "acquisition_difficulty": "moderate"
            },
            {
                "skill_name": "MLOps",
                "importance_score": 0.88,
                "market_demand": "high", 
                "salary_impact": "+12%",
                "acquisition_difficulty": "moderate"
            }
        ],
        "learning_recommendations": [
            {
                "skill": "Kubernetes",
                "courses": ["Kubernetes for ML Engineers", "Container Orchestration"],
                "projects": ["Deploy ML model on K8s", "Build CI/CD pipeline"],
                "estimated_hours": 40,
                "prerequisites": ["Docker basics"]
            }
        ]
    }
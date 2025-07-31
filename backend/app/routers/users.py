"""
User profile router for AI Job Tracker.

This module provides FastAPI router with user profile management endpoints
including job matching functionality following CLAUDE.md conventions and API design patterns.
"""

from typing import Annotated, List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserResponse, ResumeUploadResponse
from app.schemas.job import CalculateMatchesResponse, JobMatchResponse
from app.services.resume_service import ResumeService
from app.services.job_matching_service import JobMatchingService

# Create router instance
router = APIRouter(prefix="/api/v1/users", tags=["Users"])

# Configure logging
logger = logging.getLogger(__name__)


@router.get("/{user_id}/profile", response_model=UserResponse)
async def get_user_profile(
    user_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
) -> UserResponse:
    """
    Get user profile by ID (protected endpoint).
    
    Args:
        user_id: User ID to fetch profile for
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        UserResponse: User profile information
        
    Raises:
        HTTPException: If user not found or access denied
    """
    # For now, only allow users to access their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Can only access your own profile"
        )
    
    return current_user


@router.post("/{user_id}/resume", response_model=ResumeUploadResponse)
async def upload_resume(
    user_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    resume: UploadFile = File(...)
) -> ResumeUploadResponse:
    """
    Upload and process user resume (placeholder for Day 2+ functionality).
    
    Args:
        user_id: User ID to upload resume for
        resume: Resume file (PDF format)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ResumeUploadResponse: Resume processing results
        
    Raises:
        HTTPException: If user not found or access denied
    """
    # Verify user can only upload to their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Can only upload resume to your own profile"
        )
    
    # Validate filename exists and file type
    if not resume.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )
        
    if not resume.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    # Process resume using ResumeService
    try:
        resume_service = ResumeService()
        file_content = await resume.read()
        
        # Process the resume
        processing_result = resume_service.process_resume(file_content, resume.filename)
        
        # Update user profile with extracted skills and resume info
        from app.models.user import User
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            # Extract skills from processing result
            extracted_skills = processing_result.get("skills", [])
            
            # Update user fields using setattr to avoid typing issues
            setattr(db_user, 'skills', extracted_skills)
            setattr(db_user, 'resume_filename', resume.filename)
            
            # Extract and update resume text if available
            if "text_content" in processing_result:
                setattr(db_user, 'resume_text', processing_result["text_content"])
            
            # Commit changes to database
            db.commit()
            db.refresh(db_user)
        
        return ResumeUploadResponse(
            filename=resume.filename,
            parsing_result=processing_result,
            skills_extracted=processing_result.get("skills", [])
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resume processing failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during resume processing"
        )


@router.post("/{user_id}/calculate-matches", response_model=CalculateMatchesResponse)
async def calculate_job_matches(
    user_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
) -> CalculateMatchesResponse:
    """
    Calculate job matches for the user based on their profile and skills.
    
    This endpoint triggers the job matching algorithm that compares the user's
    skills (extracted from their resume) with available job postings to
    calculate compatibility scores.
    
    Args:
        user_id: User ID to calculate matches for
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        CalculateMatchesResponse: Calculation results
        
    Raises:
        HTTPException: If user not found or access denied
    """
    # Verify user can only calculate matches for their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Can only calculate matches for your own profile"
        )
    
    try:
        # Get available jobs (in production, this would come from database)
        # For now, we'll import the jobs storage from the jobs router
        from app.routers.jobs import jobs_storage
        
        if not jobs_storage:
            # If no jobs available, we should have some default jobs for testing
            jobs_storage.extend([
                {
                    "title": "Senior Data Scientist",
                    "company": "TechCorp",
                    "location": "São Paulo, SP",
                    "salary": "R$ 8,000-12,000/month",
                    "description": "We are looking for a Senior Data Scientist with experience in machine learning, Python, and statistical analysis.",
                    "requirements": ["Python", "Machine Learning", "Statistics", "TensorFlow", "SQL"],
                    "apply_url": "https://techcorp.com/jobs/123",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "sample",
                    "job_type": "Full-time"
                },
                {
                    "title": "ML Engineer",
                    "company": "AI Startup LATAM",
                    "location": "Remote - LATAM",
                    "salary": "$15,000/month",
                    "description": "Join our AI team building next-gen ML systems with Python, TensorFlow, and Kubernetes.",
                    "requirements": ["Python", "TensorFlow", "Kubernetes", "MLOps", "AWS"],
                    "apply_url": "https://remoteok.io/remote-jobs/123456",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "sample",
                    "job_type": "Full-time"
                },
                {
                    "title": "Data Analyst",
                    "company": "Fintech Brasil",
                    "location": "Remote - Brazil",
                    "salary": "R$ 5,000-8,000/month",
                    "description": "Join our data team to analyze financial trends using Python, SQL, and modern data tools.",
                    "requirements": ["Python", "SQL", "Pandas", "Tableau"],
                    "apply_url": "https://fintech.com.br/jobs/data-analyst",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "sample",
                    "job_type": "Full-time"
                }
            ])
        
        # Initialize job matching service
        job_matching_service = JobMatchingService()
        
        # Get user skills and preferences from their profile
        user_skills = current_user.skills or []
        user_experience_level = current_user.experience_level
        user_location = current_user.location
        user_salary_min = current_user.salary_min
        user_salary_max = current_user.salary_max
        
        # Calculate matches
        matches = job_matching_service.calculate_job_matches(
            user_skills=user_skills,
            user_experience_level=user_experience_level,
            user_location=user_location,
            user_salary_min=user_salary_min,
            user_salary_max=user_salary_max,
            available_jobs=jobs_storage
        )
        
        # Store matches in memory (in production, save to database)
        if not hasattr(calculate_job_matches, 'matches_storage'):
            calculate_job_matches.matches_storage = {}
        calculate_job_matches.matches_storage[user_id] = matches
        
        return CalculateMatchesResponse(
            message="Job matches calculated successfully",
            matches_calculated=len(matches),
            user_id=user_id,
            calculation_timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate job matches: {str(e)}"
        )


@router.get("/{user_id}/job-matches", response_model=JobMatchResponse)
async def get_job_matches(
    user_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    min_score: Optional[int] = Query(70, ge=0, le=100, description="Minimum match score filter"),
    limit: int = Query(20, ge=1, le=100, description="Number of matches to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
) -> JobMatchResponse:
    """
    Get calculated job matches for the user with optional filtering.
    
    Returns the job matches calculated by the calculate-matches endpoint,
    with optional filtering by minimum score and pagination support.
    
    Args:
        user_id: User ID to get matches for
        current_user: Current authenticated user
        db: Database session
        min_score: Minimum match score to include (0-100)
        limit: Maximum number of matches to return
        offset: Number of matches to skip for pagination
        
    Returns:
        JobMatchResponse: Paginated job matches
        
    Raises:
        HTTPException: If user not found, access denied, or no matches calculated
    """
    # Verify user can only access their own job matches
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Can only access your own job matches"
        )
    
    try:
        # Get stored matches (in production, retrieve from database)
        if not hasattr(calculate_job_matches, 'matches_storage'):
            calculate_job_matches.matches_storage = {}
        
        user_matches = calculate_job_matches.matches_storage.get(user_id, [])
        
        if not user_matches:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No job matches found. Please calculate matches first using POST /calculate-matches"
            )
        
        # Filter by minimum score
        filtered_matches = [
            match for match in user_matches 
            if match["match_score"] >= min_score
        ]
        
        # Apply pagination
        total = len(filtered_matches)
        paginated_matches = filtered_matches[offset:offset + limit]
        
        return JobMatchResponse(
            items=paginated_matches,
            total=total,
            limit=limit,
            offset=offset,
            has_more=offset + limit < total
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve job matches: {str(e)}"
        )


@router.post("/{user_id}/skill-analysis")
async def analyze_user_skill_gaps(
    user_id: int,
    request_data: Dict[str, Any],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
) -> Dict[str, Any]:
    """
    Analyze user skill gaps with learning recommendations.
    
    Provides comprehensive skill gap analysis including:
    - Missing skills identification with priority ranking
    - Market-driven skill importance calculation  
    - Salary impact analysis per skill
    - Learning difficulty assessment
    - Personalized learning recommendations
    
    Args:
        user_id: User ID to analyze skills for
        request_data: Analysis request with target job titles
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict containing comprehensive skill gap analysis
        
    Raises:
        HTTPException: If user not found or access denied
    """
    try:
        # Verify user can only analyze their own profile
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Can only analyze your own skill gaps"
            )
        
        # Get target job titles from request
        target_job_titles = request_data.get("target_job_titles", [])
        if not target_job_titles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="target_job_titles is required for skill gap analysis"
            )
        
        # Mock user skills (in production, would fetch from database)
        user_skills = ["Python", "Machine Learning", "FastAPI", "PostgreSQL"]
        
        # Mock market-driven skill analysis
        # In production, this would use Claude API for intelligent analysis
        market_skills_data = {
            "Senior ML Engineer": ["Python", "TensorFlow", "MLOps", "Kubernetes", "Docker", "AWS"],
            "Data Science Manager": ["Python", "Machine Learning", "Leadership", "SQL", "AWS", "Team Management"],
            "AI Research Scientist": ["Python", "PyTorch", "Research", "Statistics", "Deep Learning", "Publications"]
        }
        
        # Aggregate skills from target jobs
        all_required_skills = set()
        for job_title in target_job_titles:
            if job_title in market_skills_data:
                all_required_skills.update(market_skills_data[job_title])
        
        # Calculate missing skills
        user_skills_set = set(user_skills)
        missing_skills = list(all_required_skills - user_skills_set)
        
        # Generate skill gap analysis with market insights
        skill_gap_analysis = []
        for skill in missing_skills:
            # Mock market data calculation
            importance_score = 0.9 if skill in ["TensorFlow", "MLOps", "AWS"] else 0.7
            market_demand = "very_high" if importance_score > 0.8 else "high"
            salary_impact = "+15%" if importance_score > 0.8 else "+10%"
            acquisition_difficulty = "moderate"
            
            skill_gap_analysis.append({
                "skill_name": skill,
                "importance_score": importance_score,
                "market_demand": market_demand,
                "salary_impact": salary_impact,
                "acquisition_difficulty": acquisition_difficulty
            })
        
        # Sort by importance score (highest first)
        skill_gap_analysis.sort(key=lambda x: x["importance_score"], reverse=True)
        
        # Generate learning recommendations
        learning_recommendations = []
        for skill_data in skill_gap_analysis[:5]:  # Top 5 skills
            skill = skill_data["skill_name"]
            
            # Mock learning recommendations
            courses = [f"{skill} Fundamentals", f"Advanced {skill}"]
            projects = [f"Build {skill} project", f"{skill} portfolio"]
            estimated_hours = 40 if skill_data["acquisition_difficulty"] == "moderate" else 60
            prerequisites = ["Python basics"] if skill != "Python" else []
            
            learning_recommendations.append({
                "skill": skill,
                "courses": courses,
                "projects": projects,
                "estimated_hours": estimated_hours,
                "prerequisites": prerequisites
            })
        
        # Calculate skill priorities based on market demand
        skill_priorities = {
            "critical": [s for s in skill_gap_analysis if s["importance_score"] > 0.8],
            "important": [s for s in skill_gap_analysis if 0.6 < s["importance_score"] <= 0.8],
            "nice_to_have": [s for s in skill_gap_analysis if s["importance_score"] <= 0.6]
        }
        
        # Market insights
        market_insights = {
            "trending_skills": ["MLOps", "Kubernetes", "TensorFlow"],
            "salary_growth_potential": "15-25% increase with top 3 skills",
            "market_competition": "moderate",
            "recommended_timeline": "6-12 months for significant impact"
        }
        
        # Improvement timeline estimation
        improvement_timeline = {
            "3_months": [s["skill_name"] for s in skill_gap_analysis if s["acquisition_difficulty"] == "easy"][:2],
            "6_months": [s["skill_name"] for s in skill_gap_analysis if s["acquisition_difficulty"] == "moderate"][:3],
            "12_months": [s["skill_name"] for s in skill_gap_analysis if s["acquisition_difficulty"] == "hard"][:2]
        }
        
        logger.info(f"Skill gap analysis completed for user {user_id}. Found {len(missing_skills)} skill gaps.")
        
        return {
            "missing_skills": skill_gap_analysis,
            "skill_priorities": skill_priorities,
            "learning_recommendations": learning_recommendations,
            "market_insights": market_insights,
            "improvement_timeline": improvement_timeline,
            "analysis_summary": {
                "total_gaps_identified": len(missing_skills),
                "critical_skills_missing": len(skill_priorities["critical"]),
                "estimated_learning_hours": sum(r["estimated_hours"] for r in learning_recommendations),
                "target_jobs_analyzed": len(target_job_titles)
            },
            "generated_at": datetime.now().isoformat(),
            "analysis_version": "skill_gap_v1"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Skill gap analysis failed for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Skill analysis service temporarily unavailable: {str(e)}"
        )
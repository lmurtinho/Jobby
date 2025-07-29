"""
User profile router for AI Job Tracker.

This module provides FastAPI router with user profile management endpoints
including job matching functionality following CLAUDE.md conventions and API design patterns.
"""

from typing import Annotated, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserResponse, ResumeUploadResponse
from app.schemas.job import CalculateMatchesResponse, JobMatchResponse
from app.services.resume_service import ResumeService
from app.services.job_matching_service import JobMatchingService

# Create router instance
router = APIRouter(prefix="/api/v1/users", tags=["Users"])


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
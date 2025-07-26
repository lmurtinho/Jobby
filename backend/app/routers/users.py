"""
User profile router for AI Job Tracker.

This module provides FastAPI router with user profile management endpoints
following CLAUDE.md conventions and API design patterns.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserResponse, ResumeUploadResponse

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
    
    # Placeholder response for Day 2+ functionality
    # In Day 2+, this will:
    # 1. Save file to storage
    # 2. Extract text using PyPDF2
    # 3. Parse with Claude API for skill extraction
    # 4. Update user profile with extracted skills
    return ResumeUploadResponse(
        filename=resume.filename,
        parsing_result={
            "status": "placeholder",
            "message": "Resume upload endpoint - coming in Day 2",
            "note": "This endpoint will be enhanced with Claude API integration"
        },
        skills_extracted=["Python", "SQL", "Machine Learning"]  # Placeholder skills
    )
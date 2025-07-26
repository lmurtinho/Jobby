"""
User profile router for AI Job Tracker.

This module provides FastAPI router with user profile management endpoints
following CLAUDE.md conventions and API design patterns.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserResponse

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
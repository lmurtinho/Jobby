"""
Authentication router for AI Job Tracker.

This module provides FastAPI router with authentication endpoints
following CLAUDE.md conventions and API design patterns.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth import auth_service
from app.schemas.user import (
    UserRegistrationRequest, 
    UserRegistrationResponse,
    UserLoginRequest, 
    UserLoginResponse,
    UserResponse
)

# Create router instance
router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# Security scheme for JWT token
security = HTTPBearer()


@router.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegistrationRequest,
    db: Annotated[Session, Depends(get_db)]
) -> UserRegistrationResponse:
    """
    Register a new user account.
    
    Args:
        user_data: User registration information
        db: Database session
        
    Returns:
        UserRegistrationResponse: Created user with access token
        
    Raises:
        HTTPException: If email already exists or validation fails
    """
    try:
        # Create user through auth service
        created_user = auth_service.create_user(db, user_data)
        
        # Generate access token
        access_token = auth_service.generate_user_token(created_user)
        
        # Return response matching integration test expectations
        return UserRegistrationResponse(
            id=created_user.id,
            email=created_user.email,
            name=created_user.name,
            access_token=access_token,
            token_type="bearer"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions from auth service
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
async def login_user(
    login_data: UserLoginRequest,
    db: Annotated[Session, Depends(get_db)]
) -> UserLoginResponse:
    """
    Authenticate user and return access token.
    
    Args:
        login_data: User login credentials
        db: Database session
        
    Returns:
        UserLoginResponse: User information with access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = auth_service.authenticate_user(db, login_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Generate access token
    access_token = auth_service.generate_user_token(user)
    
    return UserLoginResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        access_token=access_token,
        token_type="bearer"
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)]
) -> UserResponse:
    """
    Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        
    Returns:
        UserResponse: Current user information
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Verify JWT token
    payload = auth_service.verify_token(credentials.credentials)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user ID from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user from database
    user = auth_service.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Return user response (excluding sensitive data)
    return UserResponse.from_orm(user)


# User profile endpoints (protected)
@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
) -> UserResponse:
    """
    Get current user's profile information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: User profile information
    """
    return current_user
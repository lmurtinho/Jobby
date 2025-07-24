"""
Authentication API endpoints.

This module provides user authentication endpoints including registration,
login, and token-based authentication following the API design in CLAUDE.md.
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.auth import auth_service


router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> UserResponse:
    """Get the current authenticated user."""
    user = auth_service.get_current_user(db, token)
    return UserResponse.model_validate(user)


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> dict:
    """
    Register a new user account and return access token.
    
    Creates a new user with the provided information and returns both the user data
    and an access token for immediate API access (auto-login after registration).
    """
    try:
        user = auth_service.create_user(db, user_data)
        
        # Generate access token for auto-login
        access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
        access_token = auth_service.create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        # Return user data + token
        user_response = UserResponse.model_validate(user)
        return {
            **user_response.model_dump(),
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": auth_service.access_token_expire_minutes * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """
    Login and receive an access token.
    
    Authenticates user credentials and returns a JWT access token for API access.
    Uses OAuth2 password flow for compatibility with FastAPI's automatic docs.
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=auth_service.access_token_expire_minutes * 60
    )


@router.post("/login-json", response_model=Token)
async def login_with_json(
    credentials: UserLogin,
    db: Session = Depends(get_db)
) -> Token:
    """
    Login with JSON credentials and receive an access token.
    
    Alternative login endpoint that accepts JSON credentials instead of form data.
    Useful for frontend applications that prefer JSON over form encoding.
    """
    user = auth_service.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=auth_service.access_token_expire_minutes * 60
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Get the current user's profile information.
    
    Returns the authenticated user's profile data. Requires a valid JWT token
    in the Authorization header.
    """
    return current_user


@router.get("/verify-token", response_model=dict)
async def verify_token(
    current_user: UserResponse = Depends(get_current_user)
) -> dict:
    """
    Verify that a token is valid and return basic user info.
    
    Useful for frontend applications to check if a stored token is still valid
    without fetching the full user profile.
    """
    return {"valid": True, "user_id": current_user.id, "email": current_user.email}

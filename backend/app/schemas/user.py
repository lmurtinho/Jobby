"""
User schemas for API request/response validation.

This module defines Pydantic models for user-related API operations
following the FastAPI conventions defined in CLAUDE.md.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., min_length=1, max_length=255, description="User's display name")
    location: Optional[str] = Field(None, max_length=255, description="User's location")
    timezone: Optional[str] = Field("UTC", max_length=100, description="User's timezone")
    experience_level: Optional[str] = Field("mid", description="Experience level: junior|mid|senior|lead")
    salary_min: Optional[int] = Field(None, ge=0, description="Minimum acceptable salary")
    salary_max: Optional[int] = Field(None, ge=0, description="Maximum salary expectation")
    currency: Optional[str] = Field("USD", max_length=10, description="Preferred currency")
    preferred_languages: Optional[List[str]] = Field(None, description="Preferred languages")
    
    @field_validator('experience_level')
    @classmethod
    def validate_experience_level(cls, v):
        """Validate experience level is one of allowed values."""
        if v and v not in ['junior', 'mid', 'senior', 'lead']:
            raise ValueError('Experience level must be one of: junior, mid, senior, lead')
        return v
    
    @field_validator('salary_max')
    @classmethod
    def validate_salary_range(cls, v, info):
        """Validate that salary_max >= salary_min if both are provided."""
        if v is not None and info.data.get('salary_min') is not None:
            if v < info.data['salary_min']:
                raise ValueError('Maximum salary must be greater than or equal to minimum salary')
        return v


class UserCreate(UserBase):
    """Schema for user registration request."""
    
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """Schema for user profile update request."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    timezone: Optional[str] = Field(None, max_length=100)
    experience_level: Optional[str] = None
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=10)
    preferred_languages: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    
    @field_validator('experience_level')
    @classmethod
    def validate_experience_level(cls, v):
        """Validate experience level is one of allowed values."""
        if v and v not in ['junior', 'mid', 'senior', 'lead']:
            raise ValueError('Experience level must be one of: junior, mid, senior, lead')
        return v


class UserResponse(UserBase):
    """Schema for user response (excludes sensitive data)."""
    
    id: int = Field(..., description="User's unique identifier")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(..., description="When the user was created")
    updated_at: datetime = Field(..., description="When the user was last updated")
    skills: Optional[List[str]] = Field(None, description="User's skills extracted from resume")
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login request."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class Token(BaseModel):
    """Schema for JWT token response."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenData(BaseModel):
    """Schema for token payload data."""
    
    user_id: Optional[int] = None
    email: Optional[str] = None

"""
User Pydantic schemas for AI Job Tracker.

This module defines request and response schemas for user-related endpoints
following CLAUDE.md conventions and FastAPI best practices.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator


class UserRegistrationRequest(BaseModel):
    """Schema for user registration request."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    location: Optional[str] = Field(None, max_length=255, description="User's location")
    timezone: Optional[str] = Field(None, max_length=100, description="User's timezone")
    experience_level: Optional[str] = Field(None, description="Experience level (junior, mid, senior, lead)")
    salary_min: Optional[int] = Field(None, ge=0, description="Minimum salary expectation")
    salary_max: Optional[int] = Field(None, ge=0, description="Maximum salary expectation")
    currency: str = Field("USD", max_length=10, description="Salary currency")
    preferred_languages: Optional[List[str]] = Field(None, description="List of preferred languages")
    
    @validator('experience_level')
    def validate_experience_level(cls, v):
        """Validate experience level is one of allowed values."""
        if v is not None and v not in ['junior', 'mid', 'senior', 'lead']:
            raise ValueError('Experience level must be one of: junior, mid, senior, lead')
        return v
    
    @validator('salary_max')
    def validate_salary_range(cls, v, values):
        """Validate salary_max is greater than salary_min."""
        if v is not None and 'salary_min' in values and values['salary_min'] is not None:
            if v < values['salary_min']:
                raise ValueError('salary_max must be greater than or equal to salary_min')
        return v


class UserLoginRequest(BaseModel):
    """Schema for user login request."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="User's full name")
    location: Optional[str] = Field(None, max_length=255, description="User's location")
    timezone: Optional[str] = Field(None, max_length=100, description="User's timezone")
    experience_level: Optional[str] = Field(None, description="Experience level (junior, mid, senior, lead)")
    salary_min: Optional[int] = Field(None, ge=0, description="Minimum salary expectation")
    salary_max: Optional[int] = Field(None, ge=0, description="Maximum salary expectation")
    currency: Optional[str] = Field(None, max_length=10, description="Salary currency")
    preferred_languages: Optional[List[str]] = Field(None, description="List of preferred languages")
    
    @validator('experience_level')
    def validate_experience_level(cls, v):
        """Validate experience level is one of allowed values."""
        if v is not None and v not in ['junior', 'mid', 'senior', 'lead']:
            raise ValueError('Experience level must be one of: junior, mid, senior, lead')
        return v


class UserResponse(BaseModel):
    """Schema for user response (public profile data)."""
    
    id: int = Field(..., description="User's unique ID")
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., description="User's full name")
    is_active: bool = Field(..., description="Whether user account is active")
    is_verified: bool = Field(..., description="Whether user email is verified")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    location: Optional[str] = Field(None, description="User's location")
    timezone: Optional[str] = Field(None, description="User's timezone")
    experience_level: Optional[str] = Field(None, description="Experience level")
    salary_min: Optional[int] = Field(None, description="Minimum salary expectation")
    salary_max: Optional[int] = Field(None, description="Maximum salary expectation")
    currency: str = Field(..., description="Salary currency")
    preferred_languages: Optional[List[str]] = Field(None, description="Preferred languages")
    skills: Optional[List[str]] = Field(None, description="User's skills from resume")
    resume_filename: Optional[str] = Field(None, description="Uploaded resume filename")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class UserRegistrationResponse(BaseModel):
    """Schema for user registration response."""
    
    id: int = Field(..., description="User's unique ID")
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., description="User's full name")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class UserLoginResponse(BaseModel):
    """Schema for user login response."""
    
    id: int = Field(..., description="User's unique ID")
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., description="User's full name")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    """Schema for resume upload response."""
    
    filename: str = Field(..., description="Uploaded filename")
    parsing_result: dict = Field(..., description="Parsed resume data from Claude API")
    skills_extracted: List[str] = Field(..., description="List of extracted skills")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
"""
Job and Job Matching Pydantic schemas for AI Job Tracker.

This module defines request and response schemas for job-related endpoints
including job matching functionality following CLAUDE.md conventions.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator


class JobResponse(BaseModel):
    """Schema for job response."""
    
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    salary: Optional[str] = Field(None, description="Salary information")
    description: str = Field(..., description="Job description")
    requirements: List[str] = Field(..., description="Job requirements/skills")
    apply_url: str = Field(..., description="Application URL")
    posted_date: str = Field(..., description="Posted date")
    source: str = Field(..., description="Job source (linkedin, remoteok, rss, etc.)")
    job_type: str = Field(..., description="Job type (Full-time, Part-time, Contract)")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class JobMatchCalculation(BaseModel):
    """Schema for job match calculation."""
    
    job_id: str = Field(..., description="Unique job identifier")
    match_score: int = Field(..., ge=0, le=100, description="Overall match score percentage")
    skill_match: int = Field(..., ge=0, le=100, description="Skill compatibility percentage")
    experience_match: int = Field(..., ge=0, le=100, description="Experience level match percentage")
    location_match: int = Field(..., ge=0, le=100, description="Location preference match percentage")
    salary_match: int = Field(..., ge=0, le=100, description="Salary expectation match percentage")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class JobMatchResult(BaseModel):
    """Schema for individual job match result."""
    
    job_id: str = Field(..., description="Unique job identifier")
    job: JobResponse = Field(..., description="Job details")
    match_score: int = Field(..., ge=0, le=100, description="Overall match score percentage")
    skill_breakdown: Dict[str, Any] = Field(..., description="Detailed skill analysis")
    experience_compatibility: Dict[str, Any] = Field(..., description="Experience level analysis")
    salary_analysis: Dict[str, Any] = Field(..., description="Salary compatibility analysis")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class JobMatchResponse(BaseModel):
    """Schema for job matching response with pagination."""
    
    items: List[JobMatchResult] = Field(..., description="List of job matches")
    total: int = Field(..., description="Total number of matches")
    limit: int = Field(..., description="Number of items per page")
    offset: int = Field(..., description="Offset for pagination")
    has_more: bool = Field(..., description="Whether there are more results")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class CalculateMatchesResponse(BaseModel):
    """Schema for calculate matches response."""
    
    message: str = Field(..., description="Status message")
    matches_calculated: int = Field(..., description="Number of matches calculated")
    user_id: int = Field(..., description="User ID")
    calculation_timestamp: datetime = Field(..., description="When calculation was performed")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class JobsListResponse(BaseModel):
    """Schema for jobs list response with pagination."""
    
    items: List[JobResponse] = Field(..., description="List of jobs")
    total: int = Field(..., description="Total number of jobs")
    limit: int = Field(..., description="Number of items per page")
    offset: int = Field(..., description="Offset for pagination")
    has_more: bool = Field(..., description="Whether there are more results")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True

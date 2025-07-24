"""
User model for AI Job Tracker application.

This module defines the User SQLAlchemy model following the project 
architecture and naming conventions defined in CLAUDE.md.
"""

from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Float, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """
    User model representing registered users in the AI Job Tracker system.
    
    This model stores user authentication information, profile details,
    and preferences for job matching and notifications.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        email: Unique email address for authentication
        password_hash: Hashed password using bcrypt
        name: User's display name
        is_active: Whether the user account is active
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last modified
        
        # Profile information
        location: User's location (city, country)
        timezone: User's timezone for scheduling
        experience_level: junior|mid|senior|lead
        
        # Job preferences
        salary_min: Minimum acceptable salary
        salary_max: Maximum salary expectation
        currency: Preferred currency (USD, BRL, etc.)
        preferred_languages: JSON array of preferred languages
        
        # Skills and resume data
        skills: JSON array of user's skills
        resume_text: Raw text from uploaded resume
        
        # Relationships (to be defined when other models are created)
        # job_matches: relationship to JobMatch
        # applications: relationship to JobApplication
        # skill_analyses: relationship to SkillGapAnalysis
    """
    
    __tablename__ = "users"
    
    # Primary key and basic fields
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Profile information
    location = Column(String(255), nullable=True)
    timezone = Column(String(100), nullable=True, default="UTC")
    experience_level = Column(String(50), nullable=True, default="mid")  # junior|mid|senior|lead
    
    # Job preferences
    salary_min = Column(Integer, nullable=True)  # Minimum salary in specified currency
    salary_max = Column(Integer, nullable=True)  # Maximum salary expectation
    currency = Column(String(10), nullable=True, default="USD")  # USD, BRL, EUR, etc.
    preferred_languages = Column(JSON, nullable=True)  # JSON array of preferred languages
    
    # Skills and resume data
    skills = Column(JSON, nullable=True)  # JSON array of skills
    resume_text = Column(Text, nullable=True)  # Raw resume text for analysis
    
    def __repr__(self) -> str:
        """String representation of User model."""
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"

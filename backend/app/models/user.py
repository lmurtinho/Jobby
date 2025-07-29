"""
User model for AI Job Tracker.

This module defines the User database model with authentication
and profile management capabilities following CLAUDE.md conventions.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    """
    User model for authentication and profile management.
    
    Attributes:
        id: Primary key
        email: Unique email address for authentication
        name: User's full name
        hashed_password: Bcrypt hashed password
        is_active: Whether the user account is active
        is_verified: Whether the user's email is verified
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        location: User's preferred location
        timezone: User's timezone preference
        experience_level: User's experience level (junior, mid, senior, lead)
        salary_min: Minimum salary expectation
        salary_max: Maximum salary expectation
        currency: Salary currency (USD, BRL, etc.)
        preferred_languages: List of preferred languages
        skills: List of user's skills extracted from resume
        resume_text: Raw extracted resume text for matching
        resume_filename: Original resume filename
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Profile fields from test expectations
    location = Column(String(255), nullable=True)
    timezone = Column(String(100), nullable=True)
    experience_level = Column(String(50), nullable=True)  # junior, mid, senior, lead
    
    # Salary expectations
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    currency = Column(String(10), default="USD", nullable=False)
    
    # Preferences
    preferred_languages = Column(JSON, nullable=True)  # List of languages
    
    # Resume and skills data
    skills = Column(JSON, nullable=True)  # List of skills from resume parsing
    resume_text = Column(Text, nullable=True)  # Extracted resume content
    resume_filename = Column(String(255), nullable=True)
    
    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated (has valid account)."""
        return self.is_active
    
    def to_dict(self) -> dict:
        """Convert User to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "location": self.location,
            "timezone": self.timezone,
            "experience_level": self.experience_level,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "currency": self.currency,
            "preferred_languages": self.preferred_languages,
            "skills": self.skills,
            "resume_filename": self.resume_filename
        }
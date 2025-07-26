"""
Authentication service for AI Job Tracker.

This module provides authentication functionality including password hashing,
JWT token generation, and user verification following CLAUDE.md conventions.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserRegistrationRequest, UserLoginRequest


class AuthService:
    """
    Authentication service for user management and security.
    
    Handles password hashing, JWT token generation, user creation,
    and authentication verification.
    """
    
    def __init__(self):
        """Initialize authentication service."""
        # Password hashing context using bcrypt
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # JWT configuration
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    def hash_password(self, password: str) -> str:
        """
        Hash a plain password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            str: Hashed password
        """
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Optional custom expiration time
            
        Returns:
            str: JWT access token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Optional[Dict[str, Any]]: Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            db: Database session
            email: User's email address
            
        Returns:
            Optional[User]: User object or None if not found
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: User's ID
            
        Returns:
            Optional[User]: User object or None if not found
        """
        return db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, db: Session, user_data: UserRegistrationRequest) -> User:
        """
        Create a new user account.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            User: Created user object
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        existing_user = self.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = self.hash_password(user_data.password)
        
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password,
            location=user_data.location,
            timezone=user_data.timezone,
            experience_level=user_data.experience_level,
            salary_min=user_data.salary_min,
            salary_max=user_data.salary_max,
            currency=user_data.currency,
            preferred_languages=user_data.preferred_languages
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    def authenticate_user(self, db: Session, login_data: UserLoginRequest) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            db: Database session
            login_data: User login credentials
            
        Returns:
            Optional[User]: User object if authentication successful, None otherwise
        """
        user = self.get_user_by_email(db, login_data.email)
        
        if not user:
            return None
        
        if not self.verify_password(login_data.password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def generate_user_token(self, user: User) -> str:
        """
        Generate JWT token for a user.
        
        Args:
            user: User object
            
        Returns:
            str: JWT access token
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name
        }
        
        return self.create_access_token(data=token_data)


# Global auth service instance
auth_service = AuthService()
"""
Pydantic schemas for AI-powered resume parsing and analysis.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ExtractedSkill(BaseModel):
    """Schema for extracted skills from resume."""
    name: str = Field(..., description="Name of the skill")
    category: str = Field(..., description="Category of the skill (e.g., Programming Language, Framework)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for skill extraction")


class ExperienceEntry(BaseModel):
    """Schema for work experience entry."""
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job position/title")
    start_date: str = Field(..., description="Start date of employment")
    end_date: Optional[str] = Field(None, description="End date of employment (None if current)")
    description: str = Field(..., description="Job description or responsibilities")
    skills_used: List[str] = Field(default=[], description="Skills used in this role")


class EducationEntry(BaseModel):
    """Schema for education entry."""
    institution: str = Field(..., description="Educational institution name")
    degree: str = Field(..., description="Degree or certification obtained")
    start_date: str = Field(..., description="Start date of education")
    end_date: Optional[str] = Field(None, description="End date of education")
    gpa: Optional[float] = Field(None, description="GPA if available")
    major: Optional[str] = Field(None, description="Major or field of study")


class ResumeParseRequest(BaseModel):
    """Request schema for resume parsing."""
    resume_text: str = Field(..., min_length=1, description="Raw resume text to parse")
    enhance_skills: bool = Field(default=True, description="Whether to enhance skill extraction")
    extract_experience: bool = Field(default=True, description="Whether to extract work experience")
    extract_education: bool = Field(default=True, description="Whether to extract education")


class ResumeParseResponse(BaseModel):
    """Response schema for parsed resume data."""
    full_name: Optional[str] = Field(None, description="Full name extracted from resume")
    email: Optional[str] = Field(None, description="Email address extracted from resume")
    phone: Optional[str] = Field(None, description="Phone number extracted from resume")
    location: Optional[str] = Field(None, description="Location/address extracted from resume")
    
    skills: List[ExtractedSkill] = Field(default=[], description="Extracted skills with confidence scores")
    experience: List[ExperienceEntry] = Field(default=[], description="Work experience entries")
    education: List[EducationEntry] = Field(default=[], description="Education entries")
    
    years_of_experience: Optional[int] = Field(None, description="Total years of professional experience")
    seniority_level: Optional[str] = Field(None, description="Estimated seniority level (Junior, Mid, Senior, Lead)")
    
    summary: Optional[str] = Field(None, description="Professional summary or objective")
    certifications: List[str] = Field(default=[], description="Professional certifications")
    languages: List[str] = Field(default=[], description="Languages spoken")
    
    parse_confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall parsing confidence")
    processing_time_ms: Optional[int] = Field(None, description="Time taken to process the resume")


class SkillGapAnalysisRequest(BaseModel):
    """Request schema for skill gap analysis."""
    user_skills: List[str] = Field(..., description="User's current skills")
    job_requirements: List[str] = Field(..., description="Required skills for target job")
    user_experience_years: Optional[int] = Field(None, description="User's years of experience")
    target_seniority: Optional[str] = Field(None, description="Target seniority level")


class SkillGap(BaseModel):
    """Schema for individual skill gap."""
    skill: str = Field(..., description="Name of the missing skill")
    importance: str = Field(..., description="Importance level (High, Medium, Low)")
    alternative_to: Optional[str] = Field(None, description="What existing skill this could replace")
    learning_resources: List[str] = Field(default=[], description="Suggested learning resources")
    estimated_learning_time: Optional[str] = Field(None, description="Estimated time to learn this skill")


class SkillGapAnalysisResponse(BaseModel):
    """Response schema for skill gap analysis."""
    skill_gaps: List[SkillGap] = Field(default=[], description="Identified skill gaps")
    matching_skills: List[str] = Field(default=[], description="Skills that already match requirements")
    gap_severity: str = Field(..., description="Overall gap severity (Low, Medium, High, Critical)")
    match_percentage: float = Field(..., ge=0.0, le=1.0, description="Percentage of skills that match")
    recommendations: List[str] = Field(default=[], description="Personalized recommendations")
    priority_skills: List[str] = Field(default=[], description="Top priority skills to learn first")


class JobEnhancementRequest(BaseModel):
    """Request schema for job description enhancement."""
    raw_description: str = Field(..., min_length=1, description="Raw job description text")
    enhance_skills: bool = Field(default=True, description="Whether to enhance skill extraction")
    estimate_salary: bool = Field(default=True, description="Whether to estimate salary range")
    analyze_requirements: bool = Field(default=True, description="Whether to analyze requirements")


class JobEnhancementResponse(BaseModel):
    """Response schema for enhanced job description."""
    enhanced_description: str = Field(..., description="Enhanced and formatted job description")
    extracted_skills: List[str] = Field(default=[], description="Extracted required skills")
    nice_to_have_skills: List[str] = Field(default=[], description="Nice-to-have skills")
    seniority_level: Optional[str] = Field(None, description="Required seniority level")
    required_experience_years: Optional[int] = Field(None, description="Required years of experience")
    industry: Optional[str] = Field(None, description="Industry classification")
    company_size: Optional[str] = Field(None, description="Estimated company size")
    remote_friendly: Optional[bool] = Field(None, description="Whether job supports remote work")
    estimated_salary_min: Optional[int] = Field(None, description="Estimated minimum salary")
    estimated_salary_max: Optional[int] = Field(None, description="Estimated maximum salary")
    benefits: List[str] = Field(default=[], description="Identified benefits")


class SemanticJobMatchRequest(BaseModel):
    """Request schema for semantic job matching."""
    user_profile: Dict[str, Any] = Field(..., description="User profile data")
    job_posting: Dict[str, Any] = Field(..., description="Job posting data")
    weight_skills: float = Field(default=0.4, description="Weight for skill matching")
    weight_experience: float = Field(default=0.3, description="Weight for experience matching")
    weight_industry: float = Field(default=0.2, description="Weight for industry matching")
    weight_location: float = Field(default=0.1, description="Weight for location matching")


class SemanticJobMatchResponse(BaseModel):
    """Response schema for semantic job matching."""
    match_score: float = Field(..., ge=0.0, le=1.0, description="Overall match score")
    skill_match_percentage: float = Field(..., ge=0.0, le=1.0, description="Skill match percentage")
    experience_match: str = Field(..., description="Experience match assessment")
    industry_alignment: str = Field(..., description="Industry alignment assessment")
    location_compatibility: Optional[str] = Field(None, description="Location compatibility")
    
    strengths: List[str] = Field(default=[], description="User's strengths for this position")
    areas_for_growth: List[str] = Field(default=[], description="Areas where user could improve")
    recommendation: str = Field(..., description="Overall recommendation for this job")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the match assessment")

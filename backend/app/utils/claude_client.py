"""
Claude API client for AI Job Tracker.

This module provides a client for interacting with the Claude API
for resume parsing and other AI functionality.
"""

import json
import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

import anthropic
from anthropic import AsyncAnthropic

from app.schemas.ai_resume import (
    ResumeParseRequest,
    ResumeParseResponse,
    SkillGapAnalysisRequest,
    SkillGapAnalysisResponse,
    JobEnhancementRequest,
    JobEnhancementResponse,
    SemanticJobMatchRequest,
    SemanticJobMatchResponse,
)


# Custom exceptions for Claude API
class ClaudeAPIError(Exception):
    """Base exception for Claude API errors."""
    pass


class ClaudeRateLimitError(ClaudeAPIError):
    """Exception raised when Claude API rate limit is exceeded."""
    pass


class ClaudeClient:
    """
    Async client for interacting with the Claude API.
    
    Provides high-level methods for resume parsing, skill gap analysis,
    job description enhancement, and semantic job matching.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 4000,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize Claude client.
        
        Args:
            api_key: Anthropic API key
            model: Claude model to use
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be empty")
            
        # Validate model name
        valid_models = [
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229",
            "claude-3-haiku-20240307"
        ]
        if model not in valid_models:
            raise ValueError(f"Invalid model: {model}")
            
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries
        
        self._client = AsyncAnthropic(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    async def parse_resume(self, request: ResumeParseRequest) -> ResumeParseResponse:
        """
        Parse resume text using Claude API.
        
        Args:
            request: Resume parse request
            
        Returns:
            Parsed resume data
            
        Raises:
            ValueError: If resume text is empty
            ClaudeAPIError: If API call fails
            ClaudeRateLimitError: If rate limit exceeded
        """
        if not request.resume_text or request.resume_text.strip() == "":
            raise ValueError("Resume text cannot be empty")
            
        # Truncate very long resumes to prevent token limit issues
        max_length = 15000  # Conservative limit for Claude
        resume_text = request.resume_text[:max_length] if len(request.resume_text) > max_length else request.resume_text
            
        # Build the prompt for Claude
        prompt = self._build_resume_parse_prompt(resume_text)
        
        try:
            # Call Claude API with retry logic
            response_text = await self._call_claude_with_retry(prompt)
            
            # Parse the JSON response
            parsed_data = self._parse_json_response(response_text)
            
            # Convert to ResumeParseResponse
            return self._convert_to_resume_response(parsed_data)
            
        except anthropic.RateLimitError as e:
            self.logger.error(f"Claude API rate limit exceeded: {e}")
            raise ClaudeRateLimitError(f"Rate limit exceeded: {e}")
        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise ClaudeAPIError(f"Failed to parse resume: {e}")

    async def analyze_skill_gap(
        self, 
        user_skills: List[str], 
        job_requirements: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze skill gaps between user skills and job requirements.
        
        Args:
            user_skills: List of user's current skills
            job_requirements: List of required skills for job
            
        Returns:
            Skill gap analysis results
        """
        if not user_skills or not job_requirements:
            raise ValueError("Both user_skills and job_requirements must be provided")
            
        # Build the prompt for Claude
        prompt = self._build_skill_gap_prompt(user_skills, job_requirements)
        
        try:
            # Call Claude API with retry logic
            response_text = await self._call_claude_with_retry(prompt)
            
            # Parse the JSON response
            parsed_data = self._parse_json_response(response_text)
            
            return parsed_data
            
        except anthropic.RateLimitError as e:
            self.logger.error(f"Claude API rate limit exceeded: {e}")
            raise ClaudeRateLimitError(f"Rate limit exceeded: {e}")
        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise ClaudeAPIError(f"Failed to analyze skill gap: {e}")

    async def enhance_job_description(self, raw_description: str) -> Dict[str, Any]:
        """
        Enhance job description with extracted skills and metadata.
        
        Args:
            raw_description: Raw job description text
            
        Returns:
            Enhanced job description data
        """
        if not raw_description or raw_description.strip() == "":
            raise ValueError("Job description cannot be empty")
            
        # Build the prompt for Claude
        prompt = self._build_job_enhancement_prompt(raw_description)
        
        try:
            # Call Claude API with retry logic
            response_text = await self._call_claude_with_retry(prompt)
            
            # Parse the JSON response
            parsed_data = self._parse_json_response(response_text)
            
            return parsed_data
            
        except anthropic.RateLimitError as e:
            self.logger.error(f"Claude API rate limit exceeded: {e}")
            raise ClaudeRateLimitError(f"Rate limit exceeded: {e}")
        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise ClaudeAPIError(f"Failed to enhance job description: {e}")

    async def semantic_job_match(
        self, 
        user_profile: Dict[str, Any], 
        job_posting: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform semantic job matching between user profile and job posting.
        
        Args:
            user_profile: User profile data
            job_posting: Job posting data
            
        Returns:
            Semantic match analysis results
        """
        if not user_profile or not job_posting:
            raise ValueError("Both user_profile and job_posting must be provided")
            
        # Build the prompt for Claude
        prompt = self._build_semantic_match_prompt(user_profile, job_posting)
        
        try:
            # Call Claude API with retry logic
            response_text = await self._call_claude_with_retry(prompt)
            
            # Parse the JSON response
            parsed_data = self._parse_json_response(response_text)
            
            return parsed_data
            
        except anthropic.RateLimitError as e:
            self.logger.error(f"Claude API rate limit exceeded: {e}")
            raise ClaudeRateLimitError(f"Rate limit exceeded: {e}")
        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise ClaudeAPIError(f"Failed to perform semantic job match: {e}")

    # Private helper methods
    
    def _build_semantic_match_prompt(self, user_profile: Dict[str, Any], job_posting: Dict[str, Any]) -> str:
        """Build the prompt for Claude to perform semantic job matching."""
        return f"""
You are an expert job matching analyst. Analyze the semantic compatibility between a user profile and job posting.

User Profile:
{user_profile}

Job Posting:
{job_posting}

Please analyze and return a JSON object with the following structure:
{{
    "overall_match_score": 0.0-1.0,
    "skill_compatibility": {{
        "matching_skills": ["skill1", "skill2"],
        "missing_skills": ["skill1", "skill2"],
        "transferable_skills": ["skill1", "skill2"],
        "skill_match_score": 0.0-1.0
    }},
    "experience_compatibility": {{
        "years_difference": integer,
        "relevant_experience": boolean,
        "experience_match_score": 0.0-1.0
    }},
    "cultural_fit": {{
        "company_culture_match": 0.0-1.0,
        "values_alignment": 0.0-1.0,
        "work_style_compatibility": 0.0-1.0
    }},
    "growth_potential": {{
        "career_progression_opportunity": 0.0-1.0,
        "learning_opportunities": ["opportunity1", "opportunity2"],
        "skill_development_potential": 0.0-1.0
    }},
    "recommendation": "Strong Match|Good Match|Moderate Match|Weak Match",
    "key_strengths": ["strength1", "strength2"],
    "areas_for_development": ["area1", "area2"],
    "interview_talking_points": ["point1", "point2"]
}}

Instructions:
1. Calculate overall match score based on skills, experience, and fit
2. Analyze skill compatibility including transferable skills
3. Evaluate experience relevance and seniority alignment
4. Assess cultural fit based on company information
5. Identify growth and learning opportunities
6. Provide specific recommendations and talking points
7. Return only valid JSON, no additional text
"""

    def _build_job_enhancement_prompt(self, raw_description: str) -> str:
        """Build the prompt for Claude to enhance job descriptions."""
        return f"""
You are an expert job description analyzer and enhancer. Analyze the following raw job description and extract structured information.

Raw Job Description:
{raw_description}

Please analyze and return a JSON object with the following structure:
{{
    "enhanced_description": "improved and structured job description text",
    "extracted_skills": ["skill1", "skill2", "skill3"],
    "seniority_level": "Junior|Mid|Senior|Lead|Executive",
    "required_experience_years": integer or null,
    "industry": "industry name",
    "remote_friendly": boolean,
    "company_size": "Startup|Small|Medium|Large|Enterprise" or null,
    "job_type": "Full-time|Part-time|Contract|Internship",
    "benefits": ["benefit1", "benefit2"],
    "responsibilities": ["responsibility1", "responsibility2"],
    "requirements": ["requirement1", "requirement2"]
}}

Instructions:
1. Enhance the description with better formatting and clarity
2. Extract technical and soft skills mentioned
3. Determine seniority level from job title and requirements
4. Estimate required experience years from context
5. Identify industry from company/role context
6. Check for remote work mentions
7. Extract benefits, responsibilities, and requirements
8. Return only valid JSON, no additional text
"""

    def _build_skill_gap_prompt(self, user_skills: List[str], job_requirements: List[str]) -> str:
        """Build the prompt for Claude to analyze skill gaps."""
        return f"""
You are an expert career analyst. Analyze the skill gap between a user's current skills and job requirements.

User's Current Skills:
{', '.join(user_skills)}

Job Requirements:
{', '.join(job_requirements)}

Please analyze and return a JSON object with the following structure:
{{
    "skill_gaps": [
        {{
            "skill": "skill_name",
            "importance": "High|Medium|Low",
            "alternative_to": "existing_skill_name or null"
        }}
    ],
    "matching_skills": ["skill1", "skill2"],
    "gap_severity": "Low|Medium|High",
    "recommendations": [
        "specific learning recommendation 1",
        "specific learning recommendation 2"
    ]
}}

Instructions:
1. Identify skills required by the job that the user doesn't have
2. Rate importance of each missing skill (High/Medium/Low)
3. Identify if missing skills are alternatives to existing skills
4. List skills the user already has that match job requirements
5. Assess overall gap severity
6. Provide specific, actionable learning recommendations
7. Return only valid JSON, no additional text
"""

    def _build_resume_parse_prompt(self, resume_text: str) -> str:
        """Build the prompt for Claude to parse a resume."""
        return f"""
You are an expert resume parser and career analyst. Parse the following resume text and extract structured information.

Resume Text:
{resume_text}

Please analyze this resume and return a JSON object with the following structure:
{{
    "full_name": "string or null",
    "email": "string or null", 
    "phone": "string or null",
    "location": "string or null",
    "skills": [
        {{"name": "skill_name", "category": "category", "confidence": 0.0-1.0}}
    ],
    "experience": [
        {{
            "company": "company_name",
            "position": "job_title", 
            "start_date": "year or date",
            "end_date": "year or date or null",
            "description": "brief description",
            "skills_used": ["skill1", "skill2"]
        }}
    ],
    "education": [
        {{
            "institution": "school_name",
            "degree": "degree_title",
            "start_date": "year",
            "end_date": "year or null",
            "gpa": null,
            "major": "major or null"
        }}
    ],
    "years_of_experience": integer,
    "seniority_level": "Junior|Mid|Senior|Lead|Executive",
    "summary": "brief professional summary",
    "certifications": ["cert1", "cert2"],
    "languages": ["language1", "language2"],
    "parse_confidence": 0.0-1.0
}}

Instructions:
1. Extract skills and categorize them (Programming Language, Framework, Database, Cloud Platform, etc.)
2. Calculate confidence scores based on how clearly skills are mentioned
3. Determine years of experience from work history
4. Assess seniority level based on job titles and experience
5. Return only valid JSON, no additional text
6. Use null for missing information, don't guess
"""

    async def _call_claude_with_retry(self, prompt: str) -> str:
        """Call Claude API with retry logic for transient failures."""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                message = await self._client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=[
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ]
                )
                
                # Extract text from response
                if message.content and len(message.content) > 0:
                    # Handle TextBlock (most common case)
                    content_block = message.content[0]
                    if hasattr(content_block, 'text'):
                        return content_block.text
                    else:
                        # Fallback - convert to string and extract what we can
                        content_str = str(content_block)
                        self.logger.warning(f"Unexpected content type: {type(content_block)}")
                        return content_str
                else:
                    raise ClaudeAPIError("Empty response from Claude API")
                    
            except anthropic.RateLimitError:
                # Don't retry rate limit errors
                raise
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Wait before retrying (exponential backoff)
                    wait_time = 2 ** attempt
                    self.logger.warning(f"Claude API call failed (attempt {attempt + 1}/{self.max_retries}), retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                    continue
                break
        
        # All retries failed
        raise ClaudeAPIError(f"Failed after {self.max_retries} attempts: {last_exception}")

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from Claude, handling potential formatting issues."""
        try:
            # Clean up the response text
            response_text = response_text.strip()
            
            # Remove any markdown code blocks
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                # Remove first line (```json or ```)
                lines = lines[1:]
                # Remove last line if it's ```
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                response_text = '\n'.join(lines)
            
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            self.logger.error(f"Response text: {response_text}")
            raise ClaudeAPIError(f"Invalid JSON response from Claude: {e}")

    def _convert_to_resume_response(self, data: Dict[str, Any]) -> ResumeParseResponse:
        """Convert parsed data to ResumeParseResponse object."""
        from app.schemas.ai_resume import ExtractedSkill, ExperienceEntry, EducationEntry
        
        # Convert skills
        skills = []
        for skill_data in data.get("skills", []):
            skills.append(ExtractedSkill(
                name=skill_data.get("name", ""),
                category=skill_data.get("category", "Other"),
                confidence=skill_data.get("confidence", 0.0)
            ))
        
        # Convert experience
        experience = []
        for exp_data in data.get("experience", []):
            experience.append(ExperienceEntry(
                company=exp_data.get("company", ""),
                position=exp_data.get("position", ""),
                start_date=exp_data.get("start_date", ""),
                end_date=exp_data.get("end_date"),
                description=exp_data.get("description", ""),
                skills_used=exp_data.get("skills_used", [])
            ))
        
        # Convert education
        education = []
        for edu_data in data.get("education", []):
            education.append(EducationEntry(
                institution=edu_data.get("institution", ""),
                degree=edu_data.get("degree", ""),
                start_date=edu_data.get("start_date", ""),
                end_date=edu_data.get("end_date"),
                gpa=edu_data.get("gpa"),
                major=edu_data.get("major")
            ))
        
        return ResumeParseResponse(
            full_name=data.get("full_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            location=data.get("location"),
            skills=skills,
            experience=experience,
            education=education,
            years_of_experience=data.get("years_of_experience"),
            seniority_level=data.get("seniority_level"),
            summary=data.get("summary"),
            certifications=data.get("certifications", []),
            languages=data.get("languages", []),
            parse_confidence=data.get("parse_confidence", 0.0),
            processing_time_ms=None  # Will be calculated if needed
        )


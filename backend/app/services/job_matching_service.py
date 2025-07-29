"""
Job Matching Service for AI Job Tracker.

This module provides job matching functionality using user skills and preferences
to calculate compatibility scores with available job postings.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class JobMatchingService:
    """Service for calculating job matches based on user profile and skills."""
    
    def __init__(self):
        """Initialize the job matching service."""
        self.logger = logger
    
    def calculate_job_matches(
        self, 
        user_skills: List[str], 
        user_experience_level: Optional[str],
        user_location: Optional[str],
        user_salary_min: Optional[int],
        user_salary_max: Optional[int],
        available_jobs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate match scores for all available jobs against user profile.
        
        Args:
            user_skills: List of user's skills extracted from resume
            user_experience_level: User's experience level (junior, mid, senior, lead)
            user_location: User's preferred location
            user_salary_min: User's minimum salary expectation
            user_salary_max: User's maximum salary expectation
            available_jobs: List of available job postings
        
        Returns:
            List of job matches with calculated scores
        """
        matches = []
        
        for i, job in enumerate(available_jobs):
            job_id = f"job_{i + 1}"  # Generate job ID based on position
            
            # Calculate individual match components
            skill_score = self._calculate_skill_match(user_skills, job.get("requirements", []))
            experience_score = self._calculate_experience_match(
                user_experience_level, 
                job.get("title", ""), 
                job.get("description", "")
            )
            location_score = self._calculate_location_match(user_location, job.get("location", ""))
            salary_score = self._calculate_salary_match(
                user_salary_min, 
                user_salary_max, 
                job.get("salary", "")
            )
            
            # Calculate overall match score (weighted average)
            overall_score = int(
                (skill_score * 0.4) +           # 40% weight on skills
                (experience_score * 0.25) +     # 25% weight on experience
                (location_score * 0.20) +       # 20% weight on location
                (salary_score * 0.15)           # 15% weight on salary
            )
            
            # Create detailed breakdown
            skill_breakdown = self._create_skill_breakdown(user_skills, job.get("requirements", []))
            experience_compatibility = self._create_experience_breakdown(
                user_experience_level, job.get("title", ""), job.get("description", "")
            )
            salary_analysis = self._create_salary_breakdown(
                user_salary_min, user_salary_max, job.get("salary", "")
            )
            
            match_result = {
                "job_id": job_id,
                "job": job,
                "match_score": overall_score,
                "skill_match": skill_score,
                "experience_match": experience_score,
                "location_match": location_score,
                "salary_match": salary_score,
                "skill_breakdown": skill_breakdown,
                "experience_compatibility": experience_compatibility,
                "salary_analysis": salary_analysis
            }
            
            matches.append(match_result)
        
        # Sort by match score (descending)
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        
        self.logger.info(f"Calculated matches for {len(available_jobs)} jobs")
        return matches
    
    def _calculate_skill_match(self, user_skills: List[str], job_requirements: List[str]) -> int:
        """Calculate skill match percentage."""
        if not user_skills or not job_requirements:
            return 0
        
        # Normalize skills to lowercase for comparison
        user_skills_lower = [skill.lower().strip() for skill in user_skills]
        job_requirements_lower = [req.lower().strip() for req in job_requirements]
        
        # Count matching skills
        matching_skills = sum(1 for skill in user_skills_lower if skill in job_requirements_lower)
        
        # Calculate percentage based on job requirements
        skill_percentage = int((matching_skills / len(job_requirements_lower)) * 100)
        
        return min(skill_percentage, 100)
    
    def _calculate_experience_match(self, user_level: Optional[str], job_title: str, job_description: str) -> int:
        """Calculate experience level match percentage."""
        if not user_level:
            return 80  # Default score if no experience level specified
        
        job_text = f"{job_title} {job_description}".lower()
        
        # Define experience level mappings
        experience_mapping = {
            "junior": ["junior", "entry", "associate", "trainee", "graduate"],
            "mid": ["mid", "intermediate", "experienced", "analyst", "developer"],
            "senior": ["senior", "lead", "principal", "expert", "architect"],
            "lead": ["lead", "manager", "director", "head", "chief", "principal"]
        }
        
        user_level_lower = user_level.lower()
        
        # Check if job matches user's experience level
        if user_level_lower in experience_mapping:
            level_keywords = experience_mapping[user_level_lower]
            for keyword in level_keywords:
                if keyword in job_text:
                    return 95  # High match if explicit level match
        
        # Check for level compatibility (can apply to lower or same level)
        levels_order = ["junior", "mid", "senior", "lead"]
        user_index = levels_order.index(user_level_lower) if user_level_lower in levels_order else 1
        
        # Determine job level from text
        job_level_index = 1  # Default to mid-level
        for i, level in enumerate(levels_order):
            level_keywords = experience_mapping.get(level, [])
            if any(keyword in job_text for keyword in level_keywords):
                job_level_index = i
                break
        
        # Calculate compatibility score
        level_diff = abs(user_index - job_level_index)
        if level_diff == 0:
            return 95  # Perfect match
        elif level_diff == 1:
            return 85  # Good match
        elif level_diff == 2:
            return 70  # Acceptable match
        else:
            return 50  # Poor match
    
    def _calculate_location_match(self, user_location: Optional[str], job_location: str) -> int:
        """Calculate location match percentage."""
        if not user_location or not job_location:
            return 100  # Default high score if no location specified
        
        user_loc_lower = user_location.lower()
        job_loc_lower = job_location.lower()
        
        # Remote work gets high score
        if "remote" in job_loc_lower:
            return 100
        
        # Exact match
        if user_loc_lower in job_loc_lower or job_loc_lower in user_loc_lower:
            return 100
        
        # City/state matching logic for Brazil
        if any(word in job_loc_lower for word in user_loc_lower.split()):
            return 85
        
        # Same country (Brazil indicators)
        brazil_indicators = ["brazil", "brasil", "br", "são paulo", "rio de janeiro", "bh", "mg", "sp", "rj"]
        user_in_brazil = any(indicator in user_loc_lower for indicator in brazil_indicators)
        job_in_brazil = any(indicator in job_loc_lower for indicator in brazil_indicators)
        
        if user_in_brazil and job_in_brazil:
            return 75
        
        return 60  # Different locations
    
    def _calculate_salary_match(
        self, 
        user_min: Optional[int], 
        user_max: Optional[int], 
        job_salary: str
    ) -> int:
        """Calculate salary match percentage."""
        if not user_min or not job_salary:
            return 90  # Default high score if no salary info
        
        # Extract numbers from job salary string
        import re
        numbers = re.findall(r'[\d,]+', job_salary.replace(',', ''))
        
        if not numbers:
            return 90  # No salary info in job posting
        
        # Try to extract salary range
        job_salaries = [int(num.replace(',', '')) for num in numbers if num.replace(',', '').isdigit()]
        
        if not job_salaries:
            return 90
        
        # Use the highest salary from the job posting
        job_max_salary = max(job_salaries)
        
        # Convert currency if needed (simplified conversion)
        if "r$" in job_salary.lower() or "brl" in job_salary.lower():
            # Convert BRL to USD (approximate rate: 1 USD = 5 BRL)
            job_max_salary = job_max_salary / 5
        
        # Calculate match based on user expectations
        if job_max_salary >= user_min:
            if user_max and job_max_salary <= user_max:
                return 100  # Perfect fit
            elif job_max_salary >= user_min * 1.2:
                return 95   # Above expectations
            else:
                return 85   # Meets minimum
        else:
            # Below expectations
            ratio = job_max_salary / user_min if user_min > 0 else 0
            return int(max(ratio * 80, 30))  # Minimum 30% if there's some salary
    
    def _create_skill_breakdown(self, user_skills: List[str], job_requirements: List[str]) -> Dict[str, Any]:
        """Create detailed skill breakdown."""
        user_skills_lower = [skill.lower().strip() for skill in user_skills]
        job_requirements_lower = [req.lower().strip() for req in job_requirements]
        
        matching_skills = [skill for skill in user_skills if skill.lower() in job_requirements_lower]
        missing_skills = [req for req in job_requirements if req.lower() not in user_skills_lower]
        
        return {
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "match_percentage": len(matching_skills) / max(len(job_requirements), 1) * 100,
            "total_required": len(job_requirements),
            "total_matched": len(matching_skills)
        }
    
    def _create_experience_breakdown(
        self, 
        user_level: Optional[str], 
        job_title: str, 
        job_description: str
    ) -> Dict[str, Any]:
        """Create detailed experience compatibility breakdown."""
        return {
            "user_level": user_level or "Not specified",
            "job_level_detected": self._detect_job_level(job_title, job_description),
            "compatibility": "Good match" if user_level else "Level not specified",
            "recommendation": self._get_experience_recommendation(user_level, job_title)
        }
    
    def _create_salary_breakdown(
        self, 
        user_min: Optional[int], 
        user_max: Optional[int], 
        job_salary: str
    ) -> Dict[str, Any]:
        """Create detailed salary analysis breakdown."""
        return {
            "user_expectation": {
                "min": user_min,
                "max": user_max,
                "currency": "USD"
            },
            "job_offer": job_salary or "Not specified",
            "analysis": "Competitive" if user_min else "No salary expectation specified"
        }
    
    def _detect_job_level(self, job_title: str, job_description: str) -> str:
        """Detect job experience level from title and description."""
        text = f"{job_title} {job_description}".lower()
        
        if any(word in text for word in ["senior", "lead", "principal", "architect"]):
            return "Senior"
        elif any(word in text for word in ["junior", "entry", "associate", "trainee"]):
            return "Junior"
        else:
            return "Mid-level"
    
    def _get_experience_recommendation(self, user_level: Optional[str], job_title: str) -> str:
        """Get experience-based recommendation."""
        if not user_level:
            return "Complete your profile with experience level for better matching"
        
        job_title_lower = job_title.lower()
        if "senior" in job_title_lower and user_level == "junior":
            return "Consider developing more experience before applying"
        elif "junior" in job_title_lower and user_level in ["senior", "lead"]:
            return "This role might be below your experience level"
        else:
            return "Good experience level match for this position"

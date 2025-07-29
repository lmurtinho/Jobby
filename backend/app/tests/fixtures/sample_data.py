"""
Sample test data and fixtures.

This module provides sample data for testing various components of the AI Job Tracker,
including resumes, job postings, user profiles, and expected parsing results.
"""

from typing import Dict, List, Any
import base64


def sample_resume_pdf() -> bytes:
    """
    Sample resume PDF file for testing.
    
    Returns:
        bytes: Sample PDF file content
    """
    # Read the actual PDF file provided by the user
    import os
    from pathlib import Path
    
    current_dir = Path(__file__).parent
    pdf_path = current_dir / "TestCV.pdf"
    
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            return f.read()
    else:
        # Fallback to a minimal PDF if file not found
        raise FileNotFoundError(f"Test PDF file not found at {pdf_path}")
        
    return pdf_content


def sample_job_postings() -> List[Dict[str, Any]]:
    """
    Sample job postings for testing job matching and aggregation.
    
    Returns:
        List[Dict[str, Any]]: List of sample job postings
    """
    return [
        {
            "id": "job-001",
            "title": "Senior Data Scientist - Remote LATAM",
            "company": "TechCorp International",
            "location": "Remote (Brazil timezone)",
            "salary": "$12,000 - $18,000 USD/month",
            "description": "Join our AI team building ML solutions for global markets. We're looking for a senior data scientist with strong Python and ML experience.",
            "requirements": ["Python", "Machine Learning", "SQL", "TensorFlow", "AWS", "Docker"],
            "posted_date": "2024-01-15",
            "apply_url": "https://techcorp.com/careers/senior-data-scientist",
            "source": "LinkedIn",
            "remote": True,
            "experience_level": "senior",
            "job_type": "full-time"
        },
        {
            "id": "job-002", 
            "title": "ML Engineer - São Paulo",
            "company": "DataBrasil",
            "location": "São Paulo, Brazil",
            "salary": "R$ 8,000 - R$ 12,000/month",
            "description": "We're seeking an ML Engineer to join our growing data team. Experience with Python, scikit-learn, and cloud platforms required.",
            "requirements": ["Python", "scikit-learn", "pandas", "AWS", "MLOps", "Git"],
            "posted_date": "2024-01-12",
            "apply_url": "https://databrasil.com/jobs/ml-engineer",
            "source": "AngelList",
            "remote": False,
            "experience_level": "mid",
            "job_type": "full-time"
        },
        {
            "id": "job-003",
            "title": "Python Data Analyst",
            "company": "Analytics Pro",
            "location": "Remote Brazil",
            "salary": "$6,000 - $10,000 USD/month",
            "description": "Remote opportunity for a Python Data Analyst. Strong SQL and data visualization skills required.",
            "requirements": ["Python", "SQL", "pandas", "matplotlib", "Tableau"],
            "posted_date": "2024-01-10",
            "apply_url": "https://analyticspro.com/careers/data-analyst",
            "source": "RemoteOK",
            "remote": True,
            "experience_level": "mid",
            "job_type": "full-time"
        }
    ]


def sample_user_profile() -> Dict[str, Any]:
    """
    Sample user profile for testing.
    
    Returns:
        Dict[str, Any]: Sample user profile data
    """
    return {
        "id": "user-001",
        "email": "maria.silva@example.com",
        "name": "Maria Silva",
        "location": "São Paulo, Brazil",
        "timezone": "America/Sao_Paulo",
        "experience_level": "mid",
        "skills": [
            "Python", "SQL", "pandas", "Machine Learning", 
            "scikit-learn", "Data Visualization", "Git"
        ],
        "years_experience": 3,
        "salary_min": 8000,
        "salary_max": 15000,
        "currency": "USD",
        "preferred_languages": ["Portuguese", "English"],
        "remote_preference": True,
        "job_types": ["full-time"],
        "industries": ["Technology", "Data Science", "AI/ML"]
    }


def expected_parsed_skills() -> List[str]:
    """
    Expected skills that should be extracted from the sample resume.
    
    Returns:
        List[str]: List of expected skills
    """
    return [
        "Python", "Machine Learning", "SQL", "pandas", "scikit-learn",
        "TensorFlow", "Docker", "Git", "AWS", "Data Visualization",
        "Statistical Analysis", "Data Cleaning", "Model Deployment"
    ]


def expected_job_matches() -> List[Dict[str, Any]]:
    """
    Expected job matches for the sample user profile.
    
    Returns:
        List[Dict[str, Any]]: Expected job matches with scores
    """
    return [
        {
            "job_id": "job-002",
            "match_score": 85,
            "title": "ML Engineer - São Paulo",
            "company": "DataBrasil",
            "matching_skills": ["Python", "scikit-learn", "pandas", "AWS", "Git"],
            "missing_skills": ["MLOps"],
            "salary_match": True,
            "location_match": True,
            "experience_match": True
        },
        {
            "job_id": "job-003",
            "match_score": 78,
            "title": "Python Data Analyst", 
            "company": "Analytics Pro",
            "matching_skills": ["Python", "SQL", "pandas"],
            "missing_skills": ["matplotlib", "Tableau"],
            "salary_match": True,
            "location_match": True,
            "experience_match": True
        },
        {
            "job_id": "job-001",
            "match_score": 72,
            "title": "Senior Data Scientist - Remote LATAM",
            "company": "TechCorp International", 
            "matching_skills": ["Python", "Machine Learning", "SQL", "AWS"],
            "missing_skills": ["TensorFlow", "Docker"],
            "salary_match": True,
            "location_match": True,
            "experience_match": False  # Senior vs Mid level
        }
    ]


def sample_skill_gap_analysis() -> Dict[str, Any]:
    """
    Expected skill gap analysis result.
    
    Returns:
        Dict[str, Any]: Sample skill gap analysis
    """
    return {
        "user_id": "user-001",
        "analysis_date": "2024-01-15",
        "target_jobs": ["job-001", "job-002", "job-003"],
        "missing_skills": [
            {
                "skill": "TensorFlow",
                "importance": 0.85,
                "frequency": 67,  # Appears in 67% of target jobs
                "learning_resources": [
                    "TensorFlow Developer Certificate",
                    "Deep Learning Specialization (Coursera)"
                ]
            },
            {
                "skill": "Docker",
                "importance": 0.78,
                "frequency": 33,
                "learning_resources": [
                    "Docker Mastery Course",
                    "Kubernetes Fundamentals"
                ]
            },
            {
                "skill": "MLOps",
                "importance": 0.72,
                "frequency": 33,
                "learning_resources": [
                    "MLOps Specialization",
                    "AWS Machine Learning"
                ]
            }
        ],
        "recommended_learning_path": [
            {
                "skill": "TensorFlow",
                "priority": 1,
                "estimated_weeks": 4,
                "prerequisites": ["Python", "Machine Learning"]
            },
            {
                "skill": "Docker", 
                "priority": 2,
                "estimated_weeks": 2,
                "prerequisites": ["Linux basics"]
            },
            {
                "skill": "MLOps",
                "priority": 3,
                "estimated_weeks": 6,
                "prerequisites": ["Docker", "AWS"]
            }
        ],
        "improvement_potential": {
            "current_avg_match": 78,
            "projected_avg_match": 92,
            "improvement": 14
        }
    }
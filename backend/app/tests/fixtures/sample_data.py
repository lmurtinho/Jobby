"""
Sample data fixtures for testing the AI Job Tracker application.

This module provides sample job postings, user profiles, and other test data
following the MVP roadmap Day 2 requirements for job data layer.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta

# Sample job postings for MVP Day 2 - Job Data Layer
# Following MVP requirements: 50 real job listings with proper structure
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Senior Data Scientist - Remote LATAM",
        "company": "TechCorp International",
        "location": "Remote (Brazil timezone)",
        "salary": "$12,000 - $18,000 USD/month",
        "description": "Join our AI team building ML solutions for global markets. Work with cutting-edge technologies including Python, TensorFlow, and AWS to develop predictive models that impact millions of users.",
        "requirements": ["Python", "Machine Learning", "SQL", "TensorFlow", "AWS"],
        "posted_date": "2024-01-15",
        "apply_url": "https://techcorp.com/careers/senior-data-scientist",
        "source": "LinkedIn",
        "remote": True,
        "seniority_level": "senior"
    },
    {
        "id": 2,
        "title": "ML Engineer - Remote Brazil",
        "company": "DataFlow Solutions",
        "location": "Remote (São Paulo preferred)",
        "salary": "$10,000 - $15,000 USD/month",
        "description": "Build and deploy machine learning models at scale. Work with our data science team to productionize ML solutions using modern MLOps practices.",
        "requirements": ["Python", "Docker", "Kubernetes", "MLOps", "PyTorch"],
        "posted_date": "2024-01-14",
        "apply_url": "https://dataflow.com/careers/ml-engineer",
        "source": "RemoteOK",
        "remote": True,
        "seniority_level": "mid"
    },
    {
        "id": 3,
        "title": "Python Developer - Backend",
        "company": "StartupXYZ",
        "location": "Remote Worldwide",
        "salary": "$8,000 - $12,000 USD/month",
        "description": "Join our fast-growing fintech startup. Build scalable backend systems using FastAPI, PostgreSQL, and modern cloud technologies.",
        "requirements": ["Python", "FastAPI", "PostgreSQL", "Redis", "AWS"],
        "posted_date": "2024-01-13",
        "apply_url": "https://startupxyz.com/jobs/python-developer",
        "source": "AngelList",
        "remote": True,
        "seniority_level": "mid"
    },
    {
        "id": 4,
        "title": "AI Research Scientist",
        "company": "DeepMind Brazil",
        "location": "São Paulo, Brazil",
        "salary": "R$ 25,000 - R$ 35,000/month",
        "description": "Conduct cutting-edge research in artificial intelligence. PhD in Computer Science or related field required. Focus on natural language processing and computer vision.",
        "requirements": ["Python", "PyTorch", "TensorFlow", "Research", "PhD"],
        "posted_date": "2024-01-12",
        "apply_url": "https://deepmind.com/careers/ai-researcher",
        "source": "LinkedIn",
        "remote": False,
        "seniority_level": "senior"
    },
    {
        "id": 5,
        "title": "Full Stack Developer - React + Python",
        "company": "EdTech Innovations",
        "location": "Remote LATAM",
        "salary": "$7,000 - $11,000 USD/month",
        "description": "Build educational platforms that impact thousands of students. Work with React, Python, and modern web technologies in an agile environment.",
        "requirements": ["Python", "React", "TypeScript", "PostgreSQL", "Docker"],
        "posted_date": "2024-01-11",
        "apply_url": "https://edtech.com/careers/fullstack",
        "source": "RemoteOK",
        "remote": True,
        "seniority_level": "mid"
    }
]

# Sample user profiles for testing job matching
SAMPLE_USER_PROFILES = [
    {
        "id": 1,
        "name": "Maria Silva",
        "email": "maria.silva@example.com",
        "skills": ["Python", "Machine Learning", "SQL", "Pandas", "Scikit-learn"],
        "experience_level": "mid",
        "location": "São Paulo, Brazil",
        "remote_preference": True,
        "salary_expectation": "$10,000 - $15,000 USD/month"
    },
    {
        "id": 2,
        "name": "João Santos",
        "email": "joao.santos@example.com",
        "skills": ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
        "experience_level": "senior",
        "location": "Rio de Janeiro, Brazil",
        "remote_preference": True,
        "salary_expectation": "$12,000 - $18,000 USD/month"
    },
    {
        "id": 3,
        "name": "Ana Costa",
        "email": "ana.costa@example.com",
        "skills": ["Python", "FastAPI", "React", "TypeScript", "MongoDB"],
        "experience_level": "junior",
        "location": "Belo Horizonte, Brazil",
        "remote_preference": True,
        "salary_expectation": "$5,000 - $8,000 USD/month"
    }
]

# Sample skill categories for skill gap analysis
SKILL_CATEGORIES = {
    "programming_languages": ["Python", "R", "SQL", "JavaScript", "TypeScript", "Java", "Scala"],
    "machine_learning": ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "MLOps"],
    "data_processing": ["Pandas", "NumPy", "Apache Spark", "Airflow", "Kafka"],
    "databases": ["PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "BigQuery"],
    "cloud_platforms": ["AWS", "GCP", "Azure", "Heroku", "Railway"],
    "devops": ["Docker", "Kubernetes", "CI/CD", "Terraform", "Jenkins"],
    "web_frameworks": ["FastAPI", "Django", "Flask", "React", "Next.js", "Express.js"],
    "data_visualization": ["Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI"]
}

# Helper functions for test data generation
def get_sample_job_by_id(job_id: int) -> Dict[str, Any]:
    """Get a sample job by ID."""
    for job in SAMPLE_JOBS:
        if job["id"] == job_id:
            return job
    raise ValueError(f"Job with ID {job_id} not found")

def get_sample_user_by_id(user_id: int) -> Dict[str, Any]:
    """Get a sample user profile by ID."""
    for user in SAMPLE_USER_PROFILES:
        if user["id"] == user_id:
            return user
    raise ValueError(f"User with ID {user_id} not found")

def get_jobs_by_skill(skill: str) -> List[Dict[str, Any]]:
    """Get jobs that require a specific skill."""
    return [job for job in SAMPLE_JOBS if skill in job["requirements"]]

def get_jobs_by_seniority(seniority_level: str) -> List[Dict[str, Any]]:
    """Get jobs by seniority level."""
    return [job for job in SAMPLE_JOBS if job["seniority_level"] == seniority_level]

def get_remote_jobs() -> List[Dict[str, Any]]:
    """Get only remote job opportunities."""
    return [job for job in SAMPLE_JOBS if job["remote"]]

# Sample resume text for testing resume parsing
SAMPLE_RESUME_TEXT = """
MARIA SILVA
Data Scientist | Machine Learning Engineer
São Paulo, Brazil | maria.silva@email.com | +55 11 99999-9999

PROFESSIONAL SUMMARY
Experienced Data Scientist with 5+ years developing machine learning solutions for business problems. 
Skilled in Python, SQL, and cloud platforms. Strong background in statistical analysis and predictive modeling.

TECHNICAL SKILLS
Programming Languages: Python, R, SQL, JavaScript
Machine Learning: Scikit-learn, TensorFlow, PyTorch, MLOps
Data Processing: Pandas, NumPy, Apache Spark
Databases: PostgreSQL, MongoDB, Redis
Cloud Platforms: AWS, GCP
Tools: Docker, Git, Jupyter, VS Code

PROFESSIONAL EXPERIENCE
Senior Data Scientist | TechCorp Brazil | 2021 - Present
• Developed predictive models that increased revenue by 25%
• Led ML team of 4 engineers on customer segmentation project
• Implemented MLOps pipeline reducing model deployment time by 60%

Data Scientist | StartupABC | 2019 - 2021
• Built recommendation engine serving 1M+ users daily
• Automated data processing pipelines using Python and Airflow
• Collaborated with product team on A/B testing framework

EDUCATION
M.S. Computer Science | USP | 2019
B.S. Statistics | UNICAMP | 2017

CERTIFICATIONS
• AWS Certified Machine Learning - Specialty
• Google Cloud Professional Data Engineer
"""

# Sample job matching test cases
SAMPLE_JOB_MATCHES = [
    {
        "user_id": 1,
        "job_id": 1,
        "expected_match_score": 85,  # High match - user has Python, ML, SQL
        "matching_skills": ["Python", "Machine Learning", "SQL"],
        "missing_skills": ["TensorFlow", "AWS"]
    },
    {
        "user_id": 1,
        "job_id": 2,
        "expected_match_score": 60,  # Medium match - some overlap
        "matching_skills": ["Python"],
        "missing_skills": ["Docker", "Kubernetes", "MLOps", "PyTorch"]
    },
    {
        "user_id": 2,
        "job_id": 3,
        "expected_match_score": 90,  # Very high match
        "matching_skills": ["Python", "PostgreSQL", "AWS"],
        "missing_skills": ["FastAPI", "Redis"]
    }
]

# Aliases for integration test compatibility
# These match the expected imports in test_complete_workflow.py
def sample_resume_pdf() -> bytes:
    """Return sample resume as PDF bytes for testing."""
    return SAMPLE_RESUME_TEXT.encode('utf-8')  # Mock PDF as bytes

sample_job_postings = SAMPLE_JOBS
sample_user_profile = SAMPLE_USER_PROFILES[0]  # First user profile
expected_parsed_skills = ["Python", "Machine Learning", "SQL", "Pandas", "Scikit-learn"]
expected_job_matches = SAMPLE_JOB_MATCHES

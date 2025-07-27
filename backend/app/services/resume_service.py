"""
ResumeService - PDF text extraction and skill analysis
Minimal implementation to make tests importable (TDD red phase)
"""

from PyPDF2 import PdfReader
from typing import Dict, List, Optional
from io import BytesIO
import re
import logging


class ResumeService:
    """Service for processing resume files and extracting information."""
    
    def __init__(self):
        """Initialize the ResumeService."""
        self.logger = logging.getLogger(__name__)
        self.skill_keywords = [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
            "React", "Vue", "Angular", "Node.js", "Django", "Flask", "FastAPI",
            "Machine Learning", "Deep Learning", "AI", "Data Science", "Analytics",
            "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
            "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Jenkins", "Git",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
            "Linux", "Ubuntu", "REST API", "GraphQL", "Microservices"
        ]
    
    def process_resume(self, file_content: bytes, filename: str) -> Dict:
        """
        Process uploaded resume file and extract structured information.
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            
        Returns:
            Dict containing extracted information
        """
        try:
            # Extract text from PDF
            text = self.extract_text_from_pdf(file_content)
            
            # Extract skills using keyword matching
            skills = self.extract_skills_simple(text)
            
            # Extract basic profile information
            profile_info = self.extract_basic_info(text)
            
            return {
                "skills": skills,
                "experience_level": profile_info.get("experience_level", "mid"),
                "years_experience": profile_info.get("years_experience", 2),
                "name": profile_info.get("name", ""),
                "raw_text": text[:500],  # First 500 chars for debugging
                "parsing_method": "simple_extraction",
                "filename": filename
            }
            
        except Exception as e:
            self.logger.error(f"Resume processing failed: {e}")
            raise ValueError(f"Failed to process resume: {str(e)}")
    
    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text content from PDF file."""
        try:
            pdf_file = BytesIO(file_content)
            reader = PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            raise ValueError(f"PDF text extraction failed: {str(e)}")
    
    def extract_skills_simple(self, text: str) -> List[str]:
        """Extract skills from text using keyword matching."""
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skill_keywords:
            # Use word boundaries to avoid partial matches
            skill_pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(skill_pattern, text_lower):
                found_skills.append(skill)
        
        # Special handling for SQL databases - if we find specific SQL databases, also include SQL
        sql_databases = ["PostgreSQL", "MySQL", "MongoDB"]  # MongoDB is NoSQL but often grouped with database skills
        if any(db in found_skills for db in sql_databases):
            if "SQL" not in found_skills:
                found_skills.append("SQL")
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def extract_basic_info(self, text: str) -> Dict:
        """Extract basic information like name and experience level."""
        info = {}
        
        # Extract name (simple heuristic - first line that looks like a name)
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if len(line.split()) == 2 and all(word.isalpha() for word in line.split()):
                info["name"] = line
                break
        
        # Extract years of experience (enhanced pattern matching)
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*anos?\s*de\s*experiência',
            r'experience:?\s*(\d+)\+?\s*years?'
        ]
        
        years_experience = 2  # default
        
        # First try explicit year mentions
        for pattern in experience_patterns:
            match = re.search(pattern, text.lower())
            if match:
                years_experience = int(match.group(1))
                break
        else:
            # If no explicit years, try to calculate from date ranges
            # Look for patterns like "Sep 2023 | Jun 2025" or "Aug 2022 | Aug 2023"
            date_ranges = re.findall(r'(\w+)\s+(\d{4})\s*\|\s*(\w+)\s+(\d{4})', text)
            if date_ranges:
                total_months = 0
                month_map = {
                    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
                }
                
                for start_month, start_year, end_month, end_year in date_ranges:
                    try:
                        start_y = int(start_year)
                        end_y = int(end_year)
                        start_m = month_map.get(start_month.lower()[:3], 1)
                        end_m = month_map.get(end_month.lower()[:3], 12)
                        
                        # Calculate months between dates
                        months = (end_y - start_y) * 12 + (end_m - start_m)
                        if months > 0:
                            total_months += months
                    except (ValueError, KeyError):
                        continue
                
                if total_months > 0:
                    years_experience = max(2, round(total_months / 12))  # At least 2 years, rounded
        
        info["years_experience"] = years_experience
        
        # Determine experience level based on years
        if years_experience < 2:
            info["experience_level"] = "junior"
        elif years_experience <= 5:
            info["experience_level"] = "mid" 
        else:
            info["experience_level"] = "senior"
        
        return info

"""
LinkedIn job scraper.

Scrapes job listings from LinkedIn using web scraping techniques.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

from .base_scraper import BaseScraper


class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn job listings."""
    
    def __init__(self):
        """Initialize the LinkedIn scraper."""
        super().__init__()
        self.base_url = "https://www.linkedin.com"
        self.jobs_url = "https://www.linkedin.com/jobs/search"
        self.rate_limit_delay = 2.0  # LinkedIn requires slower scraping
        
        # Common headers to appear more like a real browser
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    
    @property
    def source_name(self) -> str:
        """Return the source name."""
        return "linkedin"
    
    def scrape_jobs(self, keywords: Optional[List[str]] = None, location: str = "Remote", 
                   limit: int = 25, **kwargs) -> List[Dict[str, Any]]:
        """
        Scrape jobs from LinkedIn.
        
        Args:
            keywords: List of keywords to search for
            location: Location to search in
            limit: Maximum number of jobs to return
            
        Returns:
            List of job dictionaries
        """
        try:
            # Build search parameters
            params = {
                "keywords": " ".join(keywords) if keywords else "Python Data Science",
                "location": location,
                "f_JT": "F"  # Full-time jobs
            }
            
            self.logger.info(f"Scraping LinkedIn jobs with params: {params}")
            
            # Make request
            response = requests.get(self.jobs_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse jobs from HTML
            jobs = self._parse_job_listings(response.text)
            
            # Normalize and validate jobs
            normalized_jobs = []
            for job in jobs[:limit]:
                normalized = self.normalize_job_data(job)
                if self.validate_job_data(normalized):
                    normalized_jobs.append(normalized)
                
                # Apply rate limiting
                self._apply_rate_limit()
            
            self.logger.info(f"Successfully scraped {len(normalized_jobs)} LinkedIn jobs")
            return normalized_jobs
            
        except Exception as e:
            self.logger.error(f"LinkedIn scraping failed: {e}")
            return []
    
    def _parse_job_listings(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Parse job listings from LinkedIn HTML.
        
        Args:
            html_content: Raw HTML content from LinkedIn
            
        Returns:
            List of raw job data dictionaries
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            jobs = []
            
            # Find job listing containers (LinkedIn's structure)
            job_cards = soup.find_all('div', class_='job-search-card') or soup.find_all('li', class_='result-card')
            
            for card in job_cards:
                try:
                    job_data = self._extract_job_from_card(card)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    self.logger.warning(f"Failed to parse job card: {e}")
                    continue
            
            return jobs
            
        except Exception as e:
            self.logger.error(f"HTML parsing failed: {e}")
            return []
    
    def _extract_job_from_card(self, card) -> Optional[Dict[str, Any]]:
        """Extract job data from a single job card."""
        try:
            # Extract title
            title_elem = card.find('h3') or card.find('a', class_='result-card__full-card-link')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            
            # Extract company
            company_elem = card.find('h4') or card.find('a', class_='result-card__subtitle-link')
            company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
            
            # Extract location
            location_elem = card.find('span', class_='job-search-card__location') or card.find('span', class_='result-card__location')
            location = location_elem.get_text(strip=True) if location_elem else "Unknown Location"
            
            # Extract apply URL
            link_elem = card.find('a', class_='result-card__full-card-link') or card.find('a')
            apply_url = link_elem.get('href') if link_elem else ""
            if apply_url and not apply_url.startswith('http'):
                apply_url = self.base_url + apply_url
            
            # Extract description (if available)
            desc_elem = card.find('span', class_='job-search-card__snippet')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "apply_url": apply_url or f"{self.base_url}/jobs",
                "description": description,
                "requirements": self._extract_requirements_from_text(title + " " + description),
                "posted_date": datetime.now().strftime("%Y-%m-%d")
            }
            
        except Exception as e:
            self.logger.warning(f"Failed to extract job data: {e}")
            return None
    
    def _extract_requirements_from_text(self, text: str) -> List[str]:
        """Extract skill requirements from job text."""
        # Common tech skills to look for
        skills = [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
            "React", "Vue", "Angular", "Node.js", "Django", "Flask", "FastAPI",
            "Machine Learning", "Deep Learning", "AI", "Data Science", "Analytics",
            "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
            "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Jenkins", "Git",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def normalize_job_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw LinkedIn job data to standard format."""
        # Handle requirements - convert string to list if needed
        requirements = raw_data.get("requirements", [])
        if isinstance(requirements, str):
            requirements = [req.strip() for req in requirements.split(',') if req.strip()]
        
        normalized = {
            "title": raw_data.get("title", "").strip(),
            "company": raw_data.get("company", "").strip(),
            "location": raw_data.get("location", "").strip(),
            "salary": raw_data.get("salary", ""),
            "description": raw_data.get("description", ""),
            "requirements": requirements,
            "apply_url": raw_data.get("apply_url", ""),
            "posted_date": raw_data.get("posted_date", datetime.now().strftime("%Y-%m-%d"))
        }
        
        # Add metadata
        return self._add_metadata(normalized)

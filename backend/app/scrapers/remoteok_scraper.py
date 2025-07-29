"""
RemoteOK job scraper.

Scrapes remote job listings from RemoteOK using their API.
"""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

from .base_scraper import BaseScraper


class RemoteOKScraper(BaseScraper):
    """Scraper for RemoteOK job listings."""
    
    def __init__(self):
        """Initialize the RemoteOK scraper."""
        super().__init__()
        self.api_base_url = "https://remoteok.io/api"
        self.rate_limit_delay = 1.0  # RemoteOK API rate limit
        
        # API headers
        self.headers = {
            "User-Agent": "JobbyApp/1.0 (AI Job Tracker)",
            "Accept": "application/json"
        }
    
    @property
    def source_name(self) -> str:
        """Return the source name."""
        return "remoteok"
    
    def scrape_jobs(self, keywords: Optional[List[str]] = None, remote_only: bool = True,
                   limit: int = 50, **kwargs) -> List[Dict[str, Any]]:
        """
        Scrape jobs from RemoteOK API.
        
        Args:
            keywords: List of keywords to filter by
            remote_only: Only return remote jobs
            limit: Maximum number of jobs to return
            
        Returns:
            List of job dictionaries
        """
        try:
            self.logger.info("Scraping RemoteOK jobs via API")
            
            # RemoteOK API endpoint
            url = f"{self.api_base_url}"
            
            # Make API request
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse JSON response (RemoteOK API returns array)
            jobs_data = response.json()
            
            # Skip first element (metadata) and filter jobs
            raw_jobs = jobs_data[1:] if isinstance(jobs_data, list) and len(jobs_data) > 1 else []
            
            # Filter by keywords if provided
            if keywords:
                raw_jobs = self._filter_jobs_by_keywords(raw_jobs, keywords)
            
            # Normalize and validate jobs
            normalized_jobs = []
            for job in raw_jobs[:limit]:
                normalized = self.normalize_job_data(job)
                if self.validate_job_data(normalized):
                    normalized_jobs.append(normalized)
            
            self.logger.info(f"Successfully scraped {len(normalized_jobs)} RemoteOK jobs")
            return normalized_jobs
            
        except Exception as e:
            self.logger.error(f"RemoteOK scraping failed: {e}")
            return []
    
    def _filter_jobs_by_keywords(self, jobs: List[Dict[str, Any]], 
                                keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Filter jobs by keywords.
        
        Args:
            jobs: List of raw job data
            keywords: Keywords to filter by
            
        Returns:
            Filtered list of jobs
        """
        filtered_jobs = []
        keywords_lower = [k.lower() for k in keywords]
        
        for job in jobs:
            # Check title, description, and tags
            job_text = " ".join([
                job.get("position", ""),
                job.get("description", ""),
                " ".join(job.get("tags", []))
            ]).lower()
            
            # Check if any keyword matches
            if any(keyword in job_text for keyword in keywords_lower):
                filtered_jobs.append(job)
        
        return filtered_jobs
    
    def normalize_job_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw RemoteOK job data to standard format."""
        # Extract requirements from tags
        requirements = raw_data.get("tags", [])
        if isinstance(requirements, list):
            requirements = [tag for tag in requirements if isinstance(tag, str)]
        
        # Build apply URL
        apply_url = raw_data.get("url", "")
        if not apply_url.startswith("http"):
            job_id = raw_data.get("id", "")
            apply_url = f"https://remoteok.io/remote-jobs/{job_id}"
        
        # Parse salary
        salary = ""
        if raw_data.get("salary_min") and raw_data.get("salary_max"):
            salary = f"${raw_data['salary_min']:,}-{raw_data['salary_max']:,}/year"
        elif raw_data.get("salary"):
            salary = raw_data["salary"]
        
        # Parse posted date
        posted_date = raw_data.get("date", "")
        if posted_date:
            try:
                # Convert timestamp to date string
                if isinstance(posted_date, (int, float)):
                    posted_date = datetime.fromtimestamp(posted_date).strftime("%Y-%m-%d")
                elif isinstance(posted_date, str) and "T" in posted_date:
                    posted_date = datetime.fromisoformat(posted_date.replace("Z", "+00:00")).strftime("%Y-%m-%d")
            except:
                posted_date = datetime.now().strftime("%Y-%m-%d")
        else:
            posted_date = datetime.now().strftime("%Y-%m-%d")
        
        normalized = {
            "title": raw_data.get("position", raw_data.get("title", "")).strip(),
            "company": raw_data.get("company", "").strip(),
            "location": raw_data.get("location", "Remote").strip(),
            "salary": salary,
            "description": raw_data.get("description", ""),
            "requirements": requirements,
            "apply_url": apply_url,
            "posted_date": posted_date,
            "job_type": "Full-time"  # Default to Full-time for RemoteOK jobs
        }
        
        # Add metadata
        return self._add_metadata(normalized)

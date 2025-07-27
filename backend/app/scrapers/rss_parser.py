"""
RSS feed parser for job listings.

Parses job listings from various RSS feeds.
"""

import feedparser
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

from .base_scraper import BaseScraper


class RSSParser(BaseScraper):
    """Parser for RSS job feeds."""
    
    def __init__(self):
        """Initialize the RSS parser."""
        super().__init__()
        self.rate_limit_delay = 0.5  # Faster for RSS feeds
        
        # List of RSS feed URLs to parse
        self.feed_urls = [
            "https://jobs.github.com/positions.rss",
            "https://remoteok.io/remote-jobs.rss",
            "https://stackoverflow.com/jobs/feed",
            # Add more RSS feeds as needed
        ]
        
        # Headers for HTTP requests
        self.headers = {
            "User-Agent": "JobbyApp/1.0 RSS Parser"
        }
    
    @property
    def source_name(self) -> str:
        """Return the source name."""
        return "rss_feed"
    
    def scrape_jobs(self, **kwargs) -> List[Dict[str, Any]]:
        """Alias for parse_feeds to maintain interface consistency."""
        return self.parse_feeds(**kwargs)
    
    def parse_feeds(self, feed_urls: Optional[List[str]] = None, 
                   limit_per_feed: int = 10, **kwargs) -> List[Dict[str, Any]]:
        """
        Parse job listings from RSS feeds.
        
        Args:
            feed_urls: Optional list of RSS feed URLs to parse
            limit_per_feed: Maximum jobs per feed
            
        Returns:
            List of job dictionaries
        """
        urls_to_parse = feed_urls or self.feed_urls
        all_jobs = []
        
        for feed_url in urls_to_parse:
            try:
                self.logger.info(f"Parsing RSS feed: {feed_url}")
                
                # Parse the RSS feed
                feed = feedparser.parse(feed_url)
                
                # Extract jobs from feed entries
                jobs = self._extract_jobs_from_feed(feed, limit_per_feed)
                all_jobs.extend(jobs)
                
                # Apply rate limiting
                self._apply_rate_limit()
                
            except Exception as e:
                self.logger.error(f"Failed to parse RSS feed {feed_url}: {e}")
                continue
        
        self.logger.info(f"Successfully parsed {len(all_jobs)} jobs from RSS feeds")
        return all_jobs
    
    def _extract_jobs_from_feed(self, feed, limit: int) -> List[Dict[str, Any]]:
        """Extract job data from RSS feed entries."""
        jobs = []
        
        for entry in feed.entries[:limit]:
            try:
                job_data = self._extract_job_from_entry(entry)
                if job_data:
                    normalized = self.normalize_job_data(job_data)
                    if self.validate_job_data(normalized):
                        jobs.append(normalized)
            except Exception as e:
                self.logger.warning(f"Failed to extract job from RSS entry: {e}")
                continue
        
        return jobs
    
    def _extract_job_from_entry(self, entry) -> Optional[Dict[str, Any]]:
        """Extract job data from a single RSS entry."""
        try:
            # Extract basic fields
            title = getattr(entry, 'title', '')
            description = getattr(entry, 'description', '') or getattr(entry, 'summary', '')
            link = getattr(entry, 'link', '')
            
            # Parse published date
            published = getattr(entry, 'published_parsed', None)
            if published:
                posted_date = datetime(*published[:6]).strftime("%Y-%m-%d")
            else:
                posted_date = datetime.now().strftime("%Y-%m-%d")
            
            # Extract company and location from title or description
            company, location = self._parse_company_and_location(title, description)
            
            # Extract requirements from description
            requirements = self._extract_requirements_from_description(description)
            
            # Extract salary if present
            salary = self._parse_salary_from_description(description)
            
            return {
                "title": title.strip(),
                "company": company,
                "location": location,
                "description": description.strip(),
                "requirements": requirements,
                "apply_url": link,
                "salary": salary,
                "posted_date": posted_date
            }
            
        except Exception as e:
            self.logger.warning(f"Failed to extract RSS entry data: {e}")
            return None
    
    def _parse_company_and_location(self, title: str, description: str) -> tuple:
        """Parse company name and location from title/description."""
        company = "Unknown Company"
        location = "Remote"
        
        # Common patterns for extracting company from title
        # "Software Engineer at TechCorp"
        at_match = re.search(r'\s+at\s+([^,\-\|]+)', title, re.IGNORECASE)
        if at_match:
            company = at_match.group(1).strip()
        
        # "TechCorp - Software Engineer"
        dash_match = re.search(r'^([^-]+)\s*-\s*', title)
        if dash_match and not at_match:
            potential_company = dash_match.group(1).strip()
            # Check if it looks like a company name (not a job title)
            if not any(word in potential_company.lower() for word in ['engineer', 'developer', 'analyst', 'manager']):
                company = potential_company
        
        # Try to extract location
        location_patterns = [
            r'Location:\s*([^,\n]+)',
            r'in\s+([A-Za-z\s]+(?:,\s*[A-Za-z]{2,}))',
            r'Remote[\s\-]*([A-Za-z\s]+)',
            r'([A-Za-z\s]+,\s*[A-Z]{2,3})'
        ]
        
        text = title + " " + description
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                break
        
        return company, location
    
    def _extract_requirements_from_description(self, description: str) -> List[str]:
        """Extract skill requirements from job description."""
        # Common tech skills to look for
        skills = [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
            "React", "Vue", "Angular", "Node.js", "Django", "Flask", "FastAPI",
            "Machine Learning", "Deep Learning", "AI", "Data Science", "Analytics",
            "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
            "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Jenkins", "Git",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
            "Tableau", "Excel", "PowerBI", "R", "Scala", "Spark"
        ]
        
        found_skills = []
        description_lower = description.lower()
        
        for skill in skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            match = re.search(pattern, description_lower)
            if match:
                # Find the actual text in the original description to preserve case
                start_pos = match.start()
                end_pos = match.end()
                
                # Get words around the match position to find the exact text
                words = description.split()
                for word in words:
                    if word.lower().strip(',.!?;:') == skill.lower():
                        found_skills.append(word.strip(',.!?;:'))
                        break
                else:
                    # Fallback to the canonical form
                    found_skills.append(skill)
        
        return found_skills
    
    def _parse_salary_from_description(self, description: str) -> str:
        """Extract salary information from description."""
        # Salary patterns
        salary_patterns = [
            r'salary[:\s]*([£$€R\s]*[\d,]+k?[\s]*[-–to]*[\s]*[£$€R\s]*[\d,]+k?[/\s]*(?:year|month|hour|annually|monthly|hourly)?)',
            r'compensation[:\s]*([£$€R\s]*[\d,]+k?[\s]*[-–to]*[\s]*[£$€R\s]*[\d,]+k?)',
            r'pay[:\s]*([£$€R\s]*[\d,]+k?[\s]*[-–to]*[\s]*[£$€R\s]*[\d,]+k?)',
            r'([£$€R]\s*[\d,]+k?[\s]*[-–to]*[\s]*[£$€R\s]*[\d,]+k?[/\s]*(?:year|month|hour)?)',
            r'(R\$\s*[\d,.]+[\s]*[-–to]*[\s]*R\$\s*[\d,.]+[/\s]*(?:mês|month)?)',
            r'([\d,]+k[\s]*[-–to]*[\s]*[\d,]+k[\s]*(?:annually|yearly|per year)?)'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def normalize_job_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw RSS job data to standard format."""
        normalized = {
            "title": raw_data.get("title", "").strip(),
            "company": raw_data.get("company", "Unknown Company").strip(),
            "location": raw_data.get("location", "Remote").strip(),
            "salary": raw_data.get("salary", ""),
            "description": raw_data.get("description", ""),
            "requirements": raw_data.get("requirements", []),
            "apply_url": raw_data.get("apply_url", ""),
            "posted_date": raw_data.get("posted_date", datetime.now().strftime("%Y-%m-%d"))
        }
        
        # Add metadata
        return self._add_metadata(normalized)

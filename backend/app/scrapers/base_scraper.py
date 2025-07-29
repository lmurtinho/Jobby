"""
Base scraper class for job scraping infrastructure.

Provides common functionality and interface for all job scrapers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import time
import logging
from datetime import datetime


class BaseScraper(ABC):
    """Abstract base class for job scrapers."""
    
    def __init__(self):
        """Initialize the base scraper."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rate_limit_delay = 1.0  # Default 1 second between requests
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the name of the job source."""
        pass
    
    @abstractmethod
    def scrape_jobs(self, **kwargs) -> List[Dict[str, Any]]:
        """Scrape jobs from the source."""
        pass
    
    @abstractmethod
    def normalize_job_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw job data to standard format."""
        pass
    
    def validate_job_data(self, job_data: Dict[str, Any]) -> bool:
        """Validate that job data contains required fields."""
        required_fields = ["title", "company", "location", "apply_url"]
        
        try:
            for field in required_fields:
                if field not in job_data or not job_data[field]:
                    self.logger.warning(f"Missing required field: {field}")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False
    
    def _apply_rate_limit(self):
        """Apply rate limiting between requests."""
        time.sleep(self.rate_limit_delay)
    
    def _add_metadata(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add common metadata to job data."""
        job_data["source"] = self.source_name
        job_data["scraped_at"] = datetime.utcnow().isoformat()
        return job_data

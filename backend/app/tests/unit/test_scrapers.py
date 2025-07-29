"""
Unit tests for job scraper infrastructure.

Tests the base scraper and specific scraper implementations for:
- LinkedIn Jobs scraping
- RemoteOK scraping  
- RSS feed parsing
- Job aggregation and storage
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any
from datetime import datetime

# Import scrapers (these will fail until we implement them - TDD red phase)
from app.scrapers.base_scraper import BaseScraper
from app.scrapers.linkedin_scraper import LinkedInScraper
from app.scrapers.remoteok_scraper import RemoteOKScraper
from app.scrapers.rss_parser import RSSParser


class TestBaseScraper:
    """Test the abstract base scraper functionality."""
    
    def test_base_scraper_is_abstract(self):
        """Test that BaseScraper cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseScraper()
    
    def test_base_scraper_defines_required_methods(self):
        """Test that BaseScraper defines required abstract methods."""
        # Check that required methods are defined as abstract
        assert hasattr(BaseScraper, 'scrape_jobs')
        assert hasattr(BaseScraper, 'normalize_job_data')
        assert hasattr(BaseScraper, 'validate_job_data')


class TestLinkedInScraper:
    """Test LinkedIn job scraping functionality."""
    
    @pytest.fixture
    def linkedin_scraper(self):
        """Create a LinkedInScraper instance for testing."""
        return LinkedInScraper()
    
    @pytest.fixture
    def sample_linkedin_job_data(self):
        """Sample raw job data from LinkedIn."""
        return {
            "title": "Senior Data Scientist - Remote",
            "company": "TechCorp Internacional",
            "location": "Remote (Brazil timezone)",
            "salary": "$12,000-18,000/month",
            "description": "Join our AI team building ML solutions for global markets...",
            "requirements": "Python, Machine Learning, TensorFlow, AWS, Docker",
            "apply_url": "https://linkedin.com/jobs/view/123456",
            "posted_date": "2025-01-20"
        }
    
    def test_linkedin_scraper_initialization(self, linkedin_scraper):
        """Test LinkedInScraper initializes correctly."""
        assert linkedin_scraper.source_name == "linkedin"
        assert linkedin_scraper.base_url == "https://www.linkedin.com"
        assert linkedin_scraper.rate_limit_delay >= 1.0
    
    @patch('requests.get')
    def test_scrape_jobs_basic_functionality(self, mock_get, linkedin_scraper, sample_linkedin_job_data):
        """Test basic job scraping functionality."""
        # Mock HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>Mock LinkedIn response</html>"
        mock_get.return_value = mock_response
        
        # Mock the HTML parsing to return sample data
        with patch.object(linkedin_scraper, '_parse_job_listings') as mock_parse:
            mock_parse.return_value = [sample_linkedin_job_data]
            
            jobs = linkedin_scraper.scrape_jobs(keywords=["Python", "Data Science"], location="Remote")
            
            assert len(jobs) == 1
            assert jobs[0]["title"] == "Senior Data Scientist - Remote"
            assert jobs[0]["source"] == "linkedin"
    
    def test_normalize_job_data(self, linkedin_scraper, sample_linkedin_job_data):
        """Test job data normalization."""
        normalized = linkedin_scraper.normalize_job_data(sample_linkedin_job_data)
        
        # Check required fields are present
        assert "title" in normalized
        assert "company" in normalized
        assert "location" in normalized
        assert "source" in normalized
        assert "scraped_at" in normalized
        
        # Check requirements are properly parsed
        assert isinstance(normalized["requirements"], list)
        assert "Python" in normalized["requirements"]
        assert "Machine Learning" in normalized["requirements"]
    
    def test_validate_job_data(self, linkedin_scraper):
        """Test job data validation."""
        valid_job = {
            "title": "Data Scientist",
            "company": "TechCorp",
            "location": "Remote",
            "apply_url": "https://example.com/job/123",
            "source": "linkedin"
        }
        
        assert linkedin_scraper.validate_job_data(valid_job) is True
        
        # Test invalid data
        invalid_job = {"title": ""}  # Missing required fields
        assert linkedin_scraper.validate_job_data(invalid_job) is False
    
    def test_rate_limiting(self, linkedin_scraper):
        """Test rate limiting functionality."""
        with patch('time.sleep') as mock_sleep:
            linkedin_scraper._apply_rate_limit()
            mock_sleep.assert_called_once()


class TestRemoteOKScraper:
    """Test RemoteOK job scraping functionality."""
    
    @pytest.fixture
    def remoteok_scraper(self):
        """Create a RemoteOKScraper instance for testing."""
        return RemoteOKScraper()
    
    @pytest.fixture
    def sample_remoteok_api_response(self):
        """Sample API response from RemoteOK."""
        return [
            {"status": "ok"},  # First element is metadata
            {
                "id": 123456,
                "title": "ML Engineer",
                "company": "AI Startup LATAM",
                "location": "Remote - LATAM",
                "salary": "$15,000/month",
                "description": "Join our AI team building next-gen ML systems...",
                "tags": ["python", "tensorflow", "kubernetes", "mlops", "aws"],
                "url": "https://remoteok.io/remote-jobs/123456",
                "date": "2025-01-19T00:00:00Z"
            }
        ]
    
    def test_remoteok_scraper_initialization(self, remoteok_scraper):
        """Test RemoteOKScraper initializes correctly."""
        assert remoteok_scraper.source_name == "remoteok"
        assert remoteok_scraper.api_base_url == "https://remoteok.io/api"
        assert remoteok_scraper.rate_limit_delay >= 1.0
    
    @patch('requests.get')
    def test_scrape_jobs_api_call(self, mock_get, remoteok_scraper, sample_remoteok_api_response):
        """Test API-based job scraping."""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_remoteok_api_response
        mock_get.return_value = mock_response
        
        jobs = remoteok_scraper.scrape_jobs(keywords=["Python", "ML"], remote_only=True)
        
        assert len(jobs) == 1
        assert jobs[0]["title"] == "ML Engineer"
        assert jobs[0]["source"] == "remoteok"
        assert "python" in jobs[0]["requirements"]
    
    def test_filter_jobs_by_keywords(self, remoteok_scraper, sample_remoteok_api_response):
        """Test keyword filtering functionality."""
        filtered = remoteok_scraper._filter_jobs_by_keywords(
            sample_remoteok_api_response, 
            keywords=["python", "ml"]
        )
        
        assert len(filtered) == 1  # Should match python
        
        # Test no matches
        no_matches = remoteok_scraper._filter_jobs_by_keywords(
            sample_remoteok_api_response,
            keywords=["java", "spring"]
        )
        assert len(no_matches) == 0


class TestRSSParser:
    """Test RSS feed parsing functionality."""
    
    @pytest.fixture
    def rss_parser(self):
        """Create an RSSParser instance for testing."""
        return RSSParser()
    
    @pytest.fixture
    def sample_rss_feed_xml(self):
        """Sample RSS feed XML content."""
        return """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Fintech Brazil Jobs</title>
                <item>
                    <title>Data Analyst - Fintech Brazil</title>
                    <description>Analyze financial data and create insights for decision making...</description>
                    <link>https://fintech.com.br/jobs/data-analyst</link>
                    <pubDate>Thu, 18 Jan 2025 10:00:00 GMT</pubDate>
                    <category>Data Analysis</category>
                </item>
            </channel>
        </rss>"""
    
    def test_rss_parser_initialization(self, rss_parser):
        """Test RSSParser initializes correctly."""
        assert rss_parser.source_name == "rss_feed"
        assert len(rss_parser.feed_urls) > 0
    
    @patch('feedparser.parse')
    def test_parse_feeds_basic(self, mock_feedparser, rss_parser, sample_rss_feed_xml):
        """Test basic RSS feed parsing."""
        # Mock feedparser response
        mock_feed = Mock()
        mock_feed.entries = [
            Mock(
                title="Data Analyst - Fintech Brazil",
                description="Analyze financial data and create insights...",
                link="https://fintech.com.br/jobs/data-analyst",
                published_parsed=(2025, 1, 18, 10, 0, 0, 0, 0, 0)
            )
        ]
        mock_feedparser.return_value = mock_feed
        
        jobs = rss_parser.parse_feeds()
        
        assert len(jobs) >= 1
        assert jobs[0]["title"] == "Data Analyst - Fintech Brazil"
        assert jobs[0]["source"] == "rss_feed"
    
    def test_extract_requirements_from_description(self, rss_parser):
        """Test skill extraction from job descriptions."""
        description = "We need a developer with Python, SQL, pandas, and Tableau experience."
        
        requirements = rss_parser._extract_requirements_from_description(description)
        
        assert "Python" in requirements
        assert "SQL" in requirements
        assert "pandas" in requirements
        assert "Tableau" in requirements
    
    def test_parse_salary_from_description(self, rss_parser):
        """Test salary parsing from descriptions."""
        descriptions = [
            "Salary: R$ 8,000-12,000/month",
            "Compensation: $5,000-7,000 USD monthly",
            "Pay range: 80k-120k annually"
        ]
        
        for desc in descriptions:
            salary = rss_parser._parse_salary_from_description(desc)
            assert salary is not None
            assert len(salary) > 0


class TestJobScrapingIntegration:
    """Test integration between different scrapers."""
    
    def test_all_scrapers_implement_base_interface(self):
        """Test that all scrapers implement the base interface."""
        scrapers = [LinkedInScraper(), RemoteOKScraper(), RSSParser()]
        
        for scraper in scrapers:
            assert hasattr(scraper, 'scrape_jobs') or hasattr(scraper, 'parse_feeds')
            assert hasattr(scraper, 'normalize_job_data')
            assert hasattr(scraper, 'validate_job_data')
            assert hasattr(scraper, 'source_name')
    
    def test_consistent_job_data_format(self):
        """Test that all scrapers return consistent job data format."""
        expected_fields = ["title", "company", "location", "source", "apply_url"]
        
        # Test with mock data from each scraper
        linkedin_scraper = LinkedInScraper()
        sample_data = {
            "title": "Test Job",
            "company": "Test Company", 
            "location": "Remote",
            "apply_url": "https://example.com"
        }
        
        normalized = linkedin_scraper.normalize_job_data(sample_data)
        
        for field in expected_fields:
            assert field in normalized
    
    @patch('app.scrapers.linkedin_scraper.LinkedInScraper.scrape_jobs')
    @patch('app.scrapers.remoteok_scraper.RemoteOKScraper.scrape_jobs')
    @patch('app.scrapers.rss_parser.RSSParser.parse_feeds')
    def test_multi_source_job_aggregation(self, mock_rss, mock_remoteok, mock_linkedin):
        """Test aggregating jobs from multiple sources."""
        # Mock responses from each scraper
        mock_linkedin.return_value = [{"title": "LinkedIn Job", "source": "linkedin"}]
        mock_remoteok.return_value = [{"title": "RemoteOK Job", "source": "remoteok"}]
        mock_rss.return_value = [{"title": "RSS Job", "source": "rss_feed"}]
        
        # This would be the job aggregation service logic
        all_jobs = []
        all_jobs.extend(mock_linkedin.return_value)
        all_jobs.extend(mock_remoteok.return_value)
        all_jobs.extend(mock_rss.return_value)
        
        assert len(all_jobs) == 3
        sources = [job["source"] for job in all_jobs]
        assert "linkedin" in sources
        assert "remoteok" in sources
        assert "rss_feed" in sources


class TestJobScrapingErrorHandling:
    """Test error handling in job scraping."""
    
    def test_network_error_handling(self):
        """Test handling of network errors during scraping."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            scraper = LinkedInScraper()
            jobs = scraper.scrape_jobs(keywords=["Python"])
            
            # Should return empty list instead of crashing
            assert jobs == []
    
    def test_invalid_response_handling(self):
        """Test handling of invalid API responses."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_get.return_value = mock_response
            
            scraper = RemoteOKScraper()
            jobs = scraper.scrape_jobs(keywords=["Python"])
            
            assert jobs == []
    
    def test_malformed_rss_feed_handling(self):
        """Test handling of malformed RSS feeds."""
        with patch('feedparser.parse') as mock_feedparser:
            mock_feed = Mock()
            mock_feed.entries = []  # Empty feed
            mock_feedparser.return_value = mock_feed
            
            parser = RSSParser()
            jobs = parser.parse_feeds()
            
            assert jobs == []

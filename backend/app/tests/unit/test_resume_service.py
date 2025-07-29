"""
Unit tests for ResumeService - PDF text extraction and skill analysis
Tests PDF processing, skill extraction, error handling, and validation
Following TDD approach for Issue #29
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from io import BytesIO
from typing import Dict, List

from app.services.resume_service import ResumeService


class TestResumeServiceInitialization:
    """Test ResumeService initialization and basic setup."""
    
    def test_resume_service_initialization(self):
        """Test that ResumeService initializes correctly."""
        service = ResumeService()
        assert service is not None
        assert hasattr(service, 'skill_keywords')
        assert hasattr(service, 'logger')
        assert isinstance(service.skill_keywords, list)
        assert len(service.skill_keywords) > 0

    def test_skill_keywords_contains_expected_technologies(self):
        """Test that skill keywords include common tech skills."""
        service = ResumeService()
        expected_skills = [
            "Python", "JavaScript", "React", "SQL", "Machine Learning",
            "Docker", "AWS", "FastAPI", "Git"
        ]
        
        for skill in expected_skills:
            assert skill in service.skill_keywords, f"Missing skill: {skill}"

    def test_skill_keywords_are_strings(self):
        """Test that all skill keywords are strings."""
        service = ResumeService()
        for skill in service.skill_keywords:
            assert isinstance(skill, str), f"Skill {skill} is not a string"
            assert len(skill) > 0, f"Empty skill found"


class TestPDFTextExtraction:
    """Test PDF text extraction functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ResumeService()
        self.sample_pdf_text = """
        John Doe
        Senior Software Engineer
        
        Experience:
        - 5 years of experience in Python development
        - Expert in React and JavaScript
        - Machine Learning and AI projects
        - AWS cloud infrastructure
        - PostgreSQL database design
        
        Skills: Python, React, JavaScript, Machine Learning, AWS, PostgreSQL, Docker, Git
        """

    @patch('app.services.resume_service.PdfReader')
    def test_extract_text_from_pdf_success(self, mock_pdf_reader):
        """Test successful PDF text extraction."""
        # Arrange
        mock_page = Mock()
        mock_page.extract_text.return_value = self.sample_pdf_text
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        file_content = b"fake pdf content"
        
        # Act
        result = self.service.extract_text_from_pdf(file_content)
        
        # Assert
        assert result == self.sample_pdf_text.strip()
        mock_pdf_reader.assert_called_once()
        mock_page.extract_text.assert_called_once()

    @patch('app.services.resume_service.PdfReader')
    def test_extract_text_from_pdf_multiple_pages(self, mock_pdf_reader):
        """Test PDF text extraction with multiple pages."""
        # Arrange
        page1_text = "John Doe\nSoftware Engineer"
        page2_text = "Experience: Python, React"
        
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = page1_text
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = page2_text
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page1, mock_page2]
        mock_pdf_reader.return_value = mock_reader_instance
        
        file_content = b"fake pdf content"
        
        # Act
        result = self.service.extract_text_from_pdf(file_content)
        
        # Assert
        expected_text = f"{page1_text}\n{page2_text}".strip()
        assert result == expected_text
        assert mock_page1.extract_text.call_count == 1
        assert mock_page2.extract_text.call_count == 1

    @patch('app.services.resume_service.PdfReader')
    def test_extract_text_from_pdf_corrupted_file(self, mock_pdf_reader):
        """Test PDF text extraction with corrupted file."""
        # Arrange
        mock_pdf_reader.side_effect = Exception("Invalid PDF format")
        file_content = b"corrupted content"
        
        # Act & Assert
        with pytest.raises(ValueError, match="PDF text extraction failed"):
            self.service.extract_text_from_pdf(file_content)

    @patch('app.services.resume_service.PdfReader')
    def test_extract_text_from_pdf_empty_file(self, mock_pdf_reader):
        """Test PDF text extraction with empty file."""
        # Arrange
        mock_reader_instance = Mock()
        mock_reader_instance.pages = []
        mock_pdf_reader.return_value = mock_reader_instance
        
        file_content = b""
        
        # Act
        result = self.service.extract_text_from_pdf(file_content)
        
        # Assert
        assert result == ""


class TestSkillExtraction:
    """Test skill extraction functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ResumeService()

    def test_extract_skills_simple_success(self):
        """Test successful skill extraction from text."""
        # Arrange
        text = """
        I am experienced in Python, JavaScript, and React development.
        I have worked with Machine Learning, Docker, and AWS.
        My database experience includes PostgreSQL and MongoDB.
        """
        
        # Act
        skills = self.service.extract_skills_simple(text)
        
        # Assert
        expected_skills = ["Python", "JavaScript", "React", "Machine Learning", 
                          "Docker", "AWS", "PostgreSQL", "MongoDB"]
        
        for skill in expected_skills:
            assert skill in skills, f"Expected skill {skill} not found"
        
        # Should be at least 8 skills as per acceptance criteria
        assert len(skills) >= 8

    def test_extract_skills_case_insensitive(self):
        """Test that skill extraction is case insensitive."""
        # Arrange
        text = "I work with python, JAVASCRIPT, React, and machine learning."
        
        # Act
        skills = self.service.extract_skills_simple(text)
        
        # Assert
        expected_skills = ["Python", "JavaScript", "React", "Machine Learning"]
        for skill in expected_skills:
            assert skill in skills

    def test_extract_skills_no_duplicates(self):
        """Test that skill extraction removes duplicates."""
        # Arrange
        text = "Python Python JavaScript JavaScript React React"
        
        # Act
        skills = self.service.extract_skills_simple(text)
        
        # Assert
        unique_skills = list(set(skills))
        assert len(skills) == len(unique_skills), "Duplicates found in skills"

    def test_extract_skills_empty_text(self):
        """Test skill extraction with empty text."""
        # Arrange
        text = ""
        
        # Act
        skills = self.service.extract_skills_simple(text)
        
        # Assert
        assert skills == []

    def test_extract_skills_no_matching_skills(self):
        """Test skill extraction with text containing no recognizable skills."""
        # Arrange
        text = "I love cooking and painting. My hobbies include gardening."
        
        # Act
        skills = self.service.extract_skills_simple(text)
        
        # Assert
        assert skills == []

    def test_extract_skills_partial_matches(self):
        """Test that partial matches are not included."""
        # Arrange
        text = "I work with Pythonic code and JavaScripting."
        
        # Act
        skills = self.service.extract_skills_simple(text)
        
        # Assert
        # Should not match partial words
        assert "Python" not in skills  # "Pythonic" should not match "Python"
        assert "JavaScript" not in skills  # "JavaScripting" should not match "JavaScript"


class TestBasicInfoExtraction:
    """Test basic information extraction (name, experience)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ResumeService()

    def test_extract_basic_info_with_name(self):
        """Test extraction of name from resume text."""
        # Arrange
        text = """
        Maria Silva
        Software Engineer
        
        I have 3 years of experience in software development.
        """
        
        # Act
        info = self.service.extract_basic_info(text)
        
        # Assert
        assert "name" in info
        assert info["name"] == "Maria Silva"

    def test_extract_basic_info_experience_years(self):
        """Test extraction of years of experience."""
        test_cases = [
            ("I have 3 years of experience", 3),
            ("5 years experience in development", 5),
            ("Experience: 7 years", 7),
            ("10+ years of experience", 10),
            ("2 anos de experiência", 2),  # Portuguese
        ]
        
        for text, expected_years in test_cases:
            # Act
            info = self.service.extract_basic_info(text)
            
            # Assert
            assert info["years_experience"] == expected_years, f"Failed for text: {text}"

    def test_extract_basic_info_experience_level_junior(self):
        """Test experience level classification for junior."""
        # Arrange
        text = "I have 1 year of experience in development."
        
        # Act
        info = self.service.extract_basic_info(text)
        
        # Assert
        assert info["experience_level"] == "junior"
        assert info["years_experience"] == 1

    def test_extract_basic_info_experience_level_mid(self):
        """Test experience level classification for mid-level."""
        # Arrange
        text = "I have 3 years of experience in development."
        
        # Act
        info = self.service.extract_basic_info(text)
        
        # Assert
        assert info["experience_level"] == "mid"
        assert info["years_experience"] == 3

    def test_extract_basic_info_experience_level_senior(self):
        """Test experience level classification for senior."""
        # Arrange
        text = "I have 8 years of experience in development."
        
        # Act
        info = self.service.extract_basic_info(text)
        
        # Assert
        assert info["experience_level"] == "senior"
        assert info["years_experience"] == 8

    def test_extract_basic_info_defaults(self):
        """Test default values when no info found."""
        # Arrange
        text = "Just some random text without clear patterns."
        
        # Act
        info = self.service.extract_basic_info(text)
        
        # Assert
        assert info["years_experience"] == 2  # default
        assert info["experience_level"] == "mid"  # default for 2 years

    def test_extract_basic_info_invalid_name_patterns(self):
        """Test that invalid name patterns are not captured."""
        # Arrange
        text = """
        123 Main Street
        Software Engineer Position
        
        I have experience in development.
        """
        
        # Act
        info = self.service.extract_basic_info(text)
        
        # Assert
        # Should not capture "123 Main" or "Software Engineer" as name
        assert "name" not in info or info.get("name") == ""


class TestResumeProcessing:
    """Test the main resume processing workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ResumeService()
        self.sample_pdf_content = b"fake pdf bytes"
        self.filename = "john_doe_resume.pdf"

    @patch.object(ResumeService, 'extract_text_from_pdf')
    @patch.object(ResumeService, 'extract_skills_simple')
    @patch.object(ResumeService, 'extract_basic_info')
    def test_process_resume_success(self, mock_extract_info, mock_extract_skills, mock_extract_text):
        """Test successful resume processing workflow."""
        # Arrange
        mock_text = "John Doe\nSoftware Engineer\n5 years experience\nPython React"
        mock_skills = ["Python", "React", "JavaScript"]
        mock_info = {"name": "John Doe", "years_experience": 5, "experience_level": "senior"}
        
        mock_extract_text.return_value = mock_text
        mock_extract_skills.return_value = mock_skills
        mock_extract_info.return_value = mock_info
        
        # Act
        result = self.service.process_resume(self.sample_pdf_content, self.filename)
        
        # Assert
        assert "skills" in result
        assert "experience_level" in result
        assert "years_experience" in result
        assert "name" in result
        assert "parsing_method" in result
        assert "filename" in result
        
        assert result["skills"] == mock_skills
        assert result["experience_level"] == "senior"
        assert result["years_experience"] == 5
        assert result["name"] == "John Doe"
        assert result["parsing_method"] == "simple_extraction"
        assert result["filename"] == self.filename
        
        # Verify all methods were called
        mock_extract_text.assert_called_once_with(self.sample_pdf_content)
        mock_extract_skills.assert_called_once_with(mock_text)
        mock_extract_info.assert_called_once_with(mock_text)

    @patch.object(ResumeService, 'extract_text_from_pdf')
    def test_process_resume_pdf_extraction_error(self, mock_extract_text):
        """Test resume processing when PDF extraction fails."""
        # Arrange
        mock_extract_text.side_effect = ValueError("PDF extraction failed")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Failed to process resume"):
            self.service.process_resume(self.sample_pdf_content, self.filename)

    @patch.object(ResumeService, 'extract_text_from_pdf')
    @patch.object(ResumeService, 'extract_skills_simple')
    def test_process_resume_skill_extraction_error(self, mock_extract_skills, mock_extract_text):
        """Test resume processing when skill extraction fails."""
        # Arrange
        mock_extract_text.return_value = "some text"
        mock_extract_skills.side_effect = Exception("Skill extraction failed")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Failed to process resume"):
            self.service.process_resume(self.sample_pdf_content, self.filename)

    def test_process_resume_with_raw_text_truncation(self):
        """Test that raw text is properly truncated in results."""
        # Arrange
        long_text = "A" * 1000  # Text longer than 500 chars
        
        with patch.object(self.service, 'extract_text_from_pdf', return_value=long_text), \
             patch.object(self.service, 'extract_skills_simple', return_value=["Python"]), \
             patch.object(self.service, 'extract_basic_info', return_value={"years_experience": 3, "experience_level": "mid"}):
            
            # Act
            result = self.service.process_resume(self.sample_pdf_content, self.filename)
            
            # Assert
            assert "raw_text" in result
            assert len(result["raw_text"]) == 500
            assert result["raw_text"] == long_text[:500]


class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge cases."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ResumeService()

    def test_process_resume_empty_file_content(self):
        """Test processing with empty file content."""
        # Arrange
        empty_content = b""
        filename = "empty.pdf"
        
        with patch.object(self.service, 'extract_text_from_pdf', return_value=""), \
             patch.object(self.service, 'extract_skills_simple', return_value=[]), \
             patch.object(self.service, 'extract_basic_info', return_value={"years_experience": 2, "experience_level": "mid"}):
            
            # Act
            result = self.service.process_resume(empty_content, filename)
            
            # Assert
            assert result["skills"] == []
            assert result["years_experience"] == 2
            assert result["experience_level"] == "mid"

    def test_process_resume_special_characters_in_filename(self):
        """Test processing with special characters in filename."""
        # Arrange
        filename = "résumé_with_spëcial_chars.pdf"
        
        with patch.object(self.service, 'extract_text_from_pdf', return_value="text"), \
             patch.object(self.service, 'extract_skills_simple', return_value=["Python"]), \
             patch.object(self.service, 'extract_basic_info', return_value={"years_experience": 2, "experience_level": "mid"}):
            
            # Act
            result = self.service.process_resume(b"content", filename)
            
            # Assert
            assert result["filename"] == filename

    @patch('app.services.resume_service.logging')
    def test_process_resume_logs_errors(self, mock_logging):
        """Test that errors are properly logged."""
        # Arrange
        mock_logger = Mock()
        mock_logging.getLogger.return_value = mock_logger
        
        service = ResumeService()
        
        with patch.object(service, 'extract_text_from_pdf', side_effect=Exception("Test error")):
            
            # Act & Assert
            with pytest.raises(ValueError):
                service.process_resume(b"content", "test.pdf")
            
            # Verify error was logged
            mock_logger.error.assert_called_once()


class TestPerformanceAndLimits:
    """Test performance considerations and limits."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ResumeService()

    def test_skill_extraction_performance_large_text(self):
        """Test skill extraction performance with large text."""
        # Arrange
        large_text = " ".join(["Python", "JavaScript", "React"] * 1000)
        
        # Act
        import time
        start_time = time.time()
        skills = self.service.extract_skills_simple(large_text)
        end_time = time.time()
        
        # Assert
        execution_time = end_time - start_time
        assert execution_time < 1.0, "Skill extraction should complete within 1 second"
        assert "Python" in skills
        assert "JavaScript" in skills
        assert "React" in skills

    def test_skill_keywords_reasonable_size(self):
        """Test that skill keywords list is reasonable size."""
        # Arrange & Act
        skill_count = len(self.service.skill_keywords)
        
        # Assert
        assert 20 <= skill_count <= 100, f"Skill keywords count {skill_count} should be between 20-100"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

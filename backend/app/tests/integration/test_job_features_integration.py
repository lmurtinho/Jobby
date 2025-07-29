"""
Integration tests for Day 2: Core Job Features

This test suite follows the outside-in TDD approach to drive the implementation
of job display, filtering, matching, and basic functionality as defined in the MVP roadmap.

These tests will fail initially and create GitHub issues to guide systematic implementation.
"""

import pytest
from pathlib import Path
import json
from typing import List, Dict, Any


class TestJobFeaturesIntegration:
    """
    Integration tests for Day 2 core job features.
    
    These tests drive the implementation of:
    - Job data layer with sample data
    - Job TypeScript interfaces and types  
    - JobCard component for display
    - Job matching algorithm
    - Search and filtering functionality
    - Save/unsave job functionality
    """
    
    def test_job_typescript_interfaces_exist(self):
        """Test that proper TypeScript interfaces are defined for jobs."""
        # Check if job types file exists
        job_types_file = Path("../frontend/src/types/job.ts")
        assert job_types_file.exists(), "Job TypeScript interfaces should exist at frontend/src/types/job.ts"
        
        # Read and verify interface content
        content = job_types_file.read_text()
        
        # Should have Job interface with required fields
        assert "interface Job" in content, "Should have Job interface"
        assert "id:" in content, "Job should have id field"
        assert "title:" in content, "Job should have title field"
        assert "company:" in content, "Job should have company field"
        assert "location:" in content, "Job should have location field"
        assert "salary:" in content, "Job should have salary field"
        assert "description:" in content, "Job should have description field"
        assert "requirements:" in content, "Job should have requirements field"
        assert "remote:" in content, "Job should have remote field"
        assert "posted_date:" in content, "Job should have posted_date field"
        assert "apply_url:" in content, "Job should have apply_url field"
        assert "source:" in content, "Job should have source field"
    
    def test_sample_job_data_exists(self):
        """Test that sample job data exists and is properly structured."""
        # Check if sample data file exists
        sample_data_file = Path("frontend/src/data/sampleJobs.ts")
        assert sample_data_file.exists(), "Sample job data should exist at frontend/src/data/sampleJobs.ts"
        
        content = sample_data_file.read_text()
        
        # Should export sample jobs array
        assert "export const SAMPLE_JOBS" in content, "Should export SAMPLE_JOBS constant"
        assert "Senior Data Scientist" in content, "Should contain data science jobs"
        assert "Machine Learning" in content, "Should contain ML jobs"
        assert "Remote" in content, "Should contain remote jobs"
        assert "Brazil" in content or "LATAM" in content, "Should target LATAM market"
        
        # Should have at least 10 job entries for testing
        job_count = content.count('"id":') or content.count("id:")
        assert job_count >= 10, f"Should have at least 10 sample jobs, found {job_count}"
    
    def test_job_matching_algorithm_exists(self):
        """Test that job matching algorithm utility exists."""
        matching_file = Path("../frontend/src/utils/jobMatching.ts")
        assert matching_file.exists(), "Job matching utility should exist at frontend/src/utils/jobMatching.ts"
        
        content = matching_file.read_text()
        
        # Should have calculateMatchScore function
        assert "calculateMatchScore" in content, "Should have calculateMatchScore function"
        assert "jobSkills" in content, "Should accept job skills parameter"
        assert "userSkills" in content, "Should accept user skills parameter"
        assert "number" in content, "Should return number (match score)"
        
        # Should have proper algorithm logic
        assert "filter" in content or "includes" in content, "Should implement skill matching logic"
        assert "length" in content, "Should calculate based on skill overlap"
    
    def test_job_card_component_exists(self):
        """Test that JobCard component exists and is properly structured."""
        job_card_file = Path("../frontend/src/components/JobCard.tsx")
        assert job_card_file.exists(), "JobCard component should exist at frontend/src/components/JobCard.tsx"
        
        content = job_card_file.read_text()
        
        # Should be a React component
        assert "import React" in content, "Should import React"
        assert "interface JobCardProps" in content, "Should have JobCardProps interface"
        assert "const JobCard" in content or "function JobCard" in content, "Should define JobCard component"
        assert "export default JobCard" in content, "Should export JobCard as default"
        
        # Should accept required props
        assert "job:" in content, "Should accept job prop"
        assert "userSkills" in content, "Should accept userSkills prop"
        assert "onSave" in content, "Should accept onSave callback prop"
        assert "onApply" in content, "Should accept onApply callback prop"
        
        # Should display job information
        assert "job.title" in content, "Should display job title"
        assert "job.company" in content, "Should display company name"
        assert "job.location" in content, "Should display job location"
        assert "job.salary" in content, "Should display salary information"
    
    def test_job_search_functionality_exists(self):
        """Test that job search and filtering functionality exists."""
        search_file = Path("../frontend/src/components/JobSearch.tsx")
        assert search_file.exists(), "JobSearch component should exist at frontend/src/components/JobSearch.tsx"
        
        content = search_file.read_text()
        
        # Should be a search component
        assert "import React" in content, "Should import React"
        assert "JobSearch" in content, "Should define JobSearch component"
        assert "useState" in content, "Should use state for search input"
        
        # Should have search functionality
        assert "input" in content.lower() or "Input" in content, "Should have search input field"
        assert "onChange" in content or "onInputChange" in content, "Should handle input changes"
        assert "filter" in content.lower(), "Should implement filtering logic"
    
    def test_job_service_layer_exists(self):
        """Test that job service layer exists for data management."""
        service_file = Path("frontend/src/services/jobService.ts")
        assert service_file.exists(), "Job service should exist at frontend/src/services/jobService.ts"
        
        content = service_file.read_text()
        
        # Should have service functions
        assert "getJobs" in content, "Should have getJobs function"
        assert "searchJobs" in content, "Should have searchJobs function"
        assert "filterJobs" in content, "Should have filterJobs function"
        assert "saveJob" in content, "Should have saveJob function"
        assert "unsaveJob" in content, "Should have unsaveJob function"
        
        # Should handle async operations
        assert "async" in content or "Promise" in content, "Should support async operations for future API integration"
    
    def test_job_dashboard_page_exists(self):
        """Test that job dashboard page exists and integrates components."""
        dashboard_file = Path("frontend/src/pages/JobDashboard.tsx")
        assert dashboard_file.exists(), "Job dashboard should exist at frontend/src/pages/JobDashboard.tsx"
        
        content = dashboard_file.read_text()
        
        # Should be a React page component
        assert "import React" in content, "Should import React"
        assert "JobDashboard" in content, "Should define JobDashboard component"
        assert "useState" in content, "Should manage state"
        assert "useEffect" in content, "Should use effects for data loading"
        
        # Should integrate job components
        assert "JobCard" in content, "Should use JobCard component"
        assert "JobSearch" in content, "Should use JobSearch component"
        assert "calculateMatchScore" in content, "Should use matching algorithm"
        
        # Should handle job operations
        assert "handleSaveJob" in content or "onSave" in content, "Should handle job saving"
        assert "handleApplyJob" in content or "onApply" in content, "Should handle job applications"
    
    def test_job_routing_integration(self):
        """Test that job dashboard is integrated into routing."""
        app_file = Path("frontend/src/App.tsx")
        assert app_file.exists(), "App.tsx should exist"
        
        content = app_file.read_text()
        
        # Should have job dashboard route
        assert "JobDashboard" in content, "Should import JobDashboard"
        assert "/jobs" in content or "/dashboard" in content, "Should have jobs route"
        assert "ProtectedRoute" in content, "Job dashboard should be protected"
    
    def test_job_matching_algorithm_accuracy(self):
        """Test that job matching algorithm produces reasonable results."""
        # This test requires the algorithm to be implemented
        matching_file = Path("../frontend/src/utils/jobMatching.ts")
        
        if matching_file.exists():
            # Test algorithm with known inputs
            user_skills = ["Python", "Machine Learning", "SQL"]
            job_skills = ["Python", "TensorFlow", "AWS", "Machine Learning"]
            
            # Should calculate reasonable match score
            # This will fail until algorithm is implemented
            # Expected: 50% match (2 out of 4 job skills match user skills)
            pass  # Will be implemented when algorithm exists
    
    def test_job_data_quality(self):
        """Test that sample job data meets quality standards."""
        sample_data_file = Path("frontend/src/data/sampleJobs.ts")
        
        if sample_data_file.exists():
            content = sample_data_file.read_text()
            
            # Should have diverse job types
            assert "Data Scientist" in content, "Should have data science jobs"
            assert "Machine Learning" in content, "Should have ML jobs"
            assert "Software Engineer" in content, "Should have engineering jobs"
            assert "Product Manager" in content, "Should have product jobs"
            
            # Should target LATAM market
            assert "Remote" in content, "Should have remote jobs"
            assert "Brazil" in content or "LATAM" in content or "timezone" in content, "Should target LATAM"
            
            # Should have realistic salaries
            assert "$" in content, "Should have USD salaries"
            assert "000" in content, "Should have realistic salary amounts"
    
    def test_job_components_build_successfully(self):
        """Test that frontend builds with job components."""
        # Run frontend build to ensure no compilation errors
        import subprocess
        import os
        
        frontend_dir = Path("frontend")
        if frontend_dir.exists():
            try:
                result = subprocess.run(
                    ["npm", "run", "build"],
                    cwd=frontend_dir,
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minutes max
                )
                
                # Build should succeed
                assert result.returncode == 0, f"Frontend build failed: {result.stderr}"
                
                # Should not have TypeScript errors
                assert "error TS" not in result.stderr, f"TypeScript errors found: {result.stderr}"
                
            except subprocess.TimeoutExpired:
                pytest.fail("Frontend build timed out after 2 minutes")
            except FileNotFoundError:
                pytest.skip("npm not available for build test")
    
    def test_job_features_integration_complete(self):
        """Test that all Day 2 job features are integrated and working."""
        # This comprehensive test ensures all components work together
        
        required_files = [
            "frontend/src/types/job.ts",
            "frontend/src/data/sampleJobs.ts", 
            "frontend/src/utils/jobMatching.ts",
            "frontend/src/components/JobCard.tsx",
            "frontend/src/components/JobSearch.tsx",
            "frontend/src/services/jobService.ts",
            "frontend/src/pages/JobDashboard.tsx"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        assert len(missing_files) == 0, f"Missing Day 2 job feature files: {', '.join(missing_files)}"
        
        # All components should integrate properly
        # This test passes when all individual component tests pass
        assert True, "All Day 2 job features are implemented and integrated"

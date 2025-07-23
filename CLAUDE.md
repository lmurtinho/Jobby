# CLAUDE.md - Development Guide for AI Job Tracker (Python)

This file provides Claude Code with essential information for working within the AI Job Tracker Python repository.

## 🏗️ Project Architecture

**Stack**: FastAPI + Python backend, React + TypeScript frontend, PostgreSQL database, Railway + Vercel deployment
**AI Integration**: Anthropic Claude API + scikit-learn + spaCy for advanced ML capabilities
**Job Sources**: LinkedIn, RemoteOK, AngelList, RSS feeds, custom API integrations with Scrapy framework
**Background Processing**: Celery + Redis for distributed task processing

## 📝 Code Style Guidelines

### Python Backend
- Follow PEP 8 with Black formatting: `black app/ --line-length 88`
- Use type hints for all functions: `def process_job(job_data: Dict[str, Any]) -> JobMatch:`
- Async/await for I/O operations: `async def scrape_jobs() -> List[Job]:`
- Pydantic models for data validation: `class JobCreate(BaseModel):`
- Use pathlib for file operations: `from pathlib import Path`
- Exception handling with custom exceptions: `raise JobScrapingError("Failed to parse")`

### FastAPI Conventions
- Router organization: separate routers for each domain (`jobs.py`, `users.py`, `skills.py`)
- Dependency injection: use `Depends()` for database sessions, authentication
- Response models: always specify `response_model` in route decorators
- Status codes: use FastAPI status constants: `status.HTTP_201_CREATED`
- Async route handlers when performing I/O operations

### Database (SQLAlchemy)
- Model naming: singular PascalCase (`User`, `Job`, not `Users`, `Jobs`)
- Relationship definitions: use `relationship()` and `back_populates`
- Indexes: add `@@index` for frequently queried columns
- Migrations: always create migrations for schema changes: `alembic revision --autogenerate`
- Query optimization: use `select()` and `joinedload()` for efficient queries

### Machine Learning Code
- Model interfaces: inherit from abstract base classes
- Preprocessing pipelines: use scikit-learn Pipeline objects
- Model persistence: pickle or joblib for model serialization
- Feature engineering: separate modules for different feature types
- Model evaluation: comprehensive metrics and validation

### Naming Conventions
- Files: snake_case (`resume_parser.py`, `skill_analyzer.py`)
- Functions/methods: snake_case (`analyze_skill_gaps`, `parse_resume`)
- Classes: PascalCase (`SkillGapAnalyzer`, `JobMatcher`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRY_ATTEMPTS`, `DEFAULT_BATCH_SIZE`)
- Database tables: snake_case (`job_matches`, `skill_gap_analyses`)
- API endpoints: kebab-case (`/api/v1/skill-analysis`, `/api/v1/job-sources`)

## 🛠️ Development Commands

### Root Level
```bash
# Setup
make install                 # Install all dependencies (backend + frontend)
make setup-dev              # Complete development environment setup
make migrate                # Run database migrations
make seed                   # Seed database with test data

# Development
make dev                    # Start all services (API, workers, frontend)
make test                   # Run all tests with coverage
make lint                   # Run linting (black, flake8, mypy)
make typecheck              # Run mypy type checking
make format                 # Format code with black and isort

# Deployment
make deploy-prod            # Deploy to Railway + Vercel
make backup-db              # Backup production database
```

### Backend (`backend/`)
```bash
# Development
uvicorn app.main:app --reload --port 8000    # Start FastAPI development server
python -m pytest --cov=app --cov-report=html # Run tests with coverage
black app/ --check                           # Check code formatting
mypy app/                                    # Type checking
flake8 app/                                  # Linting

# Database
alembic upgrade head                         # Apply migrations
alembic revision --autogenerate -m "message" # Create new migration
python scripts/seed_database.py             # Seed test data
python scripts/backup_database.py           # Backup database

# Background Tasks
celery -A app.workers.celery_app worker --loglevel=info     # Start Celery worker
celery -A app.workers.celery_app beat --loglevel=info       # Start Celery scheduler
celery -A app.workers.celery_app flower                     # Start Celery monitoring

# Machine Learning
python scripts/train_models.py              # Train ML models
python scripts/evaluate_models.py           # Evaluate model performance
python app/ml/training/train_skill_recommender.py # Train specific model
```

### Frontend (`frontend/`)
```bash
npm start                   # Start development server (localhost:3000)
npm run build              # Build for production
npm test                   # Run React tests with Jest
npm run test:coverage      # Run tests with coverage report
npm run lint               # ESLint checking
npm run typecheck          # TypeScript checking
```

## 🔄 Development Workflow: Issue-Driven + Test-Driven Development

### Core Workflow Process
Based on the [issue-driven development methodology](https://gist.github.com/Mattchine/176ca6a0c7cd3eaa442dd9d7559ad2f9), combined with test-driven development:

#### Phase 1: Test Generation and Issue Creation
1. **Generate Unit Tests from Documentation**:
   ```bash
   # For each new feature/component, generate comprehensive unit tests
   python scripts/generate_tests_from_docs.py --component skill_analyzer
   python scripts/generate_tests_from_docs.py --api-endpoint /api/v1/jobs/match
   ```

2. **Run Tests and Identify Failures**:
   ```bash
   # Run all tests and collect failures
   pytest app/tests/ --tb=short --failed-only > test_failures.txt
   
   # Generate GitHub issues for each failure
   python scripts/create_issues_from_failures.py test_failures.txt
   ```

3. **Automatic Issue Creation**:
   ```bash
   # Each failing test becomes a GitHub issue with:
   # - Clear title: "Fix failing test: test_skill_gap_analysis_with_empty_profile"
   # - Description with test code, expected vs actual behavior
   # - Labels: "bug", "test-failure", priority level
   # - Assignment to appropriate team member
   ```

#### Phase 2: Issue-Driven Development
4. **Issue Processing Workflow**:
   ```bash
   # For each GitHub issue, follow this process:
   
   # a) Create feature branch from issue
   git checkout -b fix/issue-123-skill-gap-analysis
   
   # b) Write failing test (if not already exists)
   # c) Implement minimal code to make test pass
   # d) Refactor while keeping tests green
   # e) Update documentation
   # f) Create pull request referencing issue
   ```

5. **Commit Message Convention**:
   ```bash
   # Link commits to issues
   git commit -m "fix(skill-analyzer): handle empty user profile
   
   - Add validation for empty skills list
   - Return appropriate default recommendations
   - Add comprehensive error handling
   
   Fixes #123"
   ```

#### Phase 3: Continuous Integration
6. **Automated Workflow**:
   ```bash
   # On each push, automatically:
   # - Run all tests
   # - Check code quality (black, flake8, mypy)
   # - Update test coverage reports
   # - Close resolved issues
   # - Generate new issues for new test failures
   ```

### Issue Categories and Templates

#### Bug Issues (from failing tests)
```markdown
**Test Failure**: `test_skill_gap_analysis_with_ml_model`
**Component**: `app.services.skill_analyzer`
**Priority**: High

**Expected Behavior**:
- Skill gap analysis should return ranked missing skills
- Should include learning recommendations
- Should calculate improvement potential

**Actual Behavior**:
- Function raises AttributeError: 'NoneType' object has no attribute 'analyze'
- ML model not properly initialized

**Test Code**:
```python
def test_skill_gap_analysis_with_ml_model():
    # Test implementation here
```

**Acceptance Criteria**:
- [ ] ML model initializes correctly
- [ ] Function handles empty/null inputs gracefully
- [ ] Returns properly formatted analysis results
- [ ] Test passes consistently
```

#### Feature Issues (from missing functionality)
```markdown
**Feature Request**: Implement job salary prediction model
**Component**: `app.ml.models.salary_predictor`
**Priority**: Medium

**Description**:
Based on documentation requirements, need ML model to predict salary ranges for jobs missing salary information.

**Requirements**:
- Use job title, company, location, and required skills as features
- Train on jobs with known salaries
- Provide confidence intervals for predictions
- Integration with job matching pipeline

**Acceptance Criteria**:
- [ ] SalaryPredictorModel class implemented
- [ ] Training pipeline created
- [ ] API endpoint for salary prediction
- [ ] Model evaluation metrics >= 80% accuracy
- [ ] Unit tests with >90% coverage
```

### Test-Driven Development Guidelines

#### Outside-In TDD Approach
Use **Outside-In TDD** (London School) for complex workflows and system integration:

**Phase 1: Start with High-Level Integration Tests**
```python
# Begin with a large test that encompasses full functionality
def test_complete_resume_processing_workflow():
    """Integration test covering entire resume upload → skill extraction → job matching flow."""
    # This will fail initially and guide implementation step by step
    
    # Arrange
    user = create_test_user()
    resume_file = load_test_resume("data_scientist_resume.pdf")
    target_jobs = create_test_jobs(["Senior Data Scientist", "ML Engineer"])
    
    # Act - Test the complete workflow
    result = upload_and_process_resume(user.id, resume_file)
    matches = calculate_job_matches(user.id, target_jobs)
    skill_analysis = analyze_skill_gaps(user.id, target_jobs)
    
    # Assert - Verify end-to-end functionality
    assert result.skills == ["Python", "Machine Learning", "SQL", "TensorFlow"]
    assert result.experience_level == "mid"
    assert len(matches) > 0
    assert matches[0].match_score > 80
    assert len(skill_analysis.missing_skills) > 0
    assert "Docker" in [skill[0] for skill in skill_analysis.missing_skills]

def test_job_scraping_to_notification_workflow():
    """Integration test for job discovery → matching → notification pipeline."""
    # Another large test covering the scraping workflow
    
    # Arrange
    user = create_user_with_preferences()
    job_source = create_test_job_source("LinkedIn")
    
    # Act - Complete scraping and notification flow
    scraped_jobs = scrape_job_source(job_source)
    matches = calculate_matches_for_user(user.id, scraped_jobs)
    notification_sent = send_job_alert(user.id, matches)
    
    # Assert
    assert len(scraped_jobs) > 0
    assert len(matches) > 0
    assert notification_sent.status == "delivered"
    assert "New job matches found" in notification_sent.subject
```

**Phase 2: Let Failures Drive Unit Test Creation**
When the large test fails, create specific unit tests based on error messages:

```python
# Error: "AttributeError: 'NoneType' object has no attribute 'extract_text'"
# → Create unit test for PDF text extraction

def test_pdf_text_extraction():
    """Test PDF text extraction functionality."""
    pdf_file = load_test_pdf("sample_resume.pdf")
    
    extractor = PDFTextExtractor()
    text = extractor.extract_text(pdf_file)
    
    assert text is not None
    assert len(text) > 100
    assert "Python" in text
    assert "Machine Learning" in text

# Error: "SkillExtractor object has no attribute 'extract_skills'"
# → Create unit test for skill extraction

def test_skill_extraction_from_text():
    """Test skill extraction from resume text."""
    resume_text = "Experienced Python developer with Machine Learning and SQL expertise..."
    
    extractor = SkillExtractor()
    skills = extractor.extract_skills(resume_text)
    
    assert isinstance(skills, list)
    assert "Python" in skills
    assert "Machine Learning" in skills
    assert "SQL" in skills

# Error: "JobMatcher.calculate_score() missing required argument 'user_profile'"
# → Create unit test for job matching

def test_job_matching_calculation():
    """Test job match score calculation."""
    user_profile = {
        "skills": ["Python", "SQL"],
        "experience_level": "mid"
    }
    job = {
        "requirements": ["Python", "Machine Learning", "SQL"],
        "seniority": "mid"
    }
    
    matcher = JobMatcher()
    score = matcher.calculate_score(user_profile, job)
    
    assert 0 <= score <= 100
    assert score > 70  # Should be high match
```

**Phase 3: Iterative Refinement**
```python
# As unit tests pass, integration test reveals next layer of failures:

# Error: "Database connection not found"
# → Create database setup unit tests

def test_database_connection():
    """Test database connectivity."""
    db = get_test_database()
    assert db.is_connected()
    
def test_user_creation_in_database():
    """Test user model database operations."""
    db = get_test_database()
    user_data = {"email": "test@example.com", "name": "Test User"}
    
    user = create_user(db, user_data)
    assert user.id is not None
    assert user.email == "test@example.com"

# Error: "Claude API authentication failed"
# → Create API integration unit tests

def test_claude_api_authentication():
    """Test Claude API connection and authentication."""
    client = ClaudeAPIClient()
    response = client.test_connection()
    assert response.status == "authenticated"

def test_resume_parsing_with_claude():
    """Test resume parsing via Claude API."""
    sample_text = "John Doe - Data Scientist with Python and ML experience"
    parser = ClaudeResumeParser()
    
    result = parser.parse_resume_text(sample_text)
    assert result.name == "John Doe"
    assert "Python" in result.skills
```

**Phase 4: Issue-Driven Development Integration**
```python
# Large integration test failure creates Epic issue:
# Title: "Implement complete resume processing workflow"
# Body: Contains the failing integration test and acceptance criteria

# Each unit test failure creates specific issues:
# - "Fix PDF text extraction - AttributeError in PDFTextExtractor" 
# - "Implement skill extraction - SkillExtractor.extract_skills missing"
# - "Add job matching calculation - JobMatcher missing calculate_score method"
# - "Setup database connection - Connection not found error"
# - "Configure Claude API authentication - Authentication failed"

# Commit messages link to issues:
# "fix(pdf-extractor): implement text extraction from PDF files
# 
# - Add PDFTextExtractor class with extract_text method
# - Handle various PDF formats and encodings
# - Add error handling for corrupted files
# 
# Fixes #45"
```

#### Unit Test Structure
```python
# app/tests/unit/services/test_skill_analyzer.py
import pytest
from unittest.mock import Mock, patch
from app.services.skill_analyzer import SkillGapAnalyzer
from app.tests.fixtures.user_data import sample_user_profile
from app.tests.fixtures.job_data import sample_job_postings

class TestSkillGapAnalyzer:
    """Test suite for SkillGapAnalyzer service."""
    
    @pytest.fixture
    def analyzer(self):
        """Create SkillGapAnalyzer instance for testing."""
        return SkillGapAnalyzer()
    
    def test_analyze_skill_gaps_success(self, analyzer, sample_user_profile, sample_job_postings):
        """Test successful skill gap analysis."""
        # Arrange
        user_skills = sample_user_profile["skills"]
        
        # Act
        result = analyzer.analyze_skill_gaps(user_skills, sample_job_postings)
        
        # Assert
        assert "missing_skills" in result
        assert "learning_path" in result
        assert "improvement_potential" in result
        assert len(result["missing_skills"]) > 0
        
        # Verify skill ranking
        missing_skills = result["missing_skills"]
        assert all(isinstance(skill, tuple) for skill in missing_skills)
        assert all(len(skill) == 2 for skill in missing_skills)  # (skill_name, importance_score)
        
        # Verify scores are properly ordered (highest first)
        scores = [skill[1] for skill in missing_skills]
        assert scores == sorted(scores, reverse=True)
    
    def test_analyze_skill_gaps_empty_user_skills(self, analyzer, sample_job_postings):
        """Test skill gap analysis with empty user skills."""
        # Arrange
        empty_skills = []
        
        # Act
        result = analyzer.analyze_skill_gaps(empty_skills, sample_job_postings)
        
        # Assert
        assert result["missing_skills"] is not None
        assert len(result["missing_skills"]) > 0  # Should return all job skills as missing
        assert result["improvement_potential"]["current_avg"] == 0  # No current match
```python
# app/tests/unit/services/test_skill_analyzer.py
import pytest
from unittest.mock import Mock, patch
from app.services.skill_analyzer import SkillGapAnalyzer
from app.tests.fixtures.user_data import sample_user_profile
from app.tests.fixtures.job_data import sample_job_postings

class TestSkillGapAnalyzer:
    """Test suite for SkillGapAnalyzer service."""
    
    @pytest.fixture
    def analyzer(self):
        """Create SkillGapAnalyzer instance for testing."""
        return SkillGapAnalyzer()
    
    def test_analyze_skill_gaps_success(self, analyzer, sample_user_profile, sample_job_postings):
        """Test successful skill gap analysis."""
        # Arrange
        user_skills = sample_user_profile["skills"]
        
        # Act
        result = analyzer.analyze_skill_gaps(user_skills, sample_job_postings)
        
        # Assert
        assert "missing_skills" in result
        assert "learning_path" in result
        assert "improvement_potential" in result
        assert len(result["missing_skills"]) > 0
        
        # Verify skill ranking
        missing_skills = result["missing_skills"]
        assert all(isinstance(skill, tuple) for skill in missing_skills)
        assert all(len(skill) == 2 for skill in missing_skills)  # (skill_name, importance_score)
        
        # Verify scores are properly ordered (highest first)
        scores = [skill[1] for skill in missing_skills]
        assert scores == sorted(scores, reverse=True)
    
    def test_analyze_skill_gaps_empty_user_skills(self, analyzer, sample_job_postings):
        """Test skill gap analysis with empty user skills."""
        # Arrange
        empty_skills = []
        
        # Act
        result = analyzer.analyze_skill_gaps(empty_skills, sample_job_postings)
        
        # Assert
        assert result["missing_skills"] is not None
        assert len(result["missing_skills"]) > 0  # Should return all job skills as missing
        assert result["improvement_potential"]["current_avg"] == 0  # No current match
    
    def test_analyze_skill_gaps_no_target_jobs(self, analyzer, sample_user_profile):
        """Test skill gap analysis with no target jobs."""
        # Arrange
        user_skills = sample_user_profile["skills"]
        empty_jobs = []
        
        # Act
        result = analyzer.analyze_skill_gaps(user_skills, empty_jobs)
        
        # Assert
        assert result["missing_skills"] == []
        assert result["learning_path"] == []
        assert "no_jobs_analyzed" in result["improvement_potential"]
    
    @patch('app.services.skill_analyzer.claude_client')
    def test_analyze_skill_gaps_claude_api_failure(self, mock_claude, analyzer, sample_user_profile, sample_job_postings):
        """Test behavior when Claude API fails."""
        # Arrange
        mock_claude.complete.side_effect = Exception("API Error")
        user_skills = sample_user_profile["skills"]
        
        # Act & Assert
        with pytest.raises(SkillAnalysisError, match="Failed to analyze skills"):
            analyzer.analyze_skill_gaps(user_skills, sample_job_postings)
    
    def test_skill_importance_calculation(self, analyzer):
        """Test skill importance scoring algorithm."""
        # Arrange
        skill_frequency_data = {
            "Python": 45,      # High frequency = high importance
            "Docker": 12,      # Medium frequency
            "Blockchain": 2    # Low frequency = lower importance
        }
        
        # Act
        python_score = analyzer.calculate_skill_importance("Python", 45)
        docker_score = analyzer.calculate_skill_importance("Docker", 12)
        blockchain_score = analyzer.calculate_skill_importance("Blockchain", 2)
        
        # Assert
        assert python_score > docker_score
        assert docker_score > blockchain_score
        assert 0 <= python_score <= 100
        assert 0 <= docker_score <= 100
        assert 0 <= blockchain_score <= 100

    @pytest.mark.ml
    def test_ml_model_integration(self, analyzer):
        """Test ML model integration for skill similarity."""
        # Arrange
        user_skills = ["Python", "Machine Learning"]
        job_requirements = ["PyTorch", "Deep Learning", "Neural Networks"]
        
        # Act
        similarity_score = analyzer.calculate_semantic_similarity(user_skills, job_requirements)
        
        # Assert
        assert 0 <= similarity_score <= 1
        assert similarity_score > 0.3  # Should have some semantic similarity
    
    @pytest.mark.slow
    def test_generate_learning_path_comprehensive(self, analyzer):
        """Test comprehensive learning path generation."""
        # Arrange
        missing_skills = [
            ("TensorFlow", 0.95),
            ("Docker", 0.78),
            ("AWS", 0.82),
            ("Kubernetes", 0.65),
            ("MLOps", 0.88)
        ]
        
        # Act
        learning_path = analyzer.generate_learning_path(missing_skills)
        
        # Assert
        assert len(learning_path) <= 10  # Should limit to top 10
        assert all("skill" in item for item in learning_path)
        assert all("courses" in item for item in learning_path)
        assert all("estimated_hours" in item for item in learning_path)
        assert all("prerequisites" in item for item in learning_path)
        
        # Verify priority ordering
        priorities = [item["priority"] for item in learning_path]
        assert priorities == list(range(1, len(priorities) + 1))
```

#### Integration Test Structure
```python
# app/tests/integration/test_job_matching_workflow.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.database import get_db
from app.tests.fixtures.test_database import TestSessionLocal, override_get_db

# Override database dependency for testing
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.integration
class TestJobMatchingWorkflow:
    """Integration tests for complete job matching workflow."""
    
    def test_complete_matching_workflow(self, client: TestClient, db: Session):
        """Test complete workflow from resume upload to job matching."""
        # Step 1: Create user account
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        user_id = response.json()["id"]
        
        # Step 2: Upload and parse resume
        with open("app/tests/fixtures/sample_resume.pdf", "rb") as resume_file:
            response = client.post(
                f"/api/v1/users/{user_id}/resume",
                files={"resume": ("resume.pdf", resume_file, "application/pdf")}
            )
        assert response.status_code == 200
        resume_data = response.json()
        assert "skills" in resume_data
        
        # Step 3: Add job postings
        job_data = {
            "title": "Senior Data Scientist",
            "company": "TechCorp",
            "requirements": ["Python", "TensorFlow", "AWS"],
            "location": "Remote",
            "salary": "$15,000/month"
        }
        response = client.post("/api/v1/jobs", json=job_data)
        assert response.status_code == 201
        job_id = response.json()["id"]
        
        # Step 4: Calculate job matches
        response = client.post(f"/api/v1/users/{user_id}/calculate-matches")
        assert response.status_code == 200
        
        # Step 5: Get job matches
        response = client.get(f"/api/v1/users/{user_id}/job-matches")
        assert response.status_code == 200
        matches = response.json()
        
        assert len(matches) > 0
        match = matches[0]
        assert "job_id" in match
        assert "match_score" in match
        assert 0 <= match["match_score"] <= 100
        
        # Step 6: Perform skill gap analysis
        response = client.post(f"/api/v1/users/{user_id}/skill-analysis", json={"target_job_ids": [job_id]})
        assert response.status_code == 200
        skill_analysis = response.json()
        
        assert "missing_skills" in skill_analysis
        assert "learning_path" in skill_analysis
        assert "improvement_potential" in skill_analysis
```

### Issue Management Scripts

#### Auto-generate Tests from Documentation
```python
# scripts/generate_tests_from_docs.py
import ast
import re
from pathlib import Path
from typing import List, Dict

class TestGenerator:
    """Generate unit tests based on API documentation and function signatures."""
    
    def generate_tests_for_module(self, module_path: Path) -> str:
        """Generate comprehensive test cases for a Python module."""
        
        # Parse module AST
        with open(module_path, 'r') as f:
            tree = ast.parse(f.read())
        
        test_cases = []
        
        # Extract classes and functions
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                test_cases.extend(self.generate_class_tests(node))
            elif isinstance(node, ast.FunctionDef):
                test_cases.extend(self.generate_function_tests(node))
        
        return self.format_test_file(module_path, test_cases)
    
    def generate_class_tests(self, class_node: ast.ClassDef) -> List[str]:
        """Generate test cases for a class."""
        tests = []
        class_name = class_node.name
        
        # Generate constructor tests
        tests.append(f"""
    def test_{class_name.lower()}_initialization(self):
        \"\"\"Test {class_name} initialization.\"\"\"
        instance = {class_name}()
        assert instance is not None
        # TODO: Add specific initialization assertions
        """)
        
        # Generate method tests
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                tests.extend(self.generate_method_tests(class_name, node))
        
        return tests
    
    def generate_method_tests(self, class_name: str, method_node: ast.FunctionDef) -> List[str]:
        """Generate test cases for a class method."""
        method_name = method_node.name
        tests = []
        
        # Success case
        tests.append(f"""
    def test_{method_name}_success(self):
        \"\"\"Test {method_name} successful execution.\"\"\"
        instance = {class_name}()
        # TODO: Implement test case based on method signature
        # Method signature: {self.get_method_signature(method_node)}
        pass
        """)
        
        # Error cases based on parameters
        if self.has_parameters(method_node):
            tests.append(f"""
    def test_{method_name}_invalid_input(self):
        \"\"\"Test {method_name} with invalid input.\"\"\"
        instance = {class_name}()
        with pytest.raises(ValueError):
            # TODO: Add invalid input test
            pass
        """)
        
        return tests

# Usage in workflow
if __name__ == "__main__":
    generator = TestGenerator()
    
    # Generate tests for specific modules
    modules_to_test = [
        "app/services/skill_analyzer.py",
        "app/services/resume_parser.py", 
        "app/services/job_aggregator.py"
    ]
    
    for module_path in modules_to_test:
        test_content = generator.generate_tests_for_module(Path(module_path))
        
        # Write test file
        test_file_path = f"app/tests/unit/{module_path.replace('app/', '').replace('.py', '_test.py')}"
        Path(test_file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(test_file_path, 'w') as f:
            f.write(test_content)
```

#### Auto-create GitHub Issues from Test Failures
```python
# scripts/create_issues_from_failures.py
import re
import json
import requests
from pathlib import Path
from typing import List, Dict

class IssueCreator:
    """Create GitHub issues automatically from test failures."""
    
    def __init__(self, github_token: str, repo: str):
        self.github_token = github_token
        self.repo = repo
        self.github_api = "https://api.github.com"
    
    def parse_test_failures(self, pytest_output: str) -> List[Dict]:
        """Parse pytest output to extract failure information."""
        failures = []
        
        # Regex patterns for pytest output
        failure_pattern = r"FAILED (.*?)::(.*?) - (.*)"
        traceback_pattern = r"(.*?)\n(.*?)\n(.*?AssertionError.*?)\n"
        
        matches = re.findall(failure_pattern, pytest_output)
        
        for match in matches:
            test_file, test_name, error_summary = match
            
            failure_info = {
                "test_file": test_file,
                "test_name": test_name,
                "error_summary": error_summary,
                "component": self.extract_component(test_file),
                "priority": self.determine_priority(error_summary)
            }
            failures.append(failure_info)
        
        return failures
    
    def create_github_issue(self, failure: Dict) -> str:
        """Create a GitHub issue for a test failure."""
        
        title = f"Fix failing test: {failure['test_name']}"
        
        body = f"""
**Test Failure Report**

**Component**: `{failure['component']}`
**Test File**: `{failure['test_file']}`
**Test Name**: `{failure['test_name']}`
**Priority**: {failure['priority']}

**Error Summary**:
```
{failure['error_summary']}
```

**Expected Behavior**:
<!-- Describe what the test expects to happen -->

**Actual Behavior**:
<!-- Describe what actually happens -->

**Steps to Reproduce**:
1. Run: `pytest {failure['test_file']}::{failure['test_name']} -v`
2. Observe the failure

**Acceptance Criteria**:
- [ ] Test passes consistently
- [ ] No regression in related functionality  
- [ ] Code coverage maintained or improved
- [ ] Documentation updated if needed

**Related Files**:
- Test file: `{failure['test_file']}`
- Implementation: `{self.guess_implementation_file(failure['test_file'])}`

---
*This issue was automatically generated from test failure detection.*
        """
        
        # GitHub API request
        url = f"{self.github_api}/repos/{self.repo}/issues"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "title": title,
            "body": body,
            "labels": ["bug", "test-failure", f"priority-{failure['priority'].lower()}"],
            "assignees": self.get_component_assignee(failure['component'])
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            issue_url = response.json()["html_url"]
            print(f"Created issue: {issue_url}")
            return issue_url
        else:
            print(f"Failed to create issue: {response.status_code} - {response.text}")
            return None

# Integration with CI/CD
def run_tests_and_create_issues():
    """Complete workflow: run tests, detect failures, create issues."""
    
    # Run pytest and capture output
    result = subprocess.run(
        ["pytest", "app/tests/", "--tb=short", "-v"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:  # Tests failed
        issue_creator = IssueCreator(
            github_token=os.getenv("GITHUB_TOKEN"),
            repo=os.getenv("GITHUB_REPOSITORY")
        )
        
        failures = issue_creator.parse_test_failures(result.stdout)
        
        for failure in failures:
            issue_creator.create_github_issue(failure)
```

## 📁 Key File Locations

### Backend Structure
```
backend/app/
├── main.py                     # FastAPI application entry point
├── core/                       # Core configuration and utilities
│   ├── config.py              # Environment configuration
│   ├── database.py            # Database connection setup
│   ├── security.py            # Authentication and security utilities
│   └── logging.py             # Logging configuration
├── api/v1/                    # API version 1 routes
│   ├── endpoints/             # API endpoint definitions
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── jobs.py           # Job-related endpoints
│   │   ├── users.py          # User management endpoints
│   │   ├── skills.py         # Skill analysis endpoints (NEW)
│   │   └── matching.py       # Job matching endpoints
│   └── deps.py               # Dependency injection utilities
├── models/                    # SQLAlchemy database models
│   ├── user.py               # User model
│   ├── job.py                # Job model
│   ├── skill_gap.py          # Skill gap analysis model (NEW)
│   └── application.py        # Job application model
├── schemas/                   # Pydantic request/response schemas
│   ├── user.py               # User schemas
│   ├── job.py                # Job schemas
│   └── skill_analysis.py     # Skill analysis schemas (NEW)
├── services/                  # Business logic layer
│   ├── resume_parser.py      # AI-powered resume parsing
│   ├── job_aggregator.py     # Multi-source job collection
│   ├── matching_engine.py    # ML-powered job matching
│   ├── skill_analyzer.py     # Skill gap analysis service (NEW)
│   └── notification_service.py # Email and notifications
├── ml/                        # Machine learning modules
│   ├── models/               # ML model implementations
│   ├── preprocessing/        # Data preprocessing pipelines
│   └── training/             # Model training scripts
├── scrapers/                  # Web scraping modules
│   ├── base_scraper.py       # Abstract base scraper
│   ├── linkedin_scraper.py   # LinkedIn job scraping
│   └── rss_parser.py         # RSS feed processing
├── workers/                   # Celery background tasks
│   ├── celery_app.py         # Celery configuration
│   ├── job_scraper.py        # Job scraping tasks
│   ├── skill_analyzer.py     # Skill analysis tasks (NEW)
│   └── notification_sender.py # Email notification tasks
└── tests/                     # Test suites
    ├── unit/                 # Unit tests
    ├── integration/          # Integration tests
    └── fixtures/             # Test data and fixtures
```

### Frontend Structure (Same as JavaScript version)
```
frontend/src/
├── components/                # Reusable UI components
│   ├── JobCard.tsx           # Individual job display
│   ├── SkillGapAnalysis.tsx  # Skill gap analysis component (NEW)
│   └── MatchingDisplay.tsx   # Job matching visualization
├── pages/                     # Main application pages
│   ├── Dashboard.tsx         # Job search and results
│   ├── SkillAnalysis.tsx     # Skill gap analysis page (NEW)
│   └── Settings.tsx          # Application preferences
├── store/                     # Redux state management
├── utils/                     # Utility functions
└── types/                     # TypeScript definitions
```

### Configuration Files
- `backend/requirements.txt`: Python dependencies
- `backend/alembic.ini`: Database migration configuration
- `backend/pytest.ini`: Test configuration
- `backend/.env`: Environment variables
- `frontend/package.json`: Node.js dependencies
- `docker-compose.yml`: Local development setup

## 🔌 External Integrations

### Anthropic Claude API
- Location: `backend/app/utils/claude_client.py`
- Used for: Resume parsing, job description enhancement, skill analysis
- Rate limits: 1000 requests/minute (free tier)
- Error handling: Exponential backoff with fallback to cached responses
- Testing: Mock responses in test environment

### Machine Learning Models
- Location: `backend/app/ml/models/`
- Models: Skill extractor, job matcher, salary predictor, skill recommender
- Training: Automated retraining pipeline with performance monitoring
- Persistence: Models saved in `backend/models/` directory
- Evaluation: Continuous validation against held-out test sets

### Job Board APIs and Scrapers
- LinkedIn: `backend/app/scrapers/linkedin_scraper.py` (Rate limit: 100 requests/hour)
- RemoteOK: `backend/app/scrapers/remoteok_scraper.py` (Rate limit: 60 requests/minute)
- RSS Feeds: `backend/app/scrapers/rss_parser.py` (No rate limits)
- Custom APIs: `backend/app/scrapers/api_integrations.py` (Configurable limits)
- Error handling: Circuit breaker pattern, graceful degradation

### Background Task Processing (Celery)
- Configuration: `backend/app/workers/celery_app.py`
- Broker: Redis for task queue management
- Monitoring: Flower for task monitoring (`celery -A app.workers.celery_app flower`)
- Task routing: Different queues for different task types
- Error handling: Automatic retries with exponential backoff

## 🛡️ Security Guidelines

### API Security
- Input validation: All inputs validated with Pydantic schemas
- Authentication: JWT tokens with refresh token rotation
- Authorization: Role-based access control (RBAC)
- Rate limiting: 1000 requests/hour per user, 100/minute for heavy endpoints
- CORS: Configured for frontend domain only
- HTTPS: Enforced in production with proper certificate management

### Data Protection
- Password hashing: bcrypt with minimum 12 rounds
- Sensitive data: Encrypted at rest using AES-256
- API keys: Stored in environment variables, never in code
- Database: Connection string encryption, audit logging enabled
- File uploads: Virus scanning, file type validation, size limits

### ML Model Security
- Model files: Integrity verification with checksums
- Training data: Anonymization of sensitive information
- Inference: Input sanitization to prevent adversarial attacks
- Model serving: Isolated containers with minimal permissions

## 🧪 Testing Guidelines

### Test Organization
- Unit tests: `backend/app/tests/unit/` - Fast, isolated tests
- Integration tests: `backend/app/tests/integration/` - Database and API tests
- ML tests: `backend/app/tests/ml/` - Model performance and regression tests
- End-to-end tests: `backend/app/tests/e2e/` - Complete workflow tests

### Test Data Management
- Fixtures: `backend/app/tests/fixtures/` - Reusable test data
- Database: Separate test database with cleanup between tests
- Mock services: Mock external APIs to avoid rate limits and costs
- Test isolation: Each test should be independent and repeatable

### Coverage Requirements
- Minimum coverage: 80% for all code
- Critical paths: 95% coverage for core business logic
- ML models: Separate evaluation metrics (accuracy, precision, recall)
- Integration tests: Cover all API endpoints and database operations

### Performance Testing
- Load testing: Simulate high user loads with locust
- Database performance: Monitor query execution times
- ML inference: Benchmark model prediction latency
- Memory usage: Profile memory consumption under load

## 🚀 Deployment Considerations

### Railway Backend Deployment
- Python version: 3.11+ specified in `runtime.txt`
- Dependencies: `requirements.txt` with pinned versions
- Database migrations: Automatic migration on deployment
- Environment variables: Set via Railway dashboard or CLI
- Health checks: `/health` endpoint for monitoring
- Logging: Structured logging with JSON format

### Celery Worker Deployment
- Separate Railway service for Celery workers
- Auto-scaling based on queue length
- Dead letter queues for failed tasks
- Monitoring via Flower or Railway metrics
- Graceful shutdown handling

### ML Model Deployment
- Model artifacts: Stored in Railway persistent volumes or S3
- Model versioning: Track model versions and performance
- A/B testing: Gradual rollout of new models
- Fallback strategies: Revert to previous model if performance degrades

## 🔍 Debugging and Monitoring

### Local Development
- Logging: Use Python logging module with appropriate levels
- Database queries: Enable SQLAlchemy query logging
- API debugging: FastAPI automatic documentation at `/docs`
- ML debugging: Jupyter notebooks for model analysis
- Performance profiling: cProfile for performance bottlenecks

### Production Monitoring
- Application metrics: Response times, error rates, throughput
- Database monitoring: Query performance, connection pool usage
- ML model monitoring: Prediction accuracy, data drift detection
- Resource usage: CPU, memory, disk usage via Railway dashboard
- Error tracking: Sentry integration for error reporting

### Common Issues and Solutions
- **Database connection errors**: Check DATABASE_URL and connection pool settings
- **Celery tasks not processing**: Verify Redis connection and worker status
- **ML model loading failures**: Check model file integrity and dependencies
- **High memory usage**: Profile code for memory leaks, optimize data processing
- **Slow API responses**: Add database indexes, implement caching, optimize queries

## 📦 Dependencies Management

### Python Backend Dependencies
- **Core Framework**: FastAPI 0.104+, uvicorn, pydantic
- **Database**: SQLAlchemy 2.0+, alembic, psycopg2-binary
- **ML/AI**: scikit-learn, pandas, numpy, spacy, anthropic
- **Task Queue**: celery, redis
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Security**: passlib, python-jose, bcrypt

### Development Dependencies
- **Code Quality**: black, flake8, mypy, isort
- **Testing**: pytest-mock, factory-boy, faker
- **Debugging**: ipdb, pytest-xdist
- **Documentation**: sphinx, mkdocs

### Version Management
- Use `requirements.txt` for production dependencies
- Use `requirements-dev.txt` for development dependencies
- Pin major versions, allow minor updates: `fastapi>=0.104,<0.105`
- Regular security updates with `pip-audit`

## 🎯 Performance Considerations

### Backend Optimization
- **Database**: Connection pooling, query optimization, proper indexes
- **API**: Async endpoints for I/O operations, response caching
- **ML Models**: Model caching, batch prediction for efficiency
- **Memory**: Efficient data structures, garbage collection tuning
- **Concurrency**: Proper use of async/await, connection limits

### ML Model Performance
- **Training**: Distributed training for large datasets
- **Inference**: Model quantization, ONNX conversion for speed
- **Caching**: Cache frequent predictions, feature preprocessing
- **Batch processing**: Process multiple predictions together
- **Model serving**: Load balancing across multiple model instances

### Database Optimization
- **Indexes**: Add indexes for frequently queried columns
- **Queries**: Use SQLAlchemy select() with proper joins
- **Connection pooling**: Configure appropriate pool sizes
- **Read replicas**: Separate read/write operations for scaling
- **Query monitoring**: Track slow queries and optimize

## 🔄 Continuous Integration/Deployment

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Hooks run automatically on commit:
# - black (code formatting)
# - flake8 (linting)  
# - mypy (type checking)
# - pytest (run tests)
# - security checks (bandit)
```

### CI/CD Pipeline
```yaml
# .github/workflows/ci.yml example structure
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Railway
        run: railway up
```

### Deployment Checklist
- [ ] All tests passing
- [ ] Code coverage >= 80%
- [ ] Security scan passed
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] ML models trained and validated
- [ ] Monitoring alerts configured
- [ ] Rollback plan prepared
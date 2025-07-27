## 🚀 MVP Development Roadmap

### MVP Philosophy
Build **clean foundation quickly** → enhance iteratively. Avoid shortcuts that create technical debt, but start with simpler implementations that can be improved.

### 5-Day MVP Sprint Plan

#### Day 1: Foundation & Setup (8 hours)
**Morning (4 hours): Backend Foundation**
```bash
# Proper FastAPI structure (no shortcuts)
mkdir backend && cd backend
python -m venv venv && source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic

# Create proper project structure
mkdir -p app/models app/schemas app/api/v1/endpoints app/core
touch app/main.py app/core/config.py app/core/database.py

# Database setup with proper migrations
alembic init alembic
# Create User, Job, JobMatch models with proper relationships

# Deploy to Railway immediately
railway new job-tracker-mvp
railway add postgresql
railway up
```

**Afternoon (4 hours): Frontend Foundation**
```bash
# React setup with proper TypeScript structure
npx create-react-app frontend --template typescript
cd frontend && npm install tailwindcss @types/react-router-dom

# Create proper component structure
mkdir -p src/components src/pages src/utils src/types
# Basic routing, authentication context, API client setup

# Deploy to Vercel immediately
vercel --prod
```

**End of Day 1 Deliverables:**
- ✅ Working authentication (register/login) - 66/66 backend auth tests passing
- ✅ Database with proper schema - User model with SQLAlchemy + authentication system
- ✅ Core configuration module - Issue #27 implemented with comprehensive tests
- ❌ Deployed backend + frontend - Ready for deployment
- ✅ Basic routing and protected pages - Frontend builds successfully
- ✅ **BONUS**: Resume upload endpoint (Day 3 feature completed early) - Issue #26 with comprehensive tests

#### Day 2: Core Job Features (8 hours)
**Morning (4 hours): Job Data Layer**
```python
# Create job data in separate, easily replaceable module
# backend/app/data/sample_jobs.py
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Senior Data Scientist - Remote LATAM",
        "company": "TechCorp International",
        "location": "Remote (Brazil timezone)", 
        "salary": "$12,000 - $18,000 USD/month",
        "description": "Join our AI team building ML solutions for global markets...",
        "requirements": ["Python", "Machine Learning", "SQL", "TensorFlow", "AWS"],
        "posted_date": "2024-01-15",
        "apply_url": "https://techcorp.com/careers/senior-data-scientist",
        "source": "LinkedIn",
        "remote": True
    },
    # Add 49 more REAL job postings from manual research
]

# Proper service layer for easy replacement later
# backend/app/services/job_service.py
class JobService:
    def get_jobs(self) -> List[Job]:
        # Currently returns sample data, will be replaced with scraping
        return [Job(**job_data) for job_data in SAMPLE_JOBS]
    
    def search_jobs(self, query: str, skills: List[str]) -> List[Job]:
        # Simple filtering now, ML-powered later
        jobs = self.get_jobs()
        return [job for job in jobs if any(skill in job.requirements for skill in skills)]
```

**Afternoon (4 hours): Job Display & Basic Matching**
```typescript
// Frontend job components with proper structure
// frontend/src/components/JobCard.tsx
interface JobCardProps {
  job: Job;
  userSkills: string[];
  onSave: (jobId: string) => void;
  onApply: (job: Job) => void;
}

// Simple but proper matching algorithm (easily enhanced later)
// frontend/src/utils/jobMatching.ts
export const calculateMatchScore = (jobSkills: string[], userSkills: string[]): number => {
  // Simple keyword matching now, will be replaced with ML
  const matches = jobSkills.filter(skill => 
    userSkills.some(userSkill => 
      skill.toLowerCase().includes(userSkill.toLowerCase())
    )
  );
  return Math.round((matches.length / jobSkills.length) * 100);
};
```

**End of Day 2 Deliverables:**
- ❌ 50 real job listings displayed
- ❌ Basic search and filtering
- ❌ Simple match score calculation
- ❌ Save/unsave job functionality

#### Day 3: Resume Processing (8 hours)
**Morning (4 hours): Resume Upload & Text Extraction**
```python
# Simple but extensible resume processing
# backend/app/services/resume_service.py
from PyPDF2 import PdfReader
from typing import Dict, List

class ResumeService:
    def process_resume(self, file_content: bytes, filename: str) -> Dict:
        # Extract text (will be enhanced with Claude API later)
        text = self.extract_text_from_pdf(file_content)
        
        # Simple skill extraction (will be replaced with NLP)
        skills = self.extract_skills_simple(text)
        
        # Basic info extraction (will be enhanced with AI)
        profile_info = self.extract_basic_info(text)
        
        return {
            "skills": skills,
            "experience_level": profile_info.get("experience_level", "mid"),
            "name": profile_info.get("name", ""),
            "raw_text": text[:500]  # Store sample for debugging
        }
    
    def extract_skills_simple(self, text: str) -> List[str]:
        # Simple keyword matching (easily replaceable)
        skill_keywords = [
            "Python", "R", "SQL", "Machine Learning", "TensorFlow", 
            "PyTorch", "AWS", "GCP", "Docker", "Kubernetes"
        ]
        found_skills = []
        text_lower = text.lower()
        
        for skill in skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
```

**Afternoon (4 hours): Profile Management**
```typescript
// Frontend profile and resume upload
// frontend/src/pages/Profile.tsx
const Profile: React.FC = () => {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  
  const handleResumeUpload = async (file: File) => {
    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append('resume', file);
      
      const response = await apiClient.post('/users/resume', formData);
      setResumeData(response.data);
      
      // Update user skills for job matching
      await updateUserSkills(response.data.skills);
    } catch (error) {
      console.error('Resume upload failed:', error);
    } finally {
      setIsUploading(false);
    }
  };
  
  // Simple but complete profile management
};
```

**End of Day 3 Deliverables:**
- ❌ Resume upload working (PDF support)
- ❌ Basic skill extraction from resume
- ❌ User profile with extracted skills
- ❌ Job matching uses user skills

#### Day 4: AI Enhancement (8 hours)
**Morning (4 hours): Claude API Integration**
```python
# Replace simple extraction with Claude API
# backend/app/services/claude_service.py
import anthropic
from typing import Dict

class ClaudeResumeParser:
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    async def parse_resume(self, resume_text: str) -> Dict:
        prompt = f"""
        Analyze this resume and extract information in JSON format:
        
        {{
          "name": "candidate name",
          "experience_level": "junior|mid|senior|lead",
          "skills": ["Python", "Machine Learning", "SQL"],
          "location": "city, country",
          "summary": "2-sentence professional summary"
        }}
        
        Resume text: {resume_text}
        
        Return only valid JSON, no other text.
        """
        
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.content[0].text)

# Update ResumeService to use Claude
# backend/app/services/resume_service.py (enhanced)
class ResumeService:
    def __init__(self):
        self.claude_parser = ClaudeResumeParser()
        self.simple_parser = SimpleResumeParser()  # Keep as fallback
    
    async def process_resume(self, file_content: bytes, filename: str) -> Dict:
        text = self.extract_text_from_pdf(file_content)
        
        try:
            # Try Claude API first
            result = await self.claude_parser.parse_resume(text)
            result["parsing_method"] = "claude_api"
        except Exception as e:
            # Fallback to simple parsing
            logger.warning(f"Claude API failed, using fallback: {e}")
            result = self.simple_parser.parse_resume(text)
            result["parsing_method"] = "simple_fallback"
        
        return result
```

**Afternoon (4 hours): Enhanced Matching**
```python
# Improve matching algorithm while keeping it simple
# backend/app/services/matching_service.py
class MatchingService:
    def calculate_match_score(self, user_profile: Dict, job: Dict) -> int:
        # Enhanced but still simple algorithm
        
        # Skills matching (60% weight)
        user_skills = [skill.lower() for skill in user_profile.get("skills", [])]
        job_skills = [skill.lower() for skill in job.get("requirements", [])]
        
        skill_matches = len(set(user_skills) & set(job_skills))
        skill_score = (skill_matches / max(len(job_skills), 1)) * 100
        
        # Experience level matching (25% weight)
        exp_mapping = {"junior": 1, "mid": 2, "senior": 3, "lead": 4}
        user_exp = exp_mapping.get(user_profile.get("experience_level", "mid"), 2)
        job_exp = exp_mapping.get(job.get("seniority_level", "mid"), 2)
        exp_score = max(0, 100 - abs(user_exp - job_exp) * 25)
        
        # Location matching (15% weight)
        location_score = 100 if job.get("remote") else 70
        
        # Calculate weighted average
        total_score = (skill_score * 0.6) + (exp_score * 0.25) + (location_score * 0.15)
        
        return min(100, max(0, int(total_score)))
```

**End of Day 4 Deliverables:**
- ❌ AI-powered resume parsing with Claude API
- ❌ Enhanced job matching algorithm
- ❌ Fallback systems for reliability
- ❌ Improved match score accuracy

#### Day 5: Polish & Launch (8 hours)
**Morning (4 hours): UX Improvements**
```typescript
// Enhanced dashboard with statistics
// frontend/src/pages/Dashboard.tsx
const Dashboard: React.FC = () => {
  const { jobs, loading } = useJobs();
  const { user } = useAuth();
  const userSkills = user?.skills || [];
  
  const matchedJobs = jobs.filter(job => 
    calculateMatchScore(job.requirements, userSkills) >= 70
  );
  
  const stats = {
    totalJobs: jobs.length,
    highMatches: jobs.filter(job => 
      calculateMatchScore(job.requirements, userSkills) >= 80
    ).length,
    savedJobs: user?.savedJobs?.length || 0,
    averageMatch: Math.round(
      jobs.reduce((acc, job) => 
        acc + calculateMatchScore(job.requirements, userSkills), 0
      ) / jobs.length
    )
  };
  
  return (
    <div className="space-y-6">
      {/* Stats cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard title="Total Jobs" value={stats.totalJobs} />
        <StatCard title="High Matches" value={stats.highMatches} />
        <StatCard title="Saved Jobs" value={stats.savedJobs} />
        <StatCard title="Avg Match" value={`${stats.averageMatch}%`} />
      </div>
      
      {/* Job listings with improved filtering */}
      <JobFilters onFilterChange={handleFilterChange} />
      <JobGrid jobs={matchedJobs} userSkills={userSkills} />
    </div>
  );
};
```

**Afternoon (4 hours): Launch Preparation**
```bash
# Production deployment checklist
# Backend optimizations
pip install gunicorn  # Production WSGI server
# Add health check endpoint
# Configure logging
# Set up error monitoring

# Frontend optimizations  
npm run build  # Optimize bundle
# Configure error boundaries
# Add loading states
# Test responsive design

# Final deployment
railway deploy --prod
vercel --prod

# Post-deployment verification
curl https://your-api.railway.app/health
# Test complete user flow
# Verify database connections
# Check Claude API integration
```

**End of Day 5 Deliverables:**
- ❌ Production-ready deployment
- ❌ User dashboard with statistics
- ❌ Error handling and loading states
- ❌ Complete user onboarding flow
- ❌ Ready for user feedback

### MVP Success Metrics
- **Technical**: 99% uptime, <2s page load, all API endpoints working
- **User**: 10 signups in first week, 5 resume uploads, average 75%+ match scores
- **Business**: User feedback collected, feature priorities identified

### Post-MVP Enhancement Roadmap

#### Week 2: First Iteration (Based on User Feedback)
**High-Priority Enhancements:**
```python
# Replace hardcoded jobs with live scraping
# backend/app/scrapers/linkedin_scraper.py
class LinkedInScraper:
    def scrape_jobs(self, query: str = "data scientist remote brazil") -> List[Dict]:
        # Implement actual LinkedIn job scraping
        # Use Scrapy or requests + BeautifulSoup
        pass

# Add basic email notifications
# backend/app/services/notification_service.py  
class NotificationService:
    def send_job_alert(self, user_email: str, new_jobs: List[Job]):
        # Send weekly digest of new matching jobs
        pass
```

#### Week 3: Advanced Features
```python
# Add skill gap analysis (simplified version)
# backend/app/services/skill_analyzer.py
class SkillAnalyzer:
    def analyze_missing_skills(self, user_skills: List[str], target_jobs: List[Job]) -> Dict:
        # Identify skills missing from user profile
        # Suggest learning resources
        pass

# Background job processing
# backend/app/workers/job_scraper.py
@celery_app.task
def scrape_all_job_sources():
    # Daily job scraping from multiple sources
    pass
```

#### Week 4: Scale Preparation
- Performance optimization
- Database indexing
- Caching layer (Redis)
- User analytics
- A/B testing infrastructure

### Development Guidelines for MVP

#### Code Quality Standards (Even for MVP)
```python
# Always use proper error handling
try:
    result = external_api_call()
except APIError as e:
    logger.error(f"API call failed: {e}")
    return fallback_response()

# Always use environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Always use proper typing
def calculate_match_score(user_skills: List[str], job_skills: List[str]) -> int:
    # Implementation here
    pass

# Always separate concerns
class JobService:  # Business logic
    pass

class JobRepository:  # Data access
    pass

class JobController:  # HTTP handling
    pass
```

#### Testing Strategy for MVP
```python
# Minimum viable tests (focus on critical paths)
def test_user_registration():
    # Test user can register successfully
    pass

def test_resume_upload_and_parsing():
    # Test complete resume processing flow
    pass

def test_job_matching_calculation():
    # Test matching algorithm accuracy
    pass

def test_claude_api_integration():
    # Test AI resume parsing with mocked responses
    pass

# Integration test for complete user flow
def test_complete_user_journey():
    # Register -> Upload resume -> View matched jobs -> Save job
    pass
```

#### Deployment Pipeline for MVP
```yaml
# .github/workflows/deploy.yml (simple but effective)
name: Deploy MVP
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest app/tests/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Railway
        run: railway up
      - name: Deploy to Vercel
        run: vercel --prod
```

### MVP vs Full Product Transition Strategy

#### Designed for Enhancement (Not Replacement)
```python
# MVP approach - simple but extensible
class ResumeService:
    def parse_resume(self, file_content: bytes) -> Dict:
        # MVP: Simple keyword extraction
        # Full: Claude API + NLP models + ML enhancement
        pass

# Full product enhancement - same interface, better implementation
class ResumeService:
    def __init__(self):
        self.claude_parser = ClaudeParser()
        self.ml_model = SkillExtractionModel()
        self.nlp_pipeline = SpacyPipeline()
    
    def parse_resume(self, file_content: bytes) -> Dict:
        # Enhanced implementation, same interface
        pass
```

#### Feature Flag System for Gradual Rollout
```python
# backend/app/core/feature_flags.py
class FeatureFlags:
    USE_CLAUDE_API = os.getenv("USE_CLAUDE_API", "true") == "true"
    USE_ML_MATCHING = os.getenv("USE_ML_MATCHING", "false") == "true"
    ENABLE_SKILL_ANALYSIS = os.getenv("ENABLE_SKILL_ANALYSIS", "false") == "true"

# Usage in services
if FeatureFlags.USE_CLAUDE_API:
    result = await self.claude_parser.parse_resume(text)
else:
    result = self.simple_parser.parse_resume(text)
```

This MVP roadmap ensures you build a **solid foundation quickly** that can be **enhanced iteratively** without architectural rewrites. Each day builds upon the previous with **proper software engineering practices** from day one.

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
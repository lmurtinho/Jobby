# AI Job Tracker - Outside-In TDD Workflow Starter

This repository implements the **Issue-Driven Development with Outside-In TDD** workflow described in the project documentation.

## 🎯 Quick Start

The fastest way to begin development is to run the high-level integration test and let it drive the creation of specific implementation issues.

### 1. Setup
```bash
# Install basic dependencies
pip install -r scripts/workflow_requirements.txt

# Install backend dependencies (optional, for full development)
pip install -r backend/requirements.txt

# Set up GitHub token (optional, for automatic issue creation)
export GITHUB_TOKEN="your_github_personal_access_token"
```

### 2. Run the Workflow Starter
```bash
# Run the complete workflow (will fail initially, creating issues)
python scripts/workflow_starter.py

# Or run in dry-run mode to see what would happen
python scripts/workflow_starter.py --dry-run

# Create initial project structure
python scripts/workflow_starter.py --create-structure
```

### 3. What Happens Next

1. **Integration Test Runs**: The `test_complete_workflow.py` executes and captures all failures
2. **Issues Generated**: Each failure becomes a specific GitHub issue with acceptance criteria
3. **Roadmap Created**: A `DEVELOPMENT_ROADMAP.md` file shows the implementation order
4. **TDD Begins**: Start implementing components based on highest priority issues

## 📋 The High-Level Test

The `backend/app/tests/integration/test_complete_workflow.py` file contains a comprehensive integration test that covers:

- ✅ **User Registration & Authentication** 
- ✅ **Resume Upload & AI Parsing** (Claude API)
- ✅ **Multi-Source Job Scraping** (LinkedIn, RemoteOK, RSS feeds)
- ✅ **ML-Powered Job Matching** (TF-IDF, cosine similarity)
- ✅ **Skill Gap Analysis** (AI-powered recommendations)
- ✅ **Email Notifications** (SendGrid integration)
- ✅ **Application Tracking** (Interview prep, follow-ups)
- ✅ **Background Processing** (Celery tasks)

This test represents the complete user journey and business value of the AI Job Tracker.

## 🔄 Development Workflow

### Outside-In TDD Process
1. **Large Integration Test Fails** → Identifies missing components
2. **GitHub Issues Created** → Each failure becomes a specific task
3. **Unit Tests Written** → TDD implementation for each component  
4. **Component Implemented** → Make unit tests pass
5. **Integration Test Re-run** → See progress, identify next failures
6. **Repeat** → Until full integration test passes

### Example Issue Flow
```
Integration Test Fails: "ModuleNotFoundError: No module named 'app.models.user'"
                    ↓
GitHub Issue Created: "Epic: Implement app.models.user - User database model"
                    ↓
Unit Tests Written: test_user_model_creation(), test_user_validation(), etc.
                    ↓
Implementation: SQLAlchemy User model with all required fields
                    ↓
Unit Tests Pass: User model functionality works
                    ↓
Integration Test: Progresses further, finds next missing component
```

## 📊 Generated Artifacts

### 1. GitHub Issues
Each test failure creates a structured GitHub issue with:
- **Clear Title**: Component and specific problem
- **Acceptance Criteria**: Detailed requirements
- **Implementation Notes**: Technical guidance
- **Dependencies**: Which components must be built first
- **Estimates**: Time and complexity

### 2. Development Roadmap
The `DEVELOPMENT_ROADMAP.md` file provides:
- **Phase-based Planning**: Infrastructure → Business Logic → Enhancements
- **Dependency Graph**: Component build order
- **Time Estimates**: Total hours and per-component
- **Progress Tracking**: Checkboxes for completion

### 3. Project Structure
Initial directory structure following the documentation:
```
backend/
├── app/
│   ├── core/           # Configuration, database, security
│   ├── api/v1/         # FastAPI endpoints
│   ├── models/         # SQLAlchemy database models
│   ├── services/       # Business logic (resume parsing, matching)
│   ├── ml/             # Machine learning components
│   ├── scrapers/       # Job board scrapers
│   ├── workers/        # Celery background tasks
│   └── tests/          # Unit and integration tests
frontend/src/           # React application
docs/                   # Documentation
scripts/                # Automation scripts
```

## 🧪 Running Tests

```bash
# Run the high-level integration test
pytest backend/app/tests/integration/test_complete_workflow.py::TestCompleteJobTrackingWorkflow::test_complete_ai_job_tracker_workflow -v

# Run all tests (as components get built)
pytest backend/app/tests/ -v

# Run specific component tests
pytest backend/app/tests/unit/services/test_skill_analyzer.py -v

# Run with coverage
pytest --cov=backend/app --cov-report=html
```

## 🏗️ Component Implementation Guide

### 1. Start with Infrastructure (Phase 1)
- **app.core**: Database connection, configuration, security
- **app.models**: SQLAlchemy models for User, Job, Application
- **app.main**: FastAPI application setup

### 2. Build API Layer (Phase 2)  
- **app.api.v1.endpoints**: REST endpoints for auth, jobs, users
- **app.schemas**: Pydantic request/response models

### 3. Implement Business Logic (Phase 3)
- **app.services.resume_parser**: Claude AI integration
- **app.services.matching_engine**: ML-powered job matching
- **app.services.skill_analyzer**: Skill gap analysis

### 4. Add Data Collection (Phase 4)
- **app.scrapers**: LinkedIn, RemoteOK, RSS feed scrapers
- **app.workers**: Celery background task processing

## 📈 Success Metrics

The development is complete when:
- [ ] **Integration test passes end-to-end**
- [ ] **All GitHub issues resolved**  
- [ ] **Core user journey works**: Registration → Resume → Job Matches → Skill Analysis → Alerts
- [ ] **Background processing active**: Automated job scraping and notifications
- [ ] **ML pipeline functional**: Resume parsing, job matching, skill recommendations

## 🎯 Key Benefits of This Approach

1. **Clear Direction**: Integration test shows exactly what needs to be built
2. **Prioritized Work**: Failures indicate which components are most critical  
3. **Measurable Progress**: Each issue completion moves closer to working system
4. **Quality Assurance**: TDD ensures each component works correctly
5. **Stakeholder Communication**: GitHub issues provide transparency
6. **Technical Debt Prevention**: Outside-in approach ensures proper architecture

## 🔧 Customization

### Modify the Integration Test
Edit `backend/app/tests/integration/test_complete_workflow.py` to:
- Add new user journey steps
- Change expected behavior
- Add new integrations
- Modify success criteria

### Adjust Issue Generation
Edit `scripts/workflow_starter.py` to:
- Change component priorities
- Modify acceptance criteria templates
- Add custom GitHub labels
- Adjust time estimates

### Configure Project Structure  
Update directory creation in `scripts/workflow_starter.py` for:
- Different framework choices
- Additional service layers
- Custom tool integrations

## 📚 Documentation References

- **CLAUDE.md**: Complete TDD workflow and coding standards
- **README.md**: Full project specification and architecture
- **Generated Issues**: Specific implementation requirements
- **Development Roadmap**: Phase-based implementation plan

---

## 🚀 Ready to Start?

```bash
# Begin the journey
python workflow_starter.py
```

This will run the integration test, create your GitHub issues, and generate a development roadmap. From there, start with the highest priority issues and use TDD to implement each component.

The integration test will guide you every step of the way! 🎯

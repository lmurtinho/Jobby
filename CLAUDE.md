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
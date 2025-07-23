# AI Job Tracker for Brazil/LATAM

A comprehensive job tracking application that automatically finds, scores, and manages AI/ML/Data Science job opportunities for remote workers in Brazil and Latin America, built with Python and advanced machine learning capabilities.

## 🎯 Overview

This application combines AI-powered resume parsing, multi-source job aggregation, intelligent matching, skill gap analysis, and automated notifications to create a complete job hunting solution for data professionals in the LATAM market.

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI with Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Task Queue**: Celery with Redis
- **AI Processing**: Anthropic Claude API + scikit-learn + spaCy
- **Data Processing**: pandas + numpy for advanced analytics
- **Web Scraping**: Scrapy + BeautifulSoup + Selenium
- **Authentication**: FastAPI-Users with JWT

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit + RTK Query
- **File Handling**: React Dropzone for resume uploads
- **Charts/Analytics**: Recharts + Plotly.js for advanced visualizations
- **Deployment**: Vercel

### External Services
- **AI Processing**: Anthropic Claude API for resume parsing and job matching
- **Email**: SendGrid for notifications
- **Monitoring**: Sentry for error tracking + Railway analytics
- **File Storage**: Railway disk storage or AWS S3

## 📁 Project Structure

```
ai-job-tracker-python/
├── frontend/                    # React application (same as JS version)
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── JobCard.tsx
│   │   │   ├── ResumeUpload.tsx
│   │   │   ├── SourceManager.tsx
│   │   │   ├── SkillGapAnalysis.tsx    # NEW: Skill recommendations
│   │   │   └── MatchingAlgorithm.tsx
│   │   ├── pages/              # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Profile.tsx
│   │   │   ├── SavedJobs.tsx
│   │   │   ├── Sources.tsx
│   │   │   ├── SkillAnalysis.tsx       # NEW: Skill gap analysis page
│   │   │   └── Settings.tsx
│   │   ├── store/              # Redux store
│   │   ├── utils/              # Utility functions
│   │   └── types/              # TypeScript definitions
│   └── package.json
├── backend/                     # Python FastAPI application
│   ├── app/
│   │   ├── main.py             # FastAPI application entry
│   │   ├── core/               # Core configuration
│   │   │   ├── config.py       # Settings and environment
│   │   │   ├── database.py     # Database connection
│   │   │   ├── security.py     # Authentication utilities
│   │   │   └── logging.py      # Logging configuration
│   │   ├── api/                # API routes
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── jobs.py
│   │   │   │   │   ├── profiles.py
│   │   │   │   │   ├── sources.py
│   │   │   │   │   ├── skills.py        # NEW: Skill analysis endpoints
│   │   │   │   │   └── matching.py
│   │   │   │   └── api.py
│   │   │   └── deps.py         # Dependencies
│   │   ├── models/             # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   ├── application.py
│   │   │   ├── source.py
│   │   │   ├── skill.py        # NEW: Skill tracking
│   │   │   └── skill_gap.py    # NEW: Skill gap analysis
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   ├── source.py
│   │   │   ├── skill_analysis.py      # NEW: Skill gap schemas
│   │   │   └── matching.py
│   │   ├── services/           # Business logic
│   │   │   ├── resume_parser.py       # AI-powered resume parsing
│   │   │   ├── job_aggregator.py      # Multi-source job collection
│   │   │   ├── matching_engine.py     # ML-powered job matching
│   │   │   ├── skill_analyzer.py      # NEW: Skill gap analysis
│   │   │   ├── source_manager.py      # Custom source management
│   │   │   └── notification_service.py # Email and alert system
│   │   ├── scrapers/           # Web scraping modules
│   │   │   ├── base_scraper.py        # Abstract base scraper
│   │   │   ├── linkedin_scraper.py    # LinkedIn job scraping
│   │   │   ├── remoteok_scraper.py    # RemoteOK scraping
│   │   │   ├── angellist_scraper.py   # AngelList scraping
│   │   │   ├── rss_parser.py          # RSS feed processing
│   │   │   └── api_integrations.py    # Job board APIs
│   │   ├── ml/                 # Machine learning modules
│   │   │   ├── models/         # ML model definitions
│   │   │   │   ├── skill_extractor.py # NLP for skill extraction
│   │   │   │   ├── job_matcher.py     # ML-based matching
│   │   │   │   └── skill_recommender.py # NEW: Skill recommendation ML
│   │   │   ├── preprocessing/  # Data preprocessing
│   │   │   │   ├── text_cleaner.py
│   │   │   │   ├── feature_extractor.py
│   │   │   │   └── skill_normalizer.py
│   │   │   └── training/       # Model training scripts
│   │   │       ├── train_matcher.py
│   │   │       └── train_skill_recommender.py
│   │   ├── workers/            # Celery background tasks
│   │   │   ├── celery_app.py          # Celery configuration
│   │   │   ├── job_scraper.py         # Scheduled job scraping
│   │   │   ├── match_calculator.py    # Job matching computation
│   │   │   ├── skill_analyzer.py      # NEW: Skill gap analysis worker
│   │   │   └── notification_sender.py # Email notifications
│   │   ├── utils/              # Utility functions
│   │   │   ├── claude_client.py       # Anthropic API wrapper
│   │   │   ├── email_client.py        # SendGrid integration
│   │   │   ├── data_processor.py      # pandas/numpy utilities
│   │   │   ├── file_handler.py        # File upload/processing
│   │   │   └── validators.py          # Data validation
│   │   └── tests/              # Test suites
│   │       ├── unit/           # Unit tests
│   │       ├── integration/    # Integration tests
│   │       └── fixtures/       # Test data
│   ├── requirements.txt        # Python dependencies
│   ├── alembic/               # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── Dockerfile
│   └── pytest.ini
├── docs/                       # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── ML_MODELS.md           # NEW: ML model documentation
│   └── SKILL_ANALYSIS.md      # NEW: Skill gap analysis guide
├── scripts/                    # Automation scripts
│   ├── setup.sh
│   ├── train_models.py        # NEW: ML model training
│   └── deploy.sh
└── README.md
```

## 🔧 Core Features

### 1. AI-Powered Resume Parsing
- **Claude Integration**: Extract skills, experience, education from PDF/Word resumes
- **NLP Enhancement**: spaCy + custom models for skill extraction
- **Skill Normalization**: Map variations to standard skill names
- **Experience Calculation**: ML-based seniority level determination
- **Multi-language Support**: Portuguese, English, Spanish

### 2. Advanced Skill Gap Analysis (NEW)
- **Resume vs Job Comparison**: Identify missing skills for specific positions
- **Skill Importance Scoring**: ML model ranks skill importance by job market demand
- **Learning Path Recommendations**: Suggest courses and resources for skill development
- **Progress Tracking**: Monitor skill acquisition over time
- **Market Trend Analysis**: Track emerging skills in AI/ML job market

### 3. Multi-Source Job Aggregation
- **Built-in Sources**:
  - LinkedIn Jobs API
  - RemoteOK Scrapy spider
  - AngelList/Wellfound API
  - Indeed RSS feeds
  - Glassdoor API
  - AI Jobs Board
  - LATAM-specific job boards

- **Custom Source Management**:
  - RSS feed integration with pandas processing
  - REST API connections with automated schema detection
  - Web scraping configurations with Scrapy
  - User-submitted job boards

### 4. ML-Powered Job Matching
- **Advanced Scoring Algorithm**: 
  - TF-IDF + cosine similarity for skills (40%)
  - Experience level compatibility (25%)
  - Location/timezone analysis (20%)
  - Salary range optimization (15%)
- **Machine Learning**: scikit-learn models improve matching over time
- **Preference Learning**: Collaborative filtering for personalized recommendations
- **Skill Embeddings**: Word2Vec for semantic skill matching

### 5. Automated Job Discovery
- **Celery Task Queue**: Distributed job processing
- **Scheduled Scraping**: Configurable intervals with smart rate limiting
- **Real-time Updates**: WebSocket integration for live job notifications
- **Duplicate Detection**: Advanced deduplication using ML similarity
- **Quality Filtering**: ML classifier removes low-quality postings

### 6. Enhanced Application Tracking
- **Status Management**: Applied, Interview, Offer, Rejected with timestamps
- **Timeline Analytics**: Pandas-powered application success analysis
- **Interview Preparation**: Skill gap analysis for upcoming interviews
- **Follow-up Intelligence**: ML-predicted optimal follow-up timing
- **Salary Negotiation**: Market data analysis for salary recommendations

## 🔌 Custom Job Sources

### Adding RSS Feeds
```python
# Example RSS source configuration
from pydantic import BaseModel
from typing import List, Optional

class RSSSourceConfig(BaseModel):
    name: str
    url: str
    category: str  # 'data-science', 'machine-learning', 'ai', 'general'
    filters: dict
    parse_config: dict
    active: bool = True
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Data Science Central Jobs",
                "url": "https://datasciencecentral.com/jobs/feed/",
                "category": "data-science",
                "filters": {
                    "keywords": ["python", "machine learning", "remote"],
                    "locations": ["Brazil", "Remote", "LATAM"],
                    "exclude_keywords": ["on-site", "senior only"]
                },
                "parse_config": {
                    "title_field": "title",
                    "description_field": "description", 
                    "link_field": "link",
                    "date_field": "pubDate"
                },
                "active": True
            }
        }
```

### API Integration
```python
# Example API source configuration
class APISourceConfig(BaseModel):
    name: str
    endpoint: str
    authentication: dict
    request_config: dict
    response_mapping: dict
    rate_limiting: dict
    
    class Config:
        schema_extra = {
            "example": {
                "name": "RemoteOK API",
                "endpoint": "https://remoteok.io/api",
                "authentication": {
                    "type": "api-key",
                    "header": "X-API-Key",
                    "value": "${API_KEY}"
                },
                "request_config": {
                    "method": "GET",
                    "params": {
                        "tags": "data science,machine learning",
                        "location": "anywhere"
                    }
                },
                "response_mapping": {
                    "jobs_path": "$.jobs[*]",
                    "title_path": "$.position",
                    "company_path": "$.company",
                    "salary_path": "$.salary",
                    "description_path": "$.description"
                },
                "rate_limiting": {
                    "requests_per_minute": 60,
                    "requests_per_day": 1000
                }
            }
        }
```

### Web Scraping Configuration
```python
# Example Scrapy scraper configuration
class ScraperConfig(BaseModel):
    name: str
    base_url: str
    search_url: str
    selectors: dict
    pagination: dict
    anti_bot: dict
    
    class Config:
        schema_extra = {
            "example": {
                "name": "TechJobs Brasil",
                "base_url": "https://techjobs.com.br",
                "search_url": "https://techjobs.com.br/vagas?q={query}&l={location}",
                "selectors": {
                    "job_container": ".job-listing",
                    "title": ".job-title a",
                    "company": ".company-name",
                    "location": ".job-location",
                    "salary": ".salary-range",
                    "description": ".job-description",
                    "link": ".job-title a@href"
                },
                "pagination": {
                    "next_page_selector": ".pagination .next",
                    "max_pages": 10
                },
                "anti_bot": {
                    "use_proxy": True,
                    "random_user_agent": True,
                    "delay_range": [1, 3]
                }
            }
        }
```

## 🧠 Skill Gap Analysis Feature

### Core Components
```python
# backend/app/services/skill_analyzer.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple

class SkillGapAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.skill_importance_model = self.load_skill_importance_model()
    
    async def analyze_skill_gaps(
        self, 
        user_skills: List[str], 
        target_jobs: List[Dict]
    ) -> Dict:
        """Analyze skill gaps between user profile and target jobs."""
        
        # Extract required skills from job postings
        job_skills = self.extract_job_skills(target_jobs)
        
        # Calculate skill gaps
        missing_skills = self.identify_missing_skills(user_skills, job_skills)
        
        # Rank skills by importance and market demand
        ranked_skills = self.rank_skills_by_importance(missing_skills)
        
        # Generate learning recommendations
        learning_path = self.generate_learning_path(ranked_skills)
        
        # Calculate potential match score improvement
        improvement_potential = self.calculate_improvement_potential(
            user_skills, missing_skills, target_jobs
        )
        
        return {
            "missing_skills": ranked_skills,
            "learning_path": learning_path,
            "improvement_potential": improvement_potential,
            "market_trends": self.get_skill_market_trends(missing_skills),
            "estimated_learning_time": self.estimate_learning_time(ranked_skills)
        }
    
    def identify_missing_skills(
        self, 
        user_skills: List[str], 
        job_skills: Dict[str, int]
    ) -> List[Tuple[str, float]]:
        """Identify skills missing from user profile."""
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        missing_skills = []
        for skill, frequency in job_skills.items():
            if skill.lower() not in user_skills_lower:
                importance_score = self.calculate_skill_importance(skill, frequency)
                missing_skills.append((skill, importance_score))
        
        return sorted(missing_skills, key=lambda x: x[1], reverse=True)
    
    def generate_learning_path(
        self, 
        ranked_skills: List[Tuple[str, float]]
    ) -> List[Dict]:
        """Generate learning recommendations for missing skills."""
        learning_resources = {
            "python": {
                "courses": ["Python for Data Science - Coursera", "Automate the Boring Stuff"],
                "estimated_hours": 40,
                "difficulty": "beginner",
                "prerequisites": []
            },
            "machine learning": {
                "courses": ["Andrew Ng ML Course", "Fast.ai Practical ML"],
                "estimated_hours": 120,
                "difficulty": "intermediate",
                "prerequisites": ["python", "statistics"]
            },
            "tensorflow": {
                "courses": ["TensorFlow Developer Certificate", "Deep Learning Specialization"],
                "estimated_hours": 80,
                "difficulty": "intermediate",
                "prerequisites": ["python", "machine learning"]
            }
            # Add more skills...
        }
        
        learning_path = []
        for skill, importance in ranked_skills[:10]:  # Top 10 skills
            skill_lower = skill.lower()
            if skill_lower in learning_resources:
                resource_info = learning_resources[skill_lower]
                learning_path.append({
                    "skill": skill,
                    "importance_score": importance,
                    "courses": resource_info["courses"],
                    "estimated_hours": resource_info["estimated_hours"],
                    "difficulty": resource_info["difficulty"],
                    "prerequisites": resource_info["prerequisites"],
                    "priority": len(learning_path) + 1
                })
        
        return learning_path
```

### Frontend Integration
```typescript
// frontend/src/components/SkillGapAnalysis.tsx
import React, { useState, useEffect } from 'react';
import { TrendingUp, BookOpen, Clock, Target } from 'lucide-react';

interface SkillGapAnalysisProps {
  userId: string;
  targetJobs: Job[];
}

const SkillGapAnalysis: React.FC<SkillGapAnalysisProps> = ({ userId, targetJobs }) => {
  const [analysis, setAnalysis] = useState<SkillAnalysis | null>(null);
  const [loading, setLoading] = useState(false);

  const analyzeSkillGaps = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/skills/analyze-gaps`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          target_job_ids: targetJobs.map(job => job.id)
        })
      });
      
      const analysisData = await response.json();
      setAnalysis(analysisData);
    } catch (error) {
      console.error('Skill gap analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Skill Gap Analysis</h2>
        <button 
          onClick={analyzeSkillGaps}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Analyze Skills'}
        </button>
      </div>

      {analysis && (
        <div className="space-y-6">
          {/* Missing Skills */}
          <div>
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <Target className="w-5 h-5 mr-2 text-red-500" />
              Missing Skills ({analysis.missing_skills.length})
            </h3>
            <div className="grid gap-3">
              {analysis.missing_skills.slice(0, 10).map((skill, index) => (
                <div key={skill.name} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <div>
                    <span className="font-medium">{skill.name}</span>
                    <span className="ml-2 text-sm text-gray-600">
                      Found in {skill.frequency} jobs
                    </span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-20 bg-gray-200 rounded-full h-2 mr-3">
                      <div 
                        className="bg-red-500 h-2 rounded-full"
                        style={{ width: `${skill.importance_score}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium text-red-600">
                      {skill.importance_score}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Learning Path */}
          <div>
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <BookOpen className="w-5 h-5 mr-2 text-blue-500" />
              Recommended Learning Path
            </h3>
            <div className="space-y-4">
              {analysis.learning_path.map((item, index) => (
                <div key={item.skill} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-lg">{item.skill}</h4>
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                      Priority #{item.priority}
                    </span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600 mb-3">
                    <Clock className="w-4 h-4 mr-1" />
                    <span>{item.estimated_hours} hours</span>
                    <span className="mx-2">•</span>
                    <span className="capitalize">{item.difficulty} level</span>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm font-medium">Recommended Courses:</p>
                    <ul className="text-sm text-gray-700 list-disc list-inside">
                      {item.courses.map((course, idx) => (
                        <li key={idx}>{course}</li>
                      ))}
                    </ul>
                  </div>
                  {item.prerequisites.length > 0 && (
                    <div className="mt-3 text-sm">
                      <span className="font-medium">Prerequisites: </span>
                      <span className="text-gray-600">
                        {item.prerequisites.join(', ')}
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Improvement Potential */}
          <div className="bg-green-50 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-2 flex items-center text-green-800">
              <TrendingUp className="w-5 h-5 mr-2" />
              Improvement Potential
            </h3>
            <p className="text-green-700">
              By learning the top 5 missing skills, you could improve your average 
              match score from <strong>{analysis.improvement_potential.current_avg}%</strong> to{' '}
              <strong>{analysis.improvement_potential.potential_avg}%</strong>
              {' '}(+{analysis.improvement_potential.increase}%)
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SkillGapAnalysis;
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL 14+
- Redis 6+
- Anthropic API key (free tier available)
- SendGrid API key (100 emails/day free)

### 1. Clone and Install
```bash
git clone https://github.com/your-username/ai-job-tracker-python.git
cd ai-job-tracker-python

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Environment Configuration

#### Backend (.env)
```bash
# Database
DATABASE_URL="postgresql://user:password@localhost/jobtracker"
REDIS_URL="redis://localhost:6379/0"

# API Keys
CLAUDE_API_KEY="your-anthropic-api-key"
SENDGRID_API_KEY="your-sendgrid-key"
SECRET_KEY="your-secret-key-for-jwt"

# Optional job board APIs
LINKEDIN_CLIENT_ID="your-linkedin-client-id"
LINKEDIN_CLIENT_SECRET="your-linkedin-secret"
INDEED_API_KEY="your-indeed-api-key"

# ML Models (optional)
HUGGINGFACE_API_KEY="your-huggingface-key"
OPENAI_API_KEY="your-openai-key"  # For embeddings

# Environment
ENVIRONMENT="development"
DEBUG=True
```

#### Frontend (.env.local)
```bash
REACT_APP_API_URL="http://localhost:8000"
REACT_APP_SENTRY_DSN="your-sentry-dsn"
```

### 3. Database Setup
```bash
cd backend

# Create database and run migrations
alembic upgrade head

# Seed database with test data
python scripts/seed_database.py

# Train initial ML models (optional)
python scripts/train_models.py
```

### 4. Start Development
```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start Celery worker
cd backend
celery -A app.workers.celery_app worker --loglevel=info

# Terminal 3: Start Celery beat (scheduler)
cd backend
celery -A app.workers.celery_app beat --loglevel=info

# Terminal 4: Start frontend
cd frontend
npm start
```

## 📊 Database Schema

### Core Tables (SQLAlchemy Models)
```python
# Extended schema with skill analysis
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String)
    experience_level = Column(Enum(ExperienceLevel))
    skills = Column(JSON)  # List of current skills
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    currency = Column(String(10))
    timezone = Column(String(50))
    resume_url = Column(String(500))
    skill_analysis = relationship("SkillGapAnalysis", back_populates="user")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    title = Column(String(500), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    salary = Column(String(255))
    description = Column(Text)
    requirements = Column(JSON)  # Required skills and qualifications
    apply_url = Column(String(1000))
    source_id = Column(UUID, ForeignKey("sources.id"))
    posted_date = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    skill_embeddings = Column(JSON)  # NEW: Vector embeddings for skills

class SkillGapAnalysis(Base):
    __tablename__ = "skill_gap_analyses"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    target_jobs = Column(JSON)  # List of job IDs analyzed
    missing_skills = Column(JSON)  # Skills user should learn
    learning_path = Column(JSON)  # Recommended learning sequence
    improvement_potential = Column(JSON)  # Predicted match score improvements
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="skill_analysis")

class SkillTrend(Base):
    __tablename__ = "skill_trends"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    skill_name = Column(String(255), nullable=False)
    month_year = Column(String(7), nullable=False)  # Format: 2024-01
    job_frequency = Column(Integer, default=0)  # How many jobs mentioned this skill
    avg_salary = Column(Float)  # Average salary for jobs requiring this skill
    demand_trend = Column(Float)  # Trend indicator (-1 to 1)
    geographic_distribution = Column(JSON)  # Where this skill is most in demand
```

## 🚀 Deployment

### Recommended: Railway + Vercel (5 minutes, $5-15/month)
```bash
# 1. Deploy Frontend to Vercel (FREE)
cd frontend
npm install -g vercel
vercel login
vercel --prod

# 2. Deploy Backend to Railway ($5/month)
cd ../backend
pip install railwaycli
railway login
railway new ai-job-tracker-python
railway add postgresql redis
railway up

# 3. Configure Environment Variables
railway variables set CLAUDE_API_KEY=your-anthropic-key
railway variables set SENDGRID_API_KEY=your-sendgrid-key
railway variables set DATABASE_URL=${{Postgres.DATABASE_URL}}
railway variables set REDIS_URL=${{Redis.REDIS_URL}}
railway variables set SECRET_KEY=your-random-secret

# 4. Run Database Migrations
railway run alembic upgrade head
railway run python scripts/seed_database.py

# 5. Deploy Celery Workers
railway add  # Add another service for Celery
railway up --service celery-worker
```

### Alternative: Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

## 🔄 Background Jobs with Celery

### Celery Configuration
```python
# backend/app/workers/celery_app.py
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "job_tracker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.workers.job_scraper",
        "app.workers.match_calculator", 
        "app.workers.skill_analyzer",
        "app.workers.notification_sender"
    ]
)

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    'scrape-jobs-every-6-hours': {
        'task': 'app.workers.job_scraper.scrape_all_sources',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    'calculate-matches-hourly': {
        'task': 'app.workers.match_calculator.calculate_all_matches',
        'schedule': crontab(minute=0),
    },
    'analyze-skill-gaps-daily': {
        'task': 'app.workers.skill_analyzer.analyze_all_user_skills',
        'schedule': crontab(minute=0, hour=10),  # 10 AM daily
    },
    'send-daily-notifications': {
        'task': 'app.workers.notification_sender.send_daily_digest',
        'schedule': crontab(minute=0, hour=9),
    },
    'update-skill-trends-weekly': {
        'task': 'app.workers.skill_analyzer.update_skill_market_trends',
        'schedule': crontab(minute=0, hour=0, day_of_week=1),  # Monday at midnight
    },
}

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_routes={
        'app.workers.job_scraper.*': {'queue': 'scraping'},
        'app.workers.match_calculator.*': {'queue': 'matching'},
        'app.workers.skill_analyzer.*': {'queue': 'ml_processing'},
        'app.workers.notification_sender.*': {'queue': 'notifications'},
    }
)
```

### Background Processing Tasks
```python
# backend/app/workers/skill_analyzer.py
from celery import current_task
from app.workers.celery_app import celery_app
from app.services.skill_analyzer import SkillGapAnalyzer
from app.models.user import User
from app.core.database import SessionLocal

@celery_app.task(bind=True)
def analyze_all_user_skills(self):
    """Analyze skill gaps for all active users."""
    db = SessionLocal()
    analyzer = SkillGapAnalyzer()
    
    try:
        users = db.query(User).filter(User.is_active == True).all()
        total_users = len(users)
        
        for i, user in enumerate(users):
            try:
                # Update task progress
                current_task.update_state(
                    state='PROGRESS',
                    meta={'current': i, 'total': total_users, 'user_id': str(user.id)}
                )
                
                # Get user's recent job matches for analysis
                recent_jobs = get_user_recent_job_matches(db, user.id, limit=20)
                
                if recent_jobs:
                    # Perform skill gap analysis
                    analysis_result = await analyzer.analyze_skill_gaps(
                        user_skills=user.skills or [],
                        target_jobs=recent_jobs
                    )
                    
                    # Save analysis results
                    save_skill_analysis(db, user.id, analysis_result)
                    
            except Exception as e:
                logger.error(f"Failed to analyze skills for user {user.id}: {e}")
                continue
        
        return {'status': 'completed', 'users_processed': total_users}
        
    finally:
        db.close()

@celery_app.task
def update_skill_market_trends():
    """Update skill market trends based on recent job postings."""
    db = SessionLocal()
    analyzer = SkillGapAnalyzer()
    
    try:
        # Analyze job postings from last 30 days
        recent_jobs = get_recent_job_postings(db, days=30)
        
        # Extract skill trends
        skill_trends = analyzer.calculate_skill_market_trends(recent_jobs)
        
        # Update skill trends table
        update_skill_trends_table(db, skill_trends)
        
        return {'status': 'completed', 'trends_updated': len(skill_trends)}
        
    finally:
        db.close()
```

## 🧪 Testing

### Testing Framework Setup
```python
# backend/pytest.ini
[tool:pytest]
testpaths = app/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --cov=app
    --cov-report=term-missing:skip-covered
    --cov-report=html:htmlcov
    --cov-report=xml
markers =
    unit: Unit tests
    integration: Integration tests
    ml: Machine learning model tests
    slow: Slow running tests
```

### Unit Tests
```bash
# Backend tests
cd backend
pytest app/tests/unit/ -v

# Frontend tests  
cd frontend
npm test

# ML model tests
cd backend
pytest app/tests/unit/ml/ -v -m ml

# Integration tests
pytest app/tests/integration/ -v -m integration
```

### Test Data and Fixtures
```python
# backend/app/tests/fixtures/job_data.py
import pytest
from app.models.job import Job
from app.models.user import User

@pytest.fixture
def sample_user_profile():
    return {
        "name": "Maria Silva",
        "email": "maria@example.com",
        "location": "São Paulo, Brazil",
        "experience_level": "mid",
        "skills": ["Python", "Machine Learning", "SQL", "pandas"],
        "salary_min": 8000,
        "salary_max": 15000,
        "currency": "USD"
    }

@pytest.fixture
def sample_job_postings():
    return [
        {
            "title": "Senior Data Scientist",
            "company": "TechCorp Brasil",
            "location": "Remote (Brazil)",
            "requirements": ["Python", "TensorFlow", "AWS", "Statistics", "MLOps"],
            "salary": "$12,000 - $18,000 USD",
            "description": "Join our AI team building ML solutions...",
        },
        {
            "title": "ML Engineer",
            "company": "StartupAI",
            "location": "São Paulo/Remote", 
            "requirements": ["PyTorch", "Docker", "Kubernetes", "Python", "Git"],
            "salary": "$10,000 - $14,000 USD",
            "description": "Build scalable ML infrastructure...",
        }
    ]

# Example unit test
def test_skill_gap_analysis(sample_user_profile, sample_job_postings):
    """Test skill gap analysis functionality."""
    from app.services.skill_analyzer import SkillGapAnalyzer
    
    analyzer = SkillGapAnalyzer()
    
    # Test skill gap identification
    user_skills = sample_user_profile["skills"]
    job_skills = {}
    
    # Extract skills from job postings
    for job in sample_job_postings:
        for skill in job["requirements"]:
            job_skills[skill] = job_skills.get(skill, 0) + 1
    
    missing_skills = analyzer.identify_missing_skills(user_skills, job_skills)
    
    # Assertions
    assert len(missing_skills) > 0
    assert "TensorFlow" in [skill[0] for skill in missing_skills]
    assert "AWS" in [skill[0] for skill in missing_skills]
    assert "Python" not in [skill[0] for skill in missing_skills]  # User already has this
```

## 📈 Monitoring and Analytics

### Railway Built-in Monitoring
- **Application Metrics**: CPU, memory, request count, response times
- **Database Monitoring**: Connection pools, query performance, storage usage
- **Celery Monitoring**: Task queue length, worker status, task success rates
- **Error Tracking**: Automatic error collection and alerting

### Health Checks
```python
# backend/app/api/v1/endpoints/health.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.redis_client import redis_client
from app.services.claude_client import claude_client

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Comprehensive health check endpoint."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Check database
    try:
        db.execute("SELECT 1")
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check Redis
    try:
        redis_client.ping()
        health_status["services"]["redis"] = "healthy"
    except Exception as e:
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check Claude API
    try:
        # Simple API test
        await claude_client.test_connection()
        health_status["services"]["claude_api"] = "healthy"
    except Exception as e:
        health_status["services"]["claude_api"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"  # Non-critical service
    
    # Check Celery workers
    try:
        from app.workers.celery_app import celery_app
        inspector = celery_app.control.inspect()
        active_workers = inspector.active()
        
        if active_workers:
            health_status["services"]["celery"] = "healthy"
            health_status["services"]["active_workers"] = len(active_workers)
        else:
            health_status["services"]["celery"] = "no active workers"
            health_status["status"] = "degraded"
            
    except Exception as e:
        health_status["services"]["celery"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status
```

### Analytics and Metrics
```python
# backend/app/services/analytics.py
import pandas as pd
from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.user import User
from app.models.application import Application

class JobMarketAnalytics:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_market_report(self, days: int = 30) -> dict:
        """Generate comprehensive job market analytics."""
        
        # Get recent job postings
        recent_jobs = self.get_recent_jobs(days)
        jobs_df = pd.DataFrame([job.__dict__ for job in recent_jobs])
        
        # Skill demand analysis
        skill_demand = self.analyze_skill_demand(jobs_df)
        
        # Salary trends
        salary_trends = self.analyze_salary_trends(jobs_df)
        
        # Geographic distribution
        location_analysis = self.analyze_job_locations(jobs_df)
        
        # Company analysis
        company_trends = self.analyze_hiring_companies(jobs_df)
        
        return {
            "report_period": f"Last {days} days",
            "total_jobs": len(jobs_df),
            "skill_demand": skill_demand,
            "salary_trends": salary_trends,
            "geographic_distribution": location_analysis,
            "top_hiring_companies": company_trends,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def analyze_skill_demand(self, jobs_df: pd.DataFrame) -> dict:
        """Analyze which skills are most in demand."""
        skill_counts = {}
        
        for _, job in jobs_df.iterrows():
            if job.get('requirements'):
                for skill in job['requirements']:
                    skill_lower = skill.lower().strip()
                    skill_counts[skill_lower] = skill_counts.get(skill_lower, 0) + 1
        
        # Convert to DataFrame for analysis
        skills_df = pd.DataFrame(
            list(skill_counts.items()), 
            columns=['skill', 'frequency']
        ).sort_values('frequency', ascending=False)
        
        return {
            "top_skills": skills_df.head(20).to_dict('records'),
            "total_unique_skills": len(skills_df),
            "trending_skills": self.identify_trending_skills(skills_df)
        }
```

## 🔐 Security

### API Security
```python
# backend/app/core/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class SecurityUtils:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials):
        try:
            payload = jwt.decode(
                credentials.credentials, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
            return email
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
```

### Input Validation
```python
# backend/app/schemas/job.py
from pydantic import BaseModel, validator, HttpUrl
from typing import List, Optional
from datetime import datetime

class JobCreate(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    salary: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = []
    apply_url: Optional[HttpUrl] = None
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Job title cannot be empty')
        return v.strip()
    
    @validator('company')
    def company_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Company name cannot be empty')
        return v.strip()
    
    @validator('requirements')
    def validate_requirements(cls, v):
        if v is None:
            return []
        # Remove empty strings and duplicates
        cleaned = list(set([req.strip() for req in v if req and req.strip()]))
        return cleaned[:50]  # Max 50 requirements
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Senior Data Scientist",
                "company": "TechCorp Brasil",
                "location": "Remote (Brazil timezone)",
                "salary": "$12,000 - $18,000 USD/month",
                "description": "Join our AI team building ML solutions...",
                "requirements": ["Python", "TensorFlow", "AWS", "Statistics"],
                "apply_url": "https://techcorp.com/careers/senior-data-scientist"
            }
        }
```

## 🤝 Contributing

### Development Workflow with Issue-Driven + Test-Driven Development
See CLAUDE.md for detailed workflow instructions combining TDD with GitHub issue management.

### Code Standards
- **Python**: PEP 8 compliance with Black formatting
- **Type Hints**: Full type annotations required
- **Documentation**: Docstrings for all public functions
- **Testing**: Minimum 80% code coverage
- **Security**: Input validation and SQL injection prevention

### Adding New Features
1. Create GitHub issue with feature specification
2. Write failing tests based on requirements
3. Implement feature to pass tests
4. Update documentation
5. Submit pull request with issue reference

### ML Model Development
```python
# Example: Adding new skill recommendation model
# 1. Create model in app/ml/models/new_model.py
# 2. Add training script in app/ml/training/
# 3. Update model registry in app/ml/model_registry.py
# 4. Add API endpoints in app/api/v1/endpoints/
# 5. Write comprehensive tests
```

## 📞 Support

### Documentation
- **API Docs**: `http://localhost:8000/docs` (FastAPI automatic docs)
- **Database Schema**: Available in `/docs/database-erd.png`
- **ML Models**: See `/docs/ML_MODELS.md`
- **Skill Analysis**: See `/docs/SKILL_ANALYSIS.md`

### Getting Help
- **GitHub Issues**: Bug reports and feature requests
- **Discord**: Community support and discussions
- **Email**: support@aijobtracker.com

### Common Issues
- **Resume parsing fails**: Check file format and Claude API key
- **Skill analysis slow**: Verify ML models are trained and cached
- **Celery tasks not running**: Check Redis connection and worker status
- **Job scraping blocked**: Review rate limiting and user agents

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

Built with ❤️ and 🐍 for the LATAM data science community

## 💰 Cost Breakdown

### Development Costs (One-time)
- **Development Time**: 40-60 hours for full implementation
- **ML Model Training**: $10-50 (compute costs for initial training)
- **Testing & QA**: 20-30 hours

### Monthly Operating Costs
- **Railway (Backend + Database + Redis)**: $5-15/month
- **Vercel (Frontend)**: FREE
- **Anthropic Claude API**: $0-20/month (depending on usage)
- **SendGrid (Email)**: $0-15/month (100 emails/day free)
- **Total**: $5-50/month depending on scale

### Scale-up Costs
- **200-500 users**: $20-80/month
- **500+ users**: $100-300/month (consider AWS migration)
- **Enterprise (1000+ users)**: $300-1000/month
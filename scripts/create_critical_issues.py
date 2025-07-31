#!/usr/bin/env python3
"""
Critical Issues Creator Script
=============================

This script creates GitHub issues for the critical tasks identified in 
CriticalTasksRemaining.md that are blocking production deployment.

Usage:
    python scripts/create_critical_issues.py

This follows the issue-driven development methodology and addresses the
most critical production blockers first.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re

class CriticalIssueCreator:
    """Create GitHub issues for critical production blockers."""
    
    def __init__(self):
        self.repo_root = Path("/Users/lucasmurtinho/Documents/Jobby")
        self.issues_created = []
    
    def get_critical_issues(self) -> List[Dict]:
        """Define the critical issues based on CriticalTasksRemaining.md analysis."""
        
        critical_issues = [
            {
                "title": "🚨 CRITICAL: Fix Production Dependencies & Health Checks",
                "priority": "critical",
                "labels": ["production", "deployment", "health-checks", "dependencies"],
                "description": "Fix missing production dependencies and health endpoint issues blocking deployment",
                "tasks": [
                    "Install missing psutil dependency (pip install psutil)",
                    "Verify gunicorn is properly installed and configured",
                    "Enhance health endpoint to include database status check",
                    "Fix CORS configuration for frontend integration",
                    "Resolve resume upload authentication in production mode",
                    "Add proper error handling for health checks"
                ],
                "test_failures": [
                    "test_health_endpoint_includes_database_status",
                    "test_cors_headers_configured", 
                    "test_gunicorn_production_server_config",
                    "test_memory_usage_stable"
                ],
                "estimated_time": "2 hours",
                "impact": "Cannot deploy to production, monitoring will fail"
            },
            {
                "title": "🔥 HIGH: Implement Real Job Scraping",
                "priority": "high",
                "labels": ["scraping", "data", "jobs", "core-feature"],
                "description": "Implement actual job scraping logic to replace mock data with real job opportunities",
                "tasks": [
                    "Implement LinkedInScraper.scrape_jobs() with actual scraping logic",
                    "Implement RemoteOKScraper.scrape_jobs() with API integration",
                    "Implement RSSParser.parse_feeds() for RSS feed processing",
                    "Add background job scheduling for daily scraping",
                    "Create data validation and cleaning for scraped jobs",
                    "Add error handling and retry logic for scraping failures",
                    "Implement rate limiting to avoid being blocked",
                    "Add logging and monitoring for scraping operations"
                ],
                "estimated_time": "6-8 hours",
                "impact": "No real job data = unusable product"
            },
            {
                "title": "🔥 HIGH: Implement Email Notification Service",
                "priority": "high", 
                "labels": ["email", "notifications", "sendgrid", "core-feature"],
                "description": "Implement actual email sending functionality for job alerts and notifications",
                "tasks": [
                    "Set up SendGrid API integration",
                    "Create email templates for job alerts",
                    "Implement email sending service",
                    "Add email preferences and frequency settings",
                    "Create email validation and error handling",
                    "Add email tracking and analytics",
                    "Implement unsubscribe functionality",
                    "Add email queue management"
                ],
                "estimated_time": "4 hours",
                "impact": "Users won't receive job alerts"
            },
            {
                "title": "🔥 HIGH: Database Migration & Production Setup",
                "priority": "high",
                "labels": ["database", "migrations", "production", "alembic"],
                "description": "Set up proper database migrations and production database configuration",
                "tasks": [
                    "Set up Alembic for database migrations",
                    "Create initial migration for current schema",
                    "Configure production database settings",
                    "Add database connection pooling",
                    "Implement database backup strategy",
                    "Add database monitoring and health checks",
                    "Create database rollback procedures",
                    "Document database deployment process"
                ],
                "estimated_time": "3 hours",
                "impact": "Cannot deploy with proper database schema"
            },
            {
                "title": "🔥 HIGH: Implement Frontend Components & Pages",
                "priority": "high",
                "labels": ["frontend", "react", "ui", "user-interface"],
                "description": "Create the complete frontend user interface for the job tracking application",
                "tasks": [
                    "Create dashboard with AI insights and job recommendations",
                    "Implement job search and filtering interface",
                    "Build profile management page",
                    "Create resume upload interface",
                    "Add settings and preferences page",
                    "Implement job application tracking interface",
                    "Create skill gap analysis visualization",
                    "Add responsive design for mobile devices",
                    "Implement real-time notifications",
                    "Add dark/light theme support"
                ],
                "estimated_time": "8-12 hours",
                "impact": "No user interface = unusable product"
            },
            {
                "title": "🔥 HIGH: Background Job Processing (Celery)",
                "priority": "high",
                "labels": ["celery", "background-jobs", "redis", "automation"],
                "description": "Implement Celery background job processing for automated tasks",
                "tasks": [
                    "Set up Redis for Celery broker",
                    "Configure Celery workers and tasks",
                    "Implement automated job scraping tasks",
                    "Add email notification job processing",
                    "Create task monitoring and error handling",
                    "Add job scheduling and periodic tasks",
                    "Implement task retry logic",
                    "Add task progress tracking",
                    "Create task cleanup and maintenance"
                ],
                "estimated_time": "4 hours",
                "impact": "No automated job scraping, email sending"
            },
            {
                "title": "📊 MEDIUM: Production Error Handling & Monitoring",
                "priority": "medium",
                "labels": ["error-handling", "monitoring", "logging", "production"],
                "description": "Implement comprehensive error handling and monitoring for production",
                "tasks": [
                    "Implement structured logging with proper levels",
                    "Add error monitoring with Sentry integration",
                    "Create user-friendly error pages",
                    "Add performance monitoring and metrics",
                    "Implement health check alerts",
                    "Add business metrics tracking",
                    "Create error reporting and alerting",
                    "Add request/response logging"
                ],
                "estimated_time": "2 hours",
                "impact": "Poor production debugging and user experience"
            }
        ]
        
        return critical_issues
    
    def create_issue_content(self, issue_info: Dict) -> str:
        """Generate GitHub issue content from issue information."""
        
        content = f"""
## 🚨 Critical Production Blocker

**Issue**: {issue_info['title']}

### 📋 Background
This is a critical issue identified in CriticalTasksRemaining.md that is blocking production deployment and core functionality.

**Priority**: {issue_info['priority'].upper()}
**Estimated Time**: {issue_info['estimated_time']}
**Impact**: {issue_info['impact']}

### 📖 Description
{issue_info['description']}

### ✅ Acceptance Criteria
"""
        
        for i, task in enumerate(issue_info['tasks'], 1):
            content += f"\n- [ ] {task}"
        
        if 'test_failures' in issue_info:
            content += f"""

### 🧪 Related Test Failures
"""
            for test in issue_info['test_failures']:
                content += f"\n- `{test}`"
        
        content += f"""

### 🎯 Success Criteria
- [ ] All tasks completed and tested
- [ ] Related tests passing
- [ ] No production deployment blockers
- [ ] Core functionality working in production

### 🔗 Dependencies
- Part of critical production readiness
- Blocks MVP launch
- Required for user-facing functionality

### 📝 Implementation Notes
- Follow TDD approach for new features
- Test thoroughly in staging environment
- Document any configuration changes
- Update deployment procedures

---
*Auto-generated from CriticalTasksRemaining.md analysis*
"""
        
        return content.strip()
    
    def print_issues_to_create(self):
        """Print all critical issues that should be created."""
        
        print("🔍 Analyzing critical tasks from CriticalTasksRemaining.md...")
        critical_issues = self.get_critical_issues()
        
        print(f"🚨 Found {len(critical_issues)} critical issues that need immediate attention:")
        print()
        
        for i, issue in enumerate(critical_issues, 1):
            print(f"{'='*80}")
            print(f"ISSUE #{i}: {issue['title']}")
            print(f"Priority: {issue['priority'].upper()}")
            print(f"Labels: {', '.join(issue['labels'])}")
            print(f"Estimated Time: {issue['estimated_time']}")
            print(f"Impact: {issue['impact']}")
            print(f"{'='*80}")
            print()
            
            issue_content = self.create_issue_content(issue)
            print(issue_content)
            print()
            print("-" * 80)
            print()
        
        print(f"""
🎯 IMMEDIATE ACTION PLAN:

Phase 1: Production Blockers (2 hours)
- Fix dependencies and health checks
- Resolve deployment issues

Phase 2: Core Features (8-12 hours)  
- Implement real job scraping
- Add email notifications
- Set up database migrations

Phase 3: User Interface (8-12 hours)
- Build frontend components
- Implement background processing

📝 To create these issues automatically:
   - Use GitHub CLI: `gh issue create --title "..." --body "..."`
   - Or copy/paste the content above into GitHub Issues UI

⏰ Total estimated time to launch-ready: 18-26 hours
""")

if __name__ == "__main__":
    creator = CriticalIssueCreator()
    creator.print_issues_to_create() 
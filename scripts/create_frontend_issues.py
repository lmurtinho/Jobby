#!/usr/bin/env python3
"""
Issue Creator Script for Frontend Foundation
==========================================

This script automatically creates GitHub issues based on test failures during
the Outside-In TDD development of the frontend foundation.

Usage:
    python scripts/create_frontend_issues.py

This follows the issue-driven development methodology described in CLAUDE.md.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re

class FrontendIssueCreator:
    """Create GitHub issues for frontend foundation development."""
    
    def __init__(self):
        self.repo_root = Path("/Users/lucasmurtinho/Documents/Jobby")
        self.issues_created = []
    
    def run_frontend_tests_and_collect_failures(self) -> List[Dict]:
        """Run frontend foundation tests and collect failure information."""
        
        # Run the frontend foundation integration test
        cmd = [
            "python", "-m", "pytest", 
            "app/tests/integration/test_frontend_foundation.py",
            "-v", "--tb=short", "--no-header"
        ]
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_root / "backend",
            capture_output=True,
            text=True
        )
        
        print(f"Test command: {' '.join(cmd)}")
        print(f"Return code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        print("-" * 40)
        
        # Parse failures from pytest output
        failures = self.parse_pytest_failures(result.stdout, result.stderr)
        return failures
    
    def parse_pytest_failures(self, stdout: str, stderr: str) -> List[Dict]:
        """Parse pytest output to extract frontend-specific failures."""
        
        failures = []
        
        # Look for FAILED test lines in the summary
        failed_lines = [line for line in stdout.split('\n') if 'FAILED' in line and '::' in line]
        
        print(f"Found {len(failed_lines)} failed test lines")
        
        for line in failed_lines:
            # Extract test name from lines like:
            # "app/tests/integration/test_frontend_foundation.py::TestFrontendFoundationIntegration::test_frontend_project_structure_exists FAILED"
            if '::' in line and 'FAILED' in line:
                parts = line.split('::')
                if len(parts) >= 3:
                    test_name = parts[2].split(' ')[0]  # Get test name before FAILED
                    print(f"Processing test failure: {test_name}")
                    
                    # Map test failures to implementation issues
                    issue_info = self.map_test_failure_to_issue(test_name, f"Test failed: {line}", stdout)
                    if issue_info:
                        failures.append(issue_info)
                        print(f"Created issue for: {test_name}")
                    else:
                        print(f"No issue mapping for: {test_name}")
        
        print(f"Total issues created: {len(failures)}")
        return failures
    
    def map_test_failure_to_issue(self, test_name: str, error_message: str, full_output: str) -> Optional[Dict]:
        """Map a specific test failure to a GitHub issue."""
        
        # Map test failures to specific implementation tasks
        test_to_issue_map = {
            "test_frontend_project_structure_exists": {
                "title": "Create React TypeScript project structure",
                "priority": "high",
                "labels": ["frontend", "setup", "day-1"],
                "description": "Set up the complete React + TypeScript frontend project with proper structure",
                "tasks": [
                    "Create frontend/ directory",
                    "Initialize React TypeScript project",
                    "Install required dependencies (react-router-dom, axios, etc.)",
                    "Set up proper folder structure (components/, pages/, utils/, types/)"
                ]
            },
            "test_frontend_directory_structure": {
                "title": "Create frontend component directory structure",
                "priority": "high", 
                "labels": ["frontend", "structure", "day-1"],
                "description": "Create the proper directory structure for React components",
                "tasks": [
                    "Create src/components/ directory",
                    "Create src/pages/ directory", 
                    "Create src/utils/ directory",
                    "Create src/types/ directory"
                ]
            },
            "test_authentication_pages_exist": {
                "title": "Implement authentication pages (Login/Register)",
                "priority": "high",
                "labels": ["frontend", "auth", "day-1"],
                "description": "Create Login and Register page components with proper React structure",
                "tasks": [
                    "Create Login.tsx page component",
                    "Create Register.tsx page component",
                    "Implement basic form structures",
                    "Add proper TypeScript types"
                ]
            },
            "test_api_client_configuration": {
                "title": "Implement API client for backend communication",
                "priority": "high",
                "labels": ["frontend", "api", "day-1"],
                "description": "Set up axios-based API client for communicating with FastAPI backend",
                "tasks": [
                    "Create apiClient.ts utility",
                    "Configure axios with base URL",
                    "Add authentication headers handling",
                    "Create API method wrappers"
                ]
            },
            "test_authentication_context_setup": {
                "title": "Implement authentication context and state management",
                "priority": "high",
                "labels": ["frontend", "auth", "state", "day-1"],
                "description": "Create React context for managing authentication state across the app",
                "tasks": [
                    "Create AuthContext.tsx",
                    "Implement login/logout functions",
                    "Add token management",
                    "Create AuthProvider component"
                ]
            },
            "test_protected_route_component": {
                "title": "Implement protected route component",
                "priority": "medium",
                "labels": ["frontend", "routing", "auth", "day-1"],
                "description": "Create component to protect routes that require authentication",
                "tasks": [
                    "Create ProtectedRoute.tsx component",
                    "Add authentication checking logic",
                    "Implement redirect to login",
                    "Handle loading states"
                ]
            },
            "test_basic_routing_setup": {
                "title": "Configure React Router with authentication flow",
                "priority": "high",
                "labels": ["frontend", "routing", "day-1"],
                "description": "Set up React Router with authentication-aware routing",
                "tasks": [
                    "Configure BrowserRouter in App.tsx",
                    "Set up Routes for auth pages",
                    "Add protected route integration",
                    "Configure route navigation"
                ]
            },
            "test_typescript_configuration": {
                "title": "Configure TypeScript for React project",
                "priority": "medium",
                "labels": ["frontend", "typescript", "config", "day-1"],
                "description": "Ensure TypeScript is properly configured for React development",
                "tasks": [
                    "Verify tsconfig.json exists and is properly configured",
                    "Set up React-specific TypeScript settings",
                    "Configure proper JSX handling",
                    "Add type checking scripts"
                ]
            },
            "test_environment_configuration": {
                "title": "Configure environment variables for API endpoints", 
                "priority": "medium",
                "labels": ["frontend", "config", "env", "day-1"],
                "description": "Set up environment variables for configuring API endpoints",
                "tasks": [
                    "Create .env file for development",
                    "Add REACT_APP_API_URL configuration",
                    "Configure different environments",
                    "Document environment setup"
                ]
            },
            "test_frontend_builds_successfully": {
                "title": "Fix frontend build configuration and errors",
                "priority": "high",
                "labels": ["frontend", "build", "day-1"],
                "description": "Ensure the frontend builds successfully for production deployment",
                "tasks": [
                    "Fix any TypeScript compilation errors",
                    "Resolve build configuration issues",
                    "Ensure all dependencies are properly installed",
                    "Verify build output is correct"
                ]
            }
        }
        
        if test_name in test_to_issue_map:
            issue_template = test_to_issue_map[test_name]
            
            return {
                "title": issue_template["title"],
                "priority": issue_template["priority"], 
                "labels": issue_template["labels"],
                "test_name": test_name,
                "error_message": error_message,
                "description": issue_template["description"],
                "tasks": issue_template["tasks"],
                "test_file": "app/tests/integration/test_frontend_foundation.py"
            }
        
        return None
    
    def create_issue_content(self, issue_info: Dict) -> str:
        """Generate GitHub issue content from issue information."""
        
        content = f"""
## 🎯 Day 1 Frontend Foundation Task

**Test-Driven Issue**: {issue_info['title']}

### 📋 Background
This issue was automatically generated from failing frontend foundation tests as part of our Outside-In TDD approach for Day 1 MVP development.

**Failing Test**: `{issue_info['test_name']}`
**Test File**: `{issue_info['test_file']}`
**Priority**: {issue_info['priority'].upper()}

### 🚨 Test Failure
```
{issue_info['error_message']}
```

### 📖 Description
{issue_info['description']}

### ✅ Acceptance Criteria
"""
        
        for i, task in enumerate(issue_info['tasks'], 1):
            content += f"\n- [ ] {task}"
        
        content += f"""

### 🧪 Verification
To verify this issue is resolved:
```bash
cd backend
python -m pytest app/tests/integration/test_frontend_foundation.py::{issue_info['test_name']} -v
```

### 🔗 Related
- Part of Day 1 MVP Frontend Foundation
- Follows Outside-In TDD methodology
- Supports MVP 5-day sprint plan

---
*Auto-generated from test failure in Outside-In TDD workflow*
"""
        
        return content.strip()
    
    def print_issues_to_create(self):
        """Print all issues that should be created based on current test failures."""
        
        print("🔍 Running frontend foundation tests to identify issues...")
        failures = self.run_frontend_tests_and_collect_failures()
        
        if not failures:
            print("✅ No frontend test failures found - all issues resolved!")
            return
        
        print(f"🚨 Found {len(failures)} test failures that need issues:")
        print()
        
        for i, failure in enumerate(failures, 1):
            print(f"{'='*60}")
            print(f"ISSUE #{i}: {failure['title']}")
            print(f"Priority: {failure['priority'].upper()}")
            print(f"Labels: {', '.join(failure['labels'])}")
            print(f"{'='*60}")
            print()
            
            issue_content = self.create_issue_content(failure)
            print(issue_content)
            print()
            print("-" * 60)
            print()
        
        print(f"""
🎯 NEXT STEPS:
1. Create these {len(failures)} GitHub issues
2. Work through them in order of priority
3. Run tests after each implementation
4. Each passing test closes its issue

📝 To create these issues automatically:
   - Use GitHub CLI: `gh issue create --title "..." --body "..."`
   - Or copy/paste the content above into GitHub Issues UI
""")

if __name__ == "__main__":
    creator = FrontendIssueCreator()
    creator.print_issues_to_create()

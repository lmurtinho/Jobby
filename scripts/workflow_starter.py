#!/usr/bin/env python3
"""
Issue-Driven Development Workflow Script
========================================

This script implements the Outside-In TDD workflow described in CLAUDE.md:
1. Runs the high-level integration test
2. Captures test failures and error messages
3. Automatically creates GitHub issues for each failure
4. Generates implementation roadmap based on failures

Usage:
    python workflow_starter.py [--dry-run] [--github-token TOKEN]

The script will:
- Run the complete workflow test
- Parse pytest output for specific failures
- Create structured GitHub issues with acceptance criteria
- Generate a development roadmap
- Create initial project structure
"""

import subprocess
import sys
import re
import json
import argparse
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv


@dataclass
class TestFailure:
    """Represents a test failure that should become a GitHub issue."""
    component: str
    error_type: str
    error_message: str
    file_path: str
    line_number: Optional[int]
    priority: str
    estimated_hours: int
    prerequisites: List[str]
    acceptance_criteria: List[str]


class WorkflowStarter:
    """Manages the Issue-Driven Development workflow startup."""
    
    def __init__(self, github_token: Optional[str] = None, dry_run: bool = False):
        self.github_token = github_token
        self.dry_run = dry_run
        self.repo_owner = "lmurtinho"  # Update with actual repo owner
        self.repo_name = "Jobby"       # Update with actual repo name
        
        # Component mapping for issue assignment and organization
        self.component_mapping = {
            "app.main": {"priority": "high", "hours": 4, "category": "infrastructure"},
            "app.core": {"priority": "high", "hours": 8, "category": "infrastructure"},
            "app.models": {"priority": "high", "hours": 12, "category": "database"},
            "app.api": {"priority": "medium", "hours": 16, "category": "backend"},
            "app.services": {"priority": "high", "hours": 20, "category": "business-logic"},
            "app.ml": {"priority": "medium", "hours": 24, "category": "machine-learning"},
            "app.scrapers": {"priority": "medium", "hours": 16, "category": "data-collection"},
            "app.workers": {"priority": "medium", "hours": 12, "category": "background-tasks"},
            "app.utils": {"priority": "low", "hours": 8, "category": "utilities"},
            "app.tests": {"priority": "high", "hours": 6, "category": "testing"}
        }
    
    def run_integration_test(self) -> str:
        """Run the high-level integration test and capture output."""
        print("🧪 Running high-level integration test to capture failures...")
        
        try:
            # Ensure we're running from the project root
            project_root = Path.cwd().parent if Path.cwd().name == "scripts" else Path.cwd()
            
            result = subprocess.run([
                "python", "-m", "pytest", 
                "backend/app/tests/integration/test_complete_workflow.py::TestCompleteJobTrackingWorkflow::test_complete_ai_job_tracker_workflow",
                "-v", "--tb=short", "--no-header"
            ], capture_output=True, text=True, cwd=project_root)
            
            output = result.stdout + result.stderr
            print(f"✅ Test execution completed (exit code: {result.returncode})")
            return output
            
        except FileNotFoundError:
            print("❌ pytest not found. Please install: pip install pytest")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error running test: {e}")
            sys.exit(1)
    
    def parse_test_failures(self, pytest_output: str) -> List[TestFailure]:
        """Parse pytest output to extract actionable failure information."""
        failures = []
        
        # Common patterns in pytest output
        patterns = {
            "import_error": r"ModuleNotFoundError: No module named ['\"]([^'\"]+)['\"]",
            "missing_file": r"FileNotFoundError: \[Errno 2\] No such file or directory: ['\"]([^'\"]+)['\"]",
            "attribute_error": r"AttributeError: module ['\"]([^'\"]+)['\"] has no attribute ['\"]([^'\"]+)['\"]",
            "name_error": r"NameError: name ['\"]([^'\"]+)['\"] is not defined",
            "import_from_error": r"ImportError: cannot import name ['\"]([^'\"]+)['\"] from ['\"]([^'\"]+)['\"]"
        }
        
        lines = pytest_output.split('\n')
        
        for i, line in enumerate(lines):
            # Parse different types of failures
            for error_type, pattern in patterns.items():
                match = re.search(pattern, line)
                if match:
                    failure = self._create_failure_from_match(error_type, match, line, i)
                    if failure:
                        failures.append(failure)
        
        # Remove duplicates and sort by priority
        unique_failures = self._deduplicate_failures(failures)
        return sorted(unique_failures, key=lambda f: (f.priority, f.estimated_hours))
    
    def _create_failure_from_match(self, error_type: str, match: re.Match, line: str, line_num: int) -> Optional[TestFailure]:
        """Create a TestFailure object from a regex match."""
        
        if error_type == "import_error":
            module_name = match.group(1)
            component = module_name.split('.')[0] if '.' in module_name else module_name
            
            return TestFailure(
                component=component,
                error_type="missing_module",
                error_message=f"Module '{module_name}' does not exist",
                file_path=self._guess_file_path(module_name),
                line_number=line_num,
                priority=self._get_component_priority(component),
                estimated_hours=self._get_component_hours(component),
                prerequisites=self._get_component_prerequisites(component),
                acceptance_criteria=self._get_acceptance_criteria(component, error_type)
            )
        
        elif error_type == "attribute_error":
            module_name = match.group(1)
            attribute_name = match.group(2)
            component = module_name.split('.')[0] if '.' in module_name else module_name
            
            return TestFailure(
                component=component,
                error_type="missing_class_or_function",
                error_message=f"'{attribute_name}' not implemented in '{module_name}'",
                file_path=self._guess_file_path(module_name),
                line_number=line_num,
                priority=self._get_component_priority(component),
                estimated_hours=self._get_component_hours(component) // 2,
                prerequisites=[],
                acceptance_criteria=self._get_acceptance_criteria(component, error_type, attribute_name)
            )
        
        elif error_type == "import_from_error":
            symbol_name = match.group(1)
            module_name = match.group(2)
            component = module_name.split('.')[0] if '.' in module_name else module_name
            
            return TestFailure(
                component=component,
                error_type="missing_symbol",
                error_message=f"Cannot import '{symbol_name}' from '{module_name}'",
                file_path=self._guess_file_path(module_name),
                line_number=line_num,
                priority=self._get_component_priority(component),
                estimated_hours=self._get_component_hours(component) // 3,
                prerequisites=[],
                acceptance_criteria=self._get_acceptance_criteria(component, error_type, symbol_name)
            )
        
        return None
    
    def _guess_file_path(self, module_name: str) -> str:
        """Guess the file path based on module name."""
        if module_name.startswith('app.'):
            path_parts = module_name.split('.')
            return f"backend/{'/'.join(path_parts)}.py"
        return f"backend/{module_name.replace('.', '/')}.py"
    
    def _get_component_priority(self, component: str) -> str:
        """Get priority for a component."""
        for key, config in self.component_mapping.items():
            if component.startswith(key):
                return config["priority"]
        return "medium"
    
    def _get_component_hours(self, component: str) -> int:
        """Get estimated hours for a component."""
        for key, config in self.component_mapping.items():
            if component.startswith(key):
                return config["hours"]
        return 8
    
    def _get_component_prerequisites(self, component: str) -> List[str]:
        """Get prerequisites for a component."""
        prerequisites_map = {
            "app.api": ["app.core", "app.models"],
            "app.services": ["app.core", "app.models", "app.utils"],
            "app.ml": ["app.core", "app.models", "app.services"],
            "app.workers": ["app.core", "app.services"],
            "app.scrapers": ["app.core", "app.models"]
        }
        
        for key, prereqs in prerequisites_map.items():
            if component.startswith(key):
                return prereqs
        return []
    
    def _get_acceptance_criteria(self, component: str, error_type: str, symbol_name: Optional[str] = None) -> List[str]:
        """Generate acceptance criteria based on component and error type."""
        base_criteria = [
            "All imports resolve successfully",
            "Module can be imported without errors",
            "Basic functionality works as expected",
            "Unit tests pass",
            "Integration with existing code"
        ]
        
        if component.startswith("app.models"):
            return base_criteria + [
                "Database models defined with SQLAlchemy",
                "Relationships properly configured",
                "Migration scripts created",
                "Database schema validates"
            ]
        elif component.startswith("app.api"):
            return base_criteria + [
                "FastAPI endpoints defined",
                "Request/response schemas created",
                "Authentication middleware works",
                "API documentation generated"
            ]
        elif component.startswith("app.services"):
            return base_criteria + [
                "Business logic implemented",
                "Error handling added",
                "External API integrations work",
                "Service layer tests pass"
            ]
        elif component.startswith("app.ml"):
            return base_criteria + [
                "ML models can be loaded/saved",
                "Training pipeline works",
                "Prediction endpoints functional",
                "Model performance metrics tracked"
            ]
        
        return base_criteria
    
    def _deduplicate_failures(self, failures: List[TestFailure]) -> List[TestFailure]:
        """Remove duplicate failures."""
        seen = set()
        unique_failures = []
        
        for failure in failures:
            key = (failure.component, failure.error_type, failure.error_message)
            if key not in seen:
                seen.add(key)
                unique_failures.append(failure)
        
        return unique_failures
    
    def create_github_issues(self, failures: List[TestFailure]) -> List[str]:
        """Create GitHub issues for each test failure."""
        issue_urls = []
        
        print(f"📝 Creating {len(failures)} GitHub issues...")
        
        for i, failure in enumerate(failures, 1):
            if self.dry_run:
                print(f"[DRY RUN] Would create issue {i}: {failure.component} - {failure.error_message}")
                continue
            
            issue_data = self._format_github_issue(failure, i, len(failures))
            
            if self.github_token:
                url = self._post_github_issue(issue_data)
                if url:
                    issue_urls.append(url)
                    print(f"✅ Created issue {i}/{len(failures)}: {url}")
                else:
                    print(f"❌ Failed to create issue {i}/{len(failures)}")
            else:
                print(f"📋 Issue {i} content prepared (no GitHub token provided)")
                print(f"   Title: {issue_data['title']}")
                print(f"   Component: {failure.component}")
                print(f"   Priority: {failure.priority}")
                print()
        
        return issue_urls
    
    def _format_github_issue(self, failure: TestFailure, issue_num: int, total_issues: int) -> Dict[str, Any]:
        """Format a test failure as a GitHub issue."""
        
        # Determine issue type and labels
        if failure.error_type == "missing_module":
            issue_type = "Epic"
            labels = ["epic", "infrastructure", f"priority-{failure.priority}"]
        else:
            issue_type = "Feature"
            labels = ["feature", "enhancement", f"priority-{failure.priority}"]
        
        # Add component-specific labels
        if "ml" in failure.component:
            labels.append("machine-learning")
        elif "api" in failure.component:
            labels.append("backend")
        elif "models" in failure.component:
            labels.append("database")
        
        title = f"{issue_type}: Implement {failure.component} - {failure.error_message}"
        
        body = f"""## 🚀 Issue-Driven Development

**Issue {issue_num} of {total_issues}** - Generated from Outside-In TDD workflow

### 📋 Overview
{failure.error_message}

**Component**: `{failure.component}`  
**File Path**: `{failure.file_path}`  
**Priority**: {failure.priority.upper()}  
**Estimated Hours**: {failure.estimated_hours}h

### 🎯 Problem Statement
The high-level integration test failed because `{failure.component}` is not implemented. This component is required for the complete AI Job Tracker workflow to function.

### 📝 Requirements
Based on the documentation and test requirements, this component should:

"""
        
        # Add component-specific requirements
        if "models" in failure.component:
            body += """
- Define SQLAlchemy database models
- Set up proper relationships and constraints
- Create database migration scripts
- Implement model validation and serialization
"""
        elif "api" in failure.component:
            body += """
- Create FastAPI router and endpoints
- Define Pydantic request/response schemas
- Implement authentication and authorization
- Add proper error handling and validation
"""
        elif "services" in failure.component:
            body += """
- Implement core business logic
- Handle external API integrations
- Add comprehensive error handling
- Create service layer abstractions
"""
        elif "ml" in failure.component:
            body += """
- Implement machine learning models
- Create training and inference pipelines
- Add model persistence and loading
- Implement performance monitoring
"""
        
        body += f"""
### ✅ Acceptance Criteria
"""
        for criterion in failure.acceptance_criteria:
            body += f"- [ ] {criterion}\n"
        
        if failure.prerequisites:
            body += f"""
### 🔄 Prerequisites
This issue depends on the following components being implemented first:
"""
            for prereq in failure.prerequisites:
                body += f"- [ ] {prereq}\n"
        
        body += f"""
### 🧪 Testing
- [ ] Unit tests written and passing
- [ ] Integration with existing components verified
- [ ] High-level workflow test progresses further
- [ ] No regressions in existing functionality

### 📚 Documentation
- [ ] Code is properly documented with docstrings
- [ ] README updated if needed
- [ ] API documentation generated
- [ ] Type hints added throughout

### 🏗️ Implementation Notes
1. Follow the project structure defined in README.md
2. Use the coding standards from CLAUDE.md
3. Implement with Test-Driven Development approach
4. Ensure integration with existing components

---
*This issue was automatically generated from the Outside-In TDD workflow. The integration test will guide implementation priorities.*
"""
        
        return {
            "title": title,
            "body": body,
            "labels": labels,
            "milestone": None,  # Could add milestone for releases
            "assignees": []     # Could add default assignees
        }
    
    def _post_github_issue(self, issue_data: Dict[str, Any]) -> Optional[str]:
        """Post an issue to GitHub and return the URL."""
        if not self.github_token:
            return None
        
        try:
            import requests
            
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.post(url, headers=headers, json=issue_data)
            
            if response.status_code == 201:
                return response.json()["html_url"]
            else:
                print(f"❌ GitHub API error: {response.status_code} - {response.text}")
                return None
                
        except ImportError:
            print("❌ requests library not found. Install with: pip install requests")
            return None
        except Exception as e:
            print(f"❌ Error posting to GitHub: {e}")
            return None
    
    def create_project_structure(self) -> None:
        """Create initial project directory structure."""
        print("🏗️  Creating initial project structure...")
        
        directories = [
            "backend",
            "backend/app",
            "backend/app/core",
            "backend/app/api",
            "backend/app/api/v1",
            "backend/app/api/v1/endpoints",
            "backend/app/models",
            "backend/app/schemas",
            "backend/app/services",
            "backend/app/ml",
            "backend/app/ml/models",
            "backend/app/ml/preprocessing",
            "backend/app/ml/training",
            "backend/app/scrapers",
            "backend/app/workers",
            "backend/app/utils",
            "backend/app/tests",
            "backend/app/tests/unit",
            "backend/app/tests/integration",
            "backend/app/tests/fixtures",
            "backend/alembic",
            "backend/alembic/versions",
            "frontend",
            "frontend/src",
            "frontend/src/components",
            "frontend/src/pages",
            "frontend/src/store",
            "frontend/src/utils",
            "frontend/src/types",
            "docs",
            "scripts"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py files for Python packages
            if directory.startswith("backend/app") and not directory.endswith("tests"):
                init_file = Path(directory) / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
        
        print("✅ Project structure created successfully!")
    
    def generate_development_roadmap(self, failures: List[TestFailure]) -> str:
        """Generate a development roadmap based on test failures."""
        roadmap = f"""# 🗺️ AI Job Tracker Development Roadmap

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} from Outside-In TDD workflow*

## 📊 Summary
- **Total Components**: {len(failures)}
- **High Priority**: {len([f for f in failures if f.priority == 'high'])}
- **Medium Priority**: {len([f for f in failures if f.priority == 'medium'])}
- **Low Priority**: {len([f for f in failures if f.priority == 'low'])}
- **Estimated Total Hours**: {sum(f.estimated_hours for f in failures)}h

## 🎯 Development Phases

### Phase 1: Core Infrastructure (High Priority)
*Foundation components that everything else depends on*

"""
        
        high_priority = [f for f in failures if f.priority == "high"]
        for failure in high_priority:
            roadmap += f"- [ ] **{failure.component}** ({failure.estimated_hours}h) - {failure.error_message}\n"
        
        roadmap += f"""
**Phase 1 Total**: {sum(f.estimated_hours for f in high_priority)}h

### Phase 2: Business Logic (Medium Priority)
*Core application functionality*

"""
        
        medium_priority = [f for f in failures if f.priority == "medium"]
        for failure in medium_priority:
            roadmap += f"- [ ] **{failure.component}** ({failure.estimated_hours}h) - {failure.error_message}\n"
        
        roadmap += f"""
**Phase 2 Total**: {sum(f.estimated_hours for f in medium_priority)}h

### Phase 3: Enhancements (Low Priority)
*Additional features and optimizations*

"""
        
        low_priority = [f for f in failures if f.priority == "low"]
        for failure in low_priority:
            roadmap += f"- [ ] **{failure.component}** ({failure.estimated_hours}h) - {failure.error_message}\n"
        
        roadmap += f"""
**Phase 3 Total**: {sum(f.estimated_hours for f in low_priority)}h

## 🔄 Dependency Graph
Some components must be built before others:

"""
        
        # Create dependency visualization
        dependencies = {}
        for failure in failures:
            if failure.prerequisites:
                dependencies[failure.component] = failure.prerequisites
        
        for component, prereqs in dependencies.items():
            roadmap += f"- `{component}` depends on: {', '.join(f'`{p}`' for p in prereqs)}\n"
        
        roadmap += """
## 🧪 Testing Strategy
Following Outside-In TDD approach:

1. **Integration Test**: `test_complete_workflow.py` drives all development
2. **Component Tests**: Each component gets unit tests as it's built
3. **Continuous Validation**: Re-run integration test after each component
4. **Issue Closure**: Close GitHub issues as acceptance criteria are met

## 🎉 Success Metrics
The workflow is complete when:
- [ ] High-level integration test passes end-to-end
- [ ] All GitHub issues are resolved
- [ ] Full AI Job Tracker functionality works
- [ ] User can: register → upload resume → get job matches → analyze skills → receive alerts

## 🚀 Getting Started
1. Start with highest priority issues first
2. Follow TDD: write failing unit test → implement → make test pass
3. Regularly run integration test to see progress
4. Update this roadmap as issues are completed

---
*Follow the development guidelines in CLAUDE.md for detailed TDD workflow*
"""
        
        return roadmap


def main():
    """Main entry point for the workflow starter script."""
    parser = argparse.ArgumentParser(description="Start Issue-Driven Development workflow")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without creating issues")
    parser.add_argument("--github-token", help="GitHub personal access token for creating issues")
    parser.add_argument("--skip-test", action="store_true", help="Skip running the integration test")
    parser.add_argument("--create-structure", action="store_true", help="Create initial project structure")
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get GitHub token from environment if not provided
    github_token = args.github_token or os.getenv("GITHUB_TOKEN")
    
    workflow = WorkflowStarter(github_token=github_token, dry_run=args.dry_run)
    
    print("🚀 Starting Issue-Driven Development Workflow")
    print("=" * 50)
    
    # Create project structure if requested
    if args.create_structure:
        workflow.create_project_structure()
    
    # Run integration test to capture failures
    if not args.skip_test:
        test_output = workflow.run_integration_test()
        print(f"\n📊 Test output captured ({len(test_output)} characters)")
    else:
        # Use sample output for demonstration
        test_output = """
FAILED test_complete_workflow.py::TestCompleteJobTrackingWorkflow::test_complete_ai_job_tracker_workflow - ModuleNotFoundError: No module named 'app.main'
FAILED test_complete_workflow.py::TestCompleteJobTrackingWorkflow::test_complete_ai_job_tracker_workflow - ModuleNotFoundError: No module named 'app.core.database'
FAILED test_complete_workflow.py::TestCompleteJobTrackingWorkflow::test_complete_ai_job_tracker_workflow - ImportError: cannot import name 'TestSessionLocal' from 'app.tests.fixtures.test_database'
        """
    
    # Parse failures and create issues
    failures = workflow.parse_test_failures(test_output)
    print(f"\n🔍 Parsed {len(failures)} actionable failures")
    
    if failures:
        # Create GitHub issues
        issue_urls = workflow.create_github_issues(failures)
        
        # Generate development roadmap
        roadmap = workflow.generate_development_roadmap(failures)
        
        # Save roadmap to file
        roadmap_file = Path("DEVELOPMENT_ROADMAP.md")
        with open(roadmap_file, "w") as f:
            f.write(roadmap)
        
        print(f"\n📋 Development roadmap saved to {roadmap_file}")
        
        if issue_urls:
            print(f"\n✅ Successfully created {len(issue_urls)} GitHub issues")
            print("🔗 Issue URLs:")
            for url in issue_urls:
                print(f"   {url}")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Review the generated issues and roadmap")
        print(f"   2. Start with highest priority issues")
        print(f"   3. Follow TDD approach for each component")
        print(f"   4. Re-run integration test to track progress")
        print(f"   5. Close issues as acceptance criteria are met")
    else:
        print("✅ No failures detected - integration test may be passing!")
    
    print("\n🏁 Workflow startup complete!")


if __name__ == "__main__":
    main()

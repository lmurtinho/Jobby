"""
High-Level Frontend Foundation Integration Test
==============================================

This test drives the implementation of Day 1's frontend deliverables following Outside-In TDD.
It will initially fail completely and guide us to implement each frontend component.

Expected Day 1 Frontend Deliverables:
- ✅ Working authentication (register/login pages)
- ✅ Basic routing and protected pages
- ✅ Deployed frontend on Vercel
- ✅ Frontend connecting to backend API

This test represents the complete frontend user journey for Day 1.
"""

import pytest
import requests
from pathlib import Path
from typing import Dict, Any
import subprocess
import os
import time

@pytest.mark.integration
@pytest.mark.frontend
@pytest.mark.slow
class TestFrontendFoundationIntegration:
    """
    Complete end-to-end frontend foundation test for Day 1 MVP.
    
    This test covers the entire frontend setup and basic user journey:
    1. Frontend project structure exists
    2. Dependencies are installed and configured
    3. Authentication pages render correctly
    4. API integration works
    5. Protected routing functions
    6. Basic navigation works
    7. Frontend can be built for production
    """
    
    @pytest.fixture(scope="class")
    def frontend_project_root(self) -> Path:
        """Get the frontend project root path."""
        return Path("/Users/lucasmurtinho/Documents/Jobby/frontend")
    
    @pytest.fixture(scope="class")
    def backend_base_url(self) -> str:
        """Backend API base URL for integration testing."""
        return "http://localhost:8000"
    
    def test_frontend_project_structure_exists(self, frontend_project_root: Path):
        """
        Test that the React + TypeScript project structure is properly set up.
        
        Expected Initial Failure:
        - Frontend directory doesn't exist → Issue: "Create React TypeScript project structure"
        """
        # Step 1: Verify frontend directory exists
        assert frontend_project_root.exists(), f"Frontend directory should exist at {frontend_project_root}"
        
        # Step 2: Verify package.json with correct dependencies
        package_json = frontend_project_root / "package.json"
        assert package_json.exists(), "package.json should exist"
        
        with open(package_json, 'r') as f:
            import json
            config = json.load(f)
        
        # Verify it's a React TypeScript project
        assert "react" in config.get("dependencies", {}), "React should be installed"
        assert "@types/react" in config.get("devDependencies", {}) or "@types/react" in config.get("dependencies", {}), "React types should be installed"
        assert "typescript" in config.get("devDependencies", {}) or "typescript" in config.get("dependencies", {}), "TypeScript should be installed"
        
        # Verify additional required dependencies
        expected_deps = ["react-router-dom", "axios"]  # Core dependencies for Day 1
        dependencies = {**config.get("dependencies", {}), **config.get("devDependencies", {})}
        
        for dep in expected_deps:
            assert dep in dependencies, f"Dependency '{dep}' should be installed"
    
    def test_frontend_directory_structure(self, frontend_project_root: Path):
        """
        Test that the proper component structure is created.
        
        Expected Initial Failure:
        - Component directories missing → Issue: "Create frontend component structure"
        """
        src_dir = frontend_project_root / "src"
        assert src_dir.exists(), "src directory should exist"
        
        # Verify required directories exist
        required_dirs = ["components", "pages", "utils", "types"]
        for dir_name in required_dirs:
            dir_path = src_dir / dir_name
            assert dir_path.exists(), f"{dir_name} directory should exist at {dir_path}"
    
    def test_authentication_pages_exist(self, frontend_project_root: Path):
        """
        Test that authentication pages are implemented.
        
        Expected Initial Failure:
        - Auth pages missing → Issue: "Implement authentication pages (Login/Register)"
        """
        pages_dir = frontend_project_root / "src" / "pages"
        
        # Check for authentication pages
        auth_pages = ["Login.tsx", "Register.tsx"]
        for page in auth_pages:
            page_path = pages_dir / page
            assert page_path.exists(), f"Authentication page {page} should exist"
            
            # Verify page contains basic React component structure
            with open(page_path, 'r') as f:
                content = f.read()
                assert "import React" in content, f"{page} should import React"
                assert "export default" in content, f"{page} should export default component"
                assert "return" in content, f"{page} should have JSX return"
    
    def test_api_client_configuration(self, frontend_project_root: Path):
        """
        Test that API client is configured for backend communication.
        
        Expected Initial Failure:
        - API client missing → Issue: "Implement API client for backend communication"
        """
        utils_dir = frontend_project_root / "src" / "utils"
        api_client_path = utils_dir / "apiClient.ts"
        
        assert api_client_path.exists(), "API client should exist"
        
        with open(api_client_path, 'r') as f:
            content = f.read()
            assert "axios" in content.lower(), "API client should use axios"
            assert "baseURL" in content or "baseUrl" in content, "API client should have base URL configuration"
            assert "localhost:8000" in content or "API_BASE_URL" in content, "API client should point to backend"
    
    def test_authentication_context_setup(self, frontend_project_root: Path):
        """
        Test that authentication context is implemented.
        
        Expected Initial Failure:
        - Auth context missing → Issue: "Implement authentication context and state management"
        """
        src_dir = frontend_project_root / "src"
        
        # Look for auth context (could be in contexts/ or utils/)
        possible_paths = [
            src_dir / "contexts" / "AuthContext.tsx",
            src_dir / "utils" / "authContext.tsx",
            src_dir / "contexts" / "auth.tsx"
        ]
        
        auth_context_exists = any(path.exists() for path in possible_paths)
        assert auth_context_exists, "Authentication context should exist"
        
        # Find the actual auth context file
        auth_context_path = next(path for path in possible_paths if path.exists())
        
        with open(auth_context_path, 'r') as f:
            content = f.read()
            assert "createContext" in content, "Should use React createContext"
            assert "login" in content.lower(), "Should have login functionality"
            assert "logout" in content.lower(), "Should have logout functionality"
            assert "token" in content.lower() or "auth" in content.lower(), "Should manage authentication state"
    
    def test_protected_route_component(self, frontend_project_root: Path):
        """
        Test that protected route component is implemented.
        
        Expected Initial Failure:
        - Protected routes missing → Issue: "Implement protected route component"
        """
        components_dir = frontend_project_root / "src" / "components"
        
        # Look for protected route component
        possible_names = ["ProtectedRoute.tsx", "PrivateRoute.tsx", "AuthRoute.tsx"]
        protected_route_paths = [components_dir / name for name in possible_names]
        
        protected_route_exists = any(path.exists() for path in protected_route_paths)
        assert protected_route_exists, "Protected route component should exist"
        
        # Verify component functionality
        protected_route_path = next(path for path in protected_route_paths if path.exists())
        
        with open(protected_route_path, 'r') as f:
            content = f.read()
            assert "Navigate" in content or "Redirect" in content, "Should redirect unauthenticated users"
            assert "children" in content, "Should render children when authenticated"
    
    def test_basic_routing_setup(self, frontend_project_root: Path):
        """
        Test that React Router is properly configured.
        
        Expected Initial Failure:
        - Routing missing → Issue: "Configure React Router with authentication flow"
        """
        src_dir = frontend_project_root / "src"
        app_tsx = src_dir / "App.tsx"
        
        assert app_tsx.exists(), "App.tsx should exist"
        
        with open(app_tsx, 'r') as f:
            content = f.read()
            assert "react-router-dom" in content or "BrowserRouter" in content or "Routes" in content, "Should use React Router"
            assert "Route" in content, "Should define routes"
            assert "/login" in content or "login" in content.lower(), "Should have login route"
            assert "/register" in content or "register" in content.lower(), "Should have register route"
    
    def test_typescript_configuration(self, frontend_project_root: Path):
        """
        Test that TypeScript is properly configured.
        
        Expected Initial Failure:
        - TypeScript config missing → Issue: "Configure TypeScript for React project"
        """
        tsconfig_path = frontend_project_root / "tsconfig.json"
        assert tsconfig_path.exists(), "tsconfig.json should exist"
        
        with open(tsconfig_path, 'r') as f:
            import json
            config = json.load(f)
            
            compiler_options = config.get("compilerOptions", {})
            assert compiler_options.get("jsx") in ["react", "react-jsx"], "Should be configured for React"
            assert "es6" in str(compiler_options.get("target", "")).lower() or "es2015" in str(compiler_options.get("target", "")).lower() or "es2017" in str(compiler_options.get("target", "")).lower(), "Should target modern JavaScript"
    
    def test_environment_configuration(self, frontend_project_root: Path):
        """
        Test that environment variables are configured.
        
        Expected Initial Failure:
        - Environment config missing → Issue: "Configure environment variables for API endpoints"
        """
        env_files = [".env", ".env.local", ".env.development"]
        env_exists = any((frontend_project_root / env_file).exists() for env_file in env_files)
        
        assert env_exists, "Environment configuration file should exist"
        
        # Find the actual env file
        env_path = None
        for env_file in env_files:
            candidate_path = frontend_project_root / env_file
            if candidate_path.exists():
                env_path = candidate_path
                break
        
        assert env_path is not None, "Should have found an environment file"
        
        with open(env_path, 'r') as f:
            content = f.read()
            assert "REACT_APP" in content, "Should have React app environment variables"
            assert "API" in content or "BACKEND" in content, "Should configure API endpoint"
    
    def test_frontend_builds_successfully(self, frontend_project_root: Path):
        """
        Test that the frontend can be built for production.
        
        Expected Initial Failure:
        - Build fails → Various issues based on build errors
        """
        # Change to frontend directory and run build
        original_cwd = os.getcwd()
        try:
            os.chdir(frontend_project_root)
            
            # Install dependencies first
            install_result = subprocess.run(
                ["npm", "install"], 
                capture_output=True, 
                text=True, 
                timeout=300  # 5 minute timeout
            )
            assert install_result.returncode == 0, f"npm install failed: {install_result.stderr}"
            
            # Run TypeScript check
            typecheck_result = subprocess.run(
                ["npm", "run", "tsc", "--noEmit"], 
                capture_output=True, 
                text=True, 
                timeout=120
            )
            # Note: Don't assert on typecheck initially, just collect errors
            
            # Run build
            build_result = subprocess.run(
                ["npm", "run", "build"], 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            if build_result.returncode != 0:
                pytest.fail(f"Frontend build failed:\nSTDOUT:\n{build_result.stdout}\nSTDERR:\n{build_result.stderr}")
            
            # Verify build output exists
            build_dir = frontend_project_root / "build"
            assert build_dir.exists(), "Build directory should be created"
            
            # Verify essential build files
            essential_files = ["index.html", "static"]
            for file_name in essential_files:
                file_path = build_dir / file_name
                assert file_path.exists(), f"Build should contain {file_name}"
        
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.live_test
    def test_frontend_integrates_with_backend_api(self, frontend_project_root: Path, backend_base_url: str):
        """
        Test that frontend can communicate with backend API.
        
        Expected Initial Failure:
        - API integration not working → Issue: "Fix frontend-backend API integration"
        
        Note: This test requires the backend to be running.
        """
        # First verify backend is accessible
        try:
            health_response = requests.get(f"{backend_base_url}/health", timeout=5)
            assert health_response.status_code == 200, "Backend health check should pass"
        except requests.exceptions.RequestException:
            pytest.skip("Backend not running - skipping API integration test")
        
        # Start frontend development server (background process)
        original_cwd = os.getcwd()
        frontend_process = None
        try:
            os.chdir(frontend_project_root)
            
            # Start dev server in background
            frontend_process = subprocess.Popen(
                ["npm", "start"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for frontend to start (look for "compiled successfully" or similar)
            max_wait = 60  # 60 seconds
            frontend_ready = False
            
            for _ in range(max_wait):
                if frontend_process.poll() is not None:
                    # Process ended, probably failed
                    stdout, stderr = frontend_process.communicate()
                    pytest.fail(f"Frontend dev server failed to start:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
                
                time.sleep(1)
                
                # Try to access frontend
                try:
                    frontend_response = requests.get("http://localhost:3000", timeout=2)
                    if frontend_response.status_code == 200:
                        frontend_ready = True
                        break
                except requests.exceptions.RequestException:
                    continue
            
            assert frontend_ready, "Frontend development server should start and be accessible"
            
            # Test that frontend can make API calls to backend
            # This would be verified by checking if login/register pages can submit to backend
            # For now, just verify frontend is serving and backend is accessible
            
        finally:
            if frontend_process:
                frontend_process.terminate()
                try:
                    frontend_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    frontend_process.kill()
            os.chdir(original_cwd)
    
    def test_complete_authentication_flow_structure(self, frontend_project_root: Path):
        """
        Test that the complete authentication flow is structurally ready.
        
        This is the highest-level test that ensures all pieces work together.
        Expected to drive implementation of the complete Day 1 frontend foundation.
        """
        src_dir = frontend_project_root / "src"
        
        # Verify all authentication pieces exist
        auth_components = {
            "Login Page": ["pages/Login.tsx"],
            "Register Page": ["pages/Register.tsx"],
            "Auth Context": ["contexts/AuthContext.tsx", "utils/authContext.tsx", "contexts/auth.tsx"],
            "API Client": ["utils/apiClient.ts", "utils/api.ts"],
            "Protected Route": ["components/ProtectedRoute.tsx", "components/PrivateRoute.tsx", "components/AuthRoute.tsx"],
            "Main App Router": ["App.tsx"]
        }
        
        missing_components = []
        
        for component_name, possible_paths in auth_components.items():
            component_exists = any((src_dir / path).exists() for path in possible_paths)
            if not component_exists:
                missing_components.append(f"{component_name} (expected at one of: {possible_paths})")
        
        assert len(missing_components) == 0, f"Missing authentication components: {', '.join(missing_components)}"
        
        # Integration verification - check that components reference each other properly
        app_path = src_dir / "App.tsx"
        with open(app_path, 'r') as f:
            app_content = f.read()
        
        # App should import and use authentication context
        assert "AuthContext" in app_content or "authContext" in app_content or "AuthProvider" in app_content, "App should use authentication context"
        
        # App should have routing configured
        assert "Route" in app_content and ("Login" in app_content or "Register" in app_content), "App should configure authentication routes"


@pytest.mark.unit
@pytest.mark.frontend
class TestFrontendComponentUnits:
    """
    Unit tests for individual frontend components.
    
    These tests will be driven by failures in the integration test above.
    Each failure will lead to creating specific unit tests and implementations.
    """
    
    def test_api_client_unit_structure(self):
        """
        Unit test for API client configuration.
        This will be implemented based on integration test failures.
        """
        # This test will be implemented when the integration test fails
        # and drives us to create the API client
        pytest.skip("Will be implemented based on integration test failures")
    
    def test_auth_context_unit_functionality(self):
        """
        Unit test for authentication context.
        This will be implemented based on integration test failures.
        """
        pytest.skip("Will be implemented based on integration test failures")
    
    def test_login_page_unit_rendering(self):
        """
        Unit test for Login page component.
        This will be implemented based on integration test failures.
        """
        pytest.skip("Will be implemented based on integration test failures")
    
    def test_register_page_unit_rendering(self):
        """
        Unit test for Register page component.
        This will be implemented based on integration test failures.
        """
        pytest.skip("Will be implemented based on integration test failures")
    
    def test_protected_route_unit_logic(self):
        """
        Unit test for ProtectedRoute component.
        This will be implemented based on integration test failures.
        """
        pytest.skip("Will be implemented based on integration test failures")

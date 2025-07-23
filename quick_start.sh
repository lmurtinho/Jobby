#!/bin/bash

# Quick Start Script for AI Job Tracker Outside-In TDD Workflow
# This script sets up the development environment and starts the workflow

set -e  # Exit on any error

echo "🚀 AI Job Tracker - Outside-In TDD Workflow Setup"
echo "=================================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $python_version"

# Install requirements
echo "📦 Installing workflow requirements..."
if [ -f "scripts/workflow_requirements.txt" ]; then
    pip install -r scripts/workflow_requirements.txt
    echo "✅ Requirements installed successfully"
else
    echo "⚠️  scripts/workflow_requirements.txt not found, installing basic packages..."
    pip install pytest requests
fi

# Install backend requirements if available
if [ -f "backend/requirements.txt" ]; then
    echo "📦 Installing backend requirements..."
    pip install -r backend/requirements.txt
    echo "✅ Backend requirements installed successfully"
fi

# Create project structure
echo "🏗️  Creating project structure..."
python scripts/workflow_starter.py --create-structure --skip-test

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN environment variable not set"
    echo "   GitHub issues will not be created automatically"
    echo "   To enable issue creation:"
    echo "   1. Create a GitHub Personal Access Token"
    echo "   2. export GITHUB_TOKEN='your_token_here'"
    echo "   3. Re-run this script"
    echo ""
    
    read -p "Continue without GitHub integration? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Please set GITHUB_TOKEN and try again."
        exit 1
    fi
fi

# Run the workflow starter
echo "🧪 Running integration test to identify components to build..."
echo "This will fail initially - that's expected and drives the development!"
echo ""

if [ -n "$GITHUB_TOKEN" ]; then
    echo "🔗 Creating GitHub issues for each component..."
    python scripts/workflow_starter.py
else
    echo "📋 Running in dry-run mode (no GitHub issues will be created)..."
    python scripts/workflow_starter.py --dry-run
fi

echo ""
echo "🎉 Workflow setup complete!"
echo ""
echo "📋 Next Steps:"
echo "   1. Check DEVELOPMENT_ROADMAP.md for implementation plan"
echo "   2. Review generated GitHub issues (if token provided)"
echo "   3. Start with highest priority components"
echo "   4. Use TDD: write test → implement → make test pass"
echo "   5. Re-run 'python scripts/workflow_starter.py' to track progress"
echo ""
echo "📚 Documentation:"
echo "   - WORKFLOW_README.md: Complete workflow guide"
echo "   - CLAUDE.md: TDD best practices and coding standards"
echo "   - README.md: Full project specification"
echo ""
echo "🚀 Ready to build the AI Job Tracker!"

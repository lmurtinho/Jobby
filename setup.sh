#!/bin/bash

# Setup script for AI Job Tracker development environment
# This script creates a virtual environment and installs dependencies

set -e

echo "🚀 Setting up AI Job Tracker development environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Activate the environment: source .venv/bin/activate"
echo "   2. Run the workflow starter: python scripts/workflow_starter.py"
echo "   3. Follow the generated roadmap to implement components"
echo ""
echo "📚 For more information, see README.md and CLAUDE.md"

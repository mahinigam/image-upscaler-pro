#!/bin/bash

# Image Upscaler - Startup Script
# This script sets up the environment and launches the application

set -e

echo ""
echo "Image Upscaler Pro"
echo "========================"
echo ""

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Using Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes on first run)..."
pip install -r requirements.txt -q

# Create bin directory for models
mkdir -p bin

# Launch the application
echo ""
echo "Launching Image Upscaler..."
echo "Open http://localhost:7860 in your browser"
echo ""
python app.py

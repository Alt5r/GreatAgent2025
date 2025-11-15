#!/bin/bash

# Setup script for Red Teaming System

echo "=================================================="
echo "AI Agent Red Teaming System - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
echo ""
echo "Setting up environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template"
else
    echo ".env file already exists"
fi

# Create results directory
echo ""
echo "Creating results directory..."
mkdir -p results

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "To get started:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run quick test: python main.py --mode quick --agents bear"
echo "  3. See README.md for more usage examples"
echo ""

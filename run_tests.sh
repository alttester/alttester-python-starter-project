#!/bin/bash

# AltTester Python Test Runner Script
# This script sets up the environment and runs the Python tests

echo "AltTester Python Test Runner"
echo "============================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p reports
mkdir -p screenshots-and-logs

# Set environment variables if .env file exists
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the tests
echo "Running tests..."
python -m pytest "$@"

# Capture exit code
exit_code=$?

# Deactivate virtual environment
deactivate

# create allure report
if command -v allure &> /dev/null; then
    echo "Generating Allure report..."
    allure generate reports/allure-results --clean -o reports/Allure --single-file
    echo "Allure report generated at reports/Allure/index.html"
else
    echo "Allure command not found. Skipping report generation."
fi

echo "Test execution completed with exit code: $exit_code"
exit $exit_code

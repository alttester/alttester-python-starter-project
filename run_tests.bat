@echo off

rem AltTester Python Test Runner Script for Windows
rem This script sets up the environment and runs the Python tests

echo AltTester Python Test Runner
echo ============================

rem Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

rem Check Python version (simplified check)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo Python version: %python_version%

rem Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

rem Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

rem Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

rem Create necessary directories
if not exist "reports" mkdir reports
if not exist "screenshots-and-logs" mkdir screenshots-and-logs

rem Load environment variables if .env file exists
if exist ".env" (
    echo Loading environment variables from .env file...
    for /f "usebackq eol=# tokens=1,2 delims==" %%i in (".env") do (
        if not "%%i"=="" set "%%i=%%j"
    )
)

rem Run the tests
echo Running tests...
python -m pytest %*

rem Capture exit code
set exit_code=%errorlevel%

echo Test execution completed with exit code: %exit_code%
exit /b %exit_code%

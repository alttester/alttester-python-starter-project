# AltTester Python Test Project - Getting Started Guide

## 🎯 What is this?

This is a **beginner-friendly** test automation project for Unity games using AltTester and Python. If you're new to automated testing or Python, don't worry! This guide will walk you through everything step-by-step.

**What you'll learn:**
- How to automatically test your Unity game using Python (no manual clicking!)
- How to find and interact with game objects programmatically  
- How to verify your game works correctly across different scenarios
- How to use pytest (Python's most popular testing framework)

## ⚡ Quick Start (5 minutes to first test!)

**The fastest way to get started:**

1. **Make sure your Unity game is running** with AltTester already connected
2. **Run the test script:**
   - **macOS/Linux:** `./run_tests.sh`
   - **Windows:** `run_tests.bat`
3. **Watch the magic happen!** ✨

The template includes example tests that you can adapt for any game!

## 📋 Complete Beginner Setup

### Step 1: What You Need Before Starting

Before we begin, you need:

1. **A Unity game with AltTester integrated** (this should already be done by your development team)
2. **AltTester Desktop app** - Download from [altom.com/alttester](https://altom.com/alttester/)
3. **Python 3.8 or higher** - Download from [python.org](https://python.org/downloads/)

### Step 2: Get AltTester Desktop Running

1. **Download and install AltTester Desktop**
2. **Launch AltTester Desktop**  
3. **Start your Unity game** (the one with AltTester integration)
4. **Verify connection:** You should see your game appear in AltTester Desktop

⚠️ **Important:** Your game must be connected to AltTester Desktop before running tests!

### Step 3: Prepare Your Test Project

1. **Download/clone this project** to your computer
2. **Open a terminal/command prompt** in the project folder
3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Activate it:
   # macOS/Linux:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Run Your First Test

**Option A: Use the Simple Scripts (Recommended for beginners)**

- **macOS/Linux:**
  ```bash
  ./run_tests.sh
  ```
- **Windows:**
  ```cmd
  run_tests.bat
  ```

**Option B: Use pytest directly (More control)**
```bash
pytest -v
```

🎉 **Congratulations!** You just ran your first automated Python test!

## 🚀 Features

- **AltTester Driver Integration**: Full support for AltTester Unity SDK
- **Multi-platform Testing**: Android, iOS, and WebGL support
- **Page Object Model**: Clean separation of concerns with View classes
- **Comprehensive Reporting**: Allure reports with screenshots and attachments
- **Selenium Integration**: WebGL testing support
- **Appium Integration**: Mobile testing support
- **Configurable Environment**: Environment variable support

## Project Structure

```
alttester-python-starter-project/
├── common/                    # Common utilities and configuration
│   ├── __init__.py
│   ├── driver_container.py    # Driver management
│   ├── reporter.py           # Logging and reporting utilities
│   └── test_configuration.py # Configuration management
├── views/                     # Page Object Model views
│   ├── __init__.py
│   ├── base_view.py          # Base view with common functionality
│   ├── main_menu_view.py     # Main menu interactions
│   └── gameplay_view.py      # Gameplay interactions
├── tests/                     # Test cases
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures and configuration
│   ├── base_test.py          # Base test class
│   └── test_main_menu.py     # Main menu test cases
├── reports/                # Generated test reports
├── screenshots-and-logs/    # Generated screenshots and logs
├── requirements.txt           # Python dependencies
├── pytest.ini               # Pytest configuration
└── README.md                 # This file
```

## 🛠️ Setup Options

### Option 1: Local Testing (Easiest - Recommended for Beginners)

This is the **simplest way** to get started. Your Unity game runs on the same computer as your tests.

**Requirements:**
- Unity game with AltTester integration running locally
- AltTester Desktop app connected to your game

**How to run:**
```bash
# macOS/Linux
./run_tests.sh

# Windows
run_tests.bat
```

### Option 2: Mobile Testing with Appium (Advanced)

Use this when you want to test your game on mobile devices (Android/iOS).

**Additional Requirements:**
- **Appium Server** installed and running
- **Android SDK/Xcode** (depending on platform)
- **Physical device or emulator** connected

**Setup Appium (if you're new to this):**

1. **Install Node.js** (required for Appium):
   - Download from [nodejs.org](https://nodejs.org/)

2. **Install Appium:**
   ```bash
   npm install -g appium
   ```

3. **Start Appium Server:**
   ```bash
   appium
   ```

4. **Run tests with Appium:**
   ```bash
   # macOS/Linux
   RUN_TESTS_WITH_APPIUM=true ./run_tests.sh
   
   # Windows
   set RUN_TESTS_WITH_APPIUM=true && run_tests.bat
   ```

### Option 3: WebGL Testing with Selenium (Advanced)

Use this when your game is deployed as WebGL and runs in a browser.

**Additional Requirements:**
- **Chrome browser** installed
- **ChromeDriver** (automatically managed by Selenium)

**Run WebGL tests:**
```bash
# macOS/Linux
TEST_PLATFORM=WebGL RUN_TESTS_WITH_SELENIUM=true ./run_tests.sh

# Windows
set TEST_PLATFORM=WebGL && set RUN_TESTS_WITH_SELENIUM=true && run_tests.bat
```

## 🎮 Understanding the Code (For Python Beginners)

### What are "Views"?

Think of Views as **representatives** of your game screens. Instead of manually clicking buttons, Views do it programmatically.

**Example:** `main_menu_view.py` represents your game's main menu and can:
- Click the "Play" button
- Check if the menu loaded correctly
- Navigate to other screens

### What are "Tests"?

Tests are **instructions** that tell the computer how to verify your game works correctly.

**Example:** A test might:
1. Start the game
2. Check if the main menu appears
3. Click "Play"  
4. Verify the game starts correctly

### Project Structure Explained

```
alttester-python-starter-project/
├── views/                     # 🎭 Game screen representatives
│   ├── main_menu_view.py     #    - Handles main menu interactions
│   └── gameplay_view.py      #    - Handles gameplay interactions
├── tests/                     # 🧪 Test instructions
│   └── test_main_menu.py     #    - Tests for main menu
├── common/                    # 🔧 Shared utilities
└── run_tests.sh/.bat         # 🚀 Simple test runners
```

### Python-Specific Benefits

- **Easy to read:** Python code is very readable, even for beginners
- **pytest framework:** Industry-standard testing framework with great features
- **Rich ecosystem:** Lots of helpful libraries for testing
- **Great for beginners:** Python is often the first programming language people learn

## 🔧 Customizing for Your Game

### Step 1: Update Game Object Names

1. **Open `views/main_menu_view.py`**
2. **Find this section:**
   ```python
   PLAY_BUTTON = (By.NAME, "PlayButtonName")
   ```
3. **Replace `"PlayButtonName"`** with your actual button name from Unity
4. **Repeat for other elements**

### Step 2: Add Your Own Tests

1. **Open `tests/test_main_menu.py`**
2. **Add a new test function:**
   ```python
   def test_my_game_feature(self):
       """Test my awesome game feature"""
       # Your test steps here
       self.reporter.log("Testing my awesome feature")
       # Add assertions to verify behavior
       assert True  # Replace with actual test logic
   ```

## 🐛 Troubleshooting (Common Beginner Issues)

### ❌ "Connection refused" or "Cannot connect"
**Problem:** AltTester can't connect to your game
**Solution:**
1. Make sure your Unity game is running
2. Check that AltTester Desktop shows your game as connected
3. Verify the game has AltTester integration

### ❌ "ModuleNotFoundError" or import errors
**Problem:** Python can't find required packages
**Solution:**
1. Make sure you activated your virtual environment
2. Run `pip install -r requirements.txt` again
3. Check that you're in the correct project directory

### ❌ "Element not found" or "Object not found"
**Problem:** Test can't find a button or game object
**Solution:**
1. Check the exact name of your game object in Unity
2. Update the locator in your View class
3. Make sure the object is visible when the test runs

### ❌ "Timeout" errors
**Problem:** Test is waiting too long for something to happen
**Solution:**
1. Increase timeout values in your test
2. Check if the expected action actually happens in the game
3. Add debug logs to see what's happening

### ❌ Tests fail randomly
**Problem:** Tests work sometimes but not always
**Solution:**
1. Use proper wait conditions before interactions
2. Check if your game loads at different speeds
3. Make tests more robust with explicit waits

## 💡 Next Steps for Python Learners

Once you're comfortable with the basics:

1. **Learn more Python:** [python.org/about/gettingstarted/](https://www.python.org/about/gettingstarted/)
2. **Explore pytest features:** Fixtures, parameterized tests, test markers
3. **Add more Views** for different game screens
4. **Create data-driven tests** using pytest parameters
5. **Set up continuous integration** with GitHub Actions or Jenkins
6. **Explore Python testing ecosystem:** Mock, coverage, property-based testing

## 🛠️ Installation

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.8 or higher
   # If python doesn't work, try python3
   python3 --version
   ```

2. **Create and activate virtual environment** (strongly recommended):
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it:
   # macOS/Linux:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   
   # You should see (venv) in your terminal prompt when activated
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

**💡 Virtual Environment Tips:**
- Always activate your virtual environment before running tests
- If you see import errors, check if your virtual environment is activated
- To deactivate: just type `deactivate`

## ⚙️ Configuration

The project works with **default settings** out of the box for local testing.

### Environment Variables (Optional Customization)

You can customize behavior using environment variables. Set these in your terminal or create a `.env` file:

```bash
# AltTester Connection Settings
ALT_TESTER_SERVER_URL=127.0.0.1          # Where your game is running
ALT_TESTER_SERVER_PORT=13000              # AltTester port (usually 13000)
ALT_TESTER_APP_NAME=__default__           # Your app name
ALT_TESTER_CONNECT_TIMEOUT=60             # How long to wait for connection

# Testing Platform
TEST_PLATFORM=Android                      # Android, iOS, or WebGL

# Mobile Testing (Advanced)
DEVICE_NAME=android                       # Your device name
APP_BUNDLE_ID=com.example.app            # Your app's bundle ID
RUN_TESTS_WITH_APPIUM=false              # Enable Appium for mobile

# WebGL Testing (Advanced)  
RUN_TESTS_WITH_SELENIUM=false            # Enable Selenium for WebGL
WEBGL_URL=https://example.com/game       # URL of your WebGL game
```

**For beginners:** Don't worry about these settings initially. The defaults work fine for local testing!

## 🚀 Running Tests - Multiple Ways

### Method 1: Simple Scripts (Beginner-Friendly)

**macOS/Linux:**
```bash
# Run all tests
./run_tests.sh

# The script handles everything automatically!
```

**Windows:**
```cmd
REM Run all tests
run_tests.bat
```

### Method 2: Using pytest directly (More Control)

```bash
# Make sure your virtual environment is activated first!
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run all tests
pytest

# Run with verbose output (shows more details)
pytest -v

# Run specific test file
pytest tests/test_main_menu.py

# Run specific test method
pytest tests/test_main_menu.py::TestMainMenu::test_main_menu_loads_successfully

# Run tests with specific markers (if you add them)
pytest -m "smoke"
```

### Method 3: With Environment Variables (Advanced)

**macOS/Linux:**
```bash
# Run with different AltTester port
ALT_TESTER_SERVER_PORT=13001 ./run_tests.sh

# Run WebGL tests
TEST_PLATFORM=WebGL RUN_TESTS_WITH_SELENIUM=true ./run_tests.sh

# Run mobile tests with Appium
RUN_TESTS_WITH_APPIUM=true ./run_tests.sh
```

**Windows:**
```cmd
REM Run with different AltTester port
set ALT_TESTER_SERVER_PORT=13001 && run_tests.bat

REM Run WebGL tests
set TEST_PLATFORM=WebGL && set RUN_TESTS_WITH_SELENIUM=true && run_tests.bat

REM Run mobile tests with Appium
set RUN_TESTS_WITH_APPIUM=true && run_tests.bat
```

### Method 4: Parallel Testing (Advanced)

```bash
# Run tests in parallel (faster execution)
pytest -n auto

# Run 4 tests at the same time
pytest -n 4
```

## 📊 Test Reports

### Automatic Reports
The project generates several types of reports automatically:

- **HTML Report:** `reports/pytest_report.html` - Open in your browser to see results
- **JSON Report:** `reports/report.json` - For CI/CD integration
- **Allure Reports:** Advanced reporting with screenshots and detailed info

### Viewing Reports

**Basic HTML Report:**
```bash
# After running tests, open this file in your browser:
open reports/pytest_report.html        # macOS
start reports/pytest_report.html       # Windows
xdg-open reports/pytest_report.html    # Linux
```

**Advanced Allure Reports (Optional):**
```bash
# First install Allure (if you want fancy reports)
# macOS: brew install allure
# Windows: Download from allure.qatools.ru

# Generate Allure results
pytest --alluredir=reports/allure-results

# View interactive Allure report
allure serve reports/allure-results
```

## 🧪 Writing Your Own Tests (Python Basics)

### Basic Test Structure
```python
import pytest
import allure
from tests.base_test import BaseTest
from views.main_menu_view import MainMenuView

class TestMainMenu(BaseTest):
    
    def setup_method(self):
        """This runs before each test method"""
        self.main_menu_view = MainMenuView(self.drivers)
    
    @allure.feature("Main Menu")  # Organizes tests in reports
    @allure.story("Menu Loading")
    def test_main_menu_loads_successfully(self):
        """Test that the main menu loads successfully"""
        
        # Use allure.step to organize test steps in reports
        with allure.step("Verify game scene is loaded"):
            current_scene = self.drivers.alt_driver.get_current_scene()
            assert current_scene, "Game did not launch successfully"
```

### Python Testing Concepts for Beginners

**Classes and Methods:**
- `class TestMainMenu` - Groups related tests together
- `def test_something()` - Individual test functions (must start with "test_")

**Assertions:**
```python
# Check if something is true
assert condition, "Error message if false"

# Check if values are equal
assert actual_value == expected_value

# Check if something exists
assert game_object is not None
```

**Setup and Teardown:**
```python
def setup_method(self):
    """Runs before each test - set up test data"""
    pass

def teardown_method(self):
    """Runs after each test - clean up"""  
    pass
```

## 🐛 Troubleshooting

### Common Python/pytest Issues

1. **"pytest: command not found"**
   - Make sure your virtual environment is activated
   - Try `python -m pytest` instead of just `pytest`

2. **Import errors or ModuleNotFoundError**
   - Activate your virtual environment: `source venv/bin/activate`
   - Install requirements: `pip install -r requirements.txt`
   - Make sure you're in the project directory

3. **"No tests found" or tests don't run**
   - Test files must start with `test_` or end with `_test.py`
   - Test functions must start with `test_`
   - Make sure test files are in the `tests/` directory

### Common AltTester Issues

1. **Connection refused/timeout**
   - Ensure your Unity game is running with AltTester enabled
   - Check that AltTester Desktop shows your game as connected
   - Verify firewall settings allow connections on port 13000

2. **Element not found errors**
   - Check Unity Inspector for exact object names
   - Make sure objects are active and visible when test runs
   - Try using different locator strategies (by tag, by path, etc.)

3. **Mobile/Appium issues**
   - Ensure Appium server is running (`appium` command)
   - Check device is connected: `adb devices` (Android)
   - Verify device capabilities in test configuration

### Debug Tips for Beginners

**Add debug output:**
```python
def test_something(self):
    print("Debug: Starting test")  # Simple debug output
    self.reporter.log("More detailed log message")  # Better logging
```

**Take screenshots for debugging:**
```python
# Screenshots are automatically taken on test failures
# They're saved in the screenshots-and-logs/ directory
```

**Check what's happening step by step:**
```python
def test_step_by_step(self):
    with allure.step("Step 1: Load main menu"):
        # Your code here
        pass
    
    with allure.step("Step 2: Click play button"):
        # Your code here  
        pass
```

## 🤝 Contributing & Learning More

### Adding New Tests
When adding tests or functionality:

1. **Follow the existing project structure**
2. **Use the Page Object Model** (Views) for UI interactions  
3. **Add appropriate test descriptions** and allure annotations
4. **Include error handling** and logging
5. **Test your changes** before committing

### Learning Resources

**Python Basics:**
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/) (Free book)

**pytest Framework:**
- [pytest Documentation](https://docs.pytest.org/) 
- [Real Python pytest Guide](https://realpython.com/pytest-python-testing/)

**AltTester:**
- [AltTester Documentation](https://altom.com/alttester/)
- [AltTester Python SDK](https://altom.com/alttester/docs/sdk/python/)

**Test Automation:**
- [Test Automation University](https://testautomationu.applitools.com/) (Free courses)

### Community and Support

- **AltTester Discord:** Join the community for help and discussions
- **GitHub Issues:** Report bugs or request features
- **Stack Overflow:** Tag questions with `alttester` and `python`

## 📄 License

This template is provided as-is for educational and development purposes. Modify and adapt as needed for your projects.


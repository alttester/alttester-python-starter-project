# AltTester Python Test Project

This project provides a Python implementation of the AltTester test framework using pytest instead of NUnit. It maintains the exact same functionality as the original C# project but uses Python equivalents.

## Features

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

## Installation

1. **Install Python 3.8+**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Create and activate virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The project uses environment variables for configuration. You can set these in your environment or create a `.env` file:

```bash
# AltTester Configuration
ALT_TESTER_SERVER_URL=127.0.0.1
ALT_TESTER_SERVER_PORT=13000
ALT_TESTER_APP_NAME=__default__
ALT_TESTER_CONNECT_TIMEOUT=60

# Platform Configuration
TEST_PLATFORM=Android  # Android, iOS, WebGL
DEVICE_NAME=android
APP_BUNDLE_ID=com.example.app

# Driver Configuration
RUN_TESTS_WITH_APPIUM=false
RUN_TESTS_WITH_SELENIUM=false

# WebGL Configuration
WEBGL_URL=https://example.com/game
```

## Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_main_menu.py

# Run specific test method
pytest tests/test_main_menu.py::TestMainMenu::test_main_menu_loads_successfully

# Run tests with specific markers
pytest -m "smoke"
pytest -m "not slow"
```

### Test Execution with Options
```bash
# Run tests in parallel
pytest -n auto

# Run tests with verbose output
pytest -v

# Run tests and generate Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ALT_TESTER_SERVER_URL` | `127.0.0.1` | AltTester server IP address |
| `ALT_TESTER_SERVER_PORT` | `13000` | AltTester server port |
| `ALT_TESTER_APP_NAME` | `__default__` | Application name for AltTester |
| `ALT_TESTER_CONNECT_TIMEOUT` | `60` | Connection timeout in seconds |
| `TEST_PLATFORM` | `Android` | Target platform (Android/iOS/WebGL) |
| `DEVICE_NAME` | `android` | Device name for mobile testing |
| `APP_BUNDLE_ID` | `com.example.app` | Application bundle ID |
| `RUN_TESTS_WITH_APPIUM` | `false` | Enable Appium driver |
| `RUN_TESTS_WITH_SELENIUM` | `false` | Enable Selenium driver |
| `WEBGL_URL` | `https://example.com/game` | WebGL game URL |

## Writing Tests

### Basic Test Structure
```python
import pytest
import allure
from tests.base_test import BaseTest
from views.main_menu_view import MainMenuView

class TestMainMenu(BaseTest):
    
    def setup_method(self):
        """Set up before each test method"""
        self.main_menu_view = MainMenuView(self.drivers)
    
    @allure.feature("Main Menu")
    @allure.story("Menu Loading")
    def test_main_menu_loads_successfully(self):
        """Test that the main menu loads successfully"""
        with allure.step("Verify game scene is loaded"):
            current_scene = self.drivers.alt_driver.get_current_scene()
            assert current_scene, "Game did not launch successfully"
```

### Using Page Objects
```python
def test_start_new_game(self):
    """Test starting a new game"""
    # Wait for main menu to be ready
    self.main_menu_view.wait_for_main_menu_ready(timeout_seconds=2)
    
    # Start new game
    self.main_menu_view.start_new_game(player_name="TestPlayer")
    
    # Verify gameplay started
    self.gameplay_view.wait_for_gameplay_ready(timeout_seconds=2)
    assert self.gameplay_view.is_main_character_present()
```

## Reporting

### Allure Reports
Generate comprehensive Allure reports with screenshots, logs, and test execution details:

```bash
# Generate Allure results
pytest --alluredir=reports/allure-results

# View Allure report
allure serve reports/allure-results
```

### HTML Reports
Basic HTML reports are generated automatically:
- `reports/pytest_report.html` - Pytest HTML report
- `reports/report.json` - JSON report for CI/CD integration

## Troubleshooting

### Common Issues

1. **Connection Issues**
   - Ensure AltTester is running in your Unity game
   - Check firewall settings
   - Verify the correct IP and port

2. **Element Not Found**
   - Take screenshots to debug UI state
   - Check element locators in Unity
   - Increase wait timeouts if needed

3. **Mobile Testing**
   - Ensure Appium server is running
   - Verify device is connected and accessible
   - Check device capabilities

### Debug Mode
Enable debug logging by setting the environment variable:
```bash
export ALT_TESTER_DEBUG=true
```

## Contributing

When adding new tests or functionality:

1. Follow the existing project structure
2. Use the Page Object Model for UI interactions
3. Add appropriate Allure annotations
4. Include error handling and logging
5. Update documentation as needed


import pytest
import allure
import os
import tempfile
from datetime import datetime
from alttester import AltDriver
from alttester.commands import NotificationType
from appium import webdriver as appium_webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from common.driver_container import DriverContainer
from common.test_configuration import TestConfiguration, PlatformType
from common.reporter import Reporter


@pytest.fixture(scope="class", autouse=True)
def setup_drivers(request):
    """Session-level fixture to set up all drivers"""
    drivers = None
    unity_logs = {}

    try:
        with allure.step("Initialize Test Configuration and Start All Drivers"):
            drivers = start_all_drivers()
            setup_unity_log_listener(drivers, unity_logs, request)
            request.cls.drivers = drivers
            yield drivers

    except Exception as ex:
        pytest.fail(f"Exception during driver setup: {ex}")
        request.cls.drivers = None
    finally:
        # Cleanup
        add_unity_logs_to_allure(unity_logs)
        if drivers:
            stop_all_drivers(drivers)
        Reporter.log("All drivers stopped and cleanup completed.")


@pytest.fixture(autouse=True)
def auto_screenshot_on_failure(request):
    """Automatically take screenshot on test failure"""
    yield
    
    # This runs after each test
    if request.node.rep_call.failed:
        test_name = request.node.name
        Reporter.take_screenshot(f"{test_name}_Failed")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def start_all_drivers() -> DriverContainer:
    """Start all configured drivers"""
    Reporter.log("Setting up test environment...")
    Reporter.log(f"Platform: {TestConfiguration.PLATFORM.value}")
    Reporter.log(f"Running tests with Appium: {TestConfiguration.RUNNING_WITH_APPIUM}")
    Reporter.log(
        f"Running tests with Selenium: {TestConfiguration.RUNNING_WITH_SELENIUM}"
    )

    appium_driver = None
    selenium_driver = None

    if TestConfiguration.RUNNING_WITH_APPIUM:
        appium_driver = start_appium_driver()

    if TestConfiguration.RUNNING_WITH_SELENIUM:
        selenium_driver = start_selenium_driver()

    alt_driver = start_alttester_driver()

    drivers = DriverContainer(alt_driver, appium_driver, selenium_driver)

    Reporter.log("All drivers started successfully")
    return drivers


@allure.step("Start AltTester Driver")
def start_alttester_driver() -> AltDriver:
    """Start the AltTester driver"""
    Reporter.log(
        f"Connecting to AltTester at {TestConfiguration.ALT_TESTER_SERVER_URL}:{TestConfiguration.ALT_TESTER_SERVER_PORT}"
    )

    driver = AltDriver(
        host=TestConfiguration.ALT_TESTER_SERVER_URL,
        port=TestConfiguration.ALT_TESTER_SERVER_PORT,
        app_name=TestConfiguration.ALT_TESTER_APP_NAME,
        enable_logging=False,
    )

    Reporter.alt_driver = driver
    Reporter.log("Successfully connected to the game.")

    return driver


@allure.step("Start Appium Driver")
def start_appium_driver():
    """Start the Appium driver based on platform configuration"""
    Reporter.log("Setting up Appium driver...")

    desired_caps = {}
    driver = None

    if TestConfiguration.PLATFORM == PlatformType.ANDROID:
        desired_caps.update(
            {
                "platformName": "Android",
                "automationName": "UiAutomator2",
                "newCommandTimeout": 2000,
                "autoGrantPermissions": True,
                "deviceName": TestConfiguration.DEVICE_NAME,
                "appPackage": TestConfiguration.APP_BUNDLE_ID,
            }
        )
        driver = appium_webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

    elif TestConfiguration.PLATFORM == PlatformType.IOS:
        desired_caps.update(
            {
                "platformName": "iOS",
                "deviceName": TestConfiguration.DEVICE_NAME,
                "bundleId": TestConfiguration.APP_BUNDLE_ID,
            }
        )
        driver = appium_webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

    else:
        Reporter.log("Appium not supported for current platform")

    return driver


@allure.step("Start Selenium Driver")
def start_selenium_driver():
    """Start the Selenium driver for WebGL testing"""
    if TestConfiguration.PLATFORM == PlatformType.WEBGL:
        Reporter.log("Setting up Chrome driver for WebGL testing...")

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(TestConfiguration.WEBGL_URL)

        return driver

    Reporter.log("Selenium not needed for current platform")
    return None


def stop_all_drivers(drivers: DriverContainer) -> None:
    """Stop all drivers and clean up resources"""
    try:
        if drivers.alt_driver:
            drivers.alt_driver.stop()
        if drivers.selenium_driver:
            drivers.selenium_driver.quit()
        if drivers.appium_driver:
            drivers.appium_driver.quit()

        Reporter.log("All drivers stopped successfully")
    except Exception as ex:
        Reporter.log(f"Error stopping drivers: {ex}")


def setup_unity_log_listener(
    drivers: DriverContainer, unity_logs: dict, request
) -> None:
    """Set up Unity log listener. This will capture Unity logs during tests."""
    if not drivers.alt_driver:
        return

    Reporter.log("Setting up Unity log listener")

    project_directory = os.getcwd()
    log_directory = os.path.join(project_directory, "screenshots-and-logs")
    os.makedirs(log_directory, exist_ok=True)

    # Create timestamp for this test run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def log_callback(notification):
        """Callback function to handle Unity log notifications"""
        try:
            test_name = request.cls.__name__ if request.cls else "UnknownTest"

            filename = f"{test_name}-UnityLogs-{timestamp}.txt"
            filepath = os.path.join(log_directory, filename)

            with open(filepath, "a", encoding="utf-8") as f:
                f.write(f"{notification.message}\n")
                f.write(f"StackTrace : {notification.stack_trace}\n")

            if filename not in unity_logs:
                unity_logs[filename] = filepath

        except Exception as e:
            Reporter.log(f"Error saving Unity log: {e}")

    drivers.alt_driver.add_notification_listener(NotificationType.LOG, log_callback)


def add_unity_logs_to_allure(unity_logs: dict) -> None:
    """Add Unity logs to Allure report"""
    logs_copy = dict(unity_logs)

    for filename, filepath in logs_copy.items():
        try:
            attachment_name = filename  # Already includes test name
            Reporter.attach_file_to_allure(filepath, attachment_name)
        except Exception:
            Reporter.log("No Unity logs found.")

        unity_logs.pop(filename, None)

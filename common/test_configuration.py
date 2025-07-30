import os
from enum import Enum
from typing import Optional


class PlatformType(Enum):
    """Supported platforms for test execution"""

    ANDROID = "Android"
    IOS = "iOS"
    WEBGL = "WebGL"


class TestConfiguration:
    """
    Centralized configuration for test execution
    Handles environment variables and provides default values for test settings
    """

    # AltTester Configuration
    ALT_TESTER_SERVER_URL = os.getenv("ALT_TESTER_SERVER_URL", "127.0.0.1")
    ALT_TESTER_SERVER_PORT = int(os.getenv("ALT_TESTER_SERVER_PORT", "13000"))
    ALT_TESTER_APP_NAME = os.getenv("ALT_TESTER_APP_NAME", "__default__")
    ALT_TESTER_CONNECT_TIMEOUT = int(os.getenv("ALT_TESTER_CONNECT_TIMEOUT", "60"))

    # Platform Configuration
    PLATFORM = PlatformType(os.getenv("TEST_PLATFORM", "Android"))
    DEVICE_NAME = os.getenv("DEVICE_NAME", "android")
    APP_BUNDLE_ID = os.getenv("APP_BUNDLE_ID", "com.example.app")

    # Driver Configuration
    RUNNING_WITH_APPIUM = os.getenv("RUN_TESTS_WITH_APPIUM", "false").lower() == "true"
    RUNNING_WITH_SELENIUM = (
        os.getenv("RUN_TESTS_WITH_SELENIUM", "false").lower() == "true"
    )

    # WebGL Configuration
    WEBGL_URL = os.getenv("WEBGL_URL", "https://example.com/game")

    @staticmethod
    def get_environment_variable_or_default(
        variable_name: str, default_value: str
    ) -> str:
        """
        Gets an environment variable value or returns a default value if not set

        Args:
            variable_name: Name of the environment variable
            default_value: Default value to return if variable is not set

        Returns:
            Environment variable value or default value
        """
        value = os.getenv(variable_name, "")
        return default_value if not value else value

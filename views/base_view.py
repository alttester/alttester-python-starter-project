import time
from typing import Tuple
import allure
from alttester import AltDriver, By
from common.driver_container import DriverContainer
from common.reporter import Reporter


class BaseView:
    """Base view class with common functionality for all page objects"""

    def __init__(self, drivers: DriverContainer):
        self.drivers = drivers

    @property
    def alt_driver(self) -> AltDriver:
        """Get the AltDriver instance"""
        return self.drivers.alt_driver

    @property
    def appium_driver(self):
        """Get the Appium driver instance"""
        return self.drivers.appium_driver

    @property
    def selenium_driver(self):
        """Get the Selenium driver instance"""
        return self.drivers.selenium_driver

    @allure.step("Click on object")
    def click_object(
        self,
        locator: Tuple[By, str],
        timeout: float = 10.0,
        wait_for_click: bool = True,
    ) -> None:
        """
        Click on an object using AltDriver

        Args:
            locator: Tuple of (By, value) for locating the object
            timeout: Timeout in seconds
            wait_for_click: Whether to wait for the click to complete
        """
        alt_object = self.wait_for_object(locator, timeout)
        alt_object.click(wait=wait_for_click)
        time.sleep(0.5)  # Brief pause after click

    @allure.step("Tap on object")
    def tap_object(
        self, locator: Tuple[By, str], count: int = 1, timeout: float = 10.0
    ) -> None:
        """
        Tap on an object using AltDriver

        Args:
            locator: Tuple of (By, value) for locating the object
            count: Number of taps
            timeout: Timeout in seconds
        """
        alt_object = self.wait_for_object(locator, timeout)
        alt_object.tap(count)
        time.sleep(0.5)  # Brief pause after tap

    @allure.step("Wait for object")
    def wait_for_object(
        self, locator: Tuple[By, str], timeout: float = 20.0, interval: float = 0.5
    ):
        """
        Wait for an object to be present

        Args:
            locator: Tuple of (By, value) for locating the object
            timeout: Timeout in seconds
            interval: Polling interval in seconds

        Returns:
            AltObject instance
        """
        Reporter.log(f"Waiting for element {locator[1]} to be present.")
        try:
            return self.alt_driver.wait_for_object(
                locator[0], locator[1], timeout=timeout, interval=interval
            )
        except Exception:
            Reporter.log(
                f"Element {locator[1]} was not found within {timeout} seconds",
                with_screenshot=True,
            )
            raise AssertionError(
                f"Element '{locator[1]}' was not found within {timeout} seconds. "
                f"Please check if the element exists or if the game loaded correctly."
            )

    @allure.step("Wait for object which contains")
    def wait_for_object_which_contains(
        self, locator: Tuple[By, str], timeout: float = 20.0
    ):
        """
        Wait for an object which contains the specified text

        Args:
            locator: Tuple of (By, value) for locating the object
            timeout: Timeout in seconds

        Returns:
            AltObject instance
        """
        return self.alt_driver.wait_for_object_which_contains(
            locator[0], locator[1], timeout=timeout
        )

    @allure.step("Wait for object not to be present")
    def wait_for_object_not_be_present(
        self, locator: Tuple[By, str], timeout: float = 20.0
    ) -> None:
        """
        Wait for an object to not be present

        Args:
            locator: Tuple of (By, value) for locating the object
            timeout: Timeout in seconds
        """
        self.alt_driver.wait_for_object_not_be_present(
            locator[0], locator[1], timeout=timeout
        )

    @allure.step("Set text on object")
    def set_text(
        self, locator: Tuple[By, str], text: str, timeout: float = 10.0
    ) -> None:
        """
        Set text on an object

        Args:
            locator: Tuple of (By, value) for locating the object
            text: Text to set
            timeout: Timeout in seconds
        """
        alt_object = self.wait_for_object(locator, timeout)
        alt_object.set_text(text)

    @allure.step("Get text from object")
    def get_text(self, locator: Tuple[By, str], timeout: float = 10.0) -> str:
        """
        Get text from an object

        Args:
            locator: Tuple of (By, value) for locating the object
            timeout: Timeout in seconds

        Returns:
            Text content of the object
        """
        alt_object = self.wait_for_object(locator, timeout)
        return alt_object.get_text()

    @allure.step("Check if object is present")
    def is_object_present(self, locator: Tuple[By, str]) -> bool:
        """
        Check if an object is present

        Args:
            locator: Tuple of (By, value) for locating the object

        Returns:
            True if object is present, False otherwise
        """
        try:
            self.alt_driver.find_object(locator[0], locator[1])
            return True
        except Exception:
            return False

    @allure.step("Find element by locator")
    def find_element(self, locator: Tuple[By, str]):
        """
        Find an element by locator

        Args:
            locator: Tuple of (By, value) for locating the object

        Returns:
            AltObject instance

        Raises:
            AssertionError: If element is not found
        """
        try:
            return self.alt_driver.find_object(locator[0], locator[1])
        except Exception:
            Reporter.log(f"Element {locator[1]} not found", with_screenshot=True)
            raise AssertionError(
                f"Element '{locator[1]}' was not found. "
                f"Please verify the element exists in the current scene."
            )

    @allure.step("Get current scene")
    def get_current_scene(self) -> str:
        """
        Get the current scene name

        Returns:
            Current scene name
        """
        return self.alt_driver.get_current_scene()

    @allure.step("Load scene")
    def load_scene(self, scene_name: str) -> None:
        """
        Load a scene by name

        Args:
            scene_name: Name of the scene to load
        """
        self.alt_driver.load_scene(scene_name)

    @allure.step("Take screenshot")
    def take_screenshot(self, path: str) -> None:
        """
        Take a screenshot

        Args:
            path: Path where to save the screenshot
        """
        self.alt_driver.get_png_screenshot(path)

    @allure.step("Wait for a specified duration")
    def wait(self, seconds: float) -> None:
        """
        Wait for a specified duration

        Args:
            seconds: Number of seconds to wait
        """
        time.sleep(seconds)

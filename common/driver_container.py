from typing import Optional
from alttester import AltDriver
from selenium import webdriver
from appium import webdriver as appium_webdriver


class DriverContainer:
    """Container for managing different types of drivers used in tests"""

    def __init__(
        self,
        alt_driver: AltDriver,
        appium_driver: Optional[appium_webdriver.Remote] = None,
        selenium_driver: Optional[webdriver.Remote] = None,
    ):
        self.alt_driver = alt_driver
        self.appium_driver = appium_driver
        self.selenium_driver = selenium_driver

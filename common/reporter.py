import os
import time
from datetime import datetime
from typing import Optional
import allure


class Reporter:
    """Static class for logging and reporting utilities"""

    alt_driver = None

    @staticmethod
    def log(message: str, with_screenshot: bool = False) -> None:
        """
        Log a message with timestamp and optional screenshot

        Args:
            message: The message to log
            with_screenshot: Whether to take a screenshot
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        print(formatted_message)

        with allure.step(formatted_message):
            if with_screenshot:
                Reporter.take_screenshot()

    @staticmethod
    def take_screenshot(custom_name: Optional[str] = None) -> None:
        """
        Take a screenshot using the AltDriver

        Args:
            custom_name: Optional custom name for the screenshot
        """
        if Reporter.alt_driver is None:
            Reporter.log(
                "Cannot take screenshot: AltDriver not set", with_screenshot=False
            )
            return

        try:
            project_directory = os.getcwd()
            screenshot_directory = os.path.join(
                project_directory, "screenshots-and-logs"
            )

            # Create directory if it doesn't exist
            if not os.path.exists(screenshot_directory):
                os.makedirs(screenshot_directory)

            timestamp = int(time.time())
            filename = custom_name or f"screenshot_{timestamp}"
            screenshot_path = os.path.join(screenshot_directory, f"{filename}.png")

            Reporter.alt_driver.get_png_screenshot(screenshot_path)

            # Attach to Allure report
            with allure.step(f"Screenshot taken: {filename}"):
                with open(screenshot_path, "rb") as screenshot_file:
                    allure.attach(
                        screenshot_file.read(),
                        name=filename,
                        attachment_type=allure.attachment_type.PNG,
                    )

        except Exception as ex:
            Reporter.log(f"Failed to take screenshot: {ex}", with_screenshot=False)

    @staticmethod
    def attach_file_to_allure(
        file_path: str, custom_name: Optional[str] = None
    ) -> None:
        """
        Attach a file to the Allure report

        Args:
            file_path: Path to the file to attach
            custom_name: Optional custom name for the attachment
        """
        filename = custom_name or os.path.splitext(os.path.basename(file_path))[0]

        with allure.step(f"Attach file: {filename}"):
            try:
                if not os.path.exists(file_path):
                    Reporter.log(
                        f"Cannot attach file: File not found at {file_path}",
                        with_screenshot=False,
                    )
                    return

                file_extension = os.path.splitext(file_path)[1].lower()

                # Determine content type based on file extension
                content_type_map = {
                    ".txt": allure.attachment_type.TEXT,
                    ".log": allure.attachment_type.TEXT,
                    ".json": allure.attachment_type.JSON,
                    ".xml": allure.attachment_type.XML,
                    ".html": allure.attachment_type.HTML,
                    ".csv": allure.attachment_type.CSV,
                }

                attachment_type = content_type_map.get(
                    file_extension, allure.attachment_type.TEXT
                )

                with open(file_path, "rb") as file:
                    allure.attach(
                        file.read(), name=filename, attachment_type=attachment_type
                    )

                Reporter.log(
                    f"File attached to Allure report: {filename}", with_screenshot=False
                )

            except Exception as ex:
                Reporter.log(
                    f"Failed to attach file to Allure: {ex}", with_screenshot=False
                )

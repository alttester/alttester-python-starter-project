import pytest
import allure
from common.reporter import Reporter
from tests.base_test import BaseTest


@allure.suite("Main Menu Tests")
class TestMainMenu(BaseTest):
    """Test suite for main menu functionality"""

    @allure.feature("Main Menu")
    @allure.story("Menu Loading")
    @pytest.mark.smoke
    def test_main_menu_loads_successfully(self):
        """Test that the main menu loads successfully"""
        # This test should always pass, since there should always be a scene loaded

        Reporter.log("Testing main menu loads successfully", with_screenshot=True)
        current_scene = self.drivers.alt_driver.get_current_scene()
        assert (
            current_scene
        ), "Game did not launch successfully, expected to have a scene loaded."

    @allure.feature("Main Menu")
    @allure.story("Game Start")
    @pytest.mark.ui
    def test_can_start_new_game(self):
        """Test that a new game can be started from the main menu"""
        # This test will should fail because it's expecting an element you probably don't have in your scene

        self.main_menu_view.wait_for_main_menu_ready(timeout_seconds=2)
        self.main_menu_view.start_new_game(player_name="TestPlayer")

        self.gameplay_view.wait_for_gameplay_ready(timeout_seconds=2)
        assert (
            self.gameplay_view.is_main_character_present()
        ), "Main character should be present after starting a new game"

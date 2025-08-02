from typing import Tuple
import allure
from alttester import By
from common.driver_container import DriverContainer
from common.reporter import Reporter
from views.base_view import BaseView


class MainMenuView(BaseView):
    """Main menu view class for interacting with the main menu screen"""

    def __init__(self, drivers: DriverContainer):
        super().__init__(drivers)

        # Locators
        self.play_button_locator = (By.NAME, "PlayButton")
        self.main_menu_panel_locator = (By.NAME, "MainMenuPanel")
        self.player_name_input_locator = (By.NAME, "PlayerNameInput")
        self.settings_button_locator = (By.NAME, "SettingsButton")

    @allure.step("Click play button")
    def click_play_button(self) -> None:
        play_button = self.find_object(self.play_button_locator)
        play_button.click()
        Reporter.log("Clicked play button")

    @allure.step("Check if main menu is visible")
    def is_main_menu_visible(self) -> bool:
        try:
            main_menu_panel = self.find_object(self.main_menu_panel_locator)
            is_visible = main_menu_panel.enabled
            Reporter.log(f"Main menu panel visible: {is_visible}")
            return is_visible
        except Exception:
            Reporter.log("Main menu panel not found")
            return False

    @allure.step("Enter player name")
    def enter_player_name(self, player_name: str) -> None:
        input_field = self.find_object(self.player_name_input_locator)
        input_field.set_text(player_name, submit=True)
        Reporter.log(f"Entered player name: {player_name}")

    @allure.step("Navigate to settings")
    def navigate_to_settings(self) -> None:
        settings_button = self.find_object(self.settings_button_locator)
        settings_button.click()
        Reporter.log("Navigated to settings")

    @allure.step("Wait for main menu to be ready")
    def wait_for_main_menu_ready(self, timeout_seconds: float = 10.0) -> None:
        self.wait_for_object(self.main_menu_panel_locator, timeout_seconds)
        Reporter.log("Main menu is ready")

    @allure.step("Start new game")
    def start_new_game(self, player_name: str) -> None:
        self.wait_for_main_menu_ready()

        if not self.is_main_menu_visible():
            raise Exception("Main menu is not visible, cannot start new game")

        self.enter_player_name(player_name)
        self.click_play_button()

        Reporter.log(f"Started new game for player: {player_name}")

    # TODO: Add your own main menu-specific methods here
    # Examples:
    # - navigate_to_level_select()
    # - show_leaderboard()
    # - navigate_to_store()
    # - show_achievements()
    # - select_game_mode(mode: str)
    # etc.

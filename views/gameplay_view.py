from typing import Tuple
import allure
from alttester import By
from views.base_view import BaseView
from common.driver_container import DriverContainer
from common.reporter import Reporter


class GameplayView(BaseView):
    """Gameplay view class for handling gameplay interactions"""

    def __init__(self, driver_container: DriverContainer):
        super().__init__(driver_container)

        # Locators
        self.pause_button_locator = (By.NAME, "PauseButton")
        self.resume_button_locator = (By.NAME, "ResumeButton")
        self.main_character_locator = (By.NAME, "MainCharacter")
        self.game_hud_locator = (By.NAME, "GameHUD")

    @allure.step("Pause the game")
    def pause_game(self) -> None:
        pause_button = self.find_object(self.pause_button_locator)
        pause_button.click()
        Reporter.log("Game paused")

    @allure.step("Resume the game")
    def resume_game(self) -> None:
        resume_button = self.find_object(self.resume_button_locator)
        resume_button.click()
        Reporter.log("Game resumed")

    @allure.step("Check if game is paused")
    def is_game_paused(self) -> bool:
        try:
            resume_button = self.find_object(self.resume_button_locator)
            is_visible = resume_button.enabled
            Reporter.log(f"Game paused: {is_visible}")
            return is_visible
        except Exception:
            Reporter.log("Resume button not found - game is not paused")
            return False

    @allure.step("Check if main character is present")
    def is_main_character_present(self) -> bool:
        try:
            main_character = self.find_object(self.main_character_locator)
            is_present = main_character.enabled
            Reporter.log(f"Main character present: {is_present}")
            return is_present
        except Exception:
            Reporter.log("Main character not found")
            return False

    @allure.step("Get main character position")
    def get_main_character_position(self) -> Tuple[float, float, float]:
        main_character = self.find_object(self.main_character_locator)
        position = main_character.get_world_position()
        Reporter.log(
            f"Main character position: {position.x}, {position.y}, {position.z}"
        )
        return (position.x, position.y, position.z)

    @allure.step("Wait for gameplay to be ready")
    def wait_for_gameplay_ready(self, timeout_seconds: int = 10) -> None:
        self.wait_for_object(self.game_hud_locator, timeout_seconds)
        Reporter.log("Gameplay is ready")

    @allure.step("Check if gameplay HUD is visible")
    def is_gameplay_hud_visible(self) -> bool:
        try:
            game_hud = self.find_object(self.game_hud_locator)
            is_visible = game_hud.enabled
            Reporter.log(f"Gameplay HUD visible: {is_visible}")
            return is_visible
        except Exception:
            Reporter.log("Gameplay HUD not found")
            return False

    # TODO: Add your own gameplay-specific methods here
    # Examples:
    # - move_character(direction: str)
    # - use_ability(ability_name: str)
    # - collect_item(item_name: str)
    # - check_health() -> int
    # - get_score() -> int
    # etc.

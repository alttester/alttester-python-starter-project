# Coding Standards and Preferences

This document outlines the coding standards and preferences for the AltTester Unity/Unreal Engine test automation framework using Python and pytest. These guidelines should be followed to maintain consistency, readability, and reliability across the codebase.

## 1. Test Setup - Inherit from BaseTest and Use Pre-Initialized Views

### ✅ Preferred Approach
```python
@allure.suite("Game Feature Tests")
class TestGameFeature(BaseTest):
    """Test suite with auto-initialized view instances via fixtures"""

    @allure.feature("Game Start")
    def test_game_feature(self):
        """Test game feature using pre-initialized views"""
        # Use the pre-initialized view objects directly from BaseTest (via fixtures)
        self.main_menu_view.wait_for_main_menu_ready()
        self.main_menu_view.start_new_game("TestPlayer")
        
        self.gameplay_view.wait_for_gameplay_ready()
        assert self.gameplay_view.is_main_character_present(), \
            "Main character should be present after starting a new game"

    @allure.feature("Game Navigation")
    def test_another_feature(self):
        """Test another feature using auto-initialized views"""
        # All view instances are automatically available
        self.main_menu_view.navigate_to_settings()
        # Test implementation...
```

### ❌ Avoid
```python
class TestGameFeature(BaseTest):
    """Bad example - manual view initialization"""
    
    def setup_method(self, method):
        """Don't manually initialize view objects - they're already available from fixtures"""
        super().setup_method(method)
        # Don't do this - views are auto-initialized via fixtures
        self.main_menu_view = MainMenuView(self.drivers)
        self.gameplay_view = GameplayView(self.drivers)

    def test_game_feature(self):
        """Using local instances instead of fixture-provided properties"""
        # Using manually initialized instances instead of fixture properties
        self.main_menu_view.start_new_game("TestPlayer")

# Also avoid: Direct driver usage without view abstraction
class BadGameFeatureTests:
    def setup_class(self):
        """Duplicating driver setup logic from fixtures"""
        # Don't duplicate fixture logic
        self.alt_driver = AltDriver("127.0.0.1", 13000, "MyGame")
    
    def test_game_feature(self):
        """Direct driver usage without view abstraction"""
        # Direct driver usage without view abstraction
        button = self.alt_driver.find_object(By.NAME, "PlayButton")
        button.click()
```

**Guidelines:**
- Always inherit from `BaseTest` for consistent driver and view setup
- Use the pre-initialized view properties directly: `self.main_menu_view`, `self.gameplay_view`
- No need for `setup_method()` to initialize views - they're automatically available via fixtures
- BaseTest + fixtures handle all driver setup, teardown, and view initialization
- Leverage the automatic screenshot and logging functionality from BaseView and Reporter

## 2. Method Reuse - Leverage Existing BaseView Methods

### ✅ Preferred Approach
```python
# Use existing methods from BaseView class
self.click_object(self.play_button_locator)
game_object = self.wait_for_object(self.main_character_locator, timeout=5.0)
is_present = self.is_object_present(self.health_bar_locator)
self.set_text(self.player_name_input_locator, "TestPlayer")
health_text = self.get_text(self.health_display_locator)
```

### ❌ Avoid
```python
# Creating new methods when BaseView methods exist
def custom_click_method(self, locator):
    alt_object = self.alt_driver.find_object(locator[0], locator[1])
    alt_object.click()

def custom_wait_method(self, locator):
    # Reimplementing wait logic that already exists in BaseView
    pass
```

**Guidelines:**
- Always check `BaseView` class for existing functionality
- Only create new methods when BaseView methods don't meet specific requirements
- Extend BaseView functionality rather than reimplementing
- Use the standardized locator tuple format: `(By, string)`

## 3. Locators - Use Tuple Format with AltTester By Strategies

### ✅ Preferred Approach
```python
from alttester import By

class MainMenuView(BaseView):
    """Main menu view with properly defined locators"""
    
    def __init__(self, drivers: DriverContainer):
        super().__init__(drivers)
        
        # Define locators as tuples of (By, string)
        self.play_button_locator = (By.NAME, "PlayButton")
        self.settings_button_locator = (By.NAME, "SettingsButton")
        self.main_character_locator = (By.PATH, "//Player/Character")
        self.health_text_locator = (By.COMPONENT, "Text")
        self.ui_canvas_locator = (By.TAG, "UI")
        self.score_display_locator = (By.ID, "123")

    # Usage in methods
    @allure.step("Click play button")
    def click_play_button(self):
        self.click_object(self.play_button_locator)
    
    @allure.step("Check if main menu is visible")
    def is_main_menu_visible(self):
        return self.is_object_present(self.main_menu_panel_locator)
```

### ❌ Avoid
```python
# String locators that require By specification every time
class MainMenuView(BaseView):
    def __init__(self, drivers: DriverContainer):
        super().__init__(drivers)
        
        # Don't do this - string locators without By
        self.play_button_name = "PlayButton"
        self.settings_button_path = "//Canvas/MainMenu/SettingsButton"

    # Usage requiring By specification in every call
    def click_play_button(self):
        play_button = self.alt_driver.find_object(By.NAME, self.play_button_name)
        play_button.click()

# Hardcoded locators in test methods
def test_game_start(self):
    self.click_object((By.NAME, "PlayButton"))  # Should be defined as constant
```

**AltTester Locator Strategies:**
- `By.NAME` - Find by GameObject/Actor name
- `By.PATH` - Find by GameObject/Actor path (most reliable)
- `By.ID` - Find by GameObject/Actor instance ID
- `By.TAG` - Find by GameObject/Actor tag
- `By.LAYER` - Find by GameObject/Actor layer
- `By.COMPONENT` - Find by attached component type
- `By.TEXT` - Find by text content (for UI text elements)

**Guidelines:**
- Always define locators as tuples: `(By.STRATEGY, "selector")`
- Use descriptive names that indicate the element's purpose
- Group related locators together in the view class
- Prefer `By.PATH` for complex hierarchies and `By.NAME` for unique objects
- Use `By.COMPONENT` when you need to find objects by their component type

## 4. Waits - Use BaseView Wait Methods, Avoid time.sleep

### ✅ Preferred Approach
```python
# Use BaseView wait methods with built-in timeout handling
game_object = self.wait_for_object(self.main_character_locator, timeout=10.0)
menu_panel = self.wait_for_object_which_contains((By.NAME, "Menu"), timeout=5.0)
self.wait_for_object_not_be_present(self.loading_screen_locator, timeout=30.0)

# Check object presence without throwing exceptions
if self.is_object_present(self.optional_button_locator):
    self.click_object(self.optional_button_locator)

# Use the wait method for intentional delays (sparingly)
self.wait(0.5)  # Brief pause for UI animations
```

### ❌ Avoid
```python
# Direct AltDriver wait methods without error handling
game_object = self.alt_driver.wait_for_object(By.NAME, "Character", timeout=10.0)

# time.sleep for waiting on game state
import time
time.sleep(5)  # Avoid fixed delays

# Polling loops
found = False
attempts = 0
while not found and attempts < 10:
    try:
        self.alt_driver.find_object(By.NAME, "Character")
        found = True
    except:
        time.sleep(1)
        attempts += 1
```

**Guidelines:**
- Use `wait_for_object()` methods from BaseView for reliable object waiting
- Use `is_object_present()` for conditional logic that doesn't need exceptions
- Only use `wait()` method for brief UI synchronization (< 1 second)
- Avoid `time.sleep()` except for very short UI animation waits
- Trust the timeout mechanisms in BaseView methods

## 5. Element Interaction - Use BaseView Wrapper Methods

### ✅ Preferred Approach
```python
# Use BaseView wrapper methods with tuple locators
self.click_object(self.play_button_locator)
self.tap_object(self.menu_button_locator, count=2)
self.set_text(self.player_name_input_locator, "TestPlayer")
health_value = self.get_text(self.health_display_locator)
current_scene = self.get_current_scene()

# Use proper locator definitions
play_button_locator = (By.NAME, "PlayButton")
health_bar_locator = (By.PATH, "//Canvas/HealthPanel/HealthBar")
score_text_locator = (By.COMPONENT, "Text")
```

### ❌ Avoid
```python
# Direct AltDriver methods
play_button = self.alt_driver.find_object(By.NAME, "PlayButton")
play_button.click()

# String-based locators
play_button_name = "PlayButton"
play_button = self.alt_driver.find_object(By.NAME, play_button_name)

# Hardcoded locator values in test methods
button = self.alt_driver.find_object(By.NAME, "PlayButton")
```

**Available BaseView Methods:**
- `click_object(locator: Tuple[By, str], timeout: float = 10.0, wait_for_click: bool = True)`
- `tap_object(locator: Tuple[By, str], count: int = 1, timeout: float = 10.0)`
- `wait_for_object(locator: Tuple[By, str], timeout: float = 20.0, interval: float = 0.5)`
- `set_text(locator: Tuple[By, str], text: str, timeout: float = 10.0)`
- `get_text(locator: Tuple[By, str], timeout: float = 10.0)`
- `is_object_present(locator: Tuple[By, str])`
- `find_object(locator: Tuple[By, str])`

**Benefits:**
- Consistent error handling with meaningful exception messages
- Built-in timeout handling and retries
- Automatic screenshot capture on failures
- Standardized logging with Allure integration

## 6. Page Object Model (POM) Architecture - Create View Classes for Each Game Screen

### ✅ Preferred Approach
```python
# Create separate view classes for each distinct game screen or UI panel
class InventoryView(BaseView):
    """View class for inventory management functionality"""
    
    def __init__(self, drivers: DriverContainer):
        super().__init__(drivers)
        
        self.inventory_panel_locator = (By.NAME, "InventoryPanel")
        self.item_slot_locator = (By.COMPONENT, "InventorySlot")
        self.close_button_locator = (By.PATH, "//InventoryPanel/CloseButton")

    @allure.step("Open inventory panel")
    def open_inventory(self):
        """Implementation specific to inventory functionality"""
        pass

    @allure.step("Get item count in inventory")
    def get_item_count(self):
        """Inventory-specific logic"""
        items = self.alt_driver.find_objects(self.item_slot_locator[0], self.item_slot_locator[1])
        return len(items)

class SettingsView(BaseView):
    """View class for settings management functionality"""
    
    def __init__(self, drivers: DriverContainer):
        super().__init__(drivers)
        
        self.settings_panel_locator = (By.NAME, "SettingsPanel")
        self.volume_slider_locator = (By.NAME, "VolumeSlider")
        self.apply_button_locator = (By.NAME, "ApplyButton")

    @allure.step("Adjust volume setting")
    def set_volume(self, volume: float):
        """Settings-specific functionality"""
        pass

# Don't forget to add new views to conftest.py for automatic initialization
@pytest.fixture(scope="class", autouse=True)
def setup_views(request, setup_drivers):
    """Auto-used fixture to initialize all view instances as class properties"""
    drivers = setup_drivers
    
    if drivers:
        request.cls.main_menu_view = MainMenuView(drivers)
        request.cls.gameplay_view = GameplayView(drivers)
        request.cls.inventory_view = InventoryView(drivers)  # Add new view
        request.cls.settings_view = SettingsView(drivers)    # Add new view
    
    yield
```

### ❌ Avoid
```python
# Putting all functionality in one massive view class
class GameView(BaseView):
    """Bad example - mixing responsibilities"""
    
    def __init__(self, drivers: DriverContainer):
        super().__init__(drivers)
        
        # Main menu locators
        self.play_button_locator = (By.NAME, "PlayButton")
        
        # Inventory locators  
        self.inventory_panel_locator = (By.NAME, "InventoryPanel")
        
        # Settings locators
        self.settings_panel_locator = (By.NAME, "SettingsPanel")
        
        # Gameplay locators
        self.main_character_locator = (By.NAME, "MainCharacter")

    # Mixed responsibilities - violates single responsibility principle
    def start_new_game(self):  # Main menu functionality
        pass
    def open_inventory(self):  # Inventory functionality 
        pass
    def change_settings(self):  # Settings functionality
        pass
    def move_character(self):  # Gameplay functionality
        pass

# Using test methods without proper view abstraction
def test_inventory_feature(self):
    """Bad example - direct driver usage instead of view methods"""
    # Direct driver usage instead of view methods
    inventory_button = self.drivers.alt_driver.find_object(By.NAME, "InventoryButton")
    inventory_button.click()
    
    items = self.drivers.alt_driver.find_objects(By.COMPONENT, "InventorySlot")
    assert len(items) > 0
```

**POM Principles for View Creation:**

1. **Single Responsibility**: Each view class should represent one distinct game screen, UI panel, or functional area
2. **Encapsulation**: All locators and interactions for a specific screen should be contained within its view class
3. **Abstraction**: View methods should provide meaningful, high-level actions rather than exposing low-level driver operations
4. **Reusability**: View methods should be designed to be reusable across multiple test scenarios
5. **Maintainability**: Changes to a specific game screen should only require updates to its corresponding view class

**When to Create New View Classes:**
- **New Game Screens**: Main menu, gameplay, pause menu, game over screen
- **UI Panels**: Inventory, settings, character selection, shop/store
- **Dialog/Modal Windows**: Confirmation dialogs, error messages, tutorials
- **HUD Elements**: If complex enough, create separate views for different HUD sections
- **Mini-Games**: Separate views for distinct mini-game interfaces within the main game

**Naming Conventions:**
- Use descriptive names that clearly indicate the game screen: `MainMenuView`, `InventoryView`, `SettingsView`
- End all view class names with "View" for consistency
- Use the same name as the Unity scene, Unreal level, or main GameObject/Actor when possible

**Integration with Fixtures:**
- Always add new view properties to the `setup_views` fixture for automatic initialization
- Update the fixture to instantiate new view classes
- This ensures all views are available immediately in test classes without manual setup

## 7. Test Structure - Use pytest Parameterized Tests

### ✅ Preferred Approach
```python
@pytest.mark.parametrize("object_type,position_type", [
    ("Character", "StartPosition"),
    ("Enemy", "SpawnPoint"),
    ("Collectible", "RandomPosition")
], ids=["TestCharacterAtStartPosition", "TestEnemyAtSpawnPoint", "TestCollectibleAtRandomPosition"])
def test_game_objects_at_positions(self, object_type, position_type):
    """Single test method that handles multiple object types"""
    game_object = self.gameplay_view.find_game_object(object_type)
    expected_position = self.gameplay_view.get_position(position_type)
    
    actual_position = game_object.get_world_position()
    assert abs(actual_position.x - expected_position.x) < 0.1, \
        f"{object_type} should be at {position_type}"

# Alternative using complex test data
game_object_test_cases = [
    ("Player", {"health": 100, "level": 1}),
    ("Boss", {"health": 500, "level": 10}),
    ("NPC", {"health": 50, "level": 5})
]

@pytest.mark.parametrize("object_name,expected_properties", game_object_test_cases)
def test_game_object_properties(self, object_name, expected_properties):
    """Test implementation using dictionary properties"""
    # Test implementation using dictionary properties
    pass
```

### ❌ Avoid
```python
def test_character_at_start_position(self):
    """Separate method for each object type"""
    pass

def test_enemy_at_spawn_point(self):
    """Separate method for each object type"""
    pass

def test_collectible_at_random_position(self):
    """Separate method for each object type"""
    pass
```

**Benefits:**
- Reduces code duplication
- Easier maintenance
- Consistent test structure
- Better coverage visibility with descriptive test names

## 8. Additional Best Practices

### View Organization and Architecture
- Keep each view class focused on a single game screen or UI panel
- Use descriptive class names that match the Unity scene, Unreal level, or UI panel: `MainMenuView`, `GameplayView`, `InventoryView`
- Group related methods together within view classes
- Inherit from `BaseView` to get standard interaction methods

### Method Design
- Use descriptive method names that indicate the action being performed: `start_new_game()`, `navigate_to_settings()`, `wait_for_gameplay_ready()`
- Keep methods focused on single responsibilities
- Use `@allure.step()` decorators for better test reporting
- Return meaningful values when methods need to provide information

### Error Handling and Assertions
- Use pytest assertions with descriptive failure messages
- Leverage BaseView exception handling for consistent error reporting
- Provide context in assertion messages to help with debugging

### Test Organization
- Use `@allure.suite()` and `@allure.feature()` decorators for better organization
- Group related tests in the same test class
- Use meaningful test method names that describe the expected behavior
- Inherit from `BaseTest` to get automatic fixture-based setup

### Logging and Reporting
- Use `Reporter.log()` for important test steps and debugging information
- Add `with_screenshot=True` parameter when logging errors or important states
- Use `@allure.step()` decorators consistently across view methods

### Code Documentation
- Prefer good variable and method names over extensive comments
- Document complex game interactions or timing-sensitive operations

### Example: Complete Implementation Following Standards

```python
from typing import Tuple
import allure
import pytest
from alttester import By
from common.driver_container import DriverContainer
from common.reporter import Reporter
from views.base_view import BaseView

class InventoryView(BaseView):
    """View class for inventory management functionality"""
    
    def __init__(self, drivers: DriverContainer):
        super().__init__(drivers)
        
        # Locator definitions using tuple format
        self.inventory_panel_locator = (By.NAME, "InventoryPanel")
        self.close_button_locator = (By.PATH, "//InventoryPanel/CloseButton")
        self.item_slot_locator = (By.COMPONENT, "InventorySlot")

    @allure.step("Wait for inventory to be ready")
    def wait_for_inventory_ready(self, timeout_seconds: int = 10):
        """Wait for inventory panel to be ready for interaction"""
        self.wait_for_object(self.inventory_panel_locator, timeout_seconds)
        Reporter.log("Inventory panel is ready for interaction")

    @allure.step("Close inventory panel")
    def close_inventory(self):
        """Close the inventory panel"""
        if not self.is_object_present(self.inventory_panel_locator):
            Reporter.log("Inventory panel is not currently open")
            return

        self.click_object(self.close_button_locator)
        self.wait_for_object_not_be_present(self.inventory_panel_locator, timeout=5.0)
        Reporter.log("Inventory panel closed successfully")

    @allure.step("Get inventory item count")
    def get_inventory_item_count(self) -> int:
        """Get the number of items in inventory"""
        try:
            item_slots = self.alt_driver.find_objects(self.item_slot_locator[0], self.item_slot_locator[1])
            item_count = len([slot for slot in item_slots if slot.get_text()])
            Reporter.log(f"Found {item_count} items in inventory")
            return item_count
        except Exception as ex:
            Reporter.log(f"Error getting inventory item count: {ex}", with_screenshot=True)
            return 0

@allure.suite("Inventory Management Tests")
class TestInventory(BaseTest):
    """Test suite for inventory functionality using auto-initialized views"""
    
    @pytest.mark.parametrize("item_type,expected_count", [
        ("Sword", 1),
        ("Shield", 1), 
        ("Potion", 3)
    ], ids=["TestCollectSword", "TestCollectShield", "TestCollectMultiplePotions"])
    def test_collect_items(self, item_type, expected_count):
        """Test collecting different types of items"""
        # Setup: Start game and navigate to gameplay using pre-initialized views
        self.main_menu_view.wait_for_main_menu_ready()
        self.main_menu_view.start_new_game("TestPlayer")
        self.gameplay_view.wait_for_gameplay_ready()

        # Action: Collect the specified items
        for i in range(expected_count):
            self.gameplay_view.collect_item(item_type)

        # Verification: Check inventory contains expected items
        self.gameplay_view.open_inventory()
        # Note: If you had an InventoryView, it would also be pre-initialized via fixtures
        
        item_count = self.gameplay_view.get_inventory_item_count()  # Assuming this method exists
        assert item_count >= expected_count, \
            f"Should have collected at least {expected_count} {item_type}(s)"
```

Always refer to this document when writing new tests or refactoring existing code to maintain high code quality standards specific to Unity/Unreal Engine game testing with AltTester.
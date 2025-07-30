from abc import ABC


class BaseTest(ABC):
    """
    Base test class that handles driver setup, teardown, and common test infrastructure
    All test classes should inherit from this class to get consistent test behavior
    """

    def setup_method(self, method):
        """Set up before each test method"""
        # Add test-specific setup here if needed
        pass

    def teardown_method(self, method):
        """Clean up after each test method"""
        # Add test-specific cleanup here if needed
        pass

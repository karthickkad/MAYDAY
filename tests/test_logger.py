import unittest

from core.logger import Logger


class TestLogger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize logger once before all tests."""
        Logger.setup()

    def test_info(self):
        """Logger.info() should execute without exception."""
        try:
            Logger.info("Unit test - INFO")
        except Exception as error:
            self.fail(f"Logger.info() raised {error}")

    def test_warning(self):
        """Logger.warning() should execute without exception."""
        try:
            Logger.warning("Unit test - WARNING")
        except Exception as error:
            self.fail(f"Logger.warning() raised {error}")

    def test_error(self):
        """Logger.error() should execute without exception."""
        try:
            Logger.error("Unit test - ERROR")
        except Exception as error:
            self.fail(f"Logger.error() raised {error}")

    def test_debug(self):
        """Logger.debug() should execute without exception."""
        try:
            Logger.debug("Unit test - DEBUG")
        except Exception as error:
            self.fail(f"Logger.debug() raised {error}")


if __name__ == "__main__":
    unittest.main()
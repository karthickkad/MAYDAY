import unittest

from core.config import Config


class TestConfig(unittest.TestCase):

    def setUp(self):
        """Create a Config object before each test."""
        self.config = Config()

    def test_load_config(self):
        """Configuration should be loaded."""
        self.assertIsNotNone(self.config.settings)

    def test_get_assistant_name(self):
        """Assistant name should match settings.json."""
        self.assertEqual(
            self.config.get("assistant", "name"),
            "MAYDAY"
        )

    def test_get_version(self):
        """Version should match settings.json."""
        self.assertEqual(
            self.config.get("assistant", "version"),
            "0.1.0"
        )

    def test_invalid_key(self):
        """Invalid key should return None."""
        self.assertIsNone(
            self.config.get("invalid", "key")
        )


if __name__ == "__main__":
    unittest.main()
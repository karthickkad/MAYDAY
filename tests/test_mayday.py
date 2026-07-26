import unittest

from core.mayday import Mayday


class TestMayday(unittest.TestCase):

    def test_create_application(self):
        """Application should initialize successfully."""

        app = Mayday()

        self.assertIsNotNone(app)

    def test_command_manager_exists(self):
        """CommandManager should be initialized."""

        app = Mayday()

        self.assertIsNotNone(app.command_manager)

    def test_config_exists(self):
        """Config should be initialized."""

        app = Mayday()

        self.assertIsNotNone(app.config)


if __name__ == "__main__":
    unittest.main()
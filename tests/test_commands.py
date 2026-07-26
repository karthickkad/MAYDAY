import unittest

from core.commands import CommandManager


class TestCommandManager(unittest.TestCase):

    def setUp(self):
        """Create a CommandManager before each test."""
        self.command = CommandManager()

    def test_execute_help(self):
        """The help command should execute without exception."""
        try:
            self.command.execute("help")
        except Exception as error:
            self.fail(f"help command raised {error}")

    def test_execute_version(self):
        """The version command should execute without exception."""
        try:
            self.command.execute("version")
        except Exception as error:
            self.fail(f"version command raised {error}")

    def test_execute_clear(self):
        """The clear command should execute without exception."""
        try:
            self.command.execute("clear")
        except Exception as error:
            self.fail(f"clear command raised {error}")

    def test_unknown_command(self):
        """Unknown commands should not crash."""
        try:
            self.command.execute("mayday123")
        except Exception as error:
            self.fail(f"Unknown command raised {error}")


if __name__ == "__main__":
    unittest.main()
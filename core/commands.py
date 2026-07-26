"""
commands.py

Command manager for MAYDAY.
"""
from core.version import Version
from core.banner import Banner
from core.utils  import clear_console


class CommandManager:
    """Handles all MAYDAY commands."""

    def execute(self, command):

        command = command.strip().lower()

        if command == "":
            return

        elif command == "help":
            self.help()

        elif command == "version":
            self.version()

        elif command == "clear":
            self.clear()

        else:
            self.unknown(command)

    def help(self):
        print("\nAvailable Commands")
        print("------------------")
        print("help      - Show available commands")
        print("version   - Show MAYDAY version")
        print("clear     - Clear the console")
        print("exit      - Exit MAYDAY")
        print()

    def version(self):
        print(f"\n{Version.get_full_name()}\n")

    def clear(self):
        clear_console()
        Banner.show()

    def unknown(self, command):
        print(f"MAYDAY : Unknown command -> {command}")
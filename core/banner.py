"""
banner.py

Displays the MAYDAY startup banner.
"""

from core.version import Version


class Banner:
    """Displays the application banner."""

    @staticmethod
    def show():
        print("=" * 60)
        print(f"                 {Version.get_full_name()}")
        print("          Modular AI Assistant Framework")
        print("=" * 60)
        print("Type 'help'    - Show available commands")
        print("Type 'version' - Show application version")
        print("Type 'exit'    - Exit MAYDAY")
        print()
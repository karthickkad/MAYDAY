"""
version.py

Stores application version information.
"""

from pathlib import Path
import json


class Version:
    """Application version information."""

    VERSION_FILE = Path(__file__).resolve().parent.parent / "config" / "version.json"

    @classmethod
    def get_version(cls):
        """Return the current project version."""
        try:
            with open(cls.VERSION_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("version", "Unknown")
        except (FileNotFoundError, json.JSONDecodeError):
            return "Unknown"

    @classmethod
    def get_full_name(cls):
        """Return the formatted application name."""
        return f"MAYDAY v{cls.get_version()}"
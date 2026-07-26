from pathlib import Path
import json


class Version:
    """Version information."""

    VERSION_FILE = Path(__file__).resolve().parent.parent / "config" / "version.json"

    @classmethod
    def get_version(cls):
        """Return current project version."""
        try:
            with open(cls.VERSION_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("version", "Unknown")
        except (FileNotFoundError, json.JSONDecodeError):
            return "Unknown"

    @classmethod
    def get_full_name(cls):
        """Return formatted application name."""
        return f"MAYDAY v{cls.get_version()}"
"""
release/version.py

Handles automatic version generation.

Version format:
YYYY.MM.DD.REVISION

Examples:
2026.07.26.1
2026.07.26.2
2026.07.27.1
"""

from datetime import datetime
from pathlib import Path
import json
from typing import Optional


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = PROJECT_ROOT / "config"

VERSION_FILE = CONFIG_DIR / "version.json"


class VersionManager:
    """
    Manages project version information.
    """

    @staticmethod
    def load() -> Optional[str]:
        """
        Load the current version.
        """

        if not VERSION_FILE.exists():
            return None

        try:
            with open(VERSION_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("version")

        except (json.JSONDecodeError, OSError):
            return None

    @staticmethod
    def generate(old_version: Optional[str]) -> str:
        """
        Generate the next version.
        """

        today = datetime.now().strftime("%Y.%m.%d")

        if old_version:

            try:

                parts = old_version.split(".")

                old_date = ".".join(parts[:3])

                revision = int(parts[3])

                if old_date == today:
                    return f"{today}.{revision + 1}"

            except (ValueError, IndexError):
                pass

        return f"{today}.1"

    @staticmethod
    def save(version: str) -> None:
        """
        Save the generated version.
        """

        CONFIG_DIR.mkdir(exist_ok=True)

        with open(VERSION_FILE, "w", encoding="utf-8") as file:

            json.dump(
                {
                    "version": version
                },
                file,
                indent=4
            )

    @staticmethod
    def get_release_date() -> str:
        """
        Return today's release date.
        """

        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def get_release_time() -> str:
        """
        Return current release time.
        """

        return datetime.now().strftime("%H:%M:%S")
"""
release/readme.py

Updates the version number inside README.md.
"""

from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parent.parent
README_FILE = PROJECT_ROOT / "README.md"


class ReadmeManager:
    """
    Handles README.md updates.
    """

    # Matches:
    # | Version | **2026.07.26.2** |
    VERSION_PATTERN = re.compile(
        r"(\|\s*Version\s*\|\s*\*\*)(.+?)(\*\*\s*\|)",
        re.IGNORECASE
    )

    @classmethod
    def update_version(cls, version: str) -> None:
        """
        Update the version inside README.md.
        """

        if not README_FILE.exists():
            raise FileNotFoundError("README.md not found.")

        text = README_FILE.read_text(encoding="utf-8")

        if not cls.VERSION_PATTERN.search(text):
            raise ValueError(
                "Version entry not found in README.md."
            )

        updated = cls.VERSION_PATTERN.sub(
            rf"\1{version}\3",
            text,
            count=1
        )

        README_FILE.write_text(updated, encoding="utf-8")

    @staticmethod
    def exists() -> bool:
        """
        Check whether README.md exists.
        """

        return README_FILE.exists()

    @staticmethod
    def path() -> Path:
        """
        Return README.md path.
        """

        return README_FILE
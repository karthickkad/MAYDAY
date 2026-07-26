"""
release/changelog.py

Handles CHANGELOG.md updates.

Creates the file if it does not exist and
prepends new release entries.
"""

from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"


HEADER = """# Changelog

All notable changes to this project will be documented in this file.

The project uses the following version format:

YYYY.MM.DD.REVISION

---
"""


class ChangelogManager:
    """
    Handles CHANGELOG.md.
    """

    @staticmethod
    def exists() -> bool:
        return CHANGELOG_FILE.exists()

    @staticmethod
    def path() -> Path:
        return CHANGELOG_FILE

    @staticmethod
    def create() -> None:
        """
        Create CHANGELOG.md if missing.
        """

        if not CHANGELOG_FILE.exists():
            CHANGELOG_FILE.write_text(
                HEADER,
                encoding="utf-8"
            )

    @staticmethod
    def build_entry(version: str) -> str:
        """
        Create a new release entry.
        """

        today = datetime.now().strftime("%Y-%m-%d")

        return f"""
## [{version}] - {today}

### Added

-

### Changed

-

### Fixed

-

### Removed

-

---

"""

    @classmethod
    def update(cls, version: str) -> None:
        """
        Add a new release entry.
        """

        cls.create()

        current = CHANGELOG_FILE.read_text(
            encoding="utf-8"
        )

        entry = cls.build_entry(version)

        if f"## [{version}]" in current:
            print("CHANGELOG already contains this version.")
            return

        separator = "---"

        if separator in current:

            header, body = current.split(
                separator,
                maxsplit=1
            )

            new_content = (
                header
                + separator
                + "\n"
                + entry
                + body.lstrip()
            )

        else:
            new_content = current + "\n" + entry

        CHANGELOG_FILE.write_text(
            new_content,
            encoding="utf-8"
        )

        print("CHANGELOG updated successfully.")
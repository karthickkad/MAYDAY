"""
release/utils.py

Shared utility functions for the MAYDAY Release Manager.
"""

from pathlib import Path
from datetime import datetime
import shutil


class Console:
    """Console helper methods."""

    WIDTH = 60

    @staticmethod
    def line(char: str = "=") -> None:
        print(char * Console.WIDTH)

    @staticmethod
    def banner(title: str) -> None:
        Console.line()
        print(title.center(Console.WIDTH))
        Console.line()

    @staticmethod
    def section(title: str) -> None:
        print()
        Console.line("-")
        print(title)
        Console.line("-")

    @staticmethod
    def success(message: str) -> None:
        print(f"[OK] {message}")

    @staticmethod
    def warning(message: str) -> None:
        print(f"[WARNING] {message}")

    @staticmethod
    def error(message: str) -> None:
        print(f"[ERROR] {message}")

    @staticmethod
    def info(message: str) -> None:
        print(f"[INFO] {message}")

    @staticmethod
    def step(number: int, total: int, message: str) -> None:
        print(f"[{number}/{total}] {message}")


class Prompt:
    """User confirmation prompts."""

    @staticmethod
    def yes_no(message: str) -> bool:

        while True:

            answer = input(f"{message} (Y/N): ").strip().lower()

            if answer in ("y", "yes"):
                return True

            if answer in ("n", "no"):
                return False

            print("Please enter Y or N.")


class Backup:
    """File backup helper."""

    @staticmethod
    def create(file_path: Path) -> Path | None:

        if not file_path.exists():
            return None

        backup = file_path.with_suffix(
            file_path.suffix + ".bak"
        )

        shutil.copy2(file_path, backup)

        return backup


class Timer:
    """Simple execution timer."""

    def __init__(self):

        self.start = datetime.now()

    def elapsed(self) -> float:

        return (
            datetime.now() - self.start
        ).total_seconds()
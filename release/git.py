"""
release/git.py

Handles Git operations for the MAYDAY Release Manager.
"""

from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class GitError(Exception):
    """Raised when a Git command fails."""


class GitManager:
    """Handles Git operations."""

    @staticmethod
    def _run(command: list[str]) -> str:
        """
        Execute a Git command.
        """

        try:
            result = subprocess.run(
                command,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=True
            )

            return result.stdout.strip()

        except subprocess.CalledProcessError as error:
            raise GitError(
                error.stderr.strip() or "Git command failed."
            ) from error

    @classmethod
    def is_git_repository(cls) -> bool:
        """
        Check whether the project is a Git repository.
        """

        try:
            cls._run(["git", "rev-parse", "--is-inside-work-tree"])
            return True
        except GitError:
            return False

    @classmethod
    def current_branch(cls) -> str:
        """
        Return the current Git branch.
        """

        return cls._run(
            ["git", "branch", "--show-current"]
        )

    @classmethod
    def has_changes(cls) -> bool:
        """
        Return True if there are uncommitted changes.
        """

        output = cls._run(
            ["git", "status", "--porcelain"]
        )

        return bool(output)

    @classmethod
    def add_all(cls) -> None:
        """
        Stage all files.
        """

        cls._run(["git", "add", "."])

    @classmethod
    def commit(cls, version: str) -> None:
        """
        Create a release commit.
        """

        message = f"release: v{version}"

        cls._run(
            [
                "git",
                "commit",
                "-m",
                message
            ]
        )

    @classmethod
    def tag(cls, version: str) -> None:
        """
        Create an annotated Git tag.
        """

        cls._run(
            [
                "git",
                "tag",
                "-a",
                f"v{version}",
                "-m",
                f"Release v{version}"
            ]
        )

    @classmethod
    def push(cls) -> None:
        """
        Push commits to origin.
        """

        branch = cls.current_branch()

        cls._run(
            [
                "git",
                "push",
                "origin",
                branch
            ]
        )

    @classmethod
    def push_tags(cls) -> None:
        """
        Push tags.
        """

        cls._run(
            [
                "git",
                "push",
                "--tags"
            ]
        )

    @classmethod
    def latest_tag(cls) -> str:
        """
        Return the latest Git tag.
        """

        return cls._run(
            [
                "git",
                "describe",
                "--tags",
                "--abbrev=0"
            ]
        )

    @classmethod
    def status(cls) -> str:
        """
        Return Git status.
        """

        return cls._run(
            [
                "git",
                "status",
                "--short"
            ]
        )
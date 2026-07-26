"""
version.py

Stores application version information.
"""


class Version:
    """Application version information."""

    MAJOR = 0
    MINOR = 1
    PATCH = 0

    @classmethod
    def get_version(cls):
        return f"{cls.MAJOR}.{cls.MINOR}.{cls.PATCH}"

    @classmethod
    def get_full_name(cls):
        return f"MAYDAY v{cls.get_version()}"

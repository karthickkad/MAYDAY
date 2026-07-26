"""
exceptions.py

Custom exceptions used throughout the MAYDAY project.
"""


class MaydayError(Exception):
    """Base exception for all MAYDAY errors."""

    pass


class ConfigurationError(MaydayError):
    """Raised when configuration loading fails."""

    pass


class CommandError(MaydayError):
    """Raised when command execution fails."""

    pass


class PluginError(MaydayError):
    """Raised when a plugin cannot be loaded."""

    pass


class LoggerError(MaydayError):
    """Raised when the logger fails."""

    pass
"""
config.py

Configuration manager for MAYDAY.
"""

import json
from pathlib import Path

from core.exceptions import ConfigurationError

class Config:
    """Loads and provides access to application settings."""

    CONFIG_FILE = Path("config") / "settings.json"

    def __init__(self):
        self.settings = {}
        self.load()

    def load(self):
        """Load configuration from JSON file."""
        
        try:
            
            with open(self.CONFIG_FILE, "r", encoding="utf-8") as file:
                self.settings = json.load(file)
            
        except FileNotFoundError as error:
            
            raise ConfigurationError(
            f"Configuration file not found: {self.CONFIG_FILE}"
            ) from error
            
        except json.JSONDecodeError as error:
            
            raise ConfigurationError(
            "Invalid JSON in configuration file."
            ) from error
        

    def get(self, *keys, default=None):
        """
        Get a configuration value.

        Example:
            get("assistant", "name")
        """

        value = self.settings

        try:
            for key in keys:
                value = value[key]

            return value

        except (KeyError, TypeError):
            return default

    def reload(self):
        """Reload configuration."""

        self.load()
"""
utils.py

Common utility functions used throughout MAYDAY.
"""

import os
from datetime import datetime


def clear_console():
    """Clear the terminal screen."""

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def current_time():
    """Return the current time."""

    return datetime.now().strftime("%H:%M:%S")


def current_date():
    """Return the current date."""

    return datetime.now().strftime("%Y-%m-%d")


def current_datetime():
    """Return the current date and time."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
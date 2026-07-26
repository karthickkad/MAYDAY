import unittest
from datetime import datetime

from core.utils import (
    current_time,
    current_date,
    current_datetime,
)


class TestUtils(unittest.TestCase):

    def test_current_time(self):
        """Time should be in HH:MM:SS format."""

        time = current_time()

        try:
            datetime.strptime(time, "%H:%M:%S")
        except ValueError:
            self.fail("Invalid time format")

    def test_current_date(self):
        """Date should be in YYYY-MM-DD format."""

        date = current_date()

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            self.fail("Invalid date format")

    def test_current_datetime(self):
        """Datetime should be in YYYY-MM-DD HH:MM:SS format."""

        dt = current_datetime()

        try:
            datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.fail("Invalid datetime format")


if __name__ == "__main__":
    unittest.main()
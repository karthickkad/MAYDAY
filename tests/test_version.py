import unittest

from core.version import Version

class TestVersion(unittest.TestCase):

    def test_get_version(self):
        version = Version.get_version()

        self.assertIsInstance(version, str)
        self.assertNotEqual(version, "Unknown")
        self.assertRegex(version, r"^\d{4}\.\d{2}\.\d{2}\.\d+$")

    def test_get_full_name(self):
        self.assertEqual(
            Version.get_full_name(),
            f"MAYDAY v{Version.get_version()}"
        )


if __name__ == "__main__":
    unittest.main()
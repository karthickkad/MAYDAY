"""
release.py

MAYDAY Release Manager

Version Format:
YYYY.MM.DD.REVISION
"""

from datetime import datetime
from pathlib import Path
import json
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_DIR = PROJECT_ROOT / "config"

VERSION_FILE = CONFIG_DIR / "version.json"
BACKUP_FILE = CONFIG_DIR / "version_backup.json"


# --------------------------------------------------------
# Utility Functions
# --------------------------------------------------------

def banner():
    print("\n" + "=" * 60)
    print("              MAYDAY RELEASE MANAGER")
    print("=" * 60)


def load_version():
    if not VERSION_FILE.exists():
        return None

    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("version")
    except (json.JSONDecodeError, OSError):
        return None


def generate_version(old_version):
    today = datetime.now().strftime("%Y.%m.%d")

    if old_version:
        try:
            old_parts = old_version.split(".")

            old_date = ".".join(old_parts[:3])
            revision = int(old_parts[3])

            if old_date == today:
                return f"{today}.{revision + 1}"

        except (IndexError, ValueError):
            pass

    return f"{today}.1"


def backup_version():
    if VERSION_FILE.exists():
        shutil.copy2(VERSION_FILE, BACKUP_FILE)


def save_version(version):
    CONFIG_DIR.mkdir(exist_ok=True)

    with open(VERSION_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {
                "version": version
            },
            file,
            indent=4
        )


def show_summary(old_version, new_version):
    print()
    print(f"Current Version : {old_version}")
    print(f"Next Version    : {new_version}")
    print(f"Release Date    : {datetime.now():%Y-%m-%d}")
    print(f"Release Time    : {datetime.now():%H:%M:%S}")
    print()


def confirm():
    while True:
        choice = input("Generate this release? (Y/N): ").strip().lower()

        if choice in ("y", "yes"):
            return True

        if choice in ("n", "no"):
            return False

        print("Please enter Y or N.")


# --------------------------------------------------------
# Main
# --------------------------------------------------------

def main():
    banner()

    old_version = load_version()

    if old_version is None:
        print("No version found.")
        old_version = "None"

    new_version = generate_version(
        None if old_version == "None" else old_version
    )

    show_summary(old_version, new_version)

    if not confirm():
        print("\nRelease cancelled.")
        sys.exit(0)

    backup_version()

    save_version(new_version)

    print("\nRelease completed successfully.")
    print(f"New Version : {new_version}")

    if BACKUP_FILE.exists():
        print(f"Backup File : {BACKUP_FILE.name}")


if __name__ == "__main__":
    main()
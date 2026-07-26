#!/usr/bin/env python3
"""
release.py
Automates MAYDAY releases.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

VERSION_FILE = Path("config/version.json")


def run(cmd):
    print(f"> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


# Load version.json
with open(VERSION_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Current date & release time
release_time = datetime.now(ZoneInfo("Asia/Kolkata"))
today_str = release_time.strftime("%Y.%m.%d")
release_time_str = release_time.strftime("%Y-%m-%d %H:%M:%S %Z")

# Previous version
version = data["version"]
parts = version.split(".")

if len(parts) != 4:
    raise ValueError("Version must be YYYY.MM.DD.BUILD")

old_date = ".".join(parts[:3])
old_build = int(parts[3])

# Increment build or reset on new day
if old_date == today_str:
    build = old_build + 1
else:
    build = 1

new_version = f"{today_str}.{build}"

# Update version.json
data["version"] = new_version
data["release"] = data.get("release", "Layer 1 - Foundation")
data["released_at"] = release_time_str

with open(VERSION_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
    f.write("\n")

print(f"\nUpdated version: {version} → {new_version}")

tag = f"v{new_version}"

# Get current Git branch
branch = subprocess.check_output(
    ["git", "branch", "--show-current"],
    text=True
).strip()

# Git commands
run(["git", "add", str(VERSION_FILE)])
run(["git", "commit", "-m", f"chore: bump version to {tag}"])
run(["git", "tag", "-a", tag, "-m", f"MAYDAY {tag}"])
run(["git", "push", "origin", branch])
run(["git", "push", "origin", tag])

# Get current commit hash
commit = subprocess.check_output(
    ["git", "rev-parse", "--short", "HEAD"],
    text=True
).strip()

# Release summary
print("\n============================================================")
print("                 MAYDAY RELEASE MANAGER")
print("============================================================")
print("✓ Version updated")
print("✓ Version file saved")
print("✓ Git commit created")
print("✓ Git tag created")
print("✓ Changes pushed")
print("✓ Tag pushed")

print("\n------------------------------------------------------------")
print("Release Summary")
print("------------------------------------------------------------")
print(f"Version      : {new_version}")
print(f"Release      : {data['release']}")
print(f"Release Time : {release_time_str}")
print(f"Branch       : {branch}")
print(f"Commit       : {commit}")
print(f"Git Tag      : {tag}")

print("============================================================")
print(" Release completed successfully!")
print("============================================================")
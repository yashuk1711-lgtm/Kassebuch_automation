import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import paths
from version import VERSION

GITHUB_REPO = "yashuk1711-lgtm/kassebuch_automation"
RELEASES_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
UPDATE_ASSET_NAME = "gui-update.zip"


def _parse_version(text):
    text = text.strip().lstrip("vV")
    parts = text.split(".")
    return tuple(int(p) for p in parts if p.isdigit())


def check_for_update():
    """
    Returns a dict with "version", "notes", "download_url" if a newer
    release is available on GitHub, or None if already up to date (or
    the check failed, e.g. no internet).
    """

    try:
        request = urllib.request.Request(
            RELEASES_API,
            headers={"Accept": "application/vnd.github+json"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            release = json.load(response)

    except Exception as e:
        return {"error": str(e)}

    latest_tag = release.get("tag_name", "")

    try:
        if _parse_version(latest_tag) <= _parse_version(VERSION):
            return None
    except ValueError:
        return {"error": f"Could not parse version tag: {latest_tag}"}

    download_url = None

    for asset in release.get("assets", []):
        if asset.get("name") == UPDATE_ASSET_NAME:
            download_url = asset.get("browser_download_url")
            break

    if not download_url:
        return {"error": f"Release {latest_tag} has no {UPDATE_ASSET_NAME} asset."}

    return {
        "version": latest_tag,
        "notes": release.get("body", ""),
        "download_url": download_url
    }


def apply_update(download_url):
    """
    Downloads the update zip, extracts it, and launches a detached
    helper script that waits for this process to exit, replaces
    gui.exe + _internal with the new files, and relaunches the app.
    Data/, Outputs/, settings.json, Tesseract-OCR/, and poppler/ are
    left untouched.

    Call this, then close the application immediately afterward.
    """

    temp_dir = Path(tempfile.mkdtemp(prefix="kassenbuch_update_"))
    zip_path = temp_dir / UPDATE_ASSET_NAME
    extract_dir = temp_dir / "extracted"

    urllib.request.urlretrieve(download_url, zip_path)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    target_dir = paths.BASE_DIR
    exe_path = target_dir / "gui.exe"

    bat_path = temp_dir / "apply_update.bat"

    bat_content = (
        "@echo off\r\n"
        "timeout /t 2 /nobreak >nul\r\n"
        f'robocopy "{extract_dir}" "{target_dir}" /E /IS /IT\r\n'
        f'start "" "{exe_path}"\r\n'
        f'rmdir /s /q "{temp_dir}"\r\n'
    )

    bat_path.write_text(bat_content, encoding="utf-8")

    creationflags = (
        getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
        | getattr(subprocess, "DETACHED_PROCESS", 0)
    )

    subprocess.Popen(
        ["cmd", "/c", str(bat_path)],
        creationflags=creationflags
    )


if __name__ == "__main__":
    print("Current version:", VERSION)
    print(check_for_update())

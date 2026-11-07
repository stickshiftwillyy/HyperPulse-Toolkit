"""
=============================================================================
HyperPulse Toolkit - Remote OTA Updater Engine [V1]
Developed by Adrian (@stickshiftwillyy)
Target OS: Windows 10 / Windows 11 (64-bit)

Lightweight GitHub raw JSON version polling client allowing Adrian to push
live updates, release notes, and binary patch links to app users.
=============================================================================
"""

import os
import json
import urllib.request
import urllib.error
import sys
from typing import Dict, Any, Optional
from packaging import version

CURRENT_VERSION = "1.0.0"
DEFAULT_GITHUB_USER = "stickshiftwillyy"
DEFAULT_GITHUB_REPO = "HyperPulse-Toolkit"

if getattr(sys, "frozen", False):
    DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(sys.executable), "config.json")
else:
    DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")


def load_update_config() -> Dict[str, str]:
    """Loads configured repository info or returns defaults."""
    config_file = os.path.abspath(DEFAULT_CONFIG_PATH)
    if os.path.isfile(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "github_user": DEFAULT_GITHUB_USER,
        "github_repo": DEFAULT_GITHUB_REPO,
        "raw_url": f"https://raw.githubusercontent.com/{DEFAULT_GITHUB_USER}/{DEFAULT_GITHUB_REPO}/main/version.json"
    }


def save_update_config(github_user: str, github_repo: str):
    """Saves user-customized GitHub repository settings."""
    config_file = os.path.abspath(DEFAULT_CONFIG_PATH)
    data = {
        "github_user": github_user.strip(),
        "github_repo": github_repo.strip(),
        "raw_url": f"https://raw.githubusercontent.com/{github_user.strip()}/{github_repo.strip()}/main/version.json"
    }
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def check_for_updates(custom_raw_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Checks remote version.json on GitHub.
    Returns:
        {
            "has_update": bool,
            "current_version": str,
            "remote_version": str,
            "release_notes": str,
            "download_url": str,
            "status_message": str,
            "success": bool
        }
    """
    cfg = load_update_config()
    target_url = custom_raw_url or cfg.get("raw_url")

    result = {
        "has_update": False,
        "current_version": CURRENT_VERSION,
        "remote_version": CURRENT_VERSION,
        "release_notes": "",
        "download_url": "",
        "status_message": "",
        "success": False
    }

    if not target_url or "your-username" in target_url:
        result["status_message"] = "GitHub repository not configured yet. Configure in Settings tab."
        return result

    try:
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": f"HyperPulse-Toolkit/{CURRENT_VERSION}"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                remote_ver = str(data.get("version", CURRENT_VERSION)).strip()
                result["remote_version"] = remote_ver
                result["release_notes"] = data.get("changelog", "No release notes provided.")
                result["download_url"] = data.get("download_url", f"https://github.com/{cfg.get('github_user')}/{cfg.get('github_repo')}/releases")
                result["success"] = True

                # Version comparison
                if version.parse(remote_ver) > version.parse(CURRENT_VERSION):
                    result["has_update"] = True
                    result["status_message"] = f"New update available: v{remote_ver}!"
                else:
                    result["has_update"] = False
                    result["status_message"] = f"You are up to date! (v{CURRENT_VERSION})"
            else:
                result["status_message"] = f"Server returned HTTP {response.status}"
    except urllib.error.URLError as e:
        result["status_message"] = f"Network connection failed: {e.reason}"
    except Exception as e:
        result["status_message"] = f"Update check error: {str(e)}"

    return result

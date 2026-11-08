"""
=============================================================================
HyperPulse Toolkit - Magisk, KernelSU & APatch Module Catalog [V1.1]
Curated & Maintained by Adrian (@stickshiftwillyy)
Target OS: Windows 10 / Windows 11 (64-bit)

Provides 1-click ADB injection and pre-configured repository links for the
most critical root modules (Play Integrity Fix, Shamiko, Zygisk, AdAway).
=============================================================================
"""

import os
import urllib.request
import threading
from typing import List, Dict, Any, Tuple, Optional


MODULES_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "play_integrity_fix",
        "name": "Play Integrity Fix",
        "author": "chiteroman",
        "category": "Banking & Security",
        "badge": "🛡️ Essential",
        "desc": "Fixes Google Pay, Banking Apps, and RCS. Passes MEETS_DEVICE_INTEGRITY & MEETS_BASIC_INTEGRITY on unlocked bootloaders.",
        "download_url": "https://github.com/chiteroman/PlayIntegrityFix/releases/latest/download/PlayIntegrityFix.zip",
        "filename": "PlayIntegrityFix.zip"
    },
    {
        "id": "shamiko",
        "name": "Shamiko (Root Hider)",
        "author": "LSPosed Team",
        "category": "Root Hiding",
        "badge": "🕵️ Stealth",
        "desc": "Advanced Zygisk-based root-hiding module. Completely cloaks root, Magisk, and custom recoveries from stubborn banking apps.",
        "download_url": "https://github.com/LSPosed/LSPosed.github.io/releases/download/shamiko-336/Shamiko-v1.1.1-336-release.zip",
        "filename": "Shamiko.zip"
    },
    {
        "id": "zygisk_next",
        "name": "Zygisk Next",
        "author": "bmax121",
        "category": "Core Framework",
        "badge": "⚡ Framework",
        "desc": "Next-generation standalone Zygisk injection framework. Works on KernelSU, APatch, and Magisk with zero overhead.",
        "download_url": "https://github.com/bmax121/ZygiskNext/releases/latest/download/Zygisk-Next.zip",
        "filename": "Zygisk-Next.zip"
    },
    {
        "id": "systemless_hosts",
        "name": "Systemless Hosts (AdAway)",
        "author": "AdAway Team",
        "category": "Ad Blocking",
        "badge": "🚫 Zero Ads",
        "desc": "Enables systemless /etc/hosts file redirection for AdAway, completely stripping banner and video ads across all apps.",
        "download_url": "https://github.com/AdAway/AdAway/releases/latest",
        "filename": "systemless-hosts.zip"
    },
    {
        "id": "universal_gms_doze",
        "name": "Universal GMS Doze",
        "author": "gloomyandy",
        "category": "Battery Saver",
        "badge": "🔋 Battery",
        "desc": "Optimizes Google Play Services wakelocks in the background, extending screen-on time by 1 to 2 hours per charge.",
        "download_url": "https://github.com/gloomyandy/Universal-GMS-Doze/releases/latest/download/UniversalGMSDoze.zip",
        "filename": "UniversalGMSDoze.zip"
    },
    {
        "id": "viper4android_fx",
        "name": "ViPER4Android FX Redux",
        "author": "Team V4A",
        "category": "Audio & Sound",
        "badge": "🔊 Studio Sound",
        "desc": "Legendary parametric equalizer and DSP sound processor. Dramatically elevates bass and clarity on Xiaomi speakers & headphones.",
        "download_url": "https://github.com/AndroidAudioMods/ViPER4AndroidFX/releases/latest/download/ViPER4AndroidFX.zip",
        "filename": "ViPER4AndroidFX.zip"
    }
]


def detect_root_type(adb_manager, device: Optional[str] = None) -> Tuple[str, bool]:
    """
    Detects whether the device is rooted with Magisk, KernelSU, APatch, or standard SU.
    Returns (root_type_name, is_rooted).
    """
    code, out, _ = adb_manager.run_adb(["shell", "su -c 'which magisk || which ksud || which apd || which su'"], device=device)
    if code == 0 and out:
        out_lower = out.lower()
        if "magisk" in out_lower:
            return "Magisk", True
        elif "ksud" in out_lower:
            return "KernelSU", True
        elif "apd" in out_lower:
            return "APatch", True
        elif "su" in out_lower:
            return "Rooted (su)", True

    return "Non-Root", False


def inject_module_file(
    adb_manager,
    local_zip_path: str,
    status_callback,
    device: Optional[str] = None
) -> bool:
    """
    Pushes and executes module installation directly via ADB root command.
    """
    if not os.path.isfile(local_zip_path):
        status_callback("Error: Module file not found.")
        return False

    file_name = os.path.basename(local_zip_path)
    remote_path = f"/data/local/tmp/{file_name}"

    status_callback(f"Pushing {file_name} to device...")
    push_code, _, push_err = adb_manager.run_adb(["push", local_zip_path, remote_path], device=device)
    if push_code != 0:
        status_callback(f"Failed to push file: {push_err}")
        return False

    status_callback("Detecting root manager on device...")
    root_type, is_root = detect_root_type(adb_manager, device)

    if not is_root:
        # Fallback: copy to /sdcard/Download/HyperPulse/ so user can install via recovery or app
        adb_manager.run_adb(["shell", "mkdir -p /sdcard/Download/HyperPulse"], device=device)
        adb_manager.run_adb(["shell", f"cp {remote_path} /sdcard/Download/HyperPulse/{file_name}"], device=device)
        status_callback(f"Device not rooted: Saved module to '/sdcard/Download/HyperPulse/{file_name}' for recovery flashing.")
        return True

    status_callback(f"Injecting module via {root_type}...")
    if root_type == "KernelSU":
        cmd = f"su -c 'ksud module install {remote_path}'"
    elif root_type == "APatch":
        cmd = f"su -c 'apd module install {remote_path}'"
    else:  # Magisk / default
        cmd = f"su -c 'magisk --install-module {remote_path}'"

    inst_code, inst_out, inst_err = adb_manager.run_adb(["shell", cmd], device=device, timeout=45)
    
    # Clean up tmp
    adb_manager.run_adb(["shell", f"rm -f {remote_path}"], device=device)

    if inst_code == 0:
        status_callback(f"✓ Successfully injected {file_name}! (Reboot to activate)")
        return True
    else:
        err_msg = inst_out if inst_out else inst_err
        status_callback(f"Injection warning/error: {err_msg[:120]}")
        return False

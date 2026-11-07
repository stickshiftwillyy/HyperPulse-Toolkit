"""
=============================================================================
HyperPulse Toolkit - Curated Xiaomi & Android Debloat Database [V1]
Researched, Benchmarked & Maintained by Adrian (@stickshiftwillyy)
Target OS: Windows 10 / Windows 11 (64-bit)

A categorized catalog of Xiaomi/HyperOS packages with strict safety tiers:
- Safe: Tested bloat, tracking daemons, analytics, and pre-installed junk.
- Caution: Optional OEM ecosystem apps (Mi Cloud, Notes, Wallpaper Carousel).
- Danger: Critical components (SystemUI, Launcher, Security Center).
=============================================================================
"""

from typing import List, Dict, Any, Set


DEBLOAT_CATALOG: List[Dict[str, Any]] = [
    # --- SAFE TO REMOVE (ADS, TRACKERS, BLOAT) ---
    {
        "package": "com.miui.msa.global",
        "name": "MIUI System Ads (MSA)",
        "category": "Ads & Telemetry",
        "level": "Safe",
        "desc": "Injects advertisements into native HyperOS/MIUI system apps (Themes, File Manager, Downloads)."
    },
    {
        "package": "com.miui.analytics",
        "name": "MIUI Analytics",
        "category": "Ads & Telemetry",
        "level": "Safe",
        "desc": "Collects usage telemetry and sends user behavior data to Xiaomi servers."
    },
    {
        "package": "com.miui.daemon",
        "name": "MIUI Daemon",
        "category": "Ads & Telemetry",
        "level": "Safe",
        "desc": "Background diagnostics and statistical logging service. Safe to remove; saves battery."
    },
    {
        "package": "com.miui.bugreport",
        "name": "Bug Report",
        "category": "Ads & Telemetry",
        "level": "Safe",
        "desc": "Transmits crash logs and bug reports to Xiaomi."
    },
    {
        "package": "com.miui.miservice",
        "name": "Services & Feedback",
        "category": "System Utilities",
        "level": "Safe",
        "desc": "User feedback submission utility."
    },
    {
        "package": "com.mi.globalbrowser",
        "name": "Mi Browser (Mint)",
        "category": "Bloatware Apps",
        "level": "Safe",
        "desc": "Stock Xiaomi browser bloated with news feeds and ad tracking. Safe to replace with Chrome/Brave."
    },
    {
        "package": "com.miui.videoplayer",
        "name": "Mi Video",
        "category": "Bloatware Apps",
        "level": "Safe",
        "desc": "Stock video player filled with trending online feeds and notifications."
    },
    {
        "package": "com.miui.player",
        "name": "Mi Music",
        "category": "Bloatware Apps",
        "level": "Safe",
        "desc": "Stock music player with ads and integrated streaming feeds."
    },
    {
        "package": "com.xiaomi.midrop",
        "name": "ShareMe (Mi Drop)",
        "category": "Bloatware Apps",
        "level": "Safe",
        "desc": "Xiaomi file sharing utility. Safe to remove if using Quick Share or LocalSend."
    },
    {
        "package": "com.xiaomi.mipicks",
        "name": "GetApps (Mi App Store)",
        "category": "Bloatware Apps",
        "level": "Safe",
        "desc": "Xiaomi proprietary app store. Spams unwanted install recommendations."
    },
    {
        "package": "com.xiaomi.glgm",
        "name": "Games Center",
        "category": "Bloatware Apps",
        "level": "Safe",
        "desc": "Xiaomi gaming hub with pre-installed trial promotions and spam push notifications."
    },
    {
        "package": "com.xiaomi.payment",
        "name": "Mi Pay / Mi Coin",
        "category": "Financial / Wallet",
        "level": "Safe",
        "desc": "Xiaomi payment framework. Safe to remove if using Google Pay, PhonePe, or Paytm."
    },
    {
        "package": "com.miui.yellowpage",
        "name": "Yellow Pages",
        "category": "System Utilities",
        "level": "Safe",
        "desc": "Caller ID and business directory integration for Xiaomi Dialer."
    },
    {
        "package": "com.miui.cleanmaster",
        "name": "Clean Master Definitions",
        "category": "Ads & Telemetry",
        "level": "Safe",
        "desc": "Clean Master definition engine inside Security app."
    },
    {
        "package": "com.facebook.katana",
        "name": "Facebook",
        "category": "Preloaded Partners",
        "level": "Safe",
        "desc": "Pre-installed social app. Safe to remove or install cleanly from Play Store."
    },
    {
        "package": "com.facebook.system",
        "name": "Facebook App Installer",
        "category": "Preloaded Partners",
        "level": "Safe",
        "desc": "Background service that auto-updates Facebook and Instagram silently."
    },
    {
        "package": "com.facebook.appmanager",
        "name": "Facebook App Manager",
        "category": "Preloaded Partners",
        "level": "Safe",
        "desc": "Meta background telemetry and silent asset manager."
    },
    {
        "package": "com.facebook.services",
        "name": "Facebook Services",
        "category": "Preloaded Partners",
        "level": "Safe",
        "desc": "Meta analytics framework daemon."
    },
    {
        "package": "com.netflix.partner.activation",
        "name": "Netflix Activation",
        "category": "Preloaded Partners",
        "level": "Safe",
        "desc": "Carrier partner stub for Netflix pre-registration."
    },
    {
        "package": "com.zhiliaoapp.musically",
        "name": "TikTok Preload",
        "category": "Preloaded Partners",
        "level": "Safe",
        "desc": "Pre-installed short video app stub."
    },
    {
        "package": "com.android.providers.partnerbookmarks",
        "name": "Partner Bookmarks",
        "category": "Bloatware Apps",
        "level": "Safe",
        "desc": "Preloaded sponsor bookmarks inside default browsers."
    },

    # --- CAUTION (OPTIONAL UTILITIES) ---
    {
        "package": "com.miui.android.fashiongallery",
        "name": "Wallpaper Carousel (Glance)",
        "category": "Lockscreen & Themes",
        "level": "Caution",
        "desc": "Lock screen glance ads and auto-rotating wallpapers. High battery and data drain."
    },
    {
        "package": "com.miui.hybrid",
        "name": "Quick Apps",
        "category": "System Utilities",
        "level": "Caution",
        "desc": "Instant web app engine. Can be safely removed if you do not use Quick Apps."
    },
    {
        "package": "com.miui.hybrid.accessory",
        "name": "Quick Apps Accessory",
        "category": "System Utilities",
        "level": "Caution",
        "desc": "Companion helper for Quick Apps runtime."
    },
    {
        "package": "com.miui.compass",
        "name": "Mi Compass",
        "category": "Tools",
        "level": "Caution",
        "desc": "Stock sensor-based compass application."
    },
    {
        "package": "com.miui.weather2",
        "name": "MIUI Weather",
        "category": "Tools",
        "level": "Caution",
        "desc": "Stock weather forecast widget. Safe if using Google Weather or alternative."
    },
    {
        "package": "com.miui.notes",
        "name": "MIUI Notes",
        "category": "Tools",
        "level": "Caution",
        "desc": "Stock note taking app. Do not remove if you have unsynced notes!"
    },
    {
        "package": "com.miui.screenrecorder",
        "name": "Screen Recorder",
        "category": "Tools",
        "level": "Caution",
        "desc": "Built-in HyperOS screen recording tool."
    },
    {
        "package": "com.xiaomi.scanner",
        "name": "Mi Scanner",
        "category": "Tools",
        "level": "Caution",
        "desc": "QR code scanner and document converter tool."
    },
    {
        "package": "com.miui.cloudservice",
        "name": "Mi Cloud Service",
        "category": "Xiaomi Cloud",
        "level": "Caution",
        "desc": "Xiaomi Cloud backup and synchronization engine. Safe if you use Google Drive."
    },
    {
        "package": "com.miui.micloudsync",
        "name": "Mi Cloud Sync",
        "category": "Xiaomi Cloud",
        "level": "Caution",
        "desc": "Background photo, contact, and message sync for Mi Cloud."
    },
    {
        "package": "com.xiaomi.joyose",
        "name": "Joyose Performance Manager",
        "category": "Gaming & Thermal",
        "level": "Caution",
        "desc": "Controls aggressive thermal throttling in games. Disabling is recommended for gamers."
    },

    # --- DANGER / DO NOT REMOVE NORMALLY ---
    {
        "package": "com.miui.securitycenter",
        "name": "MIUI Security Center",
        "category": "Core Security",
        "level": "Danger",
        "desc": "Manages app permissions, game turbo, and battery profiles. Removing causes bootloop on MIUI/HyperOS!"
    },
    {
        "package": "com.miui.home",
        "name": "HyperOS / POCO System Launcher",
        "category": "System UI",
        "level": "Danger",
        "desc": "Main home screen launcher. Removing without a replacement launcher makes device unusable."
    }
]


def get_installed_packages(adb_manager, device: str = None) -> Set[str]:
    """Retrieves all installed package names on user 0."""
    code, out, _ = adb_manager.run_adb(["shell", "pm list packages -u --user 0"], device=device)
    if code != 0 or not out:
        return set()
    
    packages = set()
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("package:"):
            pkg = line.replace("package:", "").strip()
            packages.add(pkg)
    return packages


def get_active_installed_packages(adb_manager, device: str = None) -> Set[str]:
    """Retrieves active (currently enabled) package names on user 0."""
    code, out, _ = adb_manager.run_adb(["shell", "pm list packages --user 0"], device=device)
    if code != 0 or not out:
        return set()
    
    packages = set()
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("package:"):
            pkg = line.replace("package:", "").strip()
            packages.add(pkg)
    return packages

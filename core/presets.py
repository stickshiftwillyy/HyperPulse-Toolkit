"""
=============================================================================
HyperPulse Toolkit - Curated Presets & Kernel/Framework Tweaks [V1]
Developed & Tested by Adrian (@stickshiftwillyy)
Target OS: Windows 10 / Windows 11 (64-bit)

Hand-tuned ADB optimization routines designed specifically for Xiaomi,
HyperOS, MIUI, and standard Android performance tuning. Includes Joyose thermal
governor bypass, display refresh locks, Shizuku runners, and UI speed tweaks.
=============================================================================
"""

from typing import List, Dict, Any


PRESETS: List[Dict[str, Any]] = [
    {
        "id": "disable_joyose",
        "title": "Disable Joyose Thermal Throttling",
        "category": "Gaming & Performance",
        "badge": "⚡ Xiaomi / HyperOS",
        "description": "Joyose is Xiaomi's game throttling service. Disabling it prevents thermal throttling, removes aggressive FPS drops in games like BGMI, Genshin, CoD, and unlocks sustained device performance.",
        "commands": [
            "shell pm disable-user --user 0 com.xiaomi.joyose",
            "shell am force-stop com.xiaomi.joyose"
        ],
        "restore_commands": [
            "shell pm enable com.xiaomi.joyose"
        ],
        "risk": "Safe"
    },
    {
        "id": "force_120hz",
        "title": "Force Constant 120Hz Refresh Rate",
        "category": "Display & Visuals",
        "badge": "🔥 Smoothness",
        "description": "Forces the display to stay locked at 120Hz at all times. Eliminates annoying stutter when apps like YouTube, Maps, Chrome, or social feeds drop down to 60Hz.",
        "commands": [
            "shell settings put system min_refresh_rate 120.0",
            "shell settings put system peak_refresh_rate 120.0",
            "shell settings put system user_refresh_rate 120"
        ],
        "restore_commands": [
            "shell settings put system min_refresh_rate 60.0",
            "shell settings put system peak_refresh_rate 120.0"
        ],
        "risk": "Safe"
    },
    {
        "id": "start_shizuku",
        "title": "Start Shizuku Service",
        "category": "System Utilities",
        "badge": "🚀 ADB Service",
        "description": "Starts the Shizuku server directly over ADB without needing wireless debugging pairing or root privileges. Once started, apps like Canta, Swift Backup, and Termux gain privileged APIs.",
        "commands": [
            "shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh"
        ],
        "restore_commands": [],
        "risk": "Safe"
    },
    {
        "id": "disable_ads_analytics",
        "title": "Disable Xiaomi Ads (MSA) & Analytics",
        "category": "Privacy & Battery",
        "badge": "🛡️ Anti-Bloat",
        "description": "Disables MIUI System Ads (com.miui.msa.global) and Xiaomi Analytics (com.miui.analytics). Stops background tracking, prevents system app ads, and saves battery.",
        "commands": [
            "shell pm disable-user --user 0 com.miui.msa.global",
            "shell pm disable-user --user 0 com.miui.analytics",
            "shell am force-stop com.miui.msa.global",
            "shell am force-stop com.miui.analytics"
        ],
        "restore_commands": [
            "shell pm enable com.miui.msa.global",
            "shell pm enable com.miui.analytics"
        ],
        "risk": "Safe"
    },
    {
        "id": "disable_mi_daemon",
        "title": "Disable Xiaomi Background Daemon",
        "category": "Privacy & Battery",
        "badge": "🔋 Battery Saver",
        "description": "Disables 'com.miui.daemon', an internal telemetry service constantly running in the background. Does not affect system stability or notifications.",
        "commands": [
            "shell pm disable-user --user 0 com.miui.daemon",
            "shell am force-stop com.miui.daemon"
        ],
        "restore_commands": [
            "shell pm enable com.miui.daemon"
        ],
        "risk": "Safe"
    },
    {
        "id": "animation_booster",
        "title": "2x Snappier UI (0.5x Animations)",
        "category": "Gaming & Performance",
        "badge": "⚡ Instant Feel",
        "description": "Sets Window Animation Scale, Transition Animation Scale, and Animator Duration Scale to 0.5x. Makes switching apps, opening menus, and launching apps feel twice as fast.",
        "commands": [
            "shell settings put global window_animation_scale 0.5",
            "shell settings put global transition_animation_scale 0.5",
            "shell settings put global animator_duration_scale 0.5"
        ],
        "restore_commands": [
            "shell settings put global window_animation_scale 1.0",
            "shell settings put global transition_animation_scale 1.0",
            "shell settings put global animator_duration_scale 1.0"
        ],
        "risk": "Safe"
    },
    {
        "id": "fix_display_color",
        "title": "Reset Display Color & HDR Profile",
        "category": "Display & Visuals",
        "badge": "🎨 Color Fix",
        "description": "Resets the display color mode and screen calibration settings to standard sRGB/Native profile. Resolves HDR video preview washing out and color-shifting issues.",
        "commands": [
            "shell settings put system screen_mode 1",
            "shell settings put system display_color_mode 0"
        ],
        "restore_commands": [],
        "risk": "Safe"
    },
    {
        "id": "mobile_data_always_on",
        "title": "Always Keep Mobile Data Active",
        "category": "Network & 5G",
        "badge": "📶 Low Latency",
        "description": "Ensures cellular data remains active in the background when connected to Wi-Fi. Guarantees zero latency drops when switching networks or during online gaming.",
        "commands": [
            "shell settings put global mobile_data_always_on 1"
        ],
        "restore_commands": [
            "shell settings put global mobile_data_always_on 0"
        ],
        "risk": "Safe"
    },
    {
        "id": "grant_canta",
        "title": "Grant Permissions to Canta Debloater",
        "category": "System Utilities",
        "badge": "🛠️ Package Manager",
        "description": "Grants DUMP and PACKAGE_USAGE_STATS permissions to Canta debloater app directly via ADB so it works seamlessly.",
        "commands": [
            "shell pm grant com.catchingnow.canta android.permission.DUMP",
            "shell pm grant com.catchingnow.canta android.permission.PACKAGE_USAGE_STATS"
        ],
        "restore_commands": [],
        "risk": "Safe"
    }
]

REBOOT_OPTIONS: List[Dict[str, str]] = [
    {
        "title": "Reboot System",
        "command": "reboot",
        "desc": "Standard device restart"
    },
    {
        "title": "Reboot to Recovery",
        "command": "reboot recovery",
        "desc": "Boots into TWRP, OrangeFox, or Stock Recovery"
    },
    {
        "title": "Reboot to Fastboot",
        "command": "reboot bootloader",
        "desc": "Boots to Fastboot mode for ROM flashing"
    },
    {
        "title": "Reboot to EDL (9008)",
        "command": "reboot edl",
        "desc": "Emergency Download Mode (Qualcomm/MTK Preloader)"
    }
]

"""
=============================================================================
HyperPulse Toolkit - Interactive Knowledge Base & Modding Guides [V1]
Written & Documented by Adrian (@stickshiftwillyy)
Target OS: Windows 10 / Windows 11 (64-bit)

Detailed, field-tested procedures for Shizuku, Canta debloating, official
Xiaomi Bootloader unlocking, custom recovery flashing, and display tone-mapping.
=============================================================================
"""

from typing import List, Dict, Any


TUTORIALS: List[Dict[str, Any]] = [
    {
        "id": "shizuku_setup",
        "title": "How to Setup Shizuku via HyperPulse",
        "icon": "🚀",
        "category": "ADB & Permissions",
        "summary": "Activate Shizuku without needing root or complex wireless pairing codes.",
        "content": """# Setting Up Shizuku (One-Click ADB Method)

### What is Shizuku?
Shizuku allows third-party Android applications (like **Canta**, **Swift Backup**, **Termux**, and **App Ops**) to use privileged system APIs directly using ADB permissions without requiring root access.

---

### Step 1: Install Shizuku on Your Phone
1. Download Shizuku from [GitHub](https://github.com/RikkaApps/Shizuku/releases) or the Google Play Store.
2. Open the Shizuku app once to let it initialize its internal directories.

---

### Step 2: Prepare Your Xiaomi / HyperOS Device
1. Open **Settings** -> **About Phone** -> Tap **OS version / MIUI version** 7 times to enable Developer Options.
2. Go to **Additional Settings** -> **Developer Options**.
3. Enable **USB Debugging**.
4. **Critical for Xiaomi/Redmi/POCO:** Scroll down and enable **USB debugging (Security settings)**. (This requires signing in to a Mi Account and tapping 'Next' on 3 prompts).

---

### Step 3: One-Click Activation
1. Connect your phone to your PC via USB cable.
2. Click **Presets Hub** on the left sidebar in HyperPulse Toolkit.
3. Locate **Start Shizuku Service** and click **Run**.
4. Shizuku on your phone will immediately turn green and display:
   > *"Shizuku is running (Version 13.x.x, adb)"*

---

### Step 4: Grant Permissions to Apps
- You can now open **Canta** or any Shizuku-compatible app and tap **Authorize**.
"""
    },
    {
        "id": "canta_debloat",
        "title": "Complete Canta & HyperPulse Debloat Guide",
        "icon": "🗑️",
        "category": "Debloating",
        "summary": "Safely remove pre-installed bloatware, tracking analytics, and system ads.",
        "content": """# Safe Debloating Guide for Xiaomi / HyperOS

### Why Debloat?
Modern Xiaomi, Redmi, and POCO devices ship with dozens of background services (MSA, Analytics, Joyose, GetApps, Carousel) that consume RAM, drain 10-15% extra battery per day, and trigger aggressive gaming throttling.

---

### Method A: Use HyperPulse Debloater Tab (PC Direct)
1. Navigate to the **Debloater** tab in HyperPulse Toolkit.
2. Click **Scan Installed Packages** to retrieve live packages on your phone.
3. Click **Filter: Safe** to show only 100% verified bloatware.
4. Click **Select All Safe** -> **Uninstall Selected**.
5. All selected bloatware will be removed cleanly for User 0 (`pm uninstall -k --user 0`).

---

### Method B: Use Canta on Your Phone (Standalone)
1. Install **Canta** from F-Droid or GitHub.
2. Open Canta and grant it Shizuku access.
3. Canta categorizes apps by safety:
   - 🟢 **Safe:** Guaranteed safe to delete (e.g. Mi Video, Music, GetApps, Facebook, TikTok).
   - 🟡 **Advanced:** Optional utilities (Mi Cloud, Notes, Wallpaper Carousel).
   - 🔴 **Expert / Unsafe:** Never delete (Launcher, Security Center, System UI).

---

### How to Restore an Accidentally Removed App
If you ever want an app back, run this command in HyperPulse **Terminal**:
```shell
pm install-existing --user 0 <package.name>
```
*Example to restore Mi Music:*
```shell
pm install-existing --user 0 com.miui.player
```
"""
    },
    {
        "id": "bootloader_unlock",
        "title": "Xiaomi Bootloader Unlocking Guide",
        "icon": "🔓",
        "category": "Bootloader & Fastboot",
        "summary": "Official Xiaomi and HyperOS bootloader unlock prerequisites and procedure.",
        "content": """# Xiaomi Bootloader Unlocking Tutorial

### Important Security Notice
> **Data Loss Warning:** Unlocking the bootloader will completely wipe all user data (factory reset) on your phone! Backup your photos, chats, and files first.

---

### Requirements for HyperOS (2024+)
1. **Xiaomi Community App:**
   - Download the official Xiaomi Community app (v5.3.31 or newer).
   - Set region to **Global** in app settings.
   - Go to **ME** tab -> **Unlock bootloader**.
   - Your Mi Account must be active for at least 30 days and account level 2+ to apply for unlock authorization.
2. **Bind Mi Account to Device:**
   - On your phone: **Developer Options** -> **Mi Unlock Status**.
   - Turn off Wi-Fi, turn on **Mobile Data** (using the SIM card linked to your Mi Account).
   - Tap **Add account and device**.

---

### Unlocking with Mi Flash Unlock Tool
1. Download official **Mi Flash Unlock Tool** on your PC.
2. Put your device in **Fastboot Mode**:
   - Power off, then hold **Volume Down + Power** until the FASTBOOT logo appears.
   - Or click **Reboot to Fastboot** in HyperPulse Dashboard.
3. Connect USB cable to PC.
4. Log into the same Mi Account in Mi Flash Unlock and click **Unlock**.
5. If you receive a waiting period prompt (e.g., 72 hours / 168 hours), wait the required time without logging out of your account, then reconnect and finish the unlock.
"""
    },
    {
        "id": "custom_rom_flash",
        "title": "Flashing Custom ROMs (Evolution X / AOSP)",
        "icon": "⚡",
        "category": "Custom ROMs",
        "summary": "Step-by-step guide to flashing Custom Recovery and sideloading ROMs cleanly.",
        "content": """# Flashing Custom ROMs & Recovery Guide

### Step 1: Boot to Fastboot Mode
1. Connect device to PC.
2. In HyperPulse Dashboard, click **Reboot to Fastboot** (or hold Vol Down + Power).

---

### Step 2: Flash Custom Recovery (TWRP / OrangeFox / EvoX Recovery)
Modern devices (Virtual A/B) flash recovery into the boot or vendor_boot partition:
```shell
fastboot flash boot recovery.img
```
*Or for devices with a dedicated recovery partition:*
```shell
fastboot flash recovery recovery.img
```
Reboot into Recovery:
```shell
fastboot reboot recovery
```

---

### Step 3: Clean Flash & Sideload ROM
1. Inside Custom Recovery, go to **Factory Reset / Format Data** and type `yes` to decrypt storage.
2. Select **Apply Update** -> **Apply from ADB (Sideload)**.
3. Open HyperPulse Toolkit **Terminal** and run:
```shell
sideload C:\\path\\to\\your_rom.zip
```
4. Once it reaches 47% or 100% and displays `Total xfer: 1.00x`, the ROM flash is complete.
5. Tap **Reboot System Now**.
"""
    },
    {
        "id": "fix_hdr_video",
        "title": "Fixing Video Playback & Washed Out HDR",
        "icon": "🎬",
        "category": "Display Calibration",
        "summary": "Resolve color shifting, dimming previews, and washed out HDR on YouTube.",
        "content": """# Fixing Video Color Shift & HDR Washout

### Why Does This Happen?
On AMOLED displays (especially MediaTek / Xiaomi panels), Android uses dynamic display profile switching:
- Standard UI runs in **P3 / Vivid / Saturated** color gamut.
- When an HDR10/Dolby Vision video stream is detected in YouTube, Instagram, or Gallery, the display engine triggers hardware HDR tone-mapping, dimming SDR UI elements and switching to Rec.2020/sRGB color space.
- This creates an apparent "loss of color" or dimming during thumbnail previews.

---

### Fix 1: Calibrate Display Color Scheme (Phone Settings)
1. Go to **Settings** -> **Display & Brightness** -> **Color scheme**.
2. Select **Standard** or **Saturated** (avoid 'Auto' if experiencing shifting).
3. Under **Adaptive Colors / True Tone**, toggle it **OFF**.

---

### Fix 2: Run HyperPulse Color Profile Reset
1. In HyperPulse Toolkit, navigate to **Presets Hub**.
2. Click **Reset Display Color & HDR Profile**.
3. HyperPulse applies the following clean color calibration flags:
```shell
settings put system screen_mode 1
settings put system display_color_mode 0
```
4. Restart YouTube to verify consistent color rendering.
"""
    }
]

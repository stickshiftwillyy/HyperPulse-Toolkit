<p align="center">
  <img src="assets/logo_white.png" alt="HyperPulse Toolkit Logo" width="420" />
</p>

<p align="center">
  <strong>The Ultimate All-in-One ADB, Telemetry & Debloat Studio for Xiaomi, HyperOS & Android</strong><br>
  <em>Architected and Developed by Adrian (<a href="https://github.com/stickshiftwillyy">@stickshiftwillyy</a>)</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Developer-stickshiftwillyy%20(Adrian)-06b6d4?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Version-V1.0.0-emerald?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Platform-Windows%20Only%20(64--bit)-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/UI-Pure%20Black%20AMOLED-000000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-In%20Active%20Development-amber?style=for-the-badge" />
</p>

---

## ⚡ About HyperPulse Toolkit

**HyperPulse Toolkit** was engineered by **Adrian (@stickshiftwillyy)** to address the growing frustration with aggressive OEM background throttling, bloated stock firmware, and fragmented terminal commands on Xiaomi, Redmi, POCO, and standard Android devices.

After extensive hours of hands-on testing, thermal governor profiling, and system-level debloating across both MediaTek and Snapdragon platforms (MIUI, HyperOS, and AOSP), this desktop suite was built from the ground up to give power users complete control over their hardware in a seamless, standalone Windows experience.

> [!IMPORTANT]
> **V1 Pre-Release Notice:** HyperPulse Toolkit is currently in active development. All Rights Reserved. Not for redistribution or commercial mirroring while under development.

---

## 🌟 Core Highlights & Capabilities

### 🎬 1. Cinematic Startup Experience
* **Custom Opening Animation:** Features a pure pitch-black AMOLED boot animation showcasing the custom HyperPulse brand identity.
* **Engine Diagnostics:** Automatically checks ADB daemon status, system drivers, and device communication protocols upon launch.

### 📱 2. Live Device Telemetry & Root Checker
* **Real-Time Polling:** Background engine continuously monitors USB states — detecting device connections, disconnections, authorization prompts, and fastboot states automatically.
* **Hardware Specs:** Displays Brand, Model, Codename, Android Version, HyperOS/MIUI Version, and Security Patch level at a glance.
* **Superuser Verification:** Directly inspects `su` binary integrity and confirms root execution status.
* **Display & Battery Telemetry:** Monitors battery percentage, charging state, screen resolution, and display refresh rate.
* **Instant Power Menu:** 1-Click reboot to System, Recovery, Fastboot, or Emergency Download Mode (EDL 9008).

### ⚡ 3. Hand-Tuned Optimization Presets Hub
* **Kill Joyose Thermal Throttling:** Disables Xiaomi's game governor to eliminate sudden FPS drops in heavy games (BGMI, Genshin Impact, CoD: Mobile).
* **Force Lock 120Hz Everywhere:** Overrides dynamic refresh drops, locking 120Hz smoothness across YouTube, Chrome, Google Maps, and social apps.
* **1-Click Shizuku Server Starter:** Launches Shizuku over ADB automatically without requiring wireless pairing or root access.
* **2x Snappier Animations:** Cuts window transitions and animator scales to `0.5x` for instantaneous response.
* **Disable MSA & Xiaomi Analytics:** Blocks background ad services and telemetry tracking daemons in one click.
* **Display Tone-Mapping & HDR Reset:** Resets display color calibrations to prevent washed-out HDR video playback.

### 🗑️ 4. Canta-Style Safety Package Debloater
* **Curated Safety Catalog:** Over 40+ known bloat packages categorized into **Safe** (green), **Caution** (yellow), and **Danger** (red) to prevent accidental bricking.
* **Live Scanner:** Reads active packages installed on the connected device and indicates installed vs. uninstalled status.
* **Multi-Selection & Batch Removal:** Uninstall pre-installed bloatware safely for User 0 (`pm uninstall -k --user 0`).
* **1-Click Package Restore:** Recover any accidentally removed system app with one click (`pm install-existing`).
* **Manual Command Field:** Remove or restore any custom third-party package by typing its package identifier.

### 💻 5. Integrated Real-Time ADB Terminal
* Full-featured interactive terminal with continuous streaming stdout/stderr output.
* Accepts both raw shell commands (`shell pm list packages`) and full adb syntax (`adb devices`).
* Quick-command shortcuts for instant telemetry queries.

### 📚 6. Step-by-Step Modding Guides & Tutorials
* **Shizuku Setup:** Wireless and USB debugging configuration walk-through.
* **Safe Debloating:** How to debloat and restore packages properly.
* **Official Bootloader Unlocking:** Comprehensive guide on Xiaomi Community app approval, 30-day requirements, and Mi Flash Unlock.
* **Custom ROMs & Recovery:** Flashing TWRP/OrangeFox and sideloading custom ROMs (Evolution X, LineageOS).
* **Fixing HDR Video Dimming:** Deep-dive display calibration guide.

### 🚀 7. Built-In Remote OTA Update Mechanism
* HyperPulse features a built-in remote update checker connecting directly to Adrian's GitHub repository.
* When updates, presets, or database additions are published, app users receive update alerts and changelogs directly inside the app.

---

## 🖥️ System Requirements

* **Operating System:** Windows 10 (64-bit) or Windows 11 (64-bit).
* **Hardware:** Any modern PC with an available USB port.
* **Phone Prerequisites:** Android 9.0 to Android 15/16 with **USB Debugging** enabled in Developer Options.
* **Zero Dependencies Needed:** Official Google platform-tools (`adb.exe`, `fastboot.exe`, DLLs) are pre-bundled directly inside the software!

---

## 🚀 How to Run

1. Download the latest **`HyperPulse-Toolkit.exe`** from the [**Releases**](https://github.com/stickshiftwillyy/HyperPulse-Toolkit/releases) tab.
2. Connect your phone via USB cable and ensure USB Debugging is turned **ON**.
3. Run **`HyperPulse-Toolkit.exe`** and enjoy complete control over your device!

---

## 🔒 License & Intellectual Property

```text
HyperPulse Toolkit V1 - Proprietary Early Access License
Copyright (c) 2026 Adrian (@stickshiftwillyy). All Rights Reserved.
```

This software is currently in active development by **Adrian (@stickshiftwillyy)**. Redistribution, unauthorized modification, commercial packaging, or public mirroring is strictly prohibited during the development phase. Future updates and open-source licensing will be announced on this repository.

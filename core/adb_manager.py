"""
=============================================================================
HyperPulse Toolkit - Core ADB & Fastboot Engine [V1]
Developed & Architected by Adrian (@stickshiftwillyy)
Operating System: Windows 10 / Windows 11 (64-bit)

A specialized Windows ADB & Fastboot controller engineered for Xiaomi,
HyperOS, and Android power users. Handles background polling, real-time
telemetry, superuser verification, and asynchronous shell command streaming.
=============================================================================
"""

import os
import sys
import subprocess
import threading
import time
import shutil
from typing import Callable, Optional, Dict, List, Tuple


class ADBManager:
    def __init__(self, custom_bin_path: Optional[str] = None):
        self.adb_path = self._resolve_binary("adb", custom_bin_path)
        self.fastboot_path = self._resolve_binary("fastboot", custom_bin_path)
        self.selected_device: Optional[str] = None
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._device_listeners: List[Callable[[List[Dict[str, str]]], None]] = []
        self._last_devices_cache: List[Dict[str, str]] = []

    def _resolve_binary(self, binary_name: str, custom_bin_path: Optional[str]) -> str:
        """Finds the binary either in custom_bin_path, bundled bin folder, or system PATH."""
        ext = ".exe" if sys.platform.startswith("win") else ""
        binary_with_ext = f"{binary_name}{ext}"

        # 1. Check custom path if provided
        if custom_bin_path and os.path.isdir(custom_bin_path):
            candidate = os.path.join(custom_bin_path, binary_with_ext)
            if os.path.isfile(candidate):
                return candidate

        # 2. Check bundled bin directory relative to this script / application
        if getattr(sys, "frozen", False):
            # PyInstaller bundle directory
            base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        bundled_candidate = os.path.join(base_dir, "bin", binary_with_ext)
        if os.path.isfile(bundled_candidate):
            return bundled_candidate

        # 3. Fallback to system PATH
        system_candidate = shutil.which(binary_name)
        if system_candidate:
            return system_candidate

        return binary_with_ext

    def _run_subproc(self, cmd_list: List[str], timeout: int = 15) -> Tuple[int, str, str]:
        """Runs a subprocess with hidden window flags on Windows and returns (returncode, stdout, stderr)."""
        startupinfo = None
        creationflags = 0
        if sys.platform.startswith("win"):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            creationflags = subprocess.CREATE_NO_WINDOW

        try:
            res = subprocess.run(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                startupinfo=startupinfo,
                creationflags=creationflags,
                timeout=timeout
            )
            return res.returncode, res.stdout.strip(), res.stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out."
        except Exception as e:
            return -1, "", str(e)

    def run_adb(self, args: List[str], device: Optional[str] = None, timeout: int = 15) -> Tuple[int, str, str]:
        """Executes an ADB command, targeting a specific device if specified or selected."""
        cmd = [self.adb_path]
        target = device or self.selected_device
        if target:
            cmd.extend(["-s", target])
        cmd.extend(args)
        return self._run_subproc(cmd, timeout=timeout)

    def run_fastboot(self, args: List[str], timeout: int = 20) -> Tuple[int, str, str]:
        """Executes a Fastboot command."""
        cmd = [self.fastboot_path]
        cmd.extend(args)
        return self._run_subproc(cmd, timeout=timeout)

    def stream_command(
        self,
        command: str,
        output_callback: Callable[[str], None],
        on_complete: Optional[Callable[[int], None]] = None,
        use_adb: bool = True
    ):
        """Streams command execution line-by-line in a background thread."""
        def worker():
            startupinfo = None
            creationflags = 0
            if sys.platform.startswith("win"):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                creationflags = subprocess.CREATE_NO_WINDOW

            if use_adb:
                target = self.selected_device
                prefix = f'"{self.adb_path}"'
                if target:
                    prefix += f' -s {target}'
                full_cmd = f"{prefix} {command}"
            else:
                full_cmd = command

            output_callback(f"[EXEC] > {command}\n")

            try:
                proc = subprocess.Popen(
                    full_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    startupinfo=startupinfo,
                    creationflags=creationflags
                )

                for line in iter(proc.stdout.readline, ""):
                    if line:
                        output_callback(line)

                proc.stdout.close()
                code = proc.wait()
                output_callback(f"\n[DONE] Process finished with exit code {code}.\n")
                if on_complete:
                    on_complete(code)
            except Exception as e:
                output_callback(f"\n[ERROR] Failed to run command: {e}\n")
                if on_complete:
                    on_complete(-1)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def get_connected_devices(self) -> List[Dict[str, str]]:
        """Scans for all ADB and Fastboot connected devices."""
        devices = []
        code, out, _ = self._run_subproc([self.adb_path, "devices", "-l"], timeout=5)
        if code == 0:
            lines = out.splitlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    serial = parts[0]
                    state = parts[1]
                    extra_info = " ".join(parts[2:])
                    model = "Unknown"
                    for item in parts[2:]:
                        if item.startswith("model:"):
                            model = item.split(":", 1)[1]
                    devices.append({
                        "serial": serial,
                        "state": state,
                        "mode": "adb",
                        "model": model,
                        "extra": extra_info
                    })

        # Also check fastboot
        fb_code, fb_out, _ = self._run_subproc([self.fastboot_path, "devices"], timeout=4)
        if fb_code == 0 and fb_out:
            for line in fb_out.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    serial = parts[0]
                    devices.append({
                        "serial": serial,
                        "state": "fastboot",
                        "mode": "fastboot",
                        "model": "Fastboot Mode",
                        "extra": "device in bootloader/fastboot"
                    })

        return devices

    def check_root(self, device: Optional[str] = None) -> Tuple[bool, str]:
        """Checks whether the connected device has functional su / root privilege."""
        code, out, err = self.run_adb(["shell", "su -c 'id'"], device=device, timeout=4)
        if code == 0 and "uid=0(root)" in out:
            return True, "Rooted (Superuser Active / uid=0)"
        
        # Secondary check: which su
        code2, out2, _ = self.run_adb(["shell", "which su"], device=device, timeout=3)
        if code2 == 0 and "/su" in out2:
            return False, "su binary present, but access denied or unprompted"

        return False, "Not Rooted / Standard User"

    def get_device_details(self, device: Optional[str] = None) -> Dict[str, str]:
        """Gathers rich device metadata including model, codename, HyperOS/MIUI version, battery, and screen."""
        details = {
            "model": "Unknown",
            "brand": "Unknown",
            "device": "Unknown",
            "android_version": "Unknown",
            "security_patch": "Unknown",
            "miui_version": "N/A (AOSP/Custom)",
            "battery_level": "Unknown",
            "battery_status": "Unknown",
            "screen_res": "Unknown",
            "refresh_rate": "Unknown",
            "is_rooted": "No"
        }

        # Query getprop batch
        props_cmd = "getprop ro.product.model; getprop ro.product.brand; getprop ro.product.device; getprop ro.build.version.release; getprop ro.build.version.security_patch; getprop ro.miui.ui.version.name; getprop ro.build.version.incremental"
        code, out, _ = self.run_adb(["shell", props_cmd], device=device, timeout=5)
        if code == 0:
            lines = [l.strip() for l in out.splitlines()]
            if len(lines) >= 1 and lines[0]: details["model"] = lines[0]
            if len(lines) >= 2 and lines[1]: details["brand"] = lines[1].capitalize()
            if len(lines) >= 3 and lines[2]: details["device"] = lines[2]
            if len(lines) >= 4 and lines[3]: details["android_version"] = lines[3]
            if len(lines) >= 5 and lines[4]: details["security_patch"] = lines[4]
            if len(lines) >= 6 and lines[5]: 
                details["miui_version"] = lines[5]
            elif len(lines) >= 7 and lines[6] and ("V816" in lines[6] or "OS" in lines[6]):
                details["miui_version"] = f"HyperOS ({lines[6]})"

        # Battery info
        b_code, b_out, _ = self.run_adb(["shell", "dumpsys battery"], device=device, timeout=4)
        if b_code == 0:
            for b_line in b_out.splitlines():
                b_line = b_line.strip()
                if b_line.startswith("level:"):
                    details["battery_level"] = f"{b_line.split(':')[1].strip()}%"
                elif b_line.startswith("status:"):
                    status_code = b_line.split(':')[1].strip()
                    status_map = {"2": "Charging ⚡", "3": "Discharging", "4": "Not Charging", "5": "Full 🔋"}
                    details["battery_status"] = status_map.get(status_code, "Normal")

        # Screen resolution & Refresh Rate
        wm_code, wm_out, _ = self.run_adb(["shell", "wm size"], device=device, timeout=3)
        if wm_code == 0 and "Physical size:" in wm_out:
            details["screen_res"] = wm_out.replace("Physical size:", "").strip()

        rr_code, rr_out, _ = self.run_adb(["shell", "dumpsys display | grep -E -m 1 'mRefreshrate|fps'"], device=device, timeout=4)
        if rr_code == 0 and rr_out:
            import re
            match = re.search(r"(\d{2,3}(?:\.\d+)?)fps", rr_out, re.IGNORECASE)
            if match:
                details["refresh_rate"] = f"{round(float(match.group(1)))} Hz"
            else:
                details["refresh_rate"] = "Dynamic"
        else:
            details["refresh_rate"] = "Dynamic"

        # Check root
        is_root, _ = self.check_root(device)
        details["is_rooted"] = "Yes (Superuser active)" if is_root else "No (Enforcing / Non-Root)"

        return details

    def add_device_listener(self, callback: Callable[[List[Dict[str, str]]], None]):
        """Registers a callback function that is invoked whenever device connection changes."""
        self._device_listeners.append(callback)

    def start_monitoring(self, interval: float = 2.5):
        """Starts a background monitor thread to notify listeners on device changes."""
        if self._monitoring:
            return
        self._monitoring = True

        def monitor_loop():
            while self._monitoring:
                try:
                    devices = self.get_connected_devices()
                    if devices != self._last_devices_cache:
                        self._last_devices_cache = devices
                        # If selected device is no longer connected, update
                        if self.selected_device:
                            serials = [d["serial"] for d in devices]
                            if self.selected_device not in serials:
                                self.selected_device = devices[0]["serial"] if devices else None
                        elif devices:
                            self.selected_device = devices[0]["serial"]

                        for listener in self._device_listeners:
                            try:
                                listener(devices)
                            except Exception:
                                pass
                except Exception:
                    pass
                time.sleep(interval)

        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self):
        """Stops the monitoring thread."""
        self._monitoring = False

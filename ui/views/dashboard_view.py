"""
HyperPulse Toolkit - Dashboard View
Displays real-time device status, system properties, root verification, and quick power actions.
"""

import customtkinter as ctk
from ui.styles import Theme
from core.presets import REBOOT_OPTIONS
import threading


class DashboardView(ctk.CTkScrollableFrame):
    def __init__(self, master, adb_manager, status_logger=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.adb = adb_manager
        self.logger = status_logger

        self._build_ui()

    def _build_ui(self):
        # 1. Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 15))

        title = ctk.CTkLabel(
            header,
            text="📱 Device Overview & Diagnostics",
            font=Theme.FONT_TITLE,
            text_color=Theme.TEXT_MAIN
        )
        title.pack(side="left")

        self.btn_refresh = ctk.CTkButton(
            header,
            text="🔄 Refresh Status",
            width=130,
            height=32,
            fg_color=Theme.CARD_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=self.refresh_device_info
        )
        self.btn_refresh.pack(side="right")

        # 2. Connection Status Banner
        self.banner = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        self.banner.pack(fill="x", padx=10, pady=(0, 15))

        self.status_icon = ctk.CTkLabel(self.banner, text="⚪", font=("Segoe UI", 24))
        self.status_icon.pack(side="left", padx=(18, 10), pady=16)

        banner_text_box = ctk.CTkFrame(self.banner, fg_color="transparent")
        banner_text_box.pack(side="left", fill="y", pady=12)

        self.lbl_device_title = ctk.CTkLabel(
            banner_text_box,
            text="Scanning for Connected Devices...",
            font=Theme.FONT_HEADING,
            text_color=Theme.TEXT_MAIN,
            anchor="w"
        )
        self.lbl_device_title.pack(anchor="w")

        self.lbl_device_subtitle = ctk.CTkLabel(
            banner_text_box,
            text="Connect your Android or Xiaomi device via USB cable with USB Debugging enabled.",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
            anchor="w"
        )
        self.lbl_device_subtitle.pack(anchor="w")

        # 3. Specs Info Card Grid
        self.info_grid = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        self.info_grid.pack(fill="x", padx=10, pady=(0, 15))

        grid_title = ctk.CTkLabel(
            self.info_grid,
            text="Hardware & System Telemetry",
            font=Theme.FONT_SUBHEAD,
            text_color=Theme.TEXT_MAIN
        )
        grid_title.pack(anchor="w", padx=15, pady=(12, 10))

        # Table rows container
        self.rows_frame = ctk.CTkFrame(self.info_grid, fg_color="transparent")
        self.rows_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.rows_frame.grid_columnconfigure((0, 1), weight=1)

        self.info_labels = {}
        fields = [
            ("Model / Brand", "lbl_model"),
            ("Device Codename", "lbl_codename"),
            ("Android Version", "lbl_android"),
            ("HyperOS / MIUI Version", "lbl_miui"),
            ("Security Patch", "lbl_patch"),
            ("Root / Superuser Status", "lbl_root"),
            ("Battery Level & State", "lbl_battery"),
            ("Display & Refresh Rate", "lbl_display"),
        ]

        for i, (label_text, key) in enumerate(fields):
            row = i // 2
            col = i % 2
            item_box = ctk.CTkFrame(self.rows_frame, fg_color=Theme.INPUT_BG, corner_radius=8)
            item_box.grid(row=row, column=col, padx=6, pady=5, sticky="ew")

            lbl_name = ctk.CTkLabel(item_box, text=label_text, font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED)
            lbl_name.pack(anchor="w", padx=10, pady=(6, 0))

            lbl_val = ctk.CTkLabel(item_box, text="--", font=Theme.FONT_BODY, text_color=Theme.TEXT_MAIN, anchor="w")
            lbl_val.pack(anchor="w", padx=10, pady=(0, 6))
            self.info_labels[key] = lbl_val

        # 4. Quick Power / Reboot Actions
        reboot_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        reboot_card.pack(fill="x", padx=10, pady=(0, 15))

        rb_title = ctk.CTkLabel(reboot_card, text="⚡ Quick Power Actions", font=Theme.FONT_SUBHEAD, text_color=Theme.TEXT_MAIN)
        rb_title.pack(anchor="w", padx=15, pady=(12, 8))

        btn_row = ctk.CTkFrame(reboot_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(0, 15))
        btn_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

        for idx, opt in enumerate(REBOOT_OPTIONS):
            btn = ctk.CTkButton(
                btn_row,
                text=opt["title"],
                font=Theme.FONT_SMALL,
                fg_color=Theme.INPUT_BG,
                hover_color=Theme.CARD_HOVER,
                border_width=1,
                border_color=Theme.BORDER_COLOR,
                command=lambda cmd=opt["command"]: self._execute_reboot(cmd)
            )
            btn.grid(row=0, column=idx, padx=4, pady=4, sticky="ew")

    def _execute_reboot(self, cmd_arg: str):
        if self.logger:
            self.logger(f"[ACTION] Triggering: adb {cmd_arg}...")
        self.adb.stream_command(cmd_arg, output_callback=self._log_output)

    def _log_output(self, text: str):
        if self.logger:
            self.logger(text)

    def refresh_device_info(self):
        def safe_dispatch(fn):
            try:
                self.after(0, fn)
            except Exception:
                pass

        def worker():
            devices = self.adb.get_connected_devices()
            if not devices:
                safe_dispatch(self._render_disconnected)
                return

            dev = devices[0]
            self.adb.selected_device = dev["serial"]

            if dev["state"] == "device":
                details = self.adb.get_device_details(dev["serial"])
                is_root, root_msg = self.adb.check_root(dev["serial"])
                safe_dispatch(lambda: self._render_connected(dev, details, is_root, root_msg))
            elif dev["state"] == "unauthorized":
                safe_dispatch(lambda: self._render_unauthorized(dev))
            elif dev["state"] == "fastboot":
                safe_dispatch(lambda: self._render_fastboot(dev))
            else:
                safe_dispatch(lambda: self._render_custom_state(dev))

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _render_disconnected(self):
        self.status_icon.configure(text="🔴")
        self.lbl_device_title.configure(text="No Device Detected", text_color=Theme.DANGER_RED)
        self.lbl_device_subtitle.configure(
            text="Please plug in your phone via USB and enable USB Debugging in Developer Options."
        )
        for key in self.info_labels:
            self.info_labels[key].configure(text="--", text_color=Theme.TEXT_MUTED)

    def _render_unauthorized(self, dev):
        self.status_icon.configure(text="🟡")
        self.lbl_device_title.configure(text=f"Device Unauthorized ({dev['serial']})", text_color=Theme.WARNING_AMBER)
        self.lbl_device_subtitle.configure(
            text="Check your phone screen and tap 'Always allow from this computer' on the USB Debugging prompt."
        )

    def _render_fastboot(self, dev):
        self.status_icon.configure(text="⚡")
        self.lbl_device_title.configure(text=f"Device in Fastboot Mode ({dev['serial']})", text_color=Theme.ACCENT_CYAN)
        self.lbl_device_subtitle.configure(text="Bootloader active. Ready for recovery or partition flashing.")
        self.info_labels["lbl_model"].configure(text="Fastboot Device", text_color=Theme.TEXT_MAIN)
        self.info_labels["lbl_codename"].configure(text="Bootloader", text_color=Theme.TEXT_MAIN)

    def _render_connected(self, dev, details, is_root, root_msg):
        self.status_icon.configure(text="🟢")
        self.lbl_device_title.configure(
            text=f"{details['brand']} {details['model']} (Connected)",
            text_color=Theme.SUCCESS_GREEN
        )
        self.lbl_device_subtitle.configure(
            text=f"Serial: {dev['serial']}  •  Mode: ADB Authorized  •  {root_msg}"
        )

        self.info_labels["lbl_model"].configure(text=f"{details['brand']} {details['model']}", text_color=Theme.TEXT_MAIN)
        self.info_labels["lbl_codename"].configure(text=details['device'], text_color=Theme.TEXT_MAIN)
        self.info_labels["lbl_android"].configure(text=f"Android {details['android_version']}", text_color=Theme.TEXT_MAIN)
        self.info_labels["lbl_miui"].configure(text=details['miui_version'], text_color=Theme.TEXT_MAIN)
        self.info_labels["lbl_patch"].configure(text=details['security_patch'], text_color=Theme.TEXT_MAIN)
        
        root_color = Theme.SUCCESS_GREEN if is_root else Theme.TEXT_MUTED
        self.info_labels["lbl_root"].configure(text=details['is_rooted'], text_color=root_color)
        
        batt_str = f"{details['battery_level']} ({details['battery_status']})"
        self.info_labels["lbl_battery"].configure(text=batt_str, text_color=Theme.TEXT_MAIN)
        self.info_labels["lbl_display"].configure(text=f"{details['screen_res']} @ {details['refresh_rate']}", text_color=Theme.TEXT_MAIN)

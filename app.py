"""
=============================================================================
HyperPulse Toolkit [Version 1.0.0 - V1]
Architected & Developed by Adrian (@stickshiftwillyy)
Target OS: Windows 10 / Windows 11 (64-bit Exclusive)

The ultimate ADB, debloater, and device telemetry utility for Xiaomi,
HyperOS, MIUI, and Android power users.
=============================================================================
"""

import os
import sys
from PIL import Image
import customtkinter as ctk
from ui.styles import Theme
from core.adb_manager import ADBManager
from ui.views.dashboard_view import DashboardView
from ui.views.presets_view import PresetsView
from ui.views.debloater_view import DebloaterView
from ui.views.terminal_view import TerminalView
from ui.views.tutorials_view import TutorialsView
from ui.views.settings_view import SettingsView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def get_asset_path(filename: str) -> str:
    """Resolves assets directory in dev or PyInstaller bundle."""
    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "assets", filename)


class HyperPulseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HyperPulse Toolkit - Xiaomi & Android Utility Studio")
        self.geometry("1060x720")
        self.minsize(980, 650)
        self.configure(fg_color=Theme.BG_DARK)

        # Initialize ADB Manager
        self.adb = ADBManager()

        # Navigation state
        self.views = {}
        self.nav_buttons = {}

        # Build UI
        self._build_sidebar()
        self._build_content_area()
        self._init_views()

        # Protocol for clean exit
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Show default view
        self.switch_view("dashboard")

        # Launch opening splash animation on pure black canvas
        self._show_opening_animation()

    def _show_opening_animation(self):
        """Displays a sleek, pure black opening splash animation before entering the app."""
        self.splash = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.splash.place(relx=0, rely=0, relwidth=1, relheight=1)

        center_box = ctk.CTkFrame(self.splash, fg_color="transparent")
        center_box.place(relx=0.5, rely=0.5, anchor="center")

        logo_path = get_asset_path("logo_white.png")
        if os.path.isfile(logo_path):
            img = Image.open(logo_path)
            # Original ratio ~3.48:1 -> display 360 x 103
            self.splash_logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(360, 103))
            lbl_logo = ctk.CTkLabel(center_box, image=self.splash_logo_img, text="")
            lbl_logo.pack(pady=(0, 24))
        else:
            lbl_logo = ctk.CTkLabel(
                center_box,
                text="HyperPulse\nBUILT BY STICKSHIFTWILLYY",
                font=("Segoe UI Variable Display", 26, "bold"),
                text_color="#ffffff"
            )
            lbl_logo.pack(pady=(0, 20))

        # Minimalist glowing electric progress bar
        self.splash_prog = ctk.CTkProgressBar(
            center_box,
            width=260,
            height=3,
            corner_radius=2,
            mode="indeterminate",
            fg_color="#141414",
            progress_color=Theme.ACCENT_CYAN
        )
        self.splash_prog.pack(pady=(0, 14))
        self.splash_prog.start()

        self.lbl_splash_status = ctk.CTkLabel(
            center_box,
            text="INITIALIZING SYSTEM ENGINES...",
            font=Theme.FONT_CODE,
            text_color=Theme.TEXT_MUTED
        )
        self.lbl_splash_status.pack()

        # Sequence of startup status updates
        self.after(500, lambda: self._update_splash_status("CALIBRATING ADB PROTOCOLS..."))
        self.after(1000, lambda: self._update_splash_status("STARTING TELEMETRY DAEMON..."))
        self.after(1500, lambda: self._update_splash_status("SYSTEM READY."))
        self.after(1900, self._dismiss_splash)

    def _update_splash_status(self, text: str):
        if hasattr(self, "lbl_splash_status") and self.lbl_splash_status.winfo_exists():
            self.lbl_splash_status.configure(text=text, text_color=Theme.ACCENT_CYAN)

    def _dismiss_splash(self):
        if hasattr(self, "splash") and self.splash.winfo_exists():
            self.splash.destroy()
        self._start_services()

    def _start_services(self):
        self.adb.add_device_listener(self._on_devices_changed)
        self.adb.start_monitoring(interval=2.5)
        if "dashboard" in self.views:
            self.views["dashboard"].refresh_device_info()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=Theme.SIDEBAR_BG, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Custom Logo in Top-Left
        logo_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_box.pack(fill="x", padx=12, pady=(16, 18))

        logo_path = get_asset_path("logo_white.png")
        if os.path.isfile(logo_path):
            img = Image.open(logo_path)
            # Size fit for 220px wide sidebar -> 180 x 51
            self.sidebar_logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(180, 51))
            lbl_logo = ctk.CTkLabel(logo_box, image=self.sidebar_logo_img, text="")
            lbl_logo.pack(anchor="center")
        else:
            lbl_logo = ctk.CTkLabel(
                logo_box,
                text="⚡ HyperPulse",
                font=Theme.FONT_TITLE,
                text_color=Theme.TEXT_MAIN,
                anchor="w"
            )
            lbl_logo.pack(anchor="w")

        # Nav Buttons Container
        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=10, pady=0)

        nav_items = [
            ("dashboard", "📱  Dashboard"),
            ("presets", "⚡  Presets Hub"),
            ("debloater", "🗑️  Debloater"),
            ("terminal", "💻  Live Terminal"),
            ("tutorials", "📚  Tutorials"),
            ("settings", "⚙️  Settings & Updates"),
        ]

        for key, label in nav_items:
            btn = ctk.CTkButton(
                self.nav_frame,
                text=label,
                font=Theme.FONT_BODY,
                height=38,
                fg_color="transparent",
                hover_color=Theme.CARD_HOVER,
                anchor="w",
                corner_radius=8,
                command=lambda k=key: self.switch_view(k)
            )
            btn.pack(fill="x", pady=3)
            self.nav_buttons[key] = btn

        # Bottom Connection Pill
        bottom_box = ctk.CTkFrame(self.sidebar, fg_color=Theme.CARD_BG, corner_radius=8, border_width=1, border_color=Theme.BORDER_COLOR)
        bottom_box.pack(side="bottom", fill="x", padx=12, pady=16)

        self.lbl_conn_status = ctk.CTkLabel(
            bottom_box,
            text="● Scanning...",
            font=Theme.FONT_SMALL,
            text_color=Theme.WARNING_AMBER
        )
        self.lbl_conn_status.pack(pady=8)

    def _build_content_area(self):
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=12, pady=(12, 6))

        # Main dynamic views container
        self.view_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True)

        # Persistent Footer Bar with Developer Signature
        self.footer_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=24)
        self.footer_bar.pack(fill="x", side="bottom", pady=(4, 0))

        self.lbl_credit = ctk.CTkLabel(
            self.footer_bar,
            text="⚡ Developed by stickshiftwillyy (Adrian)",
            font=Theme.FONT_DEV,
            text_color=Theme.ACCENT_CYAN,
            anchor="e"
        )
        self.lbl_credit.pack(side="right", padx=10)

    def _init_views(self):
        # Global terminal logging hook
        def log_to_terminal(msg: str):
            if "terminal" in self.views:
                self.views["terminal"].append_log(msg if msg.endswith("\n") else f"{msg}\n")

        self.views["dashboard"] = DashboardView(self.view_container, self.adb, status_logger=log_to_terminal)
        self.views["presets"] = PresetsView(self.view_container, self.adb, status_logger=log_to_terminal)
        self.views["debloater"] = DebloaterView(self.view_container, self.adb, status_logger=log_to_terminal)
        self.views["terminal"] = TerminalView(self.view_container, self.adb)
        self.views["tutorials"] = TutorialsView(self.view_container, status_logger=log_to_terminal)
        self.views["settings"] = SettingsView(self.view_container, self.adb, status_logger=log_to_terminal)

    def switch_view(self, view_key: str):
        # Update nav button highlights
        for key, btn in self.nav_buttons.items():
            if key == view_key:
                btn.configure(fg_color=Theme.CARD_BG, text_color=Theme.ACCENT_CYAN)
            else:
                btn.configure(fg_color="transparent", text_color=Theme.TEXT_MAIN)

        # Hide all views and display the selected one
        for v in self.views.values():
            v.pack_forget()

        if view_key in self.views:
            self.views[view_key].pack(fill="both", expand=True)

    def _on_devices_changed(self, devices):
        def _update():
            if not devices:
                self.lbl_conn_status.configure(text="● No Device", text_color=Theme.DANGER_RED)
            else:
                dev = devices[0]
                if dev["state"] == "device":
                    self.lbl_conn_status.configure(text=f"● {dev['serial']}", text_color=Theme.SUCCESS_GREEN)
                elif dev["state"] == "unauthorized":
                    self.lbl_conn_status.configure(text=f"● Unauthorized", text_color=Theme.WARNING_AMBER)
                elif dev["state"] == "fastboot":
                    self.lbl_conn_status.configure(text="● Fastboot Mode", text_color=Theme.ACCENT_CYAN)
                else:
                    self.lbl_conn_status.configure(text=f"● {dev['state']}", text_color=Theme.TEXT_MUTED)

            if "dashboard" in self.views:
                self.views["dashboard"].refresh_device_info()

        try:
            self.after(0, _update)
        except Exception:
            pass

    def _on_close(self):
        self.adb.stop_monitoring()
        self.destroy()


if __name__ == "__main__":
    app = HyperPulseApp()
    app.mainloop()

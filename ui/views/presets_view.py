"""
HyperPulse Toolkit - Presets View
One-click optimization hub for gaming, display smoothness, Shizuku starter, and Xiaomi services.
"""

import customtkinter as ctk
from ui.styles import Theme
from core.presets import PRESETS
import threading


class PresetsView(ctk.CTkScrollableFrame):
    def __init__(self, master, adb_manager, status_logger=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.adb = adb_manager
        self.logger = status_logger

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 15))

        title = ctk.CTkLabel(
            header,
            text="⚡ One-Click Optimization Presets",
            font=Theme.FONT_TITLE,
            text_color=Theme.TEXT_MAIN
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Curated ADB tweaks tested for Xiaomi, HyperOS, MIUI, and standard Android devices.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Cards Container
        for item in PRESETS:
            self._create_preset_card(item)

    def _create_preset_card(self, preset):
        card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        card.pack(fill="x", padx=10, pady=(0, 12))

        # Top line: Title & Badge
        top_bar = ctk.CTkFrame(card, fg_color="transparent")
        top_bar.pack(fill="x", padx=15, pady=(12, 4))

        lbl_title = ctk.CTkLabel(top_bar, text=preset["title"], font=Theme.FONT_HEADING, text_color=Theme.TEXT_MAIN)
        lbl_title.pack(side="left")

        lbl_badge = ctk.CTkLabel(
            top_bar,
            text=f" {preset['badge']} ",
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            corner_radius=6,
            text_color=Theme.ACCENT_CYAN
        )
        lbl_badge.pack(side="right")

        # Description
        lbl_desc = ctk.CTkLabel(
            card,
            text=preset["description"],
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
            justify="left",
            wraplength=620,
            anchor="w"
        )
        lbl_desc.pack(fill="x", padx=15, pady=(2, 10))

        # Action Buttons row
        action_bar = ctk.CTkFrame(card, fg_color="transparent")
        action_bar.pack(fill="x", padx=15, pady=(0, 12))

        lbl_status = ctk.CTkLabel(action_bar, text="", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED)
        lbl_status.pack(side="left")

        # Revert button if available
        if preset.get("restore_commands"):
            btn_restore = ctk.CTkButton(
                action_bar,
                text="Revert to Default",
                width=130,
                height=30,
                font=Theme.FONT_SMALL,
                fg_color=Theme.INPUT_BG,
                hover_color=Theme.CARD_HOVER,
                border_width=1,
                border_color=Theme.BORDER_COLOR,
                command=lambda p=preset, s=lbl_status: self._run_commands(p["restore_commands"], s, "Reverted successfully!")
            )
            btn_restore.pack(side="right", padx=(8, 0))

        # Apply button
        btn_apply = ctk.CTkButton(
            action_bar,
            text="Apply Preset",
            width=120,
            height=30,
            font=Theme.FONT_SMALL,
            fg_color=Theme.ACCENT_BLUE,
            hover_color=Theme.ACCENT_HOVER,
            command=lambda p=preset, s=lbl_status: self._run_commands(p["commands"], s, "Applied successfully!")
        )
        btn_apply.pack(side="right")

    def _run_commands(self, cmd_list, status_label, success_msg):
        status_label.configure(text="Executing...", text_color=Theme.WARNING_AMBER)
        
        def worker():
            overall_success = True
            for cmd_str in cmd_list:
                if self.logger:
                    self.logger(f"[PRESET] > adb {cmd_str}")
                parts = cmd_str.split()
                code, out, err = self.adb.run_adb(parts)
                if self.logger:
                    if out: self.logger(out)
                    if err: self.logger(f"Error: {err}")
                if code != 0:
                    overall_success = False

            if overall_success:
                self.after(0, lambda: status_label.configure(text=f"✓ {success_msg}", text_color=Theme.SUCCESS_GREEN))
            else:
                self.after(0, lambda: status_label.configure(text="⚠️ Command had warnings/errors", text_color=Theme.WARNING_AMBER))

            # Reset status text after 4 seconds
            self.after(4000, lambda: status_label.configure(text=""))

        t = threading.Thread(target=worker, daemon=True)
        t.start()

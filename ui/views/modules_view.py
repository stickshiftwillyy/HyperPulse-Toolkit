"""
=============================================================================
HyperPulse Toolkit - Magisk & KernelSU Module Hub [V1.1]
Developed & Designed by Adrian (@stickshiftwillyy)
Target OS: Windows 10 / Windows 11 (64-bit)

Curated 1-click root modules and custom .zip module injection engine.
Supports Magisk, KernelSU, and APatch over ADB.
=============================================================================
"""

import os
import urllib.request
import threading
from tkinter import filedialog
import customtkinter as ctk
from ui.styles import Theme
from core.modules_catalog import MODULES_CATALOG, detect_root_type, inject_module_file


class ModulesView(ctk.CTkScrollableFrame):
    def __init__(self, master, adb_manager, status_logger=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.adb = adb_manager
        self.logger = status_logger

        self.selected_module_path = None
        self._build_ui()
        self.refresh_root_status()

    def _build_ui(self):
        # 1. Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 12))

        title = ctk.CTkLabel(
            header,
            text="🧩 Magisk & KernelSU Module Hub",
            font=Theme.FONT_TITLE,
            text_color=Theme.TEXT_MAIN
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Curated essential root modules & 1-click ADB injection for Magisk, KernelSU, and APatch.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # 2. Root Status Banner
        self.banner = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        self.banner.pack(fill="x", padx=10, pady=(0, 12))

        b_content = ctk.CTkFrame(self.banner, fg_color="transparent")
        b_content.pack(fill="x", padx=15, pady=12)

        self.lbl_root_icon = ctk.CTkLabel(b_content, text="⚡", font=("Segoe UI", 20))
        self.lbl_root_icon.pack(side="left", padx=(0, 10))

        b_text_box = ctk.CTkFrame(b_content, fg_color="transparent")
        b_text_box.pack(side="left", fill="both", expand=True)

        self.lbl_root_status = ctk.CTkLabel(
            b_text_box,
            text="Checking Root Environment...",
            font=Theme.FONT_SUBHEAD,
            text_color=Theme.TEXT_MAIN,
            anchor="w"
        )
        self.lbl_root_status.pack(anchor="w")

        self.lbl_root_desc = ctk.CTkLabel(
            b_text_box,
            text="Verifying Magisk, KernelSU, or APatch presence over ADB shell.",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
            anchor="w"
        )
        self.lbl_root_desc.pack(anchor="w")

        btn_refresh_root = ctk.CTkButton(
            b_content,
            text="🔄 Re-Check",
            width=90,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=self.refresh_root_status
        )
        btn_refresh_root.pack(side="right")

        # 3. Custom Module Drag & Drop / File Picker Card
        custom_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        custom_card.pack(fill="x", padx=10, pady=(0, 14))

        c_top = ctk.CTkFrame(custom_card, fg_color="transparent")
        c_top.pack(fill="x", padx=15, pady=(12, 6))

        lbl_c_title = ctk.CTkLabel(c_top, text="📥 Inject Your Own Module (.zip)", font=Theme.FONT_HEADING, text_color=Theme.TEXT_MAIN)
        lbl_c_title.pack(side="left")

        btn_browse_mod = ctk.CTkButton(
            c_top,
            text="Select .zip Module...",
            width=140,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.ACCENT_BLUE,
            hover_color=Theme.ACCENT_HOVER,
            command=self._on_browse_module
        )
        btn_browse_mod.pack(side="right")

        self.lbl_selected_mod = ctk.CTkLabel(
            custom_card,
            text="Select any Magisk/KernelSU module .zip from your PC to inject directly over ADB.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
            anchor="w"
        )
        self.lbl_selected_mod.pack(fill="x", padx=15, pady=(2, 10))

        c_action_bar = ctk.CTkFrame(custom_card, fg_color="transparent")
        c_action_bar.pack(fill="x", padx=15, pady=(0, 12))

        self.lbl_inject_status = ctk.CTkLabel(c_action_bar, text="", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED)
        self.lbl_inject_status.pack(side="left")

        self.btn_inject_custom = ctk.CTkButton(
            c_action_bar,
            text="⚡ Inject to Phone",
            width=150,
            height=30,
            font=Theme.FONT_SUBHEAD,
            fg_color=Theme.SUCCESS_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            state="disabled",
            command=self._on_inject_custom
        )
        self.btn_inject_custom.pack(side="right")

        # 4. Curated Presets Section Title
        sec_header = ctk.CTkFrame(self, fg_color="transparent")
        sec_header.pack(fill="x", padx=10, pady=(4, 8))

        lbl_sec = ctk.CTkLabel(
            sec_header,
            text="🌟 Curated Root Modules (1-Click Download & Inject)",
            font=Theme.FONT_SUBHEAD,
            text_color=Theme.TEXT_MAIN
        )
        lbl_sec.pack(anchor="w")

        # 5. Modules List
        for mod in MODULES_CATALOG:
            self._create_module_card(mod)

    def _create_module_card(self, mod):
        card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        card.pack(fill="x", padx=10, pady=(0, 10))

        top_line = ctk.CTkFrame(card, fg_color="transparent")
        top_line.pack(fill="x", padx=15, pady=(10, 4))

        lbl_name = ctk.CTkLabel(top_line, text=mod["name"], font=Theme.FONT_HEADING, text_color=Theme.TEXT_MAIN)
        lbl_name.pack(side="left")

        lbl_author = ctk.CTkLabel(top_line, text=f"by {mod['author']}", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED)
        lbl_author.pack(side="left", padx=8)

        lbl_badge = ctk.CTkLabel(
            top_line,
            text=f" {mod['badge']} ",
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            corner_radius=6,
            text_color=Theme.ACCENT_CYAN
        )
        lbl_badge.pack(side="right")

        lbl_desc = ctk.CTkLabel(
            card,
            text=mod["desc"],
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
            justify="left",
            wraplength=620,
            anchor="w"
        )
        lbl_desc.pack(fill="x", padx=15, pady=(0, 8))

        action_line = ctk.CTkFrame(card, fg_color="transparent")
        action_line.pack(fill="x", padx=15, pady=(0, 10))

        lbl_status = ctk.CTkLabel(action_line, text="", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED)
        lbl_status.pack(side="left")

        btn_install = ctk.CTkButton(
            action_line,
            text="Download & Inject",
            width=140,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.ACCENT_BLUE,
            hover_color=Theme.ACCENT_HOVER,
            command=lambda m=mod, s=lbl_status: self._download_and_inject_curated(m, s)
        )
        btn_install.pack(side="right")

    def refresh_root_status(self):
        def worker():
            root_type, is_root = detect_root_type(self.adb)
            def update_ui():
                if is_root:
                    self.lbl_root_icon.configure(text="🟢")
                    self.lbl_root_status.configure(text=f"Root Active: {root_type}", text_color=Theme.SUCCESS_GREEN)
                    self.lbl_root_desc.configure(text="Elevated permissions active. Direct module injection is ready.")
                else:
                    self.lbl_root_icon.configure(text="🟡")
                    self.lbl_root_status.configure(text="Non-Root / Unrooted Mode", text_color=Theme.WARNING_AMBER)
                    self.lbl_root_desc.configure(text="Modules injected will be saved to '/sdcard/Download/HyperPulse/' for recovery installation.")
            try:
                self.after(0, update_ui)
            except Exception:
                pass

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _on_browse_module(self):
        path = filedialog.askopenfilename(
            title="Select Magisk / KernelSU Module",
            filetypes=[("Magisk/KernelSU Module Zip", "*.zip"), ("All Files", "*.*")]
        )
        if path:
            self.selected_module_path = path
            self.lbl_selected_mod.configure(text=f"Selected: {path}", text_color=Theme.TEXT_MAIN)
            self.btn_inject_custom.configure(state="normal")

    def _on_inject_custom(self):
        if not self.selected_module_path:
            return

        self.btn_inject_custom.configure(state="disabled", text="Injecting...")
        self.lbl_inject_status.configure(text="Starting injection...", text_color=Theme.ACCENT_CYAN)

        def worker():
            def cb(msg):
                if self.logger:
                    self.logger(f"[MODULE] {msg}")
                try:
                    self.after(0, lambda m=msg: self.lbl_inject_status.configure(text=m, text_color=Theme.TEXT_MAIN))
                except Exception:
                    pass

            inject_module_file(self.adb, self.selected_module_path, status_callback=cb)
            try:
                self.after(0, lambda: self.btn_inject_custom.configure(state="normal", text="⚡ Inject to Phone"))
            except Exception:
                pass

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _download_and_inject_curated(self, mod, status_lbl):
        status_lbl.configure(text="Downloading module...", text_color=Theme.WARNING_AMBER)

        def worker():
            cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "cache")
            os.makedirs(cache_dir, exist_ok=True)
            local_path = os.path.join(cache_dir, mod["filename"])

            try:
                if self.logger:
                    self.logger(f"[MODULE] Fetching: {mod['download_url']}...")
                req = urllib.request.Request(mod["download_url"], headers={"User-Agent": "HyperPulse-Toolkit"})
                with urllib.request.urlopen(req, timeout=20) as response, open(local_path, "wb") as out_file:
                    out_file.write(response.read())

                def cb(msg):
                    if self.logger:
                        self.logger(f"[MODULE] {msg}")
                    try:
                        self.after(0, lambda m=msg: status_lbl.configure(text=m, text_color=Theme.ACCENT_CYAN))
                    except Exception:
                        pass

                inject_module_file(self.adb, local_path, status_callback=cb)
            except Exception as e:
                err_str = f"Download failed: {str(e)[:40]}"
                if self.logger:
                    self.logger(f"[MODULE] {err_str}")
                try:
                    self.after(0, lambda: status_lbl.configure(text=err_str, text_color=Theme.DANGER_RED))
                except Exception:
                    pass

        t = threading.Thread(target=worker, daemon=True)
        t.start()

"""
HyperPulse Toolkit - Settings & Updates View
Allows the repository author and users to configure GitHub auto-updates, verify ADB binaries,
and inspect changelogs.
"""

import customtkinter as ctk
import webbrowser
from ui.styles import Theme
from core.updater import CURRENT_VERSION, load_update_config, save_update_config, check_for_updates
import threading


class SettingsView(ctk.CTkScrollableFrame):
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
            text="⚙️ App Settings & In-App Updates",
            font=Theme.FONT_TITLE,
            text_color=Theme.TEXT_MAIN
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text=f"HyperPulse Toolkit v{CURRENT_VERSION}  •  Developed by stickshiftwillyy (Adrian)",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # 2. Remote GitHub In-App Updater Card
        upd_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        upd_card.pack(fill="x", padx=10, pady=(0, 15))

        upd_top = ctk.CTkFrame(upd_card, fg_color="transparent")
        upd_top.pack(fill="x", padx=15, pady=(12, 6))

        lbl_upd_title = ctk.CTkLabel(upd_top, text="🚀 Remote GitHub In-App Updater", font=Theme.FONT_HEADING, text_color=Theme.TEXT_MAIN)
        lbl_upd_title.pack(side="left")

        self.btn_check_update = ctk.CTkButton(
            upd_top,
            text="Check for Updates",
            width=140,
            height=30,
            font=Theme.FONT_SMALL,
            fg_color=Theme.ACCENT_BLUE,
            hover_color=Theme.ACCENT_HOVER,
            command=self._on_check_updates
        )
        self.btn_check_update.pack(side="right")

        # Configuration Form
        cfg = load_update_config()
        form_box = ctk.CTkFrame(upd_card, fg_color=Theme.INPUT_BG, corner_radius=8)
        form_box.pack(fill="x", padx=15, pady=(6, 12))

        lbl_desc = ctk.CTkLabel(
            form_box,
            text="Connect this app directly to your personal GitHub repository so your users receive update alerts automatically:",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
            anchor="w"
        )
        lbl_desc.pack(fill="x", padx=12, pady=(10, 8))

        row_inputs = ctk.CTkFrame(form_box, fg_color="transparent")
        row_inputs.pack(fill="x", padx=12, pady=(0, 10))

        # GitHub User
        lbl_user = ctk.CTkLabel(row_inputs, text="GitHub User:", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MAIN)
        lbl_user.pack(side="left", padx=(0, 6))

        self.entry_user = ctk.CTkEntry(row_inputs, width=160, font=Theme.FONT_CODE, height=28)
        self.entry_user.insert(0, cfg.get("github_user", ""))
        self.entry_user.pack(side="left", padx=(0, 15))

        # GitHub Repo
        lbl_repo = ctk.CTkLabel(row_inputs, text="Repo Name:", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MAIN)
        lbl_repo.pack(side="left", padx=(0, 6))

        self.entry_repo = ctk.CTkEntry(row_inputs, width=180, font=Theme.FONT_CODE, height=28)
        self.entry_repo.insert(0, cfg.get("github_repo", ""))
        self.entry_repo.pack(side="left", padx=(0, 15))

        btn_save = ctk.CTkButton(
            row_inputs,
            text="Save Repo",
            width=90,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.CARD_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=self._save_repo_settings
        )
        btn_save.pack(side="right")

        # Update Status Box
        self.status_box = ctk.CTkFrame(upd_card, fg_color=Theme.INPUT_BG, corner_radius=8)
        self.status_box.pack(fill="x", padx=15, pady=(0, 15))

        self.lbl_update_status = ctk.CTkLabel(
            self.status_box,
            text=f"Current version installed: v{CURRENT_VERSION}. Click 'Check for Updates' to verify.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MAIN,
            anchor="w"
        )
        self.lbl_update_status.pack(fill="x", padx=12, pady=10)

        # 3. How to Push Updates Guide for the Author
        guide_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        guide_card.pack(fill="x", padx=10, pady=(0, 15))

        g_title = ctk.CTkLabel(guide_card, text="💡 How to Push Updates to Your Users (Author Guide)", font=Theme.FONT_SUBHEAD, text_color=Theme.TEXT_MAIN)
        g_title.pack(anchor="w", padx=15, pady=(12, 6))

        author_guide_text = (
            "1. When you make changes to the app or add new presets, open `version.json` in your repository root.\n"
            "2. Bump the `version` field (e.g. from '1.0.0' to '1.0.1') and write your release notes in `changelog`.\n"
            "3. Commit and push `version.json` to your GitHub `main` branch.\n"
            "4. That's it! When anyone opens HyperPulse Toolkit or clicks 'Check for Updates', the app fetches "
            "your raw `version.json` and notifies them of your new release!"
        )
        lbl_author_guide = ctk.CTkLabel(
            guide_card,
            text=author_guide_text,
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
            justify="left",
            wraplength=640
        )
        lbl_author_guide.pack(anchor="w", padx=15, pady=(0, 15))

        # 4. ADB Binary Diagnostics & Server Restart
        diag_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        diag_card.pack(fill="x", padx=10, pady=(0, 15))

        d_title = ctk.CTkLabel(diag_card, text="🔧 ADB Environment Diagnostics", font=Theme.FONT_SUBHEAD, text_color=Theme.TEXT_MAIN)
        d_title.pack(anchor="w", padx=15, pady=(12, 6))

        lbl_adb_path = ctk.CTkLabel(
            diag_card,
            text=f"Active ADB Binary: {self.adb.adb_path}\nActive Fastboot Binary: {self.adb.fastboot_path}",
            font=Theme.FONT_CODE,
            text_color=Theme.ACCENT_CYAN,
            justify="left",
            anchor="w"
        )
        lbl_adb_path.pack(fill="x", padx=15, pady=(0, 10))

        btn_restart_adb = ctk.CTkButton(
            diag_card,
            text="Restart ADB Server (Kill & Restart)",
            width=220,
            height=30,
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=self._restart_adb_server
        )
        btn_restart_adb.pack(anchor="w", padx=15, pady=(0, 15))

    def _save_repo_settings(self):
        user = self.entry_user.get().strip()
        repo = self.entry_repo.get().strip()
        save_update_config(user, repo)
        self.lbl_update_status.configure(text=f"✓ Configuration saved! Pointed to GitHub: {user}/{repo}", text_color=Theme.SUCCESS_GREEN)

    def _on_check_updates(self):
        self.btn_check_update.configure(text="Checking...", state="disabled")
        
        def worker():
            user = self.entry_user.get().strip()
            repo = self.entry_repo.get().strip()
            raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/main/version.json" if user and repo else None
            
            res = check_for_updates(custom_raw_url=raw_url)
            self.after(0, lambda: self._render_update_result(res))

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _render_update_result(self, res):
        self.btn_check_update.configure(text="Check for Updates", state="normal")
        if res.get("has_update"):
            text = f"🎉 New Update Available: v{res['remote_version']}!\nChangelog: {res['release_notes']}"
            self.lbl_update_status.configure(text=text, text_color=Theme.ACCENT_CYAN)
        elif res.get("success"):
            self.lbl_update_status.configure(text=f"✓ You are running the latest version (v{CURRENT_VERSION}).", text_color=Theme.SUCCESS_GREEN)
        else:
            self.lbl_update_status.configure(text=f"ℹ️ {res['status_message']}", text_color=Theme.WARNING_AMBER)

    def _restart_adb_server(self):
        if self.logger:
            self.logger("[ADB] Restarting ADB server...")
        self.adb.run_adb(["kill-server"])
        self.adb.run_adb(["start-server"])
        if self.logger:
            self.logger("[ADB] ADB server restarted successfully.")

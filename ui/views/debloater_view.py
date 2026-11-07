"""
HyperPulse Toolkit - Debloater View
A built-in Canta-style package debloater with safety ratings, multi-selection, and restore capabilities.
"""

import customtkinter as ctk
from ui.styles import Theme
from core.debloat_db import DEBLOAT_CATALOG, get_installed_packages, get_active_installed_packages
import threading


class DebloaterView(ctk.CTkFrame):
    def __init__(self, master, adb_manager, status_logger=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.adb = adb_manager
        self.logger = status_logger

        self.installed_packages = set()
        self.active_packages = set()
        self.package_checkboxes = {}
        self.package_vars = {}

        self._build_ui()

    def _build_ui(self):
        # 1. Header & Controls
        top_box = ctk.CTkFrame(self, fg_color="transparent")
        top_box.pack(fill="x", padx=10, pady=(5, 10))

        title = ctk.CTkLabel(
            top_box,
            text="🗑️ Canta-Style Xiaomi & Android Debloater",
            font=Theme.FONT_TITLE,
            text_color=Theme.TEXT_MAIN
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            top_box,
            text="Safely uninstall Xiaomi bloatware, tracking daemons, and preloaded apps without bricking.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(2, 8))

        # Toolbar Card
        toolbar = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        toolbar.pack(fill="x", padx=10, pady=(0, 10))

        tool_row1 = ctk.CTkFrame(toolbar, fg_color="transparent")
        tool_row1.pack(fill="x", padx=12, pady=(10, 6))

        # Search box
        self.search_entry = ctk.CTkEntry(
            tool_row1,
            placeholder_text="🔍 Search package name or app title...",
            font=Theme.FONT_BODY,
            fg_color=Theme.INPUT_BG,
            border_color=Theme.BORDER_COLOR,
            height=32
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self._filter_display())

        # Scan button
        self.btn_scan = ctk.CTkButton(
            tool_row1,
            text="📡 Scan Device",
            width=120,
            height=32,
            fg_color=Theme.ACCENT_BLUE,
            hover_color=Theme.ACCENT_HOVER,
            command=self.scan_device_packages
        )
        self.btn_scan.pack(side="right")

        # Tool row 2: Filter buttons & Selection
        tool_row2 = ctk.CTkFrame(toolbar, fg_color="transparent")
        tool_row2.pack(fill="x", padx=12, pady=(0, 10))

        self.filter_var = ctk.StringVar(value="Safe")
        for f_label in ["Safe", "Caution", "All Catalog"]:
            rb = ctk.CTkRadioButton(
                tool_row2,
                text=f_label,
                value=f_label,
                variable=self.filter_var,
                command=self._filter_display,
                font=Theme.FONT_SMALL,
                text_color=Theme.TEXT_MAIN
            )
            rb.pack(side="left", padx=(0, 15))

        self.btn_select_safe = ctk.CTkButton(
            tool_row2,
            text="Select Safe Only",
            width=115,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=self._select_all_safe
        )
        self.btn_select_safe.pack(side="left", padx=(5, 5))

        self.btn_deselect_all = ctk.CTkButton(
            tool_row2,
            text="Deselect All",
            width=90,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=self._deselect_all
        )
        self.btn_deselect_all.pack(side="left")

        # Action Buttons (Uninstall / Restore)
        self.btn_uninstall = ctk.CTkButton(
            tool_row2,
            text="Uninstall Selected",
            width=135,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.DANGER_RED,
            hover_color=Theme.DANGER_HOVER,
            command=self._uninstall_selected
        )
        self.btn_uninstall.pack(side="right")

        self.btn_restore = ctk.CTkButton(
            tool_row2,
            text="Restore Selected",
            width=125,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.SUCCESS_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            command=self._restore_selected
        )
        self.btn_restore.pack(side="right", padx=(0, 8))

        # 2. Packages Scroll Area
        self.scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        # 3. Custom Package Manual Bar
        manual_bar = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=8, border_width=1, border_color=Theme.BORDER_COLOR)
        manual_bar.pack(fill="x", padx=10, pady=(5, 5))

        lbl_manual = ctk.CTkLabel(manual_bar, text="Manual Package:", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED)
        lbl_manual.pack(side="left", padx=(12, 8), pady=8)

        self.manual_pkg_entry = ctk.CTkEntry(
            manual_bar,
            placeholder_text="com.example.package",
            font=Theme.FONT_CODE,
            fg_color=Theme.INPUT_BG,
            border_color=Theme.BORDER_COLOR,
            height=28
        )
        self.manual_pkg_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=8)

        btn_manual_un = ctk.CTkButton(
            manual_bar,
            text="Uninstall",
            width=80,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.DANGER_RED,
            hover_color=Theme.DANGER_HOVER,
            command=lambda: self._manual_action("uninstall")
        )
        btn_manual_un.pack(side="right", padx=(0, 10), pady=8)

        btn_manual_res = ctk.CTkButton(
            manual_bar,
            text="Restore",
            width=80,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.SUCCESS_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            command=lambda: self._manual_action("restore")
        )
        btn_manual_res.pack(side="right", padx=(0, 6), pady=8)

        # Initial populate
        self._populate_list(DEBLOAT_CATALOG)

    def scan_device_packages(self):
        self.btn_scan.configure(text="Scanning...", state="disabled")

        def worker():
            active = get_active_installed_packages(self.adb)
            all_pkgs = get_installed_packages(self.adb)

            self.active_packages = active
            self.installed_packages = all_pkgs

            self.after(0, self._on_scan_completed)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _on_scan_completed(self):
        self.btn_scan.configure(text="📡 Scan Device", state="normal")
        if self.logger:
            self.logger(f"[DEBLOATER] Scan complete: Found {len(self.active_packages)} active packages.")
        self._filter_display()

    def _populate_list(self, catalog_items):
        for widget in self.scroll_area.winfo_children():
            widget.destroy()

        self.package_checkboxes.clear()
        self.package_vars.clear()

        for item in catalog_items:
            pkg = item["package"]
            level = item["level"]
            is_active = pkg in self.active_packages if self.active_packages else True

            row = ctk.CTkFrame(self.scroll_area, fg_color=Theme.CARD_BG, corner_radius=8, border_width=1, border_color=Theme.BORDER_COLOR)
            row.pack(fill="x", pady=3)

            # Left checkbox
            var = ctk.BooleanVar(value=False)
            self.package_vars[pkg] = var
            chk = ctk.CTkCheckBox(row, text="", variable=var, width=24)
            chk.pack(side="left", padx=(10, 6), pady=8)
            self.package_checkboxes[pkg] = (chk, item)

            # Center Info
            center = ctk.CTkFrame(row, fg_color="transparent")
            center.pack(side="left", fill="both", expand=True, pady=6)

            title_row = ctk.CTkFrame(center, fg_color="transparent")
            title_row.pack(fill="x")

            lbl_name = ctk.CTkLabel(title_row, text=item["name"], font=Theme.FONT_SUBHEAD, text_color=Theme.TEXT_MAIN)
            lbl_name.pack(side="left")

            lbl_pkg = ctk.CTkLabel(title_row, text=f"({pkg})", font=Theme.FONT_CODE, text_color=Theme.TEXT_MUTED)
            lbl_pkg.pack(side="left", padx=8)

            lbl_desc = ctk.CTkLabel(center, text=item["desc"], font=Theme.FONT_SMALL, text_color=Theme.TEXT_DIM, anchor="w")
            lbl_desc.pack(anchor="w")

            # Right Badges
            right = ctk.CTkFrame(row, fg_color="transparent")
            right.pack(side="right", padx=10, pady=8)

            level_colors = {
                "Safe": Theme.SUCCESS_GREEN,
                "Caution": Theme.WARNING_AMBER,
                "Danger": Theme.DANGER_RED
            }
            lbl_level = ctk.CTkLabel(
                right,
                text=f" {level} ",
                font=Theme.FONT_SMALL,
                fg_color=Theme.INPUT_BG,
                text_color=level_colors.get(level, Theme.TEXT_MUTED),
                corner_radius=4
            )
            lbl_level.pack(side="right", padx=(5, 0))

            # Status pill (Installed / Uninstalled)
            if self.active_packages:
                status_text = "Installed" if is_active else "Removed"
                status_color = Theme.ACCENT_CYAN if is_active else Theme.TEXT_DIM
                lbl_status = ctk.CTkLabel(
                    right,
                    text=f" {status_text} ",
                    font=Theme.FONT_SMALL,
                    fg_color=Theme.INPUT_BG,
                    text_color=status_color,
                    corner_radius=4
                )
                lbl_status.pack(side="right")

    def _filter_display(self):
        query = self.search_entry.get().strip().lower()
        filter_mode = self.filter_var.get()

        filtered = []
        for item in DEBLOAT_CATALOG:
            # Filter level
            if filter_mode == "Safe" and item["level"] != "Safe":
                continue
            if filter_mode == "Caution" and item["level"] not in ("Safe", "Caution"):
                continue

            # Query filter
            if query:
                in_name = query in item["name"].lower()
                in_pkg = query in item["package"].lower()
                in_desc = query in item["desc"].lower()
                if not (in_name or in_pkg or in_desc):
                    continue

            filtered.append(item)

        self._populate_list(filtered)

    def _select_all_safe(self):
        for pkg, (chk, item) in self.package_checkboxes.items():
            if item["level"] == "Safe":
                self.package_vars[pkg].set(True)
            else:
                self.package_vars[pkg].set(False)

    def _deselect_all(self):
        for var in self.package_vars.values():
            var.set(False)

    def _uninstall_selected(self):
        selected = [pkg for pkg, var in self.package_vars.items() if var.get()]
        if not selected:
            return

        def worker():
            for pkg in selected:
                if self.logger:
                    self.logger(f"[DEBLOATER] Uninstalling {pkg}...")
                code, out, err = self.adb.run_adb(["shell", f"pm uninstall -k --user 0 {pkg}"])
                if self.logger:
                    self.logger(out if out else err)
            self.after(0, self.scan_device_packages)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _restore_selected(self):
        selected = [pkg for pkg, var in self.package_vars.items() if var.get()]
        if not selected:
            return

        def worker():
            for pkg in selected:
                if self.logger:
                    self.logger(f"[DEBLOATER] Restoring {pkg}...")
                code, out, err = self.adb.run_adb(["shell", f"pm install-existing --user 0 {pkg}"])
                if self.logger:
                    self.logger(out if out else err)
            self.after(0, self.scan_device_packages)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _manual_action(self, action: str):
        pkg = self.manual_pkg_entry.get().strip()
        if not pkg:
            return

        def worker():
            if action == "uninstall":
                if self.logger:
                    self.logger(f"[MANUAL] Uninstalling: {pkg}")
                code, out, err = self.adb.run_adb(["shell", f"pm uninstall -k --user 0 {pkg}"])
            else:
                if self.logger:
                    self.logger(f"[MANUAL] Restoring: {pkg}")
                code, out, err = self.adb.run_adb(["shell", f"pm install-existing --user 0 {pkg}"])

            if self.logger:
                self.logger(out if out else err)
            self.after(0, self.scan_device_packages)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

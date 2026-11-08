"""
=============================================================================
HyperPulse Toolkit - Smart Flasher & Brick-Guard View [V1.1]
Developed & Designed by Adrian (@stickshiftwillyy)
Target OS: Windows 10 / Windows 11 (64-bit)

Pre-flight compatibility verification, codename brick-guard, pre-flash checklist,
first-boot timer reassurance, and bootloop recovery assistant.
=============================================================================
"""

import os
import time
import threading
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from ui.styles import Theme
from core.flasher_engine import inspect_flashable_file


class FlasherView(ctk.CTkScrollableFrame):
    def __init__(self, master, adb_manager, status_logger=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.adb = adb_manager
        self.logger = status_logger

        self.selected_file_path = None
        self.inspection_result = None
        self.is_flashing = False
        self.boot_timer_active = False
        self.boot_timer_start = 0

        self._build_ui()

    def _build_ui(self):
        # 1. Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 12))

        title = ctk.CTkLabel(
            header,
            text="🛡️ Smart Flasher & Brick-Guard",
            font=Theme.FONT_TITLE,
            text_color=Theme.TEXT_MAIN
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Universal ROM sideload & Fastboot flasher with instant device codename safety checks.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # 2. File Selection Card
        picker_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        picker_card.pack(fill="x", padx=10, pady=(0, 12))

        p_top = ctk.CTkFrame(picker_card, fg_color="transparent")
        p_top.pack(fill="x", padx=15, pady=(12, 6))

        lbl_picker_title = ctk.CTkLabel(p_top, text="📥 Select File to Flash", font=Theme.FONT_HEADING, text_color=Theme.TEXT_MAIN)
        lbl_picker_title.pack(side="left")

        self.btn_browse = ctk.CTkButton(
            p_top,
            text="Browse Files...",
            width=130,
            height=30,
            font=Theme.FONT_SMALL,
            fg_color=Theme.ACCENT_BLUE,
            hover_color=Theme.ACCENT_HOVER,
            command=self._on_browse_file
        )
        self.btn_browse.pack(side="right")

        # File path display entry
        self.lbl_selected_file = ctk.CTkLabel(
            picker_card,
            text="No file selected. Choose a Custom ROM (.zip), Recovery/Boot (.img), or Fastboot (.tgz)",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
            anchor="w"
        )
        self.lbl_selected_file.pack(fill="x", padx=15, pady=(0, 12))

        # 3. Pre-Flight Verification Card (Brick-Guard)
        self.verify_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        self.verify_card.pack(fill="x", padx=10, pady=(0, 12))

        v_top = ctk.CTkFrame(self.verify_card, fg_color="transparent")
        v_top.pack(fill="x", padx=15, pady=(12, 6))

        lbl_v_title = ctk.CTkLabel(v_top, text="🔍 Pre-Flight Safety Verification", font=Theme.FONT_HEADING, text_color=Theme.TEXT_MAIN)
        lbl_v_title.pack(side="left")

        self.lbl_badge_status = ctk.CTkLabel(
            v_top,
            text=" WAITING FOR FILE ",
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            text_color=Theme.TEXT_DIM,
            corner_radius=6
        )
        self.lbl_badge_status.pack(side="right")

        # Verification details grid
        v_grid = ctk.CTkFrame(self.verify_card, fg_color=Theme.INPUT_BG, corner_radius=8)
        v_grid.pack(fill="x", padx=15, pady=(4, 10))
        v_grid.grid_columnconfigure((0, 1), weight=1)

        self.lbl_v_filename = ctk.CTkLabel(v_grid, text="File: --", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED, anchor="w")
        self.lbl_v_filename.grid(row=0, column=0, padx=10, pady=(8, 4), sticky="w")

        self.lbl_v_filesize = ctk.CTkLabel(v_grid, text="Size: --", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED, anchor="w")
        self.lbl_v_filesize.grid(row=0, column=1, padx=10, pady=(8, 4), sticky="w")

        self.lbl_v_target = ctk.CTkLabel(v_grid, text="Target Device: --", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED, anchor="w")
        self.lbl_v_target.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="w")

        self.lbl_v_connected = ctk.CTkLabel(v_grid, text="Connected Phone: --", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED, anchor="w")
        self.lbl_v_connected.grid(row=1, column=1, padx=10, pady=(0, 8), sticky="w")

        # Banner Message
        self.banner_frame = ctk.CTkFrame(self.verify_card, fg_color=Theme.INPUT_BG, corner_radius=8)
        self.banner_frame.pack(fill="x", padx=15, pady=(0, 12))

        self.lbl_banner_headline = ctk.CTkLabel(
            self.banner_frame,
            text="Brick-Guard Standing By",
            font=Theme.FONT_SUBHEAD,
            text_color=Theme.TEXT_MAIN,
            anchor="w"
        )
        self.lbl_banner_headline.pack(anchor="w", padx=12, pady=(8, 2))

        self.lbl_banner_desc = ctk.CTkLabel(
            self.banner_frame,
            text="Select any ROM or recovery image. HyperPulse will scan the metadata headers to ensure compatibility.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
            justify="left",
            wraplength=640,
            anchor="w"
        )
        self.lbl_banner_desc.pack(anchor="w", padx=12, pady=(0, 8))

        # Action Buttons Row
        action_row = ctk.CTkFrame(self.verify_card, fg_color="transparent")
        action_row.pack(fill="x", padx=15, pady=(0, 14))

        self.btn_flash = ctk.CTkButton(
            action_row,
            text="⚡ Start Sideload / Flash",
            width=200,
            height=34,
            font=Theme.FONT_SUBHEAD,
            fg_color=Theme.ACCENT_BLUE,
            hover_color=Theme.ACCENT_HOVER,
            state="disabled",
            command=self._on_request_flash
        )
        self.btn_flash.pack(side="right")

        self.lbl_flash_status = ctk.CTkLabel(action_row, text="", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED)
        self.lbl_flash_status.pack(side="left")

        # 4. First-Boot Status & Reassurance Card (Hidden until flash completes)
        self.boot_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)

        b_top = ctk.CTkFrame(self.boot_card, fg_color="transparent")
        b_top.pack(fill="x", padx=15, pady=(12, 6))

        lbl_b_title = ctk.CTkLabel(b_top, text="🔄 System Rebooting — First Boot in Progress", font=Theme.FONT_HEADING, text_color=Theme.ACCENT_CYAN)
        lbl_b_title.pack(side="left")

        self.lbl_boot_timer = ctk.CTkLabel(b_top, text="⏱️ 00:00 (Est: 4 - 7 mins)", font=Theme.FONT_CODE, text_color=Theme.SUCCESS_GREEN)
        self.lbl_boot_timer.pack(side="right")

        boot_box = ctk.CTkFrame(self.boot_card, fg_color=Theme.INPUT_BG, corner_radius=8)
        boot_box.pack(fill="x", padx=15, pady=(4, 12))

        b_msg = (
            "💡 RELAX AND DO NOT PANIC!\n\n"
            "• The first boot after flashing a fresh ROM always takes much longer than normal (typically 4 to 7 minutes).\n"
            "• Android is actively compiling ART/Dalvik caches and configuring storage encryption in the background.\n"
            "• Keep the phone connected to your PC.\n"
            "• DO NOT force-restart or hold down the Power button while the boot animation is running!"
        )
        lbl_b_msg = ctk.CTkLabel(boot_box, text=b_msg, font=Theme.FONT_BODY, text_color=Theme.TEXT_MAIN, justify="left", wraplength=640)
        lbl_b_msg.pack(anchor="w", padx=12, pady=10)

        # 5. Bootloop Rescue Assistant Card
        rescue_card = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        rescue_card.pack(fill="x", padx=10, pady=(0, 15))

        r_top = ctk.CTkFrame(rescue_card, fg_color="transparent")
        r_top.pack(fill="x", padx=15, pady=(12, 6))

        lbl_r_title = ctk.CTkLabel(r_top, text="🆘 Bootloop Rescue Assistant (Don't Panic!)", font=Theme.FONT_HEADING, text_color=Theme.WARNING_AMBER)
        lbl_r_title.pack(side="left")

        r_box = ctk.CTkFrame(rescue_card, fg_color=Theme.INPUT_BG, corner_radius=8)
        r_box.pack(fill="x", padx=15, pady=(4, 12))

        rescue_text = (
            "99% of bootloops when flashing Custom ROMs are caused by Storage Encryption / Old Userdata conflicts.\n\n"
            "👉 STEP 1 (The Universal Fix): Format Data in Recovery\n"
            "   1. Hold [Power + Volume Up] together for 10 seconds to enter Recovery.\n"
            "   2. Select Factory Reset ➔ Format Data / Wipe Userdata.\n"
            "   3. Type 'yes' and confirm. (A dirty flash from stock ROM will ALWAYS bootloop until you format data once!).\n\n"
            "👉 STEP 2: Emergency Fastboot Mode\n"
            "   • If the device restarts continuously, hold [Power + Volume Down] to enter Fastboot mode.\n"
            "   • You can use the buttons below to reboot or rescue your partitions."
        )
        lbl_rescue = ctk.CTkLabel(r_box, text=rescue_text, font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED, justify="left", wraplength=640)
        lbl_rescue.pack(anchor="w", padx=12, pady=10)

        # Quick Rescue Power Buttons
        r_btn_row = ctk.CTkFrame(rescue_card, fg_color="transparent")
        r_btn_row.pack(fill="x", padx=15, pady=(0, 12))

        btn_r_rec = ctk.CTkButton(
            r_btn_row,
            text="Reboot to Recovery",
            width=140,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=lambda: self.adb.run_adb(["reboot", "recovery"])
        )
        btn_r_rec.pack(side="left", padx=(0, 6))

        btn_r_fb = ctk.CTkButton(
            r_btn_row,
            text="Reboot to Fastboot",
            width=140,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=lambda: self.adb.run_adb(["reboot", "bootloader"])
        )
        btn_r_fb.pack(side="left", padx=(0, 6))

        btn_r_sys = ctk.CTkButton(
            r_btn_row,
            text="Force Reboot System",
            width=140,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=lambda: self.adb.run_adb(["reboot"])
        )
        btn_r_sys.pack(side="left")

    def _on_browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select ROM, Recovery, or Firmware Package",
            filetypes=[
                ("Flashable Android Files", "*.zip;*.img;*.tgz;*.tar;*.tar.gz"),
                ("Custom ROM / Sideload Zip", "*.zip"),
                ("Fastboot Partition Image", "*.img"),
                ("Official Fastboot Archive", "*.tgz;*.tar;*.tar.gz"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self._load_and_inspect_file(file_path)

    def _load_and_inspect_file(self, file_path: str):
        self.selected_file_path = file_path
        self.lbl_selected_file.configure(text=file_path, text_color=Theme.TEXT_MAIN)

        # Get connected phone codename
        details = self.adb.get_device_details()
        connected_codename = details.get("device", "Unknown")

        # Run instant pre-flight inspection
        res = inspect_flashable_file(file_path, connected_codename)
        self.inspection_result = res

        # Update labels
        self.lbl_v_filename.configure(text=f"File: {res['file_name']}")
        self.lbl_v_filesize.configure(text=f"Size: {res['file_size_str']}")
        
        target_str = ", ".join(res["target_devices"]) if res["target_devices"] else "Generic / Auto"
        self.lbl_v_target.configure(text=f"Target Device: {target_str}")
        self.lbl_v_connected.configure(text=f"Connected Phone: {connected_codename}")

        self.lbl_banner_headline.configure(text=res["headline"])
        self.lbl_banner_desc.configure(text=res["explanation"])

        # Status badge & color formatting
        if res["status_level"] == "safe":
            self.lbl_badge_status.configure(text=" 🟢 COMPATIBLE & SAFE ", text_color=Theme.SUCCESS_GREEN, fg_color=Theme.INPUT_BG)
            self.lbl_banner_headline.configure(text_color=Theme.SUCCESS_GREEN)
            self.btn_flash.configure(state="normal", text="⚡ Start Sideload / Flash", fg_color=Theme.SUCCESS_GREEN, hover_color=Theme.SUCCESS_HOVER)
        elif res["status_level"] == "danger":
            self.lbl_badge_status.configure(text=" 🛑 FLASH BLOCKED ", text_color=Theme.DANGER_RED, fg_color=Theme.INPUT_BG)
            self.lbl_banner_headline.configure(text_color=Theme.DANGER_RED)
            self.btn_flash.configure(state="disabled", text="🛑 Incompatible Device", fg_color=Theme.DANGER_RED)
        elif res["status_level"] == "warning":
            self.lbl_badge_status.configure(text=" ⚠️ CAUTION ", text_color=Theme.WARNING_AMBER, fg_color=Theme.INPUT_BG)
            self.lbl_banner_headline.configure(text_color=Theme.WARNING_AMBER)
            self.btn_flash.configure(state="normal", text="⚡ Proceed with Caution", fg_color=Theme.WARNING_AMBER, hover_color="#d97706")
        else:
            self.lbl_badge_status.configure(text=" ℹ️ READY ", text_color=Theme.ACCENT_CYAN, fg_color=Theme.INPUT_BG)
            self.lbl_banner_headline.configure(text_color=Theme.ACCENT_CYAN)
            self.btn_flash.configure(state="normal", text="⚡ Start Sideload / Flash", fg_color=Theme.ACCENT_BLUE, hover_color=Theme.ACCENT_HOVER)

    def _on_request_flash(self):
        if not self.selected_file_path or not self.inspection_result:
            return

        # Pre-Flight Confirmation Modal
        modal = ctk.CTkToplevel(self)
        modal.title("⚠️ Pre-Flight Safety Confirmation")
        modal.geometry("520x360")
        modal.resizable(False, False)
        modal.configure(fg_color=Theme.BG_DARK)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        # Modal Content
        lbl_m_title = ctk.CTkLabel(modal, text="⚠️ Confirm Flashing Checklist", font=Theme.FONT_TITLE, text_color=Theme.WARNING_AMBER)
        lbl_m_title.pack(anchor="w", padx=20, pady=(20, 10))

        details = self.adb.get_device_details()
        batt_str = details.get("battery_level", "Unknown")

        box = ctk.CTkFrame(modal, fg_color=Theme.CARD_BG, corner_radius=8, border_width=1, border_color=Theme.BORDER_COLOR)
        box.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        checklist_text = (
            f"• File to Flash: {self.inspection_result['file_name']}\n"
            f"• Target Device: {', '.join(self.inspection_result['target_devices']) if self.inspection_result['target_devices'] else 'Standard'}\n"
            f"• Current Battery: {batt_str} (Minimum 40% recommended)\n\n"
            "🚨 CRITICAL WARNING:\n"
            "Flashing a new custom ROM requires formatting userdata in recovery. "
            "Ensure you have backed up all important photos and files!"
        )
        lbl_chk = ctk.CTkLabel(box, text=checklist_text, font=Theme.FONT_BODY, text_color=Theme.TEXT_MAIN, justify="left")
        lbl_chk.pack(anchor="w", padx=15, pady=15)

        btn_box = ctk.CTkFrame(modal, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=(0, 20))

        btn_cancel = ctk.CTkButton(
            btn_box,
            text="Abort / Cancel",
            width=120,
            height=32,
            font=Theme.FONT_SMALL,
            fg_color=Theme.CARD_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=modal.destroy
        )
        btn_cancel.pack(side="left")

        btn_confirm = ctk.CTkButton(
            btn_box,
            text="⚡ Yes, Proceed & Flash",
            width=180,
            height=32,
            font=Theme.FONT_SUBHEAD,
            fg_color=Theme.SUCCESS_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            command=lambda: [modal.destroy(), self._execute_flash()]
        )
        btn_confirm.pack(side="right")

    def _execute_flash(self):
        if self.is_flashing:
            return
        self.is_flashing = True
        self.btn_flash.configure(state="disabled", text="Flashing in Progress...")
        self.lbl_flash_status.configure(text="Preparing device...", text_color=Theme.ACCENT_CYAN)

        def worker():
            file_path = self.selected_file_path
            action = self.inspection_result["action_type"]

            if action == "sideload":
                if self.logger:
                    self.logger(f"[FLASHER] Starting ADB sideload: {file_path}")
                self.after(0, lambda: self.lbl_flash_status.configure(text="Sideloading ROM... (Check recovery screen for %)", text_color=Theme.ACCENT_CYAN))
                code, out, err = self.adb.run_adb(["sideload", file_path], timeout=1200)
            elif action == "fastboot_flash":
                part = self.inspection_result.get("suggested_partition", "boot")
                if self.logger:
                    self.logger(f"[FLASHER] Flashing {file_path} to partition '{part}' via Fastboot...")
                code, out, err = self.adb.run_fastboot(["flash", part, file_path], timeout=120)
            else:
                code, out, err = 0, "File processed", ""

            self.after(0, lambda: self._on_flash_completed(code, out, err))

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _on_flash_completed(self, code, out, err):
        self.is_flashing = False
        self.btn_flash.configure(state="normal", text="⚡ Flash Another File")

        if code == 0:
            self.lbl_flash_status.configure(text="✓ Flash Completed Successfully!", text_color=Theme.SUCCESS_GREEN)
            # Display First-Boot Reassurance Card and start live elapsed timer!
            self.boot_card.pack(fill="x", padx=10, pady=(0, 15), before=self.verify_card)
            self._start_boot_timer()
        else:
            err_msg = err if err else out
            self.lbl_flash_status.configure(text=f"⚠️ Notice: {err_msg[:60]}", text_color=Theme.WARNING_AMBER)

    def _start_boot_timer(self):
        self.boot_timer_active = True
        self.boot_timer_start = time.time()

        def timer_loop():
            while self.boot_timer_active:
                elapsed = int(time.time() - self.boot_timer_start)
                mins = elapsed // 60
                secs = elapsed % 60
                time_str = f"⏱️ {mins:02d}:{secs:02d} (Est: 4 - 7 mins)"
                try:
                    self.after(0, lambda s=time_str: self.lbl_boot_timer.configure(text=s))
                except Exception:
                    pass
                time.sleep(1)

        t = threading.Thread(target=timer_loop, daemon=True)
        t.start()

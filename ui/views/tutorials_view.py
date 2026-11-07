"""
HyperPulse Toolkit - Tutorials View
Interactive, searchable guide reader with step-by-step instructions.
"""

import customtkinter as ctk
import tkinter as tk
from ui.styles import Theme
from tutorials.guides import TUTORIALS


class TutorialsView(ctk.CTkFrame):
    def __init__(self, master, status_logger=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.logger = status_logger
        self.selected_tutorial = TUTORIALS[0]

        self._build_ui()

    def _build_ui(self):
        # 1. Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 10))

        title = ctk.CTkLabel(
            header,
            text="📚 Guides & Step-by-Step Tutorials",
            font=Theme.FONT_TITLE,
            text_color=Theme.TEXT_MAIN
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Master ADB, Shizuku setup, Canta debloating, Bootloader unlocking, and Custom ROM installation.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # 2. Main split view: Left list, Right reader
        split_frame = ctk.CTkFrame(self, fg_color="transparent")
        split_frame.pack(fill="both", expand=True, padx=10, pady=(5, 5))

        # Left List Pane (35% width)
        left_pane = ctk.CTkScrollableFrame(split_frame, fg_color=Theme.CARD_BG, width=280, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        left_pane.pack(side="left", fill="y", padx=(0, 10), pady=0)

        lbl_select = ctk.CTkLabel(left_pane, text="Select a Guide", font=Theme.FONT_SUBHEAD, text_color=Theme.TEXT_MAIN)
        lbl_select.pack(anchor="w", padx=10, pady=(10, 8))

        self.guide_buttons = []
        for t in TUTORIALS:
            btn_box = ctk.CTkFrame(left_pane, fg_color=Theme.INPUT_BG, corner_radius=8)
            btn_box.pack(fill="x", padx=6, pady=4)

            btn = ctk.CTkButton(
                btn_box,
                text=f"{t['icon']}  {t['title']}",
                font=Theme.FONT_SMALL,
                fg_color="transparent",
                hover_color=Theme.CARD_HOVER,
                anchor="w",
                command=lambda item=t: self._display_tutorial(item)
            )
            btn.pack(fill="x", padx=6, pady=4)
            self.guide_buttons.append(btn)

        # Right Reader Pane
        right_pane = ctk.CTkFrame(split_frame, fg_color=Theme.CARD_BG, corner_radius=10, border_width=1, border_color=Theme.BORDER_COLOR)
        right_pane.pack(side="right", fill="both", expand=True)

        reader_top = ctk.CTkFrame(right_pane, fg_color="transparent")
        reader_top.pack(fill="x", padx=15, pady=(12, 6))

        self.lbl_reader_title = ctk.CTkLabel(
            reader_top,
            text=self.selected_tutorial["title"],
            font=Theme.FONT_HEADING,
            text_color=Theme.TEXT_MAIN
        )
        self.lbl_reader_title.pack(side="left")

        self.btn_copy_guide = ctk.CTkButton(
            reader_top,
            text="📋 Copy Guide",
            width=100,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.INPUT_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=self._copy_current_guide
        )
        self.btn_copy_guide.pack(side="right")

        self.text_reader = ctk.CTkTextbox(
            right_pane,
            font=Theme.FONT_BODY,
            fg_color=Theme.INPUT_BG,
            text_color=Theme.TEXT_MAIN,
            border_width=0,
            corner_radius=8,
            wrap="word"
        )
        self.text_reader.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Initial display
        self._display_tutorial(self.selected_tutorial)

    def _display_tutorial(self, tutorial):
        self.selected_tutorial = tutorial
        self.lbl_reader_title.configure(text=f"{tutorial['icon']} {tutorial['title']}")
        self.text_reader.delete("1.0", "end")
        self.text_reader.insert("1.0", tutorial["content"])

    def _copy_current_guide(self):
        content = self.selected_tutorial["content"]
        self.clipboard_clear()
        self.clipboard_append(content)
        self.btn_copy_guide.configure(text="✓ Copied!")
        self.after(2000, lambda: self.btn_copy_guide.configure(text="📋 Copy Guide"))

"""
HyperPulse Toolkit - Terminal View
Live interactive ADB console with real-time stream output and quick command presets.
"""

import customtkinter as ctk
from ui.styles import Theme


class TerminalView(ctk.CTkFrame):
    def __init__(self, master, adb_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.adb = adb_manager

        self._build_ui()

    def _build_ui(self):
        # 1. Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 10))

        title = ctk.CTkLabel(
            header,
            text="💻 Interactive ADB Terminal",
            font=Theme.FONT_TITLE,
            text_color=Theme.TEXT_MAIN
        )
        title.pack(side="left")

        btn_clear = ctk.CTkButton(
            header,
            text="Clear Console",
            width=100,
            height=28,
            font=Theme.FONT_SMALL,
            fg_color=Theme.CARD_BG,
            hover_color=Theme.CARD_HOVER,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            command=self.clear_console
        )
        btn_clear.pack(side="right")

        # 2. Quick Command Pills
        pills_box = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=8, border_width=1, border_color=Theme.BORDER_COLOR)
        pills_box.pack(fill="x", padx=10, pady=(0, 10))

        lbl_quick = ctk.CTkLabel(pills_box, text="Quick Commands:", font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED)
        lbl_quick.pack(side="left", padx=(10, 8), pady=6)

        quick_cmds = [
            ("Devices", "devices -l"),
            ("Battery Stats", "shell dumpsys battery"),
            ("3rd Party Apps", "shell pm list packages -3"),
            ("Display WM", "shell wm size"),
            ("System Props", "shell getprop ro.product.model")
        ]

        for label, cmd_str in quick_cmds:
            btn = ctk.CTkButton(
                pills_box,
                text=label,
                font=Theme.FONT_SMALL,
                height=24,
                fg_color=Theme.INPUT_BG,
                hover_color=Theme.CARD_HOVER,
                border_width=1,
                border_color=Theme.BORDER_COLOR,
                command=lambda c=cmd_str: self.run_custom_command(c)
            )
            btn.pack(side="left", padx=3, pady=6)

        # 3. Terminal Output Textbox
        self.terminal_box = ctk.CTkTextbox(
            self,
            font=Theme.FONT_CODE,
            fg_color=Theme.INPUT_BG,
            text_color="#38bdf8",
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            corner_radius=8,
            wrap="char"
        )
        self.terminal_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Initial prompt
        self.append_log("HyperPulse ADB Studio [Version 1.0.0]\nType an ADB command below (e.g. 'devices', 'shell pm list packages', 'reboot')\n\n")

        # 4. Command Input Bar
        input_bar = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=8, border_width=1, border_color=Theme.BORDER_COLOR)
        input_bar.pack(fill="x", padx=10, pady=(0, 5))

        lbl_prompt = ctk.CTkLabel(input_bar, text="adb >", font=Theme.FONT_CODE, text_color=Theme.ACCENT_CYAN)
        lbl_prompt.pack(side="left", padx=(12, 6), pady=8)

        self.cmd_entry = ctk.CTkEntry(
            input_bar,
            placeholder_text="Enter command...",
            font=Theme.FONT_CODE,
            fg_color=Theme.INPUT_BG,
            border_color=Theme.BORDER_COLOR,
            height=32
        )
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=8)
        self.cmd_entry.bind("<Return>", lambda e: self._on_submit())

        self.btn_run = ctk.CTkButton(
            input_bar,
            text="Run",
            width=80,
            height=32,
            font=Theme.FONT_SUBHEAD,
            fg_color=Theme.ACCENT_BLUE,
            hover_color=Theme.ACCENT_HOVER,
            command=self._on_submit
        )
        self.btn_run.pack(side="right", padx=(0, 10), pady=8)

    def _on_submit(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        self.cmd_entry.delete(0, "end")
        self.run_custom_command(cmd)

    def run_custom_command(self, cmd_text: str):
        # Strip leading 'adb ' if user typed it
        if cmd_text.lower().startswith("adb "):
            cmd_text = cmd_text[4:].strip()

        self.append_log(f"\n$ adb {cmd_text}\n")
        self.btn_run.configure(state="disabled")

        def on_stream(line: str):
            self.append_log(line)

        def on_finish(code: int):
            self.after(0, lambda: self.btn_run.configure(state="normal"))

        self.adb.stream_command(cmd_text, output_callback=on_stream, on_complete=on_finish)

    def append_log(self, text: str):
        def _insert():
            self.terminal_box.insert("end", text)
            self.terminal_box.see("end")
        self.after(0, _insert)

    def clear_console(self):
        self.terminal_box.delete("1.0", "end")

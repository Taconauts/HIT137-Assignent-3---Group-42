# views/results_view.py
# Two independent outputs with their own scrollbars. Full nav on this view.

import tkinter as tk
from tkinter import ttk
import json


class ResultsView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller

        # nav (match other views so tabs don't "disappear")
        nav = tk.Frame(self)
        nav.pack(fill="x", pady=6)
        ttk.Button(nav, text="Home", command=lambda: controller.show_view("HomeView")).pack(side="left", padx=4)
        ttk.Button(nav, text="Input", command=lambda: controller.show_view("InputView")).pack(side="left", padx=4)
        ttk.Button(nav, text="Results", command=lambda: controller.show_view("ResultsView")).pack(side="left", padx=4)
        ttk.Button(nav, text="About", command=lambda: controller.show_view("AboutView")).pack(side="left", padx=4)
        ttk.Button(nav, text="OOP Info", command=lambda: controller.show_view("OOPInfoView")).pack(side="left", padx=4)

        tk.Label(self, text="Model Outputs", font=("Helvetica", 14, "bold")).pack(pady=8)

        # grid layout
        grid = tk.Frame(self)
        grid.pack(fill="both", expand=True, padx=10, pady=8)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        grid.grid_rowconfigure(1, weight=1)

        # left: ViT box
        tk.Label(grid, text="ViT Image Classification").grid(row=0, column=0, sticky="w", pady=(0, 4))
        vit_wrap = tk.Frame(grid, borderwidth=1, relief="groove")
        vit_wrap.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
        self.vit_text = tk.Text(vit_wrap, wrap="word", state="disabled")
        vit_scroll = ttk.Scrollbar(vit_wrap, orient="vertical", command=self.vit_text.yview)
        self.vit_text.configure(yscrollcommand=vit_scroll.set)
        self.vit_text.grid(row=0, column=0, sticky="nsew")
        vit_scroll.grid(row=0, column=1, sticky="ns")
        vit_wrap.grid_rowconfigure(0, weight=1)
        vit_wrap.grid_columnconfigure(0, weight=1)

        # right: Whisper box
        tk.Label(grid, text="Whisper Transcription").grid(row=0, column=1, sticky="w", pady=(0, 4))
        w_wrap = tk.Frame(grid, borderwidth=1, relief="groove")
        w_wrap.grid(row=1, column=1, sticky="nsew", padx=(6, 0))
        self.whisper_text = tk.Text(w_wrap, wrap="word", state="disabled")
        w_scroll = ttk.Scrollbar(w_wrap, orient="vertical", command=self.whisper_text.yview)
        self.whisper_text.configure(yscrollcommand=w_scroll.set)
        self.whisper_text.grid(row=0, column=0, sticky="nsew")
        w_scroll.grid(row=0, column=1, sticky="ns")
        w_wrap.grid_rowconfigure(0, weight=1)
        w_wrap.grid_columnconfigure(0, weight=1)

        self.render_all()

    def render_all(self):
        # pull data from controller and display
        self._set_text(self.vit_text, self._fmt_vit(self.controller.image_result))
        self._set_text(self.whisper_text, self._fmt_whisper(self.controller.asr_result))

    def _set_text(self, widget, content):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", content if content else "(no result)")
        widget.see("end")
        widget.configure(state="disabled")

    def _fmt_vit(self, data):
        if not data:
            return ""
        if isinstance(data, list) and all(isinstance(x, dict) for x in data):
            out = []
            for i, d in enumerate(data, 1):
                lbl = d.get("label", "?")
                scr = d.get("score", 0.0)
                try:
                    scr = float(scr)
                    out.append(f"{i}. {lbl} — {scr:.4f}")
                except Exception:
                    out.append(f"{i}. {lbl} — {scr}")
            return "\n".join(out)
        return json.dumps(data, indent=2)

    def _fmt_whisper(self, data):
        if not data:
            return ""
        if isinstance(data, dict) and "text" in data:
            return str(data.get("text", ""))
        return json.dumps(data, indent=2)

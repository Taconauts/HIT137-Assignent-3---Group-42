# controller.py
# View switch + shared state. Rebuilds view each time and calls render_all() if present.

import tkinter as tk
from views.home_view import HomeView
from views.input_view import InputView
from views.results_view import ResultsView
from views.about_view import AboutView
from views.oop_info_view import OOPInfoView


class Controller:
    def __init__(self, root):
        self.root = root
        self.root.title("HIT137 Assignment 3: Group 42 - AI Toolkit")

        # allow space for two scrollable panes
        self.root.resizable(True, True)
        self.root.minsize(800, 500)

        # shared state
        self.selected_file = None
        self.image_result = None   # ViT output
        self.asr_result = None     # Whisper output

        self.current_view = None
        self.show_view("HomeView")

    def show_view(self, view_name: str):
        # remove current view
        if self.current_view:
            self.current_view.destroy()

        # create requested view
        if view_name == "HomeView":
            frame = HomeView(self.root, self)
        elif view_name == "InputView":
            frame = InputView(self.root, self)
        elif view_name == "ResultsView":
            frame = ResultsView(self.root, self)
        elif view_name == "AboutView":
            frame = AboutView(self.root, self)
        elif view_name == "OOPInfoView":
            frame = OOPInfoView(self.root, self)
        else:
            frame = tk.Frame(self.root)
            tk.Label(frame, text="Page not found").pack(pady=20)

        # mount
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        frame.pack_propagate(True)

        # ensure fresh data render
        if hasattr(frame, "render_all"):
            try:
                frame.render_all()
            except Exception as e:
                print("render_all error:", e)

        self.root.update_idletasks()
        self.center_window()
        self.current_view = frame

    def center_window(self):
        # center window based on current content size
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

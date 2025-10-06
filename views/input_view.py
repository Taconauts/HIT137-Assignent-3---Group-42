# views/input_view.py
# Select file. Run ViT or Whisper. Write outputs to controller.* and refresh Results.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from models.image_classify import ImageClassify
from models.asr_whisper import ASRWhisper


class InputView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller

        # nav
        nav = tk.Frame(self); nav.pack(fill="x", pady=6)
        ttk.Button(nav, text="Results", command=lambda: controller.show_view("ResultsView")).pack(side="left", padx=4)

        # file picker
        picker = tk.LabelFrame(self, text="Select input file")
        picker.pack(fill="x", padx=10, pady=8)
        self.path_var = tk.StringVar()
        ttk.Entry(picker, textvariable=self.path_var).pack(side="left", fill="x", expand=True, padx=8, pady=8)
        ttk.Button(picker, text="Browse...", command=self._browse_any).pack(side="right", padx=8, pady=8)

        # actions
        actions = tk.LabelFrame(self, text="Run model")
        actions.pack(fill="x", padx=10, pady=8)
        ttk.Button(actions, text="Run ViT Image Classification", command=self.run_image).pack(fill="x", padx=8, pady=6)
        ttk.Button(actions, text="Run Whisper (Audio → Text)", command=self.run_asr).pack(fill="x", padx=8, pady=6)

        tk.Label(self, text="Image → ViT. Audio/Video → Whisper.", anchor="w").pack(fill="x", padx=12, pady=(0, 10))

    # helpers

    def _browse_any(self):
        # file type is validated by each model
        path = filedialog.askopenfilename()
        if path:
            self.path_var.set(path)

    def _ensure_path(self) -> str:
        # guard: require a file before running
        path = self.path_var.get().strip()
        if not path:
            messagebox.showwarning("No file", "Select a file first.")
            raise RuntimeError("No path selected")
        return path

    def _goto_results_and_refresh(self):
        # navigate + force UI to re-render results
        self.controller.show_view("ResultsView")
        view = self.controller.views.get("ResultsView")
        if hasattr(view, "render_all"):
            try:
                view.render_all()
            except Exception as e:
                print("render_all error:", e)

    # model runners

    def run_image(self):
        # ViT path
        try:
            path = self._ensure_path()
        except RuntimeError:
            return
        try:
            model = ImageClassify()
            result = model.run(path)
            self.controller.image_result = result  # only image_result
        except Exception as e:
            self.controller.image_result = [{"label": "ERROR", "score": 0.0, "detail": str(e)}]
            print("ImageClassify error:", e)
        self._goto_results_and_refresh()

    def run_asr(self):
        # Whisper path
        try:
            path = self._ensure_path()
        except RuntimeError:
            return
        try:
            model = ASRWhisper()
            result = model.run(path)
            if isinstance(result, str):  # normalize
                result = {"text": result}
            self.controller.asr_result = result  # only asr_result
        except Exception as e:
            self.controller.asr_result = {"text": f"(ERROR) {e}"}
            print("ASRWhisper error:", e)
        self._goto_results_and_refresh()

import tkinter as tk
from tkinter import ttk

class AboutView(tk.Frame):
    def __init__(self, root, controller ):
        super().__init__(root )
        self.controller = controller

        self.create_nav(controller )

        tk.Label(self, text="About the Models", font=("Helvetica", 16, "bold" ) ).pack(pady=20 )

        text_box = tk.Text(self, wrap="word", width=90, height=20 )
        text_box.pack(padx=10, pady=10 )

        # Add info text
        text_box.insert("end",
            "🖼️ Image Classification (google/vit-base-patch16-224):\n"
            "- Vision Transformer (ViT) model that classifies images into categories.\n"
            "- Works by splitting an image into patches and analyzing features.\n"
            "- Commonly used for object recognition and tagging tasks.\n\n"
            "🎙️ Speech-to-Text (openai/whisper-tiny):\n"
            "- Converts spoken audio into text.\n"
            "- Uses transformer-based encoder-decoder architecture.\n"
            "- Small, fast, and accurate for short speech tasks.\n"  )

        text_box.configure(state="disabled" )  # Read-only box

    def create_nav(self, controller ):
        nav = tk.Frame(self, bg="#ddd" )
        nav.pack(fill="x", pady=5 )

        buttons = [("Home", "HomeView" ), ("Input", "InputView" ), ("Results", "ResultsView" ), ("About", "AboutView" ), ("OOP Info", "OOPInfoView" )]
        for text, view in buttons:
            ttk.Button(nav, text=text, command=lambda v=view: controller.show_view(v ) ).pack(side="left", padx=5, pady=5 )

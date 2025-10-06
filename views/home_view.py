import tkinter as tk
from tkinter import ttk

class HomeView(tk.Frame):
    def __init__(self, root, controller ):
        super().__init__(root )
        self.controller = controller

        self.create_nav(controller )

        # Home screen content
        tk.Label(self, text="Welcome to the AI Toolkit", font=("Helvetica", 18, "bold" ) ).pack(pady=40 )
        tk.Label(self, text="Use the top menu to navigate between functions." ).pack(pady=10 )

    def create_nav(self, controller ):
        nav = tk.Frame(self, bg="#ddd" )
        nav.pack(fill="x", pady=5 )

        # Top navigation buttons
        buttons = [("Home", "HomeView" ), ("Input", "InputView" ), ("Results", "ResultsView" ), ("About", "AboutView" ), ("OOP Info", "OOPInfoView" )]
        for text, view in buttons:
            ttk.Button(nav, text=text, command=lambda v=view: controller.show_view(v ) ).pack(side="left", padx=5, pady=5 )

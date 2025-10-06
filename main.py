import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import tkinter as tk
from controller import Controller

# Entry point for the app
if __name__ == "__main__":
    root = tk.Tk()  # Create main Tkinter window
    app = Controller(root )  # Init controller to manage all pages
    root.mainloop()  # Keep window open until closed by user

import tkinter as tk
from tkinter import ttk

class OOPInfoView(tk.Frame):
    def __init__(self, root, controller ):
        super().__init__(root )
        self.controller = controller

        self.create_nav(controller )

        tk.Label(self, text="OOP Concepts in This Project", font=("Helvetica", 16, "bold" ) ).pack(pady=20 )

        text_box = tk.Text(self, wrap="word", width=90, height=20 )
        text_box.pack(padx=10, pady=10 )

        text_box.insert("end",
            "* Abstraction:\n"
            "- ModelBase defines a common interface and @abstractmethod run( ).\n"
            "- All models must implement run( ) to be usable.\n\n"
            "* Inheritance (and Multiple Inheritance):\n"
            "- ImageClassify and ASRWhisper inherit ModelBase for shared fields (name, description ).\n"
            "- Both also inherit TimestampMixin → ModelBase, TimestampMixin (multiple inheritance ).\n\n"
            "* Polymorphism & Overriding:\n"
            "- Each subclass overrides run( ) with task-specific logic.\n"
            "- ImageClassify → top-k labels from ViT.  ASRWhisper → speech/video to text.\n\n"
            "* Encapsulation:\n"
            "- ModelBase stores _name and _description as internal attributes accessed via methods.\n\n"
            "* Decorators (multiple used):\n"
            "- @ensure_path validates the input path before run( ) executes.\n"
            "- @timeit measures runtime of run( ) for transparency/perf notes.\n"
            "- @abstractmethod in ModelBase enforces the contract for subclasses.\n\n"
            "* Mixins (why used):\n"
            "- TimestampMixin adds a light provenance stamp without coupling to ModelBase.\n"
            "- Keeps cross-cutting concerns small and reusable.\n\n"
            "* Error Handling:\n"
            "- Image validation via Pillow; clear ValueError/FileNotFoundError messages.\n"
            "- Whisper auto-ensures FFmpeg; raises clean EnvironmentError if setup fails.\n\n"
            "Overall: the app shows clear abstraction, encapsulation, inheritance (incl. multiple ),\n"
            "polymorphism with method overriding, and multiple decorators applied in practice.\n")
        

        text_box.configure(state="disabled" )

    def create_nav(self, controller ):
        nav = tk.Frame(self, bg="#ddd" )
        nav.pack(fill="x", pady=5 )

        buttons = [("Home", "HomeView" ), ("Input", "InputView" ), ("Results", "ResultsView" ),
                   ("About", "AboutView" ), ("OOP Info", "OOPInfoView" )]
        for text, view in buttons:
            ttk.Button(nav, text=text, command=lambda v=view: controller.show_view(v ) ).pack(side="left", padx=5, pady=5 )

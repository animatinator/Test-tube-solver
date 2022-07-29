import tkinter as tk


class TubeView(tk.Frame):
    """Displays editable test tubes."""
    def __init__(self, parent):
        super().__init__(parent)

        self.label = tk.Label(self, text='Tube view goes here')
        self.label.pack(fill=tk.BOTH, expand=True)

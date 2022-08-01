import tkinter as tk


class TubeBoardView(tk.Frame):
    """Displays the range of editable test tubes."""
    def __init__(self, parent):
        super().__init__(parent)

        self.label = tk.Label(self, text='Tube board view goes here')
        self.label.pack(fill=tk.BOTH, expand=True)

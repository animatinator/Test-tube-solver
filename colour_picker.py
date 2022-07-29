import tkinter as tk


class ColourPicker(tk.Frame):
    """A horizontal bar of colour picker labels.
    
    These are used to define the selection of colours used.
    """
    def __init__(self, parent):
        super().__init__(parent, background="pink")

        self.label = tk.Label(self, text='Colour picker goes here', background="pink")
        self.label.pack(fill=tk.BOTH, expand=True)

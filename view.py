import tkinter as tk

import colour_picker
import tube_view


class MainWindow(tk.Frame):
    """The main view. Contains all view components."""
    def __init__(self, parent):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        self._colour_picker = colour_picker.ColourPicker(self)
        self._colour_picker.grid(row=0, column=0, sticky="nsew")
        
        self._tube_view = tube_view.TubeView(self)
        self._tube_view.grid(row=1, column=0, sticky="nsew")

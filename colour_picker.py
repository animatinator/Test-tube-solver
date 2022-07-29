import copy

import tkinter as tk
from tkinter.colorchooser import askcolor


class ColourPicker(tk.Frame):
    """A horizontal bar of colour picker labels.
    
    These are used to define the selection of colours used.
    """
    def __init__(self, parent):
        super().__init__(parent, background="pink")

        self._frames = []

        self._frames.append(tk.Frame(self, background="red"))
        self._frames.append(tk.Frame(self, background="blue"))
        self._frames.append(tk.Frame(self, background="green"))

        def create_colour_picker_callback(i):
            return lambda event: self._pick_colour(i, event)

        for i, frame in enumerate(self._frames):
            frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
            frame.bind("<Button-1>", create_colour_picker_callback(i))

    def _pick_colour(self, i, event):
        _, hex_col = askcolor(color=self._frames[i]["background"])
        self._frames[i].configure(background=hex_col)
        self._update_colours()
    
    def _update_colours(self):
        print('Colours have changed.')
        print('TODO: Update the model via the controller.')

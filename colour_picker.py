import copy

import tkinter as tk
from tkinter.colorchooser import askcolor


class ColourPicker(tk.Frame):
    """A horizontal bar of colour picker labels.
    
    These are used to define the selection of colours used.
    """
    def __init__(self, parent):
        super().__init__(parent, background="pink")

        self._frames_container = tk.Frame(self)
        self._add_colour_button = tk.Button(self, text="+", command=self._add_colour)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self._frames_container.grid(row=0, column=0, sticky="nsew")
        self._add_colour_button.grid(row=0, column=1, sticky="nsew")

        self._frames = []

        self._add_colour("red")
        self._add_colour("blue")
        self._add_colour("green")

    def _pick_colour(self, i, event):
        _, hex_col = askcolor(color=self._frames[i]["background"])
        self._frames[i].configure(background=hex_col)
        self._update_colours()
    
    def _update_colours(self):
        print('Colours have changed.')
        print('TODO: Update the model via the controller.')

    def _create_colour_picker_callback(self, i):
        return lambda event: self._pick_colour(i, event)

    def _create_del_context_callback(self, i):
        return lambda event: self._show_delete_context_menu(i, event)
    
    def _add_colour(self, initial_colour="white"):
        index = len(self._frames)
        frame = tk.Frame(self._frames_container, background=initial_colour)
        self._frames.append(frame)
        frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        frame.bind("<Button-1>", self._create_colour_picker_callback(index))
        frame.bind("<Button-3>", self._create_del_context_callback(index))
    
    def _show_delete_context_menu(self, i, event):
        print(f"Delete colour at position {i}?")

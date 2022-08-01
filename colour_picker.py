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

        self._frames.append(tk.Frame(self._frames_container, background="red"))
        self._frames.append(tk.Frame(self._frames_container, background="blue"))
        self._frames.append(tk.Frame(self._frames_container, background="green"))

        def create_colour_picker_callback(i):
            return lambda event: self._pick_colour(i, event)

        def create_del_context_callback(i):
            return lambda event: self._show_delete_context_menu(i, event)

        for i, frame in enumerate(self._frames):
            frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
            frame.bind("<Button-1>", create_colour_picker_callback(i))
            frame.bind("<Button-3>", create_del_context_callback(i))

    def _pick_colour(self, i, event):
        _, hex_col = askcolor(color=self._frames[i]["background"])
        self._frames[i].configure(background=hex_col)
        self._update_colours()
    
    def _update_colours(self):
        print('Colours have changed.')
        print('TODO: Update the model via the controller.')
    
    def _add_colour(self):
        print('Time to add a new colour.')
    
    def _show_delete_context_menu(self, i, event):
        print(f"Delete colour at position {i}?")

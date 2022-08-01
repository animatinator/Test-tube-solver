import tkinter as tk

import colour_picker
import controller_interface
import board_view
import ui_model


class MainWindow(tk.Frame):
    """The main view. Contains all view components."""
    def __init__(self, parent, model: ui_model.UiModel, initial_tubes: int):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        self._colour_picker = colour_picker.ColourPicker(self, model.get_colours())
        self._colour_picker.grid(row=0, column=0, sticky="nsew")
        
        self._board_view = board_view.TubeBoardView(self, model, initial_tubes)
        self._board_view.grid(row=1, column=0, sticky="nsew")
    
    def set_controller(self, controller: controller_interface.Controller):
        self._colour_picker.set_controller(controller)

import tkinter as tk
from tkinter import messagebox

import colour_picker
import controller_interface
import board_view
import ui_model


class MainWindow(tk.Frame):
    """The main view. Contains all view components."""
    def __init__(self, parent, model: ui_model.UiModel):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self._colour_picker = colour_picker.ColourPicker(self, model)
        self._colour_picker.grid(row=0, column=0, sticky="nsew")
        
        self._board_view = board_view.TubeBoardView(self, model)
        self._board_view.grid(row=1, column=0, sticky="nsew")

        self._controller = None

        self._solve_button = tk.Button(
            self, text="Solve!", background="green",
            command=lambda: self._controller.run_solver(self._handle_solution_error))
        self._solve_button.grid(row=2, column=0, sticky="nsew")
    
    def _handle_solution_error(self, message: str):
        messagebox.showerror("Solver failed!", f"The solver failed: '{message}'.")
    
    def set_controller(self, controller: controller_interface.Controller):
        self._controller = controller
        self._colour_picker.set_controller(controller)
        self._board_view.set_controller(controller)
    
    def notify_colours_changed(self):
        self._board_view.notify_colours_changed()
    
    def reset_to_match_model(self):
        self._colour_picker.reset_to_match_model()
        self._board_view.reset_to_match_model()

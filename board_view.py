import tkinter as tk

import controller_interface
import state
import tube_view
from typing import List
import ui_model


class TubeBoardView(tk.Frame):
    """Displays the range of editable test tubes."""
    def __init__(self, parent, model: ui_model.UiModel, initial_tubes: state.TubeBoard):
        super().__init__(parent)

        self._model = model
        # This is set later by set_controller.
        self._controller = None

        self._tubes = []

        for tube in initial_tubes.tubes:
            self._add_tube(initial_state=tube.state)
    
    def set_controller(self, controller: controller_interface.Controller):
        self._controller = controller
        for tube in self._tubes:
            tube.set_controller(self._controller)
    
    def _add_tube(self, initial_state: List[int]):
        index = len(self._tubes)
        tube = tube_view.TubeView(self, self._model, index, width=100, initial_state=initial_state)
        tube.set_controller(self._controller)
        self._tubes.append(tube)
        tube.pack(fill=tk.Y, side=tk.LEFT, expand=True, padx=20, pady=10)

    def notify_colours_changed(self):
        for tube in self._tubes:
            tube.notify_colours_changed()
    
    def _assert_has_controller(self):
        if not self._controller:
            raise AssertionError("Trying to use the controller before it has been set!")

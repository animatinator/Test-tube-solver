from typing import List

import controller_interface
import ui_model
import view


class UiController(controller_interface.Controller):
    """The UI controler.
    
    This exposes methods for updating the model and UI components.
    """
    def __init__(self, model: ui_model.UiModel, view: view.MainWindow):
        self._model = model
        self._view = view
    
    def update_colours(self, colours: List[str]):
        self._model.update_colours(colours)
        self._view.notify_colours_changed()
    
    def update_tube_state(self, index: int, state: List[int]):
        self._model.update_tube_state(index, state)
    
    def add_tube(self, initial_state: List[int]):
        self._model.add_tube(initial_state=initial_state)
    
    def delete_tube(self, index: int):
        self._model.delete_tube(index)

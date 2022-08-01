import tkinter as tk

import constants
import controller_interface
import ui_model


class TubeView(tk.Frame):
    """Displays a single editable test tube."""
    def __init__(
            self,
            parent,
            model: ui_model.UiModel,
            index: int,
            depth: int = constants.TUBE_DEPTH):
        super().__init__(parent)

        self._model = model
        # This will be set by set_controller later.
        self._controller = None
        self._index = index

        # Note: '0' means empty. Numbers above zero map to defined colours.
        # So '1' maps to the zeroth defined colour etc.
        self._state = [0] * depth

        self._frames = []

        for index, elem in enumerate(self._state):
            new_frame = tk.Frame(self._frames_conainer, background=self._get_colour_value(elem))
            self._frames.append(new_frame)
            frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
            self._bind_events_for_frame_at_index(new_frame, index)
    
    def set_controller(self, controller: controller_interface.Controller):
        self._controller = controller
    
    def set_index(new_index: int):
        self._index = new_index
    
    def _get_colour_value(colour_index: int) -> str:
        # '0' signifies empty.
        if colour_index == 0:
            return "white"
        return self._model.get_colour_for_index(colour_index - 1)
    
    def _create_colour_picker_callback(index: int):
        return lambda event: self._pick_colour_for_index(index)

    def _bind_events_for_frame_at_index(self, frame: tk.Frame, index: int):
        frame.bind("<Button-1>", self._create_colour_picker_callback(index))

    def _pick_colour(self, current_colour: int) -> int:
        print(f"TODO: Choose new colour. Current: {current_colour}")
        return current_colour
    
    def _pick_colour_for_index(self, index: int):
        new_colour_index = self._pick_colour(self._state[index])
        self._state[index] = new_colour_index
        new_colour = self._get_colour_value(new_colour_index)
        self._frames[index].configure(background=new_colour)

        self._assert_has_controller()
        self._controller.update_tube_state(self._index, self._state)
    
    def _assert_has_controller(self):
        if not self._controller:
            raise AssertionError("Trying to use the controller before it has been set!")

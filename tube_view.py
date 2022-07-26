import tkinter as tk

import constants
import controller_interface
from PIL import Image, ImageTk
from typing import Callable, List
import ui_model


class TubeView(tk.Frame):
    """Displays a single editable test tube."""
    def __init__(
            self,
            parent,
            model: ui_model.UiModel,
            index: int,
            depth: int = constants.TUBE_DEPTH,
            width: int = 100,
            initial_state: List[int] = [0] * constants.TUBE_DEPTH,
            **kwargs):
        super().__init__(parent, width=width, **kwargs)

        self._model = model
        # This will be set by set_controller later.
        self._controller = None
        self._index = index

        # Note: '0' means empty. Numbers above zero map to defined colours.
        # So '1' maps to the zeroth defined colour etc.
        self._state = initial_state

        self._frames_container = tk.Frame(self)
        self._frames = []

        for index, elem in enumerate(self._state):
            new_frame = tk.Frame(self._frames_container, background=self._get_colour_value(elem), width=width)
            self._frames.append(new_frame)
            new_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
            self._bind_events_for_frame_at_index(new_frame, index)
        
        self._frames_container.pack(fill=tk.BOTH, expand=True)
    
    def set_controller(self, controller: controller_interface.Controller):
        self._controller = controller

    def set_index(self, index: int):
        self._index = index
    
    def bind_context_menu_callback(self, callback: Callable[[tk.Event], None]):
        # Bind a right-click event for all frames. Used to allow the owner of this object to add a
        # context menu.
        for frame in self._frames:
            frame.bind("<Button-3>", callback)

    def notify_colours_changed(self):
        for index in range(len(self._state)):
            self._update_colour_for_element_at_index(index)

    def _update_colour_for_element_at_index(self, index: int):
        # If the colour index for this element is now out of range, reset it to empty.
        if self._state[index] > len(self._model.get_colours()):
            self._state[index] = 0
        self._frames[index].configure(background=self._get_colour_value(self._state[index]))
    
    def _get_colour_value(self, colour_index: int) -> str:
        # '0' signifies empty.
        if colour_index == 0:
            return "white"
        return self._model.get_colour_for_index(colour_index - 1)
    
    def _create_colour_picker_callback(self, index: int) -> Callable[[tk.Event], None]:
        return lambda event: self._pick_colour_for_index(event, index)

    def _bind_events_for_frame_at_index(self, frame: tk.Frame, index: int):
        frame.bind("<Button-1>", self._create_colour_picker_callback(index))

    def _set_colour_at_index(self, new_colour_index: int, index: int):
        self._state[index] = new_colour_index
        self._update_colour_for_element_at_index(index)

        self._assert_has_controller()
        self._controller.update_tube_state(self._index, self._state)
    
    def _create_colour_icon(self, colour: str) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(Image.new(mode="RGB", size=(50, 50), color=colour))

    def _pick_colour_for_index(self, event: tk.Event, index: int) -> int:
        current_colour = self._state[index]
        colours = self._model.get_colours()
        m = tk.Menu(self, tearoff=False)

        def _create_colour_setter(colour_id: int, index: int) -> Callable[[], None]:
            return lambda: self._set_colour_at_index(colour_id, index)

        # Add the option for emptying this element.
        m.add_command(label="Empty", command=_create_colour_setter(0, index))

        images = [self._create_colour_icon(colour) for colour in colours]

        for i, colour in enumerate(colours):
            # Adding one to each colour index because zero indicates empty.
            m.add_command(
                image=images[i],
                compound=tk.LEFT,
                command=_create_colour_setter(i+1, index))

        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

        return current_colour
    
    def _assert_has_controller(self):
        if not self._controller:
            raise AssertionError("Trying to use the controller before it has been set!")

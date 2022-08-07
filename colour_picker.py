import copy
from typing import Callable, List

import tkinter as tk
from tkinter.colorchooser import askcolor
import controller_interface
import ui_model


class ColourPicker(tk.Frame):
    """A horizontal bar of colour picker labels.
    
    These are used to define the selection of colours used.
    """
    def __init__(self, parent, model: ui_model.UiModel):
        super().__init__(parent, background="pink")

        self._model = model
        # The controller will be set by a later call to set_controller.
        self._controller = None

        self._colour_frames_container = tk.Frame(self)
        self._add_colour_button = tk.Button(self, text="+", command=self._add_colour)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self._colour_frames_container.grid(row=0, column=0, sticky="nsew")
        self._add_colour_button.grid(row=0, column=1, sticky="nsew")

        self._colour_frames = []

        self.reset_to_match_model()
    
    def set_controller(self, controller: controller_interface.Controller):
        self._controller = controller

    def reset_to_match_model(self):
        # Clear all existing colours by repeatedly deleting index zero.
        for index in range(len(self._colour_frames)):
            # Don't update the controller or we'll change the model.
            self._delete_colour(0, update_controller=False)

        # Now add the colours from the model.
        for colour in self._model.get_colours():
            self._add_colour(colour, update_controller=False)

    def _pick_colour(self, i: int, event: tk.Event):
        _, hex_col = askcolor(color=self._colour_frames[i]["background"])
        self._colour_frames[i].configure(background=hex_col)
        self._update_colours()
    
    def _update_colours(self):
        self._assert_has_controller()
        self._controller.update_colours([frame["background"] for frame in self._colour_frames])

    def _create_colour_picker_callback(self, i: int) -> Callable[[tk.Event], None]:
        return lambda event: self._pick_colour(i, event)

    def _create_del_context_callback(self, i: int) -> Callable[[tk.Event], None]:
        return lambda event: self._show_delete_context_menu(i, event)

    def _bind_events_for_frame_at_index(self, frame: tk.Frame, index: int):
        frame.bind("<Button-1>", self._create_colour_picker_callback(index))
        frame.bind("<Button-3>", self._create_del_context_callback(index))    
    
    def _add_colour(self, initial_colour: str="white", update_controller: bool=True):
        index = len(self._colour_frames)
        frame = tk.Frame(self._colour_frames_container, background=initial_colour)
        self._colour_frames.append(frame)
        frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self._bind_events_for_frame_at_index(frame, index)

        # Updating the controller is optional because we won't yet have a controller when this
        # method is first called (during construction).
        if update_controller:
            self._update_colours()

    def _rebind_frame_events(self):
        for index, frame in enumerate(self._colour_frames):
            self._bind_events_for_frame_at_index(frame, index)
    
    def _delete_colour(self, index: int, update_controller: bool = True):
        self._colour_frames[index].pack_forget()
        self._colour_frames[index:] = self._colour_frames[index + 1:]
        self._rebind_frame_events()

        # Updating the controller is optional because we may need to delete colours in response to
        # the controller and won't want to send events back in that case.
        if update_controller:
            self._update_colours()
    
    def _show_delete_context_menu(self, index: int, event: tk.Event):
        m = tk.Menu(self, tearoff=False)
        m.add_command(label="Delete colour", command=lambda: self._delete_colour(index))
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()
    
    def _assert_has_controller(self):
        if not self._controller:
            raise AssertionError("Trying to use the controller before it has been set!")

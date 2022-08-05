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
    def __init__(self, parent, initial_colours: List[str]):
        super().__init__(parent, background="pink")

        self._frames_container = tk.Frame(self)
        self._add_colour_button = tk.Button(self, text="+", command=self._add_colour)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self._frames_container.grid(row=0, column=0, sticky="nsew")
        self._add_colour_button.grid(row=0, column=1, sticky="nsew")

        self._frames = []

        for colour in initial_colours:
            self._add_colour(colour, update_controller=False)
        
        # The controller will be set by a later call to set_controller.
        self._controller = None
    
    def set_controller(self, controller: controller_interface.Controller):
        self._controller = controller

    def _pick_colour(self, i, event):
        _, hex_col = askcolor(color=self._frames[i]["background"])
        self._frames[i].configure(background=hex_col)
        self._update_colours()
    
    def _update_colours(self):
        self._assert_has_controller()
        self._controller.update_colours([frame["background"] for frame in self._frames])

    def _create_colour_picker_callback(self, i) -> Callable[[tk.Event], None]:
        return lambda event: self._pick_colour(i, event)

    def _create_del_context_callback(self, i) -> Callable[[tk.Event], None]:
        return lambda event: self._show_delete_context_menu(i, event)

    def _bind_events_for_frame_at_index(self, frame, index):
        frame.bind("<Button-1>", self._create_colour_picker_callback(index))
        frame.bind("<Button-3>", self._create_del_context_callback(index))    
    
    def _add_colour(self, initial_colour: str="white", update_controller: bool=True):
        index = len(self._frames)
        frame = tk.Frame(self._frames_container, background=initial_colour)
        self._frames.append(frame)
        frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self._bind_events_for_frame_at_index(frame, index)

        # Updating the controller is optional because we won't yet have a controller when this
        # method is first called (during construction).
        if update_controller:
            self._update_colours()

    def _rebind_frame_events(self):
        for index, frame in enumerate(self._frames):
            self._bind_events_for_frame_at_index(frame, index)
    
    def _delete_colour(self, index: int):
        self._frames[index].pack_forget()
        self._frames[index:] = self._frames[index + 1:]
        self._rebind_frame_events()
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

import tkinter as tk

import controller_interface
import state
import tube_view
from typing import Callable, List
import ui_model


class TubeBoardView(tk.Frame):
    """Displays the range of editable test tubes."""
    def __init__(self, parent, model: ui_model.UiModel):
        super().__init__(parent)

        self._model = model
        # This is set later by set_controller.
        self._controller = None

        self._tubes_container = tk.Frame(self)
        self._add_tube_button = tk.Button(
            self, text="+", width=10, height=10,
            command=lambda: self._add_tube(self._generate_empty_tube_state()))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self._tubes_container.grid(row=0, column=0, sticky="nsew")
        self._add_tube_button.grid(row=0, column=1, sticky="ew")

        self._tubes = []

        for tube in model.get_tube_board().tubes:
            self._add_tube(initial_state=tube.state)
    
    def set_controller(self, controller: controller_interface.Controller):
        self._controller = controller
        for tube in self._tubes:
            tube.set_controller(self._controller)
    
    def _create_del_context_callback(self, index: int) -> Callable[[tk.Event], None]:
        return lambda event: self._show_delete_context_menu(index, event)
    
    def _bind_events_for_tube_at_index(self, tube_frame: tube_view.TubeView, index: int):
        tube_frame.set_index(index)
        tube_frame.bind_context_menu_callback(self._create_del_context_callback(index))

    def _generate_empty_tube_state(self) -> List[int]:
        depth = self._model.get_tube_depth()
        return [0] * depth
    
    def _add_tube(self, initial_state: List[int]):
        index = len(self._tubes)
        tube = tube_view.TubeView(self._tubes_container, self._model, index, width=100, initial_state=initial_state)
        tube.set_controller(self._controller)
        self._tubes.append(tube)
        tube.pack(fill=tk.Y, side=tk.LEFT, expand=True, padx=20, pady=10)

        self._bind_events_for_tube_at_index(tube, index)
    
    def _rebind_tube_events(self):
        for i, tube_frame in enumerate(self._tubes):
            self._bind_events_for_tube_at_index(tube_frame, i)

    def _delete_tube(self, index: int):
        self._tubes[index].pack_forget()
        self._tubes[index:] = self._tubes[index+1:]
        self._rebind_tube_events()

    def _show_delete_context_menu(self, index: int, event: tk.Event):
        m = tk.Menu(self, tearoff=False)
        m.add_command(label="Delete tube", command=lambda: self._delete_tube(index))
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

    def notify_colours_changed(self):
        for tube in self._tubes:
            tube.notify_colours_changed()
    
    def _assert_has_controller(self):
        if not self._controller:
            raise AssertionError("Trying to use the controller before it has been set!")

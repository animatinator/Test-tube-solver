import tkinter as tk
from tkinter import filedialog

import constants
import ui_controller
import ui_model
import view


def show_save_menu(controller: ui_controller.UiController):
    chosen_path = filedialog.asksaveasfilename()
    if chosen_path is not None:
        print(f"Writing current puzzle to '{chosen_path}'")
        controller.save_state_to_file(chosen_path)


def main():
    window = tk.Tk()
    window.title('Test tube solver 3000')
    window.geometry("800x600")

    initial_colours = ["red", "green", "blue"]
    initial_tubes = 1
    model = ui_model.UiModel(
        initial_colours,
        tube_depth=constants.TUBE_DEPTH,
        initial_tubes=initial_tubes)

    main_window = view.MainWindow(window, model)
    main_window.pack(fill=tk.BOTH, expand=True)
    
    controller = ui_controller.UiController(model, main_window)
    main_window.set_controller(controller)

    menu = tk.Menu(window)
    window.config(menu=menu)
    fileMenu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="File", menu=fileMenu)
    # TODO: Add functionality for loading puzzles.
    # This will require a mechanism for resetting the colour and tube UIs to match the model.
    fileMenu.add_command(label="Open puzzle...")
    fileMenu.add_command(
        label="Save puzzle as...", command=lambda: show_save_menu(controller))

    window.mainloop()


if __name__ == '__main__':
    main()

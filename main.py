import tkinter as tk

import constants
import ui_controller
import ui_model
import view


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
    # TODO: Add functionality for saving puzzles.
    fileMenu.add_command(label="Save puzzle as...")

    window.mainloop()


if __name__ == '__main__':
    main()

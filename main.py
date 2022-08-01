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

    main_window = view.MainWindow(window, model, initial_tubes)
    main_window.pack(fill=tk.BOTH, expand=True)
    
    controller = ui_controller.UiController(model, main_window)
    main_window.set_controller(controller)

    window.mainloop()


if __name__ == '__main__':
    main()

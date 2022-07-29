import tkinter as tk

import view


def main():
    window = tk.Tk()
    window.title('Test tube solver 3000')
    window.geometry("800x600")

    main_window = view.MainWindow(window)
    main_window.pack(fill=tk.BOTH, expand=True)

    window.mainloop()


if __name__ == '__main__':
    main()

from typing import List

import controller_interface
import moves
import solver
from typing import List
import ui_model
import view


def _print_step(index: int, move: moves.Move):
    print(f"\t{index}) Move {move.src+1} to {move.dest+1}")

def _print_solution(solution: List[moves.Move]):
    if solution == None:
        print("No solution found!")
        return

    if len(solution):
        print("Solution steps:")
        for i, step in enumerate(solution):
            _print_step(i, step)
        print("Done!")
    else:
        print("Already solved!")


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

    def run_solver(self):
        puzzle = self._model.get_tube_board()
        solution = solver.solve(puzzle)
        _print_solution(solution)

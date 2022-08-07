from typing import List

import controller_interface
import moves
import solution_printer
import solver
import state
from typing import List
import ui_model
import view


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
    
    def save_state_to_file(self, filepath: str):
        state.write_to_file(
            state.SavedPuzzle(
                self._model.get_tube_board(), self._model.get_colours()),
            filepath)
    
    def load_state_from_file(self, filepath: str):
        loaded_puzzle = state.load_from_file(filepath)
        self._model.update_colours(loaded_puzzle.colours)
        self._model.update_tube_board(loaded_puzzle.board)
        self._view.reset_to_match_model()

    def run_solver(self):
        puzzle = self._model.get_tube_board()
        solution = solver.solve(puzzle)
        print(solution_printer.format_solution(solution))

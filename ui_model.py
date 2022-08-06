from typing import List

import constants
import state


class UiModel:
    """The UI model.
    
    This contains the state of the puzzle definition program.
    """
    def __init__(self,
            initial_colours: List[str],
            tube_depth: int = constants.TUBE_DEPTH,
            initial_tubes: int = 1):
        self._colours = initial_colours
        self._tube_depth = tube_depth
        self._board = state.TubeBoard(
            tubes=[state.TubeState([0]*tube_depth)]*initial_tubes)
    
    def get_colours(self) -> List[str]:
        return self._colours
    
    def get_colour_for_index(self, index: int) -> str:
        return self._colours[index]
    
    def update_colours(self, colours: List[str]):
        self._colours = colours
    
    def get_tube_board(self) -> state.TubeBoard:
        return self._board

    def update_tube_state(self, index: int, state: List[int]):
        self._board.tubes[index].state = state
    
    def add_tube(self):
        self._board.tubes.append(state.TubeState([0]*self._tube_depth))
    
    def delete_tube(self, index: int):
        self._board.tubes[index:] = self._board.tubes[index+1:]
    
    def get_tube_depth(self) -> int:
        return self._tube_depth

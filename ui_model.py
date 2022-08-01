from typing import List

import state


class UiModel:
    """The UI model.
    
    This contains the state of the puzzle definition program.
    """
    def __init__(self, initial_colours: List[str]):
        self._colours = initial_colours
    
    def get_colours(self):
        return self._colours
    
    def update_colours(self, colours: List[str]):
        self._colours = colours

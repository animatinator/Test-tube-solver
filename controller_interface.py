from abc import ABC, abstractmethod
from typing import List


class Controller(ABC):
    """Abstract base class for the UI controller.

    This allows the controller to be passed around without mutual imports.
    """
    @abstractmethod
    def update_colours(self, colours: List[str]):
        pass

    @abstractmethod
    def update_tube_state(self, index: int, state: List[int]):
        pass

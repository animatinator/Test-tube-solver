import dataclasses
import state
from typing import List


@dataclasses.dataclass
class Move:
    """Represents a move in the game.
    
    `src` is the source tube being poured into the `dest` tube, as indices into the board state.
    """
    src: int
    dest: int


def can_make_move(board: state.TubeBoard, move: Move) -> bool:
    # TODO
    return True

def apply_move(board: state.TubeBoard, move: Move) -> state.TubeBoard:
    if not can_make_move(board, move):
        raise ValueError(f"Attempting an illegal move '{move}'! Board state: {board}")
    # TODO
    return board

def get_possible_moves(board: state.TubeBoard) -> List[Move]:
    # TODO
    return []

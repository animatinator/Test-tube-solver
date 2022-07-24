import moves
import state
from typing import List


def _is_tube_solved(tube: state.TubeState) -> bool:
    return all(elem == tube.state[0] for elem in tube.state)

def is_solved(board: state.TubeBoard) -> bool:
    return all(_is_tube_solved(tube) for tube in board.tubes)


def _solve(board: state.TubeBoard, moves_made: List[moves.Move]) -> List[moves.Move]:
    if is_solved(board):
        return moves_made
    
    for move in moves.get_possible_moves(board):
        new_board = moves.apply_move(board, move)
        result = _solve(new_board, moves_made + [move])
        if result:
            return result
    
    return None

def solve(board: state.TubeBoard):
    return _solve(board, [])

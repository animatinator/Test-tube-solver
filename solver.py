import moves
import state
from typing import List


def _is_tube_solved(tube: state.TubeState) -> bool:
    return all(elem == tube.state[0] for elem in tube.state)

def is_solved(board: state.TubeBoard) -> bool:
    return all(_is_tube_solved(tube) for tube in board.tubes)


def _solve(
        board: state.TubeBoard,
        moves_made: List[moves.Move],
        seen: frozenset) -> List[moves.Move]:
    board_canonical = state.get_canonical_sorted_form(board)
    if board_canonical in seen:
        return None
    
    new_seen = seen.union(frozenset([board_canonical]))

    if is_solved(board):
        return moves_made
    
    for move in moves.get_possible_moves(board):
        new_board = moves.apply_move(board, move)
        result = _solve(new_board, moves_made + [move], new_seen)
        if result:
            return result
    
    return None

# TODO: This is unworkably slow. The branch factor is surprisingly high (mainly caused by empty
# tubes; likely wouldn't be so bad without them), and it takes over a minute to get to depth 8/9.
# Proposal: maybe most of the inefficiency of the DFS solution is caused by pointlessly moving
# between empties? Even filtering repeat states, there's still a lot of scope for moving things
# around, especially in larger puzzles.
def _solve_bfs(board: state.TubeBoard) -> List[moves.Move]:
    queue = [(board, [])]

    while len(queue):
        front_board, moves_made = queue.pop(0)

        if is_solved(front_board):
            return moves_made
    
        possible = moves.get_possible_moves(front_board)
        print(f"Branch {len(possible)}")
        for move in possible:
            print(len(moves_made + [move]))
            new_board = moves.apply_move(front_board, move)
            queue.append((new_board, moves_made + [move]))
    
    return None

def solve(board: state.TubeBoard):
    return _solve(board, [], frozenset())
    # return _solve_bfs(board)

from collections import defaultdict
import copy
import dataclasses
from itertools import combinations
import state
from typing import List, Tuple


@dataclasses.dataclass
class Move:
    """Represents a move in the game.
    
    `src` is the source tube being poured into the `dest` tube, as indices into the board state.
    """
    src: int
    dest: int

@dataclasses.dataclass
class _TopOfTube:
    """Stores computed information about a tube for possible moves.
    
    This stores the topmost colour (which would have to match the top colour of any tube
    participating in a move), how deep the topmost colour goes (which is how much space would need
    to be present in a receiving tube), and how much space is available above the topmost colour.

    The class also stores the location of the tube on the board for convenience.
    """
    top_colour: int
    depth: int
    available_space: int
    location_on_board: int


def _calculate_top_of_tube_info(tube: state.TubeState, index: int = 0) -> _TopOfTube:
    """Return the first nonempty element in the tube.
    
    Any move made onto this tube will need to match the colour of this element.
    """
    element = 0
    startIndex = -1
    for i, elem in enumerate(tube.state):
        if elem != 0:
            element = elem
            startIndex = i
            break
    
    if startIndex == -1:
        return _TopOfTube(0, 0, 4, index)
    
    depth = 1
    for i in range(startIndex + 1, len(tube.state)):
        if tube.state[i] != element:
            break
        depth += 1

    return _TopOfTube(element, depth, startIndex, index)

def _is_empty(tube: state.TubeState) -> bool:
    return all(elem == 0 for elem in tube.state)

def _get_empty_tube_indices(board: state.TubeBoard) -> List[int]:
    return [i for i, tube in enumerate(board.tubes) if _is_empty(tube)]

def get_possible_moves(board: state.TubeBoard) -> List[Move]:
    """Find all the possible moves in a given board state."""
    colours_to_tubes = defaultdict(list)
    for i, tube in enumerate(board.tubes):
        top_of_tube = _calculate_top_of_tube_info(tube, i)
        colours_to_tubes[top_of_tube.top_colour].append(top_of_tube)
    
    moves = []

    for colour in colours_to_tubes.keys():
        if len(colours_to_tubes[colour]) < 2:
            continue
        tubes_here = colours_to_tubes[colour]
        combinations = [(source, dest) for source in tubes_here for dest in tubes_here if source != dest]
        for source, dest in combinations:
            if dest.available_space >= source.depth:
                moves.append(Move(source.location_on_board, dest.location_on_board))
        pass

    # Every tube can pour into an empty tube.
    for empty_index in _get_empty_tube_indices(board):
        moves = moves + [
            Move(src=i, dest=empty_index) for i in range(len(board.tubes))
            if i != empty_index
            ]
    
    return moves

def _validate_move_bounds(board: state.TubeBoard, move: Move):
    if move.src == move.dest:
        raise ValueError(f"Error applying move {move}: source and destination of a move cannot " +
            "be equal.")
    if move.src < 0 or move.src >= len(board.tubes):
        raise ValueError(f"Error applying move {move}: source is out of range.")
    if move.dest < 0 or move.dest >= len(board.tubes):
        raise ValueError(f"Error applying move {move}: destination is out of range.")

def apply_move(board: state.TubeBoard, move: Move) -> state.TubeBoard:
    """Apply a move and return a new board with the result.
    
    This will also validate that the move is legal and raise a ValueError if not.
    """
    _validate_move_bounds(board, move)

    source_info = _calculate_top_of_tube_info(board.tubes[move.src])
    dest_info = _calculate_top_of_tube_info(board.tubes[move.dest])

    if dest_info.available_space < source_info.depth:
        raise ValueError(f"Error applying move {move}: trying to move liquid of depth " +
        f"{source_info.depth} into tube with only {dest_info.available_space} free.")

    new_board = copy.deepcopy(board)
    new_board.tubes[move.dest].state[dest_info.available_space - source_info.depth:dest_info.available_space] = [source_info.top_colour] * source_info.depth
    new_board.tubes[move.src].state[source_info.available_space:source_info.available_space + source_info.depth] = [0] * source_info.depth

    return new_board

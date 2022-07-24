from collections import defaultdict
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

def get_possible_moves(board: state.TubeBoard) -> List[Move]:
    """Find all the possible moves in a given board state."""
    # TODO: This will ignore empty tubes as possible receivers. Need to handle that.
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
    
    return moves

def apply_move(board: state.TubeBoard, move: Move) -> state.TubeBoard:
    # TODO
    return board

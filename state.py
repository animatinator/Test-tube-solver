import constants
import dataclasses
from enum import Enum
import json
from typing import List

_TUBE_STATE_KEY = "TubeState"
_TUBE_BOARD_KEY = "TubeBoard"
_COLOURS_KEY = "Colours"

@dataclasses.dataclass(eq=True)
class TubeState:
    """Represents the state of one tube on the board."""
    # Each distinct integer value represents a different colour.
    # Mapping to colours isn't important here.
    # Zero indicates that the space is empty.
    state: List[int]

    def __hash__(self):
        return hash(tuple(self.state))

@dataclasses.dataclass(eq=True)
class TubeBoard:
    """Represents the full game board."""
    tubes: List[TubeState]

    def __hash__(self):
        return hash(tuple(self.tubes))


@dataclasses.dataclass
class SavedPuzzle:
    """Represents a saved puzzle, including the board and the colour mapping."""
    board:   TubeBoard
    colours: List[str]


def encode(puzzle: SavedPuzzle) -> str:
    """Encode a puzzle as a JSON string.
    
    This is needed because default JSON encodinga/decoding doesn't handle dataclasses.
    """
    flattened = {
        _COLOURS_KEY: puzzle.colours,
        _TUBE_BOARD_KEY: [{_TUBE_STATE_KEY: tube.state} for tube in puzzle.board.tubes]}
    return json.dumps(flattened)

def decode(json_str: str) -> SavedPuzzle:
    """Decode a board from a JSON string.
    
    This is needed because default JSON encodinga/decoding doesn't handle dataclasses.
    """
    decoded = json.loads(json_str)
    if not (type(decoded) is dict and _TUBE_BOARD_KEY in decoded):
        raise ValueError(f"Could not decode JSON string '{json_str}': " +
        f"it must be a dictionary containing the key '{_TUBE_BOARD_KEY}'.")
    board = TubeBoard(tubes=[])
    tube_list = decoded[_TUBE_BOARD_KEY]
    if type(tube_list) is not list:
        raise ValueError(f"Could not decode JSON string '{json_str}': " +
        f"the key '{_TUBE_BOARD_KEY}' must map to a list of tube states.")
    for tube in tube_list:
        if not (type(tube) is dict and _TUBE_STATE_KEY in tube):
            raise ValueError(f"Could not decode JSON string '{json_str}': " +
            f"it contains an invalid tube definition '{tube}'. Tube definitions " +
            f"must be dictionary with the key '{_TUBE_STATE_KEY}'")
        values = tube[_TUBE_STATE_KEY]
        if type(values) is not list:
            raise ValueError(f"Could not decode JSON string '{json_str}': " +
            f"it contains an inavlid tube definition '{tube}'. Tube definitions " +
            "must map to lists of integers.")
        board.tubes.append(TubeState(state=values))

    if _COLOURS_KEY not in decoded:
        raise ValueError(f"Could not load colours from JSON string '{json_str}: '" +
        f"it must contain the key '{_COLOURS_KEY}'.")
    colours = decoded[_COLOURS_KEY]
    if type(colours) is not list:
        raise ValueError(f"Could not load colours from JSON string '{json_str}: '" +
        f"the key '{_COLOURS_KEY}' must map to a list of colours.")

    return SavedPuzzle(board, colours)


def write_to_file(board: SavedPuzzle, filepath: str):
    with open(filepath, "w") as outfile:
        outfile.write(encode(board))

def load_from_file(filepath: str) -> SavedPuzzle:
    with open(filepath, "r") as infile:
        content = "".join(infile.readlines())
        return decode(content)

def get_canonical_sorted_form(board: TubeBoard) -> TubeBoard:
    return TubeBoard(tubes=sorted(
        board.tubes,
        key=lambda tube: ''.join(str(elem) for elem in tube.state)))

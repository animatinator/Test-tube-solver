import constants
import dataclasses
from enum import Enum
import json
from typing import List

_TUBE_STATE_KEY = "TubeState"
_TUBE_BOARD_KEY = "TubeBoard"

@dataclasses.dataclass
class TubeState:
    """Represents the state of one tube on the board."""
    # Each distinct integer value represents a different colour.
    # Mapping to colours isn't important here.
    # Zero indicates that the space is empty.
    state: List[int]

@dataclasses.dataclass
class TubeBoard:
    """Represents the full game board."""
    tubes: List[TubeState]


def encode(board: TubeBoard) -> str:
    """Encode a board as a JSON string.
    
    This is needed because default JSON encodinga/decoding doesn't handle dataclasses.
    """
    flattened = {"TubeBoard": [{"TubeState": tube.state} for tube in board.tubes]}
    return json.dumps(flattened)

def decode(json_str: str) -> TubeBoard:
    """Decode a board from a JSON string.
    
    This is needed because default JSON encodinga/decoding doesn't handle dataclasses.
    """
    decoded = json.loads(json_str)
    if not (type(decoded) is dict and _TUBE_BOARD_KEY in decoded):
        raise ValueError(f"Could not decode JSON string '{json_str}': " +
        f"it must be a dictionary whose first key is '{_TUBE_BOARD_KEY}'.")
    board = TubeBoard(tubes=[])
    tube_list = decoded[_TUBE_BOARD_KEY]
    if type(tube_list) is not list:
        raise ValueError(f"Could not decode JSON string '{json_str}': " +
        f"the key '{_TUBE_BOARD_KEY}' must map to a list of tube states.")
    for tube in tube_list:
        if not (type(tube) is dict and _TUBE_STATE_KEY in tube):
            raise ValueError(f"Could not decode JSON string '{json_string}': " +
            f"it contains an invalid tube definition '{tube}'. Tube definitions " +
            f"must be dictionaries with the key '{_TUBE_STATE_KEY}'")
        values = tube[_TUBE_STATE_KEY]
        board.tubes.append(TubeState(state=values))
    return board


def create_empty_state():
    board = TubeBoard(tubes=[])
    for i in range(constants.NUM_TUBES):
        board.tubes.append(TubeState(state=[0]*constants.TUBE_DEPTH))
    return board

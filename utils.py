import colour_mapping
import constants
from random import randrange
import state


def create_empty_state() -> state.TubeBoard:
    board = state.TubeBoard(tubes=[])
    for i in range(constants.NUM_TUBES):
        board.tubes.append(state.TubeState(state=[0]*constants.TUBE_DEPTH))
    return board

def create_random_state() -> state.TubeBoard:
    board = state.TubeBoard(tubes = [])
    for i in range(constants.NUM_TUBES):
        new_state = state.TubeState(state=[])
        for i in range(constants.TUBE_DEPTH):
            new_state.state.append(randrange(1, len(colour_mapping._COLOURS)))
        board.tubes.append(new_state)
    return board

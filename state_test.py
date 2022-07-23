import constants
import json
import state
import unittest

class TestState(unittest.TestCase):
    def test_empty_state(self):
        board = state.create_empty_state()
        self.assertEqual(len(board.tubes), constants.NUM_TUBES)
        self.assertEqual(len(board.tubes[0].state), constants.TUBE_DEPTH)

    def test_serialisation(self):
        board = state.create_empty_state()
        board.tubes[2].state[3] = 4
        new_board = state.decode(state.encode(board))
        self.assertEqual(board, new_board)

if __name__ == '__main__':
    unittest.main()

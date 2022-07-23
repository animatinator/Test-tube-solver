import constants
import json
import os
import state
import unittest


_EMPTY_BOARD_PATH = "boards/empty.json"
_TEMPDIR = "boards/test_data"


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


class TestFileReadWrite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.mkdir(_TEMPDIR)

    @classmethod
    def tearDownClass(cls):
        os.rmdir(_TEMPDIR)

    def test_load_empty_state(self):
        loaded_board = state.load_from_file(_EMPTY_BOARD_PATH)
        self.assertEqual(loaded_board, state.create_empty_state())
    
    def test_write_then_read(self):
        board = state.create_empty_state()
        board.tubes[2].state[3] = 4

        filepath = os.path.join(_TEMPDIR, "tmpfile.json")
        state.write_to_file(board, filepath)
        loaded_board = state.load_from_file(filepath)

        self.assertEqual(loaded_board, board)

        os.remove(filepath)

if __name__ == '__main__':
    unittest.main()

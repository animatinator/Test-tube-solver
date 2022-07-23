import constants
import json
import os
import state
import unittest
import utils


_EMPTY_BOARD_PATH = "boards/empty.json"
_TEMPDIR = "boards/test_data"


class TestState(unittest.TestCase):
    def test_empty_state(self):
        board = utils.create_empty_state()
        self.assertEqual(len(board.tubes), constants.NUM_TUBES)
        self.assertEqual(len(board.tubes[0].state), constants.TUBE_DEPTH)

    def test_serialisation(self):
        board = utils.create_empty_state()
        board.tubes[2].state[3] = 4
        new_board = state.decode(state.encode(board))
        self.assertEqual(board, new_board)
    
    def test_deserialisation_not_dict(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("[1, 2, 3]")
        self.assertIn("must be a dictionary", str(ve.exception))
    
    def test_deserialisation_bad_key(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"Test\": [1, 2, 3]}")
        self.assertIn("whose first key is 'TubeBoard'", str(ve.exception))
    
    def test_deserialisation_bad_tubes_list(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"TubeBoard\": 49}")
        self.assertIn("must map to a list of tube states", str(ve.exception))
    
    def test_deserialisation_bad_tube_in_list(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"TubeBoard\": [{\"TubeState\": [1,2,3]}, {\"BadState\": [1,2,3]}]}")
        self.assertIn("must be dictionaries with the key 'TubeState'", str(ve.exception))
    
    def test_deserialisation_bad_tube_in_list(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"TubeBoard\": [{\"TubeState\": 12345}]}")
        self.assertIn("must map to lists of integers", str(ve.exception))


class TestFileReadWrite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.mkdir(_TEMPDIR)

    @classmethod
    def tearDownClass(cls):
        os.rmdir(_TEMPDIR)

    def test_load_empty_state(self):
        loaded_board = state.load_from_file(_EMPTY_BOARD_PATH)
        self.assertEqual(loaded_board, utils.create_empty_state())
    
    def test_write_then_read(self):
        board = utils.create_empty_state()
        board.tubes[2].state[3] = 4

        filepath = os.path.join(_TEMPDIR, "tmpfile.json")
        state.write_to_file(board, filepath)
        loaded_board = state.load_from_file(filepath)

        self.assertEqual(loaded_board, board)

        os.remove(filepath)

if __name__ == '__main__':
    unittest.main()

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
        colours = ["red", "blue", "green"]
        board.tubes[2].state[3] = 4
        decoded_state = state.decode(state.encode(state.SavedPuzzle(board, colours)))
        self.assertEqual(board, decoded_state.board)
        self.assertEqual(colours, decoded_state.colours)
    
    def test_deserialisation_not_dict(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("[1, 2, 3]")
        self.assertIn("must be a dictionary", str(ve.exception))
    
    def test_deserialisation_bad_key(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"Test\": [1, 2, 3]}")
        self.assertIn("containing the key 'TubeBoard'", str(ve.exception))
    
    def test_deserialisation_bad_tubes_list(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"TubeBoard\": 49}")
        self.assertIn("must map to a list of tube states", str(ve.exception))
    
    def test_deserialisation_bad_tube_in_list(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"TubeBoard\": [{\"TubeState\": [1,2,3]}, {\"BadState\": [1,2,3]}]}")
        self.assertIn("must be dictionaries with the key 'TubeState'", str(ve.exception))
    
    def test_deserialisation_bad_tube_mapping_in_list(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"TubeBoard\": [{\"TubeState\": 12345}]}")
        self.assertIn("must map to lists of integers", str(ve.exception))
    
    def test_deserialisation_no_colours(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"TubeBoard\": [{\"TubeState\": [1, 2, 3, 4]}]}")
        self.assertIn("must contain the key 'Colours'", str(ve.exception))
    
    def test_deserialisation_colours_not_a_list(self):
        with self.assertRaises(ValueError) as ve:
            state.decode("{\"Colours\": \"red\", \"TubeBoard\": [{\"TubeState\": [1]}]}")
        self.assertIn("'Colours' must map to a list of colours", str(ve.exception))


class TestFileReadWrite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.mkdir(_TEMPDIR)

    @classmethod
    def tearDownClass(cls):
        os.rmdir(_TEMPDIR)

    def test_load_empty_state(self):
        loaded_puzzle = state.load_from_file(_EMPTY_BOARD_PATH)
        self.assertEqual(loaded_puzzle.board, utils.create_empty_state())
    
    def test_write_then_read(self):
        colours = ["red", "green", "blue"]
        board = utils.create_empty_state()
        board.tubes[2].state[3] = 4

        filepath = os.path.join(_TEMPDIR, "tmpfile.json")

        try:
            state.write_to_file(state.SavedPuzzle(board, colours), filepath)
            loaded_puzzle = state.load_from_file(filepath)

            self.assertEqual(loaded_puzzle.board, board)
            self.assertEqual(loaded_puzzle.colours, colours)
        finally:
            os.remove(filepath)


class TestCanonicalSortedForm(unittest.TestCase):
    def test_sorted(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[1, 2, 3, 4]),
            state.TubeState(state=[0, 2, 2, 3]),
            state.TubeState(state=[0, 1, 2, 3]),
        ])
        expected = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 1, 2, 3]),
            state.TubeState(state=[0, 2, 2, 3]),
            state.TubeState(state=[1, 2, 3, 4]),
        ])

        self.assertEqual(expected, state.get_canonical_sorted_form(board))

if __name__ == '__main__':
    unittest.main()

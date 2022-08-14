import moves
import os
import state
import unittest
import utils


_TEMPDIR = "solutions/test_data"
_EMPTY_SOLUTION_PATH = "solutions/empty.json"


class TestTopOfTubeInfo(unittest.TestCase):
    def test_empty_tube(self):
        tube = state.TubeState(state=[0, 0, 0, 0])
        self.assertEqual(
            moves._TopOfTube(0, 0, 4, 0),
            moves._calculate_top_of_tube_info(tube))

    def test_single_element(self):
        tube = state.TubeState(state=[0, 0, 4, 1, 1, 3, 4, 2])
        self.assertEqual(
            moves._TopOfTube(4, 1, 2, 0),
            moves._calculate_top_of_tube_info(tube))

    def test_longer_run(self):
        tube = state.TubeState(state=[0, 0, 1, 1, 1, 3, 4, 2, 1])
        self.assertEqual(
            moves._TopOfTube(1, 3, 2, 0),
            moves._calculate_top_of_tube_info(tube))


class TestEmptyTubes(unittest.TestCase):
    def test_no_empty_tubes(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 2]),
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        self.assertEqual([], moves._get_empty_tube_indices(board))
        
    def test_two_empty_tubes(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 0])
        ])
        self.assertEqual([0, 2], moves._get_empty_tube_indices(board))
 

class TestPossibleMoves(unittest.TestCase):   
    def test_single_possible_move(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 2]),
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        self.assertEqual([moves.Move(1, 0)], moves.get_possible_moves(board))
    
    def test_multiple_possible_moves(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 2]),
            state.TubeState(state=[0, 0, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        self.assertEqual([moves.Move(1, 2), moves.Move(2, 1)], moves.get_possible_moves(board))
    
    def test_no_possible_moves(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 1, 1, 1]),
            state.TubeState(state=[0, 1, 1, 1]),
            state.TubeState(state=[0, 1, 1, 1])
        ])
        self.assertEqual([], moves.get_possible_moves(board))
    
    def test_can_move_into_empty_tube(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[2, 2, 1, 1])
        ])
        self.assertEqual([moves.Move(0, 1), moves.Move(2, 1)], moves.get_possible_moves(board))
    
    def test_two_empty_tubes(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[0, 0, 0, 0])
        ])
        self.assertEqual(4, len(moves.get_possible_moves(board)))
    
    def test_do_not_pour_empty_into_empty(self):
        # If we were to generate moves for pouring empty tubes into empty tubes, we could end up
        # infinitely recursing.
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[0, 0, 0, 0])
        ])
        self.assertEqual([], moves.get_possible_moves(board))


class TestApplyMove(unittest.TestCase):
    def test_illegal_move_same_index(self):
        board = utils.create_empty_state()
        with self.assertRaises(ValueError) as ve:
            moves.apply_move(board, moves.Move(1, 1))
        self.assertIn("source and destination of a move cannot be equal", str(ve.exception))

    def test_illegal_move_source_out_of_range(self):
        board = utils.create_empty_state()
        with self.assertRaises(ValueError) as ve:
            moves.apply_move(board, moves.Move(-1, 1))
        self.assertIn("source is out of range", str(ve.exception))

    def test_illegal_move_destination_out_of_range(self):
        board = utils.create_empty_state()
        with self.assertRaises(ValueError) as ve:
            moves.apply_move(board, moves.Move(1, 1000))
        self.assertIn("destination is out of range", str(ve.exception))

    def test_illegal_move_not_enough_space(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 2]),
            state.TubeState(state=[1, 1, 1, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        with self.assertRaises(ValueError) as ve:
            moves.apply_move(board, moves.Move(1, 0))
        self.assertIn(
            "trying to move liquid of depth 3 into tube with only 2 free",
            str(ve.exception))

    def test_apply_simple_move(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 2]),
            state.TubeState(state=[1, 2, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        want_board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 1, 1, 2]),
            state.TubeState(state=[0, 2, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        got_board = moves.apply_move(board, moves.Move(1, 0))
        self.assertEqual(want_board, got_board)
        
    def test_move_with_depth(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 2]),
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        want_board = state.TubeBoard(tubes=[
            state.TubeState(state=[1, 1, 1, 2]),
            state.TubeState(state=[0, 0, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        got_board = moves.apply_move(board, moves.Move(1, 0))
        self.assertEqual(want_board, got_board)
    
    def test_move_does_not_modify_original_board(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 2]),
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        want_original_board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 2]),
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 2])
        ])
        moves.apply_move(board, moves.Move(1, 0))
        self.assertEqual(want_original_board, board)


class TestSerialisation(unittest.TestCase):
    def test_empty_serialisation(self):
        solution = []
        self.assertEqual("{\"Solution\": []}", moves.encode_solution(solution))
    
    def test_serialisation(self):
        solution = [moves.Move(1, 2), moves.Move(2, 1)]
        decoded_solution = moves.decode_solution(moves.encode_solution(solution))
        self.assertEqual(decoded_solution, solution)
    
    def test_serialisation_not_dict(self):
        with self.assertRaises(ValueError) as ve:
            moves.decode_solution("[1, 2, 3]")
        self.assertIn("must be a dictionary", str(ve.exception))
    
    def test_serialisation_bad_key(self):
        with self.assertRaises(ValueError) as ve:
            moves.decode_solution("{\"Test\": [1, 2, 3]}")
        self.assertIn("containing the key 'Solution'", str(ve.exception))
    
    def test_serialisation_bad_moves_list(self):
        with self.assertRaises(ValueError) as ve:
            moves.decode_solution("{\"Solution\": 24601}")
        self.assertIn("must map to a list of moves", str(ve.exception))
    
    def test_serialisation_bad_move_in_list(self):
        with self.assertRaises(ValueError) as ve:
            moves.decode_solution("{\"Solution\": [[1, 2], [3, 4], 12345]}")
        self.assertIn("must be (int, int) pairs.", str(ve.exception))
    
    def test_serialisation_wrong_length_move_in_list(self):
        with self.assertRaises(ValueError) as ve:
            moves.decode_solution("{\"Solution\": [[1, 2], [3, 4], [5, 6, 7]]}")
        self.assertIn("must be (int, int) pairs.", str(ve.exception))


class TestFileReadWrite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.mkdir(_TEMPDIR)

    @classmethod
    def tearDownClass(cls):
        os.rmdir(_TEMPDIR)

    def test_load_empty_solution(self):
        loaded_solution = moves.load_solution_from_file(_EMPTY_SOLUTION_PATH)
        self.assertEqual(loaded_solution, [])
    
    def test_write_then_read(self):
        solution = [moves.Move(1, 2), moves.Move(3, 4)]

        filepath = os.path.join(_TEMPDIR, "tmpfile.json")

        try:
            moves.write_solution_to_file(solution, filepath)
            loaded_solution = moves.load_solution_from_file(filepath)

            self.assertEqual(loaded_solution, solution)
        finally:
            os.remove(filepath)


if __name__ == '__main__':
    unittest.main()

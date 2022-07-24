import moves
import state
import unittest
import utils


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


if __name__ == '__main__':
    unittest.main()

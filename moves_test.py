import moves
import state
import unittest


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
 

class TestMoves(unittest.TestCase):   
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

if __name__ == '__main__':
    unittest.main()

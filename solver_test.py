import moves
import solver
import state
import unittest


class TestIsSolved(unittest.TestCase):

    def test_solved_tube(self):
        tube = state.TubeState(state=[1, 1, 1, 1])
        self.assertTrue(solver._is_tube_solved(tube))

    def test_unsolved_tube(self):
        tube = state.TubeState(state=[1, 1, 0, 1])
        self.assertFalse(solver._is_tube_solved(tube))

    def test_solved_board(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[1, 1, 1, 1]),
            state.TubeState(state=[2, 2, 2, 2])
        ])
        self.assertTrue(solver.is_solved(board))

    def test_unsolved_board(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[1, 1, 3, 1]),
            state.TubeState(state=[2, 2, 2, 2])
        ])
        self.assertFalse(solver.is_solved(board))


class SolverTest(unittest.TestCase):

    def test_simple_solve(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 1]),
            state.TubeState(state=[0, 0, 1, 1]),
            state.TubeState(state=[2, 2, 2, 2])
        ])
        self.assertEqual(solver.solve(board), [moves.Move(0, 1)])


if __name__ == '__main__':
    unittest.main()

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

    def test_one_step_solve(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[0, 0, 1, 1]),
            state.TubeState(state=[0, 0, 1, 1]),
            state.TubeState(state=[2, 2, 2, 2])
        ])
        self.assertEqual(solver.solve(board), [moves.Move(0, 1)])
    
    def test_three_step_solve(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[1, 1, 2, 2]),
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[2, 2, 1, 1])
        ])
        self.assertEqual(
            solver.solve(board),
            [moves.Move(0, 1), moves.Move(2, 0), moves.Move(1, 2)])

    def test_longer_solution(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[1, 1, 2, 3]),
            state.TubeState(state=[2, 3, 2, 3]),
            state.TubeState(state=[1, 2, 3, 1]),
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[0, 0, 0, 0])
        ])
        solution = solver.solve(board)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 10)

    def test_improvement_with_canonical_sorted_state(self):
        board = state.TubeBoard(tubes=[
            state.TubeState(state=[1, 2, 3, 4]),
            state.TubeState(state=[1, 2, 4, 3]),
            state.TubeState(state=[5, 3, 5, 1]),
            state.TubeState(state=[2, 5, 1, 3]),
            state.TubeState(state=[2, 5, 4, 4]),
            state.TubeState(state=[0, 0, 0, 0]),
            state.TubeState(state=[0, 0, 0, 0])
        ])
        solution = solver.solve(board)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 18)  # Previously 23


if __name__ == '__main__':
    unittest.main()

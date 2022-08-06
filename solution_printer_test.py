import moves
import solution_printer
import unittest


class SolutionPrinterTest(unittest.TestCase):
    def test_no_solution(self):
        want = "No solution found!"
        self.assertEqual(want, solution_printer.format_solution(None))
    
    def test_already_solved(self):
        want = "Already solved!"
        self.assertEqual(want, solution_printer.format_solution([]))
    
    def test_multi_step_solution(self):
        want = """
Solution steps:
\t1) Move 1 to 3
\t2) Move 2 to 3
\t3) Move 3 to 1
Done!"""[1:]  # Drop the newline used for readability.
        solution = [
            moves.Move(0, 2),
            moves.Move(1, 2),
            moves.Move(2, 0),
        ]
        self.assertEqual(want, solution_printer.format_solution(solution))


if __name__ == "__main__":
    unittest.main()
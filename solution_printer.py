import moves
from typing import List


def _format_step(index: int, move: moves.Move):
    return f"\t{index+1}) Move {move.src+1} to {move.dest+1}"

def format_solution(solution: List[moves.Move]):
    if solution == None:
        return "No solution found!"

    if len(solution):
        result = "Solution steps:\n"
        for i, step in enumerate(solution):
            result += _format_step(i, step) + "\n"
        result += "Done!"
        return result
    else:
        return "Already solved!"

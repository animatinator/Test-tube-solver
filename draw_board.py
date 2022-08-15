import argparse
import constants
import moves
import pygame
import state
from typing import List, Tuple

import pdb

_BG_COLOUR = (0, 0, 0)

# Horizontal and vertical spacing as fractions of the tube width and height.
_TUBE_HSPACING_TO_WIDTH: float = 0.5
_TUBE_VSPACING_TO_HEIGHT: float = 0.3
# The ratio of padding around the board to the size of the board
_BOARD_PADDING_RATIO_TO_SIZE = 0.2

_NUM_ROWS = constants.NUM_ROWS

_STARTING_SIZE = (500, 400)


class GameBoardView():
    def __init__(self, board: state.TubeBoard, colours: List[str]):
        self.set_state(board, colours)

    def set_state(self, board: state.TubeBoard, colours: List[str]):
        self._board = board
        self._colours = colours

        self._tubes_per_row: int = int((len(board.tubes) + _NUM_ROWS - 1) / _NUM_ROWS)
        self._tube_depth: int = len(board.tubes[0].state)

        # Calculate the relative width and height of the board.
        # Units are effectively tube widths.
        # e.g. width is num tubes + (num padding * padding as fraction of tube width)
        self._relative_width: float = float(self._tubes_per_row) + (self._tubes_per_row - 1) * _TUBE_HSPACING_TO_WIDTH
        self._relative_height: float = float(_NUM_ROWS * self._tube_depth) + (_NUM_ROWS - 1) * self._tube_depth * _TUBE_VSPACING_TO_HEIGHT
    
    def draw_tube(self,
            surface: pygame.Surface,
            tube_state: state.TubeState,
            position: Tuple[int, int],
            size: Tuple[int, int]):
        elements_per_tube = len(tube_state.state)
        tube_height = size[1]

        for i, element in enumerate(tube_state.state):
            # Draw between this position and the next to avoid gaps due to rounding.
            ypos = position[1] + (i/elements_per_tube) * tube_height
            next_ypos = position[1] + ((i+1)/elements_per_tube) * tube_height

            colour = 'black' if element == 0 else self._colours[element - 1]
            colour = pygame.Color(colour)

            pygame.draw.rect(
                surface, colour,
                pygame.Rect(position[0], ypos, size[0], (next_ypos - ypos) + 1))
    
    def _compute_board_rect(self, screen_dims: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Returns ((width, height), (left, top))."""
        aspect_ratio = screen_dims[0] / screen_dims[1]

        # Relative horizontal and vertical once we include padding.
        relative_padded_width: float = self._relative_width * (1.0 + _BOARD_PADDING_RATIO_TO_SIZE)
        relative_padded_height: float = self._relative_height * (1.0 + _BOARD_PADDING_RATIO_TO_SIZE)
        # Aspect ratio of the board itself
        board_aspect_ratio = self._relative_width / self._relative_height

        if aspect_ratio > board_aspect_ratio:
            # Vertically constrained
            screen_height = screen_dims[1]
            height = int(screen_height * (self._relative_height / relative_padded_height))
            width = int(height * board_aspect_ratio)
            pass
        else:
            # Horizontally constrained
            screen_width = screen_dims[0]
            width = int(screen_width * (self._relative_width / relative_padded_width))
            height = int(width / board_aspect_ratio)
            pass
        topleft = (screen_dims[0] / 2 - width / 2, screen_dims[1] / 2 - height / 2)
        return ((width, height), topleft)

    def draw(self, surface: pygame.Surface):
        ((width, height), topleft) = self._compute_board_rect((surface.get_width(), surface.get_height()))

        # RELATIVE_WIDTH is in units of test tube width.
        tube_width = width / self._relative_width
        tube_height = self._tube_depth * tube_width
        hspacing = _TUBE_HSPACING_TO_WIDTH * tube_width
        vspacing = _TUBE_VSPACING_TO_HEIGHT * tube_height

        tube_index = 0
        for row in range(_NUM_ROWS):
            for tube in range(self._tubes_per_row):
                # Handle the case where the number of tubes doesn't evenly divide into rows.
                if tube_index >= len(self._board.tubes):
                    break

                xpos = topleft[0] + tube * (tube_width + hspacing)
                ypos = topleft[1] + row * (tube_height + vspacing)
                self.draw_tube(
                    surface,
                    self._board.tubes[tube_index],
                    (xpos, ypos),
                    (tube_width, tube_height))
                tube_index += 1


class BoardDisplayApp:
    """Controls the application's main loop.

    This sets up Pygame, handles events and delegates to the GameBoardView for drawing.
    """
    def __init__(
            self,
            board: state.TubeBoard,
            colours: List[str],
            solution: List[moves.Move],
            size: Tuple[int, int]):
        self._board = board
        self._colours = colours

        self._solution = solution

        self._size = size
        self._board_view = GameBoardView(board, colours)

        self._clock = pygame.time.Clock()

        self._solution_index = 0
        self._solution_frames = self._generate_solution_frames(self._board, self._solution)

    def _generate_solution_frames(self, board: state.TubeBoard, solution: List[moves.Move]) -> List[state.TubeBoard]:
        frames = [board]
        for i in range(0, len(solution)):
            frames.append(moves.apply_move(frames[i], solution[i]))
        return frames

    def run(self):
        pygame.init()
        surface = pygame.display.set_mode(self._size, pygame.RESIZABLE)
        pygame.display.set_caption("Test tube solver: board view")

        running = True

        while running:
            surface.fill(_BG_COLOUR)

            self._board_view.draw(surface)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    self._size = (event.w, event.h)
                    surface = pygame.display.set_mode(self._size, pygame.RESIZABLE)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self._solution_index > 0:
                        self._solution_index -= 1
                        self._board_view.set_state(self._solution_frames[self._solution_index], self._colours)
                    elif event.key == pygame.K_RIGHT and self._solution_index < len(self._solution_frames) - 1:
                        self._solution_index += 1
                        self._board_view.set_state(self._solution_frames[self._solution_index], self._colours)

            self._clock.tick(10)

        pygame.quit()


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description='Display a test tube game solution.')
    parser.add_argument(
        '--board_path', action='store', type=str, required=False,
        help='The path to the board to display. Not compatible with --board.')
    parser.add_argument(
        '--board', action='store', type=str, required=False,
        help='The encoded board to display. Not compatible with --board_path.')
    parser.add_argument(
        '--solution', action='store', type=str, required=False,
        help='The solution to display')
    args = parser.parse_args()

    if (args.board_path is not None) == (args.board is not None):
        raise ValueError("Must specify exactly one of --board or --board_path.")

    if args.board_path is not None:
        loaded_state = state.load_from_file(args.board_path)
    else:
        assert(args.board is not None)
        loaded_state = state.decode(args.board)
    solution = moves.decode_solution(args.solution) if args.solution else []
    app = BoardDisplayApp(loaded_state.board, loaded_state.colours, solution, size=_STARTING_SIZE)
    app.run()

import colour_mapping
import constants
import pygame
import state
from typing import Tuple


# TODO: Make dynamically configurable.
_BOARD_PATH = "boards/random.json"

_BG_COLOUR = (0, 0, 0)

# Horizontal and vertical spacing as fractions of the tube width and height.
_TUBE_HSPACING_TO_WIDTH: float = 0.5
_TUBE_VSPACING_TO_HEIGHT: float = 0.3
# The ratio of padding around the board to the size of the board
_BOARD_PADDING_RATIO_TO_SIZE = 0.2

_NUM_ROWS = constants.NUM_ROWS

size = (500, 400)

pygame.init()
surface = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Test tube solver: board view")


class GameBoardView():
    def __init__(self, board: state.TubeBoard):
        self._board = board

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
        element_size = size[1] / len(tube_state.state)
        for i, element in enumerate(tube_state.state):
            ypos = position[1] + i * element_size
            colour = colour_mapping.map_colour(element)
            pygame.draw.rect(
                surface, colour,
                pygame.Rect(position[0], ypos, size[0], element_size))
    
    def _compute_board_rect(self, screen_dims: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
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
        ((width, height), topleft) = self._compute_board_rect(size)

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


board = state.load_from_file(_BOARD_PATH).board
board_view = GameBoardView(board)

clock = pygame.time.Clock()

running = True

while running:
    surface.fill(_BG_COLOUR)

    board_view.draw(surface)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            size = (event.w, event.h)
            surface = pygame.display.set_mode(size, pygame.RESIZABLE)

    clock.tick(10)

pygame.quit()

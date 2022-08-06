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

# Tube height:width ratio. Just the depth of the tube, so that each element in the tube is square.
_TUBE_HEIGHT_TO_WIDTH: int = constants.TUBE_DEPTH
_NUM_ROWS = constants.NUM_ROWS
_TUBES_PER_ROW: int = int((constants.NUM_TUBES + _NUM_ROWS - 1) / _NUM_ROWS)
# Calculate the relative width and height of the board.
# Units are effectively tube widths.
# e.g. width is num tubes + (num padding * padding as fraction of tube width)
_RELATIVE_WIDTH: float = float(_TUBES_PER_ROW) + (_TUBES_PER_ROW - 1) * _TUBE_HSPACING_TO_WIDTH
_RELATIVE_HEIGHT: float = float(_NUM_ROWS * _TUBE_HEIGHT_TO_WIDTH) + (_NUM_ROWS - 1) * _TUBE_HEIGHT_TO_WIDTH * _TUBE_VSPACING_TO_HEIGHT
# Aspect ratio of the board itself
_BOARD_ASPECT_RATIO = _RELATIVE_WIDTH / _RELATIVE_HEIGHT
# Relative sizes once we include padding.
_RELATIVE_PADDED_WIDTH: float = _RELATIVE_WIDTH * (1.0 + _BOARD_PADDING_RATIO_TO_SIZE)
_RELATIVE_PADDED_HEIGHT: float = _RELATIVE_HEIGHT * (1.0 + _BOARD_PADDING_RATIO_TO_SIZE)

size = (500, 400)

pygame.init()
surface = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Test tube solver: board view")


class GameBoardView():
    def __init__(self, board: state.TubeBoard):
        self._board = board
    
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

    def draw(self, surface: pygame.Surface):
        aspect_ratio = size[0] / size[1]
        if aspect_ratio > _BOARD_ASPECT_RATIO:
            # Vertically constrained
            screen_height = size[1]
            height = int(screen_height * (_RELATIVE_HEIGHT / _RELATIVE_PADDED_HEIGHT))
            width = int(height * _BOARD_ASPECT_RATIO)
            pass
        else:
            # Horizontally constrained
            screen_width = size[0]
            width = int(screen_width * (_RELATIVE_WIDTH / _RELATIVE_PADDED_WIDTH))
            height = int(width / _BOARD_ASPECT_RATIO)
            pass
        topleft = (size[0] / 2 - width / 2, size[1] / 2 - height / 2)

        # RELATIVE_WIDTH is in units of test tube width.
        tube_width = width / _RELATIVE_WIDTH
        tube_height = _TUBE_HEIGHT_TO_WIDTH * tube_width
        hspacing = _TUBE_HSPACING_TO_WIDTH * tube_width
        vspacing = _TUBE_VSPACING_TO_HEIGHT * tube_height

        tube_index = 0
        for row in range(_NUM_ROWS):
            for tube in range(_TUBES_PER_ROW):
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

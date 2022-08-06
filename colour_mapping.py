from typing import List, Tuple

_COLOURS: List[Tuple[int, int, int]] = [
    [0, 0, 0],
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [255, 255, 0],
    [0, 255, 255],
    [255, 0, 255],
]

def map_colour(colour: int) -> Tuple[int, int, int]:
    return _COLOURS[colour]


def _convert_to_hex(colour: Tuple[int, int, int]) -> str:
    return '#' + ''.join(['%0.2x' % value for value in colour])

def get_default_colours() -> List[str]:
    return [_convert_to_hex(colour) for colour in _COLOURS]

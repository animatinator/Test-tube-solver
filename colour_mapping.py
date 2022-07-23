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

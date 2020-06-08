from enum import Enum

HEADER_V5 = b"reMarkable .lines file, version=5          "


class Colour(Enum):
    BLACK = 0
    GREY = 1
    WHITE = 2


class Pen(Enum):
    # see https://github.com/ax3l/lines-are-beautiful/blob/develop/include/rmlab/Line.hpp
    BRUSH = 0
    PENCIL_TILT = 1
    BALLPOINT_PEN_1 = 2
    MARKER_1 = 3
    FINELINER_1 = 4
    HIGHLIGHTER = 5
    RUBBER = 6  # used in version 5
    PENCIL_SHARP = 7
    RUBBER_AREA = 8
    ERASE_ALL = 9
    SELECTION_BRUSH_1 = 10
    SELECTION_BRUSH_2 = 11
    # below used for version 5
    PAINT_BRUSH_1 = 12
    MECHANICAL_PENCIL_1 = 13
    PENCIL_2 = 14
    BALLPOINT_PEN_2 = 15
    MARKER_2 = 16
    FINELINER_2 = 17
    HIGHLIGHTER_2 = 18
    DEFAULT = FINELINER_2


class Width(Enum):
    SMALL = 1.875
    MEDIUM = 2.0
    LARGE = 2.125


X_MAX, Y_MAX = 1404.0, 1872.0

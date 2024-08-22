# Local imports.

# External imports.
from enum import Enum
from math import cos, sin, pi


# Enums.
class ColumnTypes(Enum):
    RECTANGULAR = 0
    CIRCULAR = 1


class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class ElementTypes(Enum):
    BAR = 0
    STIRRUP = 1
    BEAM = 2
    COLUMN = 3


class Orientation(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


STEEL_WEIGHT = 7850  # kg / m3

COS45 = cos(45 * pi / 180)
SIN45 = sin(45 * pi / 180)

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
    CADTABLE = 21


class Orientation(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


STEEL_WEIGHT = 7850  # kg / m3

COS45 = cos(45 * pi / 180)
SIN45 = sin(45 * pi / 180)

BEAM_SET_TRANSVERSE = {"text_dim_distance": 0.05,
                       "text_dim_height": 0.05}

BEAM_SET_LONG_REBAR = {"text_height": 0.05}

COLUMN_SET_TRANSVERSE = {"text_dim_distance": 0.05,
                         "text_dim_height": 0.05}

COLUMN_SET_LONG_REBAR = {"text_height": 0.05}

CADTABLE_SET_DEFAULT = {"row_height": 0.3, "column_width": 0.6}

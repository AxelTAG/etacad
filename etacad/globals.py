# Local imports.

# External imports.
from enum import Enum
from math import cos, sin, pi


# Enums.
class Aligment(Enum):
    MTEXT_TOP_LEFT = 1
    MTEXT_TOP_CENTER = 2
    MTEXT_TOP_RIGHT = 3
    MTEXT_MIDDLE_LEFT = 4
    MTEXT_MIDDLE_CENTER = 5
    MTEXT_MIDDLE_RIGHT = 6
    MTEXT_BOTTOM_LEFT = 7
    MTEXT_BOTTOM_CENTER = 8
    MTEXT_BOTTOM_RIGHT = 9


class ColumnTypes(Enum):
    RECTANGULAR = 0
    CIRCULAR = 1


class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class DRotation(Enum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1


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


# Specific weights.
STEEL_WEIGHT = 7850  # kg / m3

CONCRETE_WEIGHT = 2400  # kg / m3

# General constants.
COS45 = cos(45 * pi / 180)
SIN45 = sin(45 * pi / 180)

# Settings dictionaries.
# Concrete.
CONCRETE_SET_TRANSVERSE = {"text_dim_distance_horizontal": 0.25,
                           "text_dim_distance_vertical": 0.25,
                           "text_dim_inner_perpendicular_distance": 0.05}

CONCRETE_SET_LONG = {"text_dim_distance_horizontal": 0.25,
                     "text_dim_distance_vertical": 0.25}

BEAM_SET_TRANSVERSE = {"text_dim_distance": 0.05,
                       "text_dim_height": 0.05}

BEAM_SET_LONG_REBAR = {"text_height": 0.05}

COLUMN_SET_TRANSVERSE = {"text_dim_distance": 0.05,
                         "text_dim_height": 0.05}

COLUMN_SET_LONG_REBAR = {"text_height": 0.05}

CADTABLE_SET_DEFAULT = {"content_row_height": 0.3,
                        "content_column_width": 0.6,
                        "content_text_height": 0.10,
                        "content_fit": True,
                        "labels_row_height": 0.3,
                        "labels_column_width": 1,
                        "labels_text_height": 0.2,
                        "labels_fit": True}

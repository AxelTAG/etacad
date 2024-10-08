# -*- coding: utf-8 -*-

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
    CONCRETE = 4
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
# Bar.
BAR_SET_LONG = {"text_dim_distance_horizontal": 0.05,
                "text_dim_distance_vertical": 0.05,
                "text_dim_height": 0.05,
                "text_denomination_distance": 0.1,
                "text_denomination_height": 0.05}

BAR_SET_TRANSVERSE = {"text_dim_distance_horizontal": 0.05,
                      "text_dim_distance_vertical": 0.05,
                      "text_dim_height": 0.05,
                      "text_denomination_distance": 0.1,
                      "text_denomination_height": 0.05}

# Beam.
BEAM_SET_LONG = {"concrete_settings": {"text_dim_distance_horizontal": 0.6,
                                       "text_dim_distance_vertical": 0.10,
                                       "dim_style_boxing": "EZ_M_25_H25_CM",
                                       "dim_style_inner": "EZ_M_10_H25_CM"},
                 "text_dim_horizontal_distance": 0.05,
                 "text_dim_height": 0.05}

BEAM_SET_TRANSVERSE = {"concrete_settings": {"text_dim_distance_horizontal": 0.10,
                                             "text_dim_distance_vertical": 0.10,
                                             "text_dim_inner_perpendicular_distance": 0.05,
                                             "dim_style_boxing": "EZ_M_10_H25_CM",
                                             "dim_style_inner": "EZ_M_10_H25_CM"},
                       "text_dim_distance": 0.05,
                       "text_dim_height": 0.05}

BEAM_SET_LONG_REBAR = {"text_height": 0.05}

# CADTable.
CADTABLE_SET_DEFAULT = {"content_row_height": 0.3,
                        "content_column_width": 0.6,
                        "content_text_height": 0.10,
                        "content_fit": True,
                        "labels_row_height": 0.3,
                        "labels_column_width": 1,
                        "labels_text_height": 0.2,
                        "labels_fit": True}

# Column.
COLUMN_SET_LONG = {"concrete_settings": {"text_dim_distance_horizontal": 0.15,
                                         "text_dim_distance_vertical": 0.25,
                                         "dim_style_boxing": "EZ_M_25_H25_CM",
                                         "dim_style_inner": "EZ_M_10_H25_CM"},
                   "text_dim_horizontal_distance": 0.05,
                   "text_dim_height": 0.05}

COLUMN_SET_TRANSVERSE = {"concrete_settings": {"text_dim_distance_horizontal": 0.05,
                                               "text_dim_distance_vertical": 0.05,
                                               "dim_style_boxing": "EZ_M_10_H25_CM",
                                               "dim_style_inner": "EZ_M_10_H25_CM"},
                         "text_dim_height": 0.05}

COLUMN_SET_LONG_REBAR = {"bar_settings": {"text_dim_distance_horizontal": 0.05,
                                          "text_dim_distance_vertical": 0.05,
                                          "text_dim_height": 0.05,
                                          "text_denomination_distance": 0.05,
                                          "text_denomination_height": 0.05},
                         "text_height": 0.05,
                         "spacing": 0.3}

COLUMN_SET_TRANSVERSE_REBAR = {"bar_settings": {"text_dim_distance_horizontal": 0.05,
                                                "text_dim_distance_vertical": 0.05,
                                                "text_dim_height": 0.05,
                                                "text_denomination_distance": 0.05,
                                                "text_denomination_height": 0.05},
                               "text_height": 0.05,
                               "spacing": 0.3}

# Concrete.
CONCRETE_SET_LONG = {"text_dim_distance_horizontal": 0.25,
                     "text_dim_distance_vertical": 0.25,
                     "dim_style_boxing": "EZ_M_10_H25_CM",
                     "dim_style_inner": "EZ_M_10_H25_CM"}

CONCRETE_SET_TRANSVERSE = {"text_dim_distance_horizontal": 0.25,
                           "text_dim_distance_vertical": 0.25,
                           "text_dim_inner_perpendicular_distance": 0.05,
                           "dim_style_boxing": "EZ_M_10_H25_CM",
                           "dim_style_inner": "EZ_M_10_H25_CM"}

# Stirrups.
STIRRUP_SET_TRANSVERSE = {"text_dim_distance_horizontal": 0.05,
                          "text_dim_distance_vertical": 0.10,
                          "text_dim_distance_anchor": 0.10,
                          "text_distance_length_count": 0.1,
                          "text_length_count_height": 0.05,
                          "dim_style": "EZ_M_10_H25_CM"}

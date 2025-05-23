# -*- coding: utf-8 -*-

# Local imports.
from etacad.bar import Bar
from etacad.cadtable import CADTable
from etacad.concrete import Concrete
from etacad.drawing_utils import delimit_axe, dim_linear, rect, text
from etacad.globals import (SlabTypes, Direction, ElementTypes, Orientation, CONCRETE_WEIGHT,
                            SLAB_SET_TOP_VIEW, SLAB_SET_TRANSVERSE, SLAB_SET_LONG_REBBAR, SLAB_SET_TRANSVERSE_REBBAR)
from etacad.stirrup import Stirrup
from etacad.utils import gen_symmetric_list, gen_position_bars

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from ezdxf.gfxattribs import GfxAttribs
from itertools import chain


@define
class Slab:
    """
    Slab element, computes geometrics and physics props and manages dxf drawing methods (longitudinal, transversal,
    reinforcement detailing, etc.)
    """
    # Geometric attributes.
    width: float = field(converter=float)
    length: float = field(converter=float)
    thickness: float = field(converter=float)
    slab_type: int = field(default=SlabTypes.RECTANGULAR)
    x: float = field(default=0, converter=float)
    y: float = field(default=0, converter=float)
    direction: Direction = field(default=Direction.HORIZONTAL)
    orientation: Orientation = field(default=Orientation.RIGHT)

    # Longitudinal steel attributes.
    as_sup: dict = field(default=None)
    as_inf: dict = field(default=None)

    max_db_sup: float = field(init=False)
    max_db_inf: float = field(init=False)
    max_db_hz: float = field(init=False)

    anchor_sup: list = field(default=0)
    anchor_inf: list = field(default=0)

    bars_as_sup: list = field(init=False)
    bars_as_inf: list = field(init=False)

    number_init_sup: int = field(init=False)
    number_init_inf: int = field(init=False)

    cover: float = field(default=0, converter=float)

    # Concrete attributes.
    concrete: Concrete = field(init=False)
    concrete_specific_weight: float = CONCRETE_WEIGHT

    # Crossing beams attributes.
    beams: list = field(default=None)  # Maybe not in use.
    beams_pos: list = field(default=None)  # Maybe not in use.
    beams_symbol: list = field(default=None)  # Maybe not in use.

    # Entities groups.
    all_bars: list = field(init=False)
    all_elements: list = field(init=False)

    # Box attributes.
    box_width: float = field(init=False)
    box_height: float = field(init=False)

    # Position bar attributes.
    nomenclature: str = field(default="#")
    positions: dict = field(init=False)

    # Slab attributes.
    denomination: str = field(default=None)
    number_init: int = field(default=None)
    element_type: ElementTypes = field(default=ElementTypes.SLAB)

    def __attrs_post_init__(self):
        # Longitudinal steel attributes.
        if self.number_init is None:
            self.number_init = 0

        # Top bars.
        if self.as_sup:
            self.max_db_sup = max(self.as_sup.keys())
            self.number_init_sup = self.number_init if self.number_init else 0
            self.number_init = self.number_init + len(self.as_sup) if self.number_init else len(self.as_sup)

            self.anchor_sup = self.anchor_sup if type(self.anchor_sup) == list else [self.anchor_sup] * sum(
                self.as_sup.values())
        else:
            self.as_sup, self.max_db_sup, self.number_init_sup = {}, 0, 0

        # Inferior bars.
        if self.as_inf:
            self.max_db_inf = max(self.as_inf.keys())
            self.number_init_inf = self.number_init if self.number_init is not None else 0
            self.number_init = self.number_init + len(self.as_inf) if self.number_init else len(self.as_inf)

            self.anchor_inf = self.anchor_inf if type(self.anchor_inf) == list else [self.anchor_inf] * sum(
                self.as_inf.values())
        else:
            self.as_inf, self.max_db_inf, self.number_init_inf = {}, 0, 0

        self.max_db_hz = max(self.max_db_sup, self.max_db_inf)

        self.bars_as_sup = self.__dict_to_bars(bars=self.as_sup,
                                               width=self.width,
                                               x=self.x,
                                               y=self.y,
                                               side=Orientation.TOP,
                                               anchor=self.anchor_sup,
                                               nomenclature=self.nomenclature,
                                               number_init=self.number_init_sup) if self.as_sup else []
        self.bars_as_inf = self.__dict_to_bars(bars=self.as_inf,
                                               width=self.width,
                                               x=self.x,
                                               y=self.y,
                                               side=Orientation.BOTTOM,
                                               anchor=self.anchor_inf,
                                               nomenclature=self.nomenclature,
                                               number_init=self.number_init_inf) if self.as_sup else []

        # Concrete attributes.
        vertices = [(0, 0),
                    (0, self.length),
                    (self.width, self.length),
                    (self.width, 0)]

        self.concrete = Concrete(vertices=vertices,
                                 height=self.thickness,
                                 x=self.x,
                                 y=self.y,
                                 specific_weight=self.concrete_specific_weight)

        # Position bar attributes.
        min_number_init = min(self.number_init_sup, self.number_init_inf)

        self.positions = gen_position_bars(dictionaries=[self.as_sup, self.as_inf],
                                           nomenclature=self.nomenclature,
                                           number_init=min_number_init)

        # Entities groups.
        self.all_bars = self.bars_as_sup + self.bars_as_inf
        self.all_elements = self.all_bars

        # Box attributes.
        self.box_width = self.width
        self.box_height = self.length

    def draw_top_view(self, document: Drawing,
                      x: float = None,
                      y: float = None,
                      concrete_shape: bool = True,
                      bars: bool = True,
                      dim: bool = True,
                      dim_style: str = "EZ_M_25_H25_CM",
                      unifilar_bars: bool = False) -> dict:
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        elements = {"concrete": [],
                    "beam_elements": [],
                    "beam_axe_elements": [],
                    "column_axe_elements": [],
                    "dimensions_elements": [],
                    "bars": []}

        delimit_axe_width = self.width * 4
        delimit_axe_x = x - self.width * 2

        # Drawing concrete shape.
        if concrete_shape:
            elements["concrete"] = self.concrete.draw_longitudinal(document=document,
                                                                   x=x,
                                                                   y=y,
                                                                   dimensions=dim,
                                                                   dimensions_inner=False,
                                                                   settings=SLAB_SET_TOP_VIEW["concrete_settings"])

        # Drawing of bars.
        if self.as_sup or self.as_right or self.as_inf or self.as_left:
            if bars:
                for bar in self.bars_as_inf:
                    delta_unfilar = 0 if not unifilar_bars else - bar.radius
                    elements["bars"].append(bar.draw_top_view(document=document,
                                                              x=x + (bar.x - self.x) + delta_unfilar,
                                                              y=y + (bar.y - self.y),
                                                              unifilar=unifilar_bars,
                                                              dimensions=False,
                                                              denomination=False))  # Only left bars.

        # Setting groups of elements in dictionary.
        elements["all_elements"] = (elements["concrete"]["all_elements"] +
                                    elements["beam_elements"] +
                                    elements["beam_axe_elements"] +
                                    elements["column_axe_elements"] +
                                    elements["dimensions_elements"] +
                                    list(chain(*[bar_dict["all_elements"] for bar_dict in elements["bars"]])) +
                                    list(chain(*[st_dict["all_elements"] for st_dict in elements["stirrups"]])))

        return elements


# -*- coding: utf-8 -*-

# Imports.
# Local imports.
from etacad.bar import Bar
from etacad.drawing_utils import *
from etacad.globals import (Direction, ElementTypes, Orientation, STEEL_WEIGHT, SPACEDBARS_SET_LONG,
                            SAPCEDBARS_SET_TRANSVERSE)

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from itertools import chain
from math import cos, sin, pi


@define
class SpacedBars:
    # Spaced bars attributes.
    reinforcement_length: float
    length: float
    diameter: float
    spacing: float
    radius: float = field(init=False)
    x: float = field(default=0)
    y: float = field(default=0)
    direction: Direction = field(default=Direction.HORIZONTAL)
    orientation: Orientation = field(default=Orientation.BOTTOM)
    transverse_center: tuple = field(default=None)
    quantity: int = field(init=False)

    # Bar elements attribute.
    bars: list[Bar] = field(init=False)

    # Bar anchor attributes.
    left_anchor: float = field(default=0)
    right_anchor: float = field(default=0)
    mandrel_radius: float = field(default=0)

    # Bar bending attributes.
    bend_longitud: float = field(default=0)
    bend_angle: float = field(default=0)
    bend_height: float = field(default=0)

    # Boxing attributes.
    _box_width: float = field(init=False)
    _box_height: float = field(init=False)

    # Amounts attributes.
    weight: float = field(init=False)

    # Others.
    element_type: ElementTypes = field(default=ElementTypes.SPACED_BARS)
    denomination: str = field(default=None)
    position: str = field(default=None)

    def __attrs_post_init__(self):
        # Others.
        self.quantity = int(self.reinforcement_length / self.spacing) + 1
        if (self.reinforcement_length * 100) % (self.spacing * 100) == 0:
            self.quantity += 1

        # Geometric attributes.
        self.radius = self.diameter / 2

        # Bar element attribute.
        self.bars = []
        for i in range(self.quantity):
            self.bars.append(Bar(reinforcement_length=self.length,
                                 diameter=self.diameter,
                                 x=0,
                                 y=i * self.spacing,
                                 direction=Direction.HORIZONTAL,
                                 orientation=self.orientation,
                                 left_anchor=self.left_anchor,
                                 right_anchor=self.right_anchor,
                                 mandrel_radius=self.mandrel_radius,
                                 bend_longitud=self.bend_longitud,
                                 bend_angle=self.bend_angle,
                                 bend_height=self.bend_height,
                                 element_type=ElementTypes.BAR,
                                 denomination=self.denomination))

        # Boxing attributes.
        self._box_width = self.bars[0].box_width
        self._box_height = (self.quantity - 1) * self.spacing + self.bars[0].box_height

        # Physics attributes.
        self.weight = (self.diameter ** 2 * pi / 4) * self.length * STEEL_WEIGHT * self.quantity

    @property
    def box_width(self) -> float:
        if self.direction == Direction.HORIZONTAL:
            return self._box_width
        return self._box_height

    @property
    def box_height(self) -> float:
        if self.direction == Direction.VERTICAL:
            return self._box_height
        return self._box_width

    def draw_longitudinal(self,
                          document: Drawing,
                          x: float = None,
                          y: float = None,
                          unifilar: bool = False,
                          dimensions: bool = True,
                          reinforcement_dimensions: bool = True,
                          bar_dimension: bool = True,
                          bar_dimension_position: int = None,
                          denomination: bool = True,
                          denomination_position: int = None,
                          one_bar: bool = False,
                          one_bar_position: int = None,
                          settings: dict = SPACEDBARS_SET_LONG) -> dict:
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        if one_bar_position is None:
            one_bar_position = self.quantity // 3
        if bar_dimension_position is None:
            bar_dimension_position = one_bar_position
        if denomination_position is None:
            denomination_position = one_bar_position

        elements = {}
        bar_dict = []
        dimension_elements = []
        denomination_elements = []

        for i, bar in enumerate(self.bars):
            if not one_bar or i == one_bar_position:
                bar_dict.append(bar.draw_longitudinal(document=document,
                                                      x=x + bar.x,
                                                      y=y + bar.y,
                                                      unifilar=unifilar,
                                                      dimensions=bar_dimension and i == bar_dimension_position,
                                                      denomination=denomination and i == denomination_position,
                                                      settings=settings))

        if dimensions and reinforcement_dimensions:
            dim_x = x + self.bars[0].x
            dim_y = y + self.bars[0].y
            dim_y_top = y + self.bars[-1].y

            # Top dimension.
            dimension_elements += dim_linear(document=document,
                                             p_base=(dim_x + self.length / 2,
                                                     dim_y_top + settings["text_dim_distance_vertical"]),
                                             p1=(dim_x, dim_y_top),
                                             p2=(dim_x + self.length, dim_y_top),
                                             dimstyle=settings["dim_style"])

            # Left dimension.
            dimension_elements += dim_linear(document=document,
                                             p_base=(dim_x - settings["text_dim_distance_horizontal"],
                                                     dim_y + self.reinforcement_length / 2),
                                             p1=(dim_x, dim_y),
                                             p2=(dim_x, dim_y_top),
                                             rotation=90,
                                             dimstyle=settings["dim_style"])

        # Setting groups of elements in dictionary.
        elements["bar_elements"] = bar_dict
        elements["dimension_elements"] = dimension_elements
        elements["denomination_elements"] = denomination_elements
        elements["all_elements"] = (list(chain(*[bar["all_elements"] for bar in bar_dict])) +
                                    elements["dimension_elements"] +
                                    elements["denomination_elements"])

        self.__direc_orient(group=elements["all_elements"], x=x, y=y, unifilar=unifilar)

        return elements

    def draw_transverse(self,
                        document: Drawing,
                        x: float = None,
                        y: float = None,
                        dimensions: bool = False,
                        settings: dict = SAPCEDBARS_SET_TRANSVERSE) -> dict:
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        if self.transverse_center:
            x += self.transverse_center[0]
            y += self.transverse_center[1]

        elements = {}
        bar_dict = []
        dimensions_elements = []

        # Drawing of circles.
        for i, bar in enumerate(self.bars):
            bar_dict.append(bar.draw_transverse(document=document,
                                                x=x,
                                                y=y + self.spacing * i,
                                                settings=settings))

        # Drawing dimensions.
        if dimensions:
            dimensions_elements += (dim_linear(document=document,
                                               p_base=(x - settings["text_dim_distance_vertical"],
                                                       y + self._box_height / 2),
                                               p1=(x, y),
                                               p2=(x, y + self._box_height),
                                               rotation=90))

        # Setting groups of elements in dictionary.
        elements["bar_elements"] = bar_dict
        elements["dimension_elements"] = dimensions_elements
        elements["all_elements"] = (list(chain(*[bar["all_elements"] for bar in elements["bar_elements"]])) +
                                    elements["dimension_elements"])

        # Orienting elements.
        self.__direc_orient(group=elements["all_elements"])

        return elements

    def __direc_orient(self,
                       group: list,
                       x: float = None,
                       y: float = None,
                       unifilar: bool = False):
        """
        Adjusts the orientation of the drawing based on the direction and orientation of the bar.

        :param group: List of drawing entities to be oriented.
        :type group: list
        :param x: X coordinate for the orientation, defaults to self.x.
        :type x: float, optional
        :param y: Y coordinate for the orientation, defaults to self.y.
        :type y: float, optional
        :param unifilar: Whether to apply unifilar adjustments, defaults to False.
        :type unifilar: bool, optional
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        # Filtering entities.
        group_filter = filter_entities(entities=group)

        # Orienting the bar (direction and orientation).
        # Direction.
        if self.direction == Direction.VERTICAL:
            pivot_point = (x, y + self._box_height)
            vector_translate = (x - (pivot_point[0] * cos(pi / 2) - pivot_point[1] * sin(pi / 2)),
                                y - (pivot_point[0] * sin(pi / 2) + pivot_point[1] * cos(pi / 2)))

            rotate(group, pi / 2)
            translate(group, vector=vector_translate)

            if unifilar:
                translate(group, vector=(-self.diameter, 0))

            translate(group, vector=(self.diameter, 0))

        # Orienting the texts elements (direction and orientation).
        if "DIMENSION" in group_filter:
            for dimension in group_filter["DIMENSION"]:
                dimension.dxf.text_rotation = dimension.dxf.angle if dimension.dxf.angle != 180 else 0
                dimension.render()

    def data(self) -> dict:
        """
        Collects and returns the essential attributes of the spaced bars element in a dictionary format.

        :return: Dictionary containing key attributes of the spaced bars such as denomination, length, diameter,
         quantity, spacing and weight.
        :rtype: dict
        """
        data = {"denomination": self.denomination,
                "length": self.length,
                "diameter": self.diameter,
                "weight": self.weight,
                "quantity": self.quantity,
                "spacing": self.spacing}

        return data

    def extract_data(self, labels: list[str] = None):
        """
        Extracts specific data attributes based on the provided list of labels.
        If no labels are provided, it defaults to extracting "denomination", "length", "diameter", "quantity", "spacing"
        and "weight".

        :param labels: List of attribute names to extract. Defaults to common attributes if not provided.
        :type labels: list[str], optional
        :return: A list of values corresponding to the requested labels.
        :rtype: list
        """
        if labels is None:
            labels = ["denomination", "length", "diameter", "weight", "quantity", "spacing"]

        data = self.data()

        data_required = []
        for key in labels:
            if key in data:
                data_required.append(data[key])
            else:
                data_required.append("-")

        return data_required

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
    mandrel_radius_ext: float = field(init=False)

    # Bar bending attributes.
    bend_longitud: float = field(default=0)
    bend_angle: float = field(default=0)
    bend_height: float = field(default=0)

    # Boxing attributes.
    _box_width: float = field(init=False)
    _box_height: float = field(init=False)
    max_height_attribute: float = field(init=False)

    # Amounts attributes.
    weight: float = field(init=False)

    # Others.
    element_type: ElementTypes = field(default=ElementTypes.SPACED_BARS)
    denomination: str = field(default=None)
    position: str = field(default=None)

    def __attrs_post_init__(self):
        # Others.
        self.quantity = int(self.reinforcement_length / self.spacing) + 1

        # Geometric attributes.
        self.radius = self.diameter / 2

        # Bar anchor attributes.
        if not self.right_anchor or not self.left_anchor:
            self.mandrel_radius = 0

        self.mandrel_radius_ext = 0
        if self.mandrel_radius:
            self.mandrel_radius_ext += self.mandrel_radius

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
        self.max_height_attribute = max(self.right_anchor, self.left_anchor, self.bend_height)

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

    @property
    def is_exact_reinforcement(self) -> bool:
        return float(self.reinforcement_length / self.spacing).is_integer()

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
                                                      dimensions=False,
                                                      denomination=denomination and i == denomination_position,
                                                      settings=settings))
                if dimensions and bar_dimension and i == bar_dimension_position:
                    y_differencial = 0
                    if bar.orientation == Orientation.TOP:
                        y_differencial = max(bar.right_anchor, bar.left_anchor, bar.bend_height)
                    dimension_elements += text(document=document,
                                               text="Ø{0} s/{1} ".format(
                                                   bar.diameter, self.spacing),
                                               height=settings["text_dim_height"],
                                               point=(x + bar.box_width / 2,
                                                      y + bar.y + bar.diameter + settings[
                                                          "text_dim_distance_horizontal"] - y_differencial),
                                               rotation=0,
                                               attr={"halign": 4, "valign": 0})

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
                        descriptions: bool = True,
                        description_start: int = None,
                        bar_displacements: dict = None,
                        rotate_angle: float = None,
                        settings: dict = SAPCEDBARS_SET_TRANSVERSE) -> dict:
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        if description_start is None:
            description_start = 0
            if self.quantity >= 6:
                description_start = self.quantity / 3

        if description_start > self.quantity - 3:
            description_start = self.quantity - 3

        if bar_displacements is None:
            bar_displacements = {}

        if rotate_angle is None:
            rotate_angle = 0

        if self.transverse_center:
            x += self.transverse_center[0]
            y += self.transverse_center[1]

        elements = {}
        bar_dict = []
        descriptions_elements = []
        dimensions_elements = []

        # Drawing of circles.
        for i, bar in enumerate(self.bars):
            x_displacement, y_displacement = (0, 0)
            if i in bar_displacements:
                x_displacement, y_displacement = bar_displacements[i]
            bar_dict.append(bar.draw_transverse(document=document,
                                                x=x + x_displacement,
                                                y=y + self.spacing * i + y_displacement,
                                                settings=settings))

        # Drawing dimensions.
        if dimensions:
            dimensions_elements += dim_linear(document=document,
                                              p_base=(x - settings["text_dim_distance_vertical"],
                                                      y + self._box_height / 2),
                                              p1=(x, y),
                                              p2=(x, y + self._box_height),
                                              rotation=90)

        if descriptions:
            description_text = f"Ø{self.diameter}/ {self.spacing}m."

            p2 = None
            for i, bar in enumerate(self.bars):
                if description_start <= i < description_start + 3:
                    p1 = (x + bar.x + bar.radius, y + bar.y + bar.radius)
                    if p2 is None:
                        p2 = (x + bar.x + settings["text_description_distance_horizontal"],
                              y + bar.y + settings["text_description_distance_vertical"])
                    descriptions_elements += line(doc=document,
                                                  p1=p1,
                                                  p2=p2)

            descriptions_elements += text(document=document,
                                          text=description_text,
                                          height=settings["text_description_height"],
                                          point=p2,
                                          rotation=90)

        # Setting groups of elements in dictionary.
        elements["bar_elements"] = bar_dict
        elements["description_elements"] = descriptions_elements
        elements["dimension_elements"] = dimensions_elements
        elements["all_elements"] = (list(chain(*[bar["all_elements"] for bar in elements["bar_elements"]])) +
                                    elements["description_elements"] +
                                    elements["dimension_elements"])

        # Orienting elements.
        self.__direc_orient(group=elements["all_elements"], x=x, y=y, rotate_angle=rads(rotate_angle))

        return elements

    def __direc_orient(self,
                       group: list,
                       x: float = None,
                       y: float = None,
                       rotate_angle: float = 0,
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

            # Orienting the texts elements (direction and orientation).
            if "DIMENSION" in group_filter:
                for dimension in group_filter["DIMENSION"]:
                    dimension.dxf.text_rotation = dimension.dxf.angle if dimension.dxf.angle != 180 else 0
                    dimension.render()

            if "TEXT" in group_filter:
                for text_element in group_filter["TEXT"]:
                    text_element.dxf.rotation = text_element.dxf.rotation if text_element.dxf.rotation != 180 else 0

        # Orienting the bar (rotation angle).
        if rotate_angle:
            pivot_point = (x, y)
            vector_translate = (x - (pivot_point[0] * cos(rotate_angle) - pivot_point[1] * sin(rotate_angle)),
                                y - (pivot_point[0] * sin(rotate_angle) + pivot_point[1] * cos(rotate_angle)))

            rotate(group, rotate_angle)
            translate(group, vector=vector_translate)

            # Orienting the texts elements (direction and orientation).
            if "DIMENSION" in group_filter:
                for dimension in group_filter["DIMENSION"]:
                    dimension.dxf.text_rotation = dimension.dxf.angle if dimension.dxf.angle != 180 else 0
                    dimension.render()

            if "TEXT" in group_filter:
                for text_element in group_filter["TEXT"]:
                    text_element.dxf.rotation = text_element.dxf.rotation if text_element.dxf.rotation != 180 else 0

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

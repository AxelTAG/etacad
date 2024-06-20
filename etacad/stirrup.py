# Imports.
# Local imports.

from drawing_utils import (curve, dim_linear, get_lines_intersec, line, mirror, rads, rect_border_curve, rotate,
                           text, translate)
from element import Element
from globals import STEEL_WEIGHT

# External imports.
import ezdxf
from ezdxf.document import Drawing
from math import cos, sin, pi, floor

# Constants.
SIN45, COS45 = sin(rads(45)), cos(rads(45))


class Stirrup(Element):
    """
    Stirrup element, computes geometrics and physics props and manages dxf drawing methods.

        :param width: External width of stirrup.
        :type width: float
        :param height: External height of stirrup.
        :type height: float
        :param diameter: Diameter of stirrup bar.
        :type diameter: float
        :param reinforcement_length: Length of the stirrup reinforcement.
        :type reinforcement_length: float
        :param spacing: Stirrup spacing.
        :type spacing: float
        :param x: X coordinate of the bottom left corner Stirrup bounding box point.
        :type x: float
        :param y: Y coordinate of the bottom left corner Stirrup bounding box point.
        :type y: float
        :param mandrel_radius_top: Mandrel radius of stirrup bar at the top.
        :type mandrel_radius_top: float
        :param mandrel_radius_bottom: Mandrel radius of stirrup bar at the bottom.
        :type mandrel_radius_bottom: float
        :param anchor: Anchor length of stirrup.
        :type anchor: float
        :param direction: Direction of the stirrup (Horizontal or Vertical).
        :type direction: str
        :param orientation: Orientation of the stirrup (top, right, down, left).
        :type orientation: str

        :ivar reinforcement_length: Length of the stirrup reinforcement.
        :ivar spacing: Stirrup spacing.
        :ivar mandrel_radius_top: Mandrel radius of stirrup bar at the top.
        :ivar mandrel_radius_ext_top: Mandrel radius plus diameter of stirrup bar at the top.
        :ivar mandrel_radius_bottom: Mandrel radius of stirrup bar at the bottom.
        :ivar mandrel_radius_ext_bottom: Mandrel radius plus diameter of stirrup bar at the bottom.
        :ivar anchor: Anchor length of stirrup.
        :ivar quantity: Number of stirrups that forms de reinforcement.
        :ivar diameter: Diameter of stirrup bar.
        :ivar direction: Direction of the stirrup (Horizontal or Vertical).
        :ivar orientation: Orientation of the Stirrup (top, right, down, left).
        :ivar length: Length of the bar to fork the stirrup.
        :ivar weight: Weight of the stirrup, considering 7850 kg / m3.
        :ivar box_width: Width of the box that contains the stirrup.
        :ivar box_height: Height of the box that contains the stirrup.
    """
    def __init__(self, width: float, height: float, diameter: float, reinforcement_length: float,
                 spacing: float, x: float = 0, y: float = 0, mandrel_radius_top: float = 0,
                 mandrel_radius_bottom: float = 0, anchor: float = 0.15, direction: str = "horizontal",
                 orientation: str = "down"):
        """
        Initialeze a new instance of Stirrup.
        """
        super().__init__(width=width, height=height, element_type="stirrup", x=x, y=y)

        # Stirrups attributes.
        self.reinforcement_length = reinforcement_length
        self.spacing = spacing
        self.mandrel_radius_top = mandrel_radius_top
        self.mandrel_radius_ext_top = mandrel_radius_top + diameter
        self.mandrel_radius_bottom = mandrel_radius_bottom
        self.mandrel_radius_ext_bottom = mandrel_radius_bottom + diameter
        self.anchor = anchor
        self.quantity = floor((reinforcement_length * 100) / (spacing * 100)) + 1

        # Geometric attributes.
        self.diameter = diameter
        self.direction = direction
        self.orientation = orientation
        self.length = (width + height + anchor) * 2
        self.weight = (diameter ** 2 * pi / 4) * self.length * STEEL_WEIGHT

        # Box attributes.
        self.box_width = self.width
        self.box_height = self.height

    # Drawing longitudinal function.
    def draw_longitudinal(self, document: Drawing, x: float = None, y: float = None, unifilar=True):
        """
        Draw the longitudinal reinforcement of the stirrup in the dxf file.

        :param document: Document in which it will be drawn.
        :type document: Drawing
        :param x: X coordinate of the bottom corner of the drawing.
        :type x: float
        :param y: Y coordinate of the bottom corner of the drawing.
        :type y: float
        :param unifilar: Single-line drawing.
        :type unifilar: bool
        :return: None.
        :rtype: None
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        if unifilar:
            group = [line(doc=document, p1=(x + self.spacing * i, y), p2=(x + self.spacing * i, y + self.height))[0]
                     for i in range(self.quantity)]
        else:
            group = [line(doc=document, p1=(x + self.spacing * i, y), p2=(x + self.spacing * i, y + self.height))[0]
                     for i in range(self.quantity)]

        # Orienting the bar (direction and orientation).
        self.__direc_orient(group, x=x, y=y, longitudinal=True)

        return group

    # Drawing transverse section of stirrup function.
    def draw_transverse(self, document: Drawing, x: float = None, y: float = None, unifilar: bool = False,
                        dimensions: bool = False) -> list:
        """
        Draw the cross-section of the stirrup in the dxf file.

        :param document: Document in which it will be drawn.
        :type document: Drawing
        :param x: X coordinate of the bottom corner of the drawing.
        :type x: float
        :param y: Y coordinate of the bottom corner of the drawing.
        :type y: float
        :param unifilar: Single-line drawing.
        :type unifilar: bool
        :param dimensions: Dimensions drawing.
        :type dimensions: bool
        :return: None.
        :rtype: None
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        # Configurations variables.
        text_dim_distance = 0.05
        text_dim_height = 0.05

        # Curves radius of rect border bordes.
        curves_radius = [self.mandrel_radius_top, self.mandrel_radius_top, self.mandrel_radius_bottom,
                         self.mandrel_radius_bottom]

        # Constants equation of anchor lines.
        diff = 0 if unifilar else self.diameter
        m_45 = -1
        b_top_anchor_int = ((y + self.height - self.mandrel_radius_top - diff + self.mandrel_radius_top * SIN45)
                            - (m_45 * (x + self.mandrel_radius_top + diff + self.mandrel_radius_top * COS45)))
        b_top_anchor_ext = ((y + self.height - self.mandrel_radius_top - diff + (self.mandrel_radius_top + diff) * SIN45)
                            - (m_45 * (x + self.mandrel_radius_top + diff + (self.mandrel_radius_top + diff) * COS45)))
        b_bottom_anchor_int = ((y + self.height - self.mandrel_radius_top - diff - self.mandrel_radius_top * SIN45)
                               - (m_45 * (x + self.mandrel_radius_top + diff - self.mandrel_radius_top * COS45)))
        b_bottom_anchor_ext = ((y + self.height - self.mandrel_radius_top - diff - (self.mandrel_radius_top + diff) * SIN45)
                               - (m_45 * (x + self.mandrel_radius_top + diff - (self.mandrel_radius_top + diff) * COS45)))

        # Constants equation calculations of sides (top/left) lines.
        m_top_side = 0
        b_top_side = y + self.height if unifilar else y + self.height - self.diameter
        m_left_side = 9999999999
        b_left_side = -x * m_left_side if unifilar else -(x + self.diameter) * m_left_side

        # Constants equation of 45° circle line.
        m_45_circle_line = 1
        if not unifilar:
            b_45_circle_line = ((y + self.box_height - self.mandrel_radius_ext_top)
                                - m_45_circle_line * (x + self.mandrel_radius_ext_top))
        else:
            b_45_circle_line = ((y + self.box_height - self.mandrel_radius_top)
                                - m_45_circle_line * (x + self.mandrel_radius_top))

        # Calculations.
        intersec_top_anchor_int = get_lines_intersec(m_45, b_top_anchor_int, m_45_circle_line, b_45_circle_line)
        intersec_top_anchor_ext = get_lines_intersec(m_45, b_top_anchor_ext, m_top_side, b_top_side)
        intersect_bottom_anchor_int = get_lines_intersec(m_45, b_bottom_anchor_int, m_45_circle_line, b_45_circle_line)
        intersect_bottom_anchor_ext = get_lines_intersec(m_45, b_bottom_anchor_ext, m_45_circle_line, b_45_circle_line)

        if unifilar:
            # Calculations.
            p1_top_anchor_int = (intersec_top_anchor_int,
                                 intersec_top_anchor_int * m_45 + b_top_anchor_int)
            p2_top_anchor_int = (p1_top_anchor_int[0] + COS45 * self.anchor,
                                 p1_top_anchor_int[1] - SIN45 * self.anchor)

            p1_bottom_anchor_int = (intersect_bottom_anchor_int,
                                    intersect_bottom_anchor_int * m_45 + b_bottom_anchor_int)
            p2_bottom_anchor_int = (p1_bottom_anchor_int[0] + COS45 * self.anchor,
                                    p1_bottom_anchor_int[1] - SIN45 * self.anchor)

            p1_bottom_anchor_ext = p1_bottom_anchor_int
            p2_bottom_anchor_ext = p2_bottom_anchor_int

            # Anchor drawing.
            group = line(doc=document, p1=p1_top_anchor_int, p2=p2_top_anchor_int)  # Internal line top anchor.
            group += line(doc=document, p1=p1_bottom_anchor_int, p2=p2_bottom_anchor_int)  # Internal line bot anchor.

            # Rectangle drawing (circle borders).
            group += rect_border_curve(doc=document, width=self.width, height=self.height,
                                       radius=self.mandrel_radius_top, x=x, y=y, thickness=0, sides=[1, 1, 1, 1],
                                       curves_radius=curves_radius)

        else:
            # Drawing of side borders.
            group = rect_border_curve(doc=document, width=self.width - 2 * self.diameter,
                                      height=self.height - 2 * self.diameter, radius=self.mandrel_radius_top,
                                      x=x + self.diameter, y=y + self.diameter, thickness=self.diameter,
                                      sides=[1, 1, 1, 0], curves=[0, 1, 1, 1], curves_radius=curves_radius)

            # External left side border.
            group += line(doc=document, p1=(x, y + self.mandrel_radius_ext_bottom),
                          p2=(x, y + self.box_height - self.mandrel_radius_ext_top))

            # Drawing of anchors.
            # Calculatios of points.
            p1_top_anchor_int = (intersec_top_anchor_int,
                                 intersec_top_anchor_int * m_45 + b_top_anchor_int)
            p2_top_anchor_int = (p1_top_anchor_int[0] + COS45 * self.anchor,
                                 p1_top_anchor_int[1] - SIN45 * self.anchor)
            p1_top_anchor_ext = (intersec_top_anchor_ext,
                                 intersec_top_anchor_ext * m_45 + b_top_anchor_ext)
            p2_top_anchor_ext = (p2_top_anchor_int[0] + self.diameter * COS45,
                                 p2_top_anchor_int[1] + self.diameter * SIN45)
            p1_bottom_anchor_int = (intersect_bottom_anchor_int,
                                    m_45 * intersect_bottom_anchor_int + b_bottom_anchor_int)
            p2_bottom_anchor_int = (p1_bottom_anchor_int[0] + COS45 * self.anchor,
                                    p1_bottom_anchor_int[1] - SIN45 * self.anchor)
            p1_bottom_anchor_ext = (intersect_bottom_anchor_ext,
                                    m_45 * intersect_bottom_anchor_ext + b_bottom_anchor_ext)
            p2_bottom_anchor_ext = (p1_bottom_anchor_ext[0] + COS45 * self.anchor,
                                    p1_bottom_anchor_ext[1] - SIN45 * self.anchor)

            # Center of top left curve.
            center_point_curve = (x + self.mandrel_radius_ext_top, y + self.box_height - self.mandrel_radius_ext_top)

            # Drawing of lines anchors.
            group += line(doc=document, p1=p1_top_anchor_ext, p2=p2_top_anchor_ext)
            group += line(doc=document, p1=p1_top_anchor_int, p2=p2_top_anchor_int)
            group += line(doc=document, p1=p1_bottom_anchor_int, p2=p2_bottom_anchor_int)
            group += line(doc=document, p1=p1_bottom_anchor_ext, p2=p2_bottom_anchor_ext)

            group += line(doc=document, p1=p2_bottom_anchor_int, p2=p2_bottom_anchor_ext)  # Closed lines bottom.
            group += line(doc=document, p1=p2_top_anchor_int, p2=p2_top_anchor_ext)  # Closed lines top.

            # Left internal side.
            group += line(doc=document, p1=(x + self.diameter, y + self.mandrel_radius_ext_bottom),
                          p2=(p1_top_anchor_ext[0] - (self.diameter * 2 + self.mandrel_radius_top * 2) * COS45,
                              p1_top_anchor_ext[1] - (self.diameter * 2 + self.mandrel_radius_top * 2) * SIN45))

            # Top left curve.
            group += curve(doc=document, center_point=center_point_curve, start_angle=90, end_angle=225,
                           radius=self.mandrel_radius_top + self.diameter, thickness=0)  # Internal.
            group += curve(doc=document, center_point=center_point_curve, start_angle=45, end_angle=225,
                           radius=self.mandrel_radius_top, thickness=0)  # External.

        if dimensions:
            group += dim_linear(document=document, p_base=(x - text_dim_distance, y + self.height / 2),
                                p1=(x, y), p2=(x, y + self.height), rotation=90,
                                dimstyle="EZ_M_10_H25_CM")
            group += dim_linear(document=document,
                                p_base=(x + self.width / 2 - text_dim_distance * 2.5,
                                        y + self.height - text_dim_distance * 2.5),
                                p1=p1_bottom_anchor_ext, p2=p2_bottom_anchor_ext, rotation=315,
                                dimstyle="EZ_M_10_H25_CM")
            group += dim_linear(document=document, p_base=(x + self.width / 2, y + self.height + text_dim_distance),
                                p1=(x, y + self.height), p2=(x + self.width, y + self.height),
                                dimstyle="EZ_M_10_H25_CM")
            group += text(document=document, text="L: {0:.2f}".format(self.length), height=text_dim_height,
                          point=(x + self.width / 2, y - 2 * text_dim_distance), attr={"halign": 4, "valign": 0})

        # Orienting the bar (direction and orientation).
        self.__direc_orient(group, x=x, y=y, longitudinal=False)

        return group

    # Function that orients drawing.
    def __direc_orient(self, group: list, x: float = None, y: float = None, longitudinal: bool = False):
        """
        Orient the elements according to the parameters of the stirrup in the group entered.

        :param group: Group of elements dxf to orient.
        :param x: X coordinate of the bottom corner of the drawing.
        :type x: float
        :param y: Y coordinate of the bottom corner of the drawing.
        :type y: float
        :param longitudinal: Type of drawing to which the dxf elements belong (longitudinal or transverse).
        :type longitudinal: bool
        :return: Group of elements dxf to oriented.
        :rtype: list
        """
        # Orienting the bar (direction and orientation).
        # Direction.
        if self.direction == "vertical":
            pivot_point = (x, y + self.box_height)
            vector_translate = (x - (pivot_point[0] * cos(pi / 2) - pivot_point[1] * sin(pi / 2)),
                                y - (pivot_point[0] * sin(pi / 2) + pivot_point[1] * cos(pi / 2)))

            rotate(group, pi / 2)
            translate(group, vector=vector_translate)

        # Orientation.
        if self.orientation == "left":
            mirror(objects=group, mirror_type="y")

            if self.direction == "vertical":
                translate(group, vector=(self.box_height + x * 2, 0))
            else:
                if longitudinal:
                    translate(group, vector=(self.reinforcement_length + x * 2, 0))
                else:
                    translate(group, vector=(self.box_width + x * 2, 0))

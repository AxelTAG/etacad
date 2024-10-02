# Imports.
# Local imports.
from etacad.geometry.utils import get_lines_intersec
from etacad.drawing_utils import curve, dim_linear, line, mirror, rect_border_curve, rotate, text, translate
from etacad.globals import COS45, Direction, ElementTypes, Orientation, SIN45, STEEL_WEIGHT, STIRRUP_SET_TRANSVERSE

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from math import cos, sin, pi, floor


@define
class Stirrup:
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
    # Stirrups attributes.
    width: float
    height: float
    diameter: float
    reinforcement_length: float
    spacing: float
    x: float = field(default=0)
    y: float = field(default=0)
    mandrel_radius_top: float = field(default=0)
    mandrel_radius_ext_top: float = field(init=False)
    mandrel_radius_bottom: float = field(default=0)
    mandrel_radius_ext_bottom: float = field(init=False)
    anchor: float = field(default=0)
    quantity: int = field(init=False)

    # Geometric attributes.
    length: float = field(init=False)
    direction: Direction = field(default=Direction.HORIZONTAL)
    orientation: Orientation = field(default=Orientation.BOTTOM)

    # Physics attributes.
    weight: float = field(init=False)

    # Box attributes.
    box_width: float = field(init=False)
    box_height: float = field(init=False)

    # Others.
    element_type: ElementTypes = field(default=ElementTypes.STIRRUP)
    denomination: str = field(default=None)
    position: str = field(default=None)

    def __attrs_post_init__(self):
        # Stirrups attributes.
        self.mandrel_radius_ext_top = self.mandrel_radius_top + self.diameter
        self.mandrel_radius_ext_bottom = self.mandrel_radius_bottom + self.diameter
        self.quantity = floor((self.reinforcement_length * 100) / (self.spacing * 100)) + 1

        # Geometric attributes.
        self.length = (self.width + self.height + self.anchor) * 2

        # Physics attributes.
        self.weight = (self.diameter ** 2 * pi / 4) * self.length * STEEL_WEIGHT

        # Box attributes.
        self.box_width = self.width
        self.box_height = self.height

    def draw_longitudinal(self,
                          document: Drawing,
                          x: float = None,
                          y: float = None,
                          unifilar=True) -> dict:
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

        elements = {}

        # Drawing stirrup steel bars.
        if unifilar:
            steel = [line(doc=document, p1=(x + self.spacing * i, y), p2=(x + self.spacing * i, y + self.height))[0]
                     for i in range(self.quantity)]
        else:
            steel = [line(doc=document, p1=(x + self.spacing * i, y), p2=(x + self.spacing * i, y + self.height))[0]
                     for i in range(self.quantity)]

        # Setting groups of elements in dictionary.
        elements["steel_elements"] = steel
        elements["all_elements"] = elements["steel_elements"]

        # Orienting the bar (direction and orientation).
        self.__direc_orient(elements["steel_elements"], x=x, y=y, longitudinal=True)

        return elements

    # Drawing transverse section of stirrup function.
    def draw_transverse(self,
                        document: Drawing,
                        x: float = None,
                        y: float = None,
                        unifilar: bool = False,
                        dimensions: bool = False,
                        settings: dict = STIRRUP_SET_TRANSVERSE) -> dict:
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
        :param settings: Dictionary of settings for dimensioning. Defaults to `STIRRUP_SET_TRANSVERSE`.
        :type settings: dict, optional
        :return: None.
        :rtype: None
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        elements = {}
        steel_elements = []
        dim_elements = []

        # Curves radius of rect border bordes.
        curves_radius = [self.mandrel_radius_top, self.mandrel_radius_top, self.mandrel_radius_bottom,
                         self.mandrel_radius_bottom]

        # Constants equation of anchor lines.
        diff = 0 if unifilar else self.diameter
        m_45 = -1
        b_top_anchor_int = ((y + self.height - self.mandrel_radius_top - diff + self.mandrel_radius_top * SIN45)
                            - (m_45 * (x + self.mandrel_radius_top + diff + self.mandrel_radius_top * COS45)))
        b_top_anchor_ext = (
                (y + self.height - self.mandrel_radius_top - diff + (self.mandrel_radius_top + diff) * SIN45)
                - (m_45 * (x + self.mandrel_radius_top + diff + (self.mandrel_radius_top + diff) * COS45)))
        b_bottom_anchor_int = ((y + self.height - self.mandrel_radius_top - diff - self.mandrel_radius_top * SIN45)
                               - (m_45 * (x + self.mandrel_radius_top + diff - self.mandrel_radius_top * COS45)))
        b_bottom_anchor_ext = (
                (y + self.height - self.mandrel_radius_top - diff - (self.mandrel_radius_top + diff) * SIN45)
                - (m_45 * (x + self.mandrel_radius_top + diff - (self.mandrel_radius_top + diff) * COS45)))

        # Constants equation calculations of sides (top/left) lines.
        m_top_side = 0
        b_top_side = y + self.height if unifilar else y + self.height - self.diameter

        # Constants equation of 45° circle line.
        m_45_circle_line = 1
        if not unifilar:
            b_45_circle_line = ((y + self.box_height - self.mandrel_radius_ext_top)
                                - m_45_circle_line * (x + self.mandrel_radius_ext_top))
        else:
            b_45_circle_line = ((y + self.box_height - self.mandrel_radius_top)
                                - m_45_circle_line * (x + self.mandrel_radius_top))

        # Calculations.
        intersec_top_anchor_int = get_lines_intersec(m_45, b_top_anchor_int, m_45_circle_line, b_45_circle_line)[0]
        intersec_top_anchor_ext = get_lines_intersec(m_45, b_top_anchor_ext, m_top_side, b_top_side)[0]
        intersect_bottom_anchor_int = get_lines_intersec(m_45, b_bottom_anchor_int, m_45_circle_line, b_45_circle_line)[
            0]
        intersect_bottom_anchor_ext = get_lines_intersec(m_45, b_bottom_anchor_ext, m_45_circle_line, b_45_circle_line)[
            0]

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
            steel_elements += line(doc=document, p1=p1_top_anchor_int,
                                   p2=p2_top_anchor_int)  # Internal line top anchor.
            steel_elements += line(doc=document, p1=p1_bottom_anchor_int,
                                   p2=p2_bottom_anchor_int)  # Internal line bot anchor.

            # Rectangle drawing (circle borders).
            steel_elements += rect_border_curve(doc=document, width=self.width, height=self.height,
                                                radius=self.mandrel_radius_top, x=x, y=y, thickness=0,
                                                sides=[1, 1, 1, 1],
                                                curves_radius=curves_radius)

        else:
            # Drawing of side borders.
            steel_elements = rect_border_curve(doc=document, width=self.width - 2 * self.diameter,
                                               height=self.height - 2 * self.diameter, radius=self.mandrel_radius_top,
                                               x=x + self.diameter, y=y + self.diameter, thickness=self.diameter,
                                               sides=[1, 1, 1, 0], curves=[0, 1, 1, 1], curves_radius=curves_radius)

            # External left side border.
            steel_elements += line(doc=document, p1=(x, y + self.mandrel_radius_ext_bottom),
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
            steel_elements += line(doc=document, p1=p1_top_anchor_ext, p2=p2_top_anchor_ext)
            steel_elements += line(doc=document, p1=p1_top_anchor_int, p2=p2_top_anchor_int)
            steel_elements += line(doc=document, p1=p1_bottom_anchor_int, p2=p2_bottom_anchor_int)
            steel_elements += line(doc=document, p1=p1_bottom_anchor_ext, p2=p2_bottom_anchor_ext)

            steel_elements += line(doc=document, p1=p2_bottom_anchor_int,
                                   p2=p2_bottom_anchor_ext)  # Closed lines bottom.
            steel_elements += line(doc=document, p1=p2_top_anchor_int, p2=p2_top_anchor_ext)  # Closed lines top.

            # Left internal side.
            steel_elements += line(doc=document, p1=(x + self.diameter, y + self.mandrel_radius_ext_bottom),
                                   p2=(p1_top_anchor_ext[0] - (self.diameter * 2 + self.mandrel_radius_top * 2) * COS45,
                                       p1_top_anchor_ext[1] - (
                                               self.diameter * 2 + self.mandrel_radius_top * 2) * SIN45))

            # Top left curve.
            steel_elements += curve(doc=document, center_point=center_point_curve, start_angle=90, end_angle=225,
                                    radius=self.mandrel_radius_top + self.diameter, thickness=0)  # Internal.
            steel_elements += curve(doc=document, center_point=center_point_curve, start_angle=45, end_angle=225,
                                    radius=self.mandrel_radius_top, thickness=0)  # External.

        if dimensions:
            # Anchor dimension.
            dim_elements += dim_linear(document=document,
                                       p_base=(x + self.width / 2 - settings["text_dim_distance_anchor"],
                                               y + self.height - settings["text_dim_distance_anchor"]),
                                       p1=p1_bottom_anchor_ext,
                                       p2=p2_bottom_anchor_ext, rotation=315,
                                       dimstyle=settings["dim_style"])

            # Vertical dimension.
            dim_elements += dim_linear(document=document,
                                       p_base=(x - settings["text_dim_distance_vertical"], y + self.height / 2),
                                       p1=(x, y),
                                       p2=(x, y + self.height),
                                       rotation=90,
                                       dimstyle=settings["dim_style"])

            # Anchor horizontal.
            dim_elements += dim_linear(document=document,
                                       p_base=(x + self.width / 2,
                                               y + self.height + settings["text_dim_distance_horizontal"]),
                                       p1=(x, y + self.height),
                                       p2=(x + self.width, y + self.height),
                                       dimstyle=settings["dim_style"])

            # Text for length count.
            dim_elements += text(document=document,
                                 text="L: {0:.2f}".format(self.length),
                                 height=settings["text_length_count_height"],
                                 point=(x + self.width / 2, y - settings["text_distance_length_count"]),
                                 attr={"halign": 4, "valign": 0})

        # Setting groups of elements in dictionary.
        elements["steel_elements"] = steel_elements
        elements["dimensions_elements"] = dim_elements
        elements["all_elements"] = (elements["steel_elements"] +
                                    elements["dimensions_elements"])

        # Orienting the bar (direction and orientation).
        self.__direc_orient(elements["steel_elements"], x=x, y=y, longitudinal=False)

        return elements

    # Function that orients drawing.
    def __direc_orient(self,
                       group: list,
                       x: float = None,
                       y: float = None,
                       longitudinal: bool = False):
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
        if self.direction == Direction.VERTICAL:
            pivot_point = (x, y + self.box_height)
            vector_translate = (x - (pivot_point[0] * cos(pi / 2) - pivot_point[1] * sin(pi / 2)),
                                y - (pivot_point[0] * sin(pi / 2) + pivot_point[1] * cos(pi / 2)))

            rotate(group, pi / 2)
            translate(group, vector=vector_translate)

        # Orientation.
        if self.orientation == Orientation.LEFT:
            mirror(objects=group, mirror_type="y")

            if self.direction == Direction.VERTICAL:
                translate(group, vector=(self.box_height + x * 2, 0))
            else:
                if longitudinal:
                    translate(group, vector=(self.reinforcement_length + x * 2, 0))
                else:
                    translate(group, vector=(self.box_width + x * 2, 0))

    def data(self):
        """
        Collects and returns the essential attributes of the stirrup element in a dictionary format.

        :return: Dictionary containing key attributes of the bar such as denomination, length, diameter, weight and
        quantity.
        :rtype: dict
        """
        data = {"denomination": self.denomination,
                "length": self.length,
                "diameter": self.diameter,
                "weight": self.weight,
                "quantity": self.quantity}

        return data

    def extract_data(self, labels: list[str] = None):
        """
        Extracts specific data attributes based on the provided list of labels.
        If no labels are provided, it defaults to extracting "denomination", "length", "diameter", "weight" and
        quantity.

        :param labels: List of attribute names to extract. Defaults to common attributes if not provided.
        :type labels: list[str], optional
        :return: A list of values corresponding to the requested labels.
        :rtype: list
        """
        if labels is None:
            labels = ["denomination", "length", "diameter", "weight", "quantity"]

        data = self.data()

        data_required = []
        for key in labels:
            if key in data:
                data_required.append(data)
            else:
                data_required.append("-")

        return data_required

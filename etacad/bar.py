# Imports.
# Local imports.
from etacad.drawing_utils import circle, curve, line, mirror, rads, rect, rotate, text, translate
from etacad.globals import Direction, ElementTypes, Orientation, STEEL_WEIGHT, BAR_SET_LONG, BAR_SET_TRANSVERSE

# External imports.
from attrs import define, field
from ezdxf.document import Drawing
from math import cos, sin, tan, pi


@define
class Bar:
    """
    Longitudinal bar element, computes geometrics and physics props and manages dxf drawing methods.

    :param reinforcement_length: Length of the stirrup reinforcement.
    :type reinforcement_length: float
    :param diameter: Diameter of stirrup bar.
    :type diameter: float
    :param x: X coordinate of the bottom left corner Stirrup bounding box point.
    :type x: float
    :param y: Y coordinate of the bottom left corner Stirrup bounding box point.
    :type y: float
    :param left_anchor: Left anchor length of stirrup.
    :type left_anchor: float
    :param right_anchor: Right anchor length of stirrup.
    :type right_anchor: float
    :param mandrel_radius: Mandrel radius of bar.
    :type mandrel_radius: float
    :param direction: Direction of the stirrup (Horizontal or Vertical).
    :type direction: Direction
    :param orientation: Orientation of the stirrup (top, right, down, left).
    :type orientation: Orientation
    :param bend_longitud: Bending longitud of the bar at center of bar.
    :type: float
    :param bend_angle: Bending declination angle.
    :type bend_angle: float
    :param bend_height: Bending height of the bar at center of bar.
    :type bend_height: float
    :param transverse_center: Transverse center of the drawing of cross-section.
    :type transverse_center: tuple

    :ivar bend_longitud: Bending longitud of the bar at center of bar.
    :ivar bend_angle: Bending declination angle.
    :ivar bend_height: Bending height of the bar at center of bar.
    :ivar bending_proyection: Proyection of the bend bar.
    :ivar left_anchor: Left anchor length of stirrup.
    :ivar right_anchor: Right anchor length of stirrup.
    :ivar mandrel_radius: Mandrel radius of bar.
    :ivar mandrel_radius_ext: Mandrel radius plus diameter of bar.
    :ivar diameter: Diameter of bar.
    :ivar radius: Radius of bar.
    :ivar direction: Direction of the bar (horizontal or vertical).
    :ivar orientation: Orientation of the bar (top, right, down, left).
    :ivar transverse_center: Transverse center of the drawing of cross-section.
    :ivar reinforcement_length: Length of the reinforcement.
    :ivar length: Length of the bar.
    :ivar weight: Weight of the reinforcement, considering 7850 kg / m3.
    :ivar box_width: Width of the box that contains the bar.
    :ivar box_height: Height of the box that contains the bar.
    """
    # Geometric attributes.
    reinforcement_length: float
    diameter: float
    radius: float = field(init=False)
    length: float = field(init=False)
    x: float = field(default=0)
    y: float = field(default=0)
    direction: Direction = field(default=Direction.HORIZONTAL)
    orientation: Orientation = field(default=Orientation.BOTTOM)
    transverse_center: tuple = field(default=None)

    # Anchor attributes.
    left_anchor: float = field(default=0)
    right_anchor: float = field(default=0)
    mandrel_radius: float = field(default=0)
    mandrel_radius_ext: float = field(init=False)

    # Bending attributes.
    bend_longitud: float = field(default=0)
    bend_angle: float = field(default=0)
    bend_height: float = field(default=0)
    bending_proyection: float = field(init=False)

    # Boxing attributes.
    box_width: float = field(init=False)
    box_height: float = field(init=False)

    # Physics attributes.
    weight: float = field(init=False)

    # Others.
    element_type: ElementTypes = field(default=ElementTypes.BAR)
    denomination: str = field(default=None)

    def __attrs_post_init__(self):
        # Bending attributes.
        self.bending_proyection = self.bend_height / tan(rads(self.bend_angle)) if self.bend_angle else 0

        # Geometric attributes.
        self.radius = self.diameter / 2
        self.length = (self.reinforcement_length + (1 / cos(rads(self.bend_angle)) - 1) * self.bending_proyection * 2
                       + self.left_anchor + self.right_anchor)

        # Mandrel attributes.
        self.mandrel_radius_ext = self.diameter + self.mandrel_radius

        # Boxing attributes.
        self.box_width = self.reinforcement_length
        if self.left_anchor or self.right_anchor or self.bend_height:
            max_anchor = max([self.left_anchor, self.right_anchor])  # Maximum anchor.

            self.box_height = max([self.mandrel_radius_ext + max_anchor, self.diameter * 2 + self.bend_height])
        else:
            self.box_height = self.diameter

        # Physics attributes.
        self.weight = (self.diameter ** 2 * pi / 4) * self.length * STEEL_WEIGHT

    # Drawing longitudinal function.
    def draw_longitudinal(self,
                          document: Drawing,
                          x: float = None,
                          y: float = None,
                          unifilar: bool = False,
                          dimensions: bool = True,
                          denomination: bool = True,
                          settings: dict = BAR_SET_LONG) -> dict:
        """
        Draws the longitudinal view of the bar in a DXF document.

        :param document: The DXF document to draw on.
        :type document: Drawing
        :param x: X coordinate for the drawing, defaults to self.x.
        :type x: float, optional
        :param y: Y coordinate for the drawing, defaults to self.y.
        :type y: float, optional
        :param unifilar: Whether to draw a unifilar representation (simplified view), defaults to False.
        :type unifilar: bool, optional
        :param dimensions: Whether to include dimensions in the drawing, defaults to True.
        :type dimensions: bool, optional
        :param denomination: Whether to include the denomination label, defaults to True.
        :type denomination: bool, optional
        :param settings: Dictionary of settings for dimensioning. Defaults to `BAR_SET_LONG`.
        :type settings: dict, optional
        :return: Dict of drawing entities for the longitudinal view.
        :rtype: dict
        """
        if x is None:
            x = self.x
        if x is None:
            y = self.y

        if not unifilar:
            diameter = self.diameter
            mandrel_radius_ext = self.mandrel_radius_ext
            sides_left_anchor = [0, 1, 1, 1]
            sides_right_anchor = [0, 1, 1, 1]
        else:
            diameter = 0
            mandrel_radius_ext = 0
            sides_left_anchor = [0, 0, 0, 1]
            sides_right_anchor = [0, 1, 0, 0]

        elements = {}
        steel_elements = []
        dimension_elements = []
        denomination_elements = []

        # Drawing of simple entities and setting of variables for progressive draw.
        length_first_rect_bar = self.reinforcement_length
        x_first_rect_bar = x
        sides_first_rect_bar = [1, 1, 1, 1]

        length_third_rect_bar = self.reinforcement_length
        sides_third_rect_bar = [1, 1, 1, 0]

        # Left anchor.
        if self.left_anchor:
            x_lab = x
            y_lab = y + self.box_height - mandrel_radius_ext - self.left_anchor
            center_point_lac = (x + mandrel_radius_ext,
                                y + self.box_height - mandrel_radius_ext)

            length_first_rect_bar -= mandrel_radius_ext
            x_first_rect_bar += mandrel_radius_ext
            sides_first_rect_bar[3] = 0

            # From left to right.
            # First anchor rect bar (left).
            steel_elements += rect(doc=document,
                                   width=diameter,
                                   height=self.left_anchor, x=x_lab, y=y_lab,
                                   sides=sides_left_anchor)

            if not unifilar:
                # First bend curve.
                steel_elements += curve(doc=document,
                                        center_point=center_point_lac,
                                        radius=self.mandrel_radius,
                                        start_angle=90,
                                        end_angle=180,
                                        thickness=diameter)

        # Right anchor.
        if self.right_anchor:
            x_rab = x + self.reinforcement_length - diameter
            y_rab = y + self.box_height - mandrel_radius_ext - self.right_anchor
            center_point_rac = (x + self.reinforcement_length - mandrel_radius_ext,
                                y + self.box_height - mandrel_radius_ext)

            length_first_rect_bar -= mandrel_radius_ext if not self.bend_longitud else 0
            sides_first_rect_bar[1] = 0
            length_third_rect_bar -= mandrel_radius_ext
            sides_third_rect_bar = [1, 0, 1, 0]

            # From left to right.
            # Sixth bend curve.
            if not unifilar:
                steel_elements += curve(doc=document, center_point=center_point_rac,
                                        radius=self.mandrel_radius,
                                        start_angle=0,
                                        end_angle=90, thickness=diameter)

            # Second anchor rect bar (right).
            steel_elements += rect(doc=document,
                                   width=diameter,
                                   height=self.right_anchor, x=x_rab, y=y_rab,
                                   sides=sides_right_anchor)

        # Bending bar.
        if self.bend_longitud:

            alpha = rads(self.bend_angle / 2)
            dx1 = cos(alpha) * sin(alpha) * diameter * 2
            dy1 = sin(alpha) * sin(alpha) * diameter * 2
            dx2 = cos(alpha) * sin(alpha) * diameter * 4
            dy2 = sin(alpha) * sin(alpha) * diameter * 4

            longitud_mid = (self.reinforcement_length + self.bend_longitud) / 2
            longitud_curves = dx1 + dx2
            longitud_proyeccion = (self.bend_height + diameter - dy1 - dy2) / tan(alpha * 2)

            length_first_rect_bar -= (longitud_mid + longitud_curves + longitud_proyeccion)
            sides_first_rect_bar[1] = 0
            length_third_rect_bar -= (longitud_mid + longitud_curves + longitud_proyeccion)

            center_point_bc_first = (x_first_rect_bar + length_first_rect_bar,
                                     y + self.box_height - diameter * 2)
            center_point_bc_second = (x + (self.reinforcement_length - self.bend_longitud) / 2,
                                      y + self.box_height - self.bend_height)

            # From left to right.
            # First piece of rect bar.
            sides_first_rect_bar = sides_first_rect_bar if not unifilar else [1, 0, 0, 0]
            steel_elements += rect(doc=document,
                                   width=length_first_rect_bar,
                                   height=diameter,
                                   x=x_first_rect_bar,
                                   y=y + self.box_height - diameter,
                                   sides=sides_first_rect_bar)

            if not unifilar:
                # First curve of bend.
                steel_elements += curve(doc=document,
                                        center_point=center_point_bc_first,
                                        radius=diameter,
                                        start_angle=90 - self.bend_angle,
                                        end_angle=90,
                                        thickness=diameter)

            # First bend rect bar.
            if not unifilar:
                steel_elements += line(doc=document,
                                       p1=(x + (self.reinforcement_length - self.bend_longitud) / 2 - dx1,
                                           y + self.box_height - self.bend_height - diameter + dy1),
                                       p2=(x + (
                                               self.reinforcement_length - self.bend_longitud) / 2 - dx1 - longitud_proyeccion,
                                           y + self.box_height - dy2))

            steel_elements += line(doc=document,
                                   p1=(x + (self.reinforcement_length - self.bend_longitud) / 2 - dx2,
                                       y + self.box_height - self.bend_height - diameter * 2 + dy2),
                                   p2=(
                                       x + (
                                               self.reinforcement_length - self.bend_longitud) / 2 - dx2 - longitud_proyeccion,
                                       y + self.box_height - diameter - dy1))

            # Second curve of bend.
            if not unifilar:
                steel_elements += curve(doc=document,
                                        center_point=center_point_bc_second,
                                        radius=diameter,
                                        start_angle=270 - self.bend_angle,
                                        end_angle=270,
                                        thickness=diameter)

            # Second rect bar.
            sides_second_rect_bar = [1, 0, 1, 0] if not unifilar else [1, 0, 0, 0]
            steel_elements += rect(doc=document,
                                   width=self.bend_longitud,
                                   height=diameter,
                                   x=x + (self.reinforcement_length - self.bend_longitud) / 2,
                                   y=y + self.box_height - diameter * 2 - self.bend_height,
                                   sides=sides_second_rect_bar)

            # Third bend curve.
            if not unifilar:
                steel_elements += curve(doc=document,
                                        center_point=(x + longitud_mid,
                                                      y + self.box_height - self.bend_height),
                                        radius=diameter,
                                        start_angle=270,
                                        end_angle=270 + self.bend_angle,
                                        thickness=diameter)

            # Second bend bar.
            if not unifilar:
                steel_elements += line(doc=document,
                                       p1=(x + longitud_mid + dx1,
                                           y + self.box_height - self.bend_height - diameter + dy1),
                                       p2=(x + longitud_mid + dx1 + longitud_proyeccion,
                                           y + self.box_height - dy2))

            steel_elements += line(doc=document,
                                   p1=(x + longitud_mid + dx2,
                                       y + self.box_height - self.bend_height - diameter * 2 + dy2),
                                   p2=(x + longitud_mid + dx2 + longitud_proyeccion,
                                       y + self.box_height - diameter - dy1))

            # Fourth bend curve.
            if not unifilar:
                steel_elements += curve(doc=document,
                                        center_point=(x + longitud_mid + longitud_curves + longitud_proyeccion,
                                                      y + self.box_height - diameter * 2),
                                        radius=diameter,
                                        start_angle=90,
                                        end_angle=90 + self.bend_angle,
                                        thickness=diameter)

            # Third rect bar.
            sides_third_rect_bar = sides_third_rect_bar if not unifilar else [1, 0, 0, 0]
            steel_elements += rect(doc=document,
                                   width=length_third_rect_bar,
                                   height=diameter,
                                   x=x + longitud_mid + longitud_curves + longitud_proyeccion,
                                   y=y + self.box_height - diameter,
                                   sides=sides_third_rect_bar)

        else:
            # From left to right.
            # First rect bar (body).
            sides_first_rect_bar = sides_first_rect_bar if not unifilar else [1, 0, 0, 0]
            mandrel_radius_ext = 0 if not self.left_anchor and not self.right_anchor else mandrel_radius_ext
            steel_elements += rect(doc=document,
                                   width=length_first_rect_bar,
                                   height=diameter,
                                   x=x + mandrel_radius_ext,
                                   y=y + self.box_height - diameter,
                                   sides=sides_first_rect_bar)

        if dimensions:
            if self.left_anchor:
                dimension_elements += text(document=document,
                                           text="({:.2f})".format(self.left_anchor),
                                           height=settings["text_dim_height"],
                                           point=(x_lab - settings["text_dim_distance_vertical"],
                                                  y + self.left_anchor / 2),
                                           rotation=90,
                                           attr={"halign": 4, "valign": 0})

            if self.right_anchor:
                dimension_elements += text(document=document,
                                           text="({:.2f})".format(self.right_anchor),
                                           height=settings["text_dim_height"],
                                           point=(x_rab + settings["text_dim_distance_vertical"],
                                                  y + self.right_anchor / 2),
                                           rotation=90,
                                           attr={"halign": 4, "valign": 0})

            dimension_elements += text(document=document,
                                       text="({:.2f})".format(self.box_width),
                                       height=settings["text_dim_height"],
                                       point=(x + self.box_width / 2,
                                              y + self.box_height + settings["text_dim_distance_horizontal"]),
                                       rotation=0,
                                       attr={"halign": 4, "valign": 0})

        if denomination:
            denomination_elements += text(document=document,
                                          text=self.denomination,
                                          height=settings["text_denomination_height"],
                                          point=(x + self.box_width / 2,
                                                 y + self.box_height - settings["text_denomination_height"] - settings[
                                                     "text_denomination_distance"]),
                                          rotation=0,
                                          attr={"halign": 4, "valign": 0})

        # Setting groups of elements in dictionary.
        elements["steel_elements"] = steel_elements
        elements["dimension_elements"] = dimension_elements
        elements["denomination_elements"] = denomination_elements
        elements["text_elements"] = (elements["dimension_elements"] +
                                     elements["denomination_elements"])
        elements["all_elements"] = (elements["steel_elements"] +
                                    elements["dimension_elements"] +
                                    elements["denomination_elements"])

        if unifilar:
            translate(objects=elements["all_elements"],
                      vector=(0, -self.mandrel_radius_ext))

        # Orienting the bar (direction and orientation).
        self.__direc_orient(elements["all_elements"],
                            x=x,
                            y=y,
                            unifilar=unifilar)

        if self.orientation == Orientation.TOP:
            self.__direct_orient_text(elements["text_elements"])

        return elements

    # Drawing of transverse section of bar function.
    def draw_transverse(self,
                        document: Drawing,
                        x: float = None,
                        y: float = None,
                        settings: dict = BAR_SET_TRANSVERSE) -> dict:
        """
        Draws the transverse section of the bar in a DXF document.

        :param document: The DXF document to draw on.
        :type document: Drawing
        :param x: X coordinate for the drawing, defaults to self.x.
        :type x: float, optional
        :param y: Y coordinate for the drawing, defaults to self.y.
        :type y: float, optional
        :param settings: Dictionary of settings for dimensioning. Defaults to `BAR_SET_TRANSVERSE`.
        :type settings: dict, optional
        :return: Dict of drawing entities for the transverse section.
        :rtype: dict
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        elements = {}
        steel_elements = []

        # Checking if there is a defined transverse center.
        if self.transverse_center:
            x += self.transverse_center[0]
            y += self.transverse_center[1]

        # Drawing of circle.
        steel_elements += circle(doc=document,
                                 center_point=(x + self.radius, y + self.radius),
                                 radius=self.radius)

        # Setting groups of elements in dictionary.
        elements["steel_elements"] = steel_elements
        elements["all_elements"] = elements["steel_elements"]

        return elements

    # Function that orients drawing.
    def __direc_orient(self, group: list, x: float = None, y: float = None, unifilar: bool = False):
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

        # Orienting the bar (direction and orientation).
        # Direction.
        if self.direction == Direction.VERTICAL:
            pivot_point = (x, y + self.box_height)
            vector_translate = (x - (pivot_point[0] * cos(pi / 2) - pivot_point[1] * sin(pi / 2)),
                                y - (pivot_point[0] * sin(pi / 2) + pivot_point[1] * cos(pi / 2)))

            rotate(group, pi / 2)
            translate(group, vector=vector_translate)

            if unifilar:
                translate(group, vector=(-self.diameter, 0))

        # Orientation.
        if self.orientation == Orientation.TOP:
            mirror(objects=group, mirror_type="x")
            if self.direction == Direction.VERTICAL:
                translate(group, vector=(0, self.box_width + y * 2))
            else:
                translate(group, vector=(0, self.box_height + y * 2))
                if unifilar:
                    translate(group, vector=(0, self.radius))

        elif self.orientation == Orientation.RIGHT:
            if self.direction == Direction.VERTICAL:
                if unifilar:
                    translate(group, vector=(-self.mandrel_radius_ext, 0))
            else:
                pass

        elif self.orientation == Orientation.LEFT:
            mirror(objects=group, mirror_type="y")

            if self.direction == Direction.VERTICAL:
                translate(group, vector=(self.box_height + x * 2, 0))
            else:
                translate(group, vector=(self.box_width + x * 2, 0))

    def __direct_orient_text(self, group: list, x: float = None, y: float = None):
        """
        Adjusts the text orientation in the drawing.

        :param group: List of drawing entities to be adjusted.
        :type group: list
        :param x: X coordinate for the text adjustment, defaults to self.x.
        :type x: float, optional
        :param y: Y coordinate for the text adjustment, defaults to self.y.
        :type y: float, optional
        """
        coordinates = [entitie.get_placement()[1] for entitie in group]
        mirror(group, mirror_type="x")

        for i, entitie in enumerate(group):
            entitie.set_placement([-coordinates[i][0], coordinates[i][1], coordinates[i][2]])

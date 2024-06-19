# Imports.
# Local imports.
from drawing_utils import (circle, curve, dim_linear, line, mirror, rads,
                           rect, rotate, text, translate)
from element import Element
from globals import STEEL_WEIGHT

# External imports.
import ezdxf
from ezdxf.document import Drawing
from math import cos, sin, tan, pi

# Constants.
SIN45, COS45 = sin(rads(45)), cos(rads(45))


class Bar(Element):
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
        :type direction: str
        :param orientation: Orientation of the stirrup (top, right, down, left).
        :type orientation: str
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
        ivar length: Length of the bar.
        :ivar weight: Weight of the reinforcement, considering 7850 kg / m3.
        :ivar box_width: Width of the box that contains the bar.
        :ivar box_height: Height of the box that contains the bar.
    """
    def __init__(self, reinforcement_length: float, diameter: float, x: float = 0, y: float = 0, left_anchor: float = 0,
                 right_anchor: float = 0, mandrel_radius: float = 0, direction: str = "horizontal",
                 orientation: str = "down", bend_longitud: float = 0, bend_angle: float = 0, bend_height: float = 0,
                 transverse_center: tuple = None, denomination: None = str):

        super().__init__(width=0, height=reinforcement_length, type="bar", x=x, y=y)

        # Bending attributes.
        self.bend_longitud = bend_longitud
        self.bend_angle = bend_angle
        self.bend_height = bend_height
        self.bending_proyection = bend_height / tan(rads(bend_angle)) if bend_angle else 0

        # Mandrel attributes.
        self.left_anchor = left_anchor
        self.right_anchor = right_anchor
        self.mandrel_radius = mandrel_radius
        self.mandrel_radius_ext = diameter + mandrel_radius

        # Geometric attributes.
        self.diameter = diameter
        self.radius = diameter / 2
        self.direction = direction
        self.orientation = orientation
        self.transverse_center = transverse_center
        self.reinforcement_length = reinforcement_length
        self.length = (reinforcement_length + (1 / cos(rads(bend_angle)) - 1) * self.bending_proyection * 2
                       + left_anchor + right_anchor)
        self.weight = (diameter ** 2 * pi / 4) * self.length * STEEL_WEIGHT

        # Boxing attributes.
        self.box_width = reinforcement_length
        if self.left_anchor or right_anchor or bend_height:
            max_anchor = max([left_anchor, right_anchor])  # Maximum anchor.

            self.box_height = max([self.mandrel_radius_ext + max_anchor,
                                   diameter * 2 + self.bend_height])
        else:
            self.box_height = self.diameter

        # Others.
        self.denomination = denomination

    # Drawing longitudinal function.
    def draw_longitudinal(self, document: Drawing, x: float = None, y: float = None, unifilar: bool = False,
                          dimensions: bool = True, denomination: bool = True) -> list:
        if x is None:
            x = self.x
        if x is None:
            y = self.y

        diameter = self.diameter if not unifilar else 0
        mandrel_radius_ext = self.mandrel_radius_ext if not unifilar else 0
        sides_left_anchor = [0, 1, 1, 1] if not unifilar else [0, 0, 0, 1]
        sides_right_anchor = [0, 1, 1, 1] if not unifilar else [0, 1, 0, 0]

        # Configurations variables.
        text_dim_distance = 0.05
        text_dim_height = 0.05
        text_denom_distance = 0.05
        text_denom_height = 0.05

        # Drawing of simple entities and setting of variables for progressive draw.
        group = []  # Variable that cointains elements objetcs.
        group_text = []  # Variable that cointains text elements objetcs.

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
            group += rect(doc=document, width=diameter, height=self.left_anchor, x=x_lab, y=y_lab,
                          sides=sides_left_anchor)

            if not unifilar:
                # First bend curve.
                group += curve(doc=document, center_point=center_point_lac, radius=self.mandrel_radius,
                               start_angle=90, end_angle=180, thickness=diameter)

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
                group += curve(doc=document, center_point=center_point_rac, radius=self.mandrel_radius, start_angle=0,
                               end_angle=90, thickness=diameter)

            # Second anchor rect bar (right).
            group += rect(doc=document, width=diameter, height=self.right_anchor, x=x_rab, y=y_rab,
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
            group += rect(doc=document, width=length_first_rect_bar, height=diameter, x=x_first_rect_bar,
                          y=y + self.box_height - diameter, sides=sides_first_rect_bar)

            if not unifilar:
                # First curve of bend.
                group += curve(doc=document, center_point=center_point_bc_first, radius=diameter,
                               start_angle=90 - self.bend_angle, end_angle=90, thickness=diameter)

            # First bend rect bar.
            if not unifilar:
                group += line(doc=document,
                              p1=(x + (self.reinforcement_length - self.bend_longitud) / 2 - dx1,
                                  y + self.box_height - self.bend_height - diameter + dy1),
                              p2=(x + (self.reinforcement_length - self.bend_longitud) / 2 - dx1 - longitud_proyeccion,
                                  y + self.box_height - dy2))

            group += line(doc=document,
                          p1=(x + (self.reinforcement_length - self.bend_longitud) / 2 - dx2,
                              y + self.box_height - self.bend_height - diameter * 2 + dy2),
                          p2=(x + (self.reinforcement_length - self.bend_longitud) / 2 - dx2 - longitud_proyeccion,
                              y + self.box_height - diameter - dy1))

            # Second curve of bend.
            if not unifilar:
                group += curve(doc=document, center_point=center_point_bc_second, radius=diameter,
                               start_angle=270 - self.bend_angle, end_angle=270, thickness=diameter)

            # Second rect bar.
            sides_second_rect_bar = [1, 0, 1, 0] if not unifilar else [1, 0, 0, 0]
            group += rect(doc=document, width=self.bend_longitud, height=diameter,
                          x=x + (self.reinforcement_length - self.bend_longitud) / 2,
                          y=y + self.box_height - diameter * 2 - self.bend_height, sides=sides_second_rect_bar)

            # Third bend curve.
            if not unifilar:
                group += curve(doc=document, center_point=(x + longitud_mid,
                                                           y + self.box_height - self.bend_height),
                               radius=diameter, start_angle=270, end_angle=270 + self.bend_angle, thickness=diameter)

            # Second bend bar.
            if not unifilar:
                group += line(doc=document,
                              p1=(x + longitud_mid + dx1,
                                  y + self.box_height - self.bend_height - diameter + dy1),
                              p2=(x + longitud_mid + dx1 + longitud_proyeccion,
                                  y + self.box_height - dy2))

            group += line(doc=document,
                          p1=(x + longitud_mid + dx2,
                              y + self.box_height - self.bend_height - diameter * 2 + dy2),
                          p2=(x + longitud_mid + dx2 + longitud_proyeccion,
                              y + self.box_height - diameter - dy1))

            # Fourth bend curve.
            if not unifilar:
                group += curve(doc=document, center_point=(x + longitud_mid + longitud_curves + longitud_proyeccion,
                                                           y + self.box_height - diameter * 2),
                               radius=diameter, start_angle=90, end_angle=90 + self.bend_angle, thickness=diameter)

            # Third rect bar.
            sides_third_rect_bar = sides_third_rect_bar if not unifilar else [1, 0, 0, 0]
            group += rect(doc=document, width=length_third_rect_bar, height=diameter,
                          x=x + longitud_mid + longitud_curves + longitud_proyeccion,
                          y=y + self.box_height - diameter, sides=sides_third_rect_bar)

        else:
            # From left to right.
            # First rect bar (body).
            sides_first_rect_bar = sides_first_rect_bar if not unifilar else [1, 0, 0, 0]
            mandrel_radius_ext = 0 if not self.left_anchor and not self.right_anchor else mandrel_radius_ext
            group += rect(doc=document, width=length_first_rect_bar, height=diameter, x=x + mandrel_radius_ext,
                          y=y + self.box_height - diameter, sides=sides_first_rect_bar)

        if dimensions:
            if self.left_anchor:
                group += text(document=document, text="({:.2f})".format(self.left_anchor), height=text_dim_height,
                              point=(x_lab - text_dim_distance, y + self.left_anchor / 2), rotation=90,
                              attr={"halign": 4, "valign": 0})
                group_text += [group[-1]]

            if self.right_anchor:
                group += text(document=document, text="({:.2f})".format(self.right_anchor), height=text_dim_height,
                              point=(x_rab + text_dim_distance, y + self.right_anchor / 2), rotation=90,
                              attr={"halign": 4, "valign": 0})
                group_text += [group[-1]]

            group += text(document=document, text="({:.2f})".format(self.box_width), height=text_dim_height,
                          point=(x + self.box_width / 2, y + self.box_height - text_dim_distance), rotation=0,
                          attr={"halign": 4, "valign": 0})
            group_text += [group[-1]]

            if denomination:
                group += text(document=document, text=self.denomination, height=text_denom_height,
                              point=(x + self.box_width / 2,
                                     y + self.box_height / 2 + text_denom_height + text_denom_distance),
                              rotation=0,
                              attr={"halign": 4, "valign": 0})
                group_text += [group[-1]]

        if unifilar:
            translate(objects=group, vector=(0, -self.mandrel_radius_ext))

        # Orienting the bar (direction and orientation).
        self.__direc_orient(group, x=x, y=y, unifilar=unifilar)
        if self.orientation == "top":
            self.__direct_orient_text(group_text)

        return group

    # Drawing of transverse section of bar function.
    def draw_transverse(self, document: Drawing, x: float = None, y: float = None):

        if x is None:
            x = self.x

        if y is None:
            y = self.y

        # Checking if there is a defined transverse center.
        if self.transverse_center:
            x += self.transverse_center[0]
            y += self.transverse_center[1]

        # Drawing of circle.
        group = circle(doc=document, center_point=(x + self.radius, y + self.radius), radius=self.radius)

        return group

    # Function that orients drawing.
    def __direc_orient(self, group: list, x: float = None, y: float = None, unifilar: bool = False):
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        # Orienting the bar (direction and orientation).
        # Direction.
        if self.direction == "vertical":
            pivot_point = (x, y + self.box_height)
            vector_translate = (x - (pivot_point[0] * cos(pi / 2) - pivot_point[1] * sin(pi / 2)),
                                y - (pivot_point[0] * sin(pi / 2) + pivot_point[1] * cos(pi / 2)))

            rotate(group, pi / 2)
            translate(group, vector=vector_translate)

        # Orientation.
        if self.orientation == "top":
            mirror(objects=group, mirror_type="x")
            if self.direction == "vertical":
                translate(group, vector=(0, self.box_width + y * 2))
            else:
                translate(group, vector=(0, self.box_height + y * 2))
                if unifilar:
                    translate(group, vector=(0, self.radius))

        elif self.orientation == "right":
            if self.direction == "vertical":
                if unifilar:
                    translate(group, vector=(-self.mandrel_radius_ext, 0))
            else:
                pass

        elif self.orientation == "left":
            mirror(objects=group, mirror_type="y")

            if self.direction == "vertical":
                translate(group, vector=(self.box_height + x * 2, 0))
            else:
                translate(group, vector=(self.box_width + x * 2, 0))

    def __direct_orient_text(self, group: list, x: float = None, y: float = None):
        coordinates = [entitie.get_placement()[1] for entitie in group]
        mirror(group, mirror_type="x")

        for i, entitie in enumerate(group):
            entitie.set_placement([-coordinates[i][0], coordinates[i][1], coordinates[i][2]])


if __name__ == "__main__":
    doc = ezdxf.new("R2000")

    # Horizontal right bar.
    bar_horizontal_down = Bar(reinforcement_length=4, diameter=.012, left_anchor=.1, right_anchor=.15,
                              mandrel_radius=.012, direction="horizontal", orientation="right")

    bar_horizontal_down.draw_longitudinal(document=doc, x=0, y=0, unifilar=False)
    bar_horizontal_down.draw_transverse(document=doc, x=bar_horizontal_down.reinforcement_length + .5, y=0)

    bar_horizontal_down.draw_longitudinal(document=doc, x=0, y=-.5, unifilar=True)
    bar_horizontal_down.draw_transverse(document=doc, x=bar_horizontal_down.reinforcement_length + .5, y=-.5)

    bar_horizontal_down.draw_longitudinal(document=doc, x=-bar_horizontal_down.reinforcement_length - 1, y=0,
                                          unifilar=False)
    bar_horizontal_down.draw_transverse(document=doc, x=-.5, y=0)

    bar_horizontal_down.draw_longitudinal(document=doc, x=-bar_horizontal_down.reinforcement_length - 1, y=-.5,
                                          unifilar=True)
    bar_horizontal_down.draw_transverse(document=doc, x=-.5, y=-.5)

    bar_horizontal_down.draw_longitudinal(document=doc, x=bar_horizontal_down.reinforcement_length + 1, y=0,
                                          unifilar=True)
    bar_horizontal_down.draw_transverse(document=doc, x=bar_horizontal_down.reinforcement_length * 2 + 1.5, y=0)

    bar_horizontal_down.draw_longitudinal(document=doc, x=bar_horizontal_down.reinforcement_length + 1, y=-.5,
                                          unifilar=False)
    bar_horizontal_down.draw_transverse(document=doc, x=bar_horizontal_down.reinforcement_length * 2 + 1.5, y=-.5)

    # Horizontal top bar.
    bar_horizontal_down = Bar(reinforcement_length=4, diameter=.012, left_anchor=.1, right_anchor=.15,
                              mandrel_radius=.012, direction="horizontal", orientation="top")

    bar_horizontal_down.draw_longitudinal(document=doc, x=bar_horizontal_down.reinforcement_length * 2 + 2, y=0,
                                          unifilar=False)

    # Horizontal left bar.
    yr = -2
    bar_horizontal_left = Bar(reinforcement_length=4, diameter=.012, left_anchor=.15, right_anchor=.1,
                              mandrel_radius=.012, direction="horizontal", orientation="left")

    bar_horizontal_left.draw_longitudinal(document=doc, x=0, y=yr + 0, unifilar=False)
    bar_horizontal_left.draw_transverse(document=doc, x=bar_horizontal_down.reinforcement_length + .5, y=yr + 0)

    bar_horizontal_left.draw_longitudinal(document=doc, x=0, y=yr - .5, unifilar=True)
    bar_horizontal_left.draw_transverse(document=doc, x=bar_horizontal_down.reinforcement_length + .5, y=yr - .5)

    bar_horizontal_left.draw_longitudinal(document=doc, x=-bar_horizontal_down.reinforcement_length - 1, y=yr + 0,
                                          unifilar=False)
    bar_horizontal_left.draw_transverse(document=doc, x=-.5, y=yr + 0)

    bar_horizontal_left.draw_longitudinal(document=doc, x=-bar_horizontal_down.reinforcement_length - 1, y=yr - .5,
                                          unifilar=True)
    bar_horizontal_left.draw_transverse(document=doc, x=-.5, y=yr - .5)

    bar_horizontal_left.draw_longitudinal(document=doc, x=bar_horizontal_down.reinforcement_length + 1, y=yr + 0,
                                          unifilar=True)
    bar_horizontal_left.draw_transverse(document=doc, x=bar_horizontal_down.reinforcement_length * 2 + 1.5, y=yr + 0)

    bar_horizontal_left.draw_longitudinal(document=doc, x=bar_horizontal_down.reinforcement_length + 1, y=yr - .5,
                                          unifilar=False)
    bar_horizontal_left.draw_transverse(document=doc, x=bar_horizontal_down.reinforcement_length * 2 + 1.5, y=yr - .5)

    # Vertical right bar.
    xr, yr = 0, 2
    bar_vertical_right = Bar(reinforcement_length=4, diameter=.012, left_anchor=.15, right_anchor=.1,
                             mandrel_radius=.012, direction="vertical", orientation="right")

    bar_vertical_right.draw_longitudinal(document=doc, x=0, y=yr, unifilar=False)

    bar_vertical_right.draw_longitudinal(document=doc, x=.5, y=yr, unifilar=True)

    bar_vertical_right.draw_longitudinal(document=doc, x=-bar_horizontal_down.reinforcement_length - 1, y=yr,
                                         unifilar=False)

    bar_vertical_right.draw_longitudinal(document=doc, x=-bar_horizontal_down.reinforcement_length - 1.5, y=yr,
                                         unifilar=True)

    bar_vertical_right.draw_longitudinal(document=doc, x=bar_horizontal_down.reinforcement_length + 1, y=yr,
                                         unifilar=True)

    bar_vertical_right.draw_longitudinal(document=doc, x=bar_horizontal_down.reinforcement_length + 1.5, y=yr,
                                         unifilar=False)

    doc.saveas("c:/users/beta/desktop/bar.dxf")

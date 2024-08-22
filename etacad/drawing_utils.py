# Imports.
# Local imports.
from etacad.globals import Direction

# External imports.
import ezdxf
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.document import Drawing
from ezdxf.transform import inplace, scale
from ezdxf.math import Matrix44
from ezdxf.enums import TextEntityAlignment
from ezdxf.tools.standards import linetypes

from math import pi

# Classes references.
doc_class = Drawing
attrib_class = GfxAttribs

linetypes_list = linetypes(scale=0.1)
lt_center = linetypes_list[1]

# Matrix transformation definition.
matrix_x_mirror = Matrix44([1, 0, 0, 0],
                           [0, -1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1])

matrix_y_mirror = Matrix44([-1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1])


# Function that draws a circunference.
def circle(doc: Drawing, center_point: tuple, radius: float, attr=None):

    if not isinstance(doc, Drawing):
        return []

    msp = doc.modelspace()

    # Drawing of circle.
    circ = [msp.add_circle(center_point, radius=radius, dxfattribs=attr)]

    return circ


# Function that draws a curve with/out thickness.
def curve(doc: Drawing, center_point: tuple, radius: float, start_angle: float, end_angle: float, thickness: float = 0,
          attr=None) -> list:

    if not isinstance(doc, Drawing):
        return []

    msp = doc.modelspace()

    # Drawing of arc.
    arcs = [msp.add_arc(center_point, radius=radius, start_angle=start_angle, end_angle=end_angle, dxfattribs=attr)]

    if thickness:
        arcs += [msp.add_arc(center_point, radius=radius + thickness, start_angle=start_angle, end_angle=end_angle,
                             dxfattribs=attr)]

    return arcs


# Create a delimit axe and rerturns and list with elements.
def delimit_axe(document: Drawing, x: float, y: float, height: float = 1, radius: float = 0.1, text_height: float = 0.1,
                symbol: str = None, direction: Direction = Direction.VERTICAL, attr: GfxAttribs = None) -> list:

    document.linetypes.add(name=lt_center[0], description=lt_center[1], pattern=lt_center[2])
    msp = document.modelspace()

    if direction == Direction.VERTICAL:
        group = [msp.add_line(start=(x, y), end=(x, y + height), dxfattribs=attr)]
        if symbol is not None:
            group += [msp.add_circle(center=(x, y + height + radius), radius=radius)]
            group += [msp.add_text(text=symbol, height=text_height).set_placement(
                p1=(x, y + height + radius), align=TextEntityAlignment.MIDDLE_CENTER)]

    elif direction == Direction.HORIZONTAL:
        group = [msp.add_line(start=(x + radius, y), end=(x + radius + height, y), dxfattribs=attr)]
        if symbol is not None:
            group += [msp.add_circle(center=(x, y), radius=radius)]
            group += [msp.add_text(text=symbol, height=text_height).set_placement(
                p1=(x, y), align=TextEntityAlignment.MIDDLE_CENTER)]

    else:
        raise ValueError

    return group


# Draws a linear dimension.
def dim_linear(document: Drawing, p_base: tuple, p1: tuple, p2: tuple, rotation: float = 0,
               dimstyle: str = "EZ_M_25_H25_CM", attr: GfxAttribs = None) -> list:
    msp = document.modelspace()

    dims = [msp.add_linear_dim(base=p_base, p1=p1, p2=p2, dimstyle=dimstyle, angle=rotation, dxfattribs=attr)]
    dims[-1].render()

    return dims


# Returns the a and b constants of the line equation from two poins.
def get_line_eq(x1, y1, x2, y2):
    if x1 == x2:  # For vertical lines.
        a = float(9999999999)  # Aproximate infinite.
        b = - a * x1

    else:  # For not vertical lines.
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

    return a, b


# Returns the intersection of two lines.
def get_lines_intersec(a1: float, b1: float, a2: float, b2: float) -> float:

    x = (b2 - b1) / (a1 - a2)

    return x


# Function that draws a line.
def line(doc: Drawing, p1: tuple, p2: tuple, attr=None) -> list:

    line_segment = doc.modelspace().add_line(p1, p2, dxfattribs=attr)

    return [line_segment]


# Function that mirrors a given group of objects.
def mirror(objects: list, mirror_type: str, in_situ: bool = False) -> int:
    # Axis "x" mirror.
    if "x" in mirror_type:
        inplace(objects, matrix_x_mirror)

    # Axis "y" mirror.
    if "y" in mirror_type:
        inplace(objects, matrix_y_mirror)

    return 1


# Returns the points ordered in function of X coordinate.
def point_order(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float, float, float]:
    if x1 <= x2:
        return x1, y1, x2, y2
    else:
        return x2, y2, x1, y1


# Function that transform degrees to radians.
def rads(degrees: float) -> float:
    return degrees * pi / 180


# Function that draws a rectangle in dxf file given.
def rect(doc: Drawing, width: float, height: float, x: float, y: float, sides=None, fill: bool = False,
         polyline: bool = False, attr=None) -> list:

    if sides is None:
        sides = [1, 1, 1, 1]

    if not isinstance(doc, Drawing):
        return []

    msp = doc.modelspace()
    lines = []

    # Polyline rectangle.
    if polyline:
        lines.append(msp.add_lwpolyline([(x, y), (x + width, y), (x + width, y + height), (x, y + height), (x, y)],
                                        dxfattribs=attr))
    else:
        # Horizontal lines.
        if sides[0]:
            lines.append(msp.add_line((x, y + height), (x + width, y + height), dxfattribs=attr))  # Top side.
        if sides[2]:
            lines.append(msp.add_line((x, y), (x + width, y), dxfattribs=attr))  # Bottom side.

        # Vertical lines.
        if sides[1]:
            lines.append(msp.add_line((x + width, y), (x + width, y + height), dxfattribs=attr))  # Right side.
        if sides[3]:
            lines.append(msp.add_line((x, y), (x, y + height), dxfattribs=attr))  # Left side.

    if fill:
        hatch = msp.add_hatch(color=7, dxfattribs=attr)
        hatch.paths.add_polyline_path([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])
        hatch.set_pattern_fill("ANSI31", scale=0.01)
        lines.append(hatch)

    return lines


# Function that draws a rectangle in dxf file given.
def rect_border_curve(doc: Drawing, width: float, height: float, radius: float, x: float, y: float,
                      thickness: float = 0, sides=None, curves=None, curves_radius=None, attr=None) -> list:

    if sides is None:
        sides = [1, 1, 1, 1]

    if curves is None:
        curves = [1, 1, 1, 1]

    if curves_radius is None:
        curves_radius = [radius, radius, radius, radius]

    if not isinstance(doc, Drawing):
        return []

    msp = doc.modelspace()
    lines = []

    # Horizontal lines.
    if sides[0]:
        lines.append(msp.add_line(start=(x + curves_radius[0], y + height),
                                  end=(x - curves_radius[1] + width, y + height),  dxfattribs=attr))  # Top side.
    if sides[2]:
        lines.append(msp.add_line(start=(x + curves_radius[3], y),
                                  end=(x - curves_radius[2] + width, y), dxfattribs=attr))  # Bottom side.

    # Vertical lines.
    if sides[1]:
        lines.append(msp.add_line(start=(x + width, y + curves_radius[2]),
                                  end=(x + width, y - curves_radius[1] + height), dxfattribs=attr))  # Right side.
    if sides[3]:
        lines.append(msp.add_line(start=(x, y + curves_radius[3]),
                                  end=(x, y - curves_radius[0] + height), dxfattribs=attr))  # Left side.

    if thickness:
        # Horizontal lines borders.
        if sides[0]:
            lines.append(msp.add_line(start=(x + curves_radius[0], y + thickness + height),
                                      end=(x - curves_radius[1] + width, y + thickness + height),
                                      dxfattribs=attr))  # Top side.
        if sides[2]:
            lines.append(msp.add_line(start=(x + curves_radius[3], y - thickness),
                                      end=(x - curves_radius[2] + width, y - thickness),
                                      dxfattribs=attr))  # Bottom side.

        # Vertical lines borders.
        if sides[1]:
            lines.append(msp.add_line(start=(x + thickness + width, y + curves_radius[2]),
                                      end=(x + thickness + width, y - curves_radius[1] + height),
                                      dxfattribs=attr))  # Right side.
        if sides[3]:
            lines.append(msp.add_line(start=(x - thickness, y + curves_radius[3]),
                                      end=(x - thickness, y - curves_radius[0] + height),
                                      dxfattribs=attr))  # Left side.

    # Curves.
    if (sides[0] or sides[3]) and curves[0]:
        lines += curve(doc=doc, center_point=(x + curves_radius[0], y - curves_radius[0] + height),
                       start_angle=90, end_angle=180, radius=curves_radius[0], thickness=thickness, attr=attr)
    if (sides[0] or sides[1]) and curves[1]:
        lines += curve(doc=doc, center_point=(x - curves_radius[1] + width, y - curves_radius[1] + height), start_angle=0, end_angle=90,
                       radius=curves_radius[1], thickness=thickness, attr=attr)
    if (sides[1] or sides[2]) and curves[2]:
        lines += curve(doc=doc, center_point=(x - curves_radius[2] + width, y + curves_radius[2]), start_angle=270, end_angle=360,
                       radius=curves_radius[2], thickness=thickness, attr=attr)
    if (sides[2] or sides[3]) and curves[3]:
        lines += curve(doc=doc, center_point=(x + curves_radius[3], y + curves_radius[3]), start_angle=180, end_angle=270,
                       radius=curves_radius[3], thickness=thickness, attr=attr)

    return lines


# Function that rotates elements.
def rotate(objects: list, angle: float) -> int:

    ezdxf.transform.z_rotate(entities=objects, angle=angle)

    return 1


# Function that draws simple text.
def text(document: Drawing, text: str, height: float, point: tuple, rotation: float = 0, attr = None) -> list:
    msp = document.modelspace()

    group = msp.add_text(text=text, height=height, rotation=rotation, dxfattribs=attr).set_placement(point)

    return [group]


# Function that translates a group of elements.
def translate(objects: list, vector: tuple) -> int:

    ezdxf.transform.translate(entities=objects, offset=vector)

    return 1

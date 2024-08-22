# Local imports.
from etacad.globals import ColumnTypes, Direction, Orientation, STEEL_WEIGHT
from etacad.bar import Bar

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3
from math import pi


@pytest.fixture
def bar_straight_horizontal():
    return Bar(reinforcement_length=12,
               diameter=0.012,
               x=1,
               y=1,
               left_anchor=0,
               right_anchor=0,
               mandrel_radius=0,
               direction=Direction.HORIZONTAL,
               orientation=Orientation.BOTTOM,
               bend_longitud=0,
               bend_angle=0,
               bend_height=0,
               transverse_center=None,
               denomination="@bar_straight_horizontal")


def test_attributes_bar_straight_horizontal(bar_straight_horizontal):
    # Bending attributes.
    assert bar_straight_horizontal.bend_longitud == 0
    assert bar_straight_horizontal.bend_angle == 0
    assert bar_straight_horizontal.bend_height == 0
    assert bar_straight_horizontal.bending_proyection == 0

    # Mandrel attributes.
    assert bar_straight_horizontal.left_anchor == 0
    assert bar_straight_horizontal.right_anchor == 0
    assert bar_straight_horizontal.mandrel_radius == 0
    assert bar_straight_horizontal.mandrel_radius_ext == 0.012

    # Geometric attributes.
    assert bar_straight_horizontal.diameter == 0.012
    assert bar_straight_horizontal.radius == 0.006
    assert bar_straight_horizontal.direction == Direction.HORIZONTAL
    assert bar_straight_horizontal.orientation == Orientation.BOTTOM
    assert bar_straight_horizontal.transverse_center is None
    assert bar_straight_horizontal.reinforcement_length == 12
    assert bar_straight_horizontal.length == 12
    assert bar_straight_horizontal.weight == ((0.012 ** 2) * pi / 4) * 12 * STEEL_WEIGHT

    # Boxing attributes.
    assert bar_straight_horizontal.box_width == 12
    assert bar_straight_horizontal.box_height == 0.012

    # Others.
    assert bar_straight_horizontal.denomination == "@bar_straight_horizontal"


def test_draw_longitudinal_bar_straight_horizontal(bar_straight_horizontal):
    doc = ezdxf.new(dxfversion="R2010", setup=True)

    ex_01 = bar_straight_horizontal.draw_longitudinal(document=doc, x=2, y=1, unifilar=False, dimensions=False)
    assert len(ex_01) == 5
    assert ex_01[0].dxf.start == Vec3(2, 1.012, 0)  # Top side start.
    assert ex_01[0].dxf.end == Vec3(14, 1.012, 0)  # Top side end.
    assert ex_01[1].dxf.start == Vec3(2, 1, 0)  # Bottom side start.
    assert ex_01[1].dxf.end == Vec3(14, 1, 0)  # Bottom side end.

    ex_02 = bar_straight_horizontal.draw_longitudinal(document=doc, x=2, y=0, unifilar=False, denomination=False)
    assert len(ex_02) == 5
    assert ex_02[0].dxf.start == Vec3(2, 0.012, 0)  # Top side start.
    assert ex_02[0].dxf.end == Vec3(14, 0.012, 0)  # Top side end.
    assert ex_02[1].dxf.start == Vec3(2, 0, 0)  # Bottom side start.
    assert ex_02[1].dxf.end == Vec3(14, 0, 0)  # Bottom side end.

    ex_03 = bar_straight_horizontal.draw_longitudinal(document=doc, x=2, y=-1, unifilar=False)
    assert len(ex_03) == 6
    assert ex_03[0].dxf.start == Vec3(2, -0.988, 0)  # Top side start.
    assert ex_03[0].dxf.end == Vec3(14, -0.988, 0)  # Top side end.
    assert ex_03[1].dxf.start == Vec3(2, -1, 0)  # Bottom side start.
    assert ex_03[1].dxf.end == Vec3(14, -1, 0)  # Bottom side end.

    ex_04 = bar_straight_horizontal.draw_longitudinal(document=doc, x=-12, y=1, unifilar=False, dimensions=False)
    assert len(ex_04) == 5
    assert ex_04[0].dxf.start == Vec3(-12, 1.012, 0)  # Top side start.
    assert ex_04[0].dxf.end == Vec3(0, 1.012, 0)  # Top side end.
    assert ex_04[1].dxf.start == Vec3(-12, 1, 0)  # Bottom side start.
    assert ex_04[1].dxf.end == Vec3(0, 1, 0)  # Bottom side end.

    ex_05 = bar_straight_horizontal.draw_longitudinal(document=doc, x=-12, y=0, unifilar=False, denomination=False)
    assert len(ex_05) == 5
    assert ex_05[0].dxf.start == Vec3(-12, 0.012, 0)  # Top side start.
    assert ex_05[0].dxf.end == Vec3(0, 0.012, 0)  # Top side end.
    assert ex_05[1].dxf.start == Vec3(-12, 0, 0)  # Bottom side start.
    assert ex_05[1].dxf.end == Vec3(0, 0, 0)  # Bottom side end.

    ex_06 = bar_straight_horizontal.draw_longitudinal(document=doc, x=-12, y=-1, unifilar=False)
    assert len(ex_06) == 6
    assert ex_06[0].dxf.start == Vec3(-12, -0.988, 0)  # Top side start.
    assert ex_06[0].dxf.end == Vec3(0, -0.988, 0)  # Top side end.
    assert ex_06[1].dxf.start == Vec3(-12, -1, 0)  # Bottom side start.
    assert ex_06[1].dxf.end == Vec3(0, -1, 0)  # Bottom side end.

    ex_07 = bar_straight_horizontal.draw_longitudinal(document=doc, x=2, y=2, unifilar=True)
    assert len(ex_07) == 3
    assert ex_07[0].dxf.start == Vec3(2, 2, 0)  # Top side start.
    assert ex_07[0].dxf.end == Vec3(14, 2, 0)  # Top side end.
    assert ex_07[0].dxf.end[0] - ex_07[0].dxf.start[0] == 12

    ex_08 = bar_straight_horizontal.draw_longitudinal(document=doc, x=-12, y=2, unifilar=True)
    assert len(ex_08) == 3
    assert ex_08[0].dxf.start == Vec3(-12, 2, 0)
    assert ex_08[0].dxf.end == Vec3(0, 2, 0)
    assert ex_08[0].dxf.end[0] - ex_08[0].dxf.start[0] == 12

    # General.
    entities = ex_01 + ex_02 + ex_03 + ex_04 + ex_05 + ex_06 + ex_07 + ex_08
    assert len(entities) == 38

    doc.saveas(filename="./tests/bar_straight_horizontal.dxf")


@pytest.fixture
def bar_straight_vertical():
    return Bar(reinforcement_length=12,
               diameter=0.01,
               x=1,
               y=1,
               left_anchor=0,
               right_anchor=0,
               mandrel_radius=0,
               direction=Direction.VERTICAL,
               orientation=Orientation.BOTTOM,
               bend_longitud=0,
               bend_angle=0,
               bend_height=0,
               transverse_center=None,
               denomination="@bar_straight_vertical")


def test_attributes_bar_straight_vertical(bar_straight_vertical):
    # Bending attributes.
    assert bar_straight_vertical.bend_longitud == 0
    assert bar_straight_vertical.bend_angle == 0
    assert bar_straight_vertical.bend_height == 0
    assert bar_straight_vertical.bending_proyection == 0

    # Mandrel attributes.
    assert bar_straight_vertical.left_anchor == 0
    assert bar_straight_vertical.right_anchor == 0
    assert bar_straight_vertical.mandrel_radius == 0
    assert bar_straight_vertical.mandrel_radius_ext == 0.01

    # Geometric attributes.
    assert bar_straight_vertical.diameter == 0.01
    assert bar_straight_vertical.radius == 0.005
    assert bar_straight_vertical.direction == Direction.VERTICAL
    assert bar_straight_vertical.orientation == Orientation.BOTTOM
    assert bar_straight_vertical.transverse_center is None
    assert bar_straight_vertical.reinforcement_length == 12
    assert bar_straight_vertical.length == 12
    assert bar_straight_vertical.weight == ((0.01 ** 2) * pi / 4) * 12 * STEEL_WEIGHT

    # Boxing attributes.
    assert bar_straight_vertical.box_width == 12
    assert bar_straight_vertical.box_height == 0.01

    # Others.
    assert bar_straight_vertical.denomination == "@bar_straight_vertical"


def test_draw_longitudinal_bar_straight_vertical(bar_straight_vertical):
    doc = ezdxf.new(dxfversion="R2010", setup=True)

    ex_01 = bar_straight_vertical.draw_longitudinal(document=doc, x=-2, y=1, unifilar=False, dimensions=False)
    assert len(ex_01) == 5
    assert ex_01[0].dxf.start == Vec3(-2, 1, 0)  # Top side start.
    assert ex_01[0].dxf.end == Vec3(-1.9999999999999991, 13, 0)  # Top side end.
    assert ex_01[1].dxf.start == Vec3(-1.99, 1, 0)  # Bottom side start.
    assert ex_01[1].dxf.end == Vec3(-1.989999999999999, 13, 0)  # Bottom side end.

    ex_02 = bar_straight_vertical.draw_longitudinal(document=doc, x=-1, y=1, unifilar=False, denomination=False)
    assert len(ex_02) == 5
    assert ex_02[0].dxf.start == Vec3(-1, 1, 0)  # Top side start.
    assert ex_02[0].dxf.end == Vec3(-0.9999999999999993, 13, 0)  # Top side end.
    assert ex_02[1].dxf.start == Vec3(-0.99, 1, 0)  # Bottom side start.
    assert ex_02[1].dxf.end == Vec3(-0.9899999999999993, 13, 0)  # Bottom side end.

    ex_03 = bar_straight_vertical.draw_longitudinal(document=doc, x=0, y=1, unifilar=False)
    assert len(ex_03) == 6
    assert ex_03[0].dxf.start == Vec3(0, 1, 0)  # Top side start.
    assert ex_03[0].dxf.end == Vec3(6.661338147750939e-16, 13, 0)  # Top side end.
    assert ex_03[1].dxf.start == Vec3(0.010000000000000009, 1, 0)  # Bottom side start.
    assert ex_03[1].dxf.end == Vec3(0.010000000000000786, 13, 0)  # Bottom side end.

    ex_04 = bar_straight_vertical.draw_longitudinal(document=doc, x=1, y=1, unifilar=True, dimensions=False)
    assert len(ex_04) == 2
    assert ex_04[0].dxf.start == Vec3(0.9999999999999998, 1, 0)  # Top side start.
    assert ex_04[0].dxf.end == Vec3(1.0000000000000007, 13, 0)  # Top side end.

    ex_05 = bar_straight_vertical.draw_longitudinal(document=doc, x=2, y=1, unifilar=True)
    assert len(ex_05) == 3
    assert ex_05[0].dxf.start == Vec3(1.9999999999999998, 1, 0)  # Top side start.
    assert ex_05[0].dxf.end == Vec3(2.000000000000001, 13, 0)  # Top side end.

    # General.
    entities = ex_01 + ex_02 + ex_03 + ex_04 + ex_05
    assert len(entities) == 21

    doc.saveas(filename="./tests/bar_straight_vertical.dxf")

# Local imports.
from etacad.globals import Direction, Orientation, STEEL_WEIGHT
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
    assert len(ex_01["all_elements"]) == 5
    assert ex_01["steel_elements"][0].dxf.start == Vec3(2, 1.012, 0)  # Top side start.
    assert ex_01["steel_elements"][0].dxf.end == Vec3(14, 1.012, 0)  # Top side end.
    assert ex_01["steel_elements"][1].dxf.start == Vec3(2, 1, 0)  # Bottom side start.
    assert ex_01["steel_elements"][1].dxf.end == Vec3(14, 1, 0)  # Bottom side end.

    ex_02 = bar_straight_horizontal.draw_longitudinal(document=doc, x=2, y=0, unifilar=False, denomination=False)
    assert len(ex_02["all_elements"]) == 5
    assert ex_02["steel_elements"][0].dxf.start == Vec3(2, 0.012, 0)  # Top side start.
    assert ex_02["steel_elements"][0].dxf.end == Vec3(14, 0.012, 0)  # Top side end.
    assert ex_02["steel_elements"][1].dxf.start == Vec3(2, 0, 0)  # Bottom side start.
    assert ex_02["steel_elements"][1].dxf.end == Vec3(14, 0, 0)  # Bottom side end.

    ex_03 = bar_straight_horizontal.draw_longitudinal(document=doc, x=2, y=-1, unifilar=False)
    assert len(ex_03["all_elements"]) == 6
    assert ex_03["steel_elements"][0].dxf.start == Vec3(2, -0.988, 0)  # Top side start.
    assert ex_03["steel_elements"][0].dxf.end == Vec3(14, -0.988, 0)  # Top side end.
    assert ex_03["steel_elements"][1].dxf.start == Vec3(2, -1, 0)  # Bottom side start.
    assert ex_03["steel_elements"][1].dxf.end == Vec3(14, -1, 0)  # Bottom side end.

    ex_04 = bar_straight_horizontal.draw_longitudinal(document=doc, x=-12, y=1, unifilar=False, dimensions=False)
    assert len(ex_04["all_elements"]) == 5
    assert ex_04["steel_elements"][0].dxf.start == Vec3(-12, 1.012, 0)  # Top side start.
    assert ex_04["steel_elements"][0].dxf.end == Vec3(0, 1.012, 0)  # Top side end.
    assert ex_04["steel_elements"][1].dxf.start == Vec3(-12, 1, 0)  # Bottom side start.
    assert ex_04["steel_elements"][1].dxf.end == Vec3(0, 1, 0)  # Bottom side end.

    ex_05 = bar_straight_horizontal.draw_longitudinal(document=doc, x=-12, y=0, unifilar=False, denomination=False)
    assert len(ex_05["all_elements"]) == 5
    assert ex_05["steel_elements"][0].dxf.start == Vec3(-12, 0.012, 0)  # Top side start.
    assert ex_05["steel_elements"][0].dxf.end == Vec3(0, 0.012, 0)  # Top side end.
    assert ex_05["steel_elements"][1].dxf.start == Vec3(-12, 0, 0)  # Bottom side start.
    assert ex_05["steel_elements"][1].dxf.end == Vec3(0, 0, 0)  # Bottom side end.

    ex_06 = bar_straight_horizontal.draw_longitudinal(document=doc, x=-12, y=-1, unifilar=False)
    assert len(ex_06["all_elements"]) == 6
    assert ex_06["steel_elements"][0].dxf.start == Vec3(-12, -0.988, 0)  # Top side start.
    assert ex_06["steel_elements"][0].dxf.end == Vec3(0, -0.988, 0)  # Top side end.
    assert ex_06["steel_elements"][1].dxf.start == Vec3(-12, -1, 0)  # Bottom side start.
    assert ex_06["steel_elements"][1].dxf.end == Vec3(0, -1, 0)  # Bottom side end.

    ex_07 = bar_straight_horizontal.draw_longitudinal(document=doc, x=2, y=2, unifilar=True)
    assert len(ex_07["all_elements"]) == 3
    assert ex_07["steel_elements"][0].dxf.start == Vec3(2, 2, 0)  # Top side start.
    assert ex_07["steel_elements"][0].dxf.end == Vec3(14, 2, 0)  # Top side end.
    assert ex_07["steel_elements"][0].dxf.end[0] - ex_07["steel_elements"][0].dxf.start[0] == 12

    ex_08 = bar_straight_horizontal.draw_longitudinal(document=doc, x=-12, y=2, unifilar=True)
    assert len(ex_08["all_elements"]) == 3
    assert ex_08["steel_elements"][0].dxf.start == Vec3(-12, 2, 0)
    assert ex_08["steel_elements"][0].dxf.end == Vec3(0, 2, 0)
    assert ex_08["steel_elements"][0].dxf.end[0] - ex_08["steel_elements"][0].dxf.start[0] == 12

    doc.saveas(filename="./tests/bar_straight_horizontal.dxf")

    # General.
    entities = (ex_01["all_elements"] + ex_02["all_elements"] + ex_03["all_elements"] + ex_04["all_elements"] +
                ex_05["all_elements"] + ex_06["all_elements"] + ex_07["all_elements"] + ex_08["all_elements"])
    assert len(entities) == 38


def test_extract_data_bar_straight_horizontal(bar_straight_horizontal):
    assert bar_straight_horizontal.extract_data(["diameter", "length"]) == [0.012, 12]


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
    assert len(ex_01["all_elements"]) == 5
    assert ex_01["steel_elements"][0].dxf.start == Vec3(-2, 1, 0)  # Top side start.
    assert ex_01["steel_elements"][0].dxf.end == Vec3(-1.9999999999999991, 13, 0)  # Top side end.
    assert ex_01["steel_elements"][1].dxf.start == Vec3(-1.99, 1, 0)  # Bottom side start.
    assert ex_01["steel_elements"][1].dxf.end == Vec3(-1.989999999999999, 13, 0)  # Bottom side end.

    ex_02 = bar_straight_vertical.draw_longitudinal(document=doc, x=-1, y=1, unifilar=False, denomination=False)
    assert len(ex_02["all_elements"]) == 5
    assert ex_02["steel_elements"][0].dxf.start == Vec3(-1, 1, 0)  # Top side start.
    assert ex_02["steel_elements"][0].dxf.end == Vec3(-0.9999999999999993, 13, 0)  # Top side end.
    assert ex_02["steel_elements"][1].dxf.start == Vec3(-0.99, 1, 0)  # Bottom side start.
    assert ex_02["steel_elements"][1].dxf.end == Vec3(-0.9899999999999993, 13, 0)  # Bottom side end.

    ex_03 = bar_straight_vertical.draw_longitudinal(document=doc, x=0, y=1, unifilar=False)
    assert len(ex_03["all_elements"]) == 6
    assert ex_03["steel_elements"][0].dxf.start == Vec3(0, 1, 0)  # Top side start.
    assert ex_03["steel_elements"][0].dxf.end == Vec3(6.661338147750939e-16, 13, 0)  # Top side end.
    assert ex_03["steel_elements"][1].dxf.start == Vec3(0.010000000000000009, 1, 0)  # Bottom side start.
    assert ex_03["steel_elements"][1].dxf.end == Vec3(0.010000000000000786, 13, 0)  # Bottom side end.

    ex_04 = bar_straight_vertical.draw_longitudinal(document=doc, x=1, y=1, unifilar=True, dimensions=False)
    assert len(ex_04["all_elements"]) == 2
    assert ex_04["steel_elements"][0].dxf.start == Vec3(0.9999999999999998, 1, 0)  # Top side start.
    assert ex_04["steel_elements"][0].dxf.end == Vec3(1.0000000000000007, 13, 0)  # Top side end.

    ex_05 = bar_straight_vertical.draw_longitudinal(document=doc, x=2, y=1, unifilar=True)
    assert len(ex_05["all_elements"]) == 3
    assert ex_05["steel_elements"][0].dxf.start == Vec3(1.9999999999999998, 1, 0)  # Top side start.
    assert ex_05["steel_elements"][0].dxf.end == Vec3(2.000000000000001, 13, 0)  # Top side end.

    # General.
    entities = (ex_01["all_elements"] + ex_02["all_elements"] + ex_03["all_elements"] + ex_04["all_elements"] +
                ex_05["all_elements"])
    assert len(entities) == 21

    doc.saveas(filename="./tests/bar_straight_vertical.dxf")


@pytest.fixture
def bar_straight_horizontal_lab():
    return Bar(reinforcement_length=4,
               diameter=0.01,
               x=0,
               y=0,
               left_anchor=0.15,
               right_anchor=0,
               mandrel_radius=0.01,
               direction=Direction.HORIZONTAL,
               orientation=Orientation.BOTTOM,
               bend_longitud=0,
               bend_angle=0,
               bend_height=0,
               denomination="bar_straight_vertical_lab")


def test_attributes_straight_horizontal_lab(bar_straight_horizontal_lab):
    # Bending attributes.
    assert bar_straight_horizontal_lab.bend_longitud == 0
    assert bar_straight_horizontal_lab.bend_angle == 0
    assert bar_straight_horizontal_lab.bend_height == 0
    assert bar_straight_horizontal_lab.bending_proyection == 0

    # Mandrel attributes.
    assert bar_straight_horizontal_lab.left_anchor == 0.15
    assert bar_straight_horizontal_lab.right_anchor == 0
    assert bar_straight_horizontal_lab.mandrel_radius == 0.01
    assert bar_straight_horizontal_lab.mandrel_radius_ext == 0.02

    # Geometric attributes.
    assert bar_straight_horizontal_lab.diameter == 0.01
    assert bar_straight_horizontal_lab.radius == 0.005
    assert bar_straight_horizontal_lab.direction == Direction.HORIZONTAL
    assert bar_straight_horizontal_lab.orientation == Orientation.BOTTOM
    assert bar_straight_horizontal_lab.transverse_center is None
    assert bar_straight_horizontal_lab.reinforcement_length == 4
    assert bar_straight_horizontal_lab.length == 4.15
    assert bar_straight_horizontal_lab.weight == ((0.01 ** 2) * pi / 4) * 4.15 * STEEL_WEIGHT

    # Boxing attributes.
    assert bar_straight_horizontal_lab.box_width == 4
    assert bar_straight_horizontal_lab.box_height == 0.16999999999999998

    # Others.
    assert bar_straight_horizontal_lab.denomination == "bar_straight_vertical_lab"


@pytest.fixture
def bar_straight_hotizontal_rab():
    pass


@pytest.fixture
def bar_straight_horizontal_lab_rab():
    pass

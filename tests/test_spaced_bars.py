# -*- coding: utf-8 -*-

# Local imports.
from etacad.globals import Direction, Orientation
from etacad.spaced_bars import SpacedBars

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3


@pytest.fixture()
def spaced_bar_horizontal() -> SpacedBars:
    return SpacedBars(
        reinforcement_length=4,
        length=6,
        diameter=0.01,
        spacing=0.12,
        x=10,
        y=10,
        direction=Direction.HORIZONTAL,
        orientation=Orientation.BOTTOM,
        transverse_center=(0, 0.2),
        left_anchor=0,
        right_anchor=0,
        mandrel_radius=0,
        bend_longitud=0,
        bend_angle=0,
        bend_height=0,
        description="R1")


def test_attributes_spaced_bar_horizontal(spaced_bar_horizontal):
    # Spaced bars attributes.
    assert spaced_bar_horizontal.reinforcement_length == 4
    assert spaced_bar_horizontal.length == 6
    assert spaced_bar_horizontal.diameter == 0.01
    assert spaced_bar_horizontal.spacing == 0.12
    assert spaced_bar_horizontal.x == 10
    assert spaced_bar_horizontal.y == 10
    assert spaced_bar_horizontal.radius == 0.005
    assert spaced_bar_horizontal.direction == Direction.HORIZONTAL
    assert spaced_bar_horizontal.orientation == Orientation.BOTTOM
    assert spaced_bar_horizontal.transverse_center == (0, 0.2)
    assert spaced_bar_horizontal.quantity == 34

    # Bar attributes.
    assert len(spaced_bar_horizontal.bars) == 34

    # Bar bending attributes.
    assert spaced_bar_horizontal.bend_longitud == 0
    assert spaced_bar_horizontal.bend_angle == 0
    assert spaced_bar_horizontal.bend_height == 0

    # Boxing attributes.
    assert spaced_bar_horizontal._box_width == 6
    assert spaced_bar_horizontal._box_height == 3.9699999999999998

    # Physics attributes.
    assert spaced_bar_horizontal.weight == 125.77366188646737


def test_draw_longitudinal_spaced_bars_horizontal(spaced_bar_horizontal):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_horizontal.draw_longitudinal(document=doc, x=2, y=1, unifilar=False, dimensions=True)
    ex_02 = spaced_bar_horizontal.draw_longitudinal(document=doc, x=9, y=1, unifilar=True, dimensions=True)
    ex_03 = spaced_bar_horizontal.draw_longitudinal(document=doc, x=2, y=-5, unifilar=False, dimensions=True, one_bar=True)
    ex_04 = spaced_bar_horizontal.draw_longitudinal(document=doc, x=9, y=-5, unifilar=True, dimensions=True, one_bar=True)
    doc.saveas(filename="./tests/spaced_bars_horizontal_draw_longitudinal.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 140
    assert len(ex_01["bar_elements"]) == 34
    assert len(ex_01["dimension_elements"]) == 3

    # Steel position.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(2, 1.01, 0)  # Top side start.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(8, 1.01, 0)  # Top side end.
    assert ex_01["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(2, 1, 0)  # Bottom side start.
    assert ex_01["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(8, 1, 0)  # Bottom side end.
    assert ex_01["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(8, 1, 0)  # Right side start.
    assert ex_01["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(8, 1.01, 0)  # Right side end.
    assert ex_01["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(2, 1, 0)  # Left side start.
    assert ex_01["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(2, 1.01, 0)  # Left side end.

    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(2, 4.97, 0)  # Top side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(8, 4.97, 0)  # Top side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][1].dxf.start == Vec3(2, 4.96, 0)  # Bottom side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][1].dxf.end == Vec3(8, 4.96, 0)  # Bottom side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.start == Vec3(8, 4.96, 0)  # Right side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.end == Vec3(8, 4.97, 0)  # Right side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][3].dxf.start == Vec3(2, 4.96, 0)  # Left side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][3].dxf.end == Vec3(2, 4.97, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_01["dimension_elements"][0].dxf.insert == Vec3(5.0, 2.3699999999999997, 0)  # Dimension text.
    assert ex_01["bar_elements"][11]["denomination_elements"][0].dxf.insert == Vec3(5.0, 2.28, 0)  # Description text.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 38
    assert len(ex_02["bar_elements"]) == 34
    assert len(ex_02["dimension_elements"]) == 3

    # Steel position.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(9, 1, 0)  # First bar start.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(15, 1, 0)  # First bar end.

    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(9, 4.96, 0)  # Last bar start.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(15, 4.96, 0)  # Last bar end.

    # Dimension and description texts.
    assert ex_02["dimension_elements"][0].dxf.insert == Vec3(12, 2.3699999999999997, 0)  # Dimension text.
    assert ex_02["bar_elements"][11]["denomination_elements"][0].dxf.insert == Vec3(12, 2.27, 0)  # Description text.

    # Example 03.
    # General.
    assert len(ex_03["all_elements"]) == 8
    assert len(ex_03["bar_elements"]) == 1
    assert len(ex_03["dimension_elements"]) == 3

    # Steel position.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(2, -3.6700000000000004, 0)  # Top side start.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(8, -3.6700000000000004, 0)  # Top side end.
    assert ex_03["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(2, -3.68, 0)  # Bottom side start.
    assert ex_03["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(8, -3.68, 0)  # Bottom side end.
    assert ex_03["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(8, -3.68, 0)  # Right side start.
    assert ex_03["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(8, -3.6700000000000004, 0)  # Right side end.
    assert ex_03["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(2, -3.68, 0)  # Left side start.
    assert ex_03["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(2, -3.6700000000000004, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_03["dimension_elements"][0].dxf.insert == Vec3(5, -3.6300000000000003, 0)  # Dimension text.
    assert ex_03["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(5, -3.72, 0)  # Description text.

    # Example 04.
    # General.
    assert len(ex_04["all_elements"]) == 5
    assert len(ex_04["bar_elements"]) == 1
    assert len(ex_04["dimension_elements"]) == 3

    # Steel position.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(9, -3.68, 0)  # First bar start.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(15, -3.68, 0)  # First bar end.

    # Dimension and description texts.
    assert ex_04["dimension_elements"][0].dxf.insert == Vec3(12, -3.6300000000000003, 0)  # Dimension text.
    assert ex_04["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(12, -3.73, 0)  # Description text.


def test_draw_transverse_spaced_bars_horizontal(spaced_bar_horizontal):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_horizontal.draw_transverse(document=doc, dimensions=True, x=0, y=0)
    doc.saveas(filename="./tests/spaced_bars_horizontal_draw_transverse.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 39
    assert len(ex_01["dimension_elements"]) == 1
    assert len(ex_01["description_elements"]) == 4
    assert len(ex_01["bar_elements"]) == 34

    # Steel elements.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(0.005, 0.20500000000000002, 0)  # First.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(0.005, 4.165, 0)  # Last.


def test_extract_data_spaced_bars_horizontal(spaced_bar_horizontal):
    data = spaced_bar_horizontal.extract_data(labels=["diameter"])
    assert len(data) == 1
    assert data == [0.01]

    data = spaced_bar_horizontal.extract_data(labels=["diameter", "length", "quantity"])
    assert len(data) == 3
    assert data == [0.01, 6, 34]

    data = spaced_bar_horizontal.extract_data()
    assert data == ["R1", 6, 0.01, 125.77366188646737, 34, 0.12]


def test_draw_transverse_rotate_spaced_bars_horizontal(spaced_bar_horizontal):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_horizontal.draw_transverse(document=doc, x=10, y=10, dimensions=True, rotate_angle=0)
    ex_02 = spaced_bar_horizontal.draw_transverse(document=doc, x=10, y=10, dimensions=True, rotate_angle=45)
    doc.saveas(filename="./tests/spaced_bars_horizontal_draw_transverse_rotate.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 39
    assert len(ex_01["dimension_elements"]) == 1
    assert len(ex_01["description_elements"]) == 4
    assert len(ex_01["bar_elements"]) == 34

    # Steel elements.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(10.005, 10.20500000000000002, 0)  # First.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(10.005, 14.165000000000001, 0)  # Last.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 39
    assert len(ex_02["dimension_elements"]) == 1
    assert len(ex_02["description_elements"]) == 4
    assert len(ex_02["bar_elements"]) == 34

    # Steel elements.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(10, 10.207071067811865, 0)  # First.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(7.19985714650127, 13.007213921310594, 0)  # Last.


@pytest.fixture()
def spaced_bar_horizontal_oe() -> SpacedBars:
    return SpacedBars(
        reinforcement_length=5.95,
        length=3,
        diameter=0.016,
        spacing=0.1,
        x=-10,
        y=10,
        direction=Direction.HORIZONTAL,
        orientation=Orientation.BOTTOM,
        transverse_center=(0.1, 0.1),
        left_anchor=0,
        right_anchor=0,
        mandrel_radius=0,
        bend_longitud=0,
        bend_angle=0,
        bend_height=0,
        description="R2")


def test_attributes_spaced_bar_horizontal_oe(spaced_bar_horizontal_oe):
    # Spaced bars attributes.
    assert spaced_bar_horizontal_oe.reinforcement_length == 5.95
    assert spaced_bar_horizontal_oe.length == 3
    assert spaced_bar_horizontal_oe.diameter == 0.016
    assert spaced_bar_horizontal_oe.spacing == 0.1
    assert spaced_bar_horizontal_oe.x == -10
    assert spaced_bar_horizontal_oe.y == 10
    assert spaced_bar_horizontal_oe.radius == 0.008
    assert spaced_bar_horizontal_oe.direction == Direction.HORIZONTAL
    assert spaced_bar_horizontal_oe.orientation == Orientation.BOTTOM
    assert spaced_bar_horizontal_oe.transverse_center == (0.1, 0.1)
    assert spaced_bar_horizontal_oe.quantity == 60

    # Bar attributes.
    assert len(spaced_bar_horizontal_oe.bars) == 60

    # Bar bending attributes.
    assert spaced_bar_horizontal_oe.bend_longitud == 0
    assert spaced_bar_horizontal_oe.bend_angle == 0
    assert spaced_bar_horizontal_oe.bend_height == 0

    # Boxing attributes.
    assert spaced_bar_horizontal_oe._box_width == 3
    assert spaced_bar_horizontal_oe._box_height == 5.916

    # Physics attributes.
    assert spaced_bar_horizontal_oe.weight == 284.1005068494321


def test_draw_longitudinal_spaced_bars_horizontal_oe(spaced_bar_horizontal_oe):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_horizontal_oe.draw_longitudinal(document=doc, x=2, y=1, unifilar=False, dimensions=True)
    ex_02 = spaced_bar_horizontal_oe.draw_longitudinal(document=doc, x=9, y=1, unifilar=True, dimensions=True)
    ex_03 = spaced_bar_horizontal_oe.draw_longitudinal(document=doc, x=2, y=-5, unifilar=False, dimensions=True, one_bar=True)
    ex_04 = spaced_bar_horizontal_oe.draw_longitudinal(document=doc, x=9, y=-5, unifilar=True, dimensions=True, one_bar=True)

    ex_05 = spaced_bar_horizontal_oe.draw_longitudinal(document=doc, x=2, y=-9, unifilar=False, dimensions=True, other_extreme=True)
    ex_06 = spaced_bar_horizontal_oe.draw_longitudinal(document=doc, x=9, y=-9, unifilar=True, dimensions=True, other_extreme=True)
    ex_07 = spaced_bar_horizontal_oe.draw_longitudinal(document=doc, x=2, y=-13, unifilar=False, dimensions=True, one_bar=True, other_extreme=True)
    ex_08 = spaced_bar_horizontal_oe.draw_longitudinal(document=doc, x=9, y=-13, unifilar=True, dimensions=True, one_bar=True, other_extreme=True)
    doc.saveas(filename="./tests/spaced_bars_horizontal_oe_draw_longitudinal.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 244
    assert len(ex_01["bar_elements"]) == 60
    assert len(ex_01["dimension_elements"]) == 3

    # Steel attributes.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(2, 1.016, 0)  # Top side start.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(5, 1.016, 0)  # Top side end.
    assert ex_01["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(2, 1, 0)  # Bottom side start.
    assert ex_01["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(5, 1, 0)  # Bottom side end.
    assert ex_01["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(5, 1, 0)  # Right side start.
    assert ex_01["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(5, 1.016, 0)  # Right side end.
    assert ex_01["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(2, 1, 0)  # Left side start.
    assert ex_01["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(2, 1.016, 0)  # Left side end.

    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(2, 6.916, 0)  # Top side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(5, 6.916, 0)  # Top side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][1].dxf.start == Vec3(2, 6.9, 0)  # Bottom side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][1].dxf.end == Vec3(5, 6.90, 0)  # Bottom side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.start == Vec3(5, 6.9, 0)  # Right side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.end == Vec3(5, 6.916, 0)  # Right side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][3].dxf.start == Vec3(2, 6.9, 0)  # Left side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][3].dxf.end == Vec3(2, 6.916, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_01["dimension_elements"][0].dxf.insert == Vec3(3.5, 3.05, 0)  # Dimension text.
    assert ex_01["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(3.5, 2.966, 0)  # Description text.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 64
    assert len(ex_02["bar_elements"]) == 60
    assert len(ex_02["dimension_elements"]) == 3

    # Steel position.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(9, 1, 0)  # First bar start.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(12, 1, 0)  # First bar end.

    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(9, 6.9, 0)  # Last bar start.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(12, 6.9, 0)  # Last bar end.

    # Dimension and description texts.
    assert ex_02["dimension_elements"][0].dxf.insert == Vec3(10.5, 3.05, 0)  # Dimension text.
    assert ex_02["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(10.5, 2.95, 0)  # Description text.

    # Example 03.
    # General.
    assert len(ex_03["all_elements"]) == 8
    assert len(ex_03["bar_elements"]) == 1
    assert len(ex_03["dimension_elements"]) == 3

    # Steel position.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(2, -2.984, 0)  # Top side start.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(5, -2.984, 0)  # Top side end.
    assert ex_03["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(2, -3, 0)  # Bottom side start.
    assert ex_03["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(5, -3, 0)  # Bottom side end.
    assert ex_03["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(5, -3, 0)  # Right side start.
    assert ex_03["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(5, -2.984, 0)  # Right side end.
    assert ex_03["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(2, -3, 0)  # Left side start.
    assert ex_03["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(2, -2.984, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_03["dimension_elements"][0].dxf.insert == Vec3(3.5, -2.95, 0)  # Dimension text.
    assert ex_03["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(3.5, -3.034, 0)  # Description text.

    # Example 04.
    assert len(ex_04["all_elements"]) == 5
    assert len(ex_04["bar_elements"]) == 1
    assert len(ex_04["dimension_elements"]) == 3

    # Steel position.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(9, -3, 0)  # First bar start.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(12, -3, 0)  # First bar end.

    # Dimension and description texts.
    assert ex_04["dimension_elements"][0].dxf.insert == Vec3(10.5, -2.95, 0)  # Dimension text.
    assert ex_04["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(10.5, -3.05, 0)  # Description text.

    # Example 05.
    # General.
    assert len(ex_05["all_elements"]) == 244
    assert len(ex_05["bar_elements"]) == 60
    assert len(ex_05["dimension_elements"]) == 3

    # Steel attributes.
    assert ex_05["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(2, -8.934, 0.0)  # Top side start.
    assert ex_05["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(5, -8.934, 0.0)  # Top side end.
    assert ex_05["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(2, -8.95, 0.0)  # Bottom side start.
    assert ex_05["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(5, -8.95, 0)  # Bottom side end.
    assert ex_05["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(5, -8.95, 0)  # Right side start.
    assert ex_05["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(5, -8.934, 0)  # Right side end.
    assert ex_05["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(2, -8.95, 0)  # Left side start.
    assert ex_05["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(2, -8.934, 0)  # Left side end.

    assert ex_05["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(2, -3.033999999999999, 0)  # Top side start.
    assert ex_05["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(5, -3.033999999999999, 0)  # Top side end.
    assert ex_05["bar_elements"][-1]["steel_elements"][1].dxf.start == Vec3(2, -3.049999999999999, 0)  # Bottom side start.
    assert ex_05["bar_elements"][-1]["steel_elements"][1].dxf.end == Vec3(5, -3.049999999999999, 0)  # Bottom side end.
    assert ex_05["bar_elements"][-1]["steel_elements"][2].dxf.start == Vec3(5, -3.049999999999999, 0)  # Right side start.
    assert ex_05["bar_elements"][-1]["steel_elements"][2].dxf.end == Vec3(5, -3.033999999999999, 0)  # Right side end.
    assert ex_05["bar_elements"][-1]["steel_elements"][3].dxf.start == Vec3(2, -3.049999999999999, 0)  # Left side start.
    assert ex_05["bar_elements"][-1]["steel_elements"][3].dxf.end == Vec3(2, -3.033999999999999, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_05["dimension_elements"][0].dxf.insert == Vec3(3.5, -6.8999999999999995, 0)  # Dimension text.
    assert ex_05["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(3.5, -6.983999999999999, 0)  # Description text.

    # Example 06.
    # General.
    assert len(ex_06["all_elements"]) == 64
    assert len(ex_06["bar_elements"]) == 60
    assert len(ex_06["dimension_elements"]) == 3

    # Steel position.
    assert ex_06["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(9, -8.95, 0)  # First bar start.
    assert ex_06["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(12, -8.95, 0)  # First bar end.

    assert ex_06["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(9, -3.049999999999999, 0)  # Last bar start.
    assert ex_06["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(12, -3.049999999999999, 0)  # Last bar end.

    # Dimension and description texts.
    assert ex_06["dimension_elements"][0].dxf.insert == Vec3(10.5, -6.8999999999999995, 0)  # Dimension text.
    assert ex_06["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(10.5, -6.999999999999999, 0)  # Description text.

    # Example 07.
    # General.
    assert len(ex_07["all_elements"]) == 8
    assert len(ex_07["bar_elements"]) == 1
    assert len(ex_07["dimension_elements"]) == 3

    # Steel position.
    assert ex_07["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(2, -10.934, 0.0)  # Top side start.
    assert ex_07["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(5, -10.934, 0.0)  # Top side end.
    assert ex_07["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(2, -10.95, 0.0)  # Bottom side start.
    assert ex_07["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(5, -10.95, 0)  # Bottom side end.
    assert ex_07["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(5, -10.95, 0.0)  # Right side start.
    assert ex_07["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(5, -10.934, 0)  # Right side end.
    assert ex_07["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(2, -10.95, 0)  # Left side start.
    assert ex_07["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(2, -10.934, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_07["dimension_elements"][0].dxf.insert == Vec3(3.5, -10.899999999999999, 0.0)  # Dimension text.
    assert ex_07["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(3.5, -10.984, 0)  # Description text.

    # Example 08.
    assert len(ex_08["all_elements"]) == 5
    assert len(ex_08["bar_elements"]) == 1
    assert len(ex_08["dimension_elements"]) == 3

    # Steel position.
    assert ex_08["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(9, -10.95, 0.0)  # First bar start.
    assert ex_08["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(12, -10.95, 0)  # First bar end.

    # Dimension and description texts.
    assert ex_08["dimension_elements"][0].dxf.insert == Vec3(10.5, -10.899999999999999, 0)  # Dimension text.
    assert ex_08["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(10.5, -11.0, 0)  # Description text.


def test_draw_transverse_spaced_bars_horizontal_oe(spaced_bar_horizontal_oe):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_horizontal_oe.draw_transverse(document=doc, x=1, y=1, dimensions=True)
    ex_02 = spaced_bar_horizontal_oe.draw_transverse(document=doc, x=2, y=1, dimensions=True, other_extreme=True)
    doc.saveas(filename="./tests/spaced_bars_horizontal_oe_draw_transverse.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 65
    assert len(ex_01["dimension_elements"]) == 1
    assert len(ex_01["description_elements"]) == 4
    assert len(ex_01["bar_elements"]) == 60

    # Steel elements.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(1.108, 1.108, 0)  # First.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(1.108, 7.008, 0)  # Last.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 65
    assert len(ex_02["dimension_elements"]) == 1
    assert len(ex_02["description_elements"]) == 4
    assert len(ex_02["bar_elements"]) == 60

    # Steel elements.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(2.108, 1.158, 0)  # First.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(2.108, 7.058000000000001, 0.0)  # Last.


def test_draw_transverse_rotate_spaced_bars_horizontal_oe(spaced_bar_horizontal_oe):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_horizontal_oe.draw_transverse(document=doc, x=10, y=10, dimensions=True, rotate_angle=0)
    ex_02 = spaced_bar_horizontal_oe.draw_transverse(document=doc, x=10, y=10, dimensions=True, rotate_angle=45)
    ex_03 = spaced_bar_horizontal_oe.draw_transverse(document=doc, x=16, y=10, dimensions=True, rotate_angle=0, other_extreme=True)
    ex_04 = spaced_bar_horizontal_oe.draw_transverse(document=doc, x=16, y=10, dimensions=True, rotate_angle=45, other_extreme=True)
    doc.saveas(filename="./tests/spaced_bars_horizontal_oe_draw_transverse_rotate.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 65
    assert len(ex_01["dimension_elements"]) == 1
    assert len(ex_01["description_elements"]) == 4
    assert len(ex_01["bar_elements"]) == 60

    # Steel elements.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(10.107999999999999, 10.107999999999999, 0.0)  # First.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(10.107999999999999, 16.008, 0.0)  # Last.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 65
    assert len(ex_02["dimension_elements"]) == 1
    assert len(ex_02["description_elements"]) == 4
    assert len(ex_02["bar_elements"]) == 60

    # Steel elements.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(10.1, 10.111313708498983, 0)  # First.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(5.928069990999368, 14.283243717499614, 0)  # Last.

    # Example 03.
    # General.
    assert len(ex_03["all_elements"]) == 65
    assert len(ex_03["dimension_elements"]) == 1
    assert len(ex_03["description_elements"]) == 4
    assert len(ex_03["bar_elements"]) == 60

    # Steel elements.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(16.108, 10.158, 0.0)  # First.
    assert ex_03["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(16.108, 16.058, 0.0)  # Last.

    # Example 04.
    # General.
    assert len(ex_04["all_elements"]) == 65
    assert len(ex_04["dimension_elements"]) == 1
    assert len(ex_04["description_elements"]) == 4
    assert len(ex_04["bar_elements"]) == 60

    # Steel elements.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(16.064644660940672, 10.146669047558309, 0)  # First.
    assert ex_04["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(11.892714651940043, 14.318599056558938, 0)  # Last.


@pytest.fixture()
def spaced_bar_vertical() -> SpacedBars:
    return SpacedBars(
        reinforcement_length=6,
        length=3,
        diameter=0.016,
        spacing=0.1,
        x=-10,
        y=10,
        direction=Direction.VERTICAL,
        orientation=Orientation.BOTTOM,
        transverse_center=(0.1, 0.1),
        left_anchor=0,
        right_anchor=0,
        mandrel_radius=0,
        bend_longitud=0,
        bend_angle=0,
        bend_height=0,
        description="R2")


def test_attributes_spaced_bar_vertical(spaced_bar_vertical):
    # Spaced bars attributes.
    assert spaced_bar_vertical.reinforcement_length == 6
    assert spaced_bar_vertical.length == 3
    assert spaced_bar_vertical.diameter == 0.016
    assert spaced_bar_vertical.spacing == 0.1
    assert spaced_bar_vertical.x == -10
    assert spaced_bar_vertical.y == 10
    assert spaced_bar_vertical.radius == 0.008
    assert spaced_bar_vertical.direction == Direction.VERTICAL
    assert spaced_bar_vertical.orientation == Orientation.BOTTOM
    assert spaced_bar_vertical.transverse_center == (0.1, 0.1)
    assert spaced_bar_vertical.quantity == 61

    # Bar attributes.
    assert len(spaced_bar_vertical.bars) == 61

    # Bar bending attributes.
    assert spaced_bar_vertical.bend_longitud == 0
    assert spaced_bar_vertical.bend_angle == 0
    assert spaced_bar_vertical.bend_height == 0

    # Boxing attributes.
    assert spaced_bar_vertical._box_width == 3
    assert spaced_bar_vertical._box_height == 6.016

    # Physics attributes.
    assert spaced_bar_vertical.weight == 288.83551529692267


def test_draw_longitudinal_spaced_bars_vertical(spaced_bar_vertical):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_vertical.draw_longitudinal(document=doc, x=2, y=1, unifilar=False, dimensions=True)
    ex_02 = spaced_bar_vertical.draw_longitudinal(document=doc, x=9, y=1, unifilar=True, dimensions=True)
    ex_03 = spaced_bar_vertical.draw_longitudinal(document=doc, x=2, y=-5, unifilar=False, dimensions=True, one_bar=True)
    ex_04 = spaced_bar_vertical.draw_longitudinal(document=doc, x=9, y=-5, unifilar=True, dimensions=True, one_bar=True)
    doc.saveas(filename="./tests/spaced_bars_vertical_draw_longitudinal.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 248
    assert len(ex_01["bar_elements"]) == 61
    assert len(ex_01["dimension_elements"]) == 3

    # Steel attributes.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(8, 0.9999999999999996, 0)  # Top side start.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(8, 3.9999999999999996, 0)  # Top side end.
    assert ex_01["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(8.016, 0.9999999999999996, 0)  # Bottom side start.
    assert ex_01["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(8.016, 3.9999999999999996, 0)  # Bottom side end.
    assert ex_01["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(8.016, 3.9999999999999996, 0)  # Right side start.
    assert ex_01["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(8, 3.9999999999999996, 0)  # Right side end.
    assert ex_01["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(8.016, 0.9999999999999996, 0)  # Left side start.
    assert ex_01["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(8, 0.9999999999999996, 0)  # Left side end.

    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(2, 1.0, 0)  # Top side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(2, 3.9999999999999996, 0)  # Top side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][1].dxf.start == Vec3(2.016, 1, 0)  # Bottom side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][1].dxf.end == Vec3(2.016, 3.9999999999999996, 0)  # Bottom side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.start == Vec3(2.016, 3.9999999999999996, 0)  # Right side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.end == Vec3(2, 3.9999999999999996, 0)  # Right side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][3].dxf.start == Vec3(2.016, 1, 0)  # Left side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][3].dxf.end == Vec3(2, 1, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_01["dimension_elements"][0].dxf.insert == Vec3(5.966, 2.4999999999999996, 0)  # Dimension text.
    assert ex_01["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(6.05, 2.4999999999999996, 0)  # Description text.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 65
    assert len(ex_02["bar_elements"]) == 61
    assert len(ex_02["dimension_elements"]) == 3

    # Steel position.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(14.999999999999998, 1, 0)  # First bar start.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(14.999999999999998, 4.0, 0)  # First bar end.

    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(8.999999999999998, 1, 0)  # Last bar start.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(8.999999999999998, 4.0, 0)  # Last bar end.

    # Dimension and description texts.
    assert ex_02["dimension_elements"][0].dxf.insert == Vec3(12.95, 2.5, 0)  # Dimension text.
    assert ex_02["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(13.049999999999999, 2.5, 0)  # Description text.

    # Example 03.
    # General.
    assert len(ex_03["all_elements"]) == 8
    assert len(ex_03["bar_elements"]) == 1
    assert len(ex_03["dimension_elements"]) == 3

    # Steel position.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(6, -5, 0)  # Top side start.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(6, -2, 0)  # Top side end.
    assert ex_03["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(6.016, -5, 0)  # Bottom side start.
    assert ex_03["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(6.016, -2, 0)  # Bottom side end.
    assert ex_03["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(6.016, -2, 0)  # Right side start.
    assert ex_03["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(6, -2, 0)  # Right side end.
    assert ex_03["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(6.016, -5, 0)  # Left side start.
    assert ex_03["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(6, -5, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_03["dimension_elements"][0].dxf.insert == Vec3(5.966, -3.5, 0.0)  # Dimension text.
    assert ex_03["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(6.05, -3.5, 0.0)  # Description text.

    # Example 04.
    assert len(ex_04["all_elements"]) == 5
    assert len(ex_04["bar_elements"]) == 1
    assert len(ex_04["dimension_elements"]) == 3

    # Steel position.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(13, -5, 0)  # First bar start.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(13.000000000000002, -2, 0)  # First bar end.

    # Dimension and description texts.
    assert ex_04["dimension_elements"][0].dxf.insert == Vec3(12.950000000000001, -3.5, 0.0)  # Dimension text.
    assert ex_04["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(13.05, -3.5, 0.0)  # Description text.


def test_draw_transverse_spaced_bars_vertical(spaced_bar_vertical):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_vertical.draw_transverse(document=doc, x=2.1, y=1, dimensions=True)
    doc.saveas(filename="./tests/spaced_bars_vertical_draw_transverse.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 66
    assert len(ex_01["dimension_elements"]) == 1
    assert len(ex_01["description_elements"]) == 4
    assert len(ex_01["bar_elements"]) == 61

    # Steel elements.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(8.207999999999998, 1.1079999999999997, 0)  # First.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(2.2079999999999993, 1.108, 0)  # Last.


def test_draw_transverse_rotate_spaced_bars_vertical(spaced_bar_vertical):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_vertical.draw_transverse(document=doc, x=10, y=10, dimensions=True, rotate_angle=0)
    ex_02 = spaced_bar_vertical.draw_transverse(document=doc, x=10, y=10, dimensions=True, rotate_angle=45)
    doc.saveas(filename="./tests/spaced_bars_vertical_draw_transverse_rotate.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 66
    assert len(ex_01["dimension_elements"]) == 1
    assert len(ex_01["description_elements"]) == 4
    assert len(ex_01["bar_elements"]) == 61

    # Steel elements.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(16.108000000000004, 10.107999999999997, 0)  # First.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(10.108, 10.107999999999999, 0)  # Last.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 66
    assert len(ex_02["dimension_elements"]) == 1
    assert len(ex_02["description_elements"]) == 4
    assert len(ex_02["bar_elements"]) == 61

    # Steel elements.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(14.34264068711929, 14.353954395618272, 0.0)  # First.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(10.100000000000001, 10.111313708498985, 0.0)  # Last.


@pytest.fixture()
def spaced_bar_vertical_oe() -> SpacedBars:
    return SpacedBars(
        reinforcement_length=5.95,
        length=3,
        diameter=0.016,
        spacing=0.1,
        x=-10,
        y=10,
        direction=Direction.VERTICAL,
        orientation=Orientation.BOTTOM,
        transverse_center=(0.1, 0.1),
        left_anchor=0,
        right_anchor=0,
        mandrel_radius=0,
        bend_longitud=0,
        bend_angle=0,
        bend_height=0,
        description="R2")


def test_attributes_spaced_bar_vertical_oe(spaced_bar_vertical_oe):
    # Spaced bars attributes.
    assert spaced_bar_vertical_oe.reinforcement_length == 5.95
    assert spaced_bar_vertical_oe.length == 3
    assert spaced_bar_vertical_oe.diameter == 0.016
    assert spaced_bar_vertical_oe.spacing == 0.1
    assert spaced_bar_vertical_oe.x == -10
    assert spaced_bar_vertical_oe.y == 10
    assert spaced_bar_vertical_oe.radius == 0.008
    assert spaced_bar_vertical_oe.direction == Direction.VERTICAL
    assert spaced_bar_vertical_oe.orientation == Orientation.BOTTOM
    assert spaced_bar_vertical_oe.transverse_center == (0.1, 0.1)
    assert spaced_bar_vertical_oe.quantity == 60

    # Bar attributes.
    assert len(spaced_bar_vertical_oe.bars) == 60

    # Bar bending attributes.
    assert spaced_bar_vertical_oe.bend_longitud == 0
    assert spaced_bar_vertical_oe.bend_angle == 0
    assert spaced_bar_vertical_oe.bend_height == 0

    # Boxing attributes.
    assert spaced_bar_vertical_oe._box_width == 3
    assert spaced_bar_vertical_oe._box_height == 5.916

    # Physics attributes.
    assert spaced_bar_vertical_oe.weight == 284.1005068494321


def test_draw_longitudinal_spaced_bars_vertical_oe(spaced_bar_vertical_oe):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_vertical_oe.draw_longitudinal(document=doc, x=2, y=1, unifilar=False, dimensions=True)
    ex_02 = spaced_bar_vertical_oe.draw_longitudinal(document=doc, x=9, y=1, unifilar=True, dimensions=True)
    ex_03 = spaced_bar_vertical_oe.draw_longitudinal(document=doc, x=2, y=-5, unifilar=False, dimensions=True, one_bar=True)
    ex_04 = spaced_bar_vertical_oe.draw_longitudinal(document=doc, x=9, y=-5, unifilar=True, dimensions=True, one_bar=True)

    ex_05 = spaced_bar_vertical_oe.draw_longitudinal(document=doc, x=2, y=-9, unifilar=False, dimensions=True, other_extreme=True)
    ex_06 = spaced_bar_vertical_oe.draw_longitudinal(document=doc, x=9, y=-9, unifilar=True, dimensions=True, other_extreme=True)
    ex_07 = spaced_bar_vertical_oe.draw_longitudinal(document=doc, x=2, y=-13, unifilar=False, dimensions=True, one_bar=True, other_extreme=True)
    ex_08 = spaced_bar_vertical_oe.draw_longitudinal(document=doc, x=9, y=-13, unifilar=True, dimensions=True, one_bar=True, other_extreme=True)
    doc.saveas(filename="./tests/spaced_bars_vertical_oe_draw_longitudinal.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 244
    assert len(ex_01["bar_elements"]) == 60
    assert len(ex_01["dimension_elements"]) == 3

    # Steel attributes.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(7.9, 0.9999999999999996, 0)  # Top side start.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(7.9, 3.9999999999999996, 0)  # Top side end.
    assert ex_01["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(7.916, 0.9999999999999996, 0)  # Bottom side start.
    assert ex_01["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(7.916, 3.9999999999999996, 0)  # Bottom side end.
    assert ex_01["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(7.916, 3.9999999999999996, 0)  # Right side start.
    assert ex_01["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(7.9, 3.9999999999999996, 0)  # Right side end.
    assert ex_01["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(7.916, 0.9999999999999996, 0)  # Left side start.
    assert ex_01["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(7.9, 0.9999999999999996, 0)  # Left side end.

    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(2, 1.0, 0)  # Top side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(2, 3.9999999999999996, 0)  # Top side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][1].dxf.start == Vec3(2.016, 1, 0)  # Bottom side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][1].dxf.end == Vec3(2.016, 3.9999999999999996, 0)  # Bottom side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.start == Vec3(2.016, 3.9999999999999996, 0)  # Right side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.end == Vec3(2, 3.9999999999999996, 0)  # Right side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][3].dxf.start == Vec3(2.016, 1, 0)  # Left side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][3].dxf.end == Vec3(2, 1, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_01["dimension_elements"][0].dxf.insert == Vec3(5.8660000000000005, 2.4999999999999996, 0)  # Dimension text.
    assert ex_01["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(5.95, 2.4999999999999996, 0)  # Description text.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 64
    assert len(ex_02["bar_elements"]) == 60
    assert len(ex_02["dimension_elements"]) == 3

    # Steel position.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(14.90, 1, 0)  # First bar start.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(14.90, 4.0, 0)  # First bar end.

    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(9.000000000000002, 1, 0)  # Last bar start.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(9.000000000000002, 4.0, 0)  # Last bar end.

    # Dimension and description texts.
    assert ex_02["dimension_elements"][0].dxf.insert == Vec3(12.850000000000001, 2.5, 0.0)  # Dimension text.
    assert ex_02["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(12.950000000000001, 2.5, 0.0)  # Description text.

    # Example 03.
    # General.
    assert len(ex_03["all_elements"]) == 8
    assert len(ex_03["bar_elements"]) == 1
    assert len(ex_03["dimension_elements"]) == 3

    # Steel position.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(5.9, -5, 0)  # Top side start.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(5.9, -2, 0)  # Top side end.
    assert ex_03["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(5.916, -5, 0)  # Bottom side start.
    assert ex_03["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(5.916, -2, 0)  # Bottom side end.
    assert ex_03["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(5.916, -2, 0)  # Right side start.
    assert ex_03["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(5.9, -2, 0)  # Right side end.
    assert ex_03["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(5.916, -5, 0)  # Left side start.
    assert ex_03["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(5.9, -5, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_03["dimension_elements"][0].dxf.insert == Vec3(5.8660000000000005, -3.5, 0.0)  # Dimension text.
    assert ex_03["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(5.95, -3.5, 0.0)  # Description text.

    # Example 04.
    assert len(ex_04["all_elements"]) == 5
    assert len(ex_04["bar_elements"]) == 1
    assert len(ex_04["dimension_elements"]) == 3

    # Steel position.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(12.9, -5, 0)  # First bar start.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(12.9, -2, 0)  # First bar end.

    # Dimension and description texts.
    assert ex_04["dimension_elements"][0].dxf.insert == Vec3(12.850000000000001, -3.5, 0.0)  # Dimension text.
    assert ex_04["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(12.950000000000001, -3.5, 0.0)  # Description text.

    # Example 05.
    # General.
    assert len(ex_05["all_elements"]) == 244
    assert len(ex_05["bar_elements"]) == 60
    assert len(ex_05["dimension_elements"]) == 3

    # Steel attributes.
    assert ex_05["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(7.949999999999999, -9.0, 0.0)  # Top side start.
    assert ex_05["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(7.949999999999999, -6.000000000000001, 0.0)  # Top side end.
    assert ex_05["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(7.965999999999999, -9.0, 0.0)  # Bottom side start.
    assert ex_05["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(7.965999999999999, -6.000000000000001, 0)  # Bottom side end.
    assert ex_05["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(7.965999999999999, -6.000000000000001, 0)  # Right side start.
    assert ex_05["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(7.949999999999999, -6.000000000000001, 0)  # Right side end.
    assert ex_05["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(7.965999999999999, -9, 0)  # Left side start.
    assert ex_05["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(7.949999999999999, -9, 0)  # Left side end.

    assert ex_05["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(2.049999999999999, -9.0, 0.0)  # Top side start.
    assert ex_05["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(2.0499999999999994, -6.0, 0.0)  # Top side end.
    assert ex_05["bar_elements"][-1]["steel_elements"][1].dxf.start == Vec3(2.065999999999999, -9.0, 0.0)  # Bottom side start.
    assert ex_05["bar_elements"][-1]["steel_elements"][1].dxf.end == Vec3(2.0659999999999994, -6.0, 0.0)  # Bottom side end.
    assert ex_05["bar_elements"][-1]["steel_elements"][2].dxf.start == Vec3(2.0659999999999994, -6.0, 0.0)  # Right side start.
    assert ex_05["bar_elements"][-1]["steel_elements"][2].dxf.end == Vec3(2.0499999999999994, -6.0, 0.0)  # Right side end.
    assert ex_05["bar_elements"][-1]["steel_elements"][3].dxf.start == Vec3(2.065999999999999, -9.0, 0.0)  # Left side start.
    assert ex_05["bar_elements"][-1]["steel_elements"][3].dxf.end == Vec3(2.049999999999999, -9, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_05["dimension_elements"][0].dxf.insert == Vec3(5.9159999999999995, -7.5, 0.0)  # Dimension text.
    assert ex_05["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(5.999999999999999, -7.5, 0.0)  # Description text.

    # Example 06.
    # General.
    assert len(ex_06["all_elements"]) == 64
    assert len(ex_06["bar_elements"]) == 60
    assert len(ex_06["dimension_elements"]) == 3

    # Steel position.
    assert ex_06["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(14.95, -9, 0)  # First bar start.
    assert ex_06["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(14.95, -6.0, 0.0)  # First bar end.

    assert ex_06["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(9.049999999999999, -9.0, 0.0)  # Last bar start.
    assert ex_06["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(9.049999999999999, -6.0, 0.0)  # Last bar end.

    # Dimension and description texts.
    assert ex_06["dimension_elements"][0].dxf.insert == Vec3(12.9, -7.5, 0.0)  # Dimension text.
    assert ex_06["bar_elements"][20]["denomination_elements"][0].dxf.insert == Vec3(13.0, -7.5, 0.0)  # Description text.

    # Example 07.
    # General.
    assert len(ex_07["all_elements"]) == 8
    assert len(ex_07["bar_elements"]) == 1
    assert len(ex_07["dimension_elements"]) == 3

    # Steel position.
    assert ex_07["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(5.949999999999999, -13.0, 0.0)  # Top side start.
    assert ex_07["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(5.949999999999999, -10.0, 0.0)  # Top side end.
    assert ex_07["bar_elements"][0]["steel_elements"][1].dxf.start == Vec3(5.965999999999999, -13.0, 0.0)  # Bottom side start.
    assert ex_07["bar_elements"][0]["steel_elements"][1].dxf.end == Vec3(5.965999999999999, -10, 0)  # Bottom side end.
    assert ex_07["bar_elements"][0]["steel_elements"][2].dxf.start == Vec3(5.965999999999999, -10.0, 0.0)  # Right side start.
    assert ex_07["bar_elements"][0]["steel_elements"][2].dxf.end == Vec3(5.949999999999999, -10, 0)  # Right side end.
    assert ex_07["bar_elements"][0]["steel_elements"][3].dxf.start == Vec3(5.965999999999999, -13, 0)  # Left side start.
    assert ex_07["bar_elements"][0]["steel_elements"][3].dxf.end == Vec3(5.949999999999999, -13, 0)  # Left side end.

    # Dimension and description texts.
    assert ex_07["dimension_elements"][0].dxf.insert == Vec3(5.915999999999999, -11.5, 0.0)  # Dimension text.
    assert ex_07["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(6.0, -11.5, 0.0)  # Description text.

    # Example 08.
    assert len(ex_08["all_elements"]) == 5
    assert len(ex_08["bar_elements"]) == 1
    assert len(ex_08["dimension_elements"]) == 3

    # Steel position.
    assert ex_08["bar_elements"][0]["steel_elements"][0].dxf.start == Vec3(12.949999999999998, -13.0, 0.0)  # First bar start.
    assert ex_08["bar_elements"][0]["steel_elements"][0].dxf.end == Vec3(12.949999999999998, -10, 0)  # First bar end.

    # Dimension and description texts.
    assert ex_08["dimension_elements"][0].dxf.insert == Vec3(12.899999999999997, -11.5, 0.0)  # Dimension text.
    assert ex_08["bar_elements"][0]["denomination_elements"][0].dxf.insert == Vec3(12.999999999999998, -11.5, 0.0)  # Description text.


def test_draw_transverse_spaced_bars_vertical_oe(spaced_bar_vertical_oe):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_vertical_oe.draw_transverse(document=doc, x=2, y=1, dimensions=True)
    ex_02 = spaced_bar_vertical_oe.draw_transverse(document=doc, x=2, y=2, dimensions=True, other_extreme=True)
    doc.saveas(filename="./tests/spaced_bars_vertical_oe_draw_transverse.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 65
    assert len(ex_01["dimension_elements"]) == 1
    assert len(ex_01["description_elements"]) == 4
    assert len(ex_01["bar_elements"]) == 60

    # Steel elements.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(8.008, 1.1079999999999997, 0)  # First.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(2.1079999999999997, 1.108, 0)  # Last.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 65
    assert len(ex_02["dimension_elements"]) == 1
    assert len(ex_02["description_elements"]) == 4
    assert len(ex_02["bar_elements"]) == 60

    # Steel elements.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(8.058, 2.1079999999999997, 0)  # First.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(2.1579999999999995, 2.108, 0.0)  # Last.


def test_draw_transverse_rotate_spaced_bars_vertical_oe(spaced_bar_vertical_oe):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_vertical_oe.draw_transverse(document=doc, x=10, y=10, dimensions=True, rotate_angle=0)
    ex_02 = spaced_bar_vertical_oe.draw_transverse(document=doc, x=10, y=10, dimensions=True, rotate_angle=45)
    ex_03 = spaced_bar_vertical_oe.draw_transverse(document=doc, x=10, y=16, dimensions=True, rotate_angle=0, other_extreme=True)
    ex_04 = spaced_bar_vertical_oe.draw_transverse(document=doc, x=10, y=16, dimensions=True, rotate_angle=45, other_extreme=True)
    doc.saveas(filename="./tests/spaced_bars_vertical_oe_draw_transverse_rotate.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 65
    assert len(ex_01["dimension_elements"]) == 1
    assert len(ex_01["description_elements"]) == 4
    assert len(ex_01["bar_elements"]) == 60

    # Steel elements.
    assert ex_01["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(16.008000000000003, 10.107999999999997, 0)  # First.
    assert ex_01["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(10.108, 10.107999999999999, 0)  # Last.

    # Example 02.
    # General.
    assert len(ex_02["all_elements"]) == 65
    assert len(ex_02["dimension_elements"]) == 1
    assert len(ex_02["description_elements"]) == 4
    assert len(ex_02["bar_elements"]) == 60

    # Steel elements.
    assert ex_02["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(14.271930009000634, 14.283243717499614, 0.0)  # First.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(10.100000000000001, 10.111313708498985, 0.0)  # Last.

    # Example 03.
    # General.
    assert len(ex_03["all_elements"]) == 65
    assert len(ex_03["dimension_elements"]) == 1
    assert len(ex_03["description_elements"]) == 4
    assert len(ex_03["bar_elements"]) == 60

    # Steel elements.
    assert ex_03["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(16.058, 16.108, 0.0)  # First.
    assert ex_03["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(10.157999999999998, 16.108, 0.0)  # Last.

    # Example 04.
    # General.
    assert len(ex_04["all_elements"]) == 65
    assert len(ex_04["dimension_elements"]) == 1
    assert len(ex_04["description_elements"]) == 4
    assert len(ex_04["bar_elements"]) == 60

    # Steel elements.
    assert ex_04["bar_elements"][0]["steel_elements"][0].dxf.center == Vec3(14.30728534805996, 20.31859905655894, 0.0)  # First.
    assert ex_04["bar_elements"][-1]["steel_elements"][0].dxf.center == Vec3(10.135355339059327, 16.14666904755831, 0.0)  # Last.


@pytest.fixture()
def spaced_bar_anchor_horizontal() -> SpacedBars:
    return SpacedBars(
        reinforcement_length=3,
        length=4,
        diameter=0.012,
        spacing=0.2,
        x=-10,
        y=-10,
        direction=Direction.HORIZONTAL,
        orientation=Orientation.BOTTOM,
        left_anchor=0.1,
        right_anchor=0.1,
        mandrel_radius=0,
        bend_longitud=2,
        bend_angle=45,
        bend_height=0.08,
        description="A1")


def test_attributes_spaced_bar_anchor_horizontal(spaced_bar_anchor_horizontal):
    # Spaced bars attributes.
    assert spaced_bar_anchor_horizontal.reinforcement_length == 3
    assert spaced_bar_anchor_horizontal.length == 4
    assert spaced_bar_anchor_horizontal.diameter == 0.012
    assert spaced_bar_anchor_horizontal.spacing == 0.2
    assert spaced_bar_anchor_horizontal.x == -10
    assert spaced_bar_anchor_horizontal.y == -10
    assert spaced_bar_anchor_horizontal.radius == 0.006
    assert spaced_bar_anchor_horizontal.direction == Direction.HORIZONTAL
    assert spaced_bar_anchor_horizontal.orientation == Orientation.BOTTOM
    assert spaced_bar_anchor_horizontal.transverse_center is None
    assert spaced_bar_anchor_horizontal.quantity == 16

    # Bar attributes.
    assert len(spaced_bar_anchor_horizontal.bars) == 16

    # Bar bending attributes.
    assert spaced_bar_anchor_horizontal.bend_longitud == 2
    assert spaced_bar_anchor_horizontal.bend_angle == 45
    assert spaced_bar_anchor_horizontal.bend_height == 0.08

    # Boxing attributes.
    assert spaced_bar_anchor_horizontal._box_width == 4
    assert spaced_bar_anchor_horizontal._box_height == 3.112

    # Physics attributes.
    assert spaced_bar_anchor_horizontal.weight == 56.82010136988643


def test_draw_longitudinal_spaced_bar_anchor_horizontal(spaced_bar_anchor_horizontal):
    doc = ezdxf.new(setup=True)
    ex_01 = spaced_bar_anchor_horizontal.draw_longitudinal(document=doc, x=-10, y=-10, unifilar=False, dimensions=True)
    ex_02 = spaced_bar_anchor_horizontal.draw_longitudinal(document=doc, x=-5, y=-10, unifilar=True, dimensions=True)
    doc.saveas(filename="./tests/spaced_bar_anchor_horizontal_draw_longitudinal.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 452

    # Example 02.
    assert len(ex_02["all_elements"]) == 116


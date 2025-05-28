# -*- coding: utf-8 -*-

# Local imports.
from etacad.globals import Direction, Orientation
from etacad.spaced_bars import SpacedBars

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3
from math import pi


@pytest.fixture()
def spaced_bar_horizontal():
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
        denomination="R1")


def test_spaced_bar_horizontal_attributes(spaced_bar_horizontal):
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
    assert len(ex_01["all_elements"]) == 140

    ex_02 = spaced_bar_horizontal.draw_longitudinal(document=doc, x=9, y=1, unifilar=True, dimensions=True)
    assert len(ex_02["all_elements"]) == 38

    ex_03 = spaced_bar_horizontal.draw_longitudinal(document=doc, x=2, y=-5, unifilar=False, dimensions=True, one_bar=True)
    assert len(ex_03["all_elements"]) == 8

    ex_04 = spaced_bar_horizontal.draw_longitudinal(document=doc, x=9, y=-5, unifilar=True, dimensions=True, one_bar=True)
    assert len(ex_04["all_elements"]) == 5

    doc.saveas(filename="./tests/spaced_bars_horizontal_draw_longitudinal.dxf")


def test_draw_transverse_spaced_bars_horizontal(spaced_bar_horizontal):
    doc = ezdxf.new(setup=True)

    ex_01 = spaced_bar_horizontal.draw_transverse(document=doc, dimensions=True, x=0, y=0)
    assert len(ex_01["all_elements"]) == 35

    doc.saveas(filename="./tests/spaced_bars_horizontal_draw_transverse.dxf")


def test_extract_data_spaced_bars_horizontal(spaced_bar_horizontal):
    data = spaced_bar_horizontal.extract_data(labels=["diameter"])
    assert len(data) == 1
    assert data == [0.01]

    data = spaced_bar_horizontal.extract_data(labels=["diameter", "length", "quantity"])
    assert len(data) == 3
    assert data == [0.01, 6, 34]

    data = spaced_bar_horizontal.extract_data()
    assert data == ["R1", 6, 0.01, 125.77366188646737, 34, 0.12]


@pytest.fixture()
def spaced_bar_vertical():
    return SpacedBars(
        reinforcement_length=6,
        length=3,
        diameter=0.016,
        spacing=0.1,
        x=-10,
        y=10,
        direction=Direction.VERTICAL,
        orientation=Orientation.BOTTOM,
        left_anchor=0,
        right_anchor=0,
        mandrel_radius=0,
        bend_longitud=0,
        bend_angle=0,
        bend_height=0,
        denomination="R2")


def test_spaced_bar_vertical_attributes(spaced_bar_vertical):
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
    assert spaced_bar_vertical.transverse_center is None
    assert spaced_bar_vertical.quantity == 62

    # Bar attributes.
    assert len(spaced_bar_vertical.bars) == 62

    # Bar bending attributes.
    assert spaced_bar_vertical.bend_longitud == 0
    assert spaced_bar_vertical.bend_angle == 0
    assert spaced_bar_vertical.bend_height == 0

    # Boxing attributes.
    assert spaced_bar_vertical._box_width == 3
    assert spaced_bar_vertical._box_height == 6.1160000000000005

    # Physics attributes.
    assert spaced_bar_vertical.weight == 293.5705237444132


def test_draw_longitudinal_spaced_bars_vertical(spaced_bar_vertical):
    doc = ezdxf.new(setup=True)

    ex_01 = spaced_bar_vertical.draw_longitudinal(document=doc, x=2, y=1, unifilar=False, dimensions=True)
    assert len(ex_01["all_elements"]) == 252
    assert ex_01["bar_elements"][-1]["steel_elements"][-1].dxf.start == Vec3(2.031999999999999, 1, 0)  # Top side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][-1].dxf.end == Vec3(2.015999999999999, 1.0, 0.0)  # Top side end.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.start == Vec3(2.031999999999999, 3.9999999999999996, 0.0)  # Bottom side start.
    assert ex_01["bar_elements"][-1]["steel_elements"][2].dxf.end == Vec3(2.015999999999999, 3.9999999999999996, 0.0)  # Bottom side end.

    ex_02 = spaced_bar_vertical.draw_longitudinal(document=doc, x=9, y=1, unifilar=True, dimensions=True)
    assert len(ex_02["all_elements"]) == 66
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.start == Vec3(9.016, 1.0, 0.0)  # Steel start.
    assert ex_02["bar_elements"][-1]["steel_elements"][0].dxf.end == Vec3(9.016, 4.0, 0.0)  # Steel end.

    ex_03 = spaced_bar_vertical.draw_longitudinal(document=doc, x=2, y=-5, unifilar=False, dimensions=True, one_bar=True)
    assert len(ex_03["all_elements"]) == 8

    ex_04 = spaced_bar_vertical.draw_longitudinal(document=doc, x=9, y=-5, unifilar=True, dimensions=True, one_bar=True)
    assert len(ex_04["all_elements"]) == 5

    doc.saveas(filename="./tests/spaced_bars_vertical_draw_longitudinal.dxf")


def test_draw_transverse_spaced_bars_vertical(spaced_bar_vertical):
    doc = ezdxf.new(setup=True)

    ex_01 = spaced_bar_vertical.draw_transverse(document=doc, x=2.1, y=1, dimensions=True)
    assert len(ex_01["all_elements"]) == 63

    doc.saveas(filename="./tests/spaced_bars_vertical_draw_transverse.dxf")


@pytest.fixture()
def spaced_bar_anchor_horizontal():
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
        denomination="A1")


def test_spaced_bar_anchor_horizontal_attributes(spaced_bar_anchor_horizontal):
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
    assert spaced_bar_anchor_horizontal.quantity == 17

    # Bar attributes.
    assert len(spaced_bar_anchor_horizontal.bars) == 17

    # Bar bending attributes.
    assert spaced_bar_anchor_horizontal.bend_longitud == 2
    assert spaced_bar_anchor_horizontal.bend_angle == 45
    assert spaced_bar_anchor_horizontal.bend_height == 0.08

    # Boxing attributes.
    assert spaced_bar_anchor_horizontal._box_width == 4
    assert spaced_bar_anchor_horizontal._box_height == 3.3120000000000003

    # Physics attributes.
    assert spaced_bar_anchor_horizontal.weight == 60.37135770550433


def test_draw_longitudinal_spaced_bar_anchor_horizontal(spaced_bar_anchor_horizontal):
    doc = ezdxf.new(setup=True)

    ex_01 = spaced_bar_anchor_horizontal.draw_longitudinal(document=doc, x=-10, y=-10, unifilar=False, dimensions=True)
    assert len(ex_01["all_elements"]) == 482

    ex_02 = spaced_bar_anchor_horizontal.draw_longitudinal(document=doc, x=-5, y=-10, unifilar=True, dimensions=True)
    assert len(ex_02["all_elements"]) == 125

    doc.saveas(filename="./tests/spaced_bar_anchor_horizontal_draw_longitudinal.dxf")

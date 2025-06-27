# -*- coding: utf-8 -*-

# Local imports.
from etacad.globals import Direction, Orientation
from etacad.slab import Slab

# External imports.
import ezdxf
import pytest

from ezdxf import zoom
from ezdxf.math import Vec3
from itertools import chain


@pytest.fixture
def slab_10x5_whithout_anchor() -> Slab:
    return Slab(length_x=10,
                length_y=5,
                thickness=0.18,
                x=-5,
                y=-5,
                direction=Direction.HORIZONTAL,
                orientation=Orientation.BOTTOM,
                as_sup_x_db=0.006,
                as_sup_y_db=0.012,
                as_inf_x_db=0.016,
                as_inf_y_db=0.02,
                as_sup_x_sp=0.10,
                as_sup_y_sp=0.10,
                as_inf_x_sp=0.20,
                as_inf_y_sp=0.20,
                cover=0.025,
                nomenclature="##",
                number_init=10,
                description="SLAB 01 10x5")


def test_attributes_slab_10x5_without_anchor(slab_10x5_whithout_anchor):
    # Geometric attributes.
    assert slab_10x5_whithout_anchor.length_x == 10
    assert slab_10x5_whithout_anchor.length_y == 5
    assert slab_10x5_whithout_anchor.thickness == 0.18
    assert slab_10x5_whithout_anchor.x == -5
    assert slab_10x5_whithout_anchor.y == -5
    assert slab_10x5_whithout_anchor.direction == Direction.HORIZONTAL
    assert slab_10x5_whithout_anchor.orientation == Orientation.BOTTOM

    # Longitudinal steel attributes.
    assert slab_10x5_whithout_anchor.as_sup_x_db == [0.006]
    assert slab_10x5_whithout_anchor.as_sup_y_db == [0.012]
    assert slab_10x5_whithout_anchor.as_inf_x_db == [0.016]
    assert slab_10x5_whithout_anchor.as_inf_y_db == [0.02]

    assert slab_10x5_whithout_anchor.as_sup_x_sp == [0.1]
    assert slab_10x5_whithout_anchor.as_sup_y_sp == [0.1]
    assert slab_10x5_whithout_anchor.as_inf_x_sp == [0.2]
    assert slab_10x5_whithout_anchor.as_inf_y_sp == [0.2]

    assert slab_10x5_whithout_anchor.max_db_sup_x == 0.006
    assert slab_10x5_whithout_anchor.max_db_sup_y == 0.012
    assert slab_10x5_whithout_anchor.max_db_inf_x == 0.016
    assert slab_10x5_whithout_anchor.max_db_inf_y == 0.02

    assert slab_10x5_whithout_anchor.as_sup_x_anchor == [0]
    assert slab_10x5_whithout_anchor.as_sup_y_anchor == [0]
    assert slab_10x5_whithout_anchor.as_inf_x_anchor == [0]
    assert slab_10x5_whithout_anchor.as_sup_x_anchor == [0]

    assert slab_10x5_whithout_anchor.as_sup_x_bend_longitud == [0]
    assert slab_10x5_whithout_anchor.as_sup_y_bend_longitud == [0]

    assert slab_10x5_whithout_anchor.as_sup_x_bend_angle == [0]
    assert slab_10x5_whithout_anchor.as_sup_y_bend_angle == [0]

    assert slab_10x5_whithout_anchor.as_sup_x_bend_height == [0]
    assert slab_10x5_whithout_anchor.as_sup_y_bend_height == [0]

    assert len(slab_10x5_whithout_anchor.bars_as_sup_x) == 1
    assert len(slab_10x5_whithout_anchor.bars_as_sup_y) == 1
    assert len(slab_10x5_whithout_anchor.bars_as_inf_x) == 1
    assert len(slab_10x5_whithout_anchor.bars_as_inf_y) == 1

    assert slab_10x5_whithout_anchor.number_init_sup_x == 10
    assert slab_10x5_whithout_anchor.number_init_sup_y == 11
    assert slab_10x5_whithout_anchor.number_init_inf_x == 12
    assert slab_10x5_whithout_anchor.number_init_inf_y == 13

    assert slab_10x5_whithout_anchor.cover == 0.025

    # Concrete attributes.
    assert slab_10x5_whithout_anchor.concrete.volume == 9
    assert slab_10x5_whithout_anchor.concrete.specific_weight == 2400
    assert slab_10x5_whithout_anchor.concrete.vertices == [(0, 0), (0, 5), (10, 5), (10, 0)]

    # Boxing attributes.
    assert slab_10x5_whithout_anchor.box_width == 10
    assert slab_10x5_whithout_anchor.box_height == 5

    # Position bar attributes.
    assert slab_10x5_whithout_anchor.nomenclature == "##"
    assert slab_10x5_whithout_anchor.number_init == 14
    assert slab_10x5_whithout_anchor.description == "SLAB 01 10x5"


def test_draw_longitudinal_slab_10x5_without_anchor(slab_10x5_whithout_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_10x5_whithout_anchor.draw_longitudinal(document=doc, x=0, y=0)
    ex_02 = slab_10x5_whithout_anchor.draw_longitudinal(document=doc, x=12, y=0, one_bar=True)
    ex_03 = slab_10x5_whithout_anchor.draw_longitudinal(document=doc, x=0, y=-10, unifilar_bars=True)
    ex_04 = slab_10x5_whithout_anchor.draw_longitudinal(document=doc, x=12, y=-10, one_bar=True, unifilar_bars=True)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_10x5_without_anchor_draw_longitudinal.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 907
    assert len(ex_01["concrete_elements"]) == 3
    assert len(ex_01["spaced_bars_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 23
    assert len(ex_02["concrete_elements"]) == 3
    assert len(ex_02["spaced_bars_elements"]) == 4

    # Example 03.
    assert len(ex_03["all_elements"]) == 232
    assert len(ex_03["concrete_elements"]) == 3
    assert len(ex_03["spaced_bars_elements"]) == 4

    # Example 04.
    assert len(ex_04["all_elements"]) == 11
    assert len(ex_04["concrete_elements"]) == 3
    assert len(ex_04["spaced_bars_elements"]) == 4


def test_draw_transverse_slab_10x5_without_anchor(slab_10x5_whithout_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_10x5_whithout_anchor.draw_transverse(document=doc, x=0, y=0, axe_section="y")
    ex_02 = slab_10x5_whithout_anchor.draw_transverse(document=doc, x=0, y=-2, unifilar=True, axe_section="y")
    ex_03 = slab_10x5_whithout_anchor.draw_transverse(document=doc, x=0, y=-4, axe_section="x")
    ex_04 = slab_10x5_whithout_anchor.draw_transverse(document=doc, x=0, y=-6, unifilar=True, axe_section="x")
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_10x5_without_anchor_draw_transverse.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 172
    assert len(ex_01["concrete_elements"]) == 3
    assert len(ex_01["spaced_bars_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 166
    assert len(ex_02["concrete_elements"]) == 3
    assert len(ex_02["spaced_bars_elements"]) == 4

    # Example 03.
    assert len(ex_03["all_elements"]) == 97
    assert len(ex_03["concrete_elements"]) == 3
    assert len(ex_03["spaced_bars_elements"]) == 4

    # Example 04.
    assert len(ex_04["all_elements"]) == 91
    assert len(ex_04["concrete_elements"]) == 3
    assert len(ex_04["spaced_bars_elements"]) == 4


def test_draw_longitudinal_rebar_detailing_slab_10x5_without_anchor(slab_10x5_whithout_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_10x5_whithout_anchor.draw_longitudinal_rebar_detailing(document=doc, x=0, y=0)
    ex_02 = slab_10x5_whithout_anchor.draw_longitudinal_rebar_detailing(document=doc, x=15, y=0, unifilar=True)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_10x5_without_anchor_draw_longitudinal_rebar_detailing.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 28
    assert len(ex_01["bars_elements"]) == 4
    assert len(ex_01["text_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 16
    assert len(ex_02["bars_elements"]) == 4
    assert len(ex_02["text_elements"]) == 4


def test_draw_table_rebar_detailing_slab_10x5_without_anchor(slab_10x5_whithout_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_10x5_whithout_anchor.draw_table_rebar_detailing(document=doc, x=10, y=-15)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_10x5_without_anchor_draw_table_rebar_detailing.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 58

    # Labels.
    assert len(ex_01["labels"]["texts"]) == 7

    assert ex_01["labels"]["texts"][0].dxf.insert == Vec3(10.8, -13.65, 0.0)
    assert ex_01["labels"]["texts"][1].dxf.insert == Vec3(12.400000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][2].dxf.insert == Vec3(13.900000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][3].dxf.insert == Vec3(15.400000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][4].dxf.insert == Vec3(16.800000000000004, -13.65, 0.0)
    assert ex_01["labels"]["texts"][5].dxf.insert == Vec3(18.600000000000005, -13.65, 0.0)
    assert ex_01["labels"]["texts"][6].dxf.insert == Vec3(20.400000000000006, -13.65, 0.0)

    assert ex_01["labels"]["grid_hz_lines"][0].dxf.start == Vec3(10.0, -13.5, 0.0)
    assert ex_01["labels"]["grid_hz_lines"][0].dxf.end == Vec3(21.0, -13.5, 0.0)
    assert ex_01["labels"]["grid_hz_lines"][1].dxf.start == Vec3(10, -13.8, 0)
    assert ex_01["labels"]["grid_hz_lines"][1].dxf.end == Vec3(21, -13.8, 0)

    assert ex_01["content"]["grid_hz_lines"][0].dxf.start == Vec3(10, -15.0, 0)
    assert ex_01["content"]["grid_hz_lines"][0].dxf.end == Vec3(21, -15.0, 0)
    assert ex_01["content"]["grid_hz_lines"][1].dxf.start == Vec3(10, -14.7, 0)
    assert ex_01["content"]["grid_hz_lines"][1].dxf.end == Vec3(21, -14.7, 0)
    assert ex_01["content"]["grid_hz_lines"][2].dxf.start == Vec3(10, -14.399999999999999, 0)
    assert ex_01["content"]["grid_hz_lines"][2].dxf.end == Vec3(21, -14.399999999999999, 0)
    assert ex_01["content"]["grid_hz_lines"][3].dxf.start == Vec3(10, -13.799999999999997, 0)
    assert ex_01["content"]["grid_hz_lines"][3].dxf.end == Vec3(21, -13.799999999999997, 0)
    assert ex_01["content"]["grid_hz_lines"][4].dxf.start == Vec3(10, -14.099999999999998, 0)
    assert ex_01["content"]["grid_hz_lines"][4].dxf.end == Vec3(21, -14.099999999999998, 0)


@pytest.fixture
def slab_5x10_whitout_anchor() -> Slab:
    return Slab(length_x=5,
                length_y=10,
                thickness=0.18,
                x=5,
                y=-5,
                direction=Direction.HORIZONTAL,
                orientation=Orientation.BOTTOM,
                as_sup_x_db=0.006,
                as_sup_y_db=0.012,
                as_inf_x_db=0.016,
                as_inf_y_db=0.02,
                as_sup_x_sp=0.10,
                as_sup_y_sp=0.10,
                as_inf_x_sp=0.20,
                as_inf_y_sp=0.20,
                cover=0.025,
                nomenclature="##",
                number_init=10,
                description="SLAB 01 5x10")


def test_attributes_slab_5x10_without_anchor(slab_5x10_whitout_anchor):
    # Geometric attributes.
    assert slab_5x10_whitout_anchor.length_x == 5
    assert slab_5x10_whitout_anchor.length_y == 10
    assert slab_5x10_whitout_anchor.thickness == 0.18
    assert slab_5x10_whitout_anchor.x == 5
    assert slab_5x10_whitout_anchor.y == -5
    assert slab_5x10_whitout_anchor.direction == Direction.HORIZONTAL
    assert slab_5x10_whitout_anchor.orientation == Orientation.BOTTOM

    # Longitudinal steel attributes.
    assert slab_5x10_whitout_anchor.as_sup_x_db == [0.006]
    assert slab_5x10_whitout_anchor.as_sup_y_db == [0.012]
    assert slab_5x10_whitout_anchor.as_inf_x_db == [0.016]
    assert slab_5x10_whitout_anchor.as_inf_y_db == [0.02]

    assert slab_5x10_whitout_anchor.as_sup_x_sp == [0.1]
    assert slab_5x10_whitout_anchor.as_sup_y_sp == [0.1]
    assert slab_5x10_whitout_anchor.as_inf_x_sp == [0.2]
    assert slab_5x10_whitout_anchor.as_inf_y_sp == [0.2]

    assert slab_5x10_whitout_anchor.max_db_sup_x == 0.006
    assert slab_5x10_whitout_anchor.max_db_sup_y == 0.012
    assert slab_5x10_whitout_anchor.max_db_inf_x == 0.016
    assert slab_5x10_whitout_anchor.max_db_inf_y == 0.02

    assert slab_5x10_whitout_anchor.as_sup_x_anchor == [0]
    assert slab_5x10_whitout_anchor.as_sup_y_anchor == [0]
    assert slab_5x10_whitout_anchor.as_inf_x_anchor == [0]
    assert slab_5x10_whitout_anchor.as_sup_x_anchor == [0]

    assert slab_5x10_whitout_anchor.as_sup_x_bend_longitud == [0]
    assert slab_5x10_whitout_anchor.as_sup_y_bend_longitud == [0]

    assert slab_5x10_whitout_anchor.as_sup_x_bend_angle == [0]
    assert slab_5x10_whitout_anchor.as_sup_y_bend_angle == [0]

    assert slab_5x10_whitout_anchor.as_sup_x_bend_height == [0]
    assert slab_5x10_whitout_anchor.as_sup_y_bend_height == [0]

    assert len(slab_5x10_whitout_anchor.bars_as_sup_x) == 1
    assert len(slab_5x10_whitout_anchor.bars_as_sup_y) == 1
    assert len(slab_5x10_whitout_anchor.bars_as_inf_x) == 1
    assert len(slab_5x10_whitout_anchor.bars_as_inf_y) == 1

    assert slab_5x10_whitout_anchor.number_init_sup_x == 10
    assert slab_5x10_whitout_anchor.number_init_sup_y == 11
    assert slab_5x10_whitout_anchor.number_init_inf_x == 12
    assert slab_5x10_whitout_anchor.number_init_inf_y == 13

    assert slab_5x10_whitout_anchor.cover == 0.025

    # Concrete attributes.
    assert slab_5x10_whitout_anchor.concrete.volume == 9
    assert slab_5x10_whitout_anchor.concrete.specific_weight == 2400
    assert slab_5x10_whitout_anchor.concrete.vertices == [(0, 0), (0, 10), (5, 10), (5, 0)]

    # Boxing attributes.
    assert slab_5x10_whitout_anchor.box_width == 5
    assert slab_5x10_whitout_anchor.box_height == 10

    # Position bar attributes.
    assert slab_5x10_whitout_anchor.nomenclature == "##"
    assert slab_5x10_whitout_anchor.number_init == 14
    assert slab_5x10_whitout_anchor.description == "SLAB 01 5x10"


def test_draw_longitudinal_slab_5x10_without_anchor(slab_5x10_whitout_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_5x10_whitout_anchor.draw_longitudinal(document=doc, x=0, y=0)
    ex_02 = slab_5x10_whitout_anchor.draw_longitudinal(document=doc, x=8, y=0, one_bar=True)
    ex_03 = slab_5x10_whitout_anchor.draw_longitudinal(document=doc, x=0, y=-15, unifilar_bars=True)
    ex_04 = slab_5x10_whitout_anchor.draw_longitudinal(document=doc, x=8, y=-15, one_bar=True, unifilar_bars=True)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_5x10_without_anchor_draw_longitudinal.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 907
    assert len(ex_01["concrete_elements"]) == 3
    assert len(ex_01["spaced_bars_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 23
    assert len(ex_02["concrete_elements"]) == 3
    assert len(ex_02["spaced_bars_elements"]) == 4

    # Example 03.
    assert len(ex_03["all_elements"]) == 232
    assert len(ex_03["concrete_elements"]) == 3
    assert len(ex_03["spaced_bars_elements"]) == 4

    # Example 04.
    assert len(ex_04["all_elements"]) == 11
    assert len(ex_04["concrete_elements"]) == 3
    assert len(ex_04["spaced_bars_elements"]) == 4


def test_draw_transverse_slab_5x10_without_anchor(slab_5x10_whitout_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_5x10_whitout_anchor.draw_transverse(document=doc, x=0, y=0, axe_section="y")
    ex_02 = slab_5x10_whitout_anchor.draw_transverse(document=doc, x=0, y=-2, unifilar=True, axe_section="y")
    ex_03 = slab_5x10_whitout_anchor.draw_transverse(document=doc, x=0, y=-4, axe_section="x")
    ex_04 = slab_5x10_whitout_anchor.draw_transverse(document=doc, x=0, y=-6, unifilar=True, axe_section="x")
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_5x10_without_anchor_draw_transverse.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 97
    assert len(ex_01["concrete_elements"]) == 3
    assert len(ex_01["spaced_bars_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 91
    assert len(ex_02["concrete_elements"]) == 3
    assert len(ex_02["spaced_bars_elements"]) == 4

    # Example 03.
    assert len(ex_03["all_elements"]) == 172
    assert len(ex_03["concrete_elements"]) == 3
    assert len(ex_03["spaced_bars_elements"]) == 4

    # Example 04.
    assert len(ex_04["all_elements"]) == 166
    assert len(ex_04["concrete_elements"]) == 3
    assert len(ex_04["spaced_bars_elements"]) == 4


def test_draw_longitudinal_rebar_detailing_slab_5x10_without_anchor(slab_5x10_whitout_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_5x10_whitout_anchor.draw_longitudinal_rebar_detailing(document=doc, x=0, y=0)
    ex_02 = slab_5x10_whitout_anchor.draw_longitudinal_rebar_detailing(document=doc, x=15, y=0, unifilar=True)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_5x10_without_anchor_draw_longitudinal_rebar_detailing.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 28
    assert len(ex_01["bars_elements"]) == 4
    assert len(ex_01["text_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 16
    assert len(ex_02["bars_elements"]) == 4
    assert len(ex_02["text_elements"]) == 4


def test_draw_table_rebar_detailing_slab_5x10_without_anchor(slab_5x10_whitout_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_5x10_whitout_anchor.draw_table_rebar_detailing(document=doc, x=10, y=-15)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_5x10_without_anchor_draw_table_rebar_detailing.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 58

    # Labels.
    assert len(ex_01["labels"]["texts"]) == 7

    assert ex_01["labels"]["texts"][0].dxf.insert == Vec3(10.8, -13.65, 0.0)
    assert ex_01["labels"]["texts"][1].dxf.insert == Vec3(12.400000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][2].dxf.insert == Vec3(13.900000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][3].dxf.insert == Vec3(15.400000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][4].dxf.insert == Vec3(16.800000000000004, -13.65, 0.0)
    assert ex_01["labels"]["texts"][5].dxf.insert == Vec3(18.600000000000005, -13.65, 0.0)
    assert ex_01["labels"]["texts"][6].dxf.insert == Vec3(20.400000000000006, -13.65, 0.0)

    assert ex_01["labels"]["grid_hz_lines"][0].dxf.start == Vec3(10.0, -13.5, 0.0)
    assert ex_01["labels"]["grid_hz_lines"][0].dxf.end == Vec3(21.0, -13.5, 0.0)
    assert ex_01["labels"]["grid_hz_lines"][1].dxf.start == Vec3(10, -13.8, 0)
    assert ex_01["labels"]["grid_hz_lines"][1].dxf.end == Vec3(21, -13.8, 0)

    assert ex_01["content"]["grid_hz_lines"][0].dxf.start == Vec3(10, -15.0, 0)
    assert ex_01["content"]["grid_hz_lines"][0].dxf.end == Vec3(21, -15.0, 0)
    assert ex_01["content"]["grid_hz_lines"][1].dxf.start == Vec3(10, -14.7, 0)
    assert ex_01["content"]["grid_hz_lines"][1].dxf.end == Vec3(21, -14.7, 0)
    assert ex_01["content"]["grid_hz_lines"][2].dxf.start == Vec3(10, -14.399999999999999, 0)
    assert ex_01["content"]["grid_hz_lines"][2].dxf.end == Vec3(21, -14.399999999999999, 0)
    assert ex_01["content"]["grid_hz_lines"][3].dxf.start == Vec3(10, -13.799999999999997, 0)
    assert ex_01["content"]["grid_hz_lines"][3].dxf.end == Vec3(21, -13.799999999999997, 0)
    assert ex_01["content"]["grid_hz_lines"][4].dxf.start == Vec3(10, -14.099999999999998, 0)
    assert ex_01["content"]["grid_hz_lines"][4].dxf.end == Vec3(21, -14.099999999999998, 0)


@pytest.fixture
def slab_10x10_with_anchor() -> Slab:
    return Slab(length_x=10,
                length_y=10,
                thickness=0.20,
                x=100,
                y=100,
                direction=Direction.HORIZONTAL,
                orientation=Orientation.BOTTOM,
                as_sup_x_db=0.006,
                as_sup_y_db=0.012,
                as_inf_x_db=0.016,
                as_inf_y_db=0.02,
                as_sup_x_sp=0.10,
                as_sup_y_sp=0.10,
                as_inf_x_sp=0.20,
                as_inf_y_sp=0.20,
                as_sup_x_anchor=0.1,
                as_sup_y_anchor=0.1,
                as_inf_x_anchor=0.05,
                as_inf_y_anchor=0.05,
                cover=0.04,
                nomenclature="%",
                number_init=1,
                description="SLAB 01 10x10")


def test_attributes_slab_10x10_with_anchor(slab_10x10_with_anchor):
    # Geometric attributes.
    assert slab_10x10_with_anchor.length_x == 10
    assert slab_10x10_with_anchor.length_y == 10
    assert slab_10x10_with_anchor.thickness == 0.2
    assert slab_10x10_with_anchor.x == 100
    assert slab_10x10_with_anchor.y == 100
    assert slab_10x10_with_anchor.direction == Direction.HORIZONTAL
    assert slab_10x10_with_anchor.orientation == Orientation.BOTTOM

    # Longitudinal steel attributes.
    assert slab_10x10_with_anchor.as_sup_x_db == [0.006]
    assert slab_10x10_with_anchor.as_sup_y_db == [0.012]
    assert slab_10x10_with_anchor.as_inf_x_db == [0.016]
    assert slab_10x10_with_anchor.as_inf_y_db == [0.02]

    assert slab_10x10_with_anchor.as_sup_x_sp == [0.1]
    assert slab_10x10_with_anchor.as_sup_y_sp == [0.1]
    assert slab_10x10_with_anchor.as_inf_x_sp == [0.2]
    assert slab_10x10_with_anchor.as_inf_y_sp == [0.2]

    assert slab_10x10_with_anchor.max_db_sup_x == 0.006
    assert slab_10x10_with_anchor.max_db_sup_y == 0.012
    assert slab_10x10_with_anchor.max_db_inf_x == 0.016
    assert slab_10x10_with_anchor.max_db_inf_y == 0.02

    assert slab_10x10_with_anchor.as_sup_x_anchor == [0.1]
    assert slab_10x10_with_anchor.as_sup_y_anchor == [0.1]
    assert slab_10x10_with_anchor.as_inf_x_anchor == [0.05]
    assert slab_10x10_with_anchor.as_inf_y_anchor == [0.05]

    assert slab_10x10_with_anchor.as_sup_x_bend_longitud == [0]
    assert slab_10x10_with_anchor.as_sup_y_bend_longitud == [0]

    assert slab_10x10_with_anchor.as_sup_x_bend_angle == [0]
    assert slab_10x10_with_anchor.as_sup_y_bend_angle == [0]

    assert slab_10x10_with_anchor.as_sup_x_bend_height == [0]
    assert slab_10x10_with_anchor.as_sup_y_bend_height == [0]

    assert len(slab_10x10_with_anchor.bars_as_sup_x) == 1
    assert len(slab_10x10_with_anchor.bars_as_sup_y) == 1
    assert len(slab_10x10_with_anchor.bars_as_inf_x) == 1
    assert len(slab_10x10_with_anchor.bars_as_inf_y) == 1

    assert slab_10x10_with_anchor.number_init_sup_x == 1
    assert slab_10x10_with_anchor.number_init_sup_y == 2
    assert slab_10x10_with_anchor.number_init_inf_x == 3
    assert slab_10x10_with_anchor.number_init_inf_y == 4

    assert slab_10x10_with_anchor.cover == 0.04

    # Concrete attributes.
    assert slab_10x10_with_anchor.concrete.volume == 20
    assert slab_10x10_with_anchor.concrete.specific_weight == 2400
    assert slab_10x10_with_anchor.concrete.vertices == [(0, 0), (0, 10), (10, 10), (10, 0)]

    # Boxing attributes.
    assert slab_10x10_with_anchor.box_width == 10
    assert slab_10x10_with_anchor.box_height == 10

    # Position bar attributes.
    assert slab_10x10_with_anchor.nomenclature == "%"
    assert slab_10x10_with_anchor.number_init == 5
    assert slab_10x10_with_anchor.description == "SLAB 01 10x10"


def test_draw_longitudinal_slab_10x10_without_anchor(slab_10x10_with_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_10x10_with_anchor.draw_longitudinal(document=doc, x=0, y=0)
    ex_02 = slab_10x10_with_anchor.draw_longitudinal(document=doc, x=12, y=0, one_bar=True)
    ex_03 = slab_10x10_with_anchor.draw_longitudinal(document=doc, x=0, y=-15, unifilar_bars=True)
    ex_04 = slab_10x10_with_anchor.draw_longitudinal(document=doc, x=12, y=-15, one_bar=True, unifilar_bars=True)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_10x10_without_anchor_draw_longitudinal.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 3607
    assert len(ex_01["concrete_elements"]) == 3
    assert len(ex_01["spaced_bars_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 55
    assert len(ex_02["concrete_elements"]) == 3
    assert len(ex_02["spaced_bars_elements"]) == 4

    # Example 03.
    assert len(ex_03["all_elements"]) == 907
    assert len(ex_03["concrete_elements"]) == 3
    assert len(ex_03["spaced_bars_elements"]) == 4

    # Example 04.
    assert len(ex_04["all_elements"]) == 19
    assert len(ex_04["concrete_elements"]) == 3
    assert len(ex_04["spaced_bars_elements"]) == 4


def test_draw_transverse_slab_10x10_without_anchor(slab_10x10_with_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_10x10_with_anchor.draw_transverse(document=doc, x=0, y=0, axe_section="y")
    ex_02 = slab_10x10_with_anchor.draw_transverse(document=doc, x=0, y=-2, unifilar=True, axe_section="y")
    ex_03 = slab_10x10_with_anchor.draw_transverse(document=doc, x=0, y=-4, axe_section="x")
    ex_04 = slab_10x10_with_anchor.draw_transverse(document=doc, x=0, y=-6, unifilar=True, axe_section="x")
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_10x10_without_anchor_draw_transverse.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 188
    assert len(ex_01["concrete_elements"]) == 3
    assert len(ex_01["spaced_bars_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 170
    assert len(ex_02["concrete_elements"]) == 3
    assert len(ex_02["spaced_bars_elements"]) == 4

    # Example 03.
    assert len(ex_03["all_elements"]) == 188
    assert len(ex_03["concrete_elements"]) == 3
    assert len(ex_03["spaced_bars_elements"]) == 4

    # Example 04.
    assert len(ex_04["all_elements"]) == 170
    assert len(ex_04["concrete_elements"]) == 3
    assert len(ex_04["spaced_bars_elements"]) == 4


def test_draw_longitudinal_rebar_detailing_slab_10x10_without_anchor(slab_10x10_with_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_10x10_with_anchor.draw_longitudinal_rebar_detailing(document=doc, x=0, y=0)
    ex_02 = slab_10x10_with_anchor.draw_longitudinal_rebar_detailing(document=doc, x=15, y=0, unifilar=True)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_10x10_without_anchor_draw_longitudinal_rebar_detailing.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 68
    assert len(ex_01["bars_elements"]) == 4
    assert len(ex_01["text_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 32
    assert len(ex_02["bars_elements"]) == 4
    assert len(ex_02["text_elements"]) == 4


def test_draw_table_rebar_detailing_slab_10x10_without_anchor(slab_10x10_with_anchor):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_10x10_with_anchor.draw_table_rebar_detailing(document=doc, x=10, y=-15)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_10x10_without_anchor_draw_table_rebar_detailing.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 58

    # Labels.
    assert len(ex_01["labels"]["texts"]) == 7

    assert ex_01["labels"]["texts"][0].dxf.insert == Vec3(10.8, -13.65, 0.0)
    assert ex_01["labels"]["texts"][1].dxf.insert == Vec3(12.400000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][2].dxf.insert == Vec3(13.900000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][3].dxf.insert == Vec3(15.400000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][4].dxf.insert == Vec3(16.800000000000004, -13.65, 0.0)
    assert ex_01["labels"]["texts"][5].dxf.insert == Vec3(18.600000000000005, -13.65, 0.0)
    assert ex_01["labels"]["texts"][6].dxf.insert == Vec3(20.400000000000006, -13.65, 0.0)

    assert ex_01["labels"]["grid_hz_lines"][0].dxf.start == Vec3(10.0, -13.5, 0.0)
    assert ex_01["labels"]["grid_hz_lines"][0].dxf.end == Vec3(21.0, -13.5, 0.0)
    assert ex_01["labels"]["grid_hz_lines"][1].dxf.start == Vec3(10, -13.8, 0)
    assert ex_01["labels"]["grid_hz_lines"][1].dxf.end == Vec3(21, -13.8, 0)

    assert ex_01["content"]["grid_hz_lines"][0].dxf.start == Vec3(10, -15.0, 0)
    assert ex_01["content"]["grid_hz_lines"][0].dxf.end == Vec3(21, -15.0, 0)
    assert ex_01["content"]["grid_hz_lines"][1].dxf.start == Vec3(10, -14.7, 0)
    assert ex_01["content"]["grid_hz_lines"][1].dxf.end == Vec3(21, -14.7, 0)
    assert ex_01["content"]["grid_hz_lines"][2].dxf.start == Vec3(10, -14.399999999999999, 0)
    assert ex_01["content"]["grid_hz_lines"][2].dxf.end == Vec3(21, -14.399999999999999, 0)
    assert ex_01["content"]["grid_hz_lines"][3].dxf.start == Vec3(10, -13.799999999999997, 0)
    assert ex_01["content"]["grid_hz_lines"][3].dxf.end == Vec3(21, -13.799999999999997, 0)
    assert ex_01["content"]["grid_hz_lines"][4].dxf.start == Vec3(10, -14.099999999999998, 0)
    assert ex_01["content"]["grid_hz_lines"][4].dxf.end == Vec3(21, -14.099999999999998, 0)


@pytest.fixture
def slab_8x3_with_anchor_bend() -> Slab:
    return Slab(length_x=8,
                length_y=3,
                thickness=0.18,
                x=100,
                y=100,
                direction=Direction.HORIZONTAL,
                orientation=Orientation.BOTTOM,
                as_sup_x_db=0.006,
                as_sup_y_db=0.012,
                as_inf_x_db=0.016,
                as_inf_y_db=0.02,
                as_sup_x_sp=0.10,
                as_sup_y_sp=0.10,
                as_inf_x_sp=0.20,
                as_inf_y_sp=0.20,
                as_sup_x_anchor=0.1,
                as_sup_y_anchor=0.1,
                as_inf_x_anchor=0.05,
                as_inf_y_anchor=0.05,
                as_sup_x_bend_height=0.03,
                as_sup_y_bend_height=0.03,
                as_sup_x_bend_longitud=4,
                as_sup_y_bend_longitud=1.5,
                as_sup_x_bend_angle=45,
                as_sup_y_bend_angle=30,
                cover=0.03,
                number_init=1,
                description="SLAB 01 8x3")


def test_attributes_slab_8x3_with_anchor_bend(slab_8x3_with_anchor_bend):
    # Geometric attributes.
    assert slab_8x3_with_anchor_bend.length_x == 8
    assert slab_8x3_with_anchor_bend.length_y == 3
    assert slab_8x3_with_anchor_bend.thickness == 0.18
    assert slab_8x3_with_anchor_bend.x == 100
    assert slab_8x3_with_anchor_bend.y == 100
    assert slab_8x3_with_anchor_bend.direction == Direction.HORIZONTAL
    assert slab_8x3_with_anchor_bend.orientation == Orientation.BOTTOM

    # Longitudinal steel attributes.
    assert slab_8x3_with_anchor_bend.as_sup_x_db == [0.006]
    assert slab_8x3_with_anchor_bend.as_sup_y_db == [0.012]
    assert slab_8x3_with_anchor_bend.as_inf_x_db == [0.016]
    assert slab_8x3_with_anchor_bend.as_inf_y_db == [0.02]

    assert slab_8x3_with_anchor_bend.as_sup_x_sp == [0.1]
    assert slab_8x3_with_anchor_bend.as_sup_y_sp == [0.1]
    assert slab_8x3_with_anchor_bend.as_inf_x_sp == [0.2]
    assert slab_8x3_with_anchor_bend.as_inf_y_sp == [0.2]

    assert slab_8x3_with_anchor_bend.max_db_sup_x == 0.006
    assert slab_8x3_with_anchor_bend.max_db_sup_y == 0.012
    assert slab_8x3_with_anchor_bend.max_db_inf_x == 0.016
    assert slab_8x3_with_anchor_bend.max_db_inf_y == 0.02

    assert slab_8x3_with_anchor_bend.as_sup_x_anchor == [0.1]
    assert slab_8x3_with_anchor_bend.as_sup_y_anchor == [0.1]
    assert slab_8x3_with_anchor_bend.as_inf_x_anchor == [0.05]
    assert slab_8x3_with_anchor_bend.as_inf_y_anchor == [0.05]

    assert slab_8x3_with_anchor_bend.as_sup_x_bend_longitud == [4]
    assert slab_8x3_with_anchor_bend.as_sup_y_bend_longitud == [1.5]

    assert slab_8x3_with_anchor_bend.as_sup_x_bend_angle == [45]
    assert slab_8x3_with_anchor_bend.as_sup_y_bend_angle == [30]

    assert slab_8x3_with_anchor_bend.as_sup_x_bend_height == [0.03]
    assert slab_8x3_with_anchor_bend.as_sup_y_bend_height == [0.03]

    assert len(slab_8x3_with_anchor_bend.bars_as_sup_x) == 1
    assert len(slab_8x3_with_anchor_bend.bars_as_sup_y) == 1
    assert len(slab_8x3_with_anchor_bend.bars_as_inf_x) == 1
    assert len(slab_8x3_with_anchor_bend.bars_as_inf_y) == 1

    assert slab_8x3_with_anchor_bend.number_init_sup_x == 1
    assert slab_8x3_with_anchor_bend.number_init_sup_y == 2
    assert slab_8x3_with_anchor_bend.number_init_inf_x == 3
    assert slab_8x3_with_anchor_bend.number_init_inf_y == 4

    assert slab_8x3_with_anchor_bend.cover == 0.03

    # Concrete attributes.
    assert slab_8x3_with_anchor_bend.concrete.volume == 4.32
    assert slab_8x3_with_anchor_bend.concrete.specific_weight == 2400
    assert slab_8x3_with_anchor_bend.concrete.vertices == [(0, 0), (0, 3), (8, 3), (8, 0)]

    # Boxing attributes.
    assert slab_8x3_with_anchor_bend.box_width == 8
    assert slab_8x3_with_anchor_bend.box_height == 3

    # Position bar attributes.
    assert slab_8x3_with_anchor_bend.nomenclature == "#"
    assert slab_8x3_with_anchor_bend.number_init == 5
    assert slab_8x3_with_anchor_bend.description == "SLAB 01 8x3"


def test_draw_longitudinal_8x3_with_anchor_bend(slab_8x3_with_anchor_bend):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_8x3_with_anchor_bend.draw_longitudinal(document=doc, x=0, y=0)
    ex_02 = slab_8x3_with_anchor_bend.draw_longitudinal(document=doc, x=12, y=0, one_bar=True)
    ex_03 = slab_8x3_with_anchor_bend.draw_longitudinal(document=doc, x=0, y=-15, unifilar_bars=True)
    ex_04 = slab_8x3_with_anchor_bend.draw_longitudinal(document=doc, x=12, y=-15, one_bar=True, unifilar_bars=True)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_8x3_with_anchor_bend_draw_longitudinal.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 3747
    assert len(ex_01["concrete_elements"]) == 3
    assert len(ex_01["spaced_bars_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 87
    assert len(ex_02["concrete_elements"]) == 3
    assert len(ex_02["spaced_bars_elements"]) == 4

    # Example 03.
    assert len(ex_03["all_elements"]) == 942
    assert len(ex_03["concrete_elements"]) == 3
    assert len(ex_03["spaced_bars_elements"]) == 4

    # Example 04.
    assert len(ex_04["all_elements"]) == 27
    assert len(ex_04["concrete_elements"]) == 3
    assert len(ex_04["spaced_bars_elements"]) == 4


def test_draw_transverse_8x3_with_anchor_bend(slab_8x3_with_anchor_bend):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_8x3_with_anchor_bend.draw_transverse(document=doc, x=0, y=0, axe_section="y")
    ex_02 = slab_8x3_with_anchor_bend.draw_transverse(document=doc, x=0, y=-2, unifilar=True, axe_section="y")
    ex_03 = slab_8x3_with_anchor_bend.draw_transverse(document=doc, x=0, y=-4, axe_section="x")
    ex_04 = slab_8x3_with_anchor_bend.draw_transverse(document=doc, x=0, y=-6, unifilar=True, axe_section="x")
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_8x3_with_anchor_bend_draw_transverse.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 174
    assert len(ex_01["concrete_elements"]) == 3
    assert len(ex_01["spaced_bars_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 144
    assert len(ex_02["concrete_elements"]) == 3
    assert len(ex_02["spaced_bars_elements"]) == 4

    # Example 03.
    assert len(ex_03["all_elements"]) == 99
    assert len(ex_03["concrete_elements"]) == 3
    assert len(ex_03["spaced_bars_elements"]) == 4

    # Example 04.
    assert len(ex_04["all_elements"]) == 69
    assert len(ex_04["concrete_elements"]) == 3
    assert len(ex_04["spaced_bars_elements"]) == 4


def test_draw_longitudinal_rebar_detailing_8x3_with_anchor_bend(slab_8x3_with_anchor_bend):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_8x3_with_anchor_bend.draw_longitudinal_rebar_detailing(document=doc, x=0, y=0)
    ex_02 = slab_8x3_with_anchor_bend.draw_longitudinal_rebar_detailing(document=doc, x=15, y=0, unifilar=True)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_8x3_with_anchor_bend_draw_longitudinal_rebar_detailing.dxf")

    # Example 01.
    assert len(ex_01["all_elements"]) == 100
    assert len(ex_01["bars_elements"]) == 4
    assert len(ex_01["text_elements"]) == 4

    # Example 02.
    assert len(ex_02["all_elements"]) == 40
    assert len(ex_02["bars_elements"]) == 4
    assert len(ex_02["text_elements"]) == 4


def test_draw_table_rebar_detailing_8x3_with_anchor_bend(slab_8x3_with_anchor_bend):
    doc = ezdxf.new(setup=True)
    ex_01 = slab_8x3_with_anchor_bend.draw_table_rebar_detailing(document=doc, x=10, y=-15)
    zoom.extents(layout=doc.modelspace())
    doc.saveas(filename="./tests/slab_8x3_with_anchor_bend_draw_table_rebar_detailing.dxf")

    # Example 01.
    # General.
    assert len(ex_01["all_elements"]) == 58

    # Labels.
    assert len(ex_01["labels"]["texts"]) == 7

    assert ex_01["labels"]["texts"][0].dxf.insert == Vec3(10.8, -13.65, 0.0)
    assert ex_01["labels"]["texts"][1].dxf.insert == Vec3(12.400000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][2].dxf.insert == Vec3(13.900000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][3].dxf.insert == Vec3(15.400000000000002, -13.65, 0.0)
    assert ex_01["labels"]["texts"][4].dxf.insert == Vec3(16.800000000000004, -13.65, 0.0)
    assert ex_01["labels"]["texts"][5].dxf.insert == Vec3(18.600000000000005, -13.65, 0.0)
    assert ex_01["labels"]["texts"][6].dxf.insert == Vec3(20.400000000000006, -13.65, 0.0)

    assert ex_01["labels"]["grid_hz_lines"][0].dxf.start == Vec3(10.0, -13.5, 0.0)
    assert ex_01["labels"]["grid_hz_lines"][0].dxf.end == Vec3(21.0, -13.5, 0.0)
    assert ex_01["labels"]["grid_hz_lines"][1].dxf.start == Vec3(10, -13.8, 0)
    assert ex_01["labels"]["grid_hz_lines"][1].dxf.end == Vec3(21, -13.8, 0)

    assert ex_01["content"]["grid_hz_lines"][0].dxf.start == Vec3(10, -15.0, 0)
    assert ex_01["content"]["grid_hz_lines"][0].dxf.end == Vec3(21, -15.0, 0)
    assert ex_01["content"]["grid_hz_lines"][1].dxf.start == Vec3(10, -14.7, 0)
    assert ex_01["content"]["grid_hz_lines"][1].dxf.end == Vec3(21, -14.7, 0)
    assert ex_01["content"]["grid_hz_lines"][2].dxf.start == Vec3(10, -14.399999999999999, 0)
    assert ex_01["content"]["grid_hz_lines"][2].dxf.end == Vec3(21, -14.399999999999999, 0)
    assert ex_01["content"]["grid_hz_lines"][3].dxf.start == Vec3(10, -13.799999999999997, 0)
    assert ex_01["content"]["grid_hz_lines"][3].dxf.end == Vec3(21, -13.799999999999997, 0)
    assert ex_01["content"]["grid_hz_lines"][4].dxf.start == Vec3(10, -14.099999999999998, 0)
    assert ex_01["content"]["grid_hz_lines"][4].dxf.end == Vec3(21, -14.099999999999998, 0)

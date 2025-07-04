# -*- coding: utf-8 -*-

# Local imports.
from etacad.globals import Direction, Orientation
from etacad.beam import Beam

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3
from itertools import chain


@pytest.fixture
def beam_concrete():
    return Beam(width=0.4,
                height=0.8,
                length=12,
                x=-1,
                y=-1)


def test_attributes_beam_concrete(beam_concrete):
    # Geometric attributes.
    assert beam_concrete.width == .4
    assert beam_concrete.height == .8
    assert beam_concrete.length == 12
    assert beam_concrete.x == -1
    assert beam_concrete.y == -1

    # Concrete attributes.
    assert beam_concrete.concrete.volume == 0.4 * 0.8 * 12


def test_draw_longitudinal_beam_concrete(beam_concrete):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam_concrete.draw_longitudinal(document=doc, unifilar_bars=False)
    doc.saveas(filename="./tests/beam_concrete_longitudinal.dxf")

    # Concrete.
    assert len(entities["concrete"]["concrete_elements"]) == 4

    # Dimensions.
    assert len(entities["dimensions_elements"]) == 0


def test_draw_transverse_beam_concrete(beam_concrete):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam_concrete.draw_transverse(document=doc)
    doc.saveas(filename="./tests/beam_concrete_transverse.dxf")

    # Concrete.
    assert len(entities["concrete"]["concrete_elements"]) == 1


@pytest.fixture
def beam():
    return Beam(width=.2,
                height=.35,
                length=6,
                x=10,
                y=5,
                as_sup={.01: 3},
                as_right={.008: 2},
                as_inf={.016: 3},
                as_left={.008: 2},
                anchor_sup=.15,
                anchor_inf=.15,
                cover=.03,
                stirrups_db=.006,
                stirrups_sep=.15,
                stirrups_anchor=.1,
                columns=[[.2, .35], [.3, .35]],
                columns_pos=[0, 5.7],
                nomenclature="@",
                number_init=7)


def test_attributes_beam(beam):
    # Geometric attributes.
    assert beam.width == .2
    assert beam.height == .35
    assert beam.length == 6
    assert beam.x == 10
    assert beam.y == 5
    assert beam.direction == Direction.HORIZONTAL
    assert beam.orientation == Orientation.RIGHT

    # Steel attributes.
    assert beam.as_sup == {.01: 3}
    assert beam.as_right == {.008: 2}
    assert beam.as_inf == {.016: 3}
    assert beam.as_left == {.008: 2}
    assert beam.anchor_sup == [.15, .15, .15]
    assert beam.anchor_inf == [.15, .15, .15]
    assert beam.cover == .03

    # Stirrups attributes.
    assert beam.stirrups_db == [.006]
    assert beam.stirrups_sep == [.15]
    assert beam.stirrups_anchor == [.1]
    assert beam.stirrups_length == [5.24]
    assert beam.stirrups_x == [0.38]

    assert beam.stirrups[0].width == .16800000000000004
    assert beam.stirrups[0].x == 10.38
    assert beam.stirrups[0].y == 5.016

    # Columns attributes.
    assert beam.columns == [[0.2, 0.35], [0.3, 0.35]]
    assert beam.columns_pos == [0, 5.7]

    # Others.
    assert beam.nomenclature == "@"
    assert beam.number_init == 11


def test_draw_longitudinal_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)

    ex_01 = beam.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=False)
    # Concrete.
    assert len(ex_01["concrete"]["concrete_elements"]) == 4

    # Dimensions.
    assert len(ex_01["dimensions_elements"]) == 1

    # Stirrups.
    assert len(ex_01["stirrups"][0]["steel_elements"]) == 35

    ex_02 = beam.draw_longitudinal(document=doc, x=2, y=0, unifilar_bars=True)
    # Concrete.
    assert len(ex_02["concrete"]["concrete_elements"]) == 4

    # Dimensions.
    assert len(ex_02["dimensions_elements"]) == 1

    # Stirrups.
    assert len(ex_02["stirrups"][0]["steel_elements"]) == 35

    doc.saveas(filename="./tests/beam_longitudinal.dxf")


def test_draw_transverse_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)

    # Example 01.
    ex_01 = beam.draw_transverse(document=doc, x=2, y=3, unifilar=False)

    # Concrete shape.
    assert [*ex_01["concrete"]["concrete_elements"][0].vertices()] == [(2,  3), (2, 3.35), (2.2, 3.35), (2.2, 3), (2, 3)]

    # Bars.
    assert ex_01["bars"][0]["steel_elements"][0].dxf.center == Vec3(2.0269999999999997, 3.32, 0)  # Top bar.
    assert ex_01["bars"][1]["steel_elements"][0].dxf.center == Vec3(2.1, 3.32, 0)  # Top bar.
    assert ex_01["bars"][2]["steel_elements"][0].dxf.center == Vec3(2.173, 3.32, 0)  # Top bar.
    assert ex_01["bars"][3]["steel_elements"][0].dxf.center == Vec3(2.174, 3.1266666666666665, 0)  # Right bar.
    assert ex_01["bars"][4]["steel_elements"][0].dxf.center == Vec3(2.174, 3.2233333333333333, 0)  # Right bar.
    assert ex_01["bars"][5]["steel_elements"][0].dxf.center == Vec3(2.03, 3.03, 0)  # Bottom bar.
    assert ex_01["bars"][6]["steel_elements"][0].dxf.center == Vec3(2.1, 3.03, 0)  # Bottom bar.
    assert ex_01["bars"][7]["steel_elements"][0].dxf.center == Vec3(2.17, 3.03, 0)  # Bottom bar.
    assert ex_01["bars"][8]["steel_elements"][0].dxf.center == Vec3(2.026, 3.1266666666666665, 0)  # Left bar.
    assert ex_01["bars"][9]["steel_elements"][0].dxf.center == Vec3(2.026, 3.2233333333333333, 0)  # Left bar.

    # Stirrups.
    assert ex_01["stirrups"][0]["steel_elements"][0].dxf.start == Vec3(2.0269999999999997, 3.3249999999999997, 0)
    assert ex_01["stirrups"][0]["steel_elements"][0].dxf.end == Vec3(2.173, 3.3249999999999997, 0)
    assert ex_01["stirrups"][0]["steel_elements"][1].dxf.start == Vec3(2.03, 3.022, 0)
    assert ex_01["stirrups"][0]["steel_elements"][1].dxf.end == Vec3(2.17, 3.022, 0)

    # General.
    assert len(ex_01["concrete"]["all_elements"]) == 3
    assert len(list(chain(*[bar_dict["all_elements"] for bar_dict in ex_01["bars"]]))) == 10
    assert len(list(chain(*[stirrup_dict["all_elements"] for stirrup_dict in ex_01["stirrups"]]))) == 22
    assert len(ex_01["all_elements"]) == 35

    # Example 02.
    ex_02 = beam.draw_transverse(document=doc, x=3, y=3, unifilar=True)

    doc.saveas(filename="./tests/beam_transverse.dxf")


def test_draw_longitudinal_rebar_detailing_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam.draw_longitudinal_rebar_detailing(document=doc, x=-10, y=1, unifilar=False)
    doc.saveas(filename="./tests/beam_longitudinal_rebar_detailing.dxf")

    assert entities["text_elements"][0].dxf.align_point == Vec3(-10.56, 0.8175000000000001, 0)
    assert entities["barline_elements"][0].dxf.start == Vec3(-10.7, 0.43, 0.0)

    # General.
    assert len(entities["text_elements"]) == 4
    assert len(entities["bars"]) == 4
    assert len(entities["barline_elements"]) == 3
    assert len(entities["all_elements"]) == 53


def test_draw_transverse_rebar_detailing_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam.draw_transverse_rebar_detailing(document=doc, x=10, y=-5)
    doc.saveas(filename="./tests/beam_transverse_rebar_detailing.dxf")

    # Steel elements.
    assert entities["stirrups"][0]["steel_elements"][0].dxf.start == Vec3(10.011000000000001, -4.691, 0.0)

    # General.
    assert len(entities["stirrups"][0]["steel_elements"]) == 22
    assert len(entities["stirrups"][0]["dimensions_elements"]) == 4
    assert len(entities["all_elements"]) == 26


def test_draw_table_rebar_detailing_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam.draw_table_rebar_detailing(document=doc, x=-20, y=-5)
    doc.saveas(filename="./tests/beam_table_rebar_detailing.dxf")

    # General.
    assert len(entities["all_elements"]) == 66

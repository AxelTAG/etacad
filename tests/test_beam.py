# Local imports.
from etacad.globals import Direction, Orientation
from etacad.beam import Beam

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3


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
    entities = beam.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=False)
    doc.saveas(filename="./tests/beam_longitudinal.dxf")

    # Stirrups.

    # General.
    assert len(entities) == 51


def test_draw_transverse_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam.draw_transverse(document=doc, x=2, y=3)
    doc.saveas(filename="./tests/beam_transverse.dxf")

    # Concrete shape.
    assert [*entities[0].vertices()] == [(2,  3), (2.2, 3), (2.2, 3.35), (2, 3.35), (2, 3)]

    # Bars.
    assert entities[1].dxf.center == Vec3(2.0269999999999997, 3.32, 0)  # Top bar.
    assert entities[2].dxf.center == Vec3(2.1, 3.32, 0)  # Top bar.
    assert entities[3].dxf.center == Vec3(2.173, 3.32, 0)  # Top bar.
    assert entities[4].dxf.center == Vec3(2.174, 3.1266666666666665, 0)  # Right bar.
    assert entities[5].dxf.center == Vec3(2.174, 3.2233333333333333, 0)  # Right bar.
    assert entities[6].dxf.center == Vec3(2.03, 3.03, 0)  # Bottom bar.
    assert entities[7].dxf.center == Vec3(2.1, 3.03, 0)  # Bottom bar.
    assert entities[8].dxf.center == Vec3(2.17, 3.03, 0)  # Bottom bar.
    assert entities[9].dxf.center == Vec3(2.026, 3.1266666666666665, 0)  # Left bar.
    assert entities[10].dxf.center == Vec3(2.026, 3.2233333333333333, 0)  # Left bar.

    # Stirrups.
    assert entities[11].dxf.start == Vec3(2.0269999999999997, 3.3249999999999997, 0)
    assert entities[11].dxf.end == Vec3(2.173, 3.3249999999999997, 0)
    assert entities[12].dxf.start == Vec3(2.03, 3.022, 0)
    assert entities[12].dxf.end == Vec3(2.17, 3.022, 0)

    # General.
    assert len(entities) == 35


def test_draw_longitudinal_rebar_detailing_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam.draw_longitudinal_rebar_detailing(document=doc, x=-10, y=1, unifilar=False)
    doc.saveas(filename="./tests/beam_longitudinal_rebar_detailing.dxf")

    assert entities[0].dxf.align_point == Vec3(-10.56, 0.8175000000000001, 0)
    assert entities[1].dxf.start == Vec3(-10.0, 0.63, 0)

    # General.
    assert len(entities) == 53


def test_draw_transverse_rebar_detailing_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam.draw_transverse_rebar_detailing(document=doc, x=10, y=-5)
    doc.saveas(filename="./tests/beam_transverse_rebar_detailing.dxf")

    assert entities[0].dxf.start == Vec3(10.011000000000001, -4.691, 0.0)

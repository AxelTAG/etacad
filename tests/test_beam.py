# Local imports.
from etacad.globals import Direction, Orientation
from etacad.beam import Beam

# External imports.
import ezdxf
import pytest


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
    assert beam.number_init == 17


def test_draw_longitudinal_beam(beam):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = beam.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=False)
    doc.saveas(filename="./tests/beam.dxf")

    # Stirrups.

    # General.
    assert len(entities) == 51

# Local imports.
from etacad.globals import ColumnTypes, Direction, Orientation
from etacad.column import Column

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3


@pytest.fixture
def column():
    return Column(width=.2,
                  depth=.2,
                  height=6,
                  cover=.03,
                  x=20,
                  y=10,
                  as_sup={0.016: 2, 0.012: 2},
                  as_right={0.012: 2},
                  as_inf={0.016: 2, 0.012: 2},
                  as_left={0.012: 2},
                  stirrups_db=[.006, 0.008, .006, .006, 0.008, .006],
                  stirrups_anchor=[.1, .12, .1, .1, .12, .1],
                  stirrups_sep=[.1, .18, .1, .1, .18, .1],
                  stirrups_length=[.6, 1.3, .6, .6, 1.3, .6],
                  stirrups_x=[.1, .85, 2.3, 3.1, 3.85, 5.3],
                  beams=[[.2, .4], [.2, .3], [.2, .3]],
                  beams_pos=[.2, 3, 5.7],
                  beam_symbol=["B1", "B2", "C1"])


def test_attributes_rectangular_column(column):
    # Geometric attributes.
    assert column.width == .2
    assert column.depth == .2
    assert column.height == 6
    assert column.diameter is None
    assert column.column_type == ColumnTypes.RECTANGULAR
    assert column.x == 20
    assert column.y == 10
    assert column.cover == .03
    assert column.direction == Direction.VERTICAL
    assert column.orientation == Orientation.RIGHT

    # Longitudinal steel attributes.
    assert column.as_sup == {0.012: 2, 0.016: 2}
    assert column.as_right == {0.012: 2}
    assert column.as_inf == {0.012: 2, 0.016: 2}
    assert column.as_left == {0.012: 2}
    assert column.anchor_sup == [0, 0, 0, 0]
    assert column.anchor_right == [0, 0]
    assert column.anchor_inf == [0, 0, 0, 0]
    assert column.anchor_left == [0, 0]

    assert column.max_db_sup == 0.016
    assert column.max_db_right == 0.012
    assert column.max_db_inf == 0.016
    assert column.max_db_left == 0.012

    # Physics attributes.
    assert column.concrete_volume == .24000000000000005

    # Box attributes.
    assert column.box_width == .2
    assert column.box_height == 6


def test_draw_longitudinal_rectangular_column(column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = column.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=False)
    doc.saveas(filename="./tests/column_rectangular_longitudinal.dxf")

    # Stirrups.
    stirrup_width = (column.width - column.cover * 2 + column.max_db_inf + 0.006 * 2)
    assert stirrup_width == .16800000000000004
    assert column.stirrups[0].width == .16800000000000004

    # General.
    assert len(entities) == 86


def test_draw_longitudinal_unifilar_rectangular_column(column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = column.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=True)
    doc.saveas(filename="./tests/column_rectangular_unifilar.dxf")

    # Stirrups.
    stirrup_width = (column.width - column.cover * 2 + column.max_db_inf + 0.006 * 2)
    assert stirrup_width == .16800000000000004
    assert column.stirrups[0].width == .16800000000000004

    # General.
    assert len(entities) == 74


def test_list_to_stirrups_rectangular_column(column):
    pass


def test_draw_transverse_rectangular_column(column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = column.draw_transverse(document=doc, x=0.5, y=1, y_section=0.65)
    entities += column.draw_transverse(document=doc, x=-0.5, y=1, y_section=1.5)
    entities += column.draw_transverse(document=doc, x=-0.5, y=-1, y_section=3.65)
    entities += column.draw_transverse(document=doc, x=0.5, y=-1, y_section=4.5)
    doc.saveas(filename="./tests/column_rectangular_transverse.dxf")

    # General.
    assert len(entities) == 148


def test_draw_longitudinal_rebar_detailing_rectangular_column(column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = column.draw_longitudinal_rebar_detailing(document=doc, x=-10, y=1, unifilar=False)
    doc.saveas(filename="./tests/column_recatangular_longitudinal_rebar_detailing.dxf")

    assert entities[0].dxf.align_point == Vec3(-9.98, 7.4, 0.0)
    assert entities[1].dxf.start == Vec3(-9.784, 1.0, 0.0)

    # General.
    assert len(entities) == 43


def test_draw_transverse_rebar_detailing_recutangular_column(column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = column.draw_transverse_rebar_detailing(document=doc, x=-10, y=1, y_section=1)
    doc.saveas(filename="./tests/column_recatangular_transverse_rebar_detailing.dxf")

    assert entities[0].dxf.start == Vec3(-9.984000000000002, 1.1640000000000001, 0.0)

    # General.
    assert len(entities) == 26

# -*- coding: utf-8 -*-

# Local imports.
from etacad.globals import ColumnTypes, Direction, Orientation
from etacad.column import Column

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3


@pytest.fixture
def concrete_column():
    return Column(width=0.8,
                  depth=0.8,
                  height=6,
                  x=-1,
                  y=-1)


def test_attributes_concrete_column(concrete_column):
    # Geometric attributes.
    assert concrete_column.width == 0.8
    assert concrete_column.depth == 0.8
    assert concrete_column.height == 6
    assert concrete_column.x == -1
    assert concrete_column.y == -1

    # Concrete attributes.
    assert concrete_column.concrete.volume == 0.8 * 0.8 * 6


def test_draw_longitudinal_concrete_column(concrete_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = concrete_column.draw_longitudinal(document=doc, unifilar_bars=False)
    doc.saveas(filename="./tests/column_concrete_longitudinal.dxf")

    # Concrete.
    assert len(entities["concrete"]["concrete_elements"]) == 4

    # Dimensions.
    assert len(entities["dimensions_elements"]) == 0


def test_draw_transverse_concret_columne(concrete_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = concrete_column.draw_transverse(document=doc)
    doc.saveas(filename="./tests/column_concrete_transverse.dxf")

    # Concrete.
    assert len(entities["concrete"]["concrete_elements"]) == 1


@pytest.fixture
def square_column():
    return Column(width=0.2,
                  depth=0.2,
                  height=6,
                  cover=.03,
                  x=20,
                  y=10,
                  as_sup={0.016: 2, 0.012: 2},
                  as_right={0.012: 2},
                  as_inf={0.016: 2, 0.012: 2},
                  as_left={0.012: 2},
                  stirrups_db=[.006, 0.008, 0.006, 0.006, 0.008, 0.006],
                  stirrups_anchor=[.1, 0.12, 0.1, 0.1, 0.12, 0.1],
                  stirrups_sep=[0.1, 0.18, 0.1, 0.1, 0.18, 0.1],
                  stirrups_length=[0.6, 1.3, 0.6, 0.6, 1.3, 0.6],
                  stirrups_x=[0.1, 0.85, 2.3, 3.1, 3.85, 5.3],
                  beams=[[0.2, 0.4], [0.2, 0.3], [0.2, 0.3]],
                  beams_pos=[0.2, 3, 5.7],
                  beams_symbol=["B1", "B2", "B3"])


def test_attributes_square_column(square_column):
    # Geometric attributes.
    assert square_column.width == 0.2
    assert square_column.depth == 0.2
    assert square_column.height == 6
    assert square_column.diameter is None
    assert square_column.column_type == ColumnTypes.RECTANGULAR
    assert square_column.x == 20
    assert square_column.y == 10
    assert square_column.cover == 0.03
    assert square_column.direction == Direction.VERTICAL
    assert square_column.orientation == Orientation.RIGHT

    # Longitudinal steel attributes.
    assert square_column.as_sup == {0.012: 2, 0.016: 2}
    assert square_column.as_right == {0.012: 2}
    assert square_column.as_inf == {0.012: 2, 0.016: 2}
    assert square_column.as_left == {0.012: 2}
    assert square_column.anchor_sup == [0, 0, 0, 0]
    assert square_column.anchor_right == [0, 0]
    assert square_column.anchor_inf == [0, 0, 0, 0]
    assert square_column.anchor_left == [0, 0]

    assert square_column.max_db_sup == 0.016
    assert square_column.max_db_right == 0.012
    assert square_column.max_db_inf == 0.016
    assert square_column.max_db_left == 0.012

    # Box attributes.
    assert square_column.box_width == 0.2
    assert square_column.box_height == 6

    # Stirrup dimensions.
    stirrup_width = (square_column.width - square_column.cover * 2 + square_column.max_db_inf + 0.006 * 2)
    assert stirrup_width == 0.16800000000000004
    assert square_column.stirrups[0].width == 0.16800000000000004


def test_draw_longitudinal_square_column(square_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = square_column.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=False)
    doc.saveas(filename="./tests/column_square_longitudinal.dxf")

    # Bars.
    assert entities["bars"][0]["steel_elements"][0].dxf.start == Vec3(2.0219999999999985, 3.0299999999999994, 0.0)

    # General.
    assert len(entities["concrete"]["all_elements"]) == 6
    assert len(entities["all_elements"]) == 90


def test_draw_longitudinal_unifilar_square_column(square_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = square_column.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=True)
    doc.saveas(filename="./tests/column_square_unifilar.dxf")

    # Stirrups.
    stirrup_width = (square_column.width - square_column.cover * 2 + square_column.max_db_inf + 0.006 * 2)
    assert stirrup_width == 0.16800000000000004
    assert square_column.stirrups[0].width == 0.16800000000000004

    # General.
    assert len(entities["all_elements"]) == 78


def test_list_to_stirrups_square_column(square_column):
    pass


def test_draw_transverse_square_column(square_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities_st_1 = square_column.draw_transverse(document=doc, x=0.5, y=1, y_section=0.65)
    entities_st_2 = square_column.draw_transverse(document=doc, x=-0.5, y=1, y_section=1.5)
    entities_st_3 = square_column.draw_transverse(document=doc, x=-0.5, y=-1, y_section=3.65)
    entities_st_4 = square_column.draw_transverse(document=doc, x=0.5, y=-1, y_section=4.5)
    doc.saveas(filename="./tests/column_square_transverse.dxf")

    # General.
    assert len(entities_st_1["all_elements"]) == 37
    assert len(entities_st_2["all_elements"]) == 37
    assert len(entities_st_3["all_elements"]) == 37
    assert len(entities_st_4["all_elements"]) == 37


def test_draw_longitudinal_rebar_detailing_square_column(square_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = square_column.draw_longitudinal_rebar_detailing(document=doc, x=-10, y=1, unifilar=False)
    doc.saveas(filename="./tests/column_square_longitudinal_rebar_detailing.dxf")

    assert entities["text_elements"][0].dxf.align_point == Vec3(-9.98, 7.6, 0.0)
    assert entities["text_elements"][0].dxf.text == "As sup."
    assert entities["barline_elements"][0].dxf.start == Vec3(-9.072, 0.7, 0.0)

    # General.
    assert len(entities["text_elements"]) == 4
    assert len(entities["bars"]) == 6
    assert len(entities["barline_elements"]) == 3
    assert len(entities["all_elements"]) == 43


def test_draw_transverse_rebar_detailing_square_column(square_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = square_column.draw_transverse_rebar_detailing(document=doc, x=-10, y=1, y_section=1)
    doc.saveas(filename="./tests/column_square_transverse_rebar_detailing.dxf")

    assert entities["stirrups"][0]["steel_elements"][0].dxf.start == Vec3(-9.992, 1.0159999999999982, 0.0)

    # General.
    assert len(entities["all_elements"]) == 26


def test_draw_table_rebar_detailing_square_column(square_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = square_column.draw_table_rebar_detailing(document=doc, x=-20, y=-5)
    doc.saveas(filename="./tests/column_square_table_rebar_detailing.dxf")

    # General.
    assert len(entities["all_elements"]) == 122


@pytest.fixture
def rectangular_dw_column():
    return Column(width=0.2,
                  depth=0.3,
                  height=6,
                  cover=.03,
                  x=20,
                  y=10,
                  as_sup={0.016: 2, 0.012: 2},
                  as_right={0.012: 2},
                  as_inf={0.016: 2, 0.012: 2},
                  as_left={0.012: 2},
                  stirrups_db=[.006, 0.008, 0.006, 0.006, 0.008, 0.006],
                  stirrups_anchor=[0.1, 0.12, 0.1, 0.1, 0.12, 0.1],
                  stirrups_sep=[0.1, 0.18, 0.1, 0.1, 0.18, 0.1],
                  stirrups_length=[0.6, 1.3, 0.6, 0.6, 1.3, 0.6],
                  stirrups_x=[.1, 0.85, 2.3, 3.1, 3.85, 5.3],
                  beams=[[0.2, 0.4], [0.2, 0.3], [0.2, 0.3]],
                  beams_pos=[0.2, 3, 5.7],
                  beams_symbol=["B1", "B2", "B3"])


def test_attributes_rectangular_dw_column(rectangular_dw_column):
    # Geometric attributes.
    assert rectangular_dw_column.width == 0.2
    assert rectangular_dw_column.depth == 0.3
    assert rectangular_dw_column.height == 6
    assert rectangular_dw_column.diameter is None
    assert rectangular_dw_column.column_type == ColumnTypes.RECTANGULAR
    assert rectangular_dw_column.x == 20
    assert rectangular_dw_column.y == 10
    assert rectangular_dw_column.cover == 0.03
    assert rectangular_dw_column.direction == Direction.VERTICAL
    assert rectangular_dw_column.orientation == Orientation.RIGHT

    # Longitudinal steel attributes.
    assert rectangular_dw_column.as_sup == {0.012: 2, 0.016: 2}
    assert rectangular_dw_column.as_right == {0.012: 2}
    assert rectangular_dw_column.as_inf == {0.012: 2, 0.016: 2}
    assert rectangular_dw_column.as_left == {0.012: 2}
    assert rectangular_dw_column.anchor_sup == [0, 0, 0, 0]
    assert rectangular_dw_column.anchor_right == [0, 0]
    assert rectangular_dw_column.anchor_inf == [0, 0, 0, 0]
    assert rectangular_dw_column.anchor_left == [0, 0]

    assert rectangular_dw_column.max_db_sup == 0.016
    assert rectangular_dw_column.max_db_right == 0.012
    assert rectangular_dw_column.max_db_inf == 0.016
    assert rectangular_dw_column.max_db_left == 0.012

    # Box attributes.
    assert rectangular_dw_column.box_width == 0.2
    assert rectangular_dw_column.box_height == 6

    # Stirrup dimensions.
    assert rectangular_dw_column.stirrups[0].width == 0.268


def test_draw_longitudinal_rectangular_dw_column(rectangular_dw_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = rectangular_dw_column.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=False)
    doc.saveas(filename="./tests/column_rectangular_dw_longitudinal.dxf")

    # Bars.
    assert entities["bars"][0]["steel_elements"][0].dxf.start == Vec3(2.0219999999999985, 3.0299999999999994, 0.0)

    # General.
    assert len(entities["concrete"]["all_elements"]) == 6
    assert len(entities["all_elements"]) == 90


def test_draw_transverse_rectangular_dw_column(rectangular_dw_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities_st_1 = rectangular_dw_column.draw_transverse(document=doc, x=0.5, y=1, y_section=0.65)
    entities_st_2 = rectangular_dw_column.draw_transverse(document=doc, x=-0.5, y=1, y_section=1.5)
    entities_st_3 = rectangular_dw_column.draw_transverse(document=doc, x=-0.5, y=-1, y_section=3.65)
    entities_st_4 = rectangular_dw_column.draw_transverse(document=doc, x=0.5, y=-1, y_section=4.5)
    doc.saveas(filename="./tests/column_rectangular_dw_column_transverse.dxf")

    # General.
    assert len(entities_st_1["all_elements"]) == 37
    assert len(entities_st_2["all_elements"]) == 37
    assert len(entities_st_3["all_elements"]) == 37
    assert len(entities_st_4["all_elements"]) == 37


@pytest.fixture
def rectangular_wd_column():
    return Column(width=0.3,
                  depth=0.2,
                  height=6,
                  cover=0.03,
                  x=20,
                  y=10,
                  as_sup={0.016: 2, 0.012: 2},
                  as_right={0.012: 2},
                  as_inf={0.016: 2, 0.012: 2},
                  as_left={0.012: 2},
                  stirrups_db=[.006, 0.008, 0.006, 0.006, 0.008, 0.006],
                  stirrups_anchor=[.1, 0.12, 0.1, 0.1, 0.12, 0.1],
                  stirrups_sep=[.1, 0.18, 0.1, 0.1, 0.18, 0.1],
                  stirrups_length=[.6, 1.3, 0.6, 0.6, 1.3, 0.6],
                  stirrups_x=[.1, 0.85, 2.3, 3.1, 3.85, 5.3],
                  beams=[[.3, 0.4], [.3, 0.3], [.3, 0.3]],
                  beams_pos=[.2, 3, 5.7],
                  beams_symbol=["B1", "B2", "B3"])


def test_attributes_rectangular_wd_column(rectangular_wd_column):
    # Geometric attributes.
    assert rectangular_wd_column.width == 0.3
    assert rectangular_wd_column.depth == 0.2
    assert rectangular_wd_column.height == 6
    assert rectangular_wd_column.diameter is None
    assert rectangular_wd_column.column_type == ColumnTypes.RECTANGULAR
    assert rectangular_wd_column.x == 20
    assert rectangular_wd_column.y == 10
    assert rectangular_wd_column.cover == 0.03
    assert rectangular_wd_column.direction == Direction.VERTICAL
    assert rectangular_wd_column.orientation == Orientation.RIGHT

    # Longitudinal steel attributes.
    assert rectangular_wd_column.as_sup == {0.012: 2, 0.016: 2}
    assert rectangular_wd_column.as_right == {0.012: 2}
    assert rectangular_wd_column.as_inf == {0.012: 2, 0.016: 2}
    assert rectangular_wd_column.as_left == {0.012: 2}
    assert rectangular_wd_column.anchor_sup == [0, 0, 0, 0]
    assert rectangular_wd_column.anchor_right == [0, 0]
    assert rectangular_wd_column.anchor_inf == [0, 0, 0, 0]
    assert rectangular_wd_column.anchor_left == [0, 0]

    assert rectangular_wd_column.max_db_sup == 0.016
    assert rectangular_wd_column.max_db_right == 0.012
    assert rectangular_wd_column.max_db_inf == 0.016
    assert rectangular_wd_column.max_db_left == 0.012

    # Box attributes.
    assert rectangular_wd_column.box_width == 0.3
    assert rectangular_wd_column.box_height == 6

    # Stirrup dimensions.
    assert rectangular_wd_column.stirrups[0].width == 0.16800000000000004


def test_draw_longitudinal_rectangular_wd_column(rectangular_wd_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = rectangular_wd_column.draw_longitudinal(document=doc, x=2, y=3, unifilar_bars=False)
    doc.saveas(filename="./tests/column_rectangular_wd_longitudinal.dxf")

    # Bars.
    assert entities["bars"][0]["steel_elements"][0].dxf.start == Vec3(2.0219999999999985, 3.0299999999999994, 0.0)

    # General.
    assert len(entities["concrete"]["all_elements"]) == 6
    assert len(entities["all_elements"]) == 90


def test_draw_transverse_rectangular_wd_column(rectangular_wd_column):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities_st_1 = rectangular_wd_column.draw_transverse(document=doc, x=0.5, y=1, y_section=0.65)
    entities_st_2 = rectangular_wd_column.draw_transverse(document=doc, x=-0.5, y=1, y_section=1.5)
    entities_st_3 = rectangular_wd_column.draw_transverse(document=doc, x=-0.5, y=-1, y_section=3.65)
    entities_st_4 = rectangular_wd_column.draw_transverse(document=doc, x=0.5, y=-1, y_section=4.5)
    doc.saveas(filename="./tests/column_rectangular_wd_column_transverse.dxf")

    # General.
    assert len(entities_st_1["all_elements"]) == 37
    assert len(entities_st_2["all_elements"]) == 37
    assert len(entities_st_3["all_elements"]) == 37
    assert len(entities_st_4["all_elements"]) == 37

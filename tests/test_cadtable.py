# -*- coding: utf-8 -*-

# Local imports.
from etacad.cadtable import CADTable

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3


@pytest.fixture
def cadtable_rows_columns():
    return CADTable(rows=10,
                    columns=11,
                    labels=["c01", "c10", "c22", "c43", "c64"],
                    index=[*range(11)],
                    x=5,
                    y=6)


def test_attributes_cadtable_rows_columns(cadtable_rows_columns):
    pass


def test_draw_table_cadtable_rows_columns(cadtable_rows_columns):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    content_grid = cadtable_rows_columns.draw_grid(document=doc)
    labels_grid = cadtable_rows_columns.draw_labels(document=doc)
    doc.saveas(filename="./tests/cadtable_draw_table_rows_columns.dxf")

    # Stirrups.

    # General.
    assert len(content_grid["grid_hz_lines"]) == 11
    assert len(content_grid["grid_vt_lines"]) == 12


@pytest.fixture
def cadtable_data():
    return CADTable(data=[["1", "16", "-", "4", "None"],
                          ["2", "12", "-", "2", "None"],
                          ["4", "8", "-", "22", "None"]],
                    labels=["POSITION", "DB", "SEP", "QUANTITY", "GRAPH"])


def test_attributes_cadtable_data(cadtable_data):

    # General attributes.
    assert cadtable_data.rows == 3
    assert cadtable_data.columns == 5


def test_draw_grid_cadtable_data(cadtable_data):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    content_grid = cadtable_data.draw_grid(document=doc)
    labels_grid = cadtable_data.draw_labels(document=doc)
    doc.saveas(filename="./tests/cadtable_draw_grid_data.dxf")

    # General.
    assert len(content_grid["grid_hz_lines"]) == 4
    assert len(content_grid["grid_vt_lines"]) == 6


def test_draw_table_cadtable_data(cadtable_data):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    table = cadtable_data.draw_table(document=doc, x=1, y=1)
    doc.saveas(filename="./tests/cadtable_draw_table_data.dxf")

    # General.
    assert len(table["labels"]["texts"]) == 5
    assert len(table["content"]["texts_row0"]) == 5
    assert len(table["content"]["texts_row1"]) == 5
    assert len(table["content"]["texts_row2"]) == 5

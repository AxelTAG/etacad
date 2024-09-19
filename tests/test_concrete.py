# Local imports.
from etacad.globals import DRotation
from etacad.concrete import Concrete

# External imports.
import ezdxf
import pytest

from ezdxf.math import Vec3


@pytest.fixture
def concrete_length_hexagon():
    return Concrete(vertices=[(0.5, 1.7321), (1.5, 1.7321), (2, 0.866), (1.5, 0), (0.5, 0), (0, 0.866)],
                    length=4,
                    x=15,
                    y=5.5)


def test_concrete_length_hexagon_attributes(concrete_length_hexagon):
    # Geometric attributes.
    assert concrete_length_hexagon.dim3D == 4

    # Boxing attributes.
    assert concrete_length_hexagon.box_width == 4
    assert concrete_length_hexagon.box_height == 1.7321


def test_concrete_length_hexagon_draw_longitudinal(concrete_length_hexagon):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = concrete_length_hexagon.draw_longitudinal(document=doc,
                                                         x=1,
                                                         y=1,
                                                         dimensions=True,
                                                         dimensions_inner=True)
    doc.saveas(filename="./tests/concrete_length_hexagon_draw_longitudinal.dxf")

    assert len(entities["concrete_lines"]) == 5
    assert len(entities["dimensions"]) == 4
    assert len(entities["all_elements"]) == 9


def test_concrete_length_hexagon_draw_transverse(concrete_length_hexagon):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = concrete_length_hexagon.draw_transverse(document=doc)
    doc.saveas(filename="./tests/concrete_length_hexagon_draw_transverse.dxf")

    assert len(entities["concrete_lines"]) == 1


@pytest.fixture
def concrete_height_hexagon():
    return Concrete(vertices=[(0.5, 1.7321), (1.5, 1.7321), (2, 0.866), (1.5, 0), (0.5, 0), (0, 0.866)],
                    height=4,
                    x=15,
                    y=5.5)


def test_concrete_height_hexagon_draw_longitudinal(concrete_height_hexagon):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = concrete_height_hexagon.draw_longitudinal(document=doc, dimensions=True, dimensions_inner=True)
    doc.saveas(filename="./tests/concrete_height_hexagon_draw_longitudinal.dxf")

    assert len(entities["concrete_lines"]) == 6


@pytest.fixture
def concrete_polygon():
    return Concrete(vertices=[(0.3527471624959566, 0.11004239479793698),
                              (0.216834688014635, 0.1886555176639173),
                              (0.24067898287947642, 0.3935260785542558),
                              (0.4886596369772782, 0.484050279638899),
                              (0.5196572198552669, 0.37208613616205444),
                              (0.6436475469041678, 0.21962432308779434),
                              (0.6436475469041678, 0.16245114261401516),
                              (0.5482703719078552, 0.1410112002218138),
                              (0.476737491776384, 0.22438875460363206),
                              (0.4075890380072602, 0.22438875460363206)],
                    length=4,
                    x=15,
                    y=5.5)


def test_concrete_length_polygon_draw_longitudinal(concrete_polygon):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = concrete_polygon.draw_longitudinal(document=doc, dimensions=True, dimensions_inner=True)
    doc.saveas(filename="./tests/concrete_length_polygon_draw_longitudinal.dxf")

    assert len(entities["concrete_lines"]) == 10
    assert len(entities["dimensions"]) == 9
    assert len(entities["all_elements"]) == 19


def test_concrete_length_polygon_draw_transverse(concrete_polygon):
    doc = ezdxf.new(dxfversion="R2010", setup=True)
    entities = concrete_polygon.draw_transverse(document=doc, dimensions=True, dimensions_boxing=True, dimensions_inner=True)
    doc.saveas(filename="./tests/concrete_length_polygon_draw_transverse.dxf")

    assert len(entities["concrete_lines"]) == 1

# Local imports.
from etacad.globals import DRotation
from etacad.geometry.polygon import Polygon
from etacad.globals import DRotation

# External imports.
import pytest


@pytest.fixture
def polygon_clockwise():
    return Polygon(vertices=[(0, 0), (0, 1), (1, 1), (2, 2), (3, 2), (3, 0)])


def test_polygon_clockwise_attributes(polygon_clockwise):
    assert polygon_clockwise.perimeter == 6.414213562373095
    assert polygon_clockwise.area == 4.5
    assert polygon_clockwise.centroid == (1.5, 1.0)


def test_polygon_clockwise_get_points_direction_of_rotation(polygon_clockwise):
    assert polygon_clockwise.get_points_direction_of_rotation() == DRotation.CLOCKWISE


def test_polygon_clockwise_get_points_between_index_limits_by_dr(polygon_clockwise):
    cw_list_1_4 = polygon_clockwise.get_points_between_index_limits_by_dr(index1=1,
                                                                          index2=4,
                                                                          direction_rotation=DRotation.CLOCKWISE)

    assert cw_list_1_4 == [(0, 1), (1, 1), (2, 2), (3, 2)]

    cw_list_0_5 = polygon_clockwise.get_points_between_index_limits_by_dr(index1=0,
                                                                          index2=5,
                                                                          direction_rotation=DRotation.CLOCKWISE)

    assert cw_list_0_5 == [(0, 0), (0, 1), (1, 1), (2, 2), (3, 2), (3, 0)]

    ccw_list_1_4 = polygon_clockwise.get_points_between_index_limits_by_dr(index1=1,
                                                                           index2=4,
                                                                           direction_rotation=DRotation.COUNTERCLOCKWISE)

    assert ccw_list_1_4 == [(0, 1), (0, 0), (3, 0), (3, 2)]

    ccw_list_0_4 = polygon_clockwise.get_points_between_index_limits_by_dr(index1=0,
                                                                           index2=4,
                                                                           direction_rotation=DRotation.COUNTERCLOCKWISE)

    assert ccw_list_0_4 == [(0, 0), (3, 0), (3, 2)]


def test_polygon_clockwise_get_side_normals(polygon_clockwise):
    sides = polygon_clockwise.get_side_equations()

    assert sides[0] == (1e+16, -0.0)
    assert sides[1] == (0, 1)
    assert sides[2] == (1, 0)
    assert sides[3] == (0, 2)
    assert sides[4] == (1e+16, -3e+16)


def test_polygon_clockwise_get_side_centers(polygon_clockwise):
    centers = polygon_clockwise.get_side_centers()

    assert centers[0] == (0, 0.5)
    assert centers[1] == (0.5, 1)
    assert centers[2] == (1.5, 1.5)
    assert centers[3] == (2.5, 2)
    assert centers[4] == (3, 1)


@pytest.fixture
def polygon_counterclockwise():
    return Polygon(vertices=[(3, 0), (3, 2), (2, 2), (1, 1), (0, 1), (0, 0)])


def test_polygon_counterclockwise_attributes(polygon_counterclockwise):
    assert polygon_counterclockwise.perimeter == 6.414213562373095
    assert polygon_counterclockwise.area == 4.5
    assert polygon_counterclockwise.centroid == (1.5, 1.0)


def test_polygon_counterclockwise_get_points_direction_of_rotation(polygon_counterclockwise):
    assert polygon_counterclockwise.get_points_direction_of_rotation() == DRotation.COUNTERCLOCKWISE


def test_polygon_counterclockwise_get_points_between_index_limits_by_dr(polygon_counterclockwise):
    cw_list_1_4 = polygon_counterclockwise.get_points_between_index_limits_by_dr(index1=1,
                                                                                 index2=4,
                                                                                 direction_rotation=DRotation.CLOCKWISE)

    assert cw_list_1_4 == [(3, 2), (3, 0), (0, 0), (0, 1)]

    cw_list_0_5 = polygon_counterclockwise.get_points_between_index_limits_by_dr(index1=0,
                                                                                 index2=5,
                                                                                 direction_rotation=DRotation.CLOCKWISE)

    assert cw_list_0_5 == [(3, 0), (0, 0)]

    ccw_list_1_4 = polygon_counterclockwise.get_points_between_index_limits_by_dr(index1=1,
                                                                                  index2=4,
                                                                                  direction_rotation=DRotation.COUNTERCLOCKWISE)

    assert ccw_list_1_4 == [(3, 2), (2, 2), (1, 1), (0, 1)]

    ccw_list_0_4 = polygon_counterclockwise.get_points_between_index_limits_by_dr(index1=0,
                                                                                  index2=4,
                                                                                  direction_rotation=DRotation.COUNTERCLOCKWISE)

    assert ccw_list_0_4 == [(3, 0), (3, 2), (2, 2), (1, 1), (0, 1)]



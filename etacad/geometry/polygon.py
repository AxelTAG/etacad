# Imports.
# Local imports.
from etacad.globals import DRotation
from etacad.geometry.utils import get_linear_center, get_line_longitud, get_line_eq, segment_center

# External imports.
from attrs import define, field


@define
class Polygon:
    """
    Represents a polygon with vertices, perimeter, area, and centroid.

    :param vertices: A list of tuples representing the vertices of the polygon.
                     Each tuple contains two float values (x, y) for the coordinates.
    :type vertices: list[tuple[float, float]]

    :ivar vertices: A list of tuples representing the vertices of the polygon.
    :vartype vertices: list[tuple[float, float]]
    :ivar perimeter: The perimeter of the polygon.
    :vartype perimeter: float
    :ivar area: The area of the polygon.
    :vartype area: float
    :ivar centroid: The centroid of the polygon, represented as a tuple of two floats (x, y).
    :vartype centroid: tuple[float, float]
    """
    # Geometry.
    vertices: list[tuple[float, float]]
    perimeter: float = field(init=False, default=0.0)
    area: float = field(init=False, default=0.0)
    centroid: tuple[float, float] = field(init=False, default=(0.0, 0.0))

    def __attrs_post_init__(self):
        self.perimeter = get_line_longitud(self.vertices)
        self.area = self.get_area()
        self.centroid = get_linear_center(points=self.vertices)

    def get_area(self) -> float:
        """
        Calculates the area of the polygon using the Shoelace formula.

        :return: The area of the polygon.
        :rtype: float
        """
        area = 0.0
        n = len(self.vertices)
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            area += x1 * y2 - x2 * y1

        return abs(area) / 2.0

    def get_top_point(self) -> list:
        """
        Get the topmost points from the vertices.

        This method finds all points in the list of vertices that have the maximum Y-coordinate (top points).
        It returns the list of points sorted by the X-coordinate.

        :return: A list of points with the highest Y-coordinate, sorted by X.
        :rtype: list
        """
        max_y = max(self.vertices, key=lambda vertice: vertice[1])[1]
        top_points = [point for point in self.vertices if point[1] == max_y]
        top_points.sort(key=lambda point: point[0])

        return top_points

    def get_right_point(self) -> list:
        """
        Get the rightmost points from the vertices.

        This method finds all points in the list of vertices that have the maximum X-coordinate (right points).
        It returns the list of points sorted by the X-coordinate.

        :return: A list of points with the highest X-coordinate, sorted by X.
        :rtype: list
        """
        max_x = max(self.vertices, key=lambda vertice: vertice[0])[0]
        right_points = [point for point in self.vertices if point[0] == max_x]
        right_points.sort(key=lambda point: point[1])

        return right_points

    def get_bottom_point(self) -> list:
        """
        Get the bottommost points from the vertices.

        This method finds all points in the list of vertices that have the minimum Y-coordinate (bottom points).
        It returns the list of points sorted by the X-coordinate.

        :return: A list of points with the lowest Y-coordinate, sorted by X.
        :rtype: list
        """
        min_y = min(self.vertices, key=lambda vertice: vertice[1])[1]
        bottom_points = [point for point in self.vertices if point[1] == min_y]
        bottom_points.sort(key=lambda point: point[0])

        return bottom_points

    def get_left_point(self) -> list:
        """
        Get the leftmost points from the vertices.

        This method finds all points in the list of vertices that have the minimum X-coordinate (left points).
        It returns the list of points sorted by the X-coordinate.

        :return: A list of points with the lowest X-coordinate, sorted by X.
        :rtype: list
        """
        min_x = min(self.vertices, key=lambda vertice: vertice[0])[0]
        left_points = [point for point in self.vertices if point[0] == min_x]
        left_points.sort(key=lambda point: point[1])

        return left_points

    def get_points_direction_of_rotation(self) -> DRotation:
        """
        Determine the direction of rotation based on the top point of the vertices.

        This method checks the relative positions of the neighboring points of the topmost point
        in the list of vertices. Based on their relative X-coordinate, it determines whether the
        direction of rotation is clockwise or counterclockwise.

        :return: Direction of rotation (clockwise or counterclockwise).
        :rtype: DRotation
        """
        top_point = self.get_top_point()[-1]
        top_index = self.vertices.index(top_point)

        if top_index - 1 > 0:
            if self.vertices[(top_index - 1)][0] <= top_point[0]:
                return DRotation.CLOCKWISE
            else:
                return DRotation.COUNTERCLOCKWISE
        else:
            if self.vertices[(top_index + 1)][0] >= top_point[0]:
                return DRotation.CLOCKWISE
            else:
                return DRotation.COUNTERCLOCKWISE

    def get_points_between_index_limits_by_dr(self,
                                              index1: int,
                                              index2: int,
                                              direction_rotation: DRotation = DRotation.CLOCKWISE):

        # Returning points.
        if self.get_points_direction_of_rotation() == DRotation.CLOCKWISE:
            if direction_rotation == DRotation.CLOCKWISE:
                if index1 <= index2:
                    return self.vertices[index1:index2 + 1]
                else:
                    return self.vertices[index1:] + self.vertices[:index2 + 1]
            else:
                if index1 <= index2:
                    return self.vertices[index1::-1] + self.vertices[-1:index2 - 1:-1]
                else:
                    return self.vertices[index2:index1:-1]
        else:
            if direction_rotation == DRotation.CLOCKWISE:
                if index1 <= index2:
                    return self.vertices[index1::-1] + self.vertices[:index2 - 1:-1]
                else:
                    return self.vertices[-index2:-index1 - 1:-1]
            else:
                if index1 <= index2:
                    return self.vertices[index1:index2 + 1]
                else:
                    return self.vertices[index1:] + self.vertices[:index2 + 1]

    def get_side_equations(self, index1: int = None, index2: int = None):
        if index1 is None:
            index1 = 0

        if index2 is None:
            index2 = len(self.vertices)

        sides = []
        for point1 in self.vertices[index1:index2]:
            if self.vertices.index(point1) == len(self.vertices) - 1:
                point2 = self.vertices[0]
            else:
                point2 = self.vertices[self.vertices.index(point1) + 1]

            x1, y1 = point1
            x2, y2 = point2
            a, b = get_line_eq(x1=x1, y1=y1, x2=x2, y2=y2)
            sides.append((a, b))

        return sides

    def get_side_centers(self, index1: int = None, index2: int = None):
        if index1 is None:
            index1 = 0

        if index2 is None:
            index2 = len(self.vertices)

        segment_centers = []
        for point1 in self.vertices[index1:index2]:
            if self.vertices.index(point1) == len(self.vertices) - 1:
                point2 = self.vertices[0]
            else:
                point2 = self.vertices[self.vertices.index(point1) + 1]

            x1, y1 = point1
            x2, y2 = point2

            segment_centers.append(segment_center([x1, y1, x2, y2]))

        return segment_centers

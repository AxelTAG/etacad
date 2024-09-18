# Imports.
# Locals imports.

# Externals imports.
import math


def displace_perpendicular(x0, y0, a, d):
    """
    Calculates coordinates at perpendicular distance from slope, x and y coordinates given.

    :param x0: X coordinate.
    :type x0: float
    :param y0: Y coordinate.
    :type y0: float
    :param a: Slope of line.
    :type a: float
    :param d: Perpendicular distance.
    :type d: float
    :return: Coordiantes at perpendicular distance.
    :rtype: tuple
    """
    # Perpendicular unit vector.
    if a == 0:
        unit_vector = (0, 1)
    else:
        unit_vector = (1 / math.sqrt((1 / a) ** 2 + 1), (-1 / a) / math.sqrt((1 / a) ** 2 + 1))

    # New point displaced by D in perpendicular direction.
    x1 = x0 + d * unit_vector[0]
    y1 = y0 + d * unit_vector[1]

    return x1, y1


def get_euclidean_distance(point1: tuple | list, point2: tuple | list):
    """
    Calculate the Euclidean distance between two Cartesian coordinates.

    :param point1: Tuple or list containing the x and y coordinates of first point.
    :type point1: tuple | list
    :param point2: Tuple or list containing the x and y coordinates of first point.
    :type point2: tuple | list
    :return: Distance between the two points.
    :rtype: float
    """
    x1, y1 = point1
    x2, y2 = point2

    distance_between_points = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance_between_points


def get_angle(point1: tuple | list, point2: tuple | list, degrees: bool = True, axis: str = "x") -> float:
    """
    Calculates de angle of to points, sorted by axis given (default X).

    :param point1: First point (x, y).
    :type point1: tuple | list
    :param point2: Second point (x, y).
    :type point2: tuple | list
    :param degrees: Transforms de angle from radians to degrees if it True.
    :type degrees: bool
    :param axis: String that specifies the axis by which the points are ordered.
    :type axis: str
    :return: angle in radians (default).
    :rtype: float
    """
    if axis == "x":
        point1, point2 = sort_points(point1, point2, axis="x")
    if axis == "y":
        point1, point2 = sort_points(point1, point2, axis="y")

    x1, y1, x2, y2 = point1[0], point1[1], point2[0], point2[1]

    if degrees:
        return math.atan2(y2 - y1, x2 - x1) * 180 / math.pi

    if not degrees:
        return math.atan2(y2 - y1, x2 - x1)


def get_angle_x_axis(point: tuple, p0: tuple = (0, 0), degrees: bool = True) -> float:
    """
    Calculates the angle of the given point from the X axis, the origin can be specified.

    :param point: Tuple of floats (x, y) representing the point to calculate angle from X axis.
    :type point: tuple
    :param p0: Point (x, y) that represents the origin.
    :type p0: tuple
    :param degrees: Transforms de angle from radians to degrees if it True.
    :type degrees: bool
    :return: Angle from X axis in degrees.
    :rtype: float
    """
    # Calculate the slope of the line.
    if point[0] != p0[0]:  # Avoid division by zero.
        slope = (point[1] - p0[1]) / (point[0] - p0[0])
    else:
        slope = math.inf

    # Calculate the angle with respect to the X-axis.
    if degrees:
        angle = math.atan(slope) * 180 / math.pi  # Convert radians to degrees.
    else:
        angle = math.atan(slope)

    # Adjust the angle if necessary.
    if slope < 0:
        if point[1] > p0[1]:
            angle += 180 if degrees else math.pi
        if point[1] < p0[1]:
            angle += 360 if degrees else math.pi * 2
    elif slope > 0:
        if point[1] < p0[1]:
            angle += 180 if degrees else math.pi
        elif point[1] == p0[1] and point[0] < p0[0]:
            angle += 180 if degrees else math.pi
    elif slope == 0:
        if point[0] < 0:
            angle += 180 if degrees else math.pi

    return angle


def get_line_longitud(line_points: list | tuple) -> float:
    """
    Calculate the total distance for a list of Cartesian coordinates.

    :param line_points: List of tuples where each tuple contains the x and y coordinates of a point.
    :type line_points: list | tuple.
    :return: Total distance between the points in the list.
    :rtype: float
    """

    length = 0.0
    for i in range(len(line_points) - 1):
        length += get_euclidean_distance(line_points[i], line_points[i + 1])

    return length


def get_linear_center(points: list) -> tuple:
    """
    Calculates the lienar center of a polygon given a list of points.

    :param points: List of tuples representing the polygon vertices [(x1, y1), (x2, y2), ..., (xn, yn)]
    :return: A tuple (xm, ym) representing the linear center coordinates
    """
    xm = sum([point[0] for point in points]) / len(points)
    ym = sum([point[1] for point in points]) / len(points)

    return xm, ym


def get_parallel_intercept(slope: float, intercep: float, distance: float) -> float:
    """
    Calculates the intercept of the parallel line of the given line (slope, intercep) at the distance given.

    :param slope: Slope of the line from which to obtain the parallel line intercep.
    :type slope: float
    :param intercep: Intercep of the line from which to obtain the parallel line intercep.
    :type intercep: float
    :param distance: Distance at which to obtain the parallel line intercep.
    :type distance: float
    :return: Parallalel line intercep at distance given.
    :rtype: float
    """
    return intercep + distance * math.sqrt(1 + slope ** 2)


def get_paralel_intersec_from_list_of_points(points: list[tuple], pn: tuple, d: float) -> list:
    """
    Calculates the intersections of the parallels lines formed by the points towards the given node point, in
    counterclockwise order.

    :param points: List of tuples of floats representing the points of the lines.
    :type points: list
    :param pn: Point representing the node (x, y).
    :type pn: tuple
    :param d: Perpendicular distance of the parallels lines to the points given.
    :type d: float
    :return: Intersections of the paralles lines in clockwise order.
    :rtype: list
    """
    xn, yn = pn
    slopes_intercepts = []
    parallel_slopes_intercepts = []

    def points_sort_function(point: tuple) -> float:
        return get_angle_x_axis(point=(point[0], point[1]), p0=(xn, yn))

    points_sorted = sorted(points, key=points_sort_function)  # Sorting the points in order of angle from X axis.

    for x, y in points_sorted:
        slope, intercep = get_line_eq(xn, yn, x, y, aprox_inf=True)
        slopes_intercepts.append((slope, intercep))

        if slope >= 0:
            if x >= xn and y >= yn:
                parallel_slopes_intercepts.append((slope, get_parallel_intercept(slope, intercep, -d)))
                parallel_slopes_intercepts.append((slope, get_parallel_intercept(slope, intercep, d)))
            else:
                parallel_slopes_intercepts.append((slope, get_parallel_intercept(slope, intercep, d)))
                parallel_slopes_intercepts.append((slope, get_parallel_intercept(slope, intercep, -d)))
        if slope < 0:
            if x <= xn:
                parallel_slopes_intercepts.append((slope, get_parallel_intercept(slope, intercep, d)))
                parallel_slopes_intercepts.append((slope, get_parallel_intercept(slope, intercep, -d)))
            else:
                parallel_slopes_intercepts.append((slope, get_parallel_intercept(slope, intercep, -d)))
                parallel_slopes_intercepts.append((slope, get_parallel_intercept(slope, intercep, d)))

    intersections = []
    num_lines = len(parallel_slopes_intercepts)

    if num_lines == 2:
        return []

    for i in range(1, num_lines + 1, 2):
        if parallel_slopes_intercepts[i][0] != parallel_slopes_intercepts[(i + 1) % num_lines][0]:
            intersection = get_lines_intersec(parallel_slopes_intercepts[i][0],
                                              parallel_slopes_intercepts[i][1],
                                              parallel_slopes_intercepts[(i + 1) % num_lines][0],
                                              parallel_slopes_intercepts[(i + 1) % num_lines][1])
        else:
            intersection = get_lines_intersec_at_distance(r1=parallel_slopes_intercepts[i],
                                                          r2=parallel_slopes_intercepts[(i + 1) % num_lines],
                                                          d=d,
                                                          x1=pn[0])
        intersections.append(intersection)

    return intersections


# Returns the a and b constants of the line equation from two poins.
def get_line_eq(x1, y1, x2, y2, aprox_inf: bool = True):
    """
    Calculates slope and intercep of the line formed by the two points given.

    :param x1: X coordinate of the first point.
    :type x1: float
    :param y1: Y coordinate of the first point.
    :type y1: float
    :param x2: X coordinate of the second point.
    :type x2: float
    :param y2: Y coordinate of the second point.
    :type y2: float
    :param aprox_inf: Boolean that specified if the vertical lines are aproximated by 9999999999999999 slope or not.
    :type aprox_inf: bool
    :return: tuple of float representing slope and intercep of line.
    :rtype: tuple
    """
    if x1 == x2:  # For vertical lines.
        a = float(9999999999999999) if aprox_inf else float("inf")  # Representation of inf. slope for a vertical line.
        b = - a * x1

    else:  # For not vertical lines.
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

    return a, b


def get_normal_line_eq(a: float, b: float, aprox_inf: bool = True) -> tuple:
    """
    Calculates slope and intercep of the normal line of the slope and intercep given.

    :param a: Slope of line.
    :type a: float
    :param b: Intercep of line.
    :type b: float
    :param aprox_inf: Boolean that specified if the vertical lines are aproximated by 9999999999999999 slope or not.
    :type aprox_inf: bool
    :return: tuple of float representing slope and intercep of normal line.
    :rtype: tuple
    """
    # If the slope is 0, the normal will be vertical.
    if a == 0:
        a_normal = float(9999999999999999) if aprox_inf else float("inf")  # Representation of inf. slope.
    else:
        # Calculate the slope of the normal (negative reciprocal).
        a_normal = -1 / a

    # The y-intercept of the normal remains the same as that of the line.
    b_normal = b

    return a_normal, b_normal


def get_lines_intersec(a1: float, b1: float, a2: float, b2: float) -> tuple[float, float]:
    """
    Calculates the intersection of the two lines given.

    :param a1: Slope of the first line.
    :type a1: float
    :param b1: Intercep of the first line.
    :type b1: float
    :param a2: Slope of the second line.
    :type a2: float
    :param b2: Intercep of the second line.
    :type b2: float
    :return: Intersection of the two lines given.
    :rtype: tuple
    """
    # Returns the intersection of two lines.
    x = (b2 - b1) / (a1 - a2)
    return x, x * a1 + b1


def get_lines_intersec_at_distance(r1: tuple, r2: tuple, d: float, x1: float) -> tuple:
    """
    Calculates the interction of the parallel lines of first and second line given at distance at X value given.

    :param r1: Slope and intercep of first line.
    :type r1: tuple
    :param r2: Slope and intercep of second line.
    :type r2: tuple
    :param d: Normal distance at the first and second line given.
    :type d: float
    :param x1:
    :type x1: float
    :return: Intersection (xi, yi) of the parallel lines at normal distance d.
    :rtype: tuple
    """
    m1, b1 = r1
    m2, b2 = r2

    # Verify that R1 and R2 are parallel by comparing their slopes
    if m1 != m2:
        raise ValueError("Lines R1 and R2 are not parallel.")

    # Find y1 using the equation of R1.
    y1 = m1 * x1 + b1

    # Calculate the angle of the lines with respect to the x-axis.
    angle = math.atan(m1)

    # Calculate the horizontal and vertical components of the distance D.
    dx = d * math.cos(angle)
    dy = d * math.sin(angle)

    # Calculate the coordinates of p2.
    x2 = x1 + dx
    y2 = y1 + dy

    return x2, y2


def get_reverse_axes(points: list) -> tuple:
    """
    Reverse the axes of the point given [x1, y1, x2, y2...] to [y1, x1, y2, x2...].

    :param points: list of x, y coordinates.
    :type points: list
    :return: X and Y coordinates reversed.
    :rtype: list
    """
    # Inverts the X and Y coordinates from a list of points, [x1, y1, x2, y2] -> [y1, x1, y2, x2]
    reversed_points = []
    for i in range(int(len(points) / 2)):
        reversed_points = reversed_points + [points[i * 2 + 1], points[i * 2]]

    return tuple(reversed_points)


def is_in_range(x: float, x1: float, x2: float) -> bool:
    """
    Verifies if X coordinate is in range of X1 and X2 limits.
    :param x: X coordinate to verify range.
    :param x1: First X coordinate limit.
    :param x2: Second X coordinat limit.
    :return: State of range X coordinate given.
    :rtype: bool
    """
    # Returns 1 if the given X is in the range X1, X2.
    extension = sorted([x1, x2])
    return extension[0] <= x <= extension[1]


def parallel_points(p1: tuple, p2: tuple, d: float, sort: bool = True) -> tuple:
    """
    Finds the parallels points at the distance given in the both sides of the line formed by the two points given.

    :param p1: First point of the line.
    :type p1: tuple
    :param p2: Second point of the line.
    :type p2: tuple
    :param d: Distance at where the parralels line pass.
    :type d: float
    :param sort: Sort the points by X coordinate if is it True.
    :type sort: bool
    :return: Tuple of four points (tuples (x, y)) of the parralels lines.
    :rtype: tuple
    """
    # Sort points.
    if sort:
        p1, p2 = sort_points(p1, p2, axis="x")

    # Calculate the slope of the original line.
    m, _ = get_line_eq(p1[0], p1[1], p2[0], p2[1])

    # Calculate the horizontal and vertical displacement.
    delta_y = d / ((1 + m ** 2) ** 0.5)
    delta_x = -m * delta_y

    # Calculate the displaced points.
    displaced_point1 = (p1[0] + delta_x, p1[1] + delta_y)
    displaced_point2 = (p2[0] + delta_x, p2[1] + delta_y)
    displaced_point3 = (p1[0] - delta_x, p1[1] - delta_y)
    displaced_point4 = (p2[0] - delta_x, p2[1] - delta_y)

    return displaced_point1, displaced_point2, displaced_point3, displaced_point4


def polygon_area(points: list[tuple[float, float]]) -> float:
    """
    Calculate the area of a polygon using the shoelace formula.

    The function takes a list of points representing the vertices of a polygon
    in 2D space and returns the area of the polygon. The vertices should be
    provided in a sequential order, either clockwise or counterclockwise.

    :param points: A list of tuples, where each tuple contains two floats
                   representing the (x, y) coordinates of a vertex.
                   Example: [(x1, y1), (x2, y2), ..., (xn, yn)].
    :type points: list[tuple[float, float]]

    :return: The area of the polygon.
    :rtype: float

    :raises ValueError: If less than 3 points are provided.

    Example:

    >>> points = [(0, 0), (4, 0), (4, 3), (0, 3)]
    >>> area = polygon_area(points)
    >>> print(area)  # Output: 12.0

    The formula used is known as the shoelace theorem or Gauss's area formula.
    """
    n = len(points)
    area = 0

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]  # Next vertex, wrapping around to the first at the end.
        area += x1 * y2 - y1 * x2
    return abs(area) / 2


def scale_coordinates(*args, scale_factor: float):
    """
    Scales the args given by the scale factor given.

    :param args: List of floats to scale.
    :type args: float
    :param scale_factor: Number to multiplicate the args given.
    :type scale_factor: float
    :return: List of args scaled.
    :rtype: list
    """
    scaled_coordinates = [(x * scale_factor, y * scale_factor) for x, y in args]

    return scaled_coordinates


# Function that returns center of a line segment.
def segment_center(points: list) -> tuple:
    """
    Calculates the mid-point coordinates of segment.

    :param points: List of two points of the segment of line.
    :type points: list
    :return: Coordinates of mid-point of segment.
    :rtype: tuple
    """
    return (points[0] + points[2]) / 2, (points[1] + points[3]) / 2


def sort_points(*args, axis: str = "x") -> list:
    """
    Sort points by axis given (x or y).

    :param args: List of points (x, y).
    :type args: list
    :param axis:
    :type axis: str
    :return:
    """
    # Extracting individual points from args.
    points = [arg for arg in args]

    # Function to sort points by x-coordinate.
    def sort_by_x(point):
        return point[0]

    # Function to sort points by y-coordinate.
    def sort_by_y(point):
        return point[1]

    # Sorting the points based on the specified axis
    if axis == "x":
        sorted_points = sorted(points, key=sort_by_x)
    elif axis == "y":
        sorted_points = sorted(points, key=sort_by_y)
    else:
        raise ValueError("Invalid axis. Axis must be 'x' or 'y'.")

    return sorted_points

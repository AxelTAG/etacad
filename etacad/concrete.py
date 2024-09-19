# Imports.
# Locals imports.
from etacad.drawing_utils import line, polyline, translate, dim_linear
from etacad.globals import CONCRETE_WEIGHT, DRotation, CONCRETE_SET_LONG, CONCRETE_SET_TRANSVERSE, ElementTypes
from etacad.geometry.polygon import Polygon
from etacad.geometry.utils import displace_perpendicular, get_angle

# External imports.
from attrs import define, field
from ezdxf.document import Drawing


@define
class Concrete:
    """
    A class used to represent a concrete section with various geometric and physical attributes.

    :param vertices: List of tuples representing the vertices of the concrete polygon.
    :type vertices: list[tuple[float, float]]
    :param height: Height of the concrete section. Defaults to None.
    :type height: float, optional
    :param length: Length of the concrete section. Defaults to None.
    :type length: float, optional
    :param x: X-coordinate for the concrete section's placement. Defaults to 0.0.
    :type x: float, optional
    :param y: Y-coordinate for the concrete section's placement. Defaults to 0.0.
    :type y: float, optional
    :param specific_weight: Specific weight of the concrete. Defaults to CONCRETE_WEIGHT.
    :type specific_weight: float, optional
    :param element_type: Type of the structural element (e.g., CONCRETE).
    :type element_type: ElementTypes, optional

    :ivar dim3D: The third dimension (either height or length) of the concrete section.
    :vartype dim3D: float
    :ivar volume: Volume of the concrete section.
    :vartype volume: float
    :ivar weight: Weight of the concrete section.
    :vartype weight: float
    :ivar box_width: Width of the bounding box in the longitudinal direction.
    :vartype box_width: float
    :ivar box_height: Height of the bounding box in the longitudinal direction.
    :vartype box_height: float
    :ivar box_width_transverse: Width of the bounding box in the transverse direction.
    :vartype box_width_transverse: float
    :ivar box_height_transverse: Height of the bounding box in the transverse direction.
    :vartype box_height_transverse: float
    :ivar element_type: Type of the structural element (e.g., CONCRETE).
    :vartype element_type: ElementTypes, optional

    :raises TypeError: If neither height nor length is provided.

    Methods
    -------
    draw_longitudinal(document, x=None, y=None, dimensions=True, dimensions_inner=True, settings=CONCRETE_SET_LONG)
        Draws the concrete section in the longitudinal direction with optional dimensioning.

    draw_transverse(document, x=None, y=None, dimensions=True, dimensions_boxing=True, dimensions_inner=True,
     settings=CONCRETE_SET_TRANSVERSE)
        Draws the concrete section in the transverse direction with optional dimensioning.

    polygon
        Property method to return a Polygon object created from the vertices of the concrete section.
    """
    # Geometric attributes.
    vertices: list[tuple[float, float]]
    height: float = field(default=None)
    length: float = field(default=None)
    x: float = field(default=0.0)
    y: float = field(default=0.0)
    dim3D: float = field(init=False)
    # polygon: Polygon = field(init=False)

    # Physics attributes.
    volume: float = field(init=False)
    weight: float = field(init=False)
    specific_weight: float = field(default=CONCRETE_WEIGHT)

    # Boxing attributes.
    box_width: float = field(init=False)
    box_height: float = field(init=False)
    box_width_transverse: float = field(init=False)
    box_height_transverse: float = field(init=False)

    # Others.
    element_type: ElementTypes = field(default=ElementTypes.CONCRETE)

    def __attrs_post_init__(self):
        # Geometric attributes.
        if self.height is not None:
            self.dim3D = self.height
            self.box_width = self.polygon.get_right_point()[0][0] - self.polygon.get_left_point()[0][0]
            self.box_height = self.height

        elif self.length is not None:
            self.dim3D = self.length
            self.box_width = self.length
            self.box_height = self.polygon.get_top_point()[0][1] - self.polygon.get_bottom_point()[0][1]

        else:
            raise TypeError("Missing length or height argument.")

        # Physics attributes.
        self.volume = self.polygon.area * self.dim3D
        self.weight = self.volume * self.specific_weight

        self.box_width_transverse = self.polygon.get_right_point()[0][0] - self.polygon.get_left_point()[0][0]
        self.box_height_transverse = self.polygon.get_top_point()[0][1] - self.polygon.get_bottom_point()[0][1]

    @property
    def polygon(self):
        """
        Property to get a Polygon object created from the vertices of the concrete section.

        :return: A Polygon object representing the concrete section.
        :rtype: Polygon
        """
        return Polygon(vertices=self.vertices)

    def draw_longitudinal(self,
                          document: Drawing,
                          x: float = None,
                          y: float = None,
                          dimensions: bool = True,
                          dimensions_inner: bool = True,
                          settings: dict = CONCRETE_SET_LONG) -> dict:
        """
        Draws the concrete section in the longitudinal direction with optional dimensioning.

        :param document: The drawing document to which the concrete section will be added.
        :type document: Drawing
        :param x: X-coordinate for the placement of the concrete section. Defaults to None, in which case `self.x` is
         used.
        :type x: float, optional
        :param y: Y-coordinate for the placement of the concrete section. Defaults to None, in which case `self.y` is
         used.
        :type y: float, optional
        :param dimensions: Flag to indicate whether to draw dimensions. Defaults to True.
        :type dimensions: bool, optional
        :param dimensions_inner: Flag to indicate whether to draw inner dimensions. Defaults to True.
        :type dimensions_inner: bool, optional
        :param settings: Dictionary of settings for dimensioning. Defaults to `CONCRETE_SET_LONG`.
        :type settings: dict, optional

        :return: A dictionary with keys "concrete_lines", "dimensions", and "all_elements", each containing the
        corresponding drawing elements.
        :rtype: dict
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        elements = {}
        concrete_lines = []
        dim = []

        if self.length is not None:
            # Getting right points between top and bottom points of concrete section.
            top_point = self.polygon.get_top_point()[-1]
            bottom_point = self.polygon.get_bottom_point()[-1]
            top_index = self.vertices.index(top_point)
            bottom_index = self.vertices.index(bottom_point)
            rotation_direction = self.polygon.get_points_direction_of_rotation()

            if rotation_direction == DRotation.CLOCKWISE:
                if top_index < bottom_index:
                    right_points = self.vertices[top_index:bottom_index + 1]
                else:
                    right_points = self.vertices[top_index:] + self.vertices[:bottom_index + 1]
            else:
                if bottom_index < top_index:
                    right_points = self.vertices[bottom_index:top_index + 1]
                else:
                    right_points = self.vertices[:top_index + 1] + self.vertices[bottom_index:]

            # Drawing concrete section.
            for point in right_points:
                concrete_lines += line(doc=document,
                                       p1=(x, y + point[1]),
                                       p2=(x + self.length, y + point[1]))
            concrete_lines += line(doc=document,
                                   p1=(x, y + top_point[1]),
                                   p2=(x, y + bottom_point[1]))
            concrete_lines += line(doc=document,
                                   p1=(x + self.length, y + top_point[1]),
                                   p2=(x + self.length, y + bottom_point[1]))

        if self.height is not None:
            # Getting front points between right and left points of concrete section.
            left_point = self.polygon.get_left_point()[-1]
            right_point = self.polygon.get_right_point()[-1]
            left_index = self.vertices.index(left_point)
            right_index = self.vertices.index(right_point)
            rotation_direction = self.polygon.get_points_direction_of_rotation()

            if rotation_direction == DRotation.CLOCKWISE:
                if right_index < left_index:
                    front_points = self.vertices[right_index:left_index + 1]
                else:
                    front_points = self.vertices[right_index:] + self.vertices[:left_index + 1]
            else:
                if left_index < right_index:
                    front_points = self.vertices[left_index:right_index + 1]
                else:
                    front_points = self.vertices[left_index:] + self.vertices[:right_index]

            # Drawing concrete section.
            for point in front_points:
                concrete_lines += line(doc=document,
                                       p1=(x + point[0], y),
                                       p2=(x + point[0], y + self.height))
            concrete_lines += line(doc=document,
                                   p1=(x + left_point[0], y),
                                   p2=(x + right_point[0], y))
            concrete_lines += line(doc=document,
                                   p1=(x + left_point[0], y + self.height),
                                   p2=(x + right_point[0], y + self.height))

        # Drawing of dimensions.
        if dimensions:
            dim = []
            if self.length:
                # Boxing dimensions.
                dim += dim_linear(document=document,
                                  p_base=(x + self.box_width / 2,
                                          y + self.box_height + settings["text_dim_distance_horizontal"]),
                                  p1=(x, y + self.box_height),
                                  p2=(x + self.box_width, y + self.box_height),
                                  dimstyle=settings["dim_style_boxing"])
                dim += dim_linear(document=document,
                                  p_base=(x - settings["text_dim_distance_vertical"] * 2,
                                          y + self.box_height / 2),
                                  p1=(x, y),
                                  p2=(x, y + self.box_height),
                                  rotation=90,
                                  dimstyle=settings["dim_style_boxing"])

                if dimensions_inner:
                    # Polygon dimensions.
                    for i in range(len(right_points) - 1):
                        dim += dim_linear(document=document,
                                          p_base=(x - settings["text_dim_distance_vertical"],
                                                  y + abs(right_points[i][1] - right_points[i + 1][1]) / 2),
                                          p1=(x, y + right_points[i][1]),
                                          p2=(x, y + right_points[i + 1][1]),
                                          rotation=90,
                                          dimstyle=settings["dim_style_inner"])

            if self.height:
                # Boxing dimensions.
                dim += dim_linear(document=document,
                                  p_base=(x + self.box_width / 2,
                                          y + self.box_height + settings["text_dim_distance_horizontal"] * 2),
                                  p1=(x, y + self.box_height),
                                  p2=(x + self.box_width, y + self.box_height),
                                  dimstyle=settings["dim_style_boxing"])
                dim += dim_linear(document=document,
                                  p_base=(x - settings["text_dim_distance_vertical"],
                                          y + self.box_height / 2),
                                  p1=(x, y),
                                  p2=(x, y + self.box_height),
                                  rotation=90,
                                  dimstyle=settings["dim_style_boxing"])

                if dimensions_inner:
                    # Polygon dimensions.
                    for i in range(len(front_points) - 1):
                        dim += dim_linear(document=document,
                                          p_base=(x + abs(front_points[i][0] - front_points[i + 1][0]) / 2,
                                                  y + self.height + settings["text_dim_distance_vertical"]),
                                          p1=(x + front_points[i][0], y + self.height),
                                          p2=(x + front_points[i + 1][0], y + self.height),
                                          dimstyle=settings["dim_style_inner"])

        # Setting elements dict.
        elements["concrete_lines"] = concrete_lines
        elements["dimensions"] = dim
        elements["all_elements"] = concrete_lines + dim

        return elements

    def draw_transverse(self,
                        document: Drawing,
                        x: float = None,
                        y: float = None,
                        dimensions: bool = True,
                        dimensions_boxing: bool = True,
                        dimensions_inner: bool = False,
                        settings: dict = CONCRETE_SET_TRANSVERSE) -> dict:
        """
        Draws the concrete section in the transverse direction with optional dimensioning.

        :param document: The drawing document to which the concrete section will be added.
        :type document: Drawing
        :param x: X-coordinate for the placement of the concrete section. Defaults to None, in which case `self.x` is used.
        :type x: float, optional
        :param y: Y-coordinate for the placement of the concrete section. Defaults to None, in which case `self.y` is used.
        :type y: float, optional
        :param dimensions: Flag to indicate whether to draw dimensions. Defaults to True.
        :type dimensions: bool, optional
        :param dimensions_boxing: Flag to indicate whether to draw boxing dimensions. Defaults to True.
        :type dimensions_boxing: bool, optional
        :param dimensions_inner: Flag to indicate whether to draw inner dimensions. Defaults to False.
        :type dimensions_inner: bool, optional
        :param settings: Dictionary of settings for dimensioning. Defaults to `CONCRETE_SET_TRANSVERSE`.
        :type settings: dict, optional

        :return: A dictionary with keys "concrete_lines" and "all_elements", each containing the corresponding drawing elements.
        :rtype: dict
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        elements = {}
        concrete_lines = []
        dim = []

        # Drawing concrete shape.
        concrete_lines += polyline(document=document, vertices=self.vertices, closed=True)

        # Moves all elements to x, y coordinates given.
        min_x = self.polygon.get_left_point()[0][0]
        min_y = self.polygon.get_bottom_point()[0][1]
        vector_translate = (x - min_x, y - min_y)
        translate(objects=concrete_lines, vector=vector_translate)

        if dimensions:
            if dimensions_boxing:
                # Boxing dimensions.
                dim += dim_linear(document=document,
                                  p_base=(x + self.box_width_transverse / 2,
                                          y + self.box_height_transverse + settings["text_dim_distance_horizontal"]),
                                  p1=(x, y + self.box_height_transverse),
                                  p2=(x + self.box_width_transverse, y + self.box_height_transverse),
                                  dimstyle=settings["dim_style_boxing"])
                dim += dim_linear(document=document,
                                  p_base=(x - settings["text_dim_distance_vertical"] * 2,
                                          y + self.box_height_transverse / 2),
                                  p1=(x, y),
                                  p2=(x, y + self.box_height_transverse),
                                  rotation=90,
                                  dimstyle=settings["dim_style_boxing"])

            # Inner dimensions.
            if dimensions_inner:
                sides_equations = self.polygon.get_side_equations()
                sides_centers = self.polygon.get_side_centers()

                for i, point1 in enumerate(self.vertices):
                    if i == len(self.vertices) - 1:
                        point2 = self.vertices[0]
                    else:
                        point2 = self.vertices[i + 1]
                    angle = get_angle(point1=point1, point2=point2)

                    point_base = displace_perpendicular(x0=sides_centers[i][0],
                                                        y0=sides_centers[i][1],
                                                        a=sides_equations[i][0],
                                                        d=-settings["text_dim_inner_perpendicular_distance"])
                    dim += dim_linear(document=document,
                                      p_base=(point_base[0] + vector_translate[0], point_base[1] + vector_translate[1]),
                                      p1=(point1[0] + vector_translate[0], point1[1] + vector_translate[1]),
                                      p2=(point2[0] + vector_translate[0], point2[1] + vector_translate[1]),
                                      rotation=angle,
                                      dimstyle=settings["dim_style_inner"])

        # Setting elements dict.
        elements["concrete_lines"] = concrete_lines
        elements["all_elements"] = concrete_lines + dim

        return elements

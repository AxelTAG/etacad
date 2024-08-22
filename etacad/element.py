# External imports.
from attrs import define, field


@define(slots=True)
class Element:
    """
    General proposes for Element objects.

    :param width: Width of the Element.
    :type width: float
    :param height: Height of the Element.
    :type height: float
    :param element_type: Type of the Element (bar, stirrup, beam, etc.).
    :type element_type: str
    :param x: X coordinate of the bottom left corner bounding box Element point.
    :type x: float
    :param y: Y coordinate of the bottom left corner bounding box Element point.

    :ivar width: Width of the Element.
    :ivar height: Height of the Element.
    :ivar element_type: Type of the Element (bar, stirrup, beam, etc.).
    :ivar x: X coordinate of the bottom left corner bounding box Element point.
    :ivar y: Y coordinate of the bottom left corner bounding box Element point.
    """

    # Geometric attributes.
    width: float
    height: float
    element_type: str
    x: float = field(default=0)
    y: float = field(default=0)

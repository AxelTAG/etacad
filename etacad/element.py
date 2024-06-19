class Element:
    """
    General proposes for Element objects.

    :param width: Width of the Element.
    :type width: float
    :param height: Height of the Element.
    :type height: float
    :param type: Type of the Element (bar, stirrup, beam, etc.).
    :type type: str
    :param x: X coordinate of the bottom left corner bounding box Element point.
    :type x: float
    :param y: Y coordinate of the bottom left corner bounding box Element point.

    :ivar width: Width of the Element.
    :ivar height: Height of the Element.
    :ivar type: Type of the Element (bar, stirrup, beam, etc.).
    :ivar x: X coordinate of the bottom left corner bounding box Element point.
    :ivar y: Y coordinate of the bottom left corner bounding box Element point.
    """

    def __init__(self, width: float, height: float, type: str, x: float, y: float):
        """
        Initialeze a new instance of Element.
        """
        self.width = width
        self.height = height
        self.type = type
        self.x = x
        self.y = y

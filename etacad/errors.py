class DrawingError(Exception):
    """
    Base class for all drawing-related errors in the module.
    """
    pass


class OneBarPositionError(DrawingError):
    """
    Raised when the top and bottom one-bar positions are set to the same value,
    which is not allowed in the drawing configuration.
    """
    def __init__(self, top_position, bottom_position):
        message = (
            f"Top and bottom bar positions cannot be the same: "
            f"{top_position} == {bottom_position}"
        )
        super().__init__(message)
        self.top_position = top_position
        self.bottom_position = bottom_position

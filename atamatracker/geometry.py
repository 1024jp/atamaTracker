"""Geometric objects
"""

class Point(object):
    """X and Y coordinate set.

    Public properties:
    x -- Horizontal coordinate
    y -- Vertical coordinate
    isAutoDetected -- [bool] Whether the point was detected automatically?
    """

    def __init__(self, x, y, isAutoDetected=False):
        self.x = x
        self.y = y
        self.isAutoDetected = isAutoDetected

    def __str__(self):
        return "Point({}, {})".format(self.x, self.y)

    def move(self, dx, dy):
        """Translate point."""
        self.x += dx
        self.y += dy

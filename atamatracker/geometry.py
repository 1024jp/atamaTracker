"""Geometric objects
"""


class Point(object):
    """X and Y coordinate set.

    Public properties:
    x -- Horizontal coordinate
    y -- Vertical coordinate
    """
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point({0.x}, {0.y})".format(self)

    def move(self, dx, dy):
        """Translate point.
        """
        self.x += dx
        self.y += dy

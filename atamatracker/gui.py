"""GUI frontend for atamaTracker
"""

import cv2

from . import graphics
from .geometry import Point


class EventListener(object):
    """Listener for mouse events

    Public properties:
    clicked_points -- [list] List of Point instances
    is_pressed -- [bool] Boolean whether the left button is pressed
    """

    is_pressed = False

    def __init__(self, window):
        self.clicked_points = []
        self.window = window
        cv2.setMouseCallback(self.window.name, self.__on_mouse_click)

    def get_xy(self):
        """Listen mouse event and return clicked coordinates.
        """
        # reset stored coordinates
        self.clicked_points = []

        cv2.waitKey(0)

        return self.clicked_points

    def __on_mouse_click(self, event, x, y, flags, param):
        """Mouse event callback.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            point = Point(x, y)
            self.is_pressed = True
            if not self.__is_clicked(point):
                self.clicked_points.append(point)
                self.window.draw_marker(point)
                self.window.display()

        elif event == cv2.EVENT_LBUTTONUP:
            self.is_pressed = False

        elif event == cv2.EVENT_MOUSEMOVE and self.is_pressed:
            pass

    def __is_clicked(self, point):
        """Check whether the given point has already been clicked.
        """
        for p in self.clicked_points:
            if p.distance(point) <= graphics.Marker.RADIUS + 2:  # +2 for buffer
                return point

        return None


class Window(object):
    """Window object.

    Public properties:
    name -- [str] Window name
    image -- [str] Current image that shown in the window
    """

    def __init__(self, name):
        self.name = name
        cv2.namedWindow(self.name)

    def close(self):
        """Close window.
        """
        cv2.destroyWindow(self.name)

    def display(self):
        """Update window contents.
        """
        cv2.imshow(self.name, self.image)

    def draw_marker(self, point, frame_size=0):
        """Draw a circle at the desired coordinate on the image.
        """
        graphics.draw_marker(self.image, point, frame_size)

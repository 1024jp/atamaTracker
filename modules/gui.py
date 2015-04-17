"""GUI frontend for atamaTracker
"""

import cv2

from .geometry import Point


class Marker:
    """Marker settings.
    """
    COLOR = (27, 190, 124)  # (B, G, R)
    RADIUS = 2


class EventListener(object):
    """Listener for mouse events

    Public properties:
    clicked_points -- list of Point instances
    is_pressed -- boolean whether the left button is pressed
    """

    is_pressed = False

    def __init__(self, window):
        self.clicked_points = []
        self.window = window
        cv2.setMouseCallback(self.window.name, self.__on_mouse_click)

    def get_xy(self):
        """Listen mouse event and return clicked coordinates.
        """
        cv2.waitKey(0)

        points = self.clicked_points

        # reset stored coordinates
        self.clicked_points = []

        return points

    def __on_mouse_click(self, event, x, y, flags, param):
        """Mouse event callback.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            point = Point(x, y)
            self.is_pressed = True
            self.clicked_points.append(point)
            self.window.draw_marker(point.x, point.y)
            self.window.display()

        elif event == cv2.EVENT_LBUTTONUP:
            self.is_pressed = False

        elif event == cv2.EVENT_MOUSEMOVE and self.is_pressed:
            pass


class Window(object):
    """Window object.

    Public properties:
    name -- [string] Window name
    image -- [string] Current image that shown in the window
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

    def draw_marker(self, x, y, frame_size=0):
        """Draw a circle at the desired coordinate on the image.
        """
        cv2.circle(self.image, (x, y), Marker.RADIUS, Marker.COLOR, 2)

        if frame_size > 0:
            point1 = (x - frame_size / 2, y - frame_size / 2)
            point2 = (x + frame_size / 2, y + frame_size / 2)
            cv2.rectangle(self.image, point1, point2, Marker.COLOR, 1)

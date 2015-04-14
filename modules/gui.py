"""GUI frontend for atamaTracker
"""

import cv2
import numpy

# constants
MARKER_COLOR = (27, 190, 124)


class EventListener(object):
    """Listener for mouse events

    Public properties:
    xx -- numpy array for horizontal positions
    yy -- numpy array for vertical positions
    isPressed -- boolean whether the left button is pressed
    """

    isPressed = False

    def __init__(self, window):
        self.xx = numpy.array([], dtype=numpy.int)
        self.yy = numpy.array([], dtype=numpy.int)
        self.window = window
        cv2.setMouseCallback(self.window.name, self.__onMouseClick)

    def get_xy(self):
        """Listen mouse event and return clicked coordinates.
        """
        cv2.waitKey(0)

        xx = self.xx
        yy = self.yy

        # reset stored coordinates
        self.xx = numpy.array([], dtype=numpy.int)
        self.yy = numpy.array([], dtype=numpy.int)

        return xx, yy

    def __onMouseClick(self, event, x, y, flags, param):
        """Mouse event callback.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.isPressed = True
            self.xx = numpy.append(self.xx, x)
            self.yy = numpy.append(self.yy, y)
            self.__draw_circle(x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            self.isPressed = False

        elif event == cv2.EVENT_MOUSEMOVE and self.isPressed:
            pass

    def __draw_circle(self, x, y, radius=2, color=MARKER_COLOR):
        """Draw a circle at the desired coordinate on the image."""
        image = self.window.image
        cv2.cv.Circle(image, (x, y), radius, color, 2)
        self.window.image = image


class Window(object):
    def __init__(self, name):
        self.name = name
        cv2.namedWindow(self.name)

    def image():
        """Accessor for image property."""
        doc = "Current image that shown in the window"

        def fget(self):
            return self.__image

        def fset(self, image):
            self.__image = image
            cv2.cv.ShowImage(self.name, image)

        return locals()

    image = property(**image())

    def close(self):
        """Close window."""
        cv2.destroyWindow(self.name)

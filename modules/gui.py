"""GUI frontend for atamaTracker
"""

import cv2
import numpy


class EventListener(object):
    """Listener for mouse events

    Public properties:
    xx -- numpy array for horizontal positions
    yy -- numpy array for vertical positions
    """

    def __init__(self, window_name):
        self.xx = numpy.array([], dtype=numpy.int)
        self.yy = numpy.array([], dtype=numpy.int)
        self.window_name = window_name

    def get_xy(self):
        """Listen mouse event and return clicked coordinates.
        """
        cv2.setMouseCallback(self.window_name, self.__onMouseClick)
        cv2.waitKey(0)

        return self.xx, self.yy

    def __onMouseClick(self, event, x, y, flags, param):
        """Mouse event callback.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.xx = numpy.append(self.xx, x)
            self.yy = numpy.append(self.yy, y)


class Window(object):
    def __init__(self, name):
        self.name = name

        cv2.cv.NamedWindow(self.name)

    def image():
        doc = "Current image that shown in the window"

        def fget(self):
            return self.__image

        def fset(self, image):
            self.__image = image
            cv2.cv.ShowImage(self.name, image)

        return locals()

    image = property(**image())

    def close(self):
        """Close window.
        """
        cv2.destroyWindow(self.name)

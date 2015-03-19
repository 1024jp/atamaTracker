"""mouseevent
"""

import cv2
import numpy


xx = numpy.array([], dtype=numpy.int)
yy = numpy.array([], dtype=numpy.int)


def get_xy(window_name):
    """Listen mouse event and return clicked coordinates.
    """
    # define event
    def onMouseClick(event, x, y, flags, param):
        """Mouse event callback.
        """
        global xx, yy
        if event == cv2.EVENT_LBUTTONDOWN:
            xx = numpy.append(xx, x)
            yy = numpy.append(yy, y)

    cv2.setMouseCallback(window_name, onMouseClick)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return xx, yy

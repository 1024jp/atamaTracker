"""Pattern detector
"""

import cv2

from . import piv


def _to_grayscale(image):
    """Convert given image to grayscale.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


class PatternDetector(object):
    """Find similar patterns in image1 from image2.

    Public properties:
    kernel_size -- [(int, int)] pattern size
    dx_range -- [(int, int)] horizontal buffer length to find
    dy_range -- [(int, int)] vertical buffer length to find

    Arguments:
    image1 -- [image] image to refer to the pattern as numpy.ndarray
    image2 -- [image] image to find the pattern as numpy.ndarray
    """

    kernel_size = (25, 25)
    dx_range = (-5, 5)
    dy_range = (-5, 5)

    def __init__(self, image1, image2):
        self._image1 = _to_grayscale(image1)
        self._image2 = _to_grayscale(image2)

    def detect(self, x, y):
        dy, dx = piv.find_point(self._image1, self._image2, y, x,
                                kernel_size=self.kernel_size,
                                di_range=self.dy_range, dj_range=self.dx_range)

        return int(dx), int(dy)

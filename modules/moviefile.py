"""Movie module for atamaTracker
"""

import cv2


class Movie(object):
    """Movie file object.
    """

    def __init__(self, file_path):
        self.__capture = cv2.VideoCapture(file_path)

    def load_image(self, time_sec):
        """Load image at the desired time.

        Retruns None if no image could load.
        """
        self.__capture.set(cv2.cv.CV_CAP_PROP_POS_MSEC, time_sec * 1000)
        f, image = self.__capture.read()

        return image

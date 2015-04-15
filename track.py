#!/usr/bin/env python
"""track.py
"""

import os.path
import sys

import cv2
import numpy

from modules import gui, piv


# constants
TIME_STEP = 0.1  # time step in second
FIND_BUFFER = 15  # buffer length to find the pattern in the next frame
PATTERN_SIZE = 25  # size of tracking pattern


def main(file_path):
    # load a movie file
    file_name = os.path.basename(file_path)
    movie = Movie(file_path)

    # open a window
    image = movie.load_image(0.0)
    window = gui.Window(file_name)
    window.image = image

    # click heads' positions on the first frame
    eventListener = gui.EventListener(window)
    clicked_points = eventListener.get_xy()

    last_index = len(clicked_points) - 1
    points = dict(zip(range(len(clicked_points)), clicked_points))

    # output
    for idx, (x, y) in points.items():
        _dump_result(0.0, idx, x, y)

    # process each frame
    time = 0.0
    while True:
        # load images
        image = movie.load_image(time)
        next_image = movie.load_image(time + TIME_STEP)
        if image is None or next_image is None:
            break

        for idx, point in points.items():
            # find similar pattern to the current frame from the next frame
            try:
                dy, dx = piv.find_point(_to_grayscale(image),
                                        _to_grayscale(next_image),
                                        point[1], point[0],
                                        kernel_size=(PATTERN_SIZE,
                                                     PATTERN_SIZE),
                                        di_range=(-FIND_BUFFER, FIND_BUFFER),
                                        dj_range=(-FIND_BUFFER, FIND_BUFFER))
            except ValueError:  # frame out
                points.pop(idx, None)
                continue

            # translate position
            point[0] += dx
            point[1] += dy

            # draw marker
            window.image = image
            window.draw_marker(point[0], point[1], PATTERN_SIZE)

        # wait for mouse event
        new_points = eventListener.get_xy()

        # append new points
        for point in new_points:
            last_index += 1
            points[last_index] = point

        # output
        for idx, (x, y) in points.items():
            _dump_result(time + TIME_STEP, idx, x, y)

        time += TIME_STEP

    window.close()


def _dump_result(time, idx, x, y):
    """Print result to the standard output.

    Arguments:
    time -- [float] time in second
    idx -- [int] index number of person
    x -- [int] x coordinate
    y -- [int] y coordinate
    """
    print("{} {} {} {}".format(time, idx, y, x))


def _to_grayscale(image):
    """Convert given image to grayscale.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


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


if __name__ == "__main__":
    main(sys.argv[1])

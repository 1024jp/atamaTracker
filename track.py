#!/usr/bin/env python
"""track.py
"""

import os.path
import sys

from modules import gui, moviefile
from modules.geometry import Point
from modules.detector import PatternDetector


# constants
TIME_STEP = 0.1  # time step in second
FIND_BUFFER = 15  # buffer length to find the pattern in the next frame
PATTERN_SIZE = 25  # size of tracking pattern


def init_detector():
    """initialize PatternDetector class.
    """
    PatternDetector.kernel_size = (PATTERN_SIZE, PATTERN_SIZE)
    PatternDetector.dx_range = (-FIND_BUFFER, FIND_BUFFER)
    PatternDetector.dy_range = (-FIND_BUFFER, FIND_BUFFER)


def main(file_path):
    time = 0.0
    last_index = -1
    points = dict()

    init_detector()

    # load a movie file
    movie = moviefile.Movie(file_path)

    # open a window
    file_name = os.path.basename(file_path)
    window = gui.Window(file_name)
    eventListener = gui.EventListener(window)

    # process each frame
    while True:
        image = movie.load_image(time)
        if image is None:
            break

        window.image = image

        # auto-track points
        if points:
            prev_image = movie.load_image(time - TIME_STEP)
            if prev_image is None:
                break
            detector = PatternDetector(prev_image, image)

            for idx, point in points.items():
                try:
                    dx, dy = detector.detect(point.x, point.y)
                except ValueError:  # frame out
                    points.pop(idx, None)
                    continue

                point.move(dx, dy)
                point.isAutoDetected = True

                window.draw_marker(point.x, point.y, PATTERN_SIZE)

        window.display()

        # wait for mouse event
        clicked_points = eventListener.get_xy()

        # append new points
        for point in clicked_points:
            last_index += 1
            points[last_index] = point

        # output
        for idx, point in points.items():
            _dump_result(time, idx, point.x, point.y)

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


if __name__ == "__main__":
    main(sys.argv[1])

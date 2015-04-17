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
    init_detector()

    # load a movie file
    file_name = os.path.basename(file_path)
    movie = moviefile.Movie(file_path)

    # open a window
    image = movie.load_image(0.0)
    window = gui.Window(file_name)
    window.image = image
    window.display()

    # click heads' positions on the first frame
    eventListener = gui.EventListener(window)
    clicked_points = eventListener.get_xy()

    last_index = len(clicked_points) - 1
    points = dict(zip(range(len(clicked_points)), clicked_points))

    # output
    for idx, point in points.items():
        _dump_result(0.0, idx, point.x, point.y)

    # process each frame
    time = 0.0
    while True:
        # load images
        image = movie.load_image(time)
        next_image = movie.load_image(time + TIME_STEP)
        if image is None or next_image is None:
            break

        window.image = image
        detector = PatternDetector(image, next_image)

        for idx, point in points.items():
            # find similar pattern to the current frame from the next frame
            try:
                dx, dy = detector.detect(point.x, point.y)
            except ValueError:  # frame out
                points.pop(idx, None)
                continue

            # translate position
            point.move(dx, dy)

            # raise flag
            point.isAutoDetected = True

            # draw marker
            window.draw_marker(point.x, point.y, PATTERN_SIZE)

        window.display()

        # wait for mouse event
        new_points = eventListener.get_xy()

        # append new points
        for point in new_points:
            last_index += 1
            points[last_index] = point

        # output
        for idx, point in points.items():
            _dump_result(time + TIME_STEP, idx, point.x, point.y)

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

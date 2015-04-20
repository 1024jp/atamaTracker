#!/usr/bin/env python
"""track.py
"""

import os.path
import sys

from atamatracker.config import manager as config_manager
from atamatracker import gui, moviefile
from atamatracker.detector import PatternDetector


def setup(config):
    """initialize PatternDetector class.
    """
    PatternDetector.kernel_size = (config.pattern_size, config.pattern_size)
    PatternDetector.dx_range = (-config.find_buffer, config.find_buffer)
    PatternDetector.dy_range = (-config.find_buffer, config.find_buffer)


def main(file_path):
    # setup with config file
    config_manager.load_config(file_path)
    config = config_manager.config
    setup(config)

    time = 0.0
    last_index = -1
    points = dict()

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
            prev_image = movie.load_image(time - config.time_step)
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

                window.draw_marker(point.x, point.y, config.pattern_size)

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

        time += config.time_step

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

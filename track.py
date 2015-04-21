#!/usr/bin/env python
"""track.py
"""

import os.path
import sys

from atamatracker.config import manager as config_manager
from atamatracker import gui, moviefile
from atamatracker.data import History, Track
from atamatracker.detector import PatternDetector


def setup(config):
    """initialize PatternDetector class.
    """
    PatternDetector.pattern_size = (config.pattern_size, config.pattern_size)
    PatternDetector.dx_range = (-config.find_buffer, config.find_buffer)
    PatternDetector.dy_range = (-config.find_buffer, config.find_buffer)


def main(file_path):
    # setup with config file
    config_manager.load_config(file_path)
    config = config_manager.config
    setup(config)

    # init variables
    time = 0.0
    last_time = None
    last_index = -1
    history = History()

    # load movie file
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
        if last_time is not None:
            prev_image = movie.load_image(last_time)
            if prev_image is None:
                break
            detector = PatternDetector(prev_image, image)

            for last_track in history.tracks(time=last_time):
                point = detector.detect(last_track.point)
                if point:
                    history.append(Track(point, last_track.label, time))
                    window.draw_marker(point, config.pattern_size)

        window.display()

        # wait for mouse event
        try:
            clicked_points = eventListener.get_xy()
        except gui.UserCancelException:  # cancel with esc key
            break

        # append new tracks
        for point in clicked_points:
            last_index += 1
            history.append(Track(point, last_index, time, is_manual=True))

        last_time = time
        time += config.time_step

    window.close()

    return history


if __name__ == "__main__":
    result = main(sys.argv[1])

    if len(sys.argv) > 2:
        result.dump(sys.argv[2])

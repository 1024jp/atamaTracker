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
MARKER_COLOR = (27, 190, 124)  # marker color (BGR)


def main(file_path):
    # load a movie file
    file_name = os.path.basename(file_path)
    capture = cv2.cv.CreateFileCapture(file_path)

    # open a window
    image = _load_image(capture, 0.0)
    window = gui.Window(file_name)
    window.image = image

    # click heads' positions on the first frame
    eventListener = gui.EventListener(window)
    jj, ii = eventListener.get_xy()

    # output
    for idx, (x, y) in enumerate(zip(jj, ii)):
        _dump_result(0.0, idx, x, y)

    # process each frame
    time = 0.0
    while True:
        image = _load_image(capture, time)
        if image is None:
            break
        gray_image = _to_grayscale(image)

        next_image = _load_image(capture, time + TIME_STEP)
        gray_next_image = _to_grayscale(next_image)

        # find similar patterns around points of the present frame from
        #     the next frame
        di, dj, ccmax = piv.find_flow(gray_image, gray_next_image, ii, jj,
                                      kernel_size=(PATTERN_SIZE, PATTERN_SIZE),
                                      di_range=(-FIND_BUFFER, FIND_BUFFER),
                                      dj_range=(-FIND_BUFFER, FIND_BUFFER))

        # translate positions
        ii += di
        jj += dj

        # draw found points
        for x, y in zip(jj, ii):
            _draw_marker(image, x, y)
        window.image = image

        # wait for mouse event
        new_xx, new_yy = eventListener.get_xy()

        # append new coordinates
        ii = numpy.append(ii, new_yy)
        jj = numpy.append(jj, new_xx)

        # output
        for idx, (x, y) in enumerate(zip(jj, ii)):
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


def _draw_marker(image, x, y, radius=2, color=MARKER_COLOR):
    """Draw a circle at the desired coordinate on the image."""
    point1 = (x - PATTERN_SIZE / 2, y - PATTERN_SIZE / 2)
    point2 = (x + PATTERN_SIZE / 2, y + PATTERN_SIZE / 2)

    cv2.cv.Rectangle(image, point1, point2, color, 1)
    cv2.cv.Circle(image, (x, y), radius, color, 2)


def _load_image(capture, time_sec):
    """Load image at the desired time.

    Retruns None if no image could load.
    """
    cv2.cv.SetCaptureProperty(capture, cv2.cv.CV_CAP_PROP_POS_MSEC,
                              time_sec * 1000)

    return cv2.cv.QueryFrame(capture)


def _to_grayscale(image):
    """Convert given image to grayscale."""
    return numpy.asarray(cv2.cv.GetMat(image)).astype(numpy.double)[:, :, 0]


if __name__ == "__main__":
    main(sys.argv[1])

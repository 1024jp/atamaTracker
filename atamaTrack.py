"""atamaTrack
"""

import sys

import cv2
import numpy

from modules import getXY, piv


# constants
TIME_STEP = 0.1  # time step in second
TOTAL_FRAMES = 20  # number of frames to track
D_RANGE = 15  # ???: something parametor for the pattern finding


def main(file_path):
    # load a movie file
    capture = cv2.cv.CreateFileCapture(file_path)

    # open a window
    cv2.cv.NamedWindow('Head Tracking', cv2.cv.CV_WINDOW_AUTOSIZE)

    # click heads' positions on the first frame
    image = load_image(capture, 0.0)
    initial_jjii = getXY.getXY(image).astype(numpy.int)
    ii = initial_jjii[:, 1]
    jj = initial_jjii[:, 0]

    # output
    for idx, (x, y) in enumerate(zip(jj, ii)):
        dump_result(0.0, idx, x, y)

    # process each frame
    for time in numpy.arange(TOTAL_FRAMES) * TIME_STEP:
        image = load_image(capture, time)
        gray_image = to_grayscale(image)
        
        next_image = load_image(capture, time + TIME_STEP)
        gray_next_image = to_grayscale(next_image)

        # find similar patterns around points of the present frame from
        #     the next frame
        di, dj, ccmax = piv.find_flow(gray_image, gray_next_image, ii, jj,
                                      kernel_size=(25, 25),
                                      di_range=(-D_RANGE, D_RANGE),
                                      dj_range=(-D_RANGE, D_RANGE))

        # translate positions
        ii += di
        jj += dj

        # output
        for idx, (x, y) in enumerate(zip(jj, ii)):
            draw_marker(image, x, y)
            dump_result(time + TIME_STEP, idx, x, y)

        cv2.cv.ShowImage('Head Tracking', image)
        cv2.waitKey(0)

    cv2.destroyAllWindows()


def dump_result(time, idx, x, y):
    """Print result to the standard output.

    Arguments:
    time -- [float] time in second
    idx -- [int] index number of person
    x -- [int] x coordinate
    y -- [int] y coordinate
    """
    print("{} {} {} {}".format(time, idx, y, x))


def draw_marker(image, x, y, radius=10, color=(255, 0, 0), stroke=2):
    """ Draw a circle at the desired coordinate on the image."""
    cv2.cv.Circle(image, (x, y), radius, color, stroke)


def load_image(capture, time_sec):
    """Load image at the desired time."""
    cv2.cv.SetCaptureProperty(capture, cv2.cv.CV_CAP_PROP_POS_MSEC,
                              time_sec * 1000)

    return cv2.cv.QueryFrame(capture)


def to_grayscale(image):
    """Convert given image to grayscale."""
    return numpy.asarray(cv2.cv.GetMat(image)).astype(numpy.double)[:, :, 0]


if __name__ == "__main__":
    main(sys.argv[1])

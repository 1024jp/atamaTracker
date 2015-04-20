"""graphics module
"""

import cv2


class Marker:
    """Marker settings.
    """
    COLOR = (27, 190, 124)  # (B, G, R)
    RADIUS = 2


def draw_marker(image, point, frame_size=0):
    """Draw a circle at the given location on the image.
    """
    cv2.circle(image, (point.x, point.y), Marker.RADIUS, Marker.COLOR, 2)

    if frame_size > 0:
        point1 = (point.x - frame_size / 2, point.y - frame_size / 2)
        point2 = (point.x + frame_size / 2, point.y + frame_size / 2)
        cv2.rectangle(image, point1, point2, Marker.COLOR, 1)

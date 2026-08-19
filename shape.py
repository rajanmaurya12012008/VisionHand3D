import cv2
import numpy as np


def detect_shape(points):

    if len(points) < 20:
        return ""

    contour = np.array(points, dtype=np.int32)

    perimeter = cv2.arcLength(contour, False)

    approx = cv2.approxPolyDP(
        contour,
        0.02 * perimeter,
        False
    )

    sides = len(approx)

    if sides >= 3 and sides <= 4:
        return "Triangle"
    elif sides >= 4 and sides <= 5:
        return "Rectangle"

    elif sides > 8:
        return "Circle"

    return "Unknown Shape"
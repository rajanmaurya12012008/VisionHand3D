import cv2
import numpy as np
import math


def distance(p1, p2):

    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def is_circle_complete(points):

    if len(points) < 30:
        return False

    # Starting point
    start_point = points[0]

    # Current / last point
    end_point = points[-1]

    # Distance between starting and ending point
    gap = distance(start_point, end_point)

    # Calculate size of drawing
    points_array = np.array(points, dtype=np.int32)

    x, y, width, height = cv2.boundingRect(points_array)

    size = max(width, height)

    if size == 0:
        return False

    # Start and end should be close
    # compared to the size of the drawing
    if gap < size * 0.15:
        return True

    return False


def detect_shape(points):

    if len(points) < 30:
        return ""

    # Don't detect anything until drawing is complete
    if not is_circle_complete(points):
        return ""

    contour = np.array(points, dtype=np.int32)

    contour = contour.reshape((-1, 1, 2))

    area = cv2.contourArea(contour)

    perimeter = cv2.arcLength(contour, True)

    if perimeter == 0:
        return ""

    circularity = (
        4 * math.pi * area
    ) / (perimeter * perimeter)

    approx = cv2.approxPolyDP(
        contour,
        0.02 * perimeter,
        True
    )

    sides = len(approx)

    if circularity > 0.60 and sides > 6:
        return "Circle"

    return ""


def create_perfect_circle(points):

    if len(points) < 30:
        return None

    points_array = np.array(
        points,
        dtype=np.int32
    )

    x, y, width, height = cv2.boundingRect(
        points_array
    )

    center_x = x + width // 2
    center_y = y + height // 2

    radius = int(
        (width + height) / 4
    )

    return center_x, center_y, radius
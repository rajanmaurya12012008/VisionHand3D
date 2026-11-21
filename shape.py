
import cv2
import numpy as np
import math


def distance(p1, p2):

    return math.hypot(
        p1[0] - p2[0],
        p1[1] - p2[1]
    )


def is_shape_complete(points):

    if len(points) < 30:
        return False

    gap = distance(points[0], points[-1])

    pts = np.array(points, dtype=np.int32)

    x, y, width, height = cv2.boundingRect(pts)

    size = max(width, height)

    if size < 80:
        return False

    if gap > size * 0.15:
        return False

    path_length = sum(
        distance(points[i - 1], points[i])
        for i in range(1, len(points))
    )

    if path_length < size * 1.5:
        return False

    return True


def get_approximation(points):

    pts = np.array(points, dtype=np.int32)

    contour = pts.reshape((-1, 1, 2))

    hull = cv2.convexHull(contour)

    perimeter = cv2.arcLength(hull, True)

    if perimeter == 0:
        return None, None

    approx = cv2.approxPolyDP(
        hull,
        0.025 * perimeter,
        True
    )

    return hull, approx


def detect_shape(points):

    if not is_shape_complete(points):
        return ""

    hull, approx = get_approximation(points)

    if hull is None:
        return ""

    sides = len(approx)

    # Triangle
    if sides == 3:
        return "Triangle"

    # Square or Rectangle
    if sides == 4:

        x, y, width, height = cv2.boundingRect(hull)

        ratio = width / height if height != 0 else 0

        if 0.85 <= ratio <= 1.15:
            return "Square"

        return "Rectangle"

    # Circle
    area = cv2.contourArea(hull)
    perimeter = cv2.arcLength(hull, True)

    if area > 0 and perimeter > 0:

        circularity = (
            4 * math.pi * area
        ) / (perimeter ** 2)

        x, y, width, height = cv2.boundingRect(hull)

        ratio = width / height if height != 0 else 0

        if (
            circularity > 0.68
            and 0.65 < ratio < 1.35
            and sides >= 5
        ):
            return "Circle"

    return ""


def create_perfect_circle(points):

    if len(points) < 30:
        return None

    pts = np.array(points, dtype=np.int32)

    x, y, width, height = cv2.boundingRect(pts)

    center_x = x + width // 2
    center_y = y + height // 2

    radius = int((width + height) / 4)

    return center_x, center_y, radius


def create_perfect_triangle(points):

    if len(points) < 30:
        return None

    hull, approx = get_approximation(points)

    if hull is None or len(approx) != 3:
        return None

    return [
        (int(point[0][0]), int(point[0][1]))
        for point in approx
    ]


def create_perfect_box(points, shape_name):

    if len(points) < 30:
        return None

    pts = np.array(points, dtype=np.int32)

    x, y, width, height = cv2.boundingRect(pts)

    # Make all four sides equal for a square
    if shape_name == "Square":

        side = max(width, height)

        center_x = x + width // 2
        center_y = y + height // 2

        x = center_x - side // 2
        y = center_y - side // 2

        width = side
        height = side

    # Four corners
    box_points = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height)
    ]

    return box_points

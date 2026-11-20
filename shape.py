
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

    start = points[0]
    end = points[-1]

    gap = distance(start, end)

    pts = np.array(points, dtype=np.int32)

    x, y, width, height = cv2.boundingRect(pts)

    size = max(width, height)

    if size < 80:
        return False

    # Check whether finger returned near starting point
    if gap > size * 0.15:
        return False

    # Check how much the finger has travelled
    path_length = sum(
        distance(points[i - 1], points[i])
        for i in range(1, len(points))
    )

    if path_length < size * 1.5:
        return False

    return True


def detect_shape(points):

    if not is_shape_complete(points):
        return ""

    pts = np.array(points, dtype=np.int32)

    contour = pts.reshape((-1, 1, 2))

    # Get outer boundary
    hull = cv2.convexHull(contour)

    perimeter = cv2.arcLength(hull, True)
    area = cv2.contourArea(hull)

    if perimeter == 0 or area == 0:
        return ""

    # Simplify boundary
    approx = cv2.approxPolyDP(
        hull,
        0.025 * perimeter,
        True
    )

    sides = len(approx)

    # Triangle detection
    if sides == 3:
        return "Triangle"

    # Circle detection
    circularity = (4 * math.pi * area) / (perimeter ** 2)

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

    pts = np.array(points, dtype=np.int32)

    contour = pts.reshape((-1, 1, 2))

    hull = cv2.convexHull(contour)

    perimeter = cv2.arcLength(hull, True)

    approx = cv2.approxPolyDP(
        hull,
        0.025 * perimeter,
        True
    )

    if len(approx) != 3:
        return None

    return [
        (int(point[0][0]), int(point[0][1]))
        for point in approx
    ]

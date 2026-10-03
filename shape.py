import cv2
import numpy as np
import math


def distance(p1, p2):

    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def is_shape_complete(points):

    # Minimum points
    if len(points) < 30:
        return False

    start_point = points[0]
    end_point = points[-1]

    # Distance between start and end
    gap = distance(
        start_point,
        end_point
    )

    points_array = np.array(
        points,
        dtype=np.int32
    )

    x, y, width, height = cv2.boundingRect(
        points_array
    )

    size = max(width, height)

    if size < 100:
        return False

    # Finger must come near starting point
    if gap > size * 0.10:
        return False

    # Calculate total distance travelled
    path_length = 0

    for i in range(1, len(points)):

        path_length += distance(
            points[i - 1],
            points[i]
        )

    # Make sure user actually drew a proper shape
    if path_length < size * 1.5:
        return False

    return True


def detect_shape(points):

    if not is_shape_complete(points):
        return ""

    contour = np.array(
        points,
        dtype=np.int32
    )

    contour = contour.reshape((-1, 1, 2))

    # Remove unnecessary noise
    hull = cv2.convexHull(contour)

    perimeter = cv2.arcLength(
        hull,
        True
    )

    if perimeter == 0:
        return ""

    approx = cv2.approxPolyDP(
        hull,
        0.04 * perimeter,
        True
    )

    sides = len(approx)


    # -----------------
    # TRIANGLE
    # -----------------

    if sides == 3:
        return "Triangle"


    # -----------------
    # CIRCLE
    # -----------------

    area = cv2.contourArea(hull)

    if area > 0:

        circularity = (
            4 * math.pi * area
        ) / (perimeter * perimeter)

        if circularity > 0.65 and sides >= 7:
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


def create_perfect_triangle(points):

    if len(points) < 30:
        return None

    contour = np.array(
        points,
        dtype=np.int32
    )

    contour = contour.reshape((-1, 1, 2))

    hull = cv2.convexHull(contour)

    perimeter = cv2.arcLength(
        hull,
        True
    )

    approx = cv2.approxPolyDP(
        hull,
        0.04 * perimeter,
        True
    )

    if len(approx) != 3:
        return None

    triangle_points = []

    for point in approx:

        x, y = point[0]

        triangle_points.append(
            (int(x), int(y))
        )

    return triangle_points
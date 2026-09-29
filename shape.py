import cv2
import numpy as np
import math


def detect_shape(points):

    if len(points) < 20:
        return ""


    contour = np.array(points, dtype=np.int32)

    # Close the rough shape
    closed_contour = contour.reshape((-1, 1, 2))

    # Calculate area and perimeter
    area = cv2.contourArea(closed_contour)
    perimeter = cv2.arcLength(closed_contour, True)

    if perimeter == 0:
        return ""

    # Circularity
    circularity = (4 * math.pi * area) / (perimeter * perimeter)

    # Approximate number of sides
    approx = cv2.approxPolyDP(
        closed_contour,
        0.02 * perimeter,
        True
    )

    sides = len(approx)


    # Circle
    if circularity > 0.70 and sides > 6:
        return "Circle"


    # Triangle
    if sides == 3:
        return "Triangle"


    # Rectangle
    if 4 <= sides <= 5:
        return "Rectangle"


    return "Unknown Shape"


def create_perfect_circle(points):

    if len(points) < 10:
        return None


    # Convert points to NumPy array
    points_array = np.array(points, dtype=np.int32)


    # Find bounding box
    x, y, width, height = cv2.boundingRect(points_array)


    # Find center
    center_x = x + width // 2
    center_y = y + height // 2


    # Use average size for equal radius
    radius = int((width + height) / 4)


    return center_x, center_y, radius
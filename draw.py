
import cv2
import numpy as np

points = []
last_point = None

def draw_with_finger(img, x, y):
    global last_point

    current_point = (x, y)

    if last_point is None:
        points.append(current_point)
        last_point = current_point
        return

    last_x, last_y = last_point

    # Ignore very small movements
    if abs(x - last_x) + abs(y - last_y) < 3:
        return

    # If finger suddenly jumps, start a new segment
    if abs(x - last_x) > 80 or abs(y - last_y) > 80:
        points.append(None)
        points.append(current_point)
        last_point = current_point
        return

    points.append(current_point)
    last_point = current_point


def show_drawing(img):
    for i in range(1, len(points)):
        if points[i] is None or points[i - 1] is None:
            continue

        cv2.line(
            img,
            points[i - 1],
            points[i],
            (0, 255, 0),
            5
        )


def clear_canvas():
    global last_point
    points.clear()
    last_point = None


def get_points():
    return [p for p in points if p is not None]

import cv2
import numpy as np

points = []


def draw_with_finger(img, x, y):

    # First point
    if len(points) == 0:
        points.append((x, y))

    else:
        last_x, last_y = points[-1]

        # Add point only when finger moves enough
        if abs(x - last_x) > 5 or abs(y - last_y) > 5:
            points.append((x, y))

    # Draw rough line
    if len(points) > 1:

        pts = np.array(points, dtype=np.int32)

        cv2.polylines(
            img,
            [pts],
            False,
            (0, 255, 0),
            5
        )


def clear_canvas():
    points.clear()


def get_points():
    return points
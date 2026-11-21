
import cv2
import numpy as np

canvas = None
points = []

def draw_with_finger(img, x, y):
    global canvas

    if canvas is None:
        canvas = np.zeros_like(img)

    points.append((x, y))

    if len(points) >= 2:
        cv2.line(
            canvas,
            points[-2],
            points[-1],
            (0, 255, 0),
            5
        )

    img[:] = cv2.add(img, canvas)


def clear_canvas():
    global canvas
    points.clear()
    canvas = None


def get_points():
    return points

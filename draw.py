
import cv2

points = []

def draw_with_finger(img, x, y):
    points.append((x, y))

    if len(points) > 1:
        cv2.line(
            img,
            points[-2],
            points[-1],
            (0, 255, 0),
            5
        )

def clear_canvas():
    points.clear()

def get_points():
    return points

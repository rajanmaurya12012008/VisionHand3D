import cv2

points = []


def draw_with_finger(img, x, y):

    points.append((x, y))

    for i in range(1, len(points)):

        cv2.line(
            img,
            points[i - 1],
            points[i],
            (0, 255, 0),
            5
        )


def clear_canvas():

    points.clear()
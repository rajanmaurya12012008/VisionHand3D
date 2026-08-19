import cv2

points = []


def draw_with_finger(img, x, y):

    if len(points) == 0:

        points.append((x, y))

    elif abs(x - points[-1][0]) > 5 or abs(y - points[-1][1]) > 5:
        
        points.append((x, y))

    if len(points) > 1:

        for i in range(1, len(points)):

            cv2.line(
                img,
                points[i -1],
                points[i],
                (0, 255, 0),
                5
            )


def clear_canvas():

    points.clear()


def get_points():

    return points
import cv2

from hand import detect_hand
from draw import draw_with_finger, clear_canvas, get_points
from shape import detect_shape

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    shape_name = ""

    if not success:
        print("Camera Error")
        continue

    img = cv2.flip(img, 1)

    img, landmarks = detect_hand(img)

    if len(landmarks) != 0:

        # Index Finger Tip
        x, y = landmarks[8]

        # Draw using finger
        draw_with_finger(img, x, y)

        # Thumb Tip
        thumb_x, thumb_y = landmarks[4] 

        # Distance between thumb & index
        distance = abs(x - thumb_x)

        # Pinch gesture = Clear Canvas
        if distance < 40:
            clear_canvas()

        # Detect Shape
        shape_name = detect_shape(get_points())

    cv2.putText(
        img,
        "Draw using Index Finger",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        3
    )

    cv2.putText(
        img,
        shape_name,
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    cv2.imshow("VisionHand 3D", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
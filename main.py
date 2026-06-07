import cv2

from hand import detect_hand
from draw import draw_with_finger, clear_canvas

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)

    img, landmarks = detect_hand(img)

    if len(landmarks) != 0:

        # Index finger tip
        x, y = landmarks[8]

        # Draw using finger
        draw_with_finger(img, x, y)

        # Thumb tip
        thumb_x, thumb_y = landmarks[4]

        # Distance between thumb & index
        distance = abs(x - thumb_x)

        # Pinch gesture = clear screen
        if distance < 40:

            clear_canvas()

    cv2.putText(
        img,
        "Draw with Index Finger",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        3
    )

    cv2.imshow("VisionHand 3D", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
import cv2

from hand import detect_hand
from draw import draw_with_finger, clear_canvas, get_points
from shape import detect_shape, create_perfect_circle


cap = cv2.VideoCapture(0)


while True:

    success, img = cap.read()

    shape_name = ""

    if not success:
        print("Camera Error")
        continue


    # Mirror camera
    img = cv2.flip(img, 1)


    # Detect hand
    img, landmarks = detect_hand(img)


    if len(landmarks) != 0:

        # Index Finger Tip
        x, y = landmarks[8]


        # Thumb Tip
        thumb_x, thumb_y = landmarks[4]


        # Distance between thumb and index
        distance = abs(x - thumb_x)


        # Get current points
        points = get_points()


        # Detect shape
        shape_name = detect_shape(points)


        # If Circle detected
        if shape_name == "Circle":

            # Create perfect mathematical circle
            circle = create_perfect_circle(points)


            if circle is not None:

                center_x, center_y, radius = circle


                # Draw perfect circle
                cv2.circle(
                    img,
                    (center_x, center_y),
                    radius,
                    (0, 255, 0),
                    5
                )


        else:

            # Normal rough drawing
            draw_with_finger(img, x, y)


        # Pinch = Clear Canvas
        if distance < 40:

            clear_canvas()


    # Instruction
    cv2.putText(
        img,
        "Draw using Index Finger",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        3
    )


    # Shape name
    cv2.putText(
        img,
        shape_name,
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )


    # Show camera
    cv2.imshow(
        "VisionHand 3D",
        img
    )


    # ESC = Exit
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
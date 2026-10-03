import cv2

from hand import detect_hand, draw_hand
from draw import draw_with_finger, clear_canvas, get_points
from shape import detect_shape, create_perfect_circle


cap = cv2.VideoCapture(0)

# Final perfect circle
final_circle = None


while True:

    success, img = cap.read()

    shape_name = ""

    if not success:
        print("Camera Error")
        continue


    # Mirror camera
    img = cv2.flip(img, 1)


    # Detect hand
    img, landmarks, hand_landmarks = detect_hand(img)


    if len(landmarks) != 0:

        # Index Finger Tip
        x, y = landmarks[8]

        # Thumb Tip
        thumb_x, thumb_y = landmarks[4]

        # Distance between thumb and index
        distance = abs(x - thumb_x)


        # Get drawing points
        points = get_points()


        # If we are already drawing
        if final_circle is None:

            # Add finger point to drawing
            draw_with_finger(
                img,
                x,
                y
            )


            # Detect shape
            shape_name = detect_shape(points)


            # Circle completed
            if shape_name == "Circle":

                circle = create_perfect_circle(points)


                if circle is not None:

                    # Save perfect circle
                    final_circle = circle

                    # Remove rough drawing
                    clear_canvas()


        # Pinch = clear everything
        if distance < 40:

            clear_canvas()

            final_circle = None

            shape_name = ""


    # Draw perfect circle
    if final_circle is not None:

        center_x, center_y, radius = final_circle

        cv2.circle(
            img,
            (center_x, center_y),
            radius,
            (0, 255, 0),
            5
        )

        shape_name = "Perfect Circle"


    # Draw hand landmarks LAST
    # So circle doesn't hide the finger
    img = draw_hand(
        img,
        hand_landmarks
    )


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
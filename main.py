import cv2
import mediapipe as mp

# If your mediapipe install is incomplete/corrupted, mp.solutions may not exist.
# This fallback makes the error message clearer.
if not hasattr(mp, "solutions"):
    raise ImportError(
        "Your mediapipe installation does not have 'solutions'. "
        "Try: pip uninstall mediapipe -y  && pip install mediapipe "
        "(inside the same Python environment you run this script)."
    )

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

    cv2.imshow("VisionHand", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()


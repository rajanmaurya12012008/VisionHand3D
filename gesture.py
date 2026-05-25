def count_fingers(landmarks):

    fingers = []

    if len(landmarks) == 0:
        return 0

    # Thumb
    if landmarks[4][0] > landmarks[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]

    for tip in tips:

        if landmarks[tip][1] < landmarks[tip - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)
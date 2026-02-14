def fingers_up(landmarks):
    fingers = []

    # Index
    if landmarks[8][2] < landmarks[6][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Middle
    if landmarks[12][2] < landmarks[10][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Ring
    if landmarks[16][2] < landmarks[14][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Pinky
    if landmarks[20][2] < landmarks[18][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers

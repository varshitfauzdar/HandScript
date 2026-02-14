def fingers_up(landmarks):
    fingers = []

    # Index fingertip = 8, PIP joint = 6
    if landmarks[8][2] < landmarks[6][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Middle fingertip = 12, PIP = 10
    if landmarks[12][2] < landmarks[10][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers

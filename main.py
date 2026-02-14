import cv2
from hand_tracker import HandTracker
from whiteboard import Whiteboard
from utils import fingers_up

cap = cv2.VideoCapture(0)
tracker = HandTracker()
board = Whiteboard()

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    board.initialize(frame)

    landmarks = tracker.get_landmarks(frame)

    if landmarks:
        fingers = fingers_up(landmarks)

        index_x, index_y = landmarks[8][1], landmarks[8][2]

        if fingers == [1, 0]:
            board.draw(frame, index_x, index_y, True)
        else:
            board.draw(frame, index_x, index_y, False)

    frame = board.merge(frame)

    cv2.imshow("HandScript", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

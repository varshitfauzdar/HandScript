import cv2
import time
from hand_tracker import HandTracker
from whiteboard import Whiteboard
from utils import fingers_up

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

tracker = HandTracker()
board = Whiteboard()

prev_time = 0
frame_count = 0
mode = "IDLE"

# Color buttons (x1, x2, color)
colors = [
    (50, 150, (255, 0, 255)),   # Purple
    (200, 300, (255, 0, 0)),    # Blue
    (350, 450, (0, 255, 0)),    # Green
    (500, 600, (0, 0, 255)),    # Red
]

cv2.namedWindow("HandScript", cv2.WINDOW_NORMAL)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    board.initialize(frame)

    # Draw color panel
    for x1, x2, color in colors:
        cv2.rectangle(frame, (x1, 10), (x2, 60), color, -1)

    frame_count += 1

    if frame_count % 2 == 0:
        landmarks = tracker.get_landmarks(frame)

        if landmarks:
            fingers = fingers_up(landmarks)
            index_x, index_y = landmarks[8][1], landmarks[8][2]

            # --- Color Selection Zone ---
            if index_y < 60:
                for x1, x2, color in colors:
                    if x1 < index_x < x2:
                        board.set_color(color)

            mode = "IDLE"

            # Draw Mode
            if fingers == [1, 0, 0, 0]:
                mode = "DRAW"
                board.draw(frame, index_x, index_y, "draw")

            # Erase Mode
            elif fingers == [1, 1, 0, 0]:
                mode = "ERASE"
                board.draw(frame, index_x, index_y, "erase")

            # Clear Mode
            elif fingers == [1, 1, 1, 1]:
                mode = "CLEAR"
                board.clear()

            else:
                board.draw(frame, index_x, index_y, "idle")

    frame = board.merge(frame)

    # FPS Counter
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time else 0
    prev_time = current_time

    cv2.putText(frame, f"FPS: {int(fps)}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2)

    display_frame = cv2.resize(frame, (800, 600))
    cv2.imshow("HandScript", display_frame)

    key = cv2.waitKey(1) & 0xFF

# Quit with Q or ESC
    if key == ord('q') or key == ord('Q') or key == 27:
        break


cap.release()
cv2.destroyAllWindows()

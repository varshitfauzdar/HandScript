import cv2
import time
from hand_tracker import HandTracker
from whiteboard import Whiteboard
from utils import fingers_up

cap = cv2.VideoCapture(0)

# Lower resolution for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

tracker = HandTracker()
board = Whiteboard()

prev_time = 0
frame_count = 0

cv2.namedWindow("HandScript", cv2.WINDOW_NORMAL)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    board.initialize(frame)

    frame_count += 1

    # Process every 2nd frame for better FPS
    if frame_count % 2 == 0:
        landmarks = tracker.get_landmarks(frame)

        if landmarks:
            fingers = fingers_up(landmarks)

            index_x, index_y = landmarks[8][1], landmarks[8][2]

            # Only index finger up → Draw
            if fingers == [1, 0, 0, 0]:
                board.draw(frame, index_x, index_y, "draw")

            # Index + middle → Erase
            elif fingers == [1, 1, 0, 0]:
                board.draw(frame, index_x, index_y, "erase")

            # All fingers → Clear
            elif fingers == [1, 1, 1, 1]:
                board.clear()

            else:
                board.draw(frame, index_x, index_y, "idle")

    # Merge canvas
    frame = board.merge(frame)

    # FPS Counter
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time else 0
    prev_time = current_time

    cv2.putText(frame, f"FPS: {int(fps)}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    # Resize display to avoid DPI scaling issues
    display_frame = cv2.resize(frame, (800, 600))

    cv2.imshow("HandScript", display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

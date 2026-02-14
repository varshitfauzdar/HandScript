import streamlit as st
import cv2
import numpy as np
from collections import deque
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

st.title("🖐️ HandScript - Gesture Whiteboard")

# --------- Load MediaPipe Model ----------
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)
detector = vision.HandLandmarker.create_from_options(options)

# --------- Video Processor ----------
class HandScriptProcessor(VideoProcessorBase):
    def __init__(self):
        self.canvas = None
        self.points = deque(maxlen=5)

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        if self.canvas is None:
            self.canvas = np.zeros_like(img)

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_image)

        if result.hand_landmarks:
            h, w, _ = img.shape
            hand_landmarks = result.hand_landmarks[0]

            # Index finger tip = landmark 8
            x = int(hand_landmarks[8].x * w)
            y = int(hand_landmarks[8].y * h)

            # Draw circle at fingertip
            cv2.circle(img, (x, y), 8, (0, 255, 0), -1)

            # Drawing mode: if index finger above middle finger
            if hand_landmarks[8].y < hand_landmarks[12].y:
                self.points.append((x, y))
                for i in range(1, len(self.points)):
                    cv2.line(self.canvas,
                             self.points[i - 1],
                             self.points[i],
                             (255, 0, 255),
                             6)
            else:
                self.points.clear()

        # Merge canvas
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, inv)
        img = cv2.bitwise_or(img, self.canvas)

        return img


webrtc_streamer(
    key="handscript",
    video_processor_factory=HandScriptProcessor
)

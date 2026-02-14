import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.tasks.vision.HandLandmarker
        self.base_options = python.BaseOptions(
            model_asset_path= "C:/Users/varsh/OneDrive/Desktop/ai/HandScript/hand_landmarker.task"  # will use default bundled model
        )
        self.options = vision.HandLandmarkerOptions(
            base_options=self.base_options,
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(self.options)

    def get_landmarks(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        result = self.detector.detect(mp_image)

        landmarks = []
        if result.hand_landmarks:
            h, w, _ = frame.shape
            for hand_landmarks in result.hand_landmarks:
                for idx, lm in enumerate(hand_landmarks):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((idx, cx, cy))

        return landmarks

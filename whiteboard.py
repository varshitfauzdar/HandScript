import cv2
import numpy as np
from collections import deque

class Whiteboard:
    def __init__(self):
        self.canvas = None
        self.color = (255, 0, 255)
        self.brush_thickness = 8
        self.points = deque(maxlen=5)

    def initialize(self, frame):
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

    def draw(self, frame, x, y, drawing_mode):
        if drawing_mode:
            self.points.append((x, y))

            if len(self.points) > 1:
                for i in range(1, len(self.points)):
                    cv2.line(self.canvas,
                             self.points[i - 1],
                             self.points[i],
                             self.color,
                             self.brush_thickness)
        else:
            self.points.clear()

    def merge(self, frame):
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, inv)
        frame = cv2.bitwise_or(frame, self.canvas)
        return frame

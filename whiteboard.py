import cv2
import numpy as np
from collections import deque

class Whiteboard:
    def __init__(self):
        self.canvas = None
        self.points = deque(maxlen=5)
        self.color = (255, 0, 255)  # Default purple
        self.thickness = 6

    def initialize(self, frame):
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

    def set_color(self, color):
        self.color = color

    def draw(self, frame, x, y, mode):
        if mode == "draw":
            self.points.append((x, y))

            for i in range(1, len(self.points)):
                cv2.line(self.canvas,
                         self.points[i - 1],
                         self.points[i],
                         self.color,
                         self.thickness)

        elif mode == "erase":
            cv2.circle(self.canvas, (x, y), 20, (0, 0, 0), -1)

        else:
            self.points.clear()

    def clear(self):
        if self.canvas is not None:
            self.canvas[:] = 0

    def merge(self, frame):
        if self.canvas is None:
            return frame
        return cv2.addWeighted(frame, 1, self.canvas, 1, 0)

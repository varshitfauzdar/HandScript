import cv2
import numpy as np

class Whiteboard:
    def __init__(self):
        self.canvas = None
        self.prev_x, self.prev_y = 0, 0
        self.color = (255, 0, 255)
        self.brush_thickness = 8

    def initialize(self, frame):
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

    def draw(self, frame, x, y, drawing_mode):
        if drawing_mode:
            if self.prev_x == 0 and self.prev_y == 0:
                self.prev_x, self.prev_y = x, y

            cv2.line(self.canvas, (self.prev_x, self.prev_y),
                     (x, y), self.color, self.brush_thickness)

            self.prev_x, self.prev_y = x, y
        else:
            self.prev_x, self.prev_y = 0, 0

    def merge(self, frame):
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, inv)
        frame = cv2.bitwise_or(frame, self.canvas)
        return frame

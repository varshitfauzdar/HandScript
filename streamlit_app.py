import streamlit as st
import cv2
import numpy as np
import pickle
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

model = pickle.load(open("gesture_model.pkl", "rb"))

st.title("🖐️ HandScript - Web Version")

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.canvas = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        if self.canvas is None:
            self.canvas = np.zeros_like(img)

        # simple demo draw dot in center
        cv2.circle(img, (320,240), 10, (255,0,255), -1)

        return img

webrtc_streamer(key="handscript", video_processor_factory=VideoProcessor)

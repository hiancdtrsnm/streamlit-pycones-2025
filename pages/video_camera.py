import streamlit as st
import cv2
import numpy as np
import av
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer

st.set_page_config(layout="wide")
st.title("Webcam Effects Demo")

# Video processor compatible with streamlit-webrtc's current API
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        # default; will be updated from the sidebar selection below
        self.effect = "Normal"

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        effect = getattr(self, "effect", "Normal")

        if effect == "Normal":
            processed_img = img

        elif effect == "Grayscale":
            processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)

        elif effect == "Canny Edge":
            edges = cv2.Canny(img, 100, 200)
            processed_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        elif effect == "Black & White":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            processed_img = cv2.cvtColor(bw, cv2.COLOR_GRAY2BGR)

        elif effect == "Blur":
            processed_img = cv2.GaussianBlur(img, (21, 21), 0)

        elif effect == "Invert":
            processed_img = cv2.bitwise_not(img)

        else:
            processed_img = img

        return av.VideoFrame.from_ndarray(processed_img, format="bgr24")

# Sidebar for effect selection
st.sidebar.title("Choose a filter")
selected_effect = st.sidebar.selectbox(
    "Select a real-time video effect",
    ("Normal", "Grayscale", "Canny Edge", "Black & White", "Blur", "Invert"),
)

# Start WebRTC and get a handle to the processor instance
webrtc_ctx = webrtc_streamer(
    key="webcam-with-effects",
    video_processor_factory=VideoProcessor,
    sendback_audio=False,
)

# Update the running processor's effect live
if webrtc_ctx.video_processor:
    webrtc_ctx.video_processor.effect = selected_effect


st.code("""
import streamlit as st
....

class VideoProcessor(VideoProcessorBase):
    pass

# Sidebar for effect selection
st.sidebar.title("Choose a filter")
selected_effect = st.sidebar.selectbox(
    "Select a real-time video effect",
    ("Normal", "Grayscale", "Canny Edge", "Black & White", "Blur", "Invert"),
)

# Start WebRTC and get a handle to the processor instance
webrtc_ctx = webrtc_streamer(
    key="webcam-with-effects",
    video_processor_factory=VideoProcessor,
    sendback_audio=False,
)

# Update the running processor's effect live
if webrtc_ctx.video_processor:
    webrtc_ctx.video_processor.effect = selected_effect
""", language="python")
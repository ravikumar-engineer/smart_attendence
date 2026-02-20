import cv2
import streamlit as st
import os
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.join(PROJECT_ROOT, "TrainingImages")

def capture_faces(student_id, name, num_images=10):
    """
    Capture 'num_images' face images from webcam using Streamlit and save as RGB uint8.
    """
    os.makedirs(TRAINING_DIR, exist_ok=True)
    cam = cv2.VideoCapture(0)
    stframe = st.empty()  # placeholder for webcam feed
    count = 0

    st.info(f"Capturing {num_images} images for {name}. Look at the camera!")

    while count < num_images:
        ret, frame = cam.read()
        if not ret:
            st.warning("Failed to capture frame")
            continue

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Ensure 8-bit and C-contiguous
        rgb_frame = np.asarray(rgb_frame, dtype=np.uint8)
        if not rgb_frame.flags['C_CONTIGUOUS']:
            rgb_frame = np.ascontiguousarray(rgb_frame)

        # Show frame in Streamlit
        stframe.image(rgb_frame, channels="RGB")

        # Save frame as JPEG in TrainingImages
        save_path = os.path.join(TRAINING_DIR, f"{student_id}_{name}_{count}.jpg")
        # Save using OpenCV (it expects BGR)
        cv2.imwrite(save_path, cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
        count += 1

    cam.release()
    stframe.empty()
    st.success(f"Captured {num_images} images for {name}")
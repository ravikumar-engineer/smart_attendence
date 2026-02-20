import os
import numpy as np
from PIL import Image
import face_recognition
import pickle

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.join(PROJECT_ROOT, "TrainingImages")
ENCODINGS_FILE = os.path.join(PROJECT_ROOT, "TrainingImageLabel/face_encodings.pkl")

def train_faces():
    os.makedirs(os.path.dirname(ENCODINGS_FILE), exist_ok=True)
    encoded_faces = []
    student_ids = []

    for file in os.listdir(TRAINING_DIR):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        img_path = os.path.join(TRAINING_DIR, file)

        try:
            pil_img = Image.open(img_path).convert("RGB")  # Force RGB
            img = np.asarray(pil_img, dtype=np.uint8)
            # Ensure C-contiguous memory layout
            if not img.flags['C_CONTIGUOUS']:
                img = np.ascontiguousarray(img)
        except Exception as e:
            print(f"Skipping {file}, cannot read: {e}")
            continue

        # Make sure shape is correct
        if img.ndim != 3 or img.shape[2] != 3:
            print(f"Skipping {file}, not RGB shape")
            continue

        try:
            encodings = face_recognition.face_encodings(img)
        except Exception as e:
            print(f"Skipping {file}, face_recognition failed: {e}")
            continue

        if encodings:
            encoded_faces.append(encodings[0])
            student_ids.append(file.split('_')[0])
        else:
            print(f"No face found in {file}")

    if encoded_faces:
        data = {"encodings": encoded_faces, "ids": student_ids}
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump(data, f)
        print(f"Trained {len(encoded_faces)} faces")
    else:
        print("No valid faces found")
import os
import cv2
import pickle
import face_recognition
from db import mark_attendance

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ENCODINGS_FILE = os.path.join(PROJECT_ROOT, "TrainingImageLabel/face_encodings.pkl")

def run_face_attendance():
    if not os.path.exists(ENCODINGS_FILE):
        print("No trained encodings found. Run training first.")
        return

    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)

    cam = cv2.VideoCapture(0)
    recognized = set()
    stframe = None

    print("Face recognition started. Press 'q' to stop.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding, location in zip(encodings, face_locations):
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            if True in matches:
                idx = matches.index(True)
                student_id = data["ids"][idx]
                if student_id not in recognized:
                    mark_attendance(student_id, "Present")
                    recognized.add(student_id)
                    print(f"{student_id} marked present")
        # Optional: show video inside terminal loop (skip in Streamlit)
        # Press 'q' in terminal to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Face recognition ended.")
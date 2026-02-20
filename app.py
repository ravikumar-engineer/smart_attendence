import streamlit as st
from db import create_tables, add_student, get_students_by_class, mark_attendance
from face_capture import capture_faces
from train_faces import train_faces
from face_attendance import run_face_attendance

create_tables()

st.title("Smart Attendance System 🌟")

menu = ["Add Student", "Mark Attendance", "View Report"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Student":
    st.subheader("Add New Student")
    student_id = st.text_input("Student ID")
    name = st.text_input("Name")
    class_name = st.text_input("Class")

    if st.button("Add & Capture Face"):
        if student_id and name and class_name:
            add_student(student_id, name, class_name)
            capture_faces(student_id, name)
            train_faces()
            st.success(f"{name} added and faces trained!")
        else:
            st.warning("Please fill all fields")

elif choice == "Mark Attendance":
    st.subheader("Mark Attendance")
    method = st.radio("Method", ["Manual", "Face Recognition"])

    if method == "Manual":
        class_name = st.text_input("Class Name")
        if st.button("Load Students"):
            students = get_students_by_class(class_name)
            for sid, name in students:
                status = st.selectbox(f"{name} ({sid})", ["Present", "Absent"], key=sid)
                if st.button(f"Submit {name}", key=f"submit_{sid}"):
                    mark_attendance(sid, status)
                    st.success(f"Attendance for {name} marked as {status}")
    else:
        st.info("Starting face recognition. Check your terminal for live updates.")
        run_face_attendance()
        st.success("Face recognition completed!")

elif choice == "View Report":
    import sqlite3, pandas as pd
    st.subheader("Attendance Report")
    sid = st.text_input("Enter Student ID")
    if st.button("View Report"):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT date, status FROM attendance WHERE student_id=?", (sid,))
        records = cursor.fetchall()
        if records:
            df = pd.DataFrame(records, columns=["Date", "Status"])
            st.table(df)
        else:
            st.warning("No records found")
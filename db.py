import sqlite3
from datetime import date
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(PROJECT_ROOT, "database.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            class TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            date TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_student(student_id, name, class_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO students(student_id,name,class) VALUES (?,?,?)",
                   (student_id, name, class_name))
    conn.commit()
    conn.close()

def get_students_by_class(class_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name FROM students WHERE class=?", (class_name,))
    students = cursor.fetchall()
    conn.close()
    return students

def mark_attendance(student_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    today = str(date.today())
    cursor.execute("INSERT INTO attendance(student_id,date,status) VALUES (?,?,?)",
                   (student_id, today, status))
    conn.commit()
    conn.close()
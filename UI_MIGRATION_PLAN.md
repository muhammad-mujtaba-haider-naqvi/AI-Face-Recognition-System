# UI Migration Strategy (Tkinter to PyQt5 + Web UI)

## 1) Existing Screens and Backend Mapping

This migration keeps all existing backend logic and launches original Tkinter modules unchanged.

- Dashboard/Home: `main.py` -> `Face_Recognition_System`
- Student Registration + Dataset Collection: `student.py` -> `student`
- Face Recognition + Attendance Marking: `face_recognition.py` -> `face_recognition`
- Attendance Records: `attendance.py` -> `attendance_management`
- Face Training: `train.py` -> `train`
- Developer/Admin Info: `developer.py` -> `developer`
- Help Desk: `helpdesk.py` -> `helpdesk`
- Dataset Gallery: `face_data/` folder open action

## 2) New Architecture

- `frontend/`
  - `index.html` (layout and modules)
  - `styles.css` (theme, animations, glassmorphism)
  - `app.js` (event wiring and bridge calls)
- `backend/`
  - `bridge.py` (PyQt bridge methods and stats signals)
  - `tk_runner.py` (launches existing Tkinter screens by action)
- `modern_main.py`
  - PyQt5 shell with QWebEngineView and QWebChannel wiring

## 3) Bridge Event Mapping

JS action -> Python bridge -> Original Tkinter logic

- `openStudentRegistration()` -> `tk_runner.py student`
- `openFaceRecognition()` -> `tk_runner.py face_recognition`
- `openAttendanceRecords()` -> `tk_runner.py attendance`
- `openFaceTraining()` -> `tk_runner.py train`
- `openPhotoDataset()` -> opens `face_data/`
- `openDeveloperPanel()` -> `tk_runner.py developer`
- `openHelpDesk()` -> `tk_runner.py helpdesk`
- `openLegacyDashboard()` -> `tk_runner.py dashboard`

## 4) Stability and Responsiveness

- Camera/recognition and Tkinter windows run in separate subprocesses from PyQt shell.
- Web UI remains responsive while OpenCV and Tkinter operations are active.
- Dashboard statistics are computed on a background thread.

## 5) How To Run

1. Install dependencies:
   - `pip install PyQt5 PyQtWebEngine`
2. Start modern UI shell:
   - `python modern_main.py`

## 6) Notes

- Backend business logic and existing algorithms are untouched.
- Current DB logic, attendance flow, and OpenCV pipeline are preserved.
- Placeholder image paths are listed in frontend placeholder section for later replacement.

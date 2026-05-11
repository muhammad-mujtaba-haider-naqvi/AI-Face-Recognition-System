import argparse
import os
import sys
from pathlib import Path
from tkinter import Tk


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def launch_dashboard() -> None:
    from main import Face_Recognition_System

    root = Tk()
    Face_Recognition_System(root)
    root.mainloop()


def launch_student() -> None:
    from student import student

    root = Tk()
    student(root)
    root.mainloop()


def launch_face_recognition() -> None:
    from face_recognition import face_recognition

    root = Tk()
    face_recognition(root)
    root.mainloop()


def launch_attendance() -> None:
    from attendance import attendance_management

    root = Tk()
    attendance_management(root)
    root.mainloop()


def launch_train() -> None:
    from train import train

    root = Tk()
    train(root)
    root.mainloop()


def launch_developer() -> None:
    from developer import developer

    root = Tk()
    developer(root)
    root.mainloop()


def launch_helpdesk() -> None:
    from helpdesk import helpdesk

    root = Tk()
    helpdesk(root)
    root.mainloop()


def open_photos() -> None:
    os.startfile(str(PROJECT_ROOT / "face_data"))


ACTION_MAP = {
    "dashboard": launch_dashboard,
    "student": launch_student,
    "face_recognition": launch_face_recognition,
    "attendance": launch_attendance,
    "train": launch_train,
    "developer": launch_developer,
    "helpdesk": launch_helpdesk,
    "photos": open_photos,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch legacy Tkinter screens")
    parser.add_argument("action", choices=ACTION_MAP.keys())
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    ACTION_MAP[args.action]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

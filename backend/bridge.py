import json
import subprocess
import sys
import threading
from datetime import date
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class AppBridge(QObject):
    notification = pyqtSignal(str)
    statsReady = pyqtSignal(str)

    def __init__(self, project_root: Path):
        super().__init__()
        self.project_root = project_root
        self.tk_runner = self.project_root / "backend" / "tk_runner.py"

    def _launch_action(self, action: str, title: str) -> None:
        try:
            subprocess.Popen(
                [sys.executable, str(self.tk_runner), action],
                cwd=str(self.project_root),
            )
            self.notification.emit(f"Opened {title} window.")
        except Exception as exc:
            self.notification.emit(f"Failed to open {title}: {exc}")

    def _gather_stats(self) -> None:
        stats = {
            "students_registered": "N/A",
            "face_samples": 0,
            "today_attendance": "N/A",
            "model_status": "Missing",
        }

        try:
            face_data = self.project_root / "face_data"
            if face_data.exists():
                samples = [
                    p
                    for p in face_data.iterdir()
                    if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}
                ]
                stats["face_samples"] = len(samples)

            classifier = self.project_root / "classifier.xml"
            stats["model_status"] = "Ready" if classifier.exists() else "Missing"
        except Exception:
            pass

        # Avoid querying the DB from the UI shell process to prevent
        # potential native-extension crashes. Leave attendance count as
        # a placeholder; detailed DB queries are performed by the legacy
        # Tkinter modules which will run in separate processes.
        stats["today_attendance"] = "N/A"

        self.statsReady.emit(json.dumps(stats))

    @pyqtSlot()
    def requestDashboardStats(self) -> None:
        thread = threading.Thread(target=self._gather_stats, daemon=True)
        thread.start()

    @pyqtSlot()
    def openLegacyDashboard(self) -> None:
        self._launch_action("dashboard", "Legacy Dashboard")

    @pyqtSlot()
    def openStudentRegistration(self) -> None:
        self._launch_action("student", "Student Registration")

    @pyqtSlot()
    def openFaceRecognition(self) -> None:
        self._launch_action("face_recognition", "Face Recognition")

    @pyqtSlot()
    def openAttendanceRecords(self) -> None:
        self._launch_action("attendance", "Attendance Records")

    @pyqtSlot()
    def openFaceTraining(self) -> None:
        self._launch_action("train", "Face Training")

    @pyqtSlot()
    def openPhotoDataset(self) -> None:
        self._launch_action("photos", "Photo Dataset")

    @pyqtSlot()
    def openDeveloperPanel(self) -> None:
        self._launch_action("developer", "Developer Panel")

    @pyqtSlot()
    def openHelpDesk(self) -> None:
        self._launch_action("helpdesk", "Help Desk")

    @pyqtSlot()
    def exitApplication(self) -> None:
        # Let JS show animation before app exit.
        self.notification.emit("Closing application...")
        from PyQt5.QtWidgets import QApplication

        QApplication.instance().quit()

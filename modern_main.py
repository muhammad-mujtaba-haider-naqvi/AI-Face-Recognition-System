import sys
from pathlib import Path

from PyQt5.QtCore import QUrl
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow

from backend.bridge import AppBridge


class ModernAppWindow(QMainWindow):
    def __init__(self, project_root: Path):
        super().__init__()
        self.project_root = project_root
        self.setWindowTitle("Automatic Attendance Management System")
        self.resize(1440, 900)

        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)

        self.bridge = AppBridge(self.project_root)
        self.channel = QWebChannel(self.web_view.page())
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        frontend_file = self.project_root / "frontend" / "index.html"
        self.web_view.load(QUrl.fromLocalFile(str(frontend_file.resolve())))


def main() -> int:
    project_root = Path(__file__).resolve().parent

    app = QApplication(sys.argv)
    window = ModernAppWindow(project_root)
    window.showMaximized()

    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())

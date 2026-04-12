from __future__ import annotations
import os
import sys

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from . import APP_NAME, APP_TITLE, ORG_NAME
from .ui.main_window import MainWindow, ensure_ffmpeg
from .ui.theme import qss


def main() -> int:
    if sys.platform.startswith("linux") and "QT_QPA_PLATFORM" not in os.environ:
        os.environ.setdefault("QT_QPA_PLATFORM", "xcb")

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_TITLE)
    app.setOrganizationName(ORG_NAME)

    settings = QSettings(ORG_NAME, APP_NAME)
    app.setStyleSheet(qss(settings.value("theme", "dark")))

    bundle = ensure_ffmpeg()
    if bundle is None:
        return 0

    window = MainWindow(bundle)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

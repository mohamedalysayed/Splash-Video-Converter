from __future__ import annotations
import traceback
from typing import Optional

from PySide6.QtCore import QObject, QThread, Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

from ..core import ffmpeg as ffmod


class _DownloadWorker(QObject):
    progress = Signal(int, str)
    finished = Signal(object, str)  # (FFmpegBundle | None, error_message)

    def run(self) -> None:
        try:
            bundle = ffmod.download(progress=lambda p, m: self.progress.emit(p, m))
            self.finished.emit(bundle, "")
        except Exception as e:  # noqa: BLE001
            self.finished.emit(None, f"{e}\n\n{traceback.format_exc()}")


class FFmpegSetupDialog(QDialog):
    """Shown at startup when FFmpeg is missing. Offers one-click download."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("FFmpeg required")
        self.setModal(True)
        self.setMinimumWidth(560)
        self._bundle: Optional[ffmod.FFmpegBundle] = None
        self._thread: Optional[QThread] = None

        title = QLabel("One more thing…")
        title.setObjectName("SectionTitle")

        heading = QLabel("Splash needs FFmpeg")
        heading.setStyleSheet("font-size: 22px; font-weight: 700; letter-spacing: -0.3px;")

        msg = QLabel(
            "Splash uses FFmpeg under the hood to convert your files. "
            "We can download a fresh copy into the app's private folder (no admin rights needed), "
            "or you can install FFmpeg yourself and check again."
        )
        msg.setWordWrap(True)
        msg.setObjectName("SectionSubtitle")

        self._status = QLabel("")
        self._status.setObjectName("Hint")
        self._status.setWordWrap(True)

        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setVisible(False)

        self._download_btn = QPushButton("Download FFmpeg")
        self._download_btn.setObjectName("Primary")
        self._download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._download_btn.clicked.connect(self._start_download)

        self._retry_btn = QPushButton("I installed it — check again")
        self._retry_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._retry_btn.clicked.connect(self._recheck)

        self._quit_btn = QPushButton("Quit")
        self._quit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._quit_btn.clicked.connect(self.reject)

        btns = QHBoxLayout()
        btns.setSpacing(10)
        btns.addWidget(self._retry_btn)
        btns.addStretch()
        btns.addWidget(self._quit_btn)
        btns.addWidget(self._download_btn)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(heading)
        layout.addWidget(msg)
        layout.addSpacing(6)
        layout.addWidget(self._progress)
        layout.addWidget(self._status)
        layout.addSpacing(6)
        layout.addLayout(btns)

    def bundle(self) -> Optional[ffmod.FFmpegBundle]:
        return self._bundle

    # ---- actions ----

    def _recheck(self) -> None:
        bundle = ffmod.discover()
        if bundle and ffmod.verify(bundle):
            self._bundle = bundle
            self.accept()
        else:
            self._status.setText("Still not found on PATH.")

    def _start_download(self) -> None:
        self._download_btn.setEnabled(False)
        self._retry_btn.setEnabled(False)
        self._progress.setVisible(True)
        self._status.setText("Starting download…")

        self._thread = QThread(self)
        self._worker = _DownloadWorker()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress, Qt.ConnectionType.QueuedConnection)
        self._worker.finished.connect(self._on_finished, Qt.ConnectionType.QueuedConnection)
        self._thread.start()

    def _on_progress(self, pct: int, msg: str) -> None:
        if pct:
            self._progress.setValue(pct)
        self._status.setText(msg)

    def _on_finished(self, bundle: Optional[ffmod.FFmpegBundle], error: str) -> None:
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
            self._thread = None

        if bundle is None:
            self._status.setText(
                f"Download failed: {error.splitlines()[0] if error else 'unknown error'}"
            )
            self._download_btn.setEnabled(True)
            self._retry_btn.setEnabled(True)
            return

        self._bundle = bundle
        self.accept()

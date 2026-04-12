from __future__ import annotations
from pathlib import Path

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent, QCursor
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsOpacityEffect

from ..core.presets import INPUT_EXTENSIONS


class DropZone(QFrame):
    files_dropped = Signal(list)
    clicked = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("DropZone")
        self.setProperty("dragover", False)
        self.setAcceptDrops(True)
        self.setMinimumHeight(190)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self._icon = QLabel("\u25BC")
        self._icon.setObjectName("DropIcon")
        self._icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._title = QLabel("Drop videos here")
        self._title.setObjectName("DropTitle")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._hint = QLabel("or click to browse  •  MKV, MP4, MOV, WebM, AVI, MP3, WAV, and more")
        self._hint.setObjectName("DropHint")
        self._hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)
        layout.addStretch()
        layout.addWidget(self._icon)
        layout.addSpacing(6)
        layout.addWidget(self._title)
        layout.addWidget(self._hint)
        layout.addStretch()

        self._fx = QGraphicsOpacityEffect(self)
        self._fx.setOpacity(1.0)
        self.setGraphicsEffect(self._fx)

    # ---- events ----

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._pulse()
            self.clicked.emit()
        super().mousePressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:  # noqa: N802
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._set_hover(True)
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:  # noqa: N802
        self._set_hover(False)
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:  # noqa: N802
        self._set_hover(False)
        paths: list[str] = []
        for url in event.mimeData().urls():
            if not url.isLocalFile():
                continue
            p = Path(url.toLocalFile())
            if p.is_dir():
                paths.extend(str(f) for f in p.rglob("*") if f.is_file() and f.suffix.lower() in INPUT_EXTENSIONS)
            elif p.is_file() and p.suffix.lower() in INPUT_EXTENSIONS:
                paths.append(str(p))
        if paths:
            self.files_dropped.emit(paths)
        event.acceptProposedAction()

    def _set_hover(self, on: bool) -> None:
        self.setProperty("dragover", on)
        self.style().unpolish(self)
        self.style().polish(self)

    def _pulse(self) -> None:
        anim = QPropertyAnimation(self._fx, b"opacity", self)
        anim.setDuration(180)
        anim.setStartValue(0.55)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

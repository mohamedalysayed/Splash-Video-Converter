from __future__ import annotations
import os
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSettings, Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QColor

from .. import APP_NAME, APP_TITLE, ORG_NAME, __version__
from ..core.ffmpeg import FFmpegBundle
from ..core.job import Job, JobStatus, default_output_path
from ..core.presets import FORMAT_ORDER, FORMATS, QUALITIES, QUALITY_ORDER, INPUT_EXTENSIONS
from ..core.queue import QueueManager
from .drop_zone import DropZone
from .ffmpeg_dialog import FFmpegSetupDialog
from .queue_view import QueueView
from .settings_dialog import SettingsDialog
from .theme import qss


def _form_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("FormLabel")
    return lbl


def _shadow(color: str, blur: int = 24, y: int = 6, alpha: int = 60) -> QGraphicsDropShadowEffect:
    fx = QGraphicsDropShadowEffect()
    c = QColor(color)
    c.setAlpha(alpha)
    fx.setColor(c)
    fx.setBlurRadius(blur)
    fx.setOffset(0, y)
    return fx


class MainWindow(QMainWindow):
    def __init__(self, bundle: FFmpegBundle) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(980, 720)

        self._settings = QSettings(ORG_NAME, APP_NAME)
        cpu = os.cpu_count() or 2
        concurrency = int(self._settings.value("concurrency", max(1, cpu // 2)))

        self._bundle = bundle
        self._manager = QueueManager(bundle, concurrency=concurrency)
        self._manager.all_finished.connect(self._on_all_finished)
        self._manager.job_updated.connect(self._refresh_controls)
        self._manager.job_added.connect(self._refresh_controls)

        self._build_menu()
        self._build_ui()
        self._apply_theme(self._settings.value("theme", "dark"))
        self._refresh_controls()
        self._fit_to_screen()

        self._status_timer = QTimer(self)
        self._status_timer.setInterval(1000)
        self._status_timer.timeout.connect(self._refresh_controls)
        self._status_timer.start()

    # ---- construction ----

    def _build_menu(self) -> None:
        bar = self.menuBar()

        file_menu = bar.addMenu("&File")
        add_act = QAction("Add files…", self)
        add_act.setShortcut(QKeySequence.StandardKey.Open)
        add_act.triggered.connect(self._pick_files)
        file_menu.addAction(add_act)

        add_folder = QAction("Add folder…", self)
        add_folder.setShortcut("Ctrl+Shift+O")
        add_folder.triggered.connect(self._pick_folder)
        file_menu.addAction(add_folder)

        file_menu.addSeparator()
        quit_act = QAction("Quit", self)
        quit_act.setShortcut(QKeySequence.StandardKey.Quit)
        quit_act.triggered.connect(self.close)
        file_menu.addAction(quit_act)

        edit_menu = bar.addMenu("&Edit")
        clear_done = QAction("Clear completed", self)
        clear_done.triggered.connect(self._clear_finished)
        edit_menu.addAction(clear_done)

        view_menu = bar.addMenu("&View")
        toggle_theme = QAction("Toggle theme", self)
        toggle_theme.setShortcut("Ctrl+T")
        toggle_theme.triggered.connect(self._toggle_theme)
        view_menu.addAction(toggle_theme)

        prefs_act = QAction("Settings…", self)
        prefs_act.setShortcut("Ctrl+,")
        prefs_act.triggered.connect(self._open_settings)
        view_menu.addAction(prefs_act)

        help_menu = bar.addMenu("&Help")
        about_act = QAction("About Cast", self)
        about_act.triggered.connect(self._show_about)
        help_menu.addAction(about_act)

    def _build_hero(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("HeroBar")
        bar.setFixedHeight(102)

        wordmark_row = QHBoxLayout()
        wordmark_row.setSpacing(2)
        wordmark_row.setContentsMargins(0, 0, 0, 0)
        wordmark = QLabel("Cast")
        wordmark.setObjectName("AppWordmark")
        dot = QLabel(".")
        dot.setObjectName("AccentDot")
        wordmark_row.addWidget(wordmark)
        wordmark_row.addWidget(dot)
        wordmark_row.addStretch()

        title_col = QVBoxLayout()
        title_col.setSpacing(0)
        title_col.setContentsMargins(0, 0, 0, 0)
        title_col.addLayout(wordmark_row)
        tagline = QLabel("Convert any video or audio file — beautifully.")
        tagline.setObjectName("AppTagline")
        title_col.addWidget(tagline)

        self._theme_btn = QPushButton("\u263D  Dark")
        self._theme_btn.setObjectName("Ghost")
        self._theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_btn.clicked.connect(self._toggle_theme)

        self._settings_btn = QPushButton("\u2699  Settings")
        self._settings_btn.setObjectName("Ghost")
        self._settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._settings_btn.clicked.connect(self._open_settings)

        row = QHBoxLayout(bar)
        row.setContentsMargins(24, 14, 18, 14)
        row.setSpacing(12)
        row.addLayout(title_col, 1)
        row.addWidget(self._theme_btn)
        row.addWidget(self._settings_btn)
        return bar

    def _build_ui(self) -> None:
        self._hero = self._build_hero()

        # ---- drop zone ----
        self._drop = DropZone()
        self._drop.files_dropped.connect(self._add_files)
        self._drop.clicked.connect(self._pick_files)

        # ---- format + quality + output card ----
        self._format = QComboBox()
        for key in FORMAT_ORDER:
            self._format.addItem(FORMATS[key].label, userData=key)
        self._format.setCurrentIndex(FORMAT_ORDER.index(self._settings.value("format", "mp4")))
        self._format.currentIndexChanged.connect(
            lambda: self._settings.setValue("format", self._format.currentData())
        )

        self._quality = QComboBox()
        for key in QUALITY_ORDER:
            self._quality.addItem(QUALITIES[key].label, userData=key)
        self._quality.setCurrentIndex(QUALITY_ORDER.index(self._settings.value("quality", "medium")))
        self._quality.currentIndexChanged.connect(
            lambda: self._settings.setValue("quality", self._quality.currentData())
        )

        self._output_dir = QLineEdit()
        self._output_dir.setPlaceholderText("Same folder as each source file")
        self._output_dir.setText(self._settings.value("output_dir", "") or "")
        browse_btn = QPushButton("Browse")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.clicked.connect(self._pick_output_dir)

        self._same_as_source = QCheckBox("Save next to source files")
        self._same_as_source.setChecked(self._settings.value("same_as_source", "true") == "true")
        self._same_as_source.toggled.connect(self._on_same_as_source_toggled)
        self._on_same_as_source_toggled(self._same_as_source.isChecked())

        fmt_col = QVBoxLayout()
        fmt_col.setSpacing(6)
        fmt_col.addWidget(_form_label("Output format"))
        fmt_col.addWidget(self._format)

        q_col = QVBoxLayout()
        q_col.setSpacing(6)
        q_col.addWidget(_form_label("Quality"))
        q_col.addWidget(self._quality)

        form_row1 = QHBoxLayout()
        form_row1.setSpacing(18)
        form_row1.addLayout(fmt_col, 1)
        form_row1.addLayout(q_col, 1)

        out_col = QVBoxLayout()
        out_col.setSpacing(6)
        out_col.addWidget(_form_label("Output folder"))
        out_input_row = QHBoxLayout()
        out_input_row.setSpacing(8)
        out_input_row.addWidget(self._output_dir, 1)
        out_input_row.addWidget(browse_btn)
        out_col.addLayout(out_input_row)

        header = QLabel("Conversion options")
        header.setObjectName("SectionTitle")
        subheader = QLabel("Pick a destination format, quality, and where results land")
        subheader.setObjectName("SectionSubtitle")

        options_card = QFrame()
        options_card.setObjectName("Card")
        options_card.setGraphicsEffect(_shadow("#000000", blur=32, y=10, alpha=38))
        ol = QVBoxLayout(options_card)
        ol.setContentsMargins(22, 20, 22, 22)
        ol.setSpacing(14)
        ol.addWidget(header)
        ol.addWidget(subheader)
        ol.addSpacing(4)
        ol.addLayout(form_row1)
        ol.addLayout(out_col)
        ol.addWidget(self._same_as_source)

        # ---- queue card ----
        self._queue = QueueView(self._manager)
        self._queue.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        q_title = QLabel("Queue")
        q_title.setObjectName("SectionTitle")
        self._queue_count = QLabel("0 files")
        self._queue_count.setObjectName("Pill")

        queue_header = QHBoxLayout()
        queue_header.setSpacing(10)
        queue_header.addWidget(q_title)
        queue_header.addWidget(self._queue_count)
        queue_header.addStretch()

        self._remove_btn = QPushButton("Remove selected")
        self._remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._remove_btn.clicked.connect(self._remove_selected)

        self._cancel_btn = QPushButton("Cancel all")
        self._cancel_btn.setObjectName("Danger")
        self._cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_btn.clicked.connect(self._manager.cancel_all)

        self._start_btn = QPushButton("\u25B6  Start conversion")
        self._start_btn.setObjectName("Primary")
        self._start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._start_btn.setGraphicsEffect(_shadow("#0A84FF", blur=28, y=8, alpha=110))
        self._start_btn.clicked.connect(self._start)

        queue_header.addWidget(self._remove_btn)
        queue_header.addWidget(self._cancel_btn)
        queue_header.addSpacing(4)
        queue_header.addWidget(self._start_btn)

        queue_card = QFrame()
        queue_card.setObjectName("Card")
        queue_card.setGraphicsEffect(_shadow("#000000", blur=32, y=10, alpha=38))
        ql = QVBoxLayout(queue_card)
        ql.setContentsMargins(22, 20, 22, 22)
        ql.setSpacing(14)
        ql.addLayout(queue_header)
        ql.addWidget(self._queue)

        # ---- compose ----
        content = QWidget()
        content.setObjectName("AppRoot")
        inner = QVBoxLayout(content)
        inner.setContentsMargins(24, 20, 24, 20)
        inner.setSpacing(18)
        inner.addWidget(self._drop)
        inner.addWidget(options_card)
        inner.addWidget(queue_card, 1)

        root = QWidget()
        root.setObjectName("AppRoot")
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(self._hero)
        root_layout.addWidget(content, 1)
        self.setCentralWidget(root)

        self._status = self.statusBar()
        self._status.showMessage("Ready.")

    # ---- event handlers ----

    def _on_same_as_source_toggled(self, checked: bool) -> None:
        self._output_dir.setEnabled(not checked)
        self._settings.setValue("same_as_source", "true" if checked else "false")

    def _pick_files(self) -> None:
        patterns = " ".join(f"*{e}" for e in INPUT_EXTENSIONS)
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Choose media files",
            self._settings.value("last_input_dir", ""),
            f"Media files ({patterns});;All files (*)",
        )
        if files:
            self._settings.setValue("last_input_dir", str(Path(files[0]).parent))
            self._add_files(files)

    def _pick_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self, "Choose a folder", self._settings.value("last_input_dir", "")
        )
        if not folder:
            return
        self._settings.setValue("last_input_dir", folder)
        files = [
            str(p) for p in Path(folder).rglob("*")
            if p.is_file() and p.suffix.lower() in INPUT_EXTENSIONS
        ]
        self._add_files(files)

    def _pick_output_dir(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self, "Choose output folder", self._output_dir.text() or ""
        )
        if folder:
            self._output_dir.setText(folder)
            self._settings.setValue("output_dir", folder)

    def _add_files(self, paths: list[str]) -> None:
        fmt_key = self._format.currentData()
        q_key = self._quality.currentData()
        out_dir = None if self._same_as_source.isChecked() else (self._output_dir.text().strip() or None)
        added = 0
        for path in paths:
            if not Path(path).exists():
                continue
            output = default_output_path(path, fmt_key, out_dir)
            self._manager.add_job(
                Job(input_path=path, output_path=output, format_key=fmt_key, quality_key=q_key)
            )
            added += 1
        if added:
            self._status.showMessage(f"Added {added} file(s) to the queue.")

    def _remove_selected(self) -> None:
        rows = sorted({i.row() for i in self._queue.selectionModel().selectedRows()}, reverse=True)
        for row in rows:
            self._queue.model().remove_row(row)

    def _clear_finished(self) -> None:
        self._manager.clear_finished()
        self._queue.model().rebuild()

    def _start(self) -> None:
        if self._manager.pending_count() == 0 and self._manager.running_count() == 0:
            QMessageBox.information(self, APP_NAME, "Add some files to the queue first.")
            return
        self._manager.start()
        self._status.showMessage("Converting…")
        self._refresh_controls()

    def _on_all_finished(self) -> None:
        self._status.showMessage("All jobs finished.")
        self._refresh_controls()

    def _refresh_controls(self) -> None:
        running = self._manager.running_count()
        pending = self._manager.pending_count()
        total = len(list(self._manager.jobs()))
        self._queue_count.setText(f"{total} file{'' if total == 1 else 's'}")
        self._start_btn.setEnabled(pending > 0 and running == 0)
        self._cancel_btn.setEnabled(running > 0 or pending > 0)
        self._remove_btn.setEnabled(any(
            j.status in (JobStatus.PENDING, JobStatus.DONE, JobStatus.FAILED, JobStatus.CANCELLED)
            for j in self._manager.jobs()
        ))
        if running:
            self._status.showMessage(f"Converting {running} file(s) · {pending} queued")

    # ---- menu actions ----

    def _toggle_theme(self) -> None:
        current = self._settings.value("theme", "dark")
        new = "light" if current == "dark" else "dark"
        self._settings.setValue("theme", new)
        self._apply_theme(new)

    def _apply_theme(self, theme: str) -> None:
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(qss(theme))
        if hasattr(self, "_theme_btn"):
            self._theme_btn.setText("\u2600  Light" if theme == "dark" else "\u263D  Dark")

    def _open_settings(self) -> None:
        cpu = os.cpu_count() or 2
        dlg = SettingsDialog(self._settings, max_concurrency=cpu, parent=self)
        if dlg.exec() == dlg.DialogCode.Accepted:
            self._apply_theme(self._settings.value("theme", "dark"))
            self._manager.set_concurrency(int(self._settings.value("concurrency", cpu // 2)))

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"<h2 style='margin:0'>{APP_NAME}<span style='color:#0A84FF'>.</span></h2>"
            f"<p style='color:#8E8E93;margin-top:2px'>Version {__version__}</p>"
            "<p>A beautiful, modern video &amp; audio converter powered by FFmpeg.</p>"
            "<p>Drop files, pick a format, press Start.</p>"
            "<p style='color:#8E8E93;font-size:11px'>Licensed under GPL-3.0 · © Mohamed Aly Sayed</p>",
        )

    # ---- window ----

    def _fit_to_screen(self) -> None:
        """Size the window so all content is visible on first open, capped to the screen."""
        self.adjustSize()
        hint = self.sizeHint()
        screen = self.screen() or QApplication.primaryScreen()
        avail = screen.availableGeometry() if screen else None
        max_w = int(avail.width() * 0.92) if avail else hint.width()
        max_h = int(avail.height() * 0.92) if avail else hint.height()
        target_w = max(self.minimumWidth(), min(hint.width() + 24, max_w))
        target_h = max(self.minimumHeight(), min(hint.height() + 24, max_h))
        self.resize(target_w, target_h)
        if avail:
            geo = self.frameGeometry()
            geo.moveCenter(avail.center())
            self.move(geo.topLeft())

    def closeEvent(self, event) -> None:  # noqa: N802
        if self._manager.running_count() > 0:
            btn = QMessageBox.question(
                self,
                "Conversions in progress",
                "Conversions are still running. Cancel them and quit?",
                QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes,
            )
            if btn != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            self._manager.cancel_all()
        event.accept()


def ensure_ffmpeg(parent: Optional[QWidget] = None) -> Optional[FFmpegBundle]:
    """Discover FFmpeg or prompt the user to download it. Returns None if the user aborts."""
    from ..core import ffmpeg as ffmod

    bundle = ffmod.discover()
    if bundle and ffmod.verify(bundle):
        return bundle

    dlg = FFmpegSetupDialog(parent)
    if dlg.exec() != dlg.DialogCode.Accepted:
        return None
    return dlg.bundle()

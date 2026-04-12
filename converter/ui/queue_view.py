from __future__ import annotations
from typing import Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QLinearGradient
from PySide6.QtWidgets import (
    QStyledItemDelegate,
    QTableView,
    QAbstractItemView,
    QHeaderView,
)

from ..core.job import Job, JobStatus
from ..core.presets import FORMATS
from ..core.probe import file_size, human_size
from ..core.queue import QueueManager


HEADERS = ["File", "Format", "Status", "Progress", "Speed", "ETA", "Size"]


def _format_eta(seconds: Optional[float]) -> str:
    if seconds is None or seconds <= 0:
        return ""
    s = int(seconds)
    if s >= 3600:
        return f"{s // 3600}h {(s % 3600) // 60}m"
    if s >= 60:
        return f"{s // 60}m {s % 60}s"
    return f"{s}s"


class QueueModel(QAbstractTableModel):
    def __init__(self, manager: QueueManager) -> None:
        super().__init__()
        self._manager = manager
        self._ids: list[str] = []
        manager.job_added.connect(self._on_added)
        manager.job_updated.connect(self._on_updated)

    def _on_added(self, job_id: str) -> None:
        self.beginInsertRows(QModelIndex(), len(self._ids), len(self._ids))
        self._ids.append(job_id)
        self.endInsertRows()

    def _on_updated(self, job_id: str) -> None:
        if job_id in self._ids:
            row = self._ids.index(job_id)
            self.dataChanged.emit(self.index(row, 0), self.index(row, len(HEADERS) - 1))

    def remove_row(self, row: int) -> None:
        if 0 <= row < len(self._ids):
            job_id = self._ids[row]
            if self._manager.remove_job(job_id):
                self.beginRemoveRows(QModelIndex(), row, row)
                del self._ids[row]
                self.endRemoveRows()

    def job_at(self, row: int) -> Optional[Job]:
        if 0 <= row < len(self._ids):
            return self._manager.job(self._ids[row])
        return None

    def rebuild(self) -> None:
        self.beginResetModel()
        self._ids = [j.id for j in self._manager.jobs()]
        self.endResetModel()

    # ---- Qt model API ----

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._ids)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return len(HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):  # noqa: N802
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return HEADERS[section]
        return None

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        job = self.job_at(index.row())
        if job is None:
            return None
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return job.input_name
            if col == 1:
                return FORMATS[job.format_key].ext.lstrip(".").upper()
            if col == 2:
                return ""  # painted by StatusPillDelegate
            if col == 3:
                return ""  # painted by ProgressDelegate
            if col == 4:
                return job.speed if job.status == JobStatus.RUNNING else ""
            if col == 5:
                return _format_eta(job.eta_seconds)
            if col == 6:
                return human_size(file_size(job.input_path))
        elif role == Qt.ItemDataRole.ToolTipRole:
            if col == 0:
                return f"{job.input_path}\n→ {job.output_path}"
            if col == 2 and job.message:
                return job.message
        elif role == Qt.ItemDataRole.UserRole:
            return job
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if col in (1, 4, 5, 6):
                return int(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            if col == 0:
                return int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return None


_STATUS_COLORS = {
    JobStatus.PENDING:   ("#8E8E93", "#2C2C2E", "Queued"),
    JobStatus.RUNNING:   ("#0A84FF", "#0E2444", "Running"),
    JobStatus.DONE:      ("#30D158", "#0F2A1C", "Done"),
    JobStatus.FAILED:    ("#FF453A", "#3A1514", "Failed"),
    JobStatus.CANCELLED: ("#8E8E93", "#2C2C2E", "Cancelled"),
}


class StatusPillDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index: QModelIndex) -> None:
        if index.column() != 2:
            super().paint(painter, option, index)
            return

        job: Optional[Job] = index.data(Qt.ItemDataRole.UserRole)
        if job is None:
            super().paint(painter, option, index)
            return

        fg, bg, label = _STATUS_COLORS[job.status]
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        f = QFont(option.font)
        f.setPointSizeF(max(8.5, f.pointSizeF() - 0.5))
        f.setWeight(QFont.Weight.DemiBold)
        painter.setFont(f)
        fm = painter.fontMetrics()
        text_w = fm.horizontalAdvance(label)
        w = text_w + 22
        h = 22
        rect = option.rect
        x = rect.x() + (rect.width() - w) / 2
        y = rect.y() + (rect.height() - h) / 2
        pill = QRectF(x, y, w, h)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(bg)))
        painter.drawRoundedRect(pill, 11, 11)

        painter.setPen(QPen(QColor(fg)))
        painter.drawText(pill, Qt.AlignmentFlag.AlignCenter, label)
        painter.restore()


class ProgressDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index: QModelIndex) -> None:
        if index.column() != 3:
            super().paint(painter, option, index)
            return

        job: Optional[Job] = index.data(Qt.ItemDataRole.UserRole)
        if job is None:
            super().paint(painter, option, index)
            return

        if job.status == JobStatus.DONE:
            pct = 1.0
            label = "100%"
        elif job.status == JobStatus.FAILED:
            pct = 0.0
            label = "—"
        elif job.status == JobStatus.CANCELLED:
            pct = 0.0
            label = "—"
        elif job.status == JobStatus.PENDING:
            pct = 0.0
            label = ""
        else:
            pct = max(0.0, min(1.0, job.progress))
            label = f"{int(pct * 100)}%"

        rect = option.rect.adjusted(10, 10, -10, -10)
        h = 10
        y = rect.y() + (rect.height() - h) / 2
        track = QRectF(rect.x(), y, rect.width(), h)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # track
        track_color = QColor("#2C2C2E")
        track_color.setAlpha(150)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(track, h / 2, h / 2)

        # fill
        if pct > 0:
            fill_w = max(h, track.width() * pct)
            fill_rect = QRectF(track.x(), track.y(), fill_w, track.height())
            grad = QLinearGradient(fill_rect.topLeft(), fill_rect.topRight())
            if job.status == JobStatus.DONE:
                grad.setColorAt(0.0, QColor("#30D158"))
                grad.setColorAt(1.0, QColor("#32D74B"))
            else:
                grad.setColorAt(0.0, QColor("#0A84FF"))
                grad.setColorAt(1.0, QColor("#5E5CE6"))
            painter.setBrush(QBrush(grad))
            painter.drawRoundedRect(fill_rect, h / 2, h / 2)

        # label
        if label:
            f = QFont(option.font)
            f.setPointSizeF(max(8.5, f.pointSizeF() - 1))
            f.setWeight(QFont.Weight.DemiBold)
            painter.setFont(f)
            painter.setPen(QPen(QColor("#8E8E93")))
            painter.drawText(
                option.rect.adjusted(0, 0, 0, 0),
                int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter),
                label + "   ",
            )
        painter.restore()


class QueueView(QTableView):
    def __init__(self, manager: QueueManager) -> None:
        super().__init__()
        self._model = QueueModel(manager)
        self.setModel(self._model)
        self.setItemDelegateForColumn(2, StatusPillDelegate(self))
        self.setItemDelegateForColumn(3, ProgressDelegate(self))
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setAlternatingRowColors(False)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.verticalHeader().setDefaultSectionSize(50)
        self.setFrameShape(QTableView.Shape.NoFrame)
        self.setAutoFillBackground(False)
        self.viewport().setAutoFillBackground(False)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        for i in (1, 2, 4, 5, 6):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setMinimumSectionSize(88)
        header.setHighlightSections(False)

    def model(self) -> QueueModel:  # type: ignore[override]
        return self._model

    def selected_jobs(self) -> list[Job]:
        rows = sorted({i.row() for i in self.selectionModel().selectedRows()})
        return [j for j in (self._model.job_at(r) for r in rows) if j is not None]

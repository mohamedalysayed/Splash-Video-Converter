from __future__ import annotations
import os
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, QThread, Signal

from .ffmpeg import FFmpegBundle, hidden_subprocess_flags
from .presets import FORMATS, QUALITIES, build_ffmpeg_args
from .probe import probe_duration


class JobStatus(str, Enum):
    PENDING = "Queued"
    RUNNING = "Converting"
    DONE = "Done"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


@dataclass
class Job:
    input_path: str
    output_path: str
    format_key: str
    quality_key: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    status: JobStatus = JobStatus.PENDING
    progress: float = 0.0          # 0..1
    duration: Optional[float] = None
    speed: str = ""
    message: str = ""
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    log_tail: list[str] = field(default_factory=list)

    @property
    def input_name(self) -> str:
        return Path(self.input_path).name

    @property
    def output_name(self) -> str:
        return Path(self.output_path).name

    @property
    def eta_seconds(self) -> Optional[float]:
        if self.status != JobStatus.RUNNING or self.progress <= 0 or self.started_at is None:
            return None
        elapsed = time.time() - self.started_at
        remaining = elapsed * (1.0 - self.progress) / max(self.progress, 1e-6)
        return remaining


class JobWorker(QObject):
    """Runs a single FFmpeg job on its own thread. Emits progress and completion signals."""

    progress_changed = Signal(str, float, str)     # (job_id, fraction 0..1, speed)
    status_changed = Signal(str, str, str)         # (job_id, status name, message)
    log_line = Signal(str, str)                    # (job_id, line)

    def __init__(self, bundle: FFmpegBundle, job: Job) -> None:
        super().__init__()
        self._bundle = bundle
        self._job = job
        self._proc: Optional[subprocess.Popen] = None
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True
        proc = self._proc
        if proc and proc.poll() is None:
            try:
                proc.terminate()
            except OSError:
                pass

    def run(self) -> None:
        job = self._job
        job.started_at = time.time()
        job.duration = probe_duration(self._bundle.ffprobe, job.input_path)
        self.status_changed.emit(job.id, JobStatus.RUNNING.value, "")

        out_dir = Path(job.output_path).parent
        out_dir.mkdir(parents=True, exist_ok=True)

        fmt = FORMATS[job.format_key]
        quality = QUALITIES[job.quality_key]

        cmd = [
            self._bundle.ffmpeg,
            "-y", "-hide_banner", "-nostats",
            "-progress", "pipe:1",
            "-i", job.input_path,
            *build_ffmpeg_args(fmt, quality),
            job.output_path,
        ]

        try:
            self._proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                **hidden_subprocess_flags(),
            )
        except OSError as e:
            self._finish_failure(f"Could not launch FFmpeg: {e}")
            return

        self._drain_progress(self._proc)
        stderr_tail = self._drain_stderr(self._proc)
        rc = self._proc.wait()

        if self._cancelled:
            job.finished_at = time.time()
            self._remove_partial_output()
            self.status_changed.emit(job.id, JobStatus.CANCELLED.value, "Cancelled")
            return

        if rc == 0:
            job.progress = 1.0
            job.finished_at = time.time()
            self.progress_changed.emit(job.id, 1.0, "")
            self.status_changed.emit(job.id, JobStatus.DONE.value, "")
        else:
            self._finish_failure(stderr_tail or f"FFmpeg exited with code {rc}")

    def _drain_progress(self, proc: subprocess.Popen) -> None:
        assert proc.stdout is not None
        for raw in proc.stdout:
            if self._cancelled:
                break
            line = raw.strip()
            if not line or "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key == "out_time_us":
                try:
                    seconds = int(value) / 1_000_000.0
                except ValueError:
                    continue
                if self._job.duration and self._job.duration > 0:
                    frac = max(0.0, min(1.0, seconds / self._job.duration))
                    self._job.progress = frac
                    self.progress_changed.emit(self._job.id, frac, self._job.speed)
            elif key == "speed":
                self._job.speed = value
                self.progress_changed.emit(self._job.id, self._job.progress, value)
            elif key == "progress" and value == "end":
                self._job.progress = 1.0
                self.progress_changed.emit(self._job.id, 1.0, self._job.speed)
                break

    def _drain_stderr(self, proc: subprocess.Popen) -> str:
        assert proc.stderr is not None
        tail: list[str] = []
        for raw in proc.stderr:
            line = raw.rstrip()
            if not line:
                continue
            tail.append(line)
            if len(tail) > 20:
                tail.pop(0)
            self.log_line.emit(self._job.id, line)
        return "\n".join(tail)

    def _remove_partial_output(self) -> None:
        try:
            p = Path(self._job.output_path)
            if p.exists():
                p.unlink()
        except OSError:
            pass

    def _finish_failure(self, message: str) -> None:
        self._job.finished_at = time.time()
        self._job.message = message
        self._remove_partial_output()
        self.status_changed.emit(self._job.id, JobStatus.FAILED.value, message)


class JobThread(QThread):
    """Thin QThread that drives a JobWorker and exposes its signals."""

    progress_changed = Signal(str, float, str)
    status_changed = Signal(str, str, str)
    log_line = Signal(str, str)

    def __init__(self, bundle: FFmpegBundle, job: Job) -> None:
        super().__init__()
        self._worker = JobWorker(bundle, job)
        self._worker.progress_changed.connect(self.progress_changed)
        self._worker.status_changed.connect(self.status_changed)
        self._worker.log_line.connect(self.log_line)
        self.job = job

    def cancel(self) -> None:
        self._worker.cancel()

    def run(self) -> None:  # noqa: D401
        self._worker.run()


def default_output_path(input_path: str, format_key: str, out_dir: Optional[str]) -> str:
    fmt = FORMATS[format_key]
    src = Path(input_path)
    parent = Path(out_dir) if out_dir else src.parent
    candidate = parent / f"{src.stem}{fmt.ext}"
    if candidate.resolve() == src.resolve():
        candidate = parent / f"{src.stem} (converted){fmt.ext}"
    i = 2
    while candidate.exists():
        candidate = parent / f"{src.stem} ({i}){fmt.ext}"
        i += 1
    return str(candidate)

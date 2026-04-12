from __future__ import annotations
from typing import Optional

from PySide6.QtCore import QObject, Signal

from .ffmpeg import FFmpegBundle
from .job import Job, JobStatus, JobThread


class QueueManager(QObject):
    """Owns the list of jobs and runs up to `concurrency` workers in parallel."""

    job_added = Signal(str)
    job_updated = Signal(str)
    all_finished = Signal()

    def __init__(self, bundle: FFmpegBundle, concurrency: int = 2) -> None:
        super().__init__()
        self.bundle = bundle
        self.concurrency = max(1, concurrency)
        self._jobs: list[Job] = []
        self._threads: dict[str, JobThread] = {}
        self._running = False

    # ---- public api ----

    def set_bundle(self, bundle: FFmpegBundle) -> None:
        self.bundle = bundle

    def set_concurrency(self, n: int) -> None:
        self.concurrency = max(1, n)
        if self._running:
            self._spawn_up_to_limit()

    def add_job(self, job: Job) -> None:
        self._jobs.append(job)
        self.job_added.emit(job.id)
        if self._running:
            self._spawn_up_to_limit()

    def remove_job(self, job_id: str) -> bool:
        if job_id in self._threads:
            return False  # refuse to remove a running job; caller should cancel first
        for i, j in enumerate(self._jobs):
            if j.id == job_id:
                del self._jobs[i]
                return True
        return False

    def clear_finished(self) -> None:
        self._jobs = [j for j in self._jobs if j.status in (JobStatus.PENDING, JobStatus.RUNNING)]

    def jobs(self) -> list[Job]:
        return list(self._jobs)

    def job(self, job_id: str) -> Optional[Job]:
        return next((j for j in self._jobs if j.id == job_id), None)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._spawn_up_to_limit()

    def cancel_all(self) -> None:
        self._running = False
        for t in list(self._threads.values()):
            t.cancel()
        for j in self._jobs:
            if j.status == JobStatus.PENDING:
                j.status = JobStatus.CANCELLED
                self.job_updated.emit(j.id)

    def cancel(self, job_id: str) -> None:
        t = self._threads.get(job_id)
        if t:
            t.cancel()
            return
        j = self.job(job_id)
        if j and j.status == JobStatus.PENDING:
            j.status = JobStatus.CANCELLED
            self.job_updated.emit(j.id)

    def running_count(self) -> int:
        return len(self._threads)

    def pending_count(self) -> int:
        return sum(1 for j in self._jobs if j.status == JobStatus.PENDING)

    # ---- internals ----

    def _spawn_up_to_limit(self) -> None:
        while self._running and len(self._threads) < self.concurrency:
            nxt = next((j for j in self._jobs if j.status == JobStatus.PENDING), None)
            if nxt is None:
                break
            self._start_job(nxt)

        if self._running and not self._threads and self.pending_count() == 0:
            self._running = False
            self.all_finished.emit()

    def _start_job(self, job: Job) -> None:
        job.status = JobStatus.RUNNING
        thread = JobThread(self.bundle, job)
        thread.progress_changed.connect(self._on_progress)
        thread.status_changed.connect(self._on_status)
        thread.finished.connect(lambda jid=job.id: self._on_thread_finished(jid))
        self._threads[job.id] = thread
        self.job_updated.emit(job.id)
        thread.start()

    def _on_progress(self, job_id: str, fraction: float, speed: str) -> None:
        j = self.job(job_id)
        if j is None:
            return
        j.progress = fraction
        j.speed = speed
        self.job_updated.emit(job_id)

    def _on_status(self, job_id: str, status_value: str, message: str) -> None:
        j = self.job(job_id)
        if j is None:
            return
        j.status = JobStatus(status_value)
        if message:
            j.message = message
        self.job_updated.emit(job_id)

    def _on_thread_finished(self, job_id: str) -> None:
        thread = self._threads.pop(job_id, None)
        if thread is not None:
            thread.deleteLater()
        self._spawn_up_to_limit()

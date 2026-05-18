from __future__ import annotations
import os
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional


WINDOWS_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
LINUX_URL = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
LINUX_ARM64_URL = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz"


def hidden_subprocess_flags() -> dict:
    """Return kwargs that suppress console popups when spawning processes on Windows."""
    if sys.platform != "win32":
        return {}
    flags = 0
    if hasattr(subprocess, "CREATE_NO_WINDOW"):
        flags |= subprocess.CREATE_NO_WINDOW
    return {"creationflags": flags}


@dataclass
class FFmpegBundle:
    ffmpeg: str
    ffprobe: str

    def is_valid(self) -> bool:
        return bool(self.ffmpeg) and bool(self.ffprobe) and Path(self.ffmpeg).exists() and Path(self.ffprobe).exists()


def app_data_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    d = base / "Cast"
    d.mkdir(parents=True, exist_ok=True)
    return d


def bin_dir() -> Path:
    d = app_data_dir() / "bin"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _exe(name: str) -> str:
    return f"{name}.exe" if sys.platform == "win32" else name


def discover() -> Optional[FFmpegBundle]:
    """Look for ffmpeg + ffprobe on PATH or in app data. Return None if missing."""
    local_ff = bin_dir() / _exe("ffmpeg")
    local_fp = bin_dir() / _exe("ffprobe")
    if local_ff.exists() and local_fp.exists():
        return FFmpegBundle(str(local_ff), str(local_fp))

    system_ff = shutil.which("ffmpeg")
    system_fp = shutil.which("ffprobe")
    if system_ff and system_fp:
        return FFmpegBundle(system_ff, system_fp)

    return None


def verify(bundle: FFmpegBundle) -> bool:
    try:
        for binary in (bundle.ffmpeg, bundle.ffprobe):
            subprocess.run(
                [binary, "-version"],
                capture_output=True,
                timeout=10,
                **hidden_subprocess_flags(),
            )
        return True
    except (OSError, subprocess.TimeoutExpired):
        return False


ProgressCb = Callable[[int, str], None]  # (percent 0-100, message)


def download(progress: Optional[ProgressCb] = None) -> FFmpegBundle:
    """Download a static ffmpeg+ffprobe build into the app data dir. Raises on failure."""
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Windows":
        url = WINDOWS_URL
    elif system == "Linux":
        url = LINUX_ARM64_URL if machine in ("aarch64", "arm64") else LINUX_URL
    else:
        raise RuntimeError(
            f"Automatic FFmpeg download is not supported on {system}. "
            "Install FFmpeg manually (e.g. `brew install ffmpeg`) and restart the app."
        )

    archive_path = app_data_dir() / ("ffmpeg-download" + (".zip" if url.endswith(".zip") else ".tar.xz"))

    def _report(p: int, msg: str) -> None:
        if progress:
            progress(p, msg)

    _report(0, "Connecting…")
    with urllib.request.urlopen(url, timeout=30) as resp, open(archive_path, "wb") as out:
        total = int(resp.headers.get("Content-Length", 0))
        read = 0
        chunk = 1024 * 128
        while True:
            block = resp.read(chunk)
            if not block:
                break
            out.write(block)
            read += len(block)
            if total:
                _report(int(read * 95 / total), f"Downloading FFmpeg… {read // (1024*1024)} MB")
            else:
                _report(0, f"Downloading FFmpeg… {read // (1024*1024)} MB")

    _report(96, "Extracting…")
    target = bin_dir()
    ff_out = target / _exe("ffmpeg")
    fp_out = target / _exe("ffprobe")

    if str(archive_path).endswith(".zip"):
        with zipfile.ZipFile(archive_path) as zf:
            for name in zf.namelist():
                base = os.path.basename(name)
                if base.lower() in ("ffmpeg.exe", "ffprobe.exe"):
                    with zf.open(name) as src, open(target / base.lower(), "wb") as dst:
                        shutil.copyfileobj(src, dst)
    else:
        with tarfile.open(archive_path, "r:xz") as tf:
            for member in tf.getmembers():
                base = os.path.basename(member.name)
                if base in ("ffmpeg", "ffprobe") and member.isfile():
                    src = tf.extractfile(member)
                    if src is None:
                        continue
                    with src, open(target / base, "wb") as dst:
                        shutil.copyfileobj(src, dst)

    try:
        archive_path.unlink()
    except OSError:
        pass

    if sys.platform != "win32":
        for binary in (ff_out, fp_out):
            if binary.exists():
                binary.chmod(binary.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    if not (ff_out.exists() and fp_out.exists()):
        raise RuntimeError("FFmpeg archive did not contain ffmpeg/ffprobe binaries.")

    bundle = FFmpegBundle(str(ff_out), str(fp_out))
    if not verify(bundle):
        raise RuntimeError("Downloaded FFmpeg failed to run. Check your system permissions.")

    _report(100, "FFmpeg ready.")
    return bundle

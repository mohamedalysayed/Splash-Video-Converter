from __future__ import annotations
import json
import subprocess
from pathlib import Path
from typing import Optional

from .ffmpeg import hidden_subprocess_flags


def probe_duration(ffprobe: str, path: str) -> Optional[float]:
    """Return the duration of a media file in seconds, or None on failure."""
    try:
        result = subprocess.run(
            [
                ffprobe, "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                path,
            ],
            capture_output=True,
            text=True,
            timeout=20,
            **hidden_subprocess_flags(),
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout or "{}")
        dur = data.get("format", {}).get("duration")
        return float(dur) if dur is not None else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, ValueError, OSError):
        return None


def human_size(n: int) -> str:
    step = 1024.0
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < step:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= step
    return f"{n:.1f} PB"


def file_size(path: str) -> int:
    try:
        return Path(path).stat().st_size
    except OSError:
        return 0

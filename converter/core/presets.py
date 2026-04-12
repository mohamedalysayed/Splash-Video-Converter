from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FormatSpec:
    key: str
    label: str
    ext: str
    video_codec: Optional[str]
    audio_codec: Optional[str]
    kind: str  # "video" | "audio" | "image"


FORMATS: dict[str, FormatSpec] = {
    "mp4":  FormatSpec("mp4",  "MP4 (H.264 + AAC)",     ".mp4",  "libx264",    "aac",         "video"),
    "mkv":  FormatSpec("mkv",  "MKV (H.264 + AAC)",     ".mkv",  "libx264",    "aac",         "video"),
    "mov":  FormatSpec("mov",  "MOV (H.264 + AAC)",     ".mov",  "libx264",    "aac",         "video"),
    "webm": FormatSpec("webm", "WebM (VP9 + Opus)",     ".webm", "libvpx-vp9", "libopus",     "video"),
    "avi":  FormatSpec("avi",  "AVI (MPEG-4 + MP3)",    ".avi",  "mpeg4",      "libmp3lame",  "video"),
    "gif":  FormatSpec("gif",  "Animated GIF",          ".gif",  "gif",        None,          "image"),
    "mp3":  FormatSpec("mp3",  "MP3 audio",             ".mp3",  None,         "libmp3lame",  "audio"),
    "m4a":  FormatSpec("m4a",  "M4A audio (AAC)",       ".m4a",  None,         "aac",         "audio"),
    "wav":  FormatSpec("wav",  "WAV audio (PCM 16-bit)", ".wav", None,         "pcm_s16le",   "audio"),
}

FORMAT_ORDER = ["mp4", "mov", "mkv", "webm", "avi", "gif", "mp3", "m4a", "wav"]


@dataclass(frozen=True)
class QualitySpec:
    key: str
    label: str
    crf: int          # x264/x265/vp9 target quality (lower = better)
    audio_bitrate: str
    x264_preset: str


QUALITIES: dict[str, QualitySpec] = {
    "original": QualitySpec("original", "Original (near-lossless)", 17, "320k", "slow"),
    "high":     QualitySpec("high",     "High",                     20, "256k", "medium"),
    "medium":   QualitySpec("medium",   "Medium (recommended)",     23, "192k", "medium"),
    "small":    QualitySpec("small",    "Small (optimized size)",   28, "128k", "fast"),
}

QUALITY_ORDER = ["original", "high", "medium", "small"]

INPUT_EXTENSIONS = (
    ".mkv", ".mp4", ".mov", ".webm", ".avi", ".flv", ".wmv", ".m4v",
    ".mpg", ".mpeg", ".ts", ".mts", ".m2ts", ".ogv", ".3gp",
    ".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".opus", ".wma",
)


def build_ffmpeg_args(fmt: FormatSpec, q: QualitySpec) -> list[str]:
    """Return codec/quality args (without -i or output path)."""
    args: list[str] = []

    if fmt.video_codec is None:
        args += ["-vn"]
    elif fmt.key == "gif":
        args += [
            "-vf",
            "fps=15,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        ]
    else:
        args += ["-c:v", fmt.video_codec]
        if fmt.video_codec in ("libx264", "libx265"):
            args += ["-crf", str(q.crf), "-preset", q.x264_preset, "-pix_fmt", "yuv420p"]
        elif fmt.video_codec == "libvpx-vp9":
            args += ["-crf", str(q.crf), "-b:v", "0", "-row-mt", "1"]
        elif fmt.video_codec == "mpeg4":
            args += ["-qscale:v", str(max(1, q.crf - 15))]

    if fmt.audio_codec is None:
        args += ["-an"]
    else:
        args += ["-c:a", fmt.audio_codec]
        if fmt.audio_codec != "pcm_s16le":
            args += ["-b:a", q.audio_bitrate]

    if fmt.key == "mp4" or fmt.key == "mov":
        args += ["-movflags", "+faststart"]

    return args

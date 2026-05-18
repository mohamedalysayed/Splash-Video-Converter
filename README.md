# Splash

> A video converter that gets out of your way. Drop a file, pick a format, hit Start.

[![License](https://img.shields.io/badge/license-GPL--3.0-1c1c1e?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-1c1c1e?style=flat-square)](https://www.python.org)
[![Platforms](https://img.shields.io/badge/macOS-%C2%B7%20Windows%20%C2%B7%20Linux-1c1c1e?style=flat-square)](#download)
[![Buy Splash](https://img.shields.io/badge/Buy%20Splash-%2419%20once-0a0a0a?style=flat-square)](https://splash-video-converter.netlify.app)

Splash is what FFmpeg should have looked like the day it shipped. Drag in a clip — or an entire folder of 4K footage — pick an output format, watch the queue chew through it. No command line. No 200-deep menu. No subscription dragging you down.

Built in PySide6, runs on macOS, Windows, and Linux. ~74 MB single binary. Ships with sane defaults so the first run is as good as the hundredth.

<p align="center">
  <img width="900" alt="Splash converting a queue of files" src="https://github.com/user-attachments/assets/71edc6cf-dfe7-4e21-81b3-ffd07680f934" />
</p>

---

## Why this exists

I needed to convert about 200 MKV files to MOV one afternoon. HandBrake's queue UI made me want to put my laptop in the ocean. Adobe Media Encoder wanted $22/month for the privilege. Wondershare and Movavi tried to sell me 14 unrelated tools and called it a "Pro Suite."

So I wrote Splash. One window. One queue. The conversion happens and it's beautiful while it does. That's the whole thing.

If you've ever right-clicked a video file, scrolled past 9 menu items, opened a tool with three nested tabs, and thought *"this should be a button"* — this is for you.

---

## Download

Pre-built binaries for every platform live on the [Releases](https://github.com/mohamedalysayed/Splash-Video-Converter/releases/latest) page:

| OS | File | Notes |
|---|---|---|
| **macOS** (Apple Silicon) | `Splash-macos-arm64.dmg` | macOS 11+. M1/M2/M3/M4. Intel returns in v1.1. |
| **Windows** | `Splash-windows-x64.exe` | Windows 10/11, 64-bit. |
| **Linux** | `Splash-linux-x86_64` | Single ELF. `chmod +x` then run. |

> Prefer to support the work? The polished build with auto-updates is [$19, one-time, at splash-video-converter.netlify.app](https://splash-video-converter.netlify.app). No subscriptions, ever.

### macOS — the "is damaged" workaround

Apple charges $99/year to notarize apps. Until Splash makes enough to justify it, macOS will refuse the app on first launch with *"Splash is damaged and can't be opened."* One-time fix in Terminal:

```bash
xattr -cr /Applications/Splash.app
```

That's the whole workaround. You'll never see it again.

### Windows — the SmartScreen detour

First launch may show *"Windows protected your PC."* Click **More info → Run anyway**. Microsoft's reputation engine takes a few weeks of downloads to relax.

---

## Building from source

You need Python 3.9 or newer and the system Qt libraries.

```bash
git clone https://github.com/mohamedalysayed/Splash-Video-Converter.git
cd Splash-Video-Converter

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
python run.py
```

**Linux system deps** (one of these, depending on distro):

```bash
# Debian / Ubuntu / Pop!_OS
sudo apt install -y python3-venv libxcb-cursor0 libxkbcommon-x11-0 \
  libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
  libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 libxcb-xkb1 \
  libegl1 libgl1

# Fedora
sudo dnf install -y python3-virtualenv xcb-util-cursor libxkbcommon-x11 mesa-libEGL mesa-libGL

# Arch
sudo pacman -S --needed python python-virtualenv xcb-util-cursor libxkbcommon-x11
```

**FFmpeg**: if it's already on your `PATH`, Splash finds it. If not, the welcome screen offers a one-click download into Splash's private folder. No admin rights, no PATH editing.

> On macOS the auto-download isn't supported yet — install FFmpeg with `brew install ffmpeg`.

---

## Using Splash

There isn't much to learn. The whole UI fits in a screenshot.

1. **Drop files** — single clips, whole folders, mixed types. Splash recursively finds every video and audio file inside.
2. **Pick an output format** — MP4, MOV, MKV, WebM, AVI, GIF, MP3, M4A, WAV.
3. **Pick a quality** — Original (near-lossless), High, Medium (default), Small.
4. **Choose where files go** — next to the source (default) or a folder you pick.
5. **Hit Start** — the queue runs in parallel across your CPU cores. Real % / speed / ETA per file, no fake spinners.

You can cancel at any time. Partial output files get cleaned up automatically. Your source files are never touched — if an output name would collide, Splash auto-numbers (`clip (2).mp4`).

### Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Add files |
| `Ctrl+Shift+O` | Add folder |
| `Ctrl+T` | Toggle dark / light theme |
| `Ctrl+,` | Open Settings |
| `Ctrl+Q` | Quit |

---

## What's in and out

**Anything FFmpeg can decode** goes in: MKV, MP4, MOV, WebM, AVI, FLV, WMV, M4V, MPG, TS / MTS / M2TS, OGV, 3GP, MP3, M4A, WAV, FLAC, AAC, OGG, OPUS, WMA.

**Outputs** are opinionated — Splash picks the codec combination that works:

| Container | Video | Audio | Why |
|---|---|---|---|
| **MP4** | H.264 | AAC | The web default. `+faststart` for instant streaming. |
| **MOV** | H.264 | AAC | The Apple default. Same flags as MP4. |
| **MKV** | H.264 | AAC | The "this'll play anywhere" container. |
| **WebM** | VP9 | Opus | Best for the open web. |
| **AVI** | MPEG-4 | MP3 | For when grandma's DVD player needs a file. |
| **GIF** | — | — | 15 fps, 640 px wide, paletted. Looks pretty good. |
| **MP3** | — | MP3 | Audio extract for podcasts and the like. |
| **M4A** | — | AAC | Audio extract, Apple-friendly. |
| **WAV** | — | PCM | Uncompressed. For editing. |

### Quality presets

| Preset | CRF | Audio bitrate | When to use |
|---|---|---|---|
| Original | 17 | 320 k | Archival, masters, "I'll never re-encode this" |
| High | 20 | 256 k | Editing, client delivery |
| **Medium** *(default)* | 23 | 192 k | Everyday sharing — the right pick 80% of the time |
| Small | 28 | 128 k | Messaging, tight disks, low-bandwidth |

---

## Building your own binary

```bash
pip install -r requirements.txt pyinstaller
pyinstaller --clean --noconfirm build/splash.spec
# → dist/Splash       (Linux)
# → dist/Splash.exe   (Windows)
# → dist/Splash.app   (macOS bundle)
```

The CI in `.github/workflows/build.yml` does this for every `v*` tag and ships the artifacts to a GitHub Release. If you want to cut your own release, tag and push:

```bash
git tag v1.2.0
git push origin v1.2.0
```

---

## Troubleshooting

**App won't open on Linux** → install the Qt runtime libs listed in the Linux section above.

**"FFmpeg not found" and the auto-download fails** → install FFmpeg manually (`brew install ffmpeg`, `sudo apt install ffmpeg`, `winget install ffmpeg`, `sudo pacman -S ffmpeg`) and click *Check again*.

**A conversion fails** → hover the red **Failed** pill in the queue to see the exact FFmpeg error. 9 times out of 10 it's a corrupt input or a codec the source uses that FFmpeg doesn't have a license for.

**Fans spin up like a 747** → open *Settings*, dial down *Parallel conversions* to 1 or 2.

**Settings not persisting** → Splash uses Qt's native settings store. On Linux that's `~/.config/Splash/Splash.conf`. Delete to reset.

---

## Project layout

```
converter/
  app.py                  application bootstrap
  core/
    ffmpeg.py             FFmpeg discovery + static-build downloader
    presets.py            format & quality matrix + ffmpeg arg builder
    probe.py              ffprobe wrapper + filesize helpers
    job.py                Job dataclass + progress-parsing worker
    queue.py              parallel worker pool
  ui/
    theme.py              iOS-inspired dark + light QSS
    drop_zone.py          animated drag-and-drop surface
    queue_view.py         table + gradient progress + status pills
    ffmpeg_dialog.py      first-run FFmpeg setup
    settings_dialog.py    preferences
    main_window.py        hero bar + cards + queue composition

build/splash.spec         PyInstaller spec (Linux / Windows / macOS .app)
.github/workflows/build.yml  cross-OS build matrix + release publisher
landing/                  Vite + React landing page (deployed to Netlify)
run.py                    entry shim
```

---

## Contributing

PRs welcome. A few ground rules so we stay aligned:

1. **Open an issue first** for anything bigger than a one-file change. Saves us both time.
2. **Keep the UI clean.** Splash is a deliberately small surface. If a new feature needs a settings page, it probably doesn't belong.
3. **Keep the dependency list tiny.** Right now it's PySide6 plus FFmpeg on disk. Adding to that bar is high.
4. **New output format?** Update `FORMATS` in `converter/core/presets.py` and the README table above.

---

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).

You're allowed (and encouraged) to clone, study, modify, and redistribute Splash. If you ship a fork, ship it under GPL too. If Splash saves you time and you want to support the work without compiling it yourself, the polished build with auto-updates is [$19, one-time, at splash-video-converter.netlify.app](https://splash-video-converter.netlify.app).

---

## Built on

- **[FFmpeg](https://ffmpeg.org)** — the actual conversion engine. Splash is a face for it.
- **[PySide6 / Qt](https://www.qt.io/qt-for-python)** — the UI toolkit that makes one codebase render natively on three OSes.

---

## Contact

[muhammmedaly@gmail.com](mailto:muhammmedaly@gmail.com) · happy to hear what's broken, what's missing, and what you converted with it.

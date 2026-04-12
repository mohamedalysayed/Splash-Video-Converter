# Splash — Video Converter

> A beautiful, modern, cross-platform video & audio converter. Drop files in, pick a format, press Start.

![License](https://img.shields.io/badge/license-GPL--3.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![UI](https://img.shields.io/badge/UI-PySide6-41CD52)

Splash is a clean, opinionated FFmpeg front-end with a **modern iOS-inspired interface**. No command lines, no guesswork — drop a file on the window, pick an output format, and hit *Start*. It handles everything from a single clip to a whole folder of 4K footage.

---

## Table of contents

- [Highlights](#highlights)
- [Install — step by step](#install--step-by-step)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Run Splash](#run-splash)
- [How to use Splash](#how-to-use-splash)
- [Supported formats](#supported-formats)
- [Quality presets](#quality-presets)
- [Settings & shortcuts](#settings--shortcuts)
- [Building your own binary](#building-your-own-binary)
- [Troubleshooting](#troubleshooting)
- [Project layout](#project-layout)
- [Contributing](#contributing)
- [License](#license)

---

## Highlights

- **iOS-inspired UI** — SF-style typography, systemBlue accents, soft cards, animated drop zone, pill status badges, gradient progress bars.
- **Any → any.** Convert between MKV, MP4, MOV, WebM, AVI, GIF, MP3, M4A, and WAV in any combination.
- **Drag & drop.** Drop individual files or entire folders; Splash recursively finds every supported file.
- **Real progress per file.** Parses FFmpeg's structured progress output — shows %, speed, and ETA.
- **Parallel queue.** Runs multiple conversions simultaneously (defaults to half your CPU cores, tunable).
- **Zero-setup on Windows & Linux.** Missing FFmpeg? Splash offers a one-click download into its private folder.
- **Dark & light themes.** Toggle instantly with `Ctrl+T`.
- **Safe output naming.** Never overwrites your source files. Auto-numbers collisions (`clip (2).mp4`).
- **Cancel & clean up.** Cancel running jobs any time — partial output files are removed automatically.

---

## Install — step by step

You have two choices:
1. **Pre-built binary** — download and run, nothing to install.
2. **From source** — needs Python 3.9+.

### Windows

#### Option A — Pre-built binary (easiest)

1. Go to the [Releases](https://github.com/mohamedalysayed/Splash-Video-Converter/releases) page.
2. Download `Splash-windows-x64.exe`.
3. Double-click it. Done.

On first launch, if FFmpeg isn't already on your system, Splash will offer to download it for you — no admin rights needed.

#### Option B — From source

```powershell
# 1. Install Python 3.9+ from https://www.python.org/downloads/
#    During install, TICK "Add Python to PATH".

# 2. Open PowerShell and clone the repo
git clone https://github.com/mohamedalysayed/Splash-Video-Converter.git
cd Splash-Video-Converter

# 3. (Optional but recommended) create a virtual env
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 4. Install the one runtime dependency
pip install -r requirements.txt

# 5. Run it
python run.py
```

> FFmpeg: if you already have it installed, Splash finds it automatically. Otherwise click **Download FFmpeg** on the welcome screen.

---

### macOS

#### Prerequisites

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and FFmpeg (automatic download is not supported on macOS)
brew install python@3.11 ffmpeg
```

#### Run from source

```bash
git clone https://github.com/mohamedalysayed/Splash-Video-Converter.git
cd Splash-Video-Converter

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python run.py
```

---

### Linux

#### 1. Install Python 3.9+ and system Qt libraries

**Debian / Ubuntu / Mint / Pop!_OS:**
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip \
    libxcb-cursor0 libxkbcommon-x11-0 libxcb-icccm4 \
    libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
    libxcb-shape0 libxcb-xinerama0 libxcb-xkb1 libegl1 libgl1
```

**Fedora / RHEL:**
```bash
sudo dnf install -y python3 python3-pip python3-virtualenv \
    xcb-util-cursor libxkbcommon-x11 mesa-libEGL mesa-libGL
```

**Arch / Manjaro:**
```bash
sudo pacman -S --needed python python-pip python-virtualenv \
    xcb-util-cursor libxkbcommon-x11
```

#### 2. (Optional) Install FFmpeg system-wide

Splash can download a static FFmpeg build for you on first launch, but you can also install it yourself:

```bash
# Debian / Ubuntu
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

#### 3. Clone and run

```bash
git clone https://github.com/mohamedalysayed/Splash-Video-Converter.git
cd Splash-Video-Converter

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python run.py
```

---

## Run Splash

After installation, the launch command is always the same:

```bash
python run.py
```

Or install Splash as a package and get a `splash` command on your PATH:

```bash
pip install .
splash
```

Where Splash stores its private data:

| OS      | Folder                                                                    |
| ------- | ------------------------------------------------------------------------- |
| Windows | `%LOCALAPPDATA%\Splash\bin`                                               |
| macOS   | `~/Library/Application Support/Splash/bin`                                |
| Linux   | `~/.local/share/Splash/bin` *(respects `$XDG_DATA_HOME`)*                 |

---

## How to use Splash

1. **Open the app.** You'll see a hero bar, a big drop zone, a conversion options card, and an empty queue.
2. **Add files.** Either:
   - Drop files or entire folders onto the drop zone, **or**
   - Click the drop zone, **or**
   - `File → Add files…` (`Ctrl+O`) / `File → Add folder…` (`Ctrl+Shift+O`).
3. **Pick an output format** — MP4, MOV, MKV, WebM, AVI, GIF, MP3, M4A, or WAV.
4. **Pick a quality preset** — Original (near-lossless), High, Medium (default), or Small.
5. **Choose where files go:**
   - **Save next to source files** (checked by default), **or**
   - Turn that off and choose an output folder.
6. **Press *Start conversion*.** Watch the gradient progress bars — each row shows live %, speed, and ETA.
7. **Cancel any time** via the Cancel button. Partial output files are automatically cleaned up.

Splash **never overwrites** your source file. If an output name collides, it auto-numbers (`clip (2).mp4`, `clip (3).mp4`, …).

---

## Supported formats

### Inputs (anything FFmpeg can decode)

MKV · MP4 · MOV · WebM · AVI · FLV · WMV · M4V · MPG/MPEG · TS/MTS/M2TS · OGV · 3GP · MP3 · M4A · WAV · FLAC · AAC · OGG · OPUS · WMA

### Outputs

| Container | Video  | Audio | Notes                                          |
| --------- | ------ | ----- | ---------------------------------------------- |
| **MP4**   | H.264  | AAC   | `+faststart` — ready for instant web playback  |
| **MOV**   | H.264  | AAC   | `+faststart` — Apple-friendly                  |
| **MKV**   | H.264  | AAC   | Universal container                            |
| **WebM**  | VP9    | Opus  | Best for web                                   |
| **AVI**   | MPEG-4 | MP3   | Legacy compatibility                           |
| **GIF**   | —      | —     | 15 fps, 640px wide, paletted                   |
| **MP3**   | —      | MP3   | Audio-only extract                             |
| **M4A**   | —      | AAC   | Audio-only extract                             |
| **WAV**   | —      | PCM   | Uncompressed audio                             |

---

## Quality presets

| Preset                   | CRF | Audio  | Best for                         |
| ------------------------ | --- | ------ | -------------------------------- |
| Original (near-lossless) | 17  | 320k   | Archival, masters                |
| High                     | 20  | 256k   | Editing, high-quality delivery   |
| **Medium** *(default)*   | 23  | 192k   | Everyday sharing                 |
| Small                    | 28  | 128k   | Messaging, small disks           |

---

## Settings & shortcuts

Open **View → Settings…** (or the *Settings* button in the hero bar) to change:
- **Theme** — Dark or Light
- **Parallel conversions** — 1 up to your CPU core count

Settings persist across launches via Qt's native storage (registry on Windows, plist on macOS, INI on Linux).

### Keyboard shortcuts

| Shortcut       | Action                 |
| -------------- | ---------------------- |
| `Ctrl+O`       | Add files              |
| `Ctrl+Shift+O` | Add folder             |
| `Ctrl+T`       | Toggle dark / light    |
| `Ctrl+,`       | Open Settings          |
| `Ctrl+Q`       | Quit                   |

---

## Building your own binary

```bash
pip install -r requirements.txt pyinstaller
pyinstaller --clean --noconfirm build/splash.spec
# → dist/Splash (Linux)
# → dist/Splash.exe (Windows)
```

The `.github/workflows/build.yml` workflow builds Windows + Linux artifacts automatically on every `v*` git tag and publishes them to a GitHub Release.

---

## Troubleshooting

**The app won't open on Linux** — install the Qt runtime libraries listed in the Linux section above.

**"FFmpeg not found" and the download fails** — install FFmpeg manually (`brew install ffmpeg` on macOS, `sudo apt install ffmpeg` on Debian, `winget install ffmpeg` on Windows) and press *Check again*.

**A conversion fails** — hover the red **Failed** pill in the queue to see the FFmpeg error message. Most failures are due to corrupt input files or unsupported codecs.

**High CPU use** — open *Settings* and reduce *Parallel conversions* to 1 or 2.

---

## Project layout

```
converter/
  app.py                # application bootstrap
  core/
    ffmpeg.py           # FFmpeg discovery + static-build downloader
    presets.py          # format & quality matrix + ffmpeg arg builder
    probe.py            # ffprobe wrapper + filesize helpers
    job.py              # Job dataclass + progress-parsing worker
    queue.py            # parallel worker pool
  ui/
    theme.py            # iOS-inspired dark + light QSS
    drop_zone.py        # animated drag-and-drop surface
    queue_view.py       # table + gradient progress + status pills
    ffmpeg_dialog.py    # first-run FFmpeg setup
    settings_dialog.py  # preferences
    main_window.py      # hero bar + cards + queue composition
build/splash.spec        # PyInstaller spec
.github/workflows/build.yml
run.py                   # entry shim
```

---

## Contributing

PRs welcome. Please open an issue first for large changes so we can agree on scope.

1. Fork → branch → commit → push → PR.
2. Keep the UI clean and the dependency list tiny (ideally just PySide6).
3. If you add a new output format, update `FORMATS` in `converter/core/presets.py` and the README table above.

---

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).

## Acknowledgments

- **FFmpeg** — the workhorse behind every conversion.
- **PySide6 / Qt** — the UI toolkit.
- Built on the original *MKV to MOV Converter* by Mohamed Aly Sayed.

## Contact

[muhammmedaly@gmail.com](mailto:muhammmedaly@gmail.com)

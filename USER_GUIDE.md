# Splash — User Guide

*Welcome. You bought a tool to make video conversion disappear. Here's the 10-minute read that makes sure it does.*

---

## The 30-second tour

1. **Drop a file on the window.** A single clip, ten clips, a whole folder of 4K footage — it all works.
2. **Pick a format.** MP4 if you're not sure. MP4 is always a good answer.
3. **Press *Start conversion*.**

That's the whole product. Every other paragraph in this guide is a sharper edge of those three steps.

---

## Adding files

Three ways, pick whichever your hand reaches for:

- **Drag & drop** anywhere on the big drop zone in the middle of the window. Folders get walked recursively — every video and audio file inside gets queued automatically.
- **Click the drop zone** to open a file picker.
- **Menu**: *File → Add files…* (`Ctrl+O`) or *Add folder…* (`Ctrl+Shift+O`).

Splash recognises 25+ input formats out of the box: MKV, MP4, MOV, WebM, AVI, FLV, WMV, M4V, MPG, TS, OGV, 3GP, MP3, M4A, WAV, FLAC, AAC, OGG, OPUS, WMA — basically anything FFmpeg can decode.

---

## Picking the right output format

| You want… | Pick |
|---|---|
| To send a clip to anyone, anywhere | **MP4** |
| To hand it to a Mac user / iPhone user | **MOV** |
| Something that plays in every desktop player | **MKV** |
| To embed in a web page | **WebM** |
| A short looping clip for Slack / Twitter | **GIF** |
| Just the audio from a video | **MP3** for podcasts, **M4A** for Apple, **WAV** for editing |
| Maximum compatibility with old gear | **AVI** |

When in doubt, **MP4**. It's the universal pick for a reason.

---

## Picking the right quality

| Quality | What you get | When to use |
|---|---|---|
| **Original** | Visually lossless. Files stay big. | Archival, masters, "I'll re-edit this someday" |
| **High** | Crisp. Files about half the size of Original. | Client delivery, YouTube uploads |
| **Medium** *(default)* | Looks great. Files small enough to email. | 80% of the time. This is the right answer. |
| **Small** | Some compression artifacts visible up close. Files tiny. | Messaging, slow connections, packed drives |

The default is Medium because Medium is what you want. The other three exist for the times you know exactly why you don't want Medium.

---

## Where the output files go

By default, Splash saves the converted file **right next to the source**. So `~/Videos/holiday.mkv` becomes `~/Videos/holiday.mp4` and lives in the same folder.

If you'd rather route everything to one place:

1. Untick **Save next to source files** in the conversion options card.
2. Click **Choose output folder** and pick where.

**Your source files are never touched.** If an output name would collide with an existing file, Splash auto-numbers — `clip (2).mp4`, `clip (3).mp4`, and so on. You'll never accidentally overwrite anything.

---

## Running multiple conversions at once

Splash uses your CPU. All of it, if you let it.

By default it runs **half your CPU cores in parallel** — a balance between speed and keeping the rest of your system responsive. On an 8-core MacBook, that's 4 conversions happening simultaneously.

To push it harder:

1. **Settings → Parallel conversions** (or `Ctrl+,`)
2. Slide it up to your full core count

On a 16-core machine, you can have 16 files converting at the same time. The queue progress bars all move at once. It looks great. It also pegs your CPU, so close your other apps first.

---

## Cancelling jobs

Click the **Cancel** button next to any running job. Or **Cancel all** in the toolbar. Splash:

1. Kills the FFmpeg process immediately
2. Deletes the half-written output file (no orphan `.mp4.tmp` to clean up later)
3. Marks the job as cancelled in the queue

You can re-run a cancelled job by clicking the round arrow next to it.

---

## When a conversion fails

Failed jobs get a red **Failed** pill in the queue. Hover it — Splash shows you the exact error message from FFmpeg.

The two most common causes:

1. **Corrupt input file.** FFmpeg refuses to read it. Open the source in a player like VLC; if VLC complains too, the file's the problem, not Splash.
2. **Unsupported codec.** Some MKVs use codecs that need licensed plugins (proprietary stuff from old Blu-Ray rips, for example). Most modern files are fine.

If you hit something weird that you think Splash should handle, email it to **[muhammmedaly@gmail.com](mailto:muhammmedaly@gmail.com)** with the FFmpeg error message — that's exactly how the supported-format list grows.

---

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Add files |
| `Ctrl+Shift+O` | Add folder |
| `Ctrl+T` | Toggle dark / light theme |
| `Ctrl+,` | Open Settings |
| `Ctrl+Q` | Quit |

On macOS substitute `⌘` for `Ctrl`.

---

## Settings

There are exactly two things to configure. That's by design.

- **Theme** — Dark or Light. Both are hand-tuned; neither is auto-inverted from the other.
- **Parallel conversions** — From 1 (gentle) to your full CPU core count (full throttle). Default is half.

Settings persist across launches via your OS's native storage:
- **Windows**: registry
- **macOS**: plist in `~/Library/Preferences/`
- **Linux**: INI in `~/.config/Splash/`

Delete those to reset.

---

## FFmpeg — the engine under the hood

Splash uses FFmpeg to do the actual conversion work. You don't have to install FFmpeg yourself.

- **Windows & Linux**: if FFmpeg isn't on your system, the welcome screen offers a one-click download. The binary lives inside Splash's own folder and gets used only by Splash. No `PATH` editing. No admin rights.
- **macOS**: install once with `brew install ffmpeg`. The auto-downloader doesn't support macOS yet — sorry, working on it.

Splash will always prefer a system-installed FFmpeg if it finds one — so if you already have it set up, nothing changes.

---

## Updating Splash

When a new version ships, you'll get an email (the address from your Stripe receipt). Updates are free, forever. Just download the new binary and replace the old one — your settings carry over.

Watch the releases page if you'd rather get notifications via GitHub:
👉 [github.com/mohamedalysayed/Splash-Video-Converter/releases](https://github.com/mohamedalysayed/Splash-Video-Converter/releases)

---

## Help, refunds, and the small print

**Something's broken?** Email **[muhammmedaly@gmail.com](mailto:muhammmedaly@gmail.com)** with your Stripe receipt and a one-line description of what went wrong. Most issues get a reply same-day.

**Want a refund?** 30 days, no questions asked. Same email address.

**Found a bug?** Open an issue at [github.com/mohamedalysayed/Splash-Video-Converter/issues](https://github.com/mohamedalysayed/Splash-Video-Converter/issues). Patches even more welcome.

**Want to support the work?** You already did. Thank you. ✨

---

*Splash is open source under GPL-3.0. The polished build you bought funds the rest of the roadmap. If a friend asks where you got it, send them to [splash-video-converter.netlify.app](https://splash-video-converter.netlify.app).*

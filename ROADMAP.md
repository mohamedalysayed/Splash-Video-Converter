# Roadmap

What's shipped, what's next, and what's deliberately not on the list.

This is a living document. Dates are rough. Priorities shift based on what actual customers ask for, not what would be fun to build.

---

## Shipped (v1.0)

- The app itself — PySide6 UI, FFmpeg back-end, parallel queue, dark + light themes
- Landing page at [splash-video-converter.netlify.app](https://splash-video-converter.netlify.app) — Vite + React + Framer Motion, greyscale system
- Stripe checkout wired into every CTA at $19 once
- `/thank-you` success page with auto-OS-detection and direct download links per platform
- CI builds for macOS (Apple Silicon), Windows, and Linux on every `v*` tag, with a `.dmg` for macOS

---

## Next up (v1.1)

### Ship the Intel Mac binary

GitHub's `macos-13` runner pool is starved as of early 2026 — jobs sit queued for hours. Switching to a `universal2` build on `macos-14` (one binary for both architectures) is the right move. Apple Silicon already covers most of the Mac install base; this closes the gap.

**Effort:** half a day. Mostly verifying PySide6's universal2 wheels survive PyInstaller.

### Email backup of the download link

Right now if the buyer closes the success tab, their only proof of purchase is the Stripe receipt — which has no download URL. A Netlify Function listening to the Stripe webhook can email the download links via Resend the moment the payment lands. Three-hour job once the keys are wired.

### A 60-second demo video

Embedded above the fold on the landing page. The single biggest conversion lever for a paid utility, full stop. I'll record it the moment I have a clean test machine.

---

## When the numbers justify it

These have real costs (money or time) and only make sense once Splash is provably making money.

### Apple Developer ID — $99/year

Stops the `xattr -cr` step on first launch. Roughly 10% of macOS buyers will refund over that friction, so it pays for itself somewhere around the 50th sale. The build job is a 30-minute change once the cert exists.

### Gated downloads via Cloudflare R2 + signed URLs

Today the binaries live on public GitHub Release URLs. Anyone with the link can download without paying — the product runs on the honor system. This isn't actually a problem until it is: the people who'd hunt for direct links are the same people who'd find a leaked mirror anyway.

When sales hit something like 50+/month and a forum thread starts circulating direct links, the migration is:

1. Move binaries from GitHub Releases to a private R2 bucket
2. Stripe webhook → Netlify Function generates a 7-day signed R2 URL
3. Function emails it via Resend
4. `/thank-you` page polls `/api/order-status?session_id=…` and only shows downloads to verified buyers

Total: ~4 hours of work. Stays free at any reasonable scale (R2 has zero egress fees).

### Windows EV code-signing cert — ~$200/year

Kills the SmartScreen warning permanently. Lower priority than the Mac signing because most Windows buyers click through it without much friction. Worth doing once Windows sales prove out.

### Custom domain

`splash-video-converter.netlify.app` is fine for launch but looks unfinished. Something like `splashconverter.app` (~$15/year) signals "real product." Five-minute DNS change once a domain is registered.

---

## Probably never

A short list of things people will ask for that I'm not going to build, because the whole point of Splash is the small surface area:

- **A library / clip manager.** Splash converts files. Your OS already has a file manager. Use Finder.
- **Cloud features.** No accounts. No sync. No "Splash for Teams." It's a desktop tool.
- **AI upscaling / re-cuts / "smart edits."** There are good tools for those and they're not Splash.
- **Telemetry, analytics, or any kind of phone-home.** Splash should work the same with the network cable yanked.
- **A free tier with watermarks.** Insulting to free users, dishonest as a funnel. Either it's free (build from source — anyone can) or it's $19.

---

## Growth (the boring half)

Building the thing is the easy part. Getting customers is everything.

### Launch week

- Post on [Product Hunt](https://www.producthunt.com), aiming for a Tuesday or Wednesday 12:01 AM PST drop
- "Show HN" on Hacker News — lead with the open-source pitch, not the price
- Cross-post to `r/macapps`, `r/software`, `r/linux_gaming`, `r/videography`, `r/podcasting`
- Tweet thread with the 60-sec demo

### Month one

- Reach out to 5 YouTube channels that cover indie Mac/Windows software
- Write one technical blog post — "Building a cross-platform desktop app with PySide6 in 2026" — and post it on Lobsters
- SEO landing pages for high-intent keywords: "convert mkv to mov mac", "handbrake alternative", "permute alternative windows", "best mp4 converter no subscription"

### Steady state

- Lifetime updates promise honored, no exceptions
- Listen to support email. Build what people actually ask for twice.
- Don't add features for hypothetical users

---

## Strategic options (later)

These are the "if Splash works, then what" branches.

- **Splash Pro at $49 once** — hardware encoding (NVENC / QSV / VideoToolbox), subtitle burn-in, batch metadata edit. Pure margin once the core is steady.
- **Team license at $99 for 5 seats** — for studios and agencies. Same binary, different receipt.
- **Bundle pricing with other Splash tools** — if I ship a second Splash product, "buy 2 get 1 free" works well in indie land.
- **Acquisition** — micro-acquisition platforms (Acquire.com, MicroAcquire) trade indie utility tools at 2.5–4× annual revenue. Once Splash clears $3K MRR (one-time amortized) it's a sellable asset. Not the goal, but worth knowing the floor.

---

*Last meaningfully updated when v1.0 shipped. If this doc looks stale, it probably is — open an issue.*

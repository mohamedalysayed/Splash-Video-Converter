# Splash — Roadmap

> Path from "landing page deployed" → "money in the bank → binary in the customer's hands."

---

## Phase 0 — ✅ Done

- [x] App built (PySide6, FFmpeg front-end, iOS-inspired UI)
- [x] Landing page designed & deployed → https://splash-video-converter.netlify.app
- [x] Stripe payment link wired into all CTAs ($19 launch / $39 strikethrough)
- [x] `/thank-you` success page with OS-auto-detect + 4 download buttons
- [x] Stripe `success_url` template documented (`?session_id={CHECKOUT_SESSION_ID}`)

---

## Phase 1 — Make it buyable end-to-end

The landing page can take money today. The buyer flow is:
**Stripe checkout → `/thank-you` → download button per OS → install**.

### 1.1 — Cross-OS binaries (release artifacts) — ✅ Wired

CI builds all four artifacts on every `v*` git tag and publishes a GitHub Release. The `/thank-you` page links to `releases/latest/download/Splash-*` — start working the moment v1.0.0 is tagged.

- [x] **macOS — Apple Silicon** → `Splash-macos-arm64.dmg` (macos-14 runner, ad-hoc signed, DMG with drag-to-Applications layout)
- [x] **macOS — Intel** → `Splash-macos-x64.dmg` (macos-13 runner, same packaging)
- [x] **Windows — x64** → `Splash-windows-x64.exe` (windows-latest)
- [x] **Linux — x64** → `Splash-linux-x86_64` (ubuntu-latest)

Trigger: `git tag v1.0.0 && git push origin v1.0.0`. Build time ~6–10 min.

#### Known gaps (not blockers — paid upgrades)

- **macOS Gatekeeper warning** — Ad-hoc signing avoids the worst "is damaged" crash but does NOT bypass Gatekeeper. First-time users hit *"Splash is damaged and can't be opened"* and need to run `xattr -cr /Applications/Splash.app`. This is documented prominently on the success page and in the README. **Fix:** Apple Developer ID ($99/yr) + `notarytool` step in CI. ~30 min to wire once the cert is paid for.
- **Windows SmartScreen warning** — Users click *More info → Run anyway* on first launch. **Fix:** EV code-signing cert (~$200/yr) — solves it permanently after Microsoft's reputation engine catches up.
- **Intel Mac runner deprecation risk** — GitHub may sunset `macos-13` in late 2026. **Fix:** ship Apple-Silicon-only when that happens (95%+ of new Mac sales are AS by then). Or invest in universal2 builds via `lipo` — more complex.
- **Linux distros** — Single ELF binary works on Ubuntu/Fedora/Arch with modern glibc. **Future:** add proper `.deb`, `.rpm`, AppImage, and Flatpak when there's demand.

### 1.2 — Gated binary delivery (the missing link)

Right now Stripe takes the money and the customer gets a thank-you page. They need the binary. Recommended architecture below — see the FAQ at the bottom of this document for the full reasoning.

**Stack:**
- **Storage:** Cloudflare R2 (free: 10 GB storage, zero egress fees)
- **Webhook:** Netlify Function (free tier) listens for `checkout.session.completed`
- **Delivery:** Webhook generates a 7-day signed R2 URL per binary and emails it via Resend (free: 3k emails/mo)
- **License key (optional, later):** Generate a per-customer unlock key, store in a tiny KV (Cloudflare KV / Upstash Redis)

**Estimated effort:** 3–4 hours once binaries exist. Stays at $0/month until you cross ~10k downloads.

### 1.3 — Stripe success page — ✅ Done

Live at https://splash-video-converter.netlify.app/thank-you. To wire Stripe:

1. Stripe Dashboard → Payment Links → your link → **After payment**
2. Set custom URL to:
   ```
   https://splash-video-converter.netlify.app/thank-you?session_id={CHECKOUT_SESSION_ID}
   ```

The page auto-detects the buyer's OS, highlights their match, and shows download links for all four artifacts. Once Phase 1.2 (R2 + webhook) is in place, the same page polls `/api/order-status?session_id=…` and only shows downloads to verified buyers.

### 1.4 — Domain mapping

- [ ] Buy domain (suggestions: `splashconverter.app`, `getsplash.io`, `usesplash.com`, `splashvideo.app`)
- [ ] Add to Netlify project: `netlify domains:add <domain>`
- [ ] Update DNS at registrar (Netlify gives the records)
- [ ] Enable HTTPS (Netlify provisions Let's Encrypt automatically)

---

## Phase 2 — Get the first 100 customers

- [ ] Record a 60-second demo video (drag a file → watch it convert) — embed on landing page
- [ ] Add 2–3 testimonials section (early users via Twitter/Reddit DMs)
- [ ] Launch on **Product Hunt** — Tuesday/Wednesday 12:01am PST
- [ ] Post on **r/macapps**, **r/software**, **r/linux_gaming**, **r/videography**
- [ ] **Hacker News** — Show HN with a clear "no subscription, no telemetry, no AI" framing
- [ ] **GitHub stars push** — pin repo, write release notes, ask for stars in app footer

---

## Phase 3 — Compound the asset

- [ ] **Free version** with a watermark or single-file limit (funnel for paid)
- [ ] **SEO landing pages** for high-intent searches: "convert mkv to mov mac", "best mp4 converter mac", "handbrake alternative", "permute alternative windows"
- [ ] **Affiliate program** — 30% commission, payable in cash, no minimum payout
- [ ] **Bundle discount** — Splash + Splash-Accountability + future Splash tools at "buy 2 get 1 free"
- [ ] **Lifetime updates promise** is already in copy — honor it religiously

---

## Phase 4 — Strategic optionality

- [ ] **Watch competitor pricing.** If Permute raises, raise. If Wondershare drops, ignore.
- [ ] **One-time → "Pro" tier** ($49 once) adds: hardware encoding (NVENC/QSV/VideoToolbox), subtitle burn-in, batch metadata edit
- [ ] **Team license** at $99 for 5 seats — pure margin
- [ ] **Sell the asset** on Acquire.com once it clears $3k+ MRR (one-time amortized). 2.5–4× ARR is the going rate for indie utility tools.

---

## Appendix: "Can I host binaries for free and gate them behind Stripe?"

**TL;DR — Yes. Here's the honest breakdown.**

### Options I considered

| Host | Free tier | Gated? | Verdict |
|---|---|---|---|
| **GitHub Releases** | Unlimited | ❌ Public URLs | Free piracy. Skip. |
| **Netlify static** | 100 GB/mo bandwidth | ❌ Public | Same issue. Skip. |
| **Cloudflare R2** | 10 GB storage, **zero egress fees** | ✅ via signed URLs | **Winner.** |
| **Backblaze B2** | 10 GB storage, 1 GB egress/day | ✅ via signed URLs | Egress limit will bite at scale. |
| **AWS S3** | 5 GB, 100 GB egress | ✅ via presigned URLs | Egress costs after free tier hurt fast. |
| **LemonSqueezy / Gumroad** | Free | ✅ Built-in delivery | Trade ~5% fee + no Stripe for zero-effort delivery. |

### Recommended: Cloudflare R2 + Netlify Functions

```
[Customer]         [Stripe]              [Netlify Function]      [Cloudflare R2]      [Resend]
    │                 │                        │                       │                  │
    │── Buy $19 ─────>│                        │                       │                  │
    │                 │── checkout.session.    │                       │                  │
    │                 │   completed webhook ──>│                       │                  │
    │                 │                        │── Sign 7-day URL ────>│                  │
    │                 │                        │<──── signed URL ──────│                  │
    │                 │                        │── Email download link ──────────────────>│
    │<──────── Email with download links arrives ────────────────────────────────────────│
```

- **Total monthly cost at < 10,000 sales:** $0
- **Total monthly cost at 100,000 sales:** ~$5 (R2 storage tier)
- **Total setup time once binaries exist:** 3–4 hours

### Why not just use GitHub Releases?

Because anyone on the internet can `wget` the URL. You'd be selling something they could get for free in 5 seconds via Google. The whole "buy once" pitch dies. Use private storage + signed URLs.

### Alternative: Switch from Stripe to LemonSqueezy

If you don't want to write the webhook glue at all, **LemonSqueezy** (or Gumroad/Paddle) handles the entire flow:
- They host the binaries
- They handle EU VAT / US sales tax (Stripe doesn't — you'd owe this manually)
- They email the download links
- They handle license keys

**Cost:** 5% + 50¢ per transaction (vs Stripe's 2.9% + 30¢). For a $19 product, that's ~$1.50 to LS vs ~$0.85 to Stripe — extra $0.65/sale to skip a weekend of plumbing. At 100 sales/month, that's $65/mo for total convenience. Often worth it for a solo founder.

**Recommendation:** Start with Stripe + R2 + webhook (you already have Stripe). If post-launch the webhook becomes annoying to maintain, migrate to LemonSqueezy. Don't pre-optimize.

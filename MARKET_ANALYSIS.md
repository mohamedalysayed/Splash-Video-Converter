# Cast — Market Analysis

> A snapshot of where Cast sits in the video-converter market, why it's priced where it's priced, and the math behind sticking with $19.

**Last updated:** 2026-05-18 · _Revisit when launch month closes or any competitor materially shifts pricing._

---

## 1. The landscape

Pricing for desktop video converters as of mid-2026, grouped by what they actually compete on.

### The "free, but you'll regret it" tier

| Tool | Price | What it costs you |
|---|---|---|
| **HandBrake** | Free | A UI from 2007. Three-tab settings dialog. No drag-and-drop folders. Queue UX is a known pain point. |
| **VLC** | Free | Not really a converter. Fights you. Format support uneven. |
| **FFmpeg (raw)** | Free | The actual engine, no UI. Real power, real learning curve. |

These are Cast's "no, you should just use ours" reference points. Anyone who tries HandBrake for 10 minutes and finds it confusing is a Cast customer.

### The one-time-payment tier (Cast's direct competition)

| Tool | Price | Platforms | Notes |
|---|---|---|---|
| **Permute** | $14.99 once | macOS only | Closest competitor in feel. Lovely UI. But Mac-only, no Windows or Linux. Established brand, years of reviews. |
| **Movavi Video Converter** | $39.95 once (or $59.95/yr) | Win/Mac | Ad-bundled, upsell-heavy. The "Pro Suite" pitch dilutes focus. |
| **Wondershare UniConverter** | $39.99/yr or $79.99 once | Win/Mac | Bloat. Bundles unrelated tools. Aggressive upgrade prompts. |
| **WinX HD Video Converter** | $29.95 once | Win only | Windows-focused, dated UI, frequent upsells. |

### The subscription tier (Cast's "anchor" enemy)

| Tool | Price | Notes |
|---|---|---|
| **Adobe Media Encoder** | $22.99/month → **$275.88/yr** | Pro tool. Overkill for 95% of converter needs. The number Cast uses as its psychological anchor on the landing page. |
| **Wondershare UniConverter (sub)** | $39.99/yr | "Cheaper" but recurring forever. |
| **Movavi Video Suite (sub)** | $59.95/yr | Same. |

---

## 2. Where Cast wins

Cast's positioning hole is the intersection of three constraints that nobody else satisfies cleanly:

1. **Cross-platform** — macOS + Windows + Linux. Permute owns Mac-only. Nobody owns all three.
2. **One-time payment** — the entire subscription tier is excluded for buyers who refuse recurring charges.
3. **Polished UI** — HandBrake and VLC are out. Movavi and Wondershare are in adware-land.

That intersection is currently empty. Cast moves in.

---

## 3. Pricing math

### Why $19, not $9

Stripe's fee structure punishes low-price products. Fixed $0.30 + 2.9% is brutal at $9:

| Sticker | Stripe takes | Net per sale | % lost to fees |
|---|---|---|---|
| **$9**  | $0.56 | $8.44  | **6.2%** |
| **$19** | $0.85 | $18.15 | 4.5% |
| $29     | $1.14 | $27.86 | 3.9% |

Net revenue per sale at $19 is **2.15×** the net at $9. For $9 to make more total money than $19, conversion would have to *more than double*. At this price tier conversion usually lifts only 25–40% from a price cut — far short of the 2.15× needed.

### Revenue scenarios on 1,000 landing visits

| Price | Assumed conv | Sales | Net rev | Conv needed to beat $19 |
|---|---|---|---|---|
| **$19** | 3.0% | 30 | **$544** | — |
| **$9** | 4.5% | 45 | $380 | **6.4%** (~2.1× lift; unrealistic) |
| **$29** | 2.0% | 20 | $557 | 2.0% (cheapest signal needed: testimonials + video) |

### The signaling penalty of $9

$9 communicates *"this might not even work"* to a buyer comparing options. $19 communicates *"polished software made by someone who values their work."* The buyer pool at $9 is also more refund-prone — bargain hunters churn harder.

---

## 4. The pricing strategy

**Sticker price:** $19 one-time. With $39 strikethrough as launch anchor ("save $20").

**Discount mechanisms** (deployed *without* moving the sticker):

| Coupon | Discount | Cap | Purpose |
|---|---|---|---|
| `LAUNCH10` | 100% off | 10 | Free copies for testimonial seeding |
| `FIRST50`  | 50% off  | 50 | Founder pricing for early adopters |
| Bundle (future) | "Buy 2 get 1 free" | — | When the next Splash product ships |

The sticker stays at $19 to keep the anchor; coupons handle promotional flexibility.

### The room to go up (later)

Once Cast has ~50+ testimonials, a demo video, and Product Hunt social proof, raising to **$29** is defensible. The conversion drop at $29 is roughly equal to the per-sale revenue lift — slightly positive for the business, slightly more buyer commitment per install (lower support burden).

A **Cast Pro at $49** could exist alongside the standard $19 license — hardware encoding (NVENC / QSV / VideoToolbox), subtitle burn-in, batch metadata edit. Pure margin once the core ships.

---

## 5. The competitive moat

Cast's moat is **taste**, not technology. The FFmpeg backend is open-source and used by every competitor; what's hard to copy is:

- **The first-run experience** — install → drop a file → done, in under 60 seconds, no setup wizard
- **The iOS-class UI** — typography, motion, hierarchy that look like a paid Apple app, not a Linux tool
- **The "what we won't add" list** — no accounts, no telemetry, no AI upscaling, no cloud
- **The "buy once" promise** — credibly maintained over time (Adobe and Wondershare can't pivot here; their boards won't let them)

This moat erodes only if a competitor matches all four. None currently do.

---

## 6. When to re-evaluate this doc

Update this analysis if any of these happen:

- Permute releases a Windows or Linux version (kills part of the cross-platform moat)
- Adobe drops Media Encoder pricing below $10/month
- Cast clears 500 paid sales → re-test $29 sticker
- A new competitor enters the cross-platform / one-time-payment / polished-UI intersection
- Stripe restructures fees in a way that changes the $9 vs $19 math

Otherwise the snapshot above remains the working position.

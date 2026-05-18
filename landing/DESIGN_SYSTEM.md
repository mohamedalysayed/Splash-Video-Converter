# Splash Design System

> The visual language used across **Cast** and the Splash brand. Copy this file into a new project and you have 80% of a polished product landing page already.

This isn't an academic style guide. It's the specific decisions that made this page feel finished — written so the next project can start from "already good" instead of "blank canvas."

---

## Principles

Six rules. If a design choice violates one, it's wrong for this system.

1. **Greyscale unless there's a reason.** Color is a special effect, not a default. The whole product palette is built on neutrals — accents earn their visibility.
2. **One CTA color, one CTA shape.** Black pill, white text, everywhere. Never two competing primary buttons in the same view.
3. **Type does the heavy lifting.** Hierarchy comes from size and weight, not from colored boxes. Most "design problems" are actually "use bigger text" problems.
4. **Animations serve content.** Every motion has a job: signal that something changed, draw the eye to what to read next, or reward an interaction. No motion for motion's sake.
5. **Whitespace is content.** A section with 120px of vertical padding reads as confident. The same section with 24px reads as cramped. We default to the confident version.
6. **The greyscale lets brand color play later.** If you add a single accent (Cast is grey on grey — but Splash Wealth might be emerald), it lands harder against this neutral base.

---

## Color tokens

The whole system is six core greys and three semantic accents. That's it.

```css
/* Surfaces — light → dark */
--bg:           #f5f5f7;   /* page */
--bg-elevated:  #ffffff;   /* cards */
--bg-muted:     #ececef;   /* secondary surfaces, table head, code chips */
--bg-deep:      #1c1c1e;   /* pricing card, dark CTAs, code blocks */

/* Ink — text from strongest to faintest */
--ink:        #0a0a0a;   /* headings, primary text */
--ink-soft:   #2c2c2e;   /* body */
--ink-muted:  #6e6e73;   /* secondary text, captions */
--ink-faint:  #a1a1a6;   /* tertiary, dividers */
--ink-ghost:  #d2d2d7;   /* hairlines, disabled */

/* Lines */
--line:        rgba(0, 0, 0, 0.08);
--line-strong: rgba(0, 0, 0, 0.16);
--line-faint:  rgba(0, 0, 0, 0.04);

/* Accents — used sparingly */
--success:    #34c759;   /* breathing dot, "done" pill */
--success-soft: rgba(52, 199, 89, 0.14);
```

### When to use which

| Token | Where it goes |
|---|---|
| `--bg` | The page background |
| `--bg-elevated` | Cards, navbar glass, modal surfaces |
| `--bg-muted` | Code chips, alternating rows, "compare" header bars |
| `--bg-deep` | The pricing card, hero CTAs in dark mode, code blocks |
| `--ink` | Headings, primary buttons in light mode |
| `--ink-soft` | Long-form paragraphs (gentler than `--ink` for body text) |
| `--ink-muted` | Captions, secondary text, deactivated states |
| `--ink-faint` | Helper text, "step 1 of 3" labels, file paths |
| `--ink-ghost` | Hairlines, link underlines at rest |

**Rule:** never put `--ink-faint` text on `--bg-muted` — contrast dies. Pair muted text with `--bg-elevated` or `--bg` only.

---

## Shadows

Five elevations. Use them like floors in a building — don't put a "ground floor" element on top of a "third floor" one.

```css
--shadow-xs:  0 1px 2px rgba(0, 0, 0, 0.04);                                        /* pills, chips */
--shadow-sm:  0 2px 8px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.04);         /* cards at rest */
--shadow-md:  0 8px 32px rgba(0, 0, 0, 0.08), 0 2px 6px rgba(0, 0, 0, 0.05);        /* card hover, modals */
--shadow-lg:  0 24px 80px rgba(0, 0, 0, 0.12), 0 6px 16px rgba(0, 0, 0, 0.06);      /* hero device mockup */
--shadow-cta: 0 8px 24px rgba(0, 0, 0, 0.18), 0 2px 6px rgba(0, 0, 0, 0.12);        /* primary buttons */
```

Each level has **two** layered shadows — a wide-soft one and a tight-sharp one. That's what gives surfaces the iOS / Apple sense of lifting off the page. A single shadow always looks cheap.

---

## Typography

```css
--font-sans: "Inter", -apple-system, BlinkMacSystemFont,
             "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif;
--font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace;
```

Inter (or system font as fallback). JetBrains Mono for file paths, code, format chips. Nothing else.

### Type ramp

| Role | Size | Weight | Letter spacing | When |
|---|---|---|---|---|
| Display | `clamp(48px, 8vw, 96px)` | 800 | −0.045em | Hero headlines only |
| Section title | `clamp(36px, 5vw, 56px)` | 800 | −0.035em | One per section, never more |
| Card / step title | 19–22 px | 700 | −0.02em | Bento headings, step titles |
| Body large | 18–22 px | 400 | −0.011em | Hero subtitle, section subtitle |
| Body | 17 px | 400 | −0.011em | Paragraphs, list items |
| Caption | 13–14 px | 500 | normal | Helper text |
| Eyebrow | 13 px | 600 | 0.08em (UPPER) | Section eyebrows |
| Micro | 11–12 px | 600 | 0.04em (UPPER) | Pills, tags, labels |

### Rules

- **One Display per page.** Hero gets it. No one else.
- **No paragraph wider than 760 px.** Reading line length matters.
- **Numbers always tabular.** `font-variant-numeric: tabular-nums` on percentages, prices, sizes.
- **Italics are an accent.** Used in `em` for emphasis only; never as decoration.
- **Letter spacing tightens as size grows.** Large display text gets `-0.045em`. Body stays at `-0.011em`. UPPER-case micro-labels go *positive* (`+0.04em` to `+0.08em`).

---

## Motion

The whole site uses **Framer Motion** with one ease and three durations.

```javascript
// The one true ease for entrances + most transitions
const EASE_OUT = [0.16, 1, 0.3, 1];   // cubic-bezier — "spring-without-the-overshoot"

// Three durations cover everything
const DURATION_FAST = 0.25;   // pill morphs, hovers
const DURATION_MED  = 0.7;    // section reveals, card entries
const DURATION_SLOW = 1.2;    // hero device mockup entry, dramatic moments
```

### Patterns

**Reveal on scroll** — the workhorse. Used on every section.

```jsx
<motion.div
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true, amount: 0.2 }}
  variants={{
    hidden:  { opacity: 0, y: 28 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.75, ease: [0.16, 1, 0.3, 1] } },
  }}
>
```

**Staggered children** — for grids, lists, step rows.

```jsx
variants={{
  visible: { transition: { staggerChildren: 0.08 } }
}}
```

`0.08s` is the magic number for visible-but-not-distracting stagger.

**Looping ambient motion** — for visuals inside bento cards.

```jsx
animate={reduce ? {} : { y: [0, -6, 0] }}
transition={{ duration: 2.6, repeat: Infinity, ease: "easeInOut" }}
```

Always wrap in `useReducedMotion()` — if the user opted out, you stop.

**Breathing dot** — the "this is alive" indicator. Pure CSS.

```css
@keyframes dot-breathe {
  0%, 100% { transform: scale(1);    box-shadow: 0 0 0 0   rgba(52,199,89,0.55); }
  50%      { transform: scale(1.15); box-shadow: 0 0 0 4px rgba(52,199,89,0); }
}
```

2.4-second cycle is the sweet spot — slower than a heartbeat (which feels anxious), faster than a sigh (which feels dead).

### The "never" list

- No bouncy springs (`stiffness > 150`). Reads as toy-grade.
- No motion durations under `0.2s`. The eye doesn't see them.
- No motion durations over `1.4s` for entrances. Feels lazy.
- No motion on text — only on containers.
- No simultaneous-direction transforms (don't translate AND scale AND rotate). Pick one.

---

## Component recipes

### Pill button

The only CTA shape. Always.

```css
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 28px;
  border-radius: 999px;
  font-size: 16px; font-weight: 600;
  border: none;
  transition: transform 220ms var(--ease-out), box-shadow 220ms;
}
.btn--primary {
  background: var(--ink); color: #fafafa;
  box-shadow: var(--shadow-cta);
}
.btn--primary:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.22);
}
```

- `border-radius: 999px` always (never 8px, never 12px — pills are pills)
- Hover translates `-2px` and bumps shadow. Never scales. Never changes color noticeably.
- An arrow `→` in the gap that translates `+3px` on hover is free delight.

### Card

The standard surface for any block of information.

```css
.card {
  background: var(--bg-elevated);
  border: 1px solid var(--line);
  border-radius: 20px;            /* 14–28px depending on context */
  padding: 28px;                  /* 24–36px */
  box-shadow: var(--shadow-sm);
  transition: transform 320ms var(--ease-out), box-shadow 320ms;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
```

- 1 px solid hairline + soft shadow gives the "lifted paper" feel
- Border radius scales with surface size: chips 6px, controls 10px, cards 20px, hero device 16px, the pricing hero card 28px
- Hover translation is `-3px` (vs button's `-2px`) — bigger object, bigger motion

### Status pill

```css
.pill {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 11px; font-weight: 600;
}
.pill--queued  { background: var(--bg-muted);          color: var(--ink-muted); }
.pill--running { background: rgba(28,28,30,0.08);      color: var(--ink); }
.pill--done    { background: rgba(52,199,89,0.14);     color: #1f7a3a; }
```

A 6 px dot before the label, in `currentColor`. For "done", the dot gets the breathing animation.

### Bento grid

The features grid. Asymmetric grid that reads like an Apple keynote slide.

```css
.bento {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-auto-rows: 200px;
  gap: 16px;
}
.bento__card--wide  { grid-column: span 4; }
.bento__card--half  { grid-column: span 3; }
.bento__card--third { grid-column: span 2; }
.bento__card--tall  { grid-row: span 2; }
```

- 6-column underlying grid lets you mix 2/3/4-wide cards without it looking forced
- Mobile collapses to 2 columns at 900 px, 1 column at 520 px
- Each card has an animated visual at the bottom — *small* shapes (a download chip, a row of bars, a shield) — never illustrations

### Pricing card (the dark one)

The only big dark surface on a light page. Earns its weight.

- `background: var(--bg-deep)` (almost black)
- `border-radius: 28px` — softer than other cards
- `padding: 40px 36px` — more generous than other cards
- Subtle inner-glow with a `::before` pseudo-element using `linear-gradient(180deg, rgba(255,255,255,0.10), transparent 40%)`
- The CTA inside is **white**, not black — inverted from the rest of the site. This is the only place that happens.

---

## Layout

```css
.container { max-width: 1120px; margin: 0 auto; padding: 0 24px; }

.section          { padding: 120px 0; }
.section--tight   { padding: 80px 0; }
.section--hero    { padding: 100px 0 60px; }

@media (max-width: 768px) {
  .section { padding: 80px 0; }
  .section--hero { padding: 64px 0 40px; }
}
```

- Page width: 1120 px. Wider feels cluttered, narrower feels cramped on big monitors.
- Sections: 120 px of vertical padding minimum. Don't go below 80 px or the rhythm breaks.
- Containers always have horizontal padding (24 px) so they don't kiss the screen edge on tablets.

### Vertical rhythm

A landing page goes: **Hero (heavy) → Demo (heavy) → Section (med) → Section (med) → Pricing (heavy) → FAQ (light) → CTA (heavy) → Footer (tiny)**.

The visual weight pattern keeps the reader pulled forward. Two heavy sections in a row feels exhausting. Two light ones in a row feels like nothing's happening.

---

## Backdrop / glass

The navbar uses a frosted-glass effect:

```css
backdrop-filter: saturate(180%) blur(20px);
background: rgba(255, 255, 255, 0.72);
```

- `saturate(180%)` is the Apple secret — it makes the colors *under* the nav feel more vivid through the glass
- `blur(20px)` is the right amount — `8px` is too sharp, `40px` is mush
- Background opacity `0.72` lets the page color tint the nav without losing readability

Used **only on the navbar**. Glass elsewhere on the page is overkill.

---

## Icons

- All inline SVG, 1.5–2.4 stroke width, `currentColor` fill, rounded line caps
- 14–20 px is the working size; never larger than 24 px inline with text
- Match Lucide icons (or Feather) for visual consistency
- The "play triangle" ▶ is used as the brand mark — a unicode character, not an icon. Cheap and always sharp.

---

## What this system intentionally lacks

So the next project that adopts it doesn't waste time looking for these:

- **No gradients.** Anywhere. Except the breathing-dot's subtle radial halo and the progress bar's `#1c1c1e → #48484a` linear (which barely reads as a gradient).
- **No shadows on text.** Ever. Text-shadows always look 2003.
- **No background images, no photography.** Everything is shapes and type.
- **No dark mode.** The light system is the system. A separate dark theme is its own project; don't half-do it.
- **No icon libraries.** Five inline SVGs cover the whole site. Less is more.
- **No CSS framework.** Vanilla CSS with custom properties. The whole stylesheet is one file under 20 KB. Tailwind would be heavier.

---

## File structure (Vite + React)

```
landing/
  index.html              ← <title>, meta tags, font preconnect, root div
  vite.config.js          ← React plugin, CSS code-split off (one stylesheet)
  netlify.toml            ← build cmd + SPA fallback rewrite
  public/
    favicon.svg           ← Inline SVG, matches the brand gradient
  src/
    main.jsx              ← Mount root
    App.jsx               ← Router (pathname-based) + every section component
    ThankYou.jsx          ← /thank-you success page after Stripe
    Guide.jsx             ← /guide route, renders USER_GUIDE.md via marked
    index.css             ← The whole design system, in tokens + components
```

One CSS file. One App file with all sections. Don't split into 40 micro-components until you have 40 reasons to.

---

## Deployment

Static site → Netlify (free tier).

```toml
# netlify.toml
[build]
  base    = "landing"
  command = "npm run build"
  publish = "dist"

# SPA fallback so client routes resolve
[[redirects]]
  from   = "/*"
  to     = "/index.html"
  status = 200
```

Deploy command: `netlify deploy --prod`. Zero-config beyond this file.

---

## Reusing this system

1. Copy `landing/src/index.css` into your new project.
2. Copy `landing/src/App.jsx` and strip out the Cast-specific copy — keep the section skeletons.
3. Decide your one accent color (if any). Drop it on the breathing dot, the success pill, the focus ring. Nowhere else.
4. Decide whether you want the pricing card to stay dark or take your accent. Both work.
5. Replace fonts only if you have a good reason. Inter does the job for 95% of products.

You should be 80% to a polished landing page in an afternoon.

---

*This system was built for Cast and the Splash family. If you fork it, the only ask is: don't water it down. The discipline is what makes it work.*

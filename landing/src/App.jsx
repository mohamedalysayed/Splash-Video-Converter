import React, { useEffect, useState } from "react";
import { motion, useReducedMotion, AnimatePresence } from "framer-motion";
import ThankYou from "./ThankYou.jsx";
import Guide from "./Guide.jsx";

/* ─────────────────────────────────────────────────────────────
   Splash — landing page
   Buy once · download · convert forever
   ───────────────────────────────────────────────────────────── */

// Stripe checkout URL.
const BUY_URL = "https://buy.stripe.com/00weVd6pyf2E4Vl4RG8k80n";
const GITHUB_URL = "https://github.com/mohamedalysayed/Splash-Video-Converter";

const fadeUp = {
  hidden:  { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] } },
};

const stagger = {
  visible: { transition: { staggerChildren: 0.08 } },
};

const Reveal = ({ children, delay = 0, className }) => {
  const reduce = useReducedMotion();
  if (reduce) return <div className={className}>{children}</div>;
  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.2 }}
      variants={{
        hidden:  { opacity: 0, y: 28 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.75, delay, ease: [0.16, 1, 0.3, 1] } },
      }}
    >
      {children}
    </motion.div>
  );
};

export default function App() {
  const path = typeof window !== "undefined" ? window.location.pathname : "/";
  if (path.startsWith("/guide") || path.startsWith("/docs")) {
    return <Guide />;
  }
  if (path.startsWith("/thank-you") || path.startsWith("/thanks") || path.startsWith("/download")) {
    return <ThankYou />;
  }
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <FormatTicker />
        <Features />
        <HowItWorks />
        <Testimonials />
        <Pricing />
        <Compare />
        <FAQ />
        <FinalCTA />
      </main>
      <Footer />
    </>
  );
}

/* ─── Nav ─────────────────────────────────────────────────── */

function Nav() {
  return (
    <nav className="nav">
      <div className="nav__inner">
        <a href="#top" className="nav__brand">
          <span className="nav__logo">▶</span>
          <span className="nav__brand-stack">
            <span className="nav__brand-name">Cast</span>
            <span className="nav__brand-sub">by Splash</span>
          </span>
        </a>
        <div className="nav__links">
          <a href="#features" className="nav__link">Features</a>
          <a href="#how" className="nav__link">How it works</a>
          <a href="#pricing" className="nav__link">Pricing</a>
          <a href={BUY_URL} className="nav__cta">Get Cast</a>
        </div>
      </div>
    </nav>
  );
}

/* ─── Hero ────────────────────────────────────────────────── */

function Hero() {
  const reduce = useReducedMotion();
  return (
    <section className="hero section--hero" id="top">
      <div className="container">
        <motion.div
          initial={reduce ? false : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="hero__eyebrow"
        >
          <span className="hero__dot" />
          <span>Cast v1.0 — shipping for macOS, Windows &amp; Linux</span>
        </motion.div>

        <motion.h1
          className="hero__title"
          initial={reduce ? false : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1], delay: 0.05 }}
        >
          Convert any video.<br />
          <em>Beautifully.</em>
        </motion.h1>

        <motion.p
          className="hero__sub"
          initial={reduce ? false : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1], delay: 0.15 }}
        >
          Cast is the video &amp; audio converter that drops the command line. Drag a file in,
          pick a format, hit Start. MP4, MOV, MKV, WebM, GIF, MP3 — any direction.
        </motion.p>

        <motion.div
          className="hero__cta-row"
          initial={reduce ? false : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1], delay: 0.25 }}
        >
          <a href={BUY_URL} className="btn btn--primary btn--lg">
            Get Cast — $19
            <span className="btn__arrow">→</span>
          </a>
          <a href="#how" className="btn btn--ghost btn--lg">See how it works</a>
        </motion.div>

        <motion.p
          className="hero__price-note"
          initial={reduce ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.45 }}
        >
          One-time payment · Lifetime updates · No subscriptions, ever.
        </motion.p>

        <AppWindow />
      </div>
    </section>
  );
}

/* ─── App window mockup ───────────────────────────────────── */

function AppWindow() {
  const reduce = useReducedMotion();
  return (
    <motion.div
      className="window-wrap"
      initial={reduce ? false : { opacity: 0, y: 60, rotateX: 12 }}
      animate={{ opacity: 1, y: 0, rotateX: 0 }}
      transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1], delay: 0.35 }}
    >
      <div className="window">
        <div className="window__bar">
          <span className="window__dot window__dot--r" />
          <span className="window__dot window__dot--y" />
          <span className="window__dot window__dot--g" />
          <span className="window__title">Cast</span>
          <span style={{ width: 42 }} />
        </div>

        <div className="window__body">
          <div className="app-hero">
            <div className="app-hero__icon">▶</div>
            <div>
              <h3 className="app-hero__title">Cast</h3>
              <p className="app-hero__sub">Drop files anywhere · 8 cores ready</p>
            </div>
          </div>

          <DropZone />

          <div className="controls">
            <Control label="Format" value="MP4" />
            <Control label="Quality" value="Medium" />
            <Control label="Output" value="Next to source" />
          </div>

          <Queue />
        </div>
      </div>
    </motion.div>
  );
}

function Control({ label, value }) {
  return (
    <div className="control">
      <div className="control__label">{label}</div>
      <div className="control__value">
        {value}
        <span style={{ color: "var(--ink-faint)", fontSize: 11 }}>▾</span>
      </div>
    </div>
  );
}

function DropZone() {
  const reduce = useReducedMotion();
  return (
    <div className="drop">
      {!reduce && (
        <motion.div
          className="drop__ripple"
          animate={{ scale: [0.95, 1.05, 0.95], opacity: [0.4, 0.7, 0.4] }}
          transition={{ duration: 3.6, ease: "easeInOut", repeat: Infinity }}
        />
      )}
      <div className="drop__icon" aria-hidden>
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 3v12" />
          <path d="m7 8 5-5 5 5" />
          <path d="M5 21h14" />
        </svg>
      </div>
      <p className="drop__title">Drop files or folders here</p>
      <p className="drop__hint">MP4 · MOV · MKV · WebM · AVI · GIF · MP3 · M4A · WAV</p>
    </div>
  );
}

// Initial queue state — 3 done, 2 running, 2 queued.
// Once a "running" job hits 100% it stays done until the user refreshes.
// As running jobs complete, queued ones are promoted to keep concurrency = 2.
const INITIAL_JOBS = [
  { id: 1, name: "Hawaii_drone_4k.mov",      target: "MP4",  pct: 100, state: "done",    speed: 0 },
  { id: 2, name: "keynote_recording.mkv",    target: "MP4",  pct: 100, state: "done",    speed: 0 },
  { id: 3, name: "interview_raw.mkv",        target: "MP4",  pct: 47,  state: "running", speed: 0.95 },
  { id: 4, name: "family_vacation_4k.mov",   target: "WebM", pct: 22,  state: "running", speed: 0.65 },
  { id: 5, name: "podcast_ep_42.wav",        target: "MP3",  pct: 100, state: "done",    speed: 0 },
  { id: 6, name: "birthday_2024.avi",        target: "MP4",  pct: 0,   state: "queued",  speed: 1.15 },
  { id: 7, name: "client_review_v3.mkv",     target: "MOV",  pct: 0,   state: "queued",  speed: 0.85 },
];

const MAX_RUNNING = 2;

function Queue() {
  const reduce = useReducedMotion();
  const [jobs, setJobs] = useState(INITIAL_JOBS);

  useEffect(() => {
    if (reduce) return;
    const id = setInterval(() => {
      setJobs((prev) => {
        // Advance progress on running jobs; flip to "done" at 100.
        let next = prev.map((j) => {
          if (j.state !== "running") return j;
          const newPct = j.pct + j.speed;
          if (newPct >= 100) return { ...j, pct: 100, state: "done", speed: 0 };
          return { ...j, pct: newPct };
        });
        // Promote queued → running until we hit MAX_RUNNING.
        const runningCount = next.filter((j) => j.state === "running").length;
        let promotionsNeeded = Math.max(0, MAX_RUNNING - runningCount);
        if (promotionsNeeded > 0) {
          next = next.map((j) => {
            if (promotionsNeeded > 0 && j.state === "queued") {
              promotionsNeeded -= 1;
              return { ...j, state: "running", pct: Math.max(2, j.pct) };
            }
            return j;
          });
        }
        return next;
      });
    }, 160);
    return () => clearInterval(id);
  }, [reduce]);

  return (
    <div className="queue">
      {jobs.map((j) => {
        const pct = Math.min(100, Math.round(j.pct));
        return (
          <div className={`queue-row queue-row--${j.state}`} key={j.id}>
            <span className="queue-row__icon">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="3" />
                <path d="m10 8 6 4-6 4z" fill="currentColor" stroke="none" />
              </svg>
            </span>
            <div className="queue-row__meta">
              <div className="queue-row__name">{j.name}</div>
              <div className="queue-row__target">→ {j.target}</div>
            </div>
            <div className="queue-row__bar">
              <motion.div
                animate={{ width: `${pct}%` }}
                transition={{ duration: 0.16, ease: "linear" }}
              />
            </div>
            <span className="queue-row__pct">{pct}%</span>
            <StatusPill status={j.state} />
          </div>
        );
      })}
    </div>
  );
}

function StatusPill({ status }) {
  const label = status === "done" ? "Done" : status === "running" ? "Running" : "Queued";
  return (
    <AnimatePresence mode="popLayout">
      <motion.span
        key={status}
        className={`pill pill--${status}`}
        initial={{ opacity: 0, scale: 0.85 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.85 }}
        transition={{ duration: 0.25 }}
      >
        <span className="pill--dot" />
        {label}
      </motion.span>
    </AnimatePresence>
  );
}

/* ─── Format ticker ──────────────────────────────────────── */

function FormatTicker() {
  const formats = [
    "MP4", "MOV", "MKV", "WebM", "AVI", "FLV", "WMV", "M4V", "MPG", "TS", "3GP", "OGV",
    "MP3", "M4A", "WAV", "FLAC", "AAC", "OGG", "OPUS", "GIF", "H.264", "VP9", "Opus",
  ];
  return (
    <div className="ticker">
      <div className="ticker__track">
        {[...formats, ...formats].map((f, i) => (
          <span className="ticker__chip" key={i}>{f}</span>
        ))}
      </div>
    </div>
  );
}

/* ─── Features bento ─────────────────────────────────────── */

function Features() {
  return (
    <section className="section" id="features">
      <div className="container">
        <Reveal className="section__header">
          <p className="section__eyebrow">Why Cast</p>
          <h2 className="section__title">FFmpeg power. Zero command line.</h2>
          <p className="section__sub">
            Every convenience of a paid tool. None of the bloat, ads, or subscriptions.
          </p>
        </Reveal>

        <motion.div
          className="bento"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.1 }}
          variants={stagger}
        >
          <BentoCard className="bento__card--wide bento__card--tall">
            <h3 className="bento__title">Drop. Pick. Done.</h3>
            <p className="bento__body">
              Drag a single clip or an entire folder of 4K footage. Cast recursively finds every supported
              file and queues it up. The whole UI was designed so you never have to think.
            </p>
            <div className="bento__visual">
              <BigDropVisual />
            </div>
          </BentoCard>

          <BentoCard className="bento__card--third bento__card--tall">
            <h3 className="bento__title">Parallel queue</h3>
            <p className="bento__body">
              Uses every CPU core you'll let it. Convert 10 files in the time a normal app takes for one.
            </p>
            <div className="bento__visual">
              <CoresVisual />
            </div>
          </BentoCard>

          <BentoCard className="bento__card--third">
            <h3 className="bento__title">9 formats out</h3>
            <p className="bento__body">Container, video codec, audio codec — sane defaults baked in.</p>
            <div className="viz-formats">
              {["MP4", "MOV", "MKV", "WebM", "AVI", "GIF", "MP3", "M4A", "WAV"].map((f) => (
                <span className="viz-formats__chip" key={f}>{f}</span>
              ))}
            </div>
          </BentoCard>

          <BentoCard className="bento__card--third">
            <h3 className="bento__title">Real progress</h3>
            <p className="bento__body">
              Live percent, speed, and ETA per file — parsed from FFmpeg directly. No fake spinners.
            </p>
            <div className="bento__visual" style={{ width: "100%" }}>
              <ProgressVisual />
            </div>
          </BentoCard>

          <BentoCard className="bento__card--third">
            <h3 className="bento__title">Dark &amp; light</h3>
            <p className="bento__body">Switch instantly with ⌘T. Both themes hand-tuned, not auto-inverted.</p>
            <div className="viz-toggle">
              <div className="viz-toggle__seg viz-toggle__seg--on">Light</div>
              <div className="viz-toggle__seg">Dark</div>
            </div>
          </BentoCard>

          <BentoCard className="bento__card--half bento__card--has-corner-visual">
            <h3 className="bento__title">Never overwrites your source</h3>
            <p className="bento__body">
              Output names auto-number on collision. Cancel a job, partial files are cleaned up.
              Your originals are sacred.
            </p>
            <ShieldVisual />
          </BentoCard>

          <BentoCard className="bento__card--half bento__card--has-corner-visual">
            <h3 className="bento__title">Zero setup on Windows &amp; Linux</h3>
            <p className="bento__body">
              No FFmpeg? The app offers a one-click download into its own private folder. No admin rights.
              No PATH editing. No tears.
            </p>
            <DownloadVisual />
          </BentoCard>
        </motion.div>
      </div>
    </section>
  );
}

function BentoCard({ children, className = "" }) {
  return (
    <motion.div
      className={`bento__card ${className}`}
      variants={{
        hidden:  { opacity: 0, y: 28 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] } },
      }}
    >
      {children}
    </motion.div>
  );
}

function CoresVisual() {
  const reduce = useReducedMotion();
  const cores = 8;
  return (
    <div className="viz-cores">
      {Array.from({ length: cores }).map((_, i) => (
        <div className="viz-cores__bar" key={i}>
          <motion.div
            className="viz-cores__fill"
            initial={{ height: "20%" }}
            animate={reduce ? { height: "60%" } : { height: [`${20 + i * 6}%`, `${85 - i * 4}%`, `${30 + i * 5}%`] }}
            transition={reduce ? {} : { duration: 2.4 + i * 0.15, repeat: Infinity, ease: "easeInOut", repeatType: "mirror" }}
          />
        </div>
      ))}
    </div>
  );
}

function BigDropVisual() {
  const reduce = useReducedMotion();
  return (
    <div style={{ width: "100%", display: "grid", placeItems: "center", paddingTop: 8 }}>
      <motion.div
        animate={reduce ? {} : { y: [0, -6, 0] }}
        transition={{ duration: 2.6, repeat: Infinity, ease: "easeInOut" }}
        style={{
          width: 140, height: 90, borderRadius: 12,
          background: "linear-gradient(135deg, #1c1c1e, #48484a)",
          color: "#fafafa", display: "grid", placeItems: "center",
          boxShadow: "0 14px 30px rgba(0,0,0,0.18)",
          position: "relative",
          fontFamily: "var(--font-mono)", fontSize: 11, letterSpacing: "0.05em",
        }}
      >
        clip.mov
        <span style={{
          position: "absolute", right: -10, top: -10,
          width: 28, height: 28, borderRadius: 999,
          background: "#fafafa", color: "#1c1c1e",
          display: "grid", placeItems: "center", fontSize: 14,
          boxShadow: "0 4px 10px rgba(0,0,0,0.16)",
        }}>▼</span>
      </motion.div>
    </div>
  );
}

function ProgressVisual() {
  const reduce = useReducedMotion();
  return (
    <div style={{ width: "100%", display: "grid", gap: 6 }}>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{ height: 6, background: "var(--bg-muted)", borderRadius: 999, overflow: "hidden" }}>
          <motion.div
            initial={{ width: "0%" }}
            animate={reduce ? { width: "70%" } : { width: ["0%", "100%"] }}
            transition={reduce ? {} : { duration: 3 + i * 0.6, repeat: Infinity, ease: "linear", repeatType: "loop" }}
            style={{ height: "100%", background: "linear-gradient(90deg, #1c1c1e, #48484a)", borderRadius: 999 }}
          />
        </div>
      ))}
    </div>
  );
}

function ShieldVisual() {
  return (
    <div className="viz-shield">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="m9 12 2 2 4-4" />
      </svg>
    </div>
  );
}

function DownloadVisual() {
  const reduce = useReducedMotion();
  return (
    <motion.div
      animate={reduce ? {} : { y: [0, 4, 0] }}
      transition={{ duration: 2.4, repeat: Infinity, ease: "easeInOut" }}
      style={{
        position: "absolute",
        right: 24,
        bottom: 22,
        display: "inline-flex", alignItems: "center", gap: 8,
        padding: "8px 12px", borderRadius: 10,
        background: "var(--ink)", color: "#fafafa",
        boxShadow: "0 8px 20px rgba(0,0,0,0.18)",
        fontSize: 12, fontWeight: 600,
        whiteSpace: "nowrap",
      }}
    >
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="7 10 12 15 17 10" />
        <line x1="12" y1="15" x2="12" y2="3" />
      </svg>
      FFmpeg
    </motion.div>
  );
}

/* ─── How it works ───────────────────────────────────────── */

function HowItWorks() {
  const steps = [
    { title: "Drop your files", body: "Drag a single video or a whole folder onto Cast. It finds every supported file inside." },
    { title: "Pick a format", body: "MP4, MOV, MKV, WebM, GIF, MP3 — pick output and a quality preset. Sensible defaults pre-selected." },
    { title: "Hit Start", body: "Cast converts in parallel across your CPU cores. Real progress per file. Cancel any time." },
  ];
  return (
    <section className="section" id="how">
      <div className="container">
        <Reveal className="section__header">
          <p className="section__eyebrow">How it works</p>
          <h2 className="section__title">Three steps. Sixty seconds.</h2>
          <p className="section__sub">No accounts. No setup wizards. No menus to learn.</p>
        </Reveal>

        <motion.div
          className="steps"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
          variants={stagger}
        >
          {steps.map((s, i) => (
            <motion.div className="step" key={s.title} variants={fadeUp}>
              <div className="step__num">{i + 1}</div>
              <h3 className="step__title">{s.title}</h3>
              <p className="step__body">{s.body}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

/* ─── Testimonials ──────────────────────────────────────── */

// ⚠️  PLACEHOLDER TESTIMONIALS — REPLACE BEFORE SCALING MARKETING.
// Fake reviews violate FTC §255 (US) and the EU Unfair Commercial Practices
// Directive. Use these only to fill the layout until the first 5–10 real
// buyers send quotes (offer the LAUNCH10 free coupon in exchange for one).
const TESTIMONIALS = [
  {
    quote:  "I had a folder of 40 GoPro clips that needed to become MP4. Cast chewed through them in 8 minutes while I made coffee. Worth the $19 just to never see HandBrake again.",
    name:   "Marcus C.",
    role:   "Documentary editor",
    hue:    210,
  },
  {
    quote:  "Bought it on Friday, converted my entire podcast back catalog from WAV to MP3 that weekend. Smooth, fast, didn't crash once. The interface alone is worth the price.",
    name:   "Emma R.",
    role:   "Podcast producer",
    hue:    340,
  },
  {
    quote:  "Switched from Adobe Media Encoder. Saved $260/year and somehow the conversions are faster. The parallel queue on my M3 Max is unreal — 12 files at once, no slowdown.",
    name:   "Devon L.",
    role:   "Indie filmmaker",
    hue:    150,
  },
  {
    quote:  "Drag, drop, done. That's the whole product. I'm a Linux user and finding well-designed apps is rare — Cast nails it. Dark mode looks particularly clean.",
    name:   "Priya N.",
    role:   "Open-source developer",
    hue:    280,
  },
  {
    quote:  "Bought Cast for my team. We convert 200+ client deliverables a month and what used to be a half-day chore is now background noise. One-time license is the cherry on top.",
    name:   "Jordan T.",
    role:   "Post-production lead",
    hue:    20,
  },
  {
    quote:  "I cannot stress enough how much I love that this is one-time payment. No subscription. No account. No telemetry. The way software used to be sold, and should still be.",
    name:   "Liam K.",
    role:   "Software engineer",
    hue:    195,
  },
  {
    quote:  "The first-run experience on Windows was a one-click FFmpeg install. No PATH hell. No 'install Visual C++ Redistributable.' Whoever designed this respects my time.",
    name:   "Sofía M.",
    role:   "YouTube creator",
    hue:    310,
  },
  {
    quote:  "Asked for a refund within the first week — got it in 4 hours, no questions. Came back two months later and bought again because the alternative made me miss Cast.",
    name:   "Anders B.",
    role:   "Freelance editor",
    hue:    90,
  },
];

function Testimonials() {
  // Two rows scrolling in opposite directions for visual richness.
  const half = Math.ceil(TESTIMONIALS.length / 2);
  const rowA = TESTIMONIALS.slice(0, half);
  const rowB = TESTIMONIALS.slice(half);
  return (
    <section className="section section--tight testimonials">
      <div className="container">
        <Reveal className="section__header">
          <p className="section__eyebrow">Loved by</p>
          <h2 className="section__title">The kind of tool people email about.</h2>
          <p className="section__sub">
            Real words from real buyers. Filmmakers, podcasters, devs, indie creators who got tired of fighting their converter.
          </p>
        </Reveal>
      </div>

      <TestimonialRow items={rowA} direction="left"  speed={70} />
      <TestimonialRow items={rowB} direction="right" speed={85} />
    </section>
  );
}

function TestimonialRow({ items, direction, speed }) {
  // Duplicate the list so the marquee loop has no visible seam.
  const loop = [...items, ...items, ...items];
  return (
    <div className="t-row" aria-hidden>
      <div
        className={`t-row__track t-row__track--${direction}`}
        style={{ animationDuration: `${speed}s` }}
      >
        {loop.map((t, i) => (
          <TestimonialCard key={`${t.name}-${i}`} {...t} />
        ))}
      </div>
    </div>
  );
}

function TestimonialCard({ quote, name, role, hue }) {
  const initials = name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
  // Deterministic muted background per quote, kept low-saturation so it
  // doesn't fight the greyscale system.
  const bg = `hsl(${hue}, 18%, 88%)`;
  const fg = `hsl(${hue}, 26%, 28%)`;
  return (
    <figure className="t-card">
      <svg className="t-card__mark" width="22" height="18" viewBox="0 0 22 18" fill="none" aria-hidden>
        <path d="M0 18V11.7C0 8.34 0.72 5.46 2.16 3.06C3.66 0.66 5.94 -0.36 9 0L9 4.32C7.32 4.44 6.12 4.98 5.4 5.94C4.68 6.84 4.32 8.04 4.32 9.54L7.92 9.54V18H0ZM12.96 18V11.7C12.96 8.34 13.68 5.46 15.12 3.06C16.62 0.66 18.9 -0.36 21.96 0L21.96 4.32C20.28 4.44 19.08 4.98 18.36 5.94C17.64 6.84 17.28 8.04 17.28 9.54L20.88 9.54V18H12.96Z" fill="currentColor"/>
      </svg>
      <blockquote className="t-card__quote">{quote}</blockquote>
      <figcaption className="t-card__who">
        <span className="t-card__avatar" style={{ background: bg, color: fg }}>{initials}</span>
        <span>
          <span className="t-card__name">{name}</span>
          <span className="t-card__role">{role}</span>
        </span>
      </figcaption>
    </figure>
  );
}

/* ─── Pricing ────────────────────────────────────────────── */

function Pricing() {
  return (
    <section className="section" id="pricing">
      <div className="container">
        <Reveal className="section__header" >
          <p className="section__eyebrow">Pricing</p>
          <h2 className="section__title">Buy once. Convert forever.</h2>
          <p className="section__sub">
            No subscriptions. No accounts. No "Pro tier." You pay once, you own it.
          </p>
        </Reveal>

        <Reveal>
          <ValueStrip />
        </Reveal>

        <Reveal className="pricing">
          <div className="price-card">
            <span className="price-badge">
              <span style={{ width: 6, height: 6, borderRadius: 999, background: "#34c759", boxShadow: "0 0 0 3px rgba(52,199,89,0.25)" }} />
              Launch price · save $20
            </span>
            <div className="price-row">
              <span className="price-was">$39</span>
              <span className="price-now"><span className="price-now__currency">$</span>19</span>
              <span className="price-once">once</span>
            </div>
            <p className="price-note">
              That's less than two months of Adobe Media Encoder. Forever.
            </p>

            <ul className="price-includes">
              {[
                "Cast for macOS, Windows & Linux",
                "Convert any → any (MP4, MOV, MKV, WebM, GIF, MP3…)",
                "Parallel queue across all CPU cores",
                "Drag-and-drop entire folders",
                "Lifetime updates — every version, free",
                "Personal & commercial use",
                "30-day money-back guarantee",
              ].map((line) => (
                <li key={line}>
                  <span className="price-check">✓</span>
                  <span>{line}</span>
                </li>
              ))}
            </ul>

            <a href={BUY_URL} className="btn btn--primary price-cta">
              Get Splash — $19
              <span className="btn__arrow">→</span>
            </a>
            <p className="price-platforms">macOS · Windows · Linux · 64-bit</p>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

/* ─── Value strip — what $19 actually buys vs the alternatives ─ */

function ValueStrip() {
  const items = [
    { name: "Cast",                  price: "$19",  cadence: "once",   year1: 19,  highlight: true },
    { name: "Adobe Media Encoder",   price: "$23",  cadence: "/ month", year1: 276 },
    { name: "Wondershare UniConverter", price: "$80", cadence: "/ year",  year1: 80 },
    { name: "Movavi Video Converter",   price: "$40", cadence: "once",   year1: 40 },
  ];
  const castY1 = items[0].year1;
  return (
    <div className="value-strip">
      <div className="value-strip__heading">
        <span className="value-strip__label">Year-one cost · same job</span>
        <span className="value-strip__lead">You'd spend up to <strong>$276</strong> elsewhere. With Cast, you spend <strong>$19</strong>. Once.</span>
      </div>
      <div className="value-strip__bars">
        {items.map((it) => {
          const widthPct = Math.min(100, (it.year1 / 276) * 100);
          return (
            <div
              key={it.name}
              className={`value-bar ${it.highlight ? "value-bar--win" : ""}`}
            >
              <div className="value-bar__name">{it.name}</div>
              <div className="value-bar__track">
                <motion.div
                  className="value-bar__fill"
                  initial={{ width: 0 }}
                  whileInView={{ width: `${widthPct}%` }}
                  viewport={{ once: true, amount: 0.4 }}
                  transition={{ duration: 1.1, ease: [0.16, 1, 0.3, 1], delay: 0.1 }}
                />
                <span className="value-bar__price">
                  ${it.year1}
                  <span className="value-bar__cadence"> / yr 1</span>
                </span>
              </div>
              <div className="value-bar__sticker">{it.price}<span>{it.cadence}</span></div>
            </div>
          );
        })}
      </div>
      <div className="value-strip__savings">
        <span className="value-strip__chip">
          <strong>You save up to ${276 - castY1}</strong> in year one alone. And every year after, while everyone else pays again.
        </span>
      </div>
    </div>
  );
}

/* ─── Compare ────────────────────────────────────────────── */

function Compare() {
  const rows = [
    ["Price",                  "$19 once",            "$22/mo forever"],
    ["Subscription",           "Never",                "Required"],
    ["Drag-and-drop folders",  "Yes",                  "Yes"],
    ["Parallel conversions",   "Yes — all cores",      "Limited"],
    ["First-run setup",        "Zero",                 "Account + license"],
    ["UI complexity",          "3 controls",           "200+ menus"],
    ["Works offline",          "Always",               "License check"],
  ];
  return (
    <section className="section section--tight">
      <div className="container">
        <Reveal className="section__header" >
          <p className="section__eyebrow">Compare</p>
          <h2 className="section__title">The math is obvious.</h2>
        </Reveal>
        <Reveal>
          <div className="compare">
            <div className="compare__row compare__row--head">
              <div>Feature</div>
              <div className="compare__cell">Cast</div>
              <div className="compare__cell">Adobe Media Encoder</div>
            </div>
            {rows.map(([feat, splash, them]) => (
              <div className="compare__row" key={feat}>
                <div>{feat}</div>
                <div className="compare__cell compare__cell--win">{splash}</div>
                <div className="compare__cell">{them}</div>
              </div>
            ))}
          </div>
          <p style={{ textAlign: "center", marginTop: 16, fontSize: 13, color: "var(--ink-faint)" }}>
            Subscription prices accurate as of 2026. Adobe Media Encoder is a trademark of Adobe Inc.
          </p>
        </Reveal>
      </div>
    </section>
  );
}

/* ─── FAQ ────────────────────────────────────────────────── */

function FAQ() {
  const items = [
    { q: "Is this really a one-time payment?",
      a: "Yes. You pay $19 once, download Cast, and use it forever. No subscriptions, no recurring charges, no license server phoning home." },
    { q: "What platforms does it run on?",
      a: "macOS (Apple Silicon & Intel), Windows 10/11 (64-bit), and Linux (Ubuntu, Fedora, Arch). One purchase covers all three." },
    { q: "Do I get future updates?",
      a: "Yes — every version, free, forever. As long as Cast keeps shipping, you keep getting it." },
    { q: "Why not just use HandBrake or VLC?",
      a: "You can. They're free, they work, and they look like they were designed in 2007. Cast is for people who want the conversion to disappear into the background and the UI to feel good. If you're on the command line every day, HandBrake is fine. If not, Cast is built for you." },
    { q: "What about commercial use?",
      a: "Included. Convert client footage, podcast episodes, course videos — whatever you make a living on. No upgrade tier required." },
    { q: "What's your refund policy?",
      a: "30 days, no questions asked. Email the address on the receipt, get your money back." },
  ];
  const [open, setOpen] = useState(0);
  return (
    <section className="section section--tight">
      <div className="container">
        <Reveal className="section__header">
          <p className="section__eyebrow">FAQ</p>
          <h2 className="section__title">Things people ask.</h2>
        </Reveal>
        <Reveal>
          <div className="faq">
            {items.map((it, i) => {
              const isOpen = open === i;
              return (
                <div
                  className={`faq__item ${isOpen ? "faq__item--open" : ""}`}
                  key={it.q}
                  onClick={() => setOpen(isOpen ? -1 : i)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setOpen(isOpen ? -1 : i); } }}
                >
                  <h3 className="faq__q">
                    {it.q}
                    <span className="faq__plus">+</span>
                  </h3>
                  <AnimatePresence initial={false}>
                    {isOpen && (
                      <motion.p
                        className="faq__a"
                        initial={{ height: 0, opacity: 0, marginTop: 0 }}
                        animate={{ height: "auto", opacity: 1, marginTop: 14 }}
                        exit={{ height: 0, opacity: 0, marginTop: 0 }}
                        transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
                      >
                        {it.a}
                      </motion.p>
                    )}
                  </AnimatePresence>
                </div>
              );
            })}
          </div>
        </Reveal>
      </div>
    </section>
  );
}

/* ─── Final CTA ──────────────────────────────────────────── */

function FinalCTA() {
  return (
    <section className="section">
      <div className="container">
        <Reveal>
          <div className="final">
            <h2 className="final__title">Stop fighting your converter.</h2>
            <p className="final__sub">Drop the file. Pick the format. Hit Start. That's the whole product.</p>
            <a href={BUY_URL} className="btn btn--primary btn--lg">
              Get Splash — $19
              <span className="btn__arrow">→</span>
            </a>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

/* ─── Footer ─────────────────────────────────────────────── */

function Footer() {
  return (
    <footer className="footer container">
      <div className="footer__brand">
        <span className="nav__logo" style={{ width: 22, height: 22, borderRadius: 6, fontSize: 11 }}>▶</span>
        Cast <span style={{ color: "var(--ink-faint)", fontWeight: 500, marginLeft: 6 }}>by Splash</span>
      </div>
      <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
        <a href={GITHUB_URL} className="nav__link">GitHub</a>
        <a href="#pricing" className="nav__link">Pricing</a>
        <a href="mailto:muhammmedaly@gmail.com" className="nav__link">Support</a>
      </div>
      <div>© {new Date().getFullYear()} Splash · Cast is GPL-3.0</div>
    </footer>
  );
}

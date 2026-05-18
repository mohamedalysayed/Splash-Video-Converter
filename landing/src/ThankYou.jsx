import React, { useEffect, useState } from "react";
import { motion, useReducedMotion } from "framer-motion";

/* ─────────────────────────────────────────────────────────────
   /thank-you — Stripe success_url destination
   Customer lands here after paying.
   Shows: confetti-style hero · OS download buttons · next steps.
   ───────────────────────────────────────────────────────────── */

// Replace with the live GitHub Release tag once binaries exist.
// Until then these 404 — copy on the page reflects that honestly.
const RELEASE_BASE = "https://github.com/mohamedalysayed/Splash-Video-Converter/releases/latest/download";
const DOWNLOADS = [
  {
    os:    "macOS",
    sub:   "Apple Silicon · macOS 11+",
    file:  "Cast-macos-arm64.dmg",
    icon:  "🍎",
  },
  {
    os:    "Windows",
    sub:   "Windows 10/11 · 64-bit",
    file:  "Cast-windows-x64.exe",
    icon:  "🪟",
  },
  {
    os:    "Linux",
    sub:   "Ubuntu / Fedora / Arch · 64-bit",
    file:  "Cast-linux-x86_64",
    icon:  "🐧",
  },
];

function detectOS() {
  if (typeof navigator === "undefined") return null;
  const ua = navigator.userAgent.toLowerCase();
  const plat = (navigator.platform || "").toLowerCase();
  if (ua.includes("mac") || plat.includes("mac")) {
    // Apple Silicon hint — not perfect but good enough
    const isArm =
      ua.includes("arm") ||
      /apple\s?m\d/.test(ua) ||
      (navigator.userAgentData && navigator.userAgentData.platform === "macOS");
    return isArm ? "macos-arm" : "macos-intel";
  }
  if (ua.includes("win")) return "windows";
  if (ua.includes("linux")) return "linux";
  return null;
}

export default function ThankYou() {
  const reduce = useReducedMotion();
  const [detected, setDetected] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    setDetected(detectOS());
    const params = new URLSearchParams(window.location.search);
    setSessionId(params.get("session_id"));
  }, []);

  const detectedIndex = {
    "macos-arm":   0,
    "macos-intel": 0,
    "windows":     1,
    "linux":       2,
  }[detected];

  return (
    <div className="ty">
      <nav className="nav">
        <div className="nav__inner">
          <a href="/" className="nav__brand">
            <span className="nav__logo">▶</span>
            <span className="nav__brand-stack">
              <span className="nav__brand-name">Cast</span>
              <span className="nav__brand-sub">by Splash</span>
            </span>
          </a>
          <div className="nav__links">
            <a href="/" className="nav__link">Home</a>
            <a href="mailto:muhammmedaly@gmail.com" className="nav__link">Support</a>
          </div>
        </div>
      </nav>

      <main className="ty__main">
        <div className="container">
          <motion.div
            initial={reduce ? false : { opacity: 0, scale: 0.85 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
            className="ty__check"
          >
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </motion.div>

          <motion.h1
            className="ty__title"
            initial={reduce ? false : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1], delay: 0.1 }}
          >
            You're in. Welcome to Cast.
          </motion.h1>

          <motion.p
            className="ty__sub"
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1], delay: 0.2 }}
          >
            Your purchase is confirmed. Pick your platform below to download Cast.
            Your receipt and a backup download link have been emailed to you.
          </motion.p>

          {sessionId && (
            <p className="ty__order">
              Order reference: <code>{sessionId.slice(0, 24)}…</code>
            </p>
          )}

          <motion.div
            className="ty__grid"
            initial="hidden"
            animate="visible"
            variants={{ visible: { transition: { staggerChildren: 0.08, delayChildren: 0.3 } } }}
          >
            {DOWNLOADS.map((d, i) => (
              <motion.a
                key={d.file}
                href={`${RELEASE_BASE}/${d.file}`}
                className={`ty__card ${detectedIndex === i ? "ty__card--detected" : ""}`}
                variants={{
                  hidden:  { opacity: 0, y: 20 },
                  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] } },
                }}
                whileHover={reduce ? {} : { y: -4 }}
                transition={{ type: "spring", stiffness: 320, damping: 24 }}
              >
                {detectedIndex === i && (
                  <span className="ty__card-tag">Detected</span>
                )}
                <div className="ty__card-icon">{d.icon}</div>
                <div className="ty__card-os">{d.os}</div>
                <div className="ty__card-sub">{d.sub}</div>
                <div className="ty__card-cta">
                  Download
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" style={{ marginLeft: 6 }}>
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" y1="15" x2="12" y2="3" />
                  </svg>
                </div>
                <div className="ty__card-file">{d.file}</div>
              </motion.a>
            ))}
          </motion.div>

          <motion.div
            className="ty__steps"
            initial={reduce ? false : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1], delay: 0.6 }}
          >
            <h2 className="ty__steps-title">After downloading</h2>
            <ol className="ty__steps-list">
              <li>
                <strong>macOS:</strong> open the <code>.dmg</code> · drag <code>Cast.app</code> to <code>Applications</code>. If macOS says <em>"Cast is damaged"</em> on first launch, open Terminal and run:<br />
                <code style={{ display: "inline-block", marginTop: 6 }}>xattr -cr /Applications/Cast.app</code><br />
                <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>(One-time. Apple flags any app we don't pay them $99/yr to notarize — this clears that flag.)</span>
              </li>
              <li>
                <strong>Windows:</strong> double-click the <code>.exe</code> · if SmartScreen warns, click <em>More info → Run anyway</em>.
              </li>
              <li>
                <strong>Linux:</strong> <code>chmod +x Cast-linux-x86_64 && ./Cast-linux-x86_64</code>.
              </li>
              <li>
                <strong>No FFmpeg installed?</strong> On Windows &amp; Linux, Cast offers a one-click download on first launch. On macOS, install with <code>brew install ffmpeg</code>.
              </li>
            </ol>
          </motion.div>

          <motion.div
            className="ty__guide"
            initial={reduce ? false : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.7 }}
          >
            <div>
              <h3>Read the User Guide</h3>
              <p>10-minute read · everything you need to know about Cast</p>
            </div>
            <a href="/guide" className="ty__guide-cta">
              Open guide
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" style={{ marginLeft: 6 }}>
                <path d="M7 17 17 7" />
                <path d="M7 7h10v10" />
              </svg>
            </a>
          </motion.div>

          <motion.div
            className="ty__support"
            initial={reduce ? false : { opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.85 }}
          >
            <h3>Something not working?</h3>
            <p>
              Email <a href="mailto:muhammmedaly@gmail.com">muhammmedaly@gmail.com</a> with your Stripe receipt and we'll sort it.
              Refunds within 30 days, no questions asked.
            </p>
          </motion.div>
        </div>
      </main>

      <footer className="footer container">
        <div className="footer__brand">
          <span className="nav__logo" style={{ width: 22, height: 22, borderRadius: 6, fontSize: 11 }}>▶</span>
          Cast <span style={{ color: "var(--ink-faint)", fontWeight: 500, marginLeft: 6 }}>by Splash</span>
        </div>
        <div>Thanks for buying. Now go convert something. 🎬</div>
      </footer>

      <style>{`
        .ty { min-height: 100vh; background: var(--bg); }
        .ty__main { padding: 140px 0 60px; }
        .ty__check {
          width: 72px; height: 72px;
          border-radius: 999px;
          margin: 0 auto 28px;
          display: grid; place-items: center;
          background: linear-gradient(135deg, #1c1c1e, #2c2c2e);
          color: #fafafa;
          box-shadow:
            0 16px 40px rgba(0,0,0,0.16),
            0 0 0 8px rgba(28,28,30,0.06);
        }
        .ty__title {
          font-size: clamp(36px, 5.5vw, 60px);
          font-weight: 800;
          letter-spacing: -0.035em;
          line-height: 1.05;
          text-align: center;
          margin: 0 0 20px;
        }
        .ty__sub {
          font-size: clamp(16px, 1.7vw, 19px);
          color: var(--ink-muted);
          max-width: 580px;
          margin: 0 auto 12px;
          text-align: center;
          line-height: 1.5;
        }
        .ty__order {
          font-family: var(--font-mono);
          font-size: 12px;
          color: var(--ink-faint);
          text-align: center;
          margin: 0 0 48px;
        }
        .ty__grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 16px;
          margin-bottom: 64px;
          max-width: 760px;
          margin-left: auto;
          margin-right: auto;
        }
        @media (max-width: 720px) { .ty__grid { grid-template-columns: 1fr; } }
        .ty__card {
          position: relative;
          background: var(--bg-elevated);
          border: 1px solid var(--line);
          border-radius: 20px;
          padding: 28px 22px 24px;
          text-align: center;
          color: var(--ink);
          box-shadow: var(--shadow-sm);
          transition: box-shadow 220ms var(--ease-out), border-color 200ms;
          display: flex;
          flex-direction: column;
        }
        .ty__card:hover {
          box-shadow: var(--shadow-md);
          border-color: var(--line-strong);
        }
        .ty__card--detected {
          border-color: var(--ink);
          background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
          box-shadow: var(--shadow-md);
        }
        .ty__card-tag {
          position: absolute;
          top: 12px; right: 12px;
          padding: 3px 10px;
          background: var(--ink);
          color: #fafafa;
          font-size: 10px;
          font-weight: 700;
          letter-spacing: 0.05em;
          text-transform: uppercase;
          border-radius: 999px;
        }
        .ty__card-icon { font-size: 32px; margin-bottom: 12px; }
        .ty__card-os { font-size: 17px; font-weight: 700; letter-spacing: -0.02em; }
        .ty__card-sub { font-size: 13px; color: var(--ink-muted); margin-top: 4px; }
        .ty__card-cta {
          margin-top: 18px;
          padding: 10px 14px;
          background: var(--ink);
          color: #fafafa;
          border-radius: 999px;
          font-size: 14px;
          font-weight: 600;
          display: inline-flex;
          align-items: center;
          justify-content: center;
        }
        .ty__card-file {
          margin-top: 12px;
          font-family: var(--font-mono);
          font-size: 11px;
          color: var(--ink-faint);
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .ty__steps {
          background: var(--bg-elevated);
          border: 1px solid var(--line);
          border-radius: 20px;
          padding: 32px 36px;
          max-width: 720px;
          margin: 0 auto;
          box-shadow: var(--shadow-sm);
        }
        .ty__steps-title {
          font-size: 22px;
          font-weight: 700;
          letter-spacing: -0.02em;
          margin: 0 0 16px;
        }
        .ty__steps-list {
          padding-left: 24px;
          margin: 0;
          display: grid;
          gap: 12px;
          color: var(--ink-soft);
          font-size: 15px;
          line-height: 1.55;
        }
        .ty__steps-list code {
          font-family: var(--font-mono);
          font-size: 12px;
          background: var(--bg-muted);
          padding: 2px 6px;
          border-radius: 4px;
        }
        .ty__guide {
          margin: 0 auto;
          max-width: 720px;
          padding: 22px 26px;
          border-radius: 16px;
          border: 1px solid var(--line);
          background: var(--bg-elevated);
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 24px;
          box-shadow: var(--shadow-sm);
        }
        .ty__guide h3 { margin: 0 0 4px; font-size: 17px; font-weight: 700; letter-spacing: -0.02em; }
        .ty__guide p  { margin: 0; font-size: 13px; color: var(--ink-muted); }
        .ty__guide-cta {
          display: inline-flex;
          align-items: center;
          padding: 10px 18px;
          border-radius: 999px;
          background: var(--ink);
          color: #fafafa;
          font-size: 14px;
          font-weight: 600;
          white-space: nowrap;
          transition: transform 200ms var(--ease-out);
        }
        .ty__guide-cta:hover { transform: translateY(-1px); }
        @media (max-width: 560px) {
          .ty__guide { flex-direction: column; text-align: center; }
        }
        .ty__support {
          margin: 24px auto 0;
          max-width: 720px;
          padding: 24px;
          border-radius: 16px;
          border: 1px solid var(--line);
          background: var(--bg-muted);
          text-align: center;
        }
        .ty__support h3 { margin: 0 0 6px; font-size: 16px; font-weight: 700; }
        .ty__support p { margin: 0; font-size: 14px; color: var(--ink-muted); }
        .ty__support a { color: var(--ink); text-decoration: underline; }
      `}</style>
    </div>
  );
}

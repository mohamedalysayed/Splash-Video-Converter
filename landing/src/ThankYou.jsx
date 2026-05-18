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
  // Gating: "loading" → "valid" → reveal | "invalid" → reject view
  const [verifyState, setVerifyState] = useState("loading");
  const [verifyData, setVerifyData] = useState(null);

  useEffect(() => {
    setDetected(detectOS());
    const params = new URLSearchParams(window.location.search);
    const sid = params.get("session_id");
    setSessionId(sid);

    if (!sid) {
      setVerifyState("invalid");
      return;
    }

    (async () => {
      try {
        const res = await fetch(`/api/verify-session?session_id=${encodeURIComponent(sid)}`);
        const data = await res.json();
        if (data.valid) {
          setVerifyState("valid");
          setVerifyData(data);
        } else {
          setVerifyState("invalid");
          setVerifyData(data);
        }
      } catch (e) {
        setVerifyState("invalid");
      }
    })();
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

      {verifyState === "loading" && <VerifyLoader />}
      {verifyState === "invalid" && <VerifyRejected reason={verifyData?.reason} />}

      {verifyState === "valid" && (
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
      )}

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

        /* ── Gate states ───────────────────────────────────── */
        .ty-gate {
          min-height: calc(100vh - 200px);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 80px 24px;
        }
        .ty-gate__inner {
          max-width: 520px;
          text-align: center;
        }
        .ty-spinner {
          width: 44px; height: 44px;
          margin: 0 auto 24px;
          border-radius: 999px;
          border: 3px solid var(--bg-muted);
          border-top-color: var(--ink);
          animation: ty-spin 0.9s linear infinite;
        }
        @keyframes ty-spin { to { transform: rotate(360deg); } }
        .ty-gate__title {
          font-size: clamp(24px, 4vw, 32px);
          font-weight: 800;
          letter-spacing: -0.02em;
          margin: 0 0 12px;
          color: var(--ink);
        }
        .ty-gate__sub {
          font-size: 16px;
          color: var(--ink-muted);
          line-height: 1.55;
          margin: 0;
        }
        .ty-gate__lock {
          width: 56px; height: 56px;
          margin: 0 auto 22px;
          border-radius: 14px;
          display: grid; place-items: center;
          background: var(--bg-elevated);
          border: 1px solid var(--line);
          color: var(--ink-muted);
          box-shadow: var(--shadow-sm);
        }
        .ty-gate__actions {
          display: flex;
          gap: 12px;
          justify-content: center;
          margin-top: 28px;
          flex-wrap: wrap;
        }
        .ty-gate__btn {
          padding: 12px 22px;
          border-radius: 999px;
          font-size: 14px;
          font-weight: 600;
          background: var(--ink);
          color: #fafafa;
          transition: transform 200ms var(--ease-out);
        }
        .ty-gate__btn:hover { transform: translateY(-1px); }
        .ty-gate__btn--ghost {
          background: transparent;
          color: var(--ink);
          border: 1px solid var(--line-strong);
        }
        .ty-gate__btn--ghost:hover { background: var(--bg-elevated); }
      `}</style>
    </div>
  );
}

/* ─── Gate views (loader + rejected) ────────────────────── */

function VerifyLoader() {
  return (
    <main className="ty-gate">
      <div className="ty-gate__inner">
        <div className="ty-spinner" />
        <h2 className="ty-gate__title">Verifying your purchase…</h2>
        <p className="ty-gate__sub">
          One sec. We're checking with Stripe to confirm your payment landed.
        </p>
      </div>
    </main>
  );
}

function VerifyRejected({ reason }) {
  const headlines = {
    no_session_id:        "This page is for verified buyers only.",
    not_paid:             "We couldn't confirm your payment yet.",
    invalid_session:      "We can't find that purchase.",
    server_misconfigured: "Something's off on our end.",
  };
  const subs = {
    no_session_id:        "If you just paid, please use the link in your Stripe receipt email — it includes the verification code that unlocks the downloads.",
    not_paid:             "Your Stripe session exists but the payment hasn't completed. If your card is being charged, give it a minute and refresh.",
    invalid_session:      "The verification code in this URL doesn't match a real Stripe checkout. If you paid, check your receipt email for the correct link.",
    server_misconfigured: "The site is temporarily unable to verify purchases. Please email muhammmedaly@gmail.com with your Stripe receipt and we'll send your downloads directly.",
  };
  const title = headlines[reason] || headlines.invalid_session;
  const sub   = subs[reason]      || subs.invalid_session;
  return (
    <main className="ty-gate">
      <div className="ty-gate__inner">
        <div className="ty-gate__lock" aria-hidden>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
        </div>
        <h2 className="ty-gate__title">{title}</h2>
        <p className="ty-gate__sub">{sub}</p>
        <div className="ty-gate__actions">
          <a href="/" className="ty-gate__btn">Back to Cast</a>
          <a href="mailto:muhammmedaly@gmail.com?subject=Cast%20download%20issue" className="ty-gate__btn ty-gate__btn--ghost">Email support</a>
        </div>
      </div>
    </main>
  );
}

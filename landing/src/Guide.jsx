import React, { useEffect, useMemo } from "react";
import { marked } from "marked";
import guideMd from "../../USER_GUIDE.md?raw";

/* ─────────────────────────────────────────────────────────────
   /guide — the User Guide as a beautifully-typeset web page.
   Single-sourced from USER_GUIDE.md, so the print-PDF and the
   web read are identical.
   ───────────────────────────────────────────────────────────── */

marked.setOptions({ gfm: true, breaks: false });

export default function Guide() {
  const html = useMemo(() => marked.parse(guideMd), []);

  useEffect(() => {
    document.title = "Cast — User Guide";
  }, []);

  return (
    <div className="guide-page">
      <nav className="nav guide-nav">
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
            <button className="nav__cta" onClick={() => window.print()}>Save as PDF</button>
          </div>
        </div>
      </nav>

      <header className="guide-hero">
        <p className="guide-eyebrow">User guide · v1.0</p>
        <h1 className="guide-h1">Everything you need to know about Cast.</h1>
        <p className="guide-sub">
          A 10-minute read. Print it, save it, or just keep this tab open. It's the same words your binary shipped with — and the same ones you'll find in the release.
        </p>
      </header>

      <main className="guide-body container">
        <div className="guide-content" dangerouslySetInnerHTML={{ __html: html }} />
      </main>

      <footer className="footer container">
        <div className="footer__brand">
          <span className="nav__logo" style={{ width: 22, height: 22, borderRadius: 6, fontSize: 11 }}>▶</span>
          Cast <span style={{ color: "var(--ink-faint)", fontWeight: 500, marginLeft: 6 }}>by Splash</span>
        </div>
        <div style={{ fontSize: 13, color: "var(--ink-muted)" }}>© {new Date().getFullYear()} Splash · GPL-3.0</div>
      </footer>

      <style>{`
        .guide-page { background: var(--bg); min-height: 100vh; }
        .guide-nav  { border-bottom: 1px solid var(--line-faint); }
        .guide-hero {
          padding: 140px 24px 56px;
          text-align: center;
          max-width: 760px;
          margin: 0 auto;
        }
        .guide-eyebrow {
          display: inline-flex;
          align-items: center;
          padding: 6px 14px;
          border-radius: 999px;
          background: var(--bg-elevated);
          border: 1px solid var(--line);
          font-size: 12px;
          font-weight: 600;
          letter-spacing: 0.04em;
          color: var(--ink-muted);
          margin-bottom: 24px;
          box-shadow: var(--shadow-xs);
        }
        .guide-h1 {
          font-size: clamp(36px, 5.5vw, 60px);
          font-weight: 800;
          line-height: 1.05;
          letter-spacing: -0.035em;
          margin: 0 0 20px;
        }
        .guide-sub {
          font-size: clamp(16px, 1.7vw, 19px);
          color: var(--ink-muted);
          margin: 0;
          line-height: 1.5;
        }
        .guide-body { padding: 24px 0 80px; }

        /* ── Typography ─────────────────────────────────────── */
        .guide-content {
          max-width: 720px;
          margin: 0 auto;
          color: var(--ink);
          font-size: 17px;
          line-height: 1.65;
        }
        .guide-content > *:first-child { display: none; } /* hide the redundant H1 from the .md file */
        .guide-content > p:first-of-type { display: none; } /* and the welcome italic */
        .guide-content > hr:first-of-type { display: none; }
        .guide-content h2 {
          margin: 64px 0 14px;
          font-size: 30px;
          font-weight: 800;
          letter-spacing: -0.025em;
          line-height: 1.15;
          scroll-margin-top: 90px;
        }
        .guide-content h3 {
          margin: 32px 0 10px;
          font-size: 20px;
          font-weight: 700;
          letter-spacing: -0.015em;
        }
        .guide-content p {
          margin: 14px 0;
          color: var(--ink-soft);
        }
        .guide-content strong { color: var(--ink); font-weight: 700; }
        .guide-content em { color: var(--ink-muted); }
        .guide-content a {
          color: var(--ink);
          text-decoration: underline;
          text-decoration-color: var(--ink-ghost);
          text-underline-offset: 3px;
          transition: text-decoration-color 160ms;
        }
        .guide-content a:hover { text-decoration-color: var(--ink); }

        /* ── Lists ──────────────────────────────────────────── */
        .guide-content ul,
        .guide-content ol { padding-left: 24px; margin: 14px 0; }
        .guide-content li { margin: 8px 0; color: var(--ink-soft); }
        .guide-content li::marker { color: var(--ink-faint); }

        /* ── Code ───────────────────────────────────────────── */
        .guide-content code {
          font-family: var(--font-mono);
          font-size: 14px;
          background: var(--bg-muted);
          padding: 2px 7px;
          border-radius: 5px;
          color: var(--ink);
        }
        .guide-content pre {
          background: var(--bg-deep);
          color: #f5f5f7;
          padding: 18px 20px;
          border-radius: 12px;
          overflow-x: auto;
          margin: 18px 0;
          box-shadow: var(--shadow-sm);
        }
        .guide-content pre code {
          background: transparent;
          padding: 0;
          color: inherit;
          font-size: 13.5px;
          line-height: 1.55;
        }

        /* ── Tables ─────────────────────────────────────────── */
        .guide-content table {
          width: 100%;
          border-collapse: collapse;
          margin: 20px 0;
          font-size: 15px;
          background: var(--bg-elevated);
          border: 1px solid var(--line);
          border-radius: 14px;
          overflow: hidden;
          box-shadow: var(--shadow-sm);
        }
        .guide-content thead {
          background: var(--bg-muted);
        }
        .guide-content th {
          text-align: left;
          padding: 12px 16px;
          font-size: 12px;
          font-weight: 700;
          letter-spacing: 0.05em;
          text-transform: uppercase;
          color: var(--ink-muted);
        }
        .guide-content td {
          padding: 12px 16px;
          border-top: 1px solid var(--line-faint);
          color: var(--ink-soft);
          vertical-align: top;
        }
        .guide-content td strong { color: var(--ink); }

        /* ── Blockquote ─────────────────────────────────────── */
        .guide-content blockquote {
          margin: 20px 0;
          padding: 16px 20px;
          border-left: 3px solid var(--ink);
          background: var(--bg-muted);
          border-radius: 0 12px 12px 0;
          color: var(--ink-soft);
        }
        .guide-content blockquote p { margin: 0; }

        /* ── Horizontal rule ────────────────────────────────── */
        .guide-content hr {
          border: 0;
          height: 1px;
          background: var(--line);
          margin: 56px 0;
        }

        /* ── Print ──────────────────────────────────────────── */
        @media print {
          body { background: #fff; }
          .guide-nav, .footer { display: none; }
          .guide-hero { padding: 0 0 32px; text-align: left; }
          .guide-eyebrow { display: none; }
          .guide-content { max-width: none; font-size: 12pt; }
          .guide-content pre { box-shadow: none; border: 1px solid #ccc; }
          .guide-content table { box-shadow: none; }
          a { color: #000 !important; text-decoration: none !important; }
        }
      `}</style>
    </div>
  );
}

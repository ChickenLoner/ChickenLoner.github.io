#!/usr/bin/env python3
"""Transform all review pages to full SOC Console theme.

Replaces the old Tailwind nav/dark-mode chrome with SOC topbar,
SOC cover hero, SOC meta-grid, SOC res-toc, and SOC footer —
modelled on the research article pages.
"""

import os, re

REVIEWS_DIR = os.path.join(os.path.dirname(__file__), "reviews")

# ── SOC chrome CSS to replace the <style> block content ──────────────────────
SOC_STYLE_CONTENT = """\
        @keyframes fadeIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
        @keyframes socbp{50%{opacity:.3}}
        .animate-fadeIn{animation:fadeIn 0.45s ease-out}
        body{background:var(--soc-bg);color:var(--soc-ink);font-family:system-ui,-apple-system,sans-serif;margin:0}
        /* Top bar */
        .soc-tb{position:sticky;top:0;z-index:50;background:rgba(7,11,20,.94);backdrop-filter:blur(10px) saturate(140%);-webkit-backdrop-filter:blur(10px) saturate(140%);border-bottom:1px solid var(--soc-line)}
        .soc-tb-row{display:flex;align-items:center;gap:14px;padding:9px 22px;font-size:12px;flex-wrap:wrap}
        .soc-live{display:inline-flex;align-items:center;gap:6px;color:var(--soc-gn);font-weight:600;letter-spacing:.06em;font-family:'JetBrains Mono',monospace}
        .soc-live::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--soc-gn);box-shadow:0 0 8px var(--soc-gn);animation:socbp 1.6s ease infinite}
        .soc-crumb{color:var(--soc-ink3);display:flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:11px}
        .soc-crumb b{color:var(--soc-ink);font-weight:600}
        .soc-clock{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--soc-ink3)}
        /* Badges */
        .sev{display:inline-flex;align-items:center;gap:5px;padding:3px 9px;border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.1em;font-weight:700;text-transform:uppercase;white-space:nowrap}
        .sev .dot{width:6px;height:6px;border-radius:50%;background:currentcolor;flex-shrink:0}
        .sev.green {background:rgba(61,220,132,.12);color:var(--soc-gn);border:1px solid rgba(61,220,132,.3)}
        .sev.red   {background:rgba(255,85,119,.12);color:var(--soc-rd);border:1px solid rgba(255,85,119,.3)}
        .sev.cyan  {background:rgba(34,225,255,.1);color:var(--soc-cy);border:1px solid rgba(34,225,255,.25)}
        .sev.amber {background:rgba(255,181,71,.12);color:var(--soc-am);border:1px solid rgba(255,181,71,.3)}
        .sev.violet{background:rgba(167,139,250,.1);color:var(--soc-vi);border:1px solid rgba(167,139,250,.25)}
        /* Cover */
        .res-cover{position:relative;border-radius:6px;overflow:hidden;border:1px solid var(--soc-line);margin-bottom:20px}
        .res-cover img{width:100%;max-height:340px;object-fit:cover;display:block}
        .res-cover-overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(7,11,20,.92) 0%,rgba(7,11,20,.35) 55%,transparent 100%)}
        .res-cover-content{position:absolute;bottom:0;left:0;right:0;padding:24px}
        .res-cover-title{font-size:22px;font-weight:800;color:var(--soc-ink);letter-spacing:-.01em;margin:0 0 12px;line-height:1.3}
        .res-cover-badges{display:flex;flex-wrap:wrap;gap:8px}
        /* Meta grid */
        .res-meta-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;background:var(--soc-bg-1);border:1px solid var(--soc-line);border-radius:6px;padding:16px 18px;margin-bottom:20px}
        .res-meta-lbl{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--soc-ink3);text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px}
        .res-meta-val{font-size:13px;font-weight:600;color:var(--soc-ink)}
        /* TOC */
        .res-toc{background:var(--soc-bg-1);border:1px solid var(--soc-line);border-radius:6px;padding:16px 18px;margin-bottom:24px}
        .res-toc-title{font-size:12px;font-weight:600;color:var(--soc-ink2);font-family:'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px}
        .res-toc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:2px}
        .res-toc-item{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:4px;color:var(--soc-ink3);font-size:12px;text-decoration:none;transition:.15s}
        .res-toc-item:hover{background:rgba(34,225,255,.05);color:var(--soc-cy)}
        .res-toc-num{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--soc-ink4);width:20px;flex-shrink:0}
        /* Sections */
        .res-section{scroll-margin-top:60px;margin-bottom:32px}
        .res-section-title{display:flex;align-items:center;gap:10px;font-size:17px;font-weight:700;color:var(--soc-ink);padding-bottom:12px;margin-bottom:18px;border-bottom:1px solid var(--soc-line)}
        .res-section-icon{width:32px;height:32px;border-radius:6px;display:grid;place-items:center;background:rgba(34,225,255,.1);border:1px solid rgba(34,225,255,.25);flex-shrink:0}
        /* Footer */
        .soc-ft{margin-top:32px;padding:16px 0;text-align:center;color:var(--soc-ink4);font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.06em;border-top:1px solid var(--soc-line)}
        /* Scrollbar */
        ::-webkit-scrollbar{width:6px;height:6px}
        ::-webkit-scrollbar-track{background:var(--soc-bg)}
        ::-webkit-scrollbar-thumb{background:var(--soc-line2);border-radius:4px}
        *{scrollbar-color:var(--soc-line2) var(--soc-bg)}
        /* Global text */
        strong{color:var(--soc-ink)}
        p{font-size:13px;color:var(--soc-ink2);line-height:1.75;margin:0 0 10px}
        a{color:var(--soc-cy)}
        a:hover{text-decoration:underline}
        /* Figure */
        figure{margin:14px 0}
        figure img{border:1px solid var(--soc-line);border-radius:5px;max-width:100%;display:block;background:var(--soc-bg-2);margin:0 auto}
        figcaption{text-align:center;font-size:11px;color:var(--soc-ink3);margin-top:6px;font-style:italic}
        /* Inline code */
        code{font-family:'JetBrains Mono',monospace;font-size:11px;background:rgba(34,225,255,.06);color:var(--soc-cy);padding:1px 6px;border-radius:3px;border:1px solid rgba(34,225,255,.15)}
        /* Tailwind overrides for content sections */
        .bg-white,.bg-white\\/80{background:var(--soc-bg-1) !important}
        .bg-gray-50{background:var(--soc-bg) !important}
        .bg-gray-100{background:var(--soc-bg-2) !important}
        .border-gray-100,.border-gray-200{border-color:var(--soc-line) !important}
        .text-gray-800{color:var(--soc-ink) !important}
        .text-gray-700{color:var(--soc-ink2) !important}
        .text-gray-600{color:var(--soc-ink3) !important}
        .text-gray-500{color:var(--soc-ink4) !important}
        .text-gray-400{color:var(--soc-ink4) !important}
        .text-blue-600{color:var(--soc-cy) !important}
        .text-amber-600,.text-amber-700,.text-yellow-500{color:var(--soc-am) !important}
        .text-orange-600,.text-orange-700{color:var(--soc-am) !important}
        .text-green-600,.text-green-700,.text-green-800{color:var(--soc-gn) !important}
        .text-red-600{color:var(--soc-rd) !important}
        .bg-amber-50,.bg-orange-50{background:rgba(255,181,71,.06) !important}
        .border-amber-200,.border-amber-400,.border-orange-200,.border-orange-400{border-color:rgba(255,181,71,.3) !important}
        .bg-blue-50,.bg-indigo-50{background:rgba(34,225,255,.05) !important}
        .border-blue-200,.border-blue-400{border-color:rgba(34,225,255,.2) !important}
        .bg-green-50,.bg-green-100{background:rgba(61,220,132,.05) !important}
        .border-green-200,.border-green-400{border-color:rgba(61,220,132,.2) !important}
        .shadow-sm{box-shadow:none !important}
        .hover\\:bg-gray-50:hover{background:var(--soc-bg-2) !important}
        ul{list-style-type:disc;padding-left:20px;margin:8px 0}
        ol{list-style-type:decimal;padding-left:20px;margin:8px 0}
        li{font-size:13px;color:var(--soc-ink2);line-height:1.7;margin-bottom:4px}
"""

# ── SocClock component (to inject before App) ─────────────────────────────────
SOC_CLOCK_COMPONENT = """\
        const SocClock = () => {
            const ref = useRef(null);
            useEffect(() => {
                const tick = () => {
                    if (!ref.current) return;
                    const n = new Date();
                    ref.current.textContent = n.toISOString().slice(0,10) + ' · ' + n.toISOString().slice(11,19) + 'Z';
                };
                tick();
                const id = setInterval(tick, 1000);
                return () => clearInterval(id);
            }, []);
            return <span ref={ref} className="soc-clock" />;
        };
"""

# ── SOC Section component ─────────────────────────────────────────────────────
SOC_SECTION = """\
        const Section = ({ id, title, icon, children }) => (
            <section id={id} className="res-section">
                <div className="res-section-title">
                    <div className="res-section-icon">
                        <Icon name={icon} className="w-4 h-4" style={{color:'var(--soc-cy)'}} />
                    </div>
                    {title}
                </div>
                <div style={{display:'flex',flexDirection:'column',gap:'14px'}}>{children}</div>
            </section>
        );"""


def extract(src, pattern, group=1, default=''):
    m = re.search(pattern, src, re.DOTALL)
    return m.group(group).strip() if m else default


def build_nav(crumb_text):
    return f"""\
                    {'{/* SOC Topbar */}'}
                    <nav className="soc-tb" aria-label="Site navigation">
                        <div className="soc-tb-row">
                            <span className="soc-live">UPLINK</span>
                            <div className="soc-crumb">
                                <a href="/" style={{{{color:'var(--soc-ink3)',textDecoration:'none'}}}}>SOC</a>
                                <span>/</span>
                                <a href="/" style={{{{color:'var(--soc-ink3)',textDecoration:'none'}}}}>OPERATOR.PROFILE</a>
                                <span>/</span>
                                <a href="/reviews/index.html" style={{{{color:'var(--soc-ink3)',textDecoration:'none'}}}}>REVIEWS</a>
                                <span>/</span>
                                <b>{crumb_text}</b>
                            </div>
                            <div style={{{{flex:1}}}} />
                            <span className="sev cyan"><span className="dot"></span>TLP:CLEAR</span>
                            <span className="sev amber"><span className="dot"></span>CERT.REVIEW</span>
                            <SocClock />
                        </div>
                    </nav>"""


def build_hero(h1_title, provider, date_text, img_alt):
    return f"""\
                        {'{/* Cover */}'}
                        <div className="res-cover">
                            <img src="cover.png" alt="{img_alt}" />
                            <div className="res-cover-overlay" />
                            <div className="res-cover-content">
                                <h1 className="res-cover-title">{h1_title}</h1>
                                <div className="res-cover-badges">
                                    <span className="sev cyan"><span className="dot"></span>{date_text}</span>
                                    <span className="sev amber"><span className="dot"></span>{provider}</span>
                                    <span className="sev green"><span className="dot"></span>Passed</span>
                                </div>
                            </div>
                        </div>"""


def build_meta(cert_code, provider):
    return """\
                        {/* Metadata */}
                        <div className="res-meta-grid">
                            <div><div className="res-meta-lbl">Certification</div><div className="res-meta-val">""" + cert_code + """</div></div>
                            <div><div className="res-meta-lbl">Provider</div><div className="res-meta-val">""" + provider + """</div></div>
                            <div><div className="res-meta-lbl">Difficulty</div><div className="res-meta-val" style={{color:'var(--soc-am)'}}>{meta?.difficulty ?? '—'}</div></div>
                            <div><div className="res-meta-lbl">Rating</div>
                                <div className="res-meta-val">
                                    {meta?.rating ? (
                                        <span style={{display:'flex',alignItems:'center',gap:'4px'}}>
                                            <span style={{color:'var(--soc-am)'}}>{renderStars(meta.rating)}</span>
                                            <span style={{color:'var(--soc-ink3)',fontSize:'11px'}}>{meta.rating.toFixed(1)}/5.0</span>
                                        </span>
                                    ) : <span style={{color:'var(--soc-ink4)'}}>—</span>}
                                </div>
                            </div>
                        </div>"""


SOC_TOC = """\
                        {/* Table of Contents */}
                        <div className="res-toc">
                            <div className="res-toc-title">// TABLE OF CONTENTS</div>
                            <div className="res-toc-grid">
                                {tocItems.map((item, i) => (
                                    <a key={item.id} href={`#${item.id}`} className="res-toc-item">
                                        <span className="res-toc-num">{String(i+1).padStart(2,'0')}.</span>
                                        <Icon name={item.icon} className="w-3.5 h-3.5" style={{color:'var(--soc-ink4)',flexShrink:0}} />
                                        <span>{item.label}</span>
                                    </a>
                                ))}
                            </div>
                        </div>"""


SOC_FOOTER = """\
                        {/* Footer */}
                        <div className="soc-ft">
                            <a href="/reviews/index.html" style={{color:'var(--soc-ink4)',textDecoration:'none'}}>← ALL REVIEWS</a>
                            <span style={{margin:'0 12px'}}>|</span>
                            <a href="#" style={{color:'var(--soc-ink4)',textDecoration:'none'}}>↑ BACK TO TOP</a>
                        </div>"""


def transform(path):
    with open(path, encoding='utf-8') as f:
        src = f.read()

    # ── 1. Extract cert-specific data ─────────────────────────────────────────
    folder = os.path.basename(os.path.dirname(path)).upper()

    # Nav breadcrumb text (last <span> in old nav)
    crumb = extract(src, r'<span className="font-semibold text-gray-700">([^<]+)</span>', 1, folder)

    # Hero h1 title
    h1_title = extract(src,
        r'<h1 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-3 leading-snug">\s*(.*?)\s*</h1>', 1,
        crumb + ' Certification Review')

    # img alt from hero
    img_alt = extract(src,
        r'<img src="cover\.png" alt="([^"]+)"', 1, h1_title)

    # Provider (Building2 icon badge text)
    provider = extract(src,
        r'<Icon name="Building2" className="w-3\.5 h-3\.5" />\s*([^\n<]+)', 1, 'Unknown')
    provider = provider.strip()

    # Date (Calendar icon badge text)
    date_text = extract(src,
        r'<Icon name="Calendar" className="w-3\.5 h-3\.5" />\s*([^\n<]+)', 1, '')
    date_text = date_text.strip()

    # Cert code from metadata card
    cert_code = extract(src,
        r'>Certification</span><span className="font-semibold text-gray-800">([^<]+)</span>', 1,
        crumb)

    # ── 2. Replace <style> block ───────────────────────────────────────────────
    src = re.sub(
        r'<style>.*?</style>',
        '<style>\n' + SOC_STYLE_CONTENT + '    </style>',
        src, count=1, flags=re.DOTALL)

    # ── 3. Add JetBrains Mono font after favicon link ─────────────────────────
    FONT_LINKS = (
        '\n    <link rel="preconnect" href="https://fonts.googleapis.com">'
        '\n    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '\n    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">'
    )
    FAVICON_PAT = r'(<link rel="icon" href="/chicken0248\.png" type="image/png">)'
    if 'JetBrains Mono' not in src:
        src = re.sub(FAVICON_PAT, r'\1' + FONT_LINKS, src, count=1)

    # ── 4. Replace Section component definition ────────────────────────────────
    src = re.sub(
        r'        const Section = \(\{ id, title, icon, children \}\) => \(.*?        \);',
        SOC_SECTION,
        src, count=1, flags=re.DOTALL)

    # ── 5. Remove dark mode state and its useEffect ────────────────────────────
    src = re.sub(
        r"            const \[dark, setDark\] = useState\([^\n]+\n",
        '', src, count=1)
    src = re.sub(
        r"            useEffect\(\(\) => \{ localStorage\.setItem\([^\n]+\n",
        '', src, count=1)

    # ── 6. Inject SocClock before App definition ───────────────────────────────
    if 'SocClock' not in src:
        src = src.replace(
            '        /* ── App ── */\n',
            SOC_CLOCK_COMPONENT + '\n        /* ── App ── */\n', 1)
        if 'SocClock' not in src:
            # fallback: inject before const App
            src = src.replace(
                '        const App = () => {',
                SOC_CLOCK_COMPONENT + '\n        const App = () => {', 1)

    # ── 7. Replace outer wrapper div ──────────────────────────────────────────
    src = re.sub(
        r'<div className=\{`min-h-screen bg-gradient-to-br[^`]+`\}>',
        "<div style={{background:'var(--soc-bg)',minHeight:'100vh'}}>",
        src, count=1)

    # ── 8. Replace nav block ───────────────────────────────────────────────────
    NAV_BLOCK_PAT = (
        r'\{/\* Navigation \*/\}\s*'
        r'<nav aria-label="Site navigation".*?</nav>'
    )
    src = re.sub(NAV_BLOCK_PAT, build_nav(crumb), src, count=1, flags=re.DOTALL)

    # ── 9. Replace main tag classes ───────────────────────────────────────────
    src = re.sub(
        r'<main id="main-content" className="max-w-4xl mx-auto px-4 py-8 space-y-10 animate-fadeIn">',
        '<main id="main-content" style={{maxWidth:\'860px\',margin:\'0 auto\',padding:\'24px 20px\'}} className="animate-fadeIn">',
        src, count=1)

    # ── 10. Replace hero block ────────────────────────────────────────────────
    HERO_PAT = (
        r'\{/\* Hero \*/\}\s*'
        r'<div className="relative overflow-hidden rounded-3xl shadow-2xl">.*?</div>'
        r'\s*\{/\* Metadata \*/\}'
    )
    hero_replacement = build_hero(h1_title, provider, date_text, img_alt) + '\n\n                        {/* Metadata */}'
    src = re.sub(HERO_PAT, hero_replacement, src, count=1, flags=re.DOTALL)

    # ── 11. Replace metadata card ─────────────────────────────────────────────
    META_PAT = (
        r'\{/\* Metadata \*/\}\s*'
        r'<div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm">.*?</div>'
        r'\s*\{/\* Table of Contents \*/\}'
    )
    src = re.sub(META_PAT,
                 build_meta(cert_code, provider) + '\n\n                        {/* Table of Contents */}',
                 src, count=1, flags=re.DOTALL)

    # ── 12. Replace TOC card (include outer closing </div>) ───────────────────
    TOC_PAT = (
        r'\{/\* Table of Contents \*/\}\s*'
        r'<div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">.*?</div>'
        r'\s*</div>'
    )
    src = re.sub(TOC_PAT, SOC_TOC, src, count=1, flags=re.DOTALL)

    # ── 13. Replace footer ────────────────────────────────────────────────────
    FOOTER_PAT = (
        r'\{/\* Footer navigation \*/\}\s*'
        r'<div className="text-center py-8 border-t border-gray-200">.*?</div>'
    )
    src = re.sub(FOOTER_PAT, SOC_FOOTER, src, count=1, flags=re.DOTALL)

    return src


changed, errors = [], []

for root, dirs, files in os.walk(REVIEWS_DIR):
    for fname in files:
        if fname != 'index.html':
            continue
        path = os.path.join(root, fname)
        # Skip the reviews landing page — it already has full SOC theme
        if os.path.abspath(path) == os.path.abspath(os.path.join(REVIEWS_DIR, 'index.html')):
            continue
        rel  = os.path.relpath(path, os.path.dirname(__file__))
        try:
            new_src = transform(path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_src)
            changed.append(rel)
        except Exception as e:
            errors.append((rel, str(e)))

print(f"Changed : {len(changed)}")
for p in changed: print(f"  + {p}")
if errors:
    print(f"Errors  : {len(errors)}")
    for p, msg in errors: print(f"  ! {p}: {msg}")
else:
    print("Errors  : 0")

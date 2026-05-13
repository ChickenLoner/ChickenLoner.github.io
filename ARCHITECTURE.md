# ChickenLoner.github.io — Architecture Reference

Static portfolio site. Cybersecurity focus: DFIR, SOC, Blue Team. React SPAs embedded in every HTML page. SOC Console dark theme throughout.

---

## Directory Structure

```
/
├── index.html                        # Main portfolio (React SPA)
├── reviews/
│   ├── index.html                    # Reviews hub — lists all cert reviews
│   ├── oscp/index.html
│   ├── cdsa/index.html
│   └── [18 total cert subdirs]       # Each is a self-contained React SPA
├── research/
│   ├── index.html                    # Research hub
│   ├── anydesk-forensics-windows/index.html
│   ├── chrome-remote-desktop-forensics/index.html
│   ├── git-commits-persistence/index.html
│   ├── gotohttp-forensics-windows/index.html
│   ├── rustdesk-forensics-windows/index.html
│   └── windows-forensics-lab/index.html
├── ir-reports/
│   ├── index.html                    # IR hub
│   ├── btlo-halloween-2025/index.html
│   └── htb-tinsel-trace-1/index.html
├── cloud-labs/index.html             # Cloud security labs hub
├── siem-labs/index.html              # SIEM labs hub
├── data/                             # JSON — single source of truth for all content
│   ├── certifications.json
│   ├── reviews.json
│   ├── research.json
│   ├── ir-reports.json
│   ├── labs.json
│   ├── labs_metadata.json            # Auto-updated by GitHub Actions daily
│   ├── achievements.json
│   ├── skills.json
│   └── social.json
├── assets/
│   ├── badges/                       # Cert badge PNGs
│   ├── certificates/                 # Cert screenshot JPGs
│   ├── labs/                         # Lab cover images
│   ├── reports/[slug]/               # IR report figures
│   ├── research/[slug]/              # Research article figures (cover.png + figures)
│   └── achievements/                 # Talk/CTF images
├── themes/
│   ├── soc.css                       # Shared CSS variables + Tailwind utility overrides
│   ├── soc-nav.js                    # Page transition overlay
│   └── soc-components.js             # Shared React components (plain createElement, no JSX)
├── scripts/
│   └── update_lab_data.py            # Fetches lab metadata from external APIs
├── _soc_reviews_full.py              # Batch: apply SOC theme to all review pages
├── _soc_research_articles.py         # Batch: apply SOC theme to all research pages
├── _soc_reviews.py                   # Legacy (deprecated, superseded by _full.py)
├── .github/workflows/
│   ├── static.yml                    # Deploy to GitHub Pages on push to main
│   └── update_lab_data.yml           # Daily: refresh labs_metadata.json
├── chicken0248.png                   # Favicon + avatar
└── export_from_notion/               # Drop zone for Notion exports (new content)
```

---

## Page Architecture

### Types of Pages

| Type | Count | Location | Data Source |
|------|-------|----------|-------------|
| Main portfolio | 1 | `/index.html` | All 9 JSON files |
| Section hubs | 5 | `/reviews/`, `/research/`, `/ir-reports/`, `/cloud-labs/`, `/siem-labs/` | Respective JSON |
| Cert review detail | 18 | `/reviews/[slug]/` | `/data/reviews.json` |
| Research article | 6 | `/research/[slug]/` | `/data/research.json` |
| IR report | 2 | `/ir-reports/[slug]/` | `/data/ir-reports.json` |

### HTML Page Template

Every page follows this exact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title — ChickenLoner</title>

    <!-- OG + Twitter Card meta tags (required on all pages) -->
    <meta property="og:type" content="article" />
    <meta property="og:title" content="..." />
    <meta property="og:description" content="..." />
    <meta property="og:image" content="..." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="..." />
    <meta name="twitter:description" content="..." />
    <meta name="twitter:image" content="..." />

    <link rel="icon" href="/chicken0248.png">

    <!-- External dependencies (CDN, pinned versions — no local bundling) -->
    <!-- Note: Tailwind CDN is EXCLUDED from all detail pages (reviews, research, IR reports).
         Hub pages (reviews/index, research/index, ir-reports/index, cloud-labs, siem-labs) still load it. -->
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7.29.2/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@1.14.0/dist/umd/lucide.min.js"></script>

    <!-- SOC theme + shared components (load BEFORE text/babel scripts) -->
    <link rel="stylesheet" href="/themes/soc.css">
    <script src="/themes/soc-components.js"></script>
    <script src="/themes/soc-nav.js" defer></script>

    <!-- Page-specific inline styles -->
    <style>
        :root { /* CSS variables re-declared inline for self-containment */ }
        /* Component-specific styles */
    </style>
</head>
<body>
    <a href="#main-content" class="sr-only">Skip to content</a>
    <noscript>JavaScript required.</noscript>
    <div id="root"></div>
    <script type="text/babel">
        const { useState, useEffect, useRef } = React;
        /* All React components and page content */
        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
```

**Key constraint:** Pages are self-contained. The inline `<style>` re-declares all CSS variables so the page renders correctly even if `/themes/soc.css` fails to load.

---

## Design System — SOC Console Dark Theme

### Color Palette

| Variable | Hex | Usage |
|----------|-----|-------|
| `--soc-bg` | `#070b14` | Page background |
| `--soc-bg-1` | `#0c1322` | Cards, surfaces |
| `--soc-bg-2` | `#121a2e` | Elevated surfaces |
| `--soc-line` | `#1c2740` | Subtle borders |
| `--soc-line2` | `#2a3a5c` | Visible borders |
| `--soc-ink` | `#e4ecff` | Primary text |
| `--soc-ink2` | `#a9b6d3` | Secondary text |
| `--soc-ink3` | `#6c7a9c` | Tertiary/disabled |
| `--soc-ink4` | `#475070` | Faint text |
| `--soc-cy` | `#22e1ff` | Cyan — interactive elements, links, highlights |
| `--soc-cy2` | `#06b8d9` | Cyan darker variant |
| `--soc-am` | `#ffb547` | Amber — warnings, secondary accent |
| `--soc-gn` | `#3ddc84` | Green — success, online indicators |
| `--soc-rd` | `#ff5577` | Red — danger, alerts |
| `--soc-vi` | `#a78bfa` | Violet — accent |

**Category → color mapping (severity badges):**
- Digital Forensics → cyan (`--soc-cy`)
- Red Teaming → red (`--soc-rd`)
- Lab Making → amber (`--soc-am`)
- Blue Team / SOC → green (`--soc-gn`)

### Key CSS Classes

**Navigation:**
- `.soc-tb` — Sticky topbar with `backdrop-filter: blur`
- `.soc-tb-row` — Flex row inside topbar
- `.soc-crumb` — Breadcrumb: `SOC / OPERATOR.PROFILE / [section]`
- `.soc-live` — "UPLINK" pulsing indicator (top right)
- `.soc-clock` — Real-time UTC clock display

**Status Badges:**
- `.sev` — Base severity/category badge
- `.sev.green` / `.sev.cyan` / `.sev.amber` / `.sev.red` / `.sev.violet` — Color variants
- Used for: TLP:CLEAR, cert category, dates, platform labels

**Content Sections:**
- `.res-section` — Research/review section block (icon + title + left bar)
- `.ir-section` — IR report section block
- `.res-subsection` — Nested subsection within a section

**Content Components:**
- `.res-code-wrap` + `.res-code-lang` — Code block with language label
- `.res-table-wrap` + `.res-table` — Styled data table
- `.res-figure` — Figure with caption
- `.res-callout.info` / `.warning` / `.tip` — Colored callout boxes
- `.ir-finding` — Numbered finding card (IR reports only)

**Hub/Listing Pages:**
- `.soc-section` — Section heading with colored left border
- `.soc-stat-grid` / `.soc-stat-cell` — 4-column stats grid
- `.soc-credit` — Cert badge card
- `.soc-rail` — Marquee badge carousel
- `.soc-search-bar` — Search input with icon
- `.soc-select` — Styled dropdown
- `.soc-alert` / `.soc-alerts` — Alert-log style containers

**Hero:**
- `.soc-hero` — Main hero box with gradient overlay
- `.res-cover` — Research/review article cover
- `.ir-cover` — IR report cover

### Typography

- Font: **JetBrains Mono** (Google Fonts CDN) — all text
- All pages use monospace to reinforce terminal aesthetic

---

## React Component Patterns

### Shared Components — `themes/soc-components.js`

Loaded globally via `<script src="/themes/soc-components.js">` before any `type="text/babel"` script.
Exposes `window.SocComponents`. All detail pages destructure from it:

```javascript
const { SocClock, Icon, Section, Fig, resetFigCount, TipList, B, A, Code, CodeBlock, Img, dedent } = window.SocComponents;
```

| Export | Used by | Purpose |
|--------|---------|---------|
| `SocClock` | All detail pages | Live UTC clock via `useRef` + `setInterval` |
| `Icon` | All detail pages | Lucide icon wrapper (DOM injection, no JSX) |
| `Section` | 19 reviews + 6 research | H2 section with cyan icon, `res-section` class |
| `Fig` | 19 reviews | Auto-numbered figure (`figCount` module-level) |
| `resetFigCount` | 19 reviews | Resets figure counter — call at start of `App()` |
| `TipList` | 19 reviews | Styled `<ul>` for tips/takeaways |
| `B` | All detail pages | `<strong>` wrapper |
| `A` | 19 reviews | External link (new tab, `text-blue-600`) |
| `Code` | 19 reviews | Inline code (`bg-gray-100 px-1.5`) |
| `CodeBlock` | 6 research + 2 IR | Code block with language label; accepts `prefix` prop (`"res"` or `"ir"`) |
| `Img` | 6 research + 2 IR | Figure with caption; accepts `prefix` + `base` props |
| `dedent` | internal (CodeBlock) | Strips common indentation from template literal strings |

**IR and research pages use thin wrappers to pre-bind `prefix` and `base`:**
```javascript
// In research pages:
const { CodeBlock, Img: ImgBase } = window.SocComponents;
const Img = (props) => <ImgBase base={IMG} {...props} />;

// In IR pages:
const { CodeBlock: CB, Img: ImgBase } = window.SocComponents;
const CodeBlock = (props) => <CB prefix="ir" {...props} />;
const Img = (props) => <ImgBase base={IMG} prefix="ir" {...props} />;
```

### Components Still Defined Inline Per Page

| Component | Pages | Reason not extracted |
|-----------|-------|----------------------|
| `Callout` | Reviews, research, IR | 3 incompatible APIs (color prop vs type prop vs no prop) |
| `SubSection` | Research + IR | `res-subsection` vs `ir-subsection` class drift |
| `ReportSection` | IR reports | `ir-section` class, different color/icon — not same as `Section` |
| `ReportTable` | IR reports | `ir-table-wrap` / `ir-table` — different from research `Table` |
| `Finding` | IR reports | IR-only numbered finding card |
| `Table` | Research | `res-table-wrap` / `res-table` |
| `renderStars` | Reviews | Rating → star string helper |
| `Callout` | Reviews | Amber blockquote — API differs from research Callout |

### Data Loading Pattern

Every page fetches its metadata from the appropriate JSON on mount:

```javascript
const App = () => {
    const [meta, setMeta] = useState(null);
    useEffect(() => {
        fetch('/data/reviews.json')
            .then(r => r.json())
            .then(data => setMeta(data.find(r => r.url === '/reviews/[slug]/index.html')));
    }, []);
    // render using meta for cover, title, badges, etc.
};
```

### Hub Page Data Loading (index.html)

```javascript
// Main portfolio loads all JSON
useEffect(() => {
    Promise.all([
        fetch('/data/certifications.json').then(r => r.json()),
        fetch('/data/reviews.json').then(r => r.json()),
        fetch('/data/research.json').then(r => r.json()),
        fetch('/data/ir-reports.json').then(r => r.json()),
        fetch('/data/labs.json').then(r => r.json()),
        fetch('/data/labs_metadata.json').then(r => r.json()),
        fetch('/data/achievements.json').then(r => r.json()),
        fetch('/data/skills.json').then(r => r.json()),
    ]).then(([certs, reviews, research, irReports, labs, labsMeta, achievements, skills]) => {
        // merge labs + labsMeta
        const mergedLabs = labs.map(lab => ({ ...lab, ...(labsMeta[lab.title] || {}) }));
        setState({ certs, reviews, research, irReports, labs: mergedLabs, achievements, skills });
    });
}, []);
```

---

## JSON Data Schemas

### certifications.json

```json
[{
    "name": "OSCP - OffSec Certified Professional",
    "issuer": "OffSec",
    "year": "2025",
    "status": "Active",           // "Active" | "Expired"
    "category": "Offensive Security",
    "badge": "./assets/badges/oscp.png",
    "certificate": "./assets/certificates/oscp.jpg",
    "url": "https://credentials.offsec.com/..."
}]
```

### reviews.json

```json
[{
    "title": "...",
    "excerpt": "...",
    "date": "March 2025",
    "readTime": "15 min read",
    "tags": ["HTB CDSA", "Blue Team", "DFIR"],
    "url": "/reviews/cdsa/index.html",
    "image": "/assets/badges/cdsa.png",
    "difficulty": "Intermediate",   // "Beginner" | "Intermediate" | "Advanced"
    "rating": 4.8
}]
```

### research.json

```json
[{
    "slug": "anydesk-forensics-windows",
    "title": "...",
    "subtitle": "...",
    "date": "2026-01-10",           // ISO 8601
    "source": "Medium",             // "Original" | "Medium"
    "sourceUrl": "https://...",     // null if original
    "cover": "/assets/research/anydesk-forensics-windows/cover.png",
    "tags": ["Digital Forensics", "RMM", "AnyDesk", "Windows"],
    "category": "Digital Forensics", // "Digital Forensics" | "Red Teaming" | "Lab Making"
    "summary": "...",
    "url": "/research/anydesk-forensics-windows/index.html"
}]
```

### ir-reports.json

```json
[{
    "slug": "btlo-halloween-2025",
    "title": "Zeta-9 Security Incident Report",
    "subtitle": "BTLO Halloween 2025 Challenge",
    "date": "2025-11-01",
    "platform": "Blue Team Labs Online",
    "cover": "/assets/labs/btlo_halloween2025_ir_report.png",
    "tags": ["Incident Response", "Splunk", "Data Exfiltration"],
    "summary": "...",
    "url": "/ir-reports/btlo-halloween-2025/index.html"
}]
```

### labs.json

```json
[{
    "title": "UtensilMenace",
    "description": "...",
    "platform": "Blue Team Labs Online",
    "link": "https://...",
    "tags": ["Endpoint Forensics", "Windows Forensics"],
    "type": "lab",
    "difficulty": "easy",           // "easy" | "medium" | "hard"
    "player_difficulty": "medium",  // user's perceived difficulty
    "image": "./assets/labs/utensil.png",
    "rating": 4.5,                  // optional
    "is_retired": true,
    "tactics": ["TA0001", "TA0003"] // optional MITRE ATT&CK
}]
```

### labs_metadata.json

Generated by GitHub Actions. Merged with `labs.json` at render time:
```javascript
const labs = labsData.map(lab => ({ ...lab, ...(labsMeta[lab.title] || {}) }));
```

### achievements.json

```json
[
    {
        "category": "talk",
        "name": "Talk Title",
        "event": "Event Name",
        "year": "2026",
        "role": "Speaker",
        "image": "/assets/achievements/photo.png"
    },
    {
        "category": "competition",
        "name": "CTF Name",
        "organizer": "Null404",
        "placement": "Winner",       // "Winner" | "2nd" | etc.
        "year": "2026",
        "team": "TeamName",          // optional
        "description": "...",
        "image": "/assets/achievements/badge.png",
        "tags": ["CTF"]
    }
]
```

### skills.json

```json
[{
    "category": "Digital Forensics",
    "items": ["Disk Forensics", "Memory Forensics", "Network Forensics"]
}]
```

### social.json

```json
[{
    "platform": "GitHub",
    "url": "https://github.com/ChickenLoner",
    "handle": "@ChickenLoner",
    "svg": "M12 0C5.374 0..."        // SVG path data OR use "icon" for Lucide name
}]
```

---

## Routing

No router library. Pure filesystem routing.

| URL | File |
|-----|------|
| `/` | `/index.html` |
| `/reviews/` | `/reviews/index.html` |
| `/reviews/oscp/` | `/reviews/oscp/index.html` |
| `/research/` | `/research/index.html` |
| `/research/anydesk-forensics-windows/` | `/research/anydesk-forensics-windows/index.html` |
| `/ir-reports/` | `/ir-reports/index.html` |
| `/ir-reports/btlo-halloween-2025/` | `/ir-reports/btlo-halloween-2025/index.html` |

Navigation between pages uses standard `<a href>` links. `soc-nav.js` intercepts clicks and shows the UPLINK overlay animation before the browser navigates.

---

## Shared JS: soc-components.js

Provides all shared React components as plain `React.createElement` (no JSX, no Babel dependency).
Must load **after** React + Lucide, **before** any `type="text/babel"` script.

**Exports via `window.SocComponents`:**
`SocClock`, `Icon`, `dedent`, `CodeBlock`, `Img`, `Section`, `Fig`, `resetFigCount`, `TipList`, `B`, `A`, `Code`

See the [React Component Patterns](#react-component-patterns) section for usage.

---

## Shared JS: soc-nav.js

Injected globally via `<script src="/themes/soc-nav.js" defer>`.

**Behavior:**
1. On DOM ready: injects fixed overlay `#soc-nav-overlay` (progress bar + ring spinner + "UPLINK CONNECTING_" text)
2. On any internal link click: shows overlay, waits 420ms, then navigates
3. On page load: fades overlay out
4. Uses `sessionStorage` to track whether this is a first-load or navigation-load

**Does not affect:** External links (`target="_blank"`), anchor links (`#id`), `mailto:`, `tel:`

---

## Shared CSS: themes/soc.css

Provides:
1. CSS variable definitions (same palette as inline `:root` — shared for non-self-contained contexts)
2. Tailwind `.dark` class overrides to remap Tailwind colors to SOC palette
3. Global scrollbar styling (custom dark scrollbar)

Tailwind utility equivalents (~140 classes) were added to `soc.css` during O2 so detail pages don't need the Tailwind CDN.

**Note:** Each page also declares `:root` inline for self-containment. `soc.css` is the canonical reference.

---

## Python Automation Scripts

### _soc_reviews_full.py

Batch script to apply SOC theme to all review pages.

**Run:** `python _soc_reviews_full.py`

**What it changes:**
- Replaces `<style>` block with standardized SOC CSS
- Injects `SocClock` and `Section` components
- Updates topbar breadcrumbs
- Standardizes cover, meta grid, TOC, footer structure
- Safe to re-run (idempotent)

### _soc_research_articles.py

Same purpose for research pages.

**Additional logic:** Maps research category to severity badge color.

### scripts/update_lab_data.py

Fetches lab stats from external platform APIs (HackTheBox, TryHackMe, CyberDefenders). Writes to `data/labs_metadata.json`. Run by GitHub Actions on a daily schedule.

---

## CI/CD

### .github/workflows/static.yml

- **Trigger:** Push to `main`
- **Action:** Deploy site to GitHub Pages
- **URL:** https://chickenloner.github.io

### .github/workflows/update_lab_data.yml

- **Trigger:** Daily cron + manual dispatch
- **Action:** `python scripts/update_lab_data.py` → commit `data/labs_metadata.json` → push to main

---

## Adding New Content

### New Certification Review

1. Add entry to `data/reviews.json`
2. Add cert to `data/certifications.json` (if not present)
3. Drop badge PNG into `assets/badges/`
4. Create `reviews/[slug]/index.html` using an existing review as template
5. Update `reviews/index.html` hub (if it doesn't auto-load from JSON — verify)

### New Research Article

1. Add entry to `data/research.json`
2. Add cover to `assets/research/[slug]/cover.png`
3. Create `research/[slug]/index.html` using existing research page as template
4. Run `python _soc_research_articles.py` if bulk restyling is needed

### New IR Report

1. Add entry to `data/ir-reports.json`
2. Add cover to `assets/reports/[slug]/cover.png` (or `assets/labs/`)
3. Create `ir-reports/[slug]/index.html` using existing IR report as template

### New Lab Entry

1. Add entry to `data/labs.json`
2. Add cover to `assets/labs/`

---

## External Dependencies (All CDN — No Local Bundling)

| Library | Pinned version | Purpose | Pages |
|---------|---------------|---------|-------|
| Tailwind CSS | 3.4.17 | Utility classes | Hub pages only (not detail pages) |
| React | 18 | UI rendering | All pages |
| ReactDOM | 18 | DOM mounting | All pages |
| Babel Standalone | 7.29.2 | JSX transpilation in-browser | All pages |
| Lucide | 1.14.0 | Icons | All pages |
| Google Fonts (JetBrains Mono) | — | Monospace font | All pages |

**No build step.** Everything runs directly in the browser. Babel transpiles JSX at runtime via `<script type="text/babel">`.

Detail pages (reviews, research, IR reports) do **not** load Tailwind CDN — utility equivalents live in `soc.css`.

---

## Conventions & Constraints

- **Dark mode only.** No light mode support.
- **No backend.** Pure static HTML/JS/CSS + JSON.
- **No router library.** Filesystem-based routing.
- **Self-contained pages.** CSS variables declared inline in every page so pages work without `/themes/soc.css`.
- **OG/Twitter meta required on all pages.** Memory note: always include when creating new pages.
- **JetBrains Mono everywhere.** Monospace font is core to the SOC aesthetic.
- **Shared components via `soc-components.js`.** `Icon`, `SocClock`, `Section`, `Fig`, `CodeBlock`, `Img`, `TipList`, `B`, `A`, `Code`, `dedent` are loaded from `themes/soc-components.js` (plain `React.createElement`, no JSX). Per-page components (`Callout`, `SubSection`, `ReportSection`, etc.) remain inline. No module bundler — `window.SocComponents` is the injection point.
- **Assets co-located by content type.** `/assets/research/[slug]/` for research, `/assets/reports/[slug]/` for IR, `/assets/badges/` for all cert badges.
- **Favicon:** `/chicken0248.png` (used on all pages).

---
name: new-ir-report
description: Scaffolds a complete IR report page for ChickenLoner.github.io from the user's writeup notes. Use this skill when the user wants to publish a new incident response report, create an IR writeup page, or document a CTF/competition challenge as an IR report. Triggers on phrases like "new IR report", "create IR report", "publish IR writeup", "add report for [challenge name]", or when the user shares incident response notes.
---

# New IR Report

Scaffolds a complete, styled IR report page from the user's notes, following the established `htb-tinsel-trace-1` template pattern (SOC Console dark theme).

## Step 1 — Gather required info

Ask for any missing fields not provided in the user's message:

| Field | Notes |
|---|---|
| `slug` | URL folder name, e.g. `htb-sherlock-xyz` — lowercase, hyphenated |
| `title` | Full report title, e.g. `"Operation Tinsel Trace I — IR Report"` |
| `subtitle` | Platform context, e.g. `"Hack The Box — Festive Sherlocks 2023"` |
| `platform` | `"Hack The Box"`, `"Blue Team Labs Online"`, etc. |
| `date` | ISO date `"YYYY-MM-DD"` |
| `tags` | Array of relevant tags, e.g. `["Incident Response", "Ransomware", "Active Directory"]` |
| `summary` | 1–2 sentence description of the incident investigated |
| `cover` | Cover image path — default `"/assets/labs/<slug>.jpg"` if not specified |
| `writeup` | The user's notes/writeup content — ask them to paste it or point to a file |

## Step 2 — Prepare assets directory

```bash
mkdir -p assets/reports/<slug>
```

If the user has images for the report, copy them to `assets/reports/<slug>/`. Name them `img-01.png`, `img-02.png`, etc. in the order they appear.

If a cover image exists at `assets/labs/<slug>.*`, note its path — it will be used in the listing card.

## Step 3 — Add entry to ir-reports.json

1. Read `data/ir-reports.json`.
2. Prepend a new entry (most recent first):

```json
{
  "slug": "<slug>",
  "title": "<title>",
  "subtitle": "<subtitle>",
  "date": "<date>",
  "platform": "<platform>",
  "cover": "/assets/labs/<slug>.jpg",
  "tags": [...],
  "summary": "<summary>",
  "url": "/ir-reports/<slug>/index.html"
}
```

## Step 4 — Scaffold ir-reports/<slug>/index.html

Use `ir-reports/htb-tinsel-trace-1/index.html` as the canonical template. Do not diverge from its patterns.

### 4a. Head section (required)

```html
<title><title> | Chicken0248</title>
<meta name="description" content="<summary>" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Chicken0248" />
<meta property="og:url" content="https://chickenloner.github.io/ir-reports/<slug>/" />
<meta property="og:title" content="<title>" />
<meta property="og:description" content="<summary>" />
<meta property="og:image" content="https://chickenloner.github.io/assets/labs/<slug>.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@Chicken_0248" />
<meta name="twitter:title" content="<title>" />
<meta name="twitter:description" content="<summary>" />
<meta name="twitter:image" content="https://chickenloner.github.io/assets/labs/<slug>.jpg" />
<link rel="icon" href="/chicken0248.png" type="image/png">
```

Also include JetBrains Mono font and the SOC stylesheet:
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/themes/soc.css">
```

### 4b. Components

Load shared components from `window.SocComponents`. Include the script tag **before** the `type="text/babel"` script:

```html
<!-- In <head>, after lucide script -->
<script src="/themes/soc-components.js"></script>
```

At the top of `<script type="text/babel">`:
```js
const { SocClock, Icon, CodeBlock: CB, Img: ImgBase } = window.SocComponents;
const IMG = '/assets/reports/<slug>';
const CodeBlock = (props) => <CB prefix="ir" {...props} />;
const Img = (props) => <ImgBase base={IMG} prefix="ir" {...props} />;
```

| Source | Component | Purpose |
|--------|-----------|---------|
| `window.SocComponents` | `SocClock` | Live UTC clock via `useRef` + `setInterval` — no React state re-renders |
| `window.SocComponents` | `Icon` | Lucide icon wrapper |
| `window.SocComponents` (via wrapper) | `CodeBlock` | Dark code block (`ir-code-wrap`) with language label |
| `window.SocComponents` (via wrapper) | `Img` | Figure (`ir-figure`) with caption, auto-prefixed with `IMG` |
| Inline | `ReportSection` | H2 section with red icon box, scroll anchor, `ir-section` class |
| Inline | `SubSection` | H3 subheading with red left border (`ir-subsection`) |
| Inline | `ReportTable` | SOC-styled table (`ir-table-wrap` / `ir-table`) with headers + rows |
| Inline | `Finding` | Red-badged finding card (`ir-finding`) with number + title |
| Inline | `B` | `<strong>` wrapper — renders `var(--soc-ink)` white |
| Inline | `C` | Inline code (`ir-c`) — cyan monospace on dark background |

Copy `ReportSection`, `SubSection`, `ReportTable`, `Finding`, `B`, `C` verbatim from `ir-reports/htb-tinsel-trace-1/index.html`.

### 4c. SOC top bar

The page uses a sticky SOC Console top bar instead of a nav — no dark mode toggle:

```
UPLINK  •  SOC / OPERATOR.PROFILE / IR.REPORTS / <SLUG>  •  [TLP:CLEAR]  [IR.REPORT]  [clock]
```

Breadcrumb links: `SOC` → `/`, `OPERATOR.PROFILE` → `/`, `IR.REPORTS` → `/ir-reports/index.html`, then bold slug.
Badges: `sev cyan` for `TLP:CLEAR`, `sev red` for `IR.REPORT`.

### 4d. Standard TOC items

Default sections for an IR report (adjust based on the user's writeup structure):

```js
const tocItems = [
  { id: 'executive-summary', label: 'Executive Summary', icon: 'FileText' },
  { id: 'timeline',          label: 'Timeline',          icon: 'Clock' },
  { id: 'scope-evidence',    label: 'Scope & Evidence',  icon: 'Database' },
  { id: 'findings',          label: 'Findings',          icon: 'Search' },
  { id: 'iocs',              label: 'Indicators of Compromise', icon: 'AlertTriangle' },
  { id: 'recommendations',   label: 'Recommendations',   icon: 'Shield' },
  { id: 'appendix',          label: 'Appendix',          icon: 'Paperclip' },
];
```

Remove sections not covered in the user's writeup. Add custom sections as needed.

### 4e. Page structure (in order)

1. **SOC top bar** — sticky, `soc-tb` class, breadcrumb + sev badges + `<SocClock />`
2. **Cover** (`ir-cover`) — cover image with dark gradient overlay, title, subtitle pill badges, platform, date
3. **Meta grid** (`ir-meta-grid`) — Platform, Date, Difficulty/Severity, Category columns
4. **TOC** (`ir-toc`) — `// TABLE OF CONTENTS` header, one link per section
5. **Report sections** — render user's writeup content using components above
6. **Footer** (`soc-ft`) — `← ALL REPORTS` and `↑ BACK TO TOP` links

### 4f. Content rendering rules

| Writeup element | Output |
|---|---|
| Main heading | `<ReportSection id="..." title="..." icon="...">` |
| Subheading | `<SubSection title="...">` |
| Paragraph | `<p className="ir-p">` |
| Bullet list | `<ul><li className="ir-li">...</li></ul>` |
| Code / command | `<CodeBlock language="...">` or inline `<C>` |
| Table | `<ReportTable headers={[...]} rows={[[...]]} />` |
| Image | `<Img src="img-NN.png" alt="..." caption="..." />` |
| Key finding | `<Finding number={N} title="...">` |
| Bold | `<B>` |
| Inline code | `<C>` |

### 4g. Section icon suggestions

| Section | Icon |
|---|---|
| Executive Summary | `FileText` |
| Timeline | `Clock` |
| Scope & Evidence | `Database` |
| Findings | `Search` |
| IOCs | `AlertTriangle` |
| Recommendations | `Shield` |
| Appendix | `Paperclip` |
| Lateral Movement | `Network` |
| Persistence | `Lock` |
| Exfiltration | `Upload` |
| Credentials | `Key` |

## Step 5 — Verify

- [ ] Meta tags present with correct slug URLs
- [ ] `data/ir-reports.json` has the new entry prepended
- [ ] `ir-reports/<slug>/index.html` created
- [ ] `IMG` const set to `/assets/reports/<slug>`
- [ ] SOC Console CSS block present (copied from template)
- [ ] SOC top bar breadcrumb shows correct slug
- [ ] TOC links match actual section IDs
- [ ] JetBrains Mono font link in `<head>`

## Step 6 — Commit

```bash
git add ir-reports/<slug>/ data/ir-reports.json assets/reports/<slug>/
git commit -m "add IR report: <title>"
git push origin main
```

## Reference files

- `ir-reports/htb-tinsel-trace-1/index.html` — canonical IR report template (SOC Console theme)
- `data/ir-reports.json` — report listing metadata
- `ir-reports/index.html` — listing page (for card rendering context)

---
name: new-ir-report
description: Scaffolds a complete IR report page for ChickenLoner.github.io from the user's writeup notes. Use this skill when the user wants to publish a new incident response report, create an IR writeup page, or document a CTF/competition challenge as an IR report. Triggers on phrases like "new IR report", "create IR report", "publish IR writeup", "add report for [challenge name]", or when the user shares incident response notes.
---

# New IR Report

Scaffolds a complete, styled IR report page from the user's notes, following the established `htb-tinsel-trace-1` template pattern.

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

If the user has images for the report, copy them to `assets/reports/<slug>/`. Name them `image-1.png`, `image-2.png`, etc. in the order they appear.

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

### 4b. Components (copy verbatim from template)

| Component | Purpose |
|---|---|
| `Icon` | Lucide icon wrapper |
| `ReportSection` | H2 section with red icon, scroll anchor |
| `SubSection` | H3 subheading |
| `ReportTable` | Styled table with headers + rows |
| `CodeBlock` | Dark code block with language label |
| `Img` | Figure with caption, references `IMG` const |
| `Finding` | Red-badged finding card with number + title |
| `B` | `<strong>` wrapper |
| `C` | Inline `<code>` in red monospace |

Set `const IMG = '/assets/reports/<slug>';` at the top of the script.

### 4c. Standard TOC items

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

### 4d. Page structure (in order)

1. **Nav** — `Chicken0248 / IR Reports / <title>` breadcrumb + dark mode toggle
2. **Hero** — cover image with dark gradient overlay, title, subtitle, platform badge, date
3. **TOC sidebar** — sticky left panel on desktop, inline on mobile
4. **Report sections** — render user's writeup content using components above
5. **Footer** — "Back to top" + links to `/ir-reports/index.html`

### 4e. Content rendering rules

| Writeup element | HTML output |
|---|---|
| Main heading | `<ReportSection id="..." title="..." icon="...">` |
| Subheading | `<SubSection title="...">` |
| Paragraph | `<p className="text-gray-700 leading-relaxed">` |
| Code/command | `<CodeBlock language="...">` or inline `<C>` |
| Table | `<ReportTable headers={[...]} rows={[[...]]} />` |
| Image | `<Img src="image-N.png" alt="..." caption="..." />` |
| Key finding | `<Finding number={N} title="...">` |
| Bold | `<B>` |
| Inline code | `<C>` |

### 4f. Section icon suggestions

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
- [ ] `data/ir-reports.json` has the new entry
- [ ] `ir-reports/<slug>/index.html` created
- [ ] `IMG` const set to `/assets/reports/<slug>`
- [ ] Nav breadcrumb shows correct title
- [ ] Dark mode CSS block present (copied from template)
- [ ] TOC links match actual section IDs

## Step 6 — Commit

```bash
git add ir-reports/<slug>/ data/ir-reports.json assets/reports/<slug>/
git commit -m "add IR report: <title>"
git push origin main
```

## Reference files

- `ir-reports/htb-tinsel-trace-1/index.html` — canonical IR report template
- `data/ir-reports.json` — report listing metadata
- `ir-reports/index.html` — listing page (for card rendering context)

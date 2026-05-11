---
name: new-research
description: Scaffolds a complete research article page for ChickenLoner.github.io from the user's notes. Use this skill when the user wants to publish a new research post, forensics investigation guide, or technical deep dive. Triggers on phrases like "new research", "create research page", "publish research", "add research for [topic]", or when the user shares investigation notes or technical writeup content.
---

# New Research Page

Scaffolds a complete, styled research article from the user's notes, following the SOC Console dark theme established in the existing research articles.

## Step 1 — Gather required info

Ask for any missing fields not provided in the user's message:

| Field | Notes |
|---|---|
| `slug` | URL folder name, e.g. `teamviewer-forensics-windows` — lowercase, hyphenated |
| `title` | Full article title |
| `subtitle` | One-line description of scope |
| `date` | ISO date `"YYYY-MM-DD"` |
| `source` | `"Original"` (written here first) or `"Medium"` (migrated) |
| `sourceUrl` | Medium URL if source is Medium, else `""` |
| `category` | Broad topic — see accent color table below |
| `tags` | Array of tags, e.g. `["Digital Forensics", "RMM", "Windows"]` |
| `summary` | 1–2 sentence description for the listing card |
| `cover` | Cover image — default `"/assets/research/<slug>/cover.png"` |
| `content` | User's notes/writeup — ask them to paste or point to a file |

### Category → accent color mapping

| Category | Sev color | Used for |
|---|---|---|
| `Digital Forensics` | `cyan` | RMM investigation, artifact analysis, DFIR |
| `Red Teaming` | `red` | Offensive techniques, persistence, TTPs |
| `Lab Making` | `amber` | Lab design, environment setup guides |

If the category doesn't fit these three, choose the closest one and note it.

## Step 2 — Prepare assets

1. Create directories:
```bash
mkdir -p research/<slug>
mkdir -p assets/research/<slug>
```

2. If the user provides images, copy them to `assets/research/<slug>/`:
   - Cover/hero → `cover.png`
   - Article images → `img-01.png`, `img-02.png`, etc. in order of appearance

## Step 3 — Add entry to research.json

1. Read `data/research.json`.
2. Prepend a new entry (most recent first):

```json
{
  "slug": "<slug>",
  "title": "<title>",
  "subtitle": "<subtitle>",
  "date": "<date>",
  "source": "<source>",
  "sourceUrl": "<sourceUrl>",
  "cover": "/assets/research/<slug>/cover.png",
  "tags": [...],
  "category": "<category>",
  "summary": "<summary>",
  "url": "/research/<slug>/index.html"
}
```

## Step 4 — Scaffold research/<slug>/index.html

Use `research/anydesk-forensics-windows/index.html` as the canonical template. Do not diverge from its patterns.

### 4a. Head section (required)

```html
<title><title> | Chicken0248</title>
<meta name="description" content="<summary>" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Chicken0248" />
<meta property="og:url" content="https://chickenloner.github.io/research/<slug>/" />
<meta property="og:title" content="<title>" />
<meta property="og:description" content="<summary>" />
<meta property="og:image" content="https://chickenloner.github.io/assets/research/<slug>/cover.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@Chicken_0248" />
<meta name="twitter:title" content="<title>" />
<meta name="twitter:description" content="<summary>" />
<meta name="twitter:image" content="https://chickenloner.github.io/assets/research/<slug>/cover.png" />
<link rel="icon" href="/chicken0248.png" type="image/png">
```

Also include JetBrains Mono font and the SOC stylesheet:
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/themes/soc.css">
```

### 4b. Components (copy verbatim from template)

| Component | Purpose |
|---|---|
| `SocClock` | Live UTC clock via `useRef` + `setInterval` — no React state re-renders |
| `Icon` | Lucide icon wrapper |
| `Section` | H2 section with cyan icon box (`res-section-icon`), scroll anchor |
| `SubSection` | H3 subheading with cyan left border (`res-subsection`) |
| `CodeBlock` | Dark code block (`res-code-wrap`) with language label in JetBrains Mono |
| `Img` | Figure (`res-figure`) with caption, references `IMG` const, horizontally centered |
| `Callout` | Alert block (`res-callout info/warning/tip`) with colored icon |
| `Table` | SOC-styled table (`res-table-wrap` / `res-table`) with `headers` + `rows` arrays |
| `B` | `<strong>` wrapper — renders `var(--soc-ink)` |
| `C` | Inline code (`res-c`) — cyan monospace on dark background |

Set `const IMG = '/assets/research/<slug>';` at the top of the script.

The **accent color is always cyan** for the section icons and subsection borders regardless of article category. Category only affects the topbar badge and cover badge sev class.

### 4c. SOC top bar

Sticky top bar — no dark mode toggle:

```
UPLINK  •  SOC / OPERATOR.PROFILE / RESEARCH / <SLUG>  •  [TLP:CLEAR]  [CATEGORY]  [clock]
```

- Breadcrumb: `SOC` → `/`, `OPERATOR.PROFILE` → `/`, `RESEARCH` → `/research/index.html`, then bold `<SLUG>` (e.g. `ANYDESK.FORENSICS.WINDOWS`)
- Badges: `sev cyan` for `TLP:CLEAR`, `sev <cat-sev>` for the category (e.g. `sev cyan DIGITAL FORENSICS`)

### 4d. Page structure (in order)

1. **SOC top bar** — sticky, `soc-tb` class, breadcrumb + sev badges + `<SocClock />`
2. **Cover** (`res-cover`) — cover image `${IMG}/cover.png` with dark gradient overlay, `<h1>` title, date badge + category sev badge
3. **Meta grid** (`res-meta-grid`) — Author (`Chicken0248`), Published (date), Originally on (Medium link if applicable), Category
4. **TOC** (`res-toc`) — `// TABLE OF CONTENTS` header, `res-toc-grid` with icon + number + label per section
5. **Content sections** — render writeup using `<Section>` components
6. **Footer** (`soc-ft`) — `← ALL RESEARCH` and `↑ BACK TO TOP`

### 4e. Content rendering rules

| Writeup element | Output |
|---|---|
| Main heading | `<Section id="..." title="..." icon="...">` |
| Subheading | `<SubSection title="...">` |
| Paragraph | `<p>` (SOC global `p` rule applies color and size) |
| Bullet list | `<ul><li>...</li></ul>` inside a Section (`.res-section ul` applies `list-style-type:disc`) |
| Ordered list | `<ol><li>...</li></ol>` inside a Section |
| Code block | `<CodeBlock language="bash">...</CodeBlock>` |
| Inline code / path | `<C>value</C>` |
| Bold | `<B>text</B>` |
| Table | `<Table headers={['Col1','Col2']} rows={[['a','b'],['c','d']]} />` — rows support HTML strings via `dangerouslySetInnerHTML` |
| Image | `<Img src="img-NN.png" alt="..." caption="..." />` |
| Info callout | `<Callout type="info"><p>...</p></Callout>` — cyan border |
| Warning callout | `<Callout type="warning"><p>...</p></Callout>` — amber border |
| Tip callout | `<Callout type="tip"><p>...</p></Callout>` — green border |
| External link | `<a href="..." target="_blank" rel="noopener noreferrer">label</a>` — SOC `a` rule applies cyan color |

### 4f. Section icon suggestions

| Section topic | Icon |
|---|---|
| Introduction / overview | `BookOpen` |
| Terminology / glossary | `BookMarked` |
| Installation / setup | `Package` |
| Usage & behavior | `Monitor` |
| CLI / commands | `Terminal` |
| Artifacts / evidence | `Database` |
| Network / connections | `Network` |
| File transfer | `FolderOpen` |
| Logging / events | `ScrollText` |
| Detection / hunting | `Search` |
| Persistence | `Lock` |
| Unattended access | `Lock` |
| Self-hosting / config | `Server` |
| Decryption / crypto | `Key` |
| Conclusion / summary | `CheckCircle` |

Use `FileText` as a safe default.

## Step 5 — Verify

- [ ] Meta tags present with correct slug URLs
- [ ] `data/research.json` has the new entry prepended
- [ ] `research/<slug>/index.html` created
- [ ] `IMG` const set to `/assets/research/<slug>`
- [ ] SOC Console CSS block present (copied from template) with Tailwind class overrides
- [ ] SOC top bar breadcrumb and badges correct (slug, category sev color)
- [ ] Cover image path correct (`${IMG}/cover.png`)
- [ ] TOC links match actual section IDs
- [ ] JetBrains Mono font link in `<head>`
- [ ] All `<ul>` / `<ol>` lists are inside a `<Section>` so `.res-section ul` CSS applies disc bullets

## Step 6 — Commit

```bash
git add research/<slug>/ data/research.json assets/research/<slug>/
git commit -m "add research: <title>"
git push origin main
```

## Reference files

- `research/anydesk-forensics-windows/index.html` — canonical research article template (SOC Console theme, Digital Forensics)
- `research/git-commits-persistence/index.html` — Red Teaming category example (red sev badge)
- `research/windows-forensics-lab/index.html` — Lab Making category example (amber sev badge)
- `data/research.json` — research listing metadata
- `research/index.html` — listing page (for card rendering context)

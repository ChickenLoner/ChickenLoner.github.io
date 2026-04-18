---
name: new-research
description: Scaffolds a complete research article page for ChickenLoner.github.io from the user's notes. Use this skill when the user wants to publish a new research post, forensics investigation guide, or technical deep dive. Triggers on phrases like "new research", "create research page", "publish research", "add research for [topic]", or when the user shares investigation notes or technical writeup content.
---

# New Research Page

Scaffolds a complete, styled research page from the user's notes, following the `anydesk-forensics-windows` template pattern.

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
| `category` | Broad topic: `"Digital Forensics"`, `"Red Teaming"`, `"Lab Making"`, etc. |
| `tags` | Array of tags, e.g. `["Digital Forensics", "RMM", "Windows"]` |
| `summary` | 1–2 sentence description for the listing card |
| `cover` | Cover image — default `"/assets/research/<slug>/cover.png"` |
| `content` | User's notes/writeup — ask them to paste or point to a file |

## Step 2 — Prepare assets

1. Create the page and assets directories:
```bash
mkdir -p research/<slug>
mkdir -p assets/research/<slug>
```

2. If the user provides images, copy them to `assets/research/<slug>/` named `cover.png` (hero) then `image-1.png`, `image-2.png`, etc.

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

### 4b. Components (copy verbatim from template)

| Component | Purpose |
|---|---|
| `Icon` | Lucide icon wrapper |
| `Section` | H2 section with indigo icon, scroll anchor |
| `SubSection` | H3 subheading block |
| `CodeBlock` | Dark code block with language label |
| `Img` | Figure with optional caption, references `IMG` const |
| `B` | `<strong>` wrapper |
| `A` | External link opener |

Set `const IMG = '/assets/research/<slug>';` at the top of the script.

The accent color for research pages is **indigo** (`text-indigo-600`, `bg-indigo-50`) — not red (that's IR reports) or amber (that's reviews).

### 4c. Page structure (in order)

1. **Nav** — `Chicken0248 / Research / <title>` breadcrumb + dark mode toggle
2. **Hero** — cover image with gradient overlay, title, subtitle, category badge, date, source badge (Original / Medium)
3. **TOC** — sticky sidebar on desktop, inline on mobile — one link per Section
4. **Content sections** — render the writeup using components above
5. **Footer** — "Back to top" + link to `/research/index.html`

### 4d. Content rendering rules

| Writeup element | HTML output |
|---|---|
| Main heading (`##`) | `<Section id="..." title="..." icon="...">` |
| Subheading (`###`) | `<SubSection title="...">` |
| Paragraph | `<p className="text-gray-700 leading-relaxed">` |
| Code block | `<CodeBlock language="bash/powershell/python/etc">` |
| Inline code | `` `code` `` → `<code className="bg-gray-100 text-indigo-700 px-1.5 py-0.5 rounded text-sm font-mono">` |
| Table | `<div className="overflow-x-auto">` with styled `<table>` |
| Image | `<Img src="image-N.png" alt="..." caption="..." />` |
| Callout/note | `<div className="bg-indigo-50 border-l-4 border-indigo-400 rounded-r-xl p-4 text-indigo-900">` |
| Bold | `<B>` |
| External link | `<A href="...">` |

### 4e. Section icon suggestions

| Section topic | Icon |
|---|---|
| Introduction / overview | `BookOpen` |
| Installation / setup | `Package` |
| Behavior / how it works | `Activity` |
| Artifacts / evidence | `Database` |
| Registry | `Settings` |
| Network / connections | `Network` |
| File transfer | `FolderOpen` |
| Logging / events | `ScrollText` |
| Detection / hunting | `Search` |
| CLI / commands | `Terminal` |
| Persistence | `Lock` |
| Conclusion / summary | `CheckCircle` |

Use `FileText` as a safe default.

## Step 5 — Verify

- [ ] Meta tags present with correct slug URLs
- [ ] `data/research.json` has the new entry prepended
- [ ] `research/<slug>/index.html` created
- [ ] `IMG` const set to `/assets/research/<slug>`
- [ ] Nav breadcrumb shows correct title
- [ ] Dark mode CSS block present (copied from template)
- [ ] Cover image referenced correctly in hero
- [ ] TOC links match actual section IDs

## Step 6 — Commit

```bash
git add research/<slug>/ data/research.json assets/research/<slug>/
git commit -m "add research: <title>"
git push origin main
```

## Reference files

- `research/anydesk-forensics-windows/index.html` — canonical research page template
- `data/research.json` — research listing metadata
- `research/index.html` — listing page (for card rendering context)

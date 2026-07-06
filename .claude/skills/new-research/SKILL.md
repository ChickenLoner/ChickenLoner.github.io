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
| `cover` | Cover image — default `"/assets/research/<slug>/cover.png"` or `cover.jpg` |
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
   - Cover/hero → `cover.png` or `cover.jpg`
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

Read `.claude/skills/new-research/template.html` as your starting point. Replace every `{{PLACEHOLDER}}` with the real value, then fill in the content sections. Do not diverge from the template structure without a reason.

### Placeholder reference

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | URL folder name, e.g. `anydesk-forensics-windows` |
| `{{SLUG_BREADCRUMB}}` | Dotted uppercase for breadcrumb, e.g. `ANYDESK.FORENSICS.WINDOWS` |
| `{{TITLE}}` | Full article title |
| `{{DESCRIPTION}}` | Meta description (1–2 sentences) |
| `{{DATE_DISPLAY}}` | Human-readable date, e.g. `January 10, 2026` |
| `{{DATE_ISO}}` | ISO date for JSON-LD `datePublished`, same as `date`, e.g. `2026-01-10` |
| `{{CAT_SEV}}` | Sev class: `cyan` (Digital Forensics), `red` (Red Teaming), `amber` (Lab Making) |
| `{{CATEGORY}}` | Category label, e.g. `Digital Forensics` |
| `{{CATEGORY_UPPER}}` | Uppercase for topbar badge, e.g. `DIGITAL FORENSICS` |
| `{{MEDIUM_URL}}` | Medium article URL, or remove the `<a>` and use `<div className="res-meta-val">Original</div>` |
| `{{SECTION_N_ID}}` | Kebab-case anchor, e.g. `artifact-analysis` |
| `{{SECTION_N_LABEL}}` | Section display name |
| `{{SECTION_N_ICON}}` | Lucide icon name (see 4b below) |
| `{{CONTENT}}` | Replace with actual JSX content |
| `{{ALT_TEXT}}` / `{{CAPTION}}` | Image descriptions |

**`IMG` is auto-derived from the URL** — no placeholder needed, already in the template.

**Accent color is always cyan** for Section icons and SubSection borders, regardless of category. Category only affects the topbar badge and cover badge.

### 4a. Components (all in template)

| Component | Purpose |
|---|---|
| `Section` | H2 section with cyan icon box and scroll anchor |
| `SubSection` | H3 subheading with cyan left border |
| `CodeBlock` | Dark code block with language label in JetBrains Mono |
| `Img` | Figure with caption (pre-wired to `IMG` path) |
| `Table` | SOC-styled table; cells support HTML strings |
| `Callout` | Alert block — `type="info"` (cyan), `"warning"` (amber), `"tip"` (green) |
| `B` | `<strong>` wrapper |
| `C` | Inline code (`res-c` class) |

### 4b. Content rendering rules

| Writeup element | Output |
|---|---|
| Main heading | `<Section id="..." title="..." icon="...">` |
| Subheading | `<SubSection title="...">` |
| Paragraph | `<p className="text-gray-700 leading-relaxed">` |
| Bullet list | `<ul><li>` inside a Section (`.res-section ul` applies disc bullets) |
| Ordered list | `<ol><li>` inside a Section |
| Code block | `<CodeBlock language="bash">...</CodeBlock>` |
| Inline code / path | `<C>value</C>` |
| Bold | `<B>text</B>` |
| Table | `<Table headers={['Col1']} rows={[['val']]} />` |
| Image | `<Img src="img-NN.png" alt="..." caption="..." />` |
| Callout | `<Callout type="info|warning|tip"><p>...</p></Callout>` |
| External link | `<a href="..." target="_blank" rel="noopener noreferrer">label</a>` |

### 4c. Section icon suggestions

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
| Self-hosting / config | `Server` |
| Decryption / crypto | `Key` |
| Conclusion / summary | `CheckCircle` |

Use `FileText` as a safe default.

## Writing style rules

These apply to all prose written by this skill:

- **No em dashes (—)**. Never use `—` in body text. Replace with: a comma, a colon, parentheses, or rewrite into two sentences.
- **Write like a human researcher, not a document generator.** Vary sentence length. Mix short direct statements with longer explanations. Don't start every paragraph the same way.
- **Avoid AI filler phrases**: "it's worth noting", "it is important to", "it should be noted", "in order to", "this allows you to", "overall", "in conclusion". Cut or rewrite.
- **Active voice preferred.** "TeamViewer stores logs in `%AppData%`" not "Logs are stored in `%AppData%` by TeamViewer."
- **Technical precision over verbosity.** One clear sentence beats three vague ones. Don't explain what the reader can infer.
- **Don't pad.** If a section has little to say, say little. Don't add filler sentences to fill visual space.

## Step 5 — Verify

- [ ] No `{{PLACEHOLDER}}` markers left in the output file
- [ ] Meta tags present with correct slug URLs
- [ ] `data/research.json` has the new entry prepended
- [ ] `research/<slug>/index.html` created
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

- `.claude/skills/new-research/template.html` — page template with `{{PLACEHOLDER}}` markers (start here)
- `data/research.json` — research listing metadata
- `research/index.html` — listing page (for card rendering context)

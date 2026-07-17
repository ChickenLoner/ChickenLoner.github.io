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

Read `.claude/skills/new-ir-report/template.html` as your starting point. Replace every `{{PLACEHOLDER}}` with the real value, then fill in the content sections. Do not diverge from the template structure without a reason.

### Placeholder reference

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | URL folder name, e.g. `htb-tinsel-trace-1` |
| `{{SLUG_UPPER}}` | Uppercased with hyphens for breadcrumb, e.g. `TINSEL-TRACE-1` |
| `{{TITLE}}` | Full report title |
| `{{DESCRIPTION}}` | Meta description (1–2 sentences) |
| `{{COVER_PATH}}` | Path from site root, e.g. `assets/labs/htb-tinsel-trace-1.jpg` |
| `{{INCIDENT_ID}}` | Incident identifier, e.g. `HTB-OpTinselTrace-2023` |
| `{{DATE_RANGE}}` | Incident period, e.g. `November – December 2023` |
| `{{REPORT_DATE}}` | Date report was written, e.g. `April 7, 2026` |
| `{{DATE_ISO}}` | ISO form of the report date for JSON-LD `datePublished`, e.g. `2026-04-07` |
| `{{CONTENT}}` | Replace with actual JSX content |
| `{{FINDING_TITLE}}` | Finding title text |
| `{{IOC}}` / `{{HASH}}` / `{{FILENAME}}` | IOC values |
| `{{REC_TITLE}}` / `{{REC_DETAIL}}` | Recommendation items |
| `{{APPENDIX_SECTION}}` | Appendix subsection title |

**`IMG` is auto-derived from the URL** — no placeholder needed, already in the template.

### 4a. Components (all in template)

| Component | Purpose |
|---|---|
| `ReportSection` | H2 section with red icon box and scroll anchor |
| `SubSection` | H3 subheading with red left border |
| `ReportTable` | SOC-styled table; cells support HTML strings via `dangerouslySetInnerHTML` |
| `Finding` | Red-badged finding card; use `variant="vi"` for malware analysis blocks |
| `CodeBlock` | Dark code block with language label (pre-wrapped with `prefix="ir"`) |
| `Img` | Figure with caption (pre-wired to `IMG` path) |
| `B` | `<strong>` wrapper |
| `C` | Inline code (`ir-c` class) |

### 4b. Content rendering rules

| Writeup element | Output |
|---|---|
| Main heading | `<ReportSection id="..." title="..." icon="...">` |
| Subheading | `<SubSection title="...">` |
| Paragraph | `<p className="ir-p">` |
| Bullet list | `<ul style={{paddingLeft:'20px',margin:'0'}}><li className="ir-li">` |
| Code / command | `<CodeBlock language="...">` or inline `<C>` |
| Table | `<ReportTable headers={[...]} rows={[[...]]} />` |
| Image | `<Img src="img-NN.png" alt="..." caption="..." />` |
| Key finding | `<Finding number={N} title="...">` |
| IOC block | `<div className="ir-ioc-panel">` with `ir-ioc-title` + `ir-ioc-row` divs |

### 4c. Section icon suggestions

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

## Writing style rules

**Read `.claude/skills/humanizer/RULES.md` before writing any prose for this report.** It is the single source of truth for prose style across this site: banned phrases, banned structures, positive rules, and a pre-ship checklist. Do not work from memory of it.

Voice for this skill specifically: an analyst writing up what happened. Active voice on attacker actions ("the attacker exfiltrated credentials", never "credentials were exfiltrated"). State what the evidence shows and what it doesn't.

## Step 5 — Verify

- [ ] No `{{PLACEHOLDER}}` markers left in the output file
- [ ] Meta tags present with correct slug URLs
- [ ] `data/ir-reports.json` has the new entry prepended
- [ ] `ir-reports/<slug>/index.html` created
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

- `.claude/skills/new-ir-report/template.html` — page template with `{{PLACEHOLDER}}` markers (start here)
- `data/ir-reports.json` — report listing metadata
- `ir-reports/index.html` — listing page (for card rendering context)

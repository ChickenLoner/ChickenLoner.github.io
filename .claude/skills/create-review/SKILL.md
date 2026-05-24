---
name: create-review
description: Creates and polishes a certification review page for ChickenLoner.github.io from a Notion/Markdown export. Use this skill whenever the user wants to publish a new certification review, migrate a review from Medium or Notion, add a review page to the site, or refine an existing review. Triggers on phrases like "create review", "add review", "new review", "migrate review", "publish review", "review for [cert name]", or when the user points at an export_from_notion directory.
---

# Create & Polish Certification Review

Creates a complete, styled certification review page from a Notion/Markdown export, following the site's established patterns.

## Inputs to gather

Before starting, confirm:
1. **Export path** — directory with the `.md` file and images (e.g., `export_from_notion/psap-review`). If not provided, ask.
2. **Slug** — URL folder name for the review (e.g., `psap`, `cdsa`). Derive from the export dir name if obvious, otherwise ask.
3. **reviews.json entry** — check `data/reviews.json` first. If the entry already exists (`"url": "/reviews/<slug>/index.html"`), its metadata is the source of truth. If missing, ask the user for: title, excerpt, date, readTime, tags, difficulty, rating.

---

## Step 1 — Read the export

1. List the export directory — find the `.md` file and all image files.
2. Read the markdown fully. Build a precise map of:
   - All H2 headings (→ sections)
   - All H3 headings (→ subsections)
   - Every paragraph, bullet list, numbered list, blockquote
   - **Every image reference and its exact surrounding context** — which paragraph comes before it, which comes after. Image position is intentional and must be preserved exactly.
3. Identify the hero/cover image — typically `<slug>.jpg` or a standalone image at the very top of the document before any text. It does NOT get a Figure number.

---

## Step 2 — Prepare assets

1. Create `reviews/<slug>/` directory.
2. Copy all images (`.png`, `.jpg`, `.webp`, etc.) from the export directory to `reviews/<slug>/`, renaming them as follows:
   - **Hero/cover image** → `cover.png` (or `cover.jpg` if the source is JPEG)
   - **All other images** → `image-1.png`, `image-2.png`, … `image-N.png` in the order they appear in the markdown (top to bottom). Keep the original extension.
3. Use these renamed filenames in all `<Fig src="...">` references in the HTML — never use Notion hash filenames like `09a09d2ac97a87abec4ff8f9bca6ce64.png`.
4. Verify copy: `ls reviews/<slug>/` should show `cover.*`, `image-1.*` … `image-N.*` and `index.html`.

---

## Step 3 — Sync reviews.json

- Read `data/reviews.json`.
- If an entry with `"url": "/reviews/<slug>/index.html"` exists → use its `title`, `rating`, `difficulty`, `date`, `readTime`, `tags`. Do not overwrite it.
- If no entry exists → add one at the top of the array:
  ```json
  {
    "title": "...",
    "excerpt": "...",
    "date": "...",
    "readTime": "...",
    "tags": [...],
    "url": "/reviews/<slug>/index.html",
    "image": "/assets/badges/<slug>.png",
    "difficulty": "Beginner|Intermediate|Advanced",
    "rating": 0.0
  }
  ```
  Use `0.0` for rating if the user hasn't decided yet — it renders as no stars rather than crashing.

---

## Step 4 — Build `reviews/<slug>/index.html`

Read `.claude/skills/create-review/template.html` as your starting point. Replace every `{{PLACEHOLDER}}` with the real value, then fill in the content sections. Do not diverge from the template structure without a reason.

**Do NOT add a Tailwind CDN `<script>` tag.** Pages use `soc.css` utility equivalents instead.

### Placeholder reference

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | URL folder name (e.g. `csoa`) |
| `{{SLUG_UPPER}}` | Uppercase slug for breadcrumb (e.g. `CSOA`) |
| `{{TITLE}}` | Full review title |
| `{{DESCRIPTION}}` | Meta description (1–2 sentences) |
| `{{COVER_FILENAME}}` | `cover.jpg` or `cover.png` |
| `{{CERT_SHORT}}` | Short cert acronym (e.g. `CSOA`) |
| `{{PROVIDER}}` | Certification provider name |
| `{{DATE}}` | Month + year (e.g. `May 2026`) |
| `{{SECTION_N_ID}}` | Kebab-case anchor id (e.g. `exam-experience`) |
| `{{SECTION_N_LABEL}}` | Section display name |
| `{{SECTION_N_ICON}}` | Lucide icon name (see 4b below) |
| `{{CONTENT}}` | Replace with actual JSX content |
| `{{ALT_TEXT}}` | Brief image description |

### 4a. Components available in the template

| Component | Purpose |
|---|---|
| `Icon` | Lucide icon wrapper |
| `SocClock` | Live UTC clock |
| `Section` | H2 section with icon and scroll anchor |
| `Fig` | Figure with auto-incrementing counter (no caption text) |
| `resetFigCount` | Call as **first line inside `App()`** — already in template |
| `TipList` | Styled bullet list for exam tips |
| `B` | `<strong>` wrapper |
| `A` | External link (opens new tab) |
| `Code` | Inline code |
| `Callout` | Amber-accent blockquote — already defined in template |
| `renderStars` | Converts `4.5` → `★★★★½☆` — already defined in template |

The hero image is NOT a `Fig`. Every other image in the markdown becomes one `<Fig>` in order.

**Ampersand rule** — `&amp;` is only valid in JSX text/attributes (Babel decodes it). Inside plain JS object literals (e.g. `tocItems` label strings), use `&` directly.

**Difficulty and rating** — always from `meta?.difficulty` and `meta?.rating`, never hardcoded. Already wired in the template.

### 4b. Section icon suggestions

| Section topic | Icon |
|---|---|
| Introduction / overview | `BookOpen` |
| Course / learning content | `GraduationCap` |
| Exam / assessment | `ClipboardList` |
| Final review / summary | `Star` |
| Tips / takeaways | `Lightbulb` |
| Pricing / what you get | `DollarSign` |
| Prerequisites / requirements | `ListChecks` |
| Lab / hands-on | `FlaskConical` |

If none fit, `FileText` is a safe default.

### 4c. Page structure (in order)

1. **Nav** — `Chicken0248 / Reviews / <Cert Name>` breadcrumb + dark mode toggle
2. **Hero** — cover image with `bg-gradient-to-t from-black/80`, title overlay, pill badges (provider, date, domain, Passed/Failed)
3. **Metadata strip** — 4-column: Certification, Provider, Difficulty (from meta), Rating (from meta with `renderStars`)
4. **Table of Contents** — one link per Section, using icon + number + label
5. **Content sections** — see rules below
6. **Footer** — "Back to top" + "All Reviews" (`/reviews/index.html`)

### 4d. Content rendering rules

| Markdown element | HTML output |
|---|---|
| `## Heading` | `<Section id="..." title="..." icon="...">` |
| `### Subheading` | `<h3 className="text-xl font-semibold text-gray-800 mt-4 mb-2">` |
| Paragraph | `<p className="text-gray-700 leading-relaxed">` |
| `> blockquote` | `<Callout>` with amber left border |
| `- bullet list` | `<ul className="list-disc list-outside ml-5 space-y-1 text-gray-700">` |
| Tips/takeaways list | `<TipList items={[...]} />` inside amber `bg-amber-50` card |
| `**bold**` | `<B>` component |
| `[text](url)` | `<A href="...">` for external, plain `<a>` for internal |
| `---` divider | Already handled by Section boundaries — omit or use `<hr className="border-gray-200 my-6" />` |
| Image | `<Fig src="<filename>" alt="<brief description>" />` |
| Emoji | Preserve as-is in JSX |

**Image position rule**: Every image from the markdown must appear in the HTML between the exact same surrounding content. If an image appears between paragraph A and paragraph B in the markdown, it must appear between those same paragraphs in the JSX. This is intentional layout — do not reorder.

---

## Step 5 — Verify before finishing

Run these checks mentally:

- [ ] Count `<Fig` tags in HTML == count of non-hero images in markdown
- [ ] Every image filename referenced in `<Fig src="...">` exists in `reviews/<slug>/`
- [ ] `data/reviews.json` has an entry for this review
- [ ] No `{{PLACEHOLDER}}` markers left in the output file
- [ ] Meta tags present in `<head>` with correct slug URLs
- [ ] Metadata strip uses `meta?.rating` and `meta?.difficulty`, not hardcoded values
- [ ] Nav breadcrumb shows correct cert name
- [ ] Hero uses the cover image (not a `<Fig>`)

---

## Polishing pass

After generating the initial page, review the content for:

- **Prose quality** — fix grammar, awkward phrasing, or unclear sentences from the original export while preserving the author's voice and opinions. Do not change facts, ratings, or the author's judgments.
- **Consistency** — cert names, provider names, and acronyms should be spelled consistently throughout.
- **Link validity** — external links in `<A>` should look plausible. Flag any that look broken or placeholder-ish to the user.
- **Section balance** — if a section has only one short paragraph, flag it to the user rather than padding it.

Do not alter the meaning or sentiment of any review content. The author's voice is intentional.

## Writing style rules

These apply to all prose generated or polished by this skill:

- **No em dashes (—)**. Never use `—` in body text. Replace with: a comma, a colon, parentheses, or rewrite into two sentences. Example: "The exam was hard — but fair" → "The exam was hard, but fair."
- **Write like a human, not a report generator.** Vary sentence length. Mix short punchy sentences with longer ones. Don't start every sentence the same way.
- **Avoid AI filler phrases**: "it's worth noting", "it is important to", "it should be noted", "in order to", "this allows you to", "overall", "in conclusion". Cut them or rewrite the sentence.
- **Active voice preferred.** "The exam tests your memory" not "Your memory is tested by the exam."
- **No padding.** Don't add content to make a section look longer. If the source material is thin, leave it thin and flag it.
- **Preserve facts and opinions exactly.** Only fix phrasing, not substance. The author's judgment on ratings, difficulty, and recommendations is not yours to change.

---

## Reference files

- `.claude/skills/create-review/template.html` — page template with `{{PLACEHOLDER}}` markers (start here)
- `data/reviews.json` — all review metadata
- `reviews/index.html` — reviews listing page (for context on how cards render)

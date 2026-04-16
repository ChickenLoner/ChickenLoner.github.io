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
2. Copy all images (`.png`, `.jpg`, `.webp`, etc.) from the export directory to `reviews/<slug>/`.
3. Verify copy: `ls reviews/<slug>/` should show all images.

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

Use `reviews/psap/index.html` as the canonical reference for structure, components, and dark mode CSS. Do not diverge from its patterns without a reason.

### 4a. Head section

```html
<title>[Review Title] | Chicken0248</title>
<meta name="description" content="..." />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Chicken0248" />
<meta property="og:url" content="https://chickenloner.github.io/reviews/<slug>/" />
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:image" content="https://chickenloner.github.io/reviews/<slug>/<cover-image>" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@Chicken_0248" />
<meta name="twitter:title" content="..." />
<meta name="twitter:description" content="..." />
<meta name="twitter:image" content="https://chickenloner.github.io/reviews/<slug>/<cover-image>" />
<link rel="icon" href="/chicken0248.png" type="image/png">
```

Meta tags are **required** on every page — this was a site-wide instruction from the owner.

### 4b. Dark mode CSS

Copy the full dark mode `<style>` block from `reviews/psap/index.html` verbatim. It covers all amber/orange color variants used in the review theme. Add any extra color overrides if the content needs them (e.g., if the review has green/red badge elements).

### 4c. React components

Include all of these exactly as in `reviews/psap/index.html`:

| Component | Purpose |
|---|---|
| `Icon` | Lucide icon wrapper using `useRef` + `useEffect` |
| `Section` | H2 section with amber icon, scroll-mt-24 anchor, `id` for TOC links |
| `Fig` | Figure with auto-incrementing counter — shows **only "Figure N"**, no caption text. Image uses `max-w-full mx-auto block` (not `w-full`) so small screenshots render at natural size rather than stretching to container width |
| `Callout` | Amber-accent blockquote for exam descriptions or key quotes |
| `TipList` | Styled bullet list, used for exam tips sections |
| `B` | `<strong>` wrapper |
| `A` | External link (opens new tab) |
| `renderStars(rating)` | Converts `4.5` → `★★★★½☆` |

**Figure counter pattern** — the counter is module-level and must be reset at render start:
```js
let figCount = 0;
const resetFigCount = () => { figCount = 0; };
// Inside App(), first line:
resetFigCount();
```
The hero image is NOT a `Fig`. Every other image in the markdown becomes one `<Fig>` in order.

### 4d. Metadata fetch from reviews.json

```jsx
const [meta, setMeta] = useState(null);
useEffect(() => {
  fetch('/data/reviews.json')
    .then(r => r.json())
    .then(data => {
      const entry = data.find(r => r.url === '/reviews/<slug>/index.html');
      if (entry) setMeta(entry);
    })
    .catch(() => {});
}, []);
```

Use `meta?.rating`, `meta?.difficulty`, `meta?.date`, `meta?.readTime` in the metadata strip. Render `—` as fallback. Never hardcode rating or difficulty in the HTML.

### 4e. Page structure (in order)

1. **Nav** — `Chicken0248 / Reviews / <Cert Name>` breadcrumb + dark mode toggle
2. **Hero** — cover image with `bg-gradient-to-t from-black/80`, title overlay, pill badges (provider, date, domain, Passed/Failed)
3. **Metadata strip** — 4-column: Certification, Provider, Difficulty (from meta), Rating (from meta with `renderStars`)
4. **Table of Contents** — one link per Section, using icon + number + label
5. **Content sections** — see rules below
6. **Footer** — "Back to top" + "All Reviews" (`/reviews/index.html`)

### 4f. Content rendering rules

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

### 4g. Section icon suggestions

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

---

## Step 5 — Verify before finishing

Run these checks mentally:

- [ ] Count `<Fig` tags in HTML == count of non-hero images in markdown
- [ ] Every image filename referenced in `<Fig src="...">` exists in `reviews/<slug>/`
- [ ] `data/reviews.json` has an entry for this review
- [ ] Meta tags present in `<head>` with correct slug URLs
- [ ] Metadata strip uses `meta?.rating` and `meta?.difficulty`, not hardcoded values
- [ ] Nav breadcrumb shows correct cert name
- [ ] Hero uses the cover image (not a `<Fig>`)
- [ ] Dark mode CSS block is present

---

## Polishing pass

After generating the initial page, review the content for:

- **Prose quality** — fix grammar, awkward phrasing, or unclear sentences from the original export while preserving the author's voice and opinions. Do not change facts, ratings, or the author's judgments.
- **Consistency** — cert names, provider names, and acronyms should be spelled consistently throughout.
- **Link validity** — external links in `<A>` should look plausible. Flag any that look broken or placeholder-ish to the user.
- **Section balance** — if a section has only one short paragraph, flag it to the user rather than padding it.

Do not alter the meaning or sentiment of any review content. The author's voice is intentional.

---

## Reference files

- `reviews/psap/index.html` — canonical finished review page (PSAP, April 2026)
- `data/reviews.json` — all review metadata
- `reviews/index.html` — reviews listing page (for context on how cards render)

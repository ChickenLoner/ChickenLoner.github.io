# Security & UI/UX Improvement Plan

Audit date: 2026-05-10  
Consistency pass already committed (`854a665`). This plan covers the remaining two categories.

---

## Security Fixes

### S1 — Subresource Integrity (SRI) on CDN scripts
**Risk:** High. Every page loads React, ReactDOM, Babel standalone, Tailwind CDN, and Lucide from unpkg/jsdelivr without integrity checks. A CDN compromise or MITM would serve malicious scripts; Babel is especially dangerous because it transforms and executes arbitrary JSX.

**Fix:**
1. Pin each CDN dependency to a specific version (instead of `@latest` or `@18`).
2. Generate the `integrity` hash for each pinned URL using `openssl dgst -sha384 -binary <file> | openssl base64 -A`.
3. Add `integrity="sha384-..."` and `crossorigin="anonymous"` to every `<script>` tag across all pages.

**Affected files:** All 30+ HTML pages (index, reviews/*, research/*, ir-reports/*, cloud-labs, siem-labs).

**Suggested pinned versions:**
- `react@18.3.1` / `react-dom@18.3.1`
- `@babel/standalone@7.26.x`
- `lucide@0.x` (pin to current latest)
- Tailwind CDN — note: Tailwind CDN is development-only; for production consider building a static CSS bundle instead.

---

### S2 — Content Security Policy (CSP) meta tag
**Risk:** Medium. Without a CSP, any injected script (from S1 or elsewhere) runs with full page privileges.

**Fix:** Add a `<meta http-equiv="Content-Security-Policy">` tag to every page's `<head>`. Start with a permissive-but-defined policy, then tighten:

```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' https://cdn.tailwindcss.com https://unpkg.com 'unsafe-eval';
  style-src 'self' 'unsafe-inline';
  img-src 'self' https://chickenloner.github.io data:;
  connect-src 'self' https://raw.githubusercontent.com;
  font-src 'self';
">
```

Note: `'unsafe-eval'` is required for Babel standalone. Once SRI is added (S1), also add `require-sri-for script` to enforce it.

**Affected files:** All HTML pages.

---

### S3 — URL validation for README-parsed lab links
**Risk:** Medium. `cloud-labs/index.html` and `siem-labs/index.html` fetch external GitHub README files, parse markdown, and inject extracted URLs directly into `href` attributes. A malicious `javascript:` or `data:` URL in the README would execute on click.

**Fix:** Add a URL allowlist/validator in the `parseReadme()` function in both files:

```js
function isSafeUrl(url) {
    if (!url || url === '#') return true;
    try {
        const parsed = new URL(url);
        return ['https:', 'http:'].includes(parsed.protocol);
    } catch {
        return false;
    }
}
```

Then gate the `url` field assignment:

```js
url: linkMatch && isSafeUrl(linkMatch[1]) ? linkMatch[1] : '#',
```

**Affected files:** `cloud-labs/index.html`, `siem-labs/index.html`.

---

### S4 — Remove `console.log` / `console.error` from production
**Risk:** Low. Exposes internal debugging info to anyone opening DevTools.

**Fix:** Remove or replace these three statements in `index.html`:

```js
// Line ~358 — remove:
.catch(err => console.error('Failed to load site data:', err));

// Line ~370 — remove:
console.log('✓ Loaded dynamic metadata for', Object.keys(data).length, 'labs');

// Line ~374 — remove:
console.log('ℹ Using static data only:', err.message);
```

**Affected files:** `index.html`.

---

## UI/UX Improvements

### U1 — `<noscript>` fallback message
**Impact:** Accessibility / SEO. All pages render a blank `<div id="root"></div>` with no content when JS is disabled.

**Fix:** Add inside `<body>` before `<div id="root">`:

```html
<noscript>
  <style>body{font-family:system-ui,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}</style>
  <div style="text-align:center;padding:2rem">
    <h1>JavaScript required</h1>
    <p>This site requires JavaScript to display content. Please enable it in your browser settings.</p>
    <a href="https://chickenloner.github.io">chickenloner.github.io</a>
  </div>
</noscript>
```

**Affected files:** All HTML pages.

---

### U2 — Dark mode toggle `aria-label`
**Impact:** Accessibility. The ☀️/🌙 button is completely invisible to screen readers.

**Fix:** Add `aria-label` that reflects current state:

```jsx
<button
  onClick={() => setDark(!dark)}
  aria-label={dark ? 'Switch to light mode' : 'Switch to dark mode'}
  className="p-2 rounded-lg hover:bg-gray-100 text-gray-600 transition-colors text-lg">
  {dark ? '☀️' : '🌙'}
</button>
```

**Affected files:** All section index pages (reviews, research, ir-reports, cloud-labs, siem-labs, index).

---

### U3 — Skip-to-content link
**Impact:** Accessibility. Keyboard-only users must tab through the entire navigation before reaching content on every page load.

**Fix:** Add as the first child of `<body>`:

```html
<a href="#main-content"
   class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[100] focus:bg-white focus:px-4 focus:py-2 focus:rounded-lg focus:shadow-lg focus:text-blue-600 focus:font-semibold">
  Skip to content
</a>
```

And add `id="main-content"` to the `<main>` element on each page.

**Affected files:** All HTML pages.

---

### U4 — `<nav>` aria-label
**Impact:** Accessibility. Screen readers announce all `<nav>` elements without labels as just "navigation", making it hard to distinguish site nav from in-page anchors (e.g. IR report table of contents).

**Fix:**

```jsx
<nav aria-label="Site navigation" className="sticky top-0 ...">
```

For pages with a secondary in-page ToC nav, label it separately:

```jsx
<nav aria-label="Table of contents" ...>
```

**Affected files:** All HTML pages, especially IR report and review article pages.

---

### U5 — Lazy-load cover images
**Impact:** Performance. Research and IR report card grids load all cover images eagerly, including ones well below the fold.

**Fix:** Add `loading="lazy"` to all card cover images:

```jsx
<img src={article.cover} alt={article.title} loading="lazy"
     className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
```

**Affected files:** `research/index.html`, `ir-reports/index.html`.

---

### U6 — Back-navigation footer on article pages
**Impact:** UX. IR report and review article pages have a sticky top nav but no way to navigate forward or back without scrolling all the way up. Users reading long articles lose orientation.

**Fix:** Add a minimal sticky footer (or bottom bar) to article pages:

```jsx
<footer className="fixed bottom-0 left-0 right-0 z-40 bg-white/90 backdrop-blur-md border-t border-gray-200 px-4 py-3">
  <div className="max-w-4xl mx-auto flex items-center justify-between text-sm">
    <a href="/ir-reports/" className="flex items-center gap-1.5 text-gray-500 hover:text-gray-800 transition-colors">
      <Icon name="ArrowLeft" className="w-4 h-4" /> All Reports
    </a>
    <a href="#top" className="text-gray-400 hover:text-gray-600 transition-colors">Back to top ↑</a>
  </div>
</footer>
```

**Affected files:** All `reviews/*/index.html`, `ir-reports/*/index.html`, `research/*/index.html` article pages (~25 files).

---

### U7 — SVG star ratings (replace text glyphs)
**Impact:** Visual consistency. `★½☆` text glyphs render at different sizes and weights across platforms/fonts. Half-star `½` is especially inconsistent.

**Fix:** Replace `renderStars()` in `reviews/index.html` with an SVG-based renderer:

```jsx
const StarIcon = ({ filled, half }) => (
    <svg viewBox="0 0 20 20" className="w-3.5 h-3.5 inline-block">
        <defs>
            <linearGradient id={half ? 'half' : undefined}>
                <stop offset="50%" stopColor="currentColor"/>
                <stop offset="50%" stopColor="transparent"/>
            </linearGradient>
        </defs>
        <path
            fill={half ? 'url(#half)' : filled ? 'currentColor' : 'none'}
            stroke="currentColor" strokeWidth="1.5"
            d="M10 1l2.39 4.84 5.34.78-3.87 3.77.91 5.32L10 13.27l-4.77 2.44.91-5.32L2.27 6.62l5.34-.78L10 1z"
        />
    </svg>
);
```

**Affected files:** `reviews/index.html`, any review article pages that render stars.

---

### U8 — `<link rel="canonical">` on all pages
**Impact:** SEO. Without canonical tags, search engines may index GitHub Pages URLs inconsistently (trailing slash vs no slash, HTTP vs HTTPS).

**Fix:** Add to every page's `<head>`:

```html
<link rel="canonical" href="https://chickenloner.github.io/reviews/" />
```

Each page needs its own URL. This should be added alongside the OG meta tags (same pattern, same files).

**Affected files:** All HTML pages.

---

## Priority Order

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| 1 | **S4** — Remove console logs | 5 min | Low risk, instant |
| 2 | **S3** — URL validation in README parsers | 30 min | Security |
| 3 | **U5** — Lazy-load images | 15 min | Performance |
| 4 | **U2** — aria-label on dark toggle | 30 min | Accessibility |
| 5 | **U3** — Skip-to-content | 30 min | Accessibility |
| 6 | **U4** — nav aria-label | 30 min | Accessibility |
| 7 | **U1** — noscript fallback | 45 min | Accessibility |
| 8 | **U6** — Back-navigation footer | 1–2 hrs | UX (many files) |
| 9 | **U7** — SVG star ratings | 1 hr | Visual polish |
| 10 | **U8** — canonical links | 1 hr | SEO |
| 11 | **S2** — CSP meta tag | 1–2 hrs | Security |
| 12 | **S1** — SRI hashes + pin versions | 2–3 hrs | Security (high impact) |

# Mobile Responsiveness — Per-Page Fix Plan

## Fix 1 — `siem-labs/index.html`

`flex:none` on `.soc-search-bar` prevents stretching on narrow screens.

```css
/* Before */
.soc-search-bar { flex:none;min-height:48px; }

/* After */
.soc-search-bar { flex:1;min-width:200px;min-height:48px; }
```

---

## Fix 2 — All 22 review pages (`reviews/*/index.html`)

Every topbar shows TLP:CLEAR + CERT.REVIEW badges + clock on all screen sizes — no `hidden md:*`. Wraps to second line on mobile.

```jsx
/* Before — always visible */
<span className="sev cyan"><span className="dot"></span>TLP:CLEAR</span>
<span className="sev amber"><span className="dot"></span>CERT.REVIEW</span>
<SocClock /><ThemeToggle />

/* After — hidden on mobile */
<span className="sev cyan hidden md:inline-flex"><span className="dot"></span>TLP:CLEAR</span>
<span className="sev amber hidden md:inline-flex"><span className="dot"></span>CERT.REVIEW</span>
<span className="hidden md:block"><SocClock /></span><ThemeToggle />
```

Affected pages (22 total):
- reviews/oscp, gcfe, csoa, psap, cjca, sal1, cpts, crta, cdsa, ccda, ccdfa, ccdff,
  ccdl1, cceh, ccse, celms, cjde, cpta, cbteamerx, cagaipen, pt1, pwfa

---

## Fix 3 — `index.html` (main home page)

`.featured-latest` is a 3-col grid (`auto 1fr auto`: 72px glyph | content | CTA). No mobile breakpoint.
On 375px: content gets ~133px — tight. On 320px: ~78px — breaks.

Add to `index.html` inline `<style>` block:

```css
@media(max-width:480px) {
  .featured-latest { grid-template-columns:auto 1fr; padding:14px 16px; gap:12px; }
  .fl-cta { display:none; }
  .fl-glyph { width:48px; height:48px; font-size:11px; }
}
```

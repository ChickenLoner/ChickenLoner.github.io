# Redesign Implementation Plan

Source: `export_from_notion/redesign/` — Claude Design layouts for each portfolio page.

---

## ✅ Certifications Page (Done)

**Reference:** `export_from_notion/redesign/08-certifications-refined.html`

**What changed in `index.html`:**

### CSS added (before `</style>`)
- `--cat-off/blu/fir/fnd` CSS variables (dark + light theme)
- `.dist` — horizontal distribution bar strips
- `.toolbar` — flex toolbar wrapper
- `.soc-seg-btn.t-rd/t-cy/t-am/t-vi` — coloured active states per category
- `.filters`, `.fchip`, `.fchip-label` — status filter chips
- `.year-bar` — year divider with gradient line
- `.featured-latest` + `.fl-*` — featured "newest cert" banner
- `.cert-grid`, `.cert-card`, `.cert-glyph`, `.cert-body`, `.cert-name`, `.cert-meta` — cert grid cards with left-edge category accent
- `.cert-grid-dense` / `.cert-grid-airy` — grid density variants
- `.cert-compact` — compact layout density
- `.issuer-roster`, `.issuer-card` — issuer roster grid
- `.tweaks-fab`, `.tweaks-panel`, `.tw-*` — floating tweaks panel + controls
- Light theme overrides for all cert components
- `h2.soc-section.am/rd/vi` — coloured section heading accents
- `.soc-stat-val .unit` — smaller unit label inside stat value

### Component replaced: `CertificationsPage`
Old: category accordion with badge/certificate tabs.

New: full SOC-console dashboard:
- **Hero** — dynamic stats with `.dist` bars (total, active/total, top issuer, issuer count)
- **Tabs** — All / Offensive / Blue Team / DFIR / Foundational / By Issuer (6 tabs with counts)
- **Status filters** — All / Active / Expired chips
- **Featured latest banner** — pulls cert with `latest: true`
- **Cert grid** — cards with category colour accent, badge image (fallback glyph), issuer, year, status badge
- **Grouping modes** — Year (default), Category, Flat
- **Issuer pane** — roster grid + sorted list
- **Tweaks panel** (FAB) — Group by, Grid density, Layout density, Show/hide toggles; persisted to `soc-cert-tweaks-v1`

### Post-redesign cleanup
- `certificate` field removed from `certifications.json`
- `assets/certificates/` emptied — archived to `export_from_notion/cert/`
- `add-cert` skill updated: no longer collects/writes `certificate` field

---

## ✅ Labs & Projects Page (Done)

**Reference:** `export_from_notion/redesign/07-lab_project.html`

**What changed in `index.html`:**

### CSS added
- `.labs-page-wrap` — scoped wrapper for labs/projects page
- `.crow` — grid row layout (cover | info | action button); density variants via wrapper class
- `.crow .cover` — cover image cell with gradient overlay, retired badge
- `.crow .info` — title, subtitle, description, tags-row
- `.crow .ar` — action button (Play/Open variants, cy/vi colors)
- `.crow .place` (labs version) — absolute-positioned pill inside cover cell
- Retired styling: 3 variants (A=corner ribbon, B=overlay text, C=row tint)
- `.comp-list` — container for grouped crow rows
- `.year-bar` — group divider (shared with certs)
- `.tweaks-fab/.tweaks-panel` — reused FAB pattern
- Light mode overrides for all labs components

### Component replaced: `LabsPage`
Old: simple card grid.

New: SOC-console dashboard:
- **Hero** — custom `soc-page-hero` with 4 `.dist` stat cells (total labs, avg rating, active/retired, projects)
- **Tabs** — Labs / Projects (seg buttons)
- **Labs filters** — All / ★ 4.5+ / Hard / Active / Retired
- **Projects filters** — All / Tools / Research / Lists
- **Labs display** — `.crow` rows grouped by platform/rating; cover images; tweaks-controlled density
- **Projects display** — card grid with cover images
- **Tweaks panel** (FAB) — Group by, sort, density, retired style, show/hide covers/tags/desc; persisted to `soc-lab-tweaks-v2`

---

## ✅ Achievements Page (Done)

**Reference:** `export_from_notion/redesign/archievement.html`

**What changed in `index.html`:**

### CSS added (in achievements block)
- `.achiev-page-wrap` — scoped wrapper
- `.achiev-page-wrap .crow` override — `90px 1fr auto auto` grid (place | info | tags | arrow); `.place` reset to `position:static`
- `.place.gold/silver/bronze/other` — pill badge color variants
- `.feat-row`, `.fcard` — featured win cards (gradient, crown emoji, placement stamp; no image)
- `.talk-grid`, `.tcard` — speaking cards with gradient cover + real image overlay + mic/play icon
- `.fb-platforms`, `.fb-panel`, `.fb-panel-hd`, `.fb-detail-grid`, `.fb-detail` — First Bloods panels with cover images
- `.achiev-page-wrap .crow-expand` — expandable row panel (cover + description)
- `.achiev-page-wrap .soc-seg-btn.t-am/rd/vi.active` — scoped tab colors (overrides cert `--cat-*` vars)
- Light mode overrides for achievements components

### Component replaced: `AchievementsPage`
Old: generic `SocPageHero` + 2-column image card grid (competitions + speaking).

New: SOC-console dashboard:
- **Hero** — custom `soc-page-hero` with 4 `.dist` stat cells (competitions dist, wins, top-3, speaking)
- **Tabs** — Competitions (amber) / First Bloods (red, count badge) / Speaking (violet)
- **Competition filters** — All / ★ Wins / Podium
- **Featured wins** — `.fcard` grid (amber gradient, crown, placement stamp); hidden by tweaks or non-all filter
- **Non-win rows** — `.crow` expandable rows grouped by year; click expands cover image + description
- **First Bloods** — loads `data/firstbloods.json` on mount; BTLO / HTB Sherlock / CD panels each with `.fb-detail-grid` cards (cover image, platform tag, verify link)
- **Speaking** — `.talk-grid` with `.tcard`; real cover image + gradient overlay + mic/play icon; YouTube watch button
- **Tweaks panel** (FAB) — Featured Wins toggle, Year dividers, Tags on rows; persisted to `soc-achiev-tweaks-v1`

### New files
- `data/firstbloods.json` — 17 BTLO + 2 HTB Sherlock + 1 CD entries with names, verify URLs, image paths
- `assets/firstbloods/` — 20 cover images (btlo_NNN.png, htb_NNN.png, consentstorm.png)
- `architecture.html` updated — added `firstbloods.json` schema + `assets/firstbloods/` to directory tree
- Competition cover images moved to `export_from_notion/achievement-migrate/` (not displayed); talk images kept in `assets/achievements/`

---

## ⬜ Remaining Pages (not yet started)

| File | Page |
|---|---|
| `09-stats-refined.html` | Stats tab |

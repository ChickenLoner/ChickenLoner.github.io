# Mobile Responsiveness Fixes

## Done
- [x] Mobile: tab bar (All → By Issuer) overflows off-screen → fixed with `flex-wrap:wrap` + `width:100%` on `.toolbar .soc-seg` at ≤768px; buttons get `flex:1` to fill rows evenly

- [x] Mobile: labs & projects filter chips fall off screen → toolbar stacks vertically (`flex-direction:column`), `.toolbar .filters` gets `width:100%; margin-left:0; flex-wrap:wrap`; label forced to own line with `flex-basis:100%`

- [x] Mobile: achievements tab bar (outside `.toolbar`) + competitions filter div not covered by toolbar rules → added `.achiev-page-wrap .soc-seg` wrap rules + `.achiev-comp-filters` class with same scroll behavior

- [x] Stats page mobile: multiple layout issues fixed:
  - `.soc-stat-grid` inline style overrode 768px CSS → added `!important` to force 2-col on mobile
  - `.tile-grid` (1fr 1fr) too narrow on mobile → collapse to `1fr !important` at ≤768px
  - Competitions inner grid had inline `gridTemplateColumns:'1fr 1fr'` overriding CSS → added `.comp-inner-l`/`.comp-inner-r` classes, border swaps to top on mobile
  - `.brow` fixed 130px label column shrinks to 100px at ≤768px, 80px + drop `%` col at ≤480px
  - `.rating-summary` 3-col stays at 768px, collapses to 1-col at ≤480px
  - `.mitre-grid` min shrinks 155px→120px at ≤480px
  - `.act-row` year col shrinks 64px→48px at ≤480px
  - `.issuer-roster` min shrinks 220px→160px at ≤768px

- [x] Mobile topbar unbalanced (main index): crumb + badges + clock wrap chaotically → hide on mobile (`hidden md:flex` / `hidden md:block`), flex spacer pushes ThemeToggle + hamburger right

- [x] PC nav bar required horizontal scroll → changed `.soc-nav-inner` from `overflow-x:auto` to `flex-wrap:wrap` so items wrap to second row instead

- [x] Labs/projects cover image broken on mobile → cover + play button hidden at ≤480px via separate media block placed after the 820px crow block (cascade order fix); card goes single-column

- [x] Hero strap overflow on mobile (all pages) → right metadata seg (`verified_credentials`, `last_issued`, etc.) hidden at ≤768px; left path label stays visible

- [x] Mobile topbar unbalanced (all sub-pages: siem-labs, cloud-labs, ir-reports, reviews, research) → same `hidden md:flex/block` pattern applied across 32 files; badges + clock hidden, ThemeToggle stays

- [x] No way to navigate back to home from sub-pages on mobile → UPLINK span converted to `<a href="/">` on all 32 sub-pages; always visible on mobile as home link

## Pending
<!-- add items here as we go -->

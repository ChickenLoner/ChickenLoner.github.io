# Cert Page Filter Adjustments

## Done
- [x] Mobile: tab bar (All → By Issuer) overflows off-screen → fixed with `overflow-x:auto` + `display:flex;width:100%` on `.toolbar .soc-seg` at ≤768px breakpoint; toolbar stacks vertically so tabs get full row

- [x] Mobile: labs & projects platform/filter chip rows wrap messily with 5 chips → fixed with `flex-wrap:nowrap; overflow-x:auto` on `.toolbar .filters` at ≤768px; chips scroll horizontally, consistent with tab bar
- [x] Mobile: achievements tab bar bare `nav.soc-seg` (outside `.toolbar`) + competitions filter div (inline styles) not covered by toolbar fixes → added `.achiev-page-wrap .soc-seg` scroll rule + `.achiev-comp-filters` class with scroll behavior

- [x] Stats page mobile: multiple layout issues fixed:
  - `.soc-stat-grid` inline style overrode 768px CSS → added `!important` to force 2-col on mobile
  - `.tile-grid` (1fr 1fr) too narrow on mobile → collapse to `1fr !important` at ≤768px
  - Competitions inner grid had inline `gridTemplateColumns:'1fr 1fr'` overriding CSS → added `.comp-inner-l`/`.comp-inner-r` classes, border swaps to top on mobile
  - `.brow` fixed 130px label column shrinks to 100px at ≤768px, 80px + drop `%` col at ≤480px
  - `.rating-summary` 3-col stays at 768px, collapses to 1-col at ≤480px
  - `.mitre-grid` min shrinks 155px→120px at ≤480px
  - `.act-row` year col shrinks 64px→48px at ≤480px
  - `.issuer-roster` min shrinks 220px→160px at ≤768px

- [x] Mobile topbar unbalanced: crumb + severity badges + clock all wrap chaotically → hide them on mobile (`hidden md:flex` / `hidden md:block`), insert flex spacer so ThemeToggle + hamburger push to the right cleanly

## Pending
<!-- add items here as we go -->

This is a repository for my portfolio site live at https://chickenloner.github.io/

Do not code or edit file right away, give user solutions first, providing them how each approach works and let user decide which approach to implement

If user ask to change anything and you have no context about structure, refer to architecture.html for that and if any change happened that affect architecture.html that edit this file to make it always up-to-date

If there is any change that affects skill located at ./.claude/skills then make sure to edit it to make it always up-to-date

Let user experience and when he "satisfied" then commit and push to github.

If there is any problem that keep repeating, put them here to prevent the same problem occurs in the future
-

## Responsive Design
All design changes must consider mobile responsiveness. Every new page, component, or layout change must:
- Test at mobile breakpoints (≤768px phones, ≤1024px tablets)
- Avoid hardcoded pixel widths on containers; use `%`, `vw`, `max-width`, or flexbox/grid
- Hide or stack elements that overflow on small screens
- Check topbar, hero, grid, and card components on mobile after any layout edit
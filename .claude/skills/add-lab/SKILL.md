---
name: add-lab
description: Adds a new lab entry to data/labs.json for ChickenLoner.github.io. Use this skill when the user publishes a new lab on BTLO, HackTheBox, CyberDefenders, or another platform. Triggers on phrases like "add lab", "new lab", "my lab launched", "lab is live", "add [lab name] to labs", or when the user shares a new lab link.
---

# Add Lab

Adds a new lab authored by Chicken0248 to `data/labs.json`.

## Step 1 — Gather required info

Ask for any missing fields not provided in the user's message:

| Field | Notes |
|---|---|
| `title` | Lab title as shown on the platform |
| `description` | 1–2 sentence description of the scenario |
| `platform` | `"Blue Team Labs Online"`, `"HackTheBox"`, `"CyberDefenders"`, or a CTF event name |
| `link` | Direct URL to the lab. **Optional** — omit the field entirely if there is nowhere to point yet (see "Labs with no link") |
| `tags` | Array of topic tags, e.g. `["Endpoint Forensics", "Windows Forensics"]` |
| `difficulty` | `"easy"`, `"medium"`, or `"hard"` (author-set difficulty) |
| `is_retired` | `true` or `false` — default `false` for a newly launched lab |
| `image` | Cover image path `"./assets/labs/<filename>.png"` — ask if file exists |
| `tactics` | Optional MITRE ATT&CK tactics array — skip if not applicable |
| `player_difficulty` | Optional perceived difficulty from players — omit if unknown at launch |

### Valid platforms (core)
- `"Blue Team Labs Online"` — grouped as BTLO in Labs page
- `"HackTheBox"` — grouped as HTB
- `"CyberDefenders"` — grouped as CD
- Any other string → grouped as CTF/Other

**CTF events** use the event name verbatim as the platform, e.g. `"STDiO CTF 2025"`,
`"Women Thailand Cyber Top Talent 2025"`. One challenge = one lab entry; all challenges from the same
event share the platform string so they group together. A finished event means `"is_retired": true`
on every entry from it.

### Labs with no link

Challenges authored for a CTF often go public before the writeup exists. When there is no URL yet,
**omit `link` entirely** — do not invent a placeholder or point at the event homepage.

Two consequences, both mandatory:

- The Labs card renders `<a href={undefined}>`. It still looks clickable but navigates nowhere. This
  is accepted; the alternative is a broken link.
- **Never set `"latest": true` on a linkless lab.** The home page ticker builds its "Play ↗" button
  from `lab.link` (`index.html`, the `type:'LAB'` ticker entry), so a linkless latest lab renders a
  dead button in the hero. Leave `latest` on the previous lab until the URL exists.

Add `link` in a later edit once the writeup is published, and only then consider moving `latest`.

## Step 2 — Check for cover image

```bash
ls assets/labs/
```

If the cover image doesn't exist, note it to the user and use the placeholder path anyway. Naming convention: lowercase slug of the title, e.g. `utensilmenace.png`.

## Step 3 — Add to labs.json

1. Read `data/labs.json`.
2. Find the **last existing entry with the same platform**. Insert the new entry immediately after it (newer labs follow older labs within the same platform group).
   - If no entry with the same platform exists yet, prepend to the top.

```json
{
  "title": "<title>",
  "description": "<description>",
  "platform": "<platform>",
  "link": "<link>",
  "tags": [...],
  "type": "lab",
  "difficulty": "<difficulty>",
  "is_retired": false,
  "latest": true,
  "image": "./assets/labs/<filename>.png"
}
```

Drop both `link` and `latest` if there is no URL yet — see "Labs with no link" above.

Add optional fields only if provided:
```json
  "player_difficulty": "<player_difficulty>",
  "tactics": [...]
```

**Ratings: leave them out.** Do not add `rating` when creating the entry.

For a **CyberDefenders** lab, the daily script now fills it in automatically — it gates on
`released_at`, so any lab released 2026-06-01 or later starts tracking on its own with
`rating_scale: 3` and a monthly `rating_as_of`. Nothing to set up, and a lab with no votes yet
(`0.0`) is skipped rather than published as a zero.

For **HackTheBox / BTLO**, ratings are hand-entered and there is no scraper. Add them once the score
settles, as a set of three:
```json
  "rating": 4.5,
  "rating_scale": 5,
  "rating_as_of": "2026-08"
```

`rating_scale` **must match the platform's maximum** — the site divides by it to compare labs across
scales, so a wrong value silently misranks the lab.

| Platform / era | `rating_scale` | maintained by |
|---|---|---|
| CyberDefenders, released **2026-06 or later** | `3` | daily script |
| CyberDefenders, released before 2026-06 | `5` | frozen — never update |
| HackTheBox, Blue Team Labs Online | `5` | by hand |

`rating_as_of` is the month you actually read the value — omit it rather than guess.

Never hand-write a **pre-2026-06** CyberDefenders rating into `labs_metadata.json`; that file wins the
render-time merge and would override the frozen value. See "Lab Ratings" in `architecture.html`.

3. Remove `"latest": true` from the previously latest lab entry — **only if the new entry has a
   `link`**. A linkless lab does not take `latest`, so leave the old one alone.
4. Write the updated file. Preserve all existing entries exactly.
5. Validate: `node -e "require('./data/labs.json')"` — a trailing-comma slip silently blanks the whole
   Labs page at runtime.

## Step 4 — Register in metadata script (CyberDefenders only)

If platform is `"CyberDefenders"`, also update `scripts/update_lab_data.py`.

Derive the slug: lowercase title, spaces → hyphens, strip special chars. Examples:
- "Satisfaction" → `satisfaction`
- "YARA Trap" → `yara-trap`
- "RaaS Unfold - RansomHub" → `raas-unfold-ransomhub`

Add a new entry to `labs_to_update` dict inside `update_lab_metadata()`:

```python
'<title>': {
    'platform': 'cyberdefenders',
    'slug': '<slug>'
},
```

Insert it before the closing `}` of the dict. Preserve all existing entries exactly.

## Step 5 — Commit

```bash
git add data/labs.json scripts/update_lab_data.py
git commit -m "add lab: <title> (<platform>)"
git push origin main
```

If platform is not CyberDefenders, only stage `data/labs.json`.

## Step 6 — Confirm

Tell the user:
- Which platform group it appears under on the Labs page
- Whether the cover image needs to be added to `assets/labs/`
- If `link` was omitted: that the card is not clickable until the URL is filled in, and that `latest`
  was deliberately left on the previous lab
- If CyberDefenders: that the lab is now registered in the daily metadata script — `player_difficulty`, `is_retired` and `tactics` will auto-populate, and so will `rating` if the lab was released 2026-06-01 or later (see Step 2). Expect the rating to swing for the first few weeks.

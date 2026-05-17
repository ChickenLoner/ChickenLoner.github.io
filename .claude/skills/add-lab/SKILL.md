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
| `platform` | `"Blue Team Labs Online"`, `"HackTheBox"`, `"CyberDefenders"`, or other |
| `link` | Direct URL to the lab on the platform |
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

## Step 2 — Check for cover image

```bash
ls assets/labs/
```

If the cover image doesn't exist, note it to the user and use the placeholder path anyway. Naming convention: lowercase slug of the title, e.g. `utensilmenace.png`.

## Step 3 — Add to labs.json

1. Read `data/labs.json`.
2. Prepend the new entry at the **top** of the array (newest first):

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
  "image": "./assets/labs/<filename>.png"
}
```

Add optional fields only if provided:
```json
  "player_difficulty": "<player_difficulty>",
  "rating": null,
  "tactics": [...]
```

3. Write the updated file. Preserve all existing entries exactly.

## Step 4 — Commit

```bash
git add data/labs.json
git commit -m "add lab: <title> (<platform>)"
git push origin main
```

## Step 5 — Confirm

Tell the user:
- Which platform group it appears under on the Labs page
- Whether the cover image needs to be added to `assets/labs/`
- That `rating` and `player_difficulty` will be populated automatically by the GitHub Actions script once the lab has reviews (`labs_metadata.json` is updated daily)

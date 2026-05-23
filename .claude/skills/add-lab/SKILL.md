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
- If CyberDefenders: that the lab is now registered in the daily metadata script — `rating` and `player_difficulty` will auto-populate once the lab has player reviews

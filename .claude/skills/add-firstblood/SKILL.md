---
name: add-firstblood
description: Adds a new first blood entry to data/firstbloods.json for ChickenLoner.github.io. Use this skill when the user earns a first blood on BTLO, HackTheBox Sherlock, or CyberDefenders. Triggers on phrases like "add first blood", "new first blood", "I got first blood on", "first blood on [challenge]".
---

# Add First Blood

Adds a new first blood entry to `data/firstbloods.json` and copies the cover image to `assets/firstbloods/`.

## Step 1 — Gather required info

Ask for any missing fields not provided in the user's message:

| Field | Notes |
|---|---|
| `platform` | One of: `btlo`, `htb_sherlock`, `cd` |
| `name` | Challenge name |
| `url` | Achievement/verification URL |
| `id` | Numeric challenge ID (BTLO and HTB only — not needed for CyberDefenders) |
| `image` | Cover image file — user should provide the file path or confirm it exists |

### Platform → URL patterns

| Platform | URL pattern |
|---|---|
| BTLO | `https://blueteamlabs.online/achievement/share/52929/<id>` |
| HTB Sherlock | `https://labs.hackthebox.com/achievement/sherlock/1438364/<id>` |
| CyberDefenders | `https://cyberdefenders.org/blueteam-ctf-challenges/achievements/Chicken_0248/<slug>/` |

### Image naming convention

| Platform | Filename |
|---|---|
| BTLO | `btlo_<id>.png` |
| HTB Sherlock | `htb_<id>.png` |
| CyberDefenders | `<slug>.png` (lowercase challenge slug) |

## Step 2 — Copy cover image

Ask the user where the cover image is. Copy it to `assets/firstbloods/` with the correct filename:

```bash
cp "<source path>" "assets/firstbloods/<filename>"
```

If the image doesn't exist yet, use an empty placeholder path and remind the user to add it later.

## Step 3 — Add to firstbloods.json

1. Read `data/firstbloods.json`.
2. Prepend the new entry to the correct platform array (most recent first):

**BTLO:**
```json
{ "id": <id>, "name": "<name>", "url": "<url>", "image": "./assets/firstbloods/btlo_<id>.png", "latest": true }
```

**HTB Sherlock:**
```json
{ "id": <id>, "name": "<name>", "url": "<url>", "image": "./assets/firstbloods/htb_<id>.png", "latest": true }
```

**CyberDefenders:**
```json
{ "name": "<name>", "url": "<url>", "image": "./assets/firstbloods/<slug>.png", "latest": true }
```

3. Remove `"latest": true` from the previously latest entry across all platform arrays (btlo, htb_sherlock, cd).
4. Write the updated file. Preserve all existing entries exactly.

## Step 4 — Commit

```bash
git add data/firstbloods.json assets/firstbloods/<filename>
git commit -m "add first blood: <name> (<platform>)"
git push origin main
```

## Step 5 — Confirm

Tell the user:
- Which platform panel it appears in on the Achievements page (First Bloods tab)
- The total blood count for that platform after adding
- Whether the cover image was copied or still needs to be added

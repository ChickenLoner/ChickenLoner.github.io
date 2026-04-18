---
name: add-cert
description: Adds a new certification entry to certifications.json for ChickenLoner.github.io. Use this skill whenever the user wants to add a new cert, badge, or credential to their portfolio. Triggers on phrases like "add cert", "new cert", "add certification", "I got a new cert", "add [cert name]", or when the user mentions passing an exam.
---

# Add Certification

Adds a new certification to `data/certifications.json` with the correct schema and category.

## Step 1 — Gather required info

Ask for any missing fields (don't ask for fields already provided in the user's message):

| Field | Notes |
|---|---|
| `name` | Full cert name, e.g. `"OSCP - OffSec Certified Professional"` |
| `issuer` | Certification body, e.g. `"OffSec"` |
| `year` | 4-digit year earned, e.g. `"2026"` |
| `status` | `"Active"` or `"Expired"` — default `"Active"` |
| `category` | One of the 4 below — pick the best fit or ask |
| `badge` | Path like `"./assets/badges/<slug>.png"` — ask if file exists or needs copying |
| `certificate` | Path like `"./assets/certificates/<slug>.jpg"` — ask if available |
| `url` | Credly/credential verification URL — empty string `""` if not yet available |

### Valid categories
- `Offensive Security` — pen testing, red team, exploit dev
- `Blue Team & Detection` — SOC, SIEM, detection engineering, threat hunting
- `Digital Forensics & DFIR` — disk/memory/network forensics, malware analysis
- `General & Foundational` — broad security, networking, entry-level

If the category is ambiguous, suggest the most likely one and confirm with the user.

## Step 2 — Check for badge/certificate files

Run:
```bash
ls assets/badges/
ls assets/certificates/
```

If the badge or certificate file doesn't exist yet, note it to the user and use the placeholder path anyway — they can copy the file later.

## Step 3 — Add to certifications.json

1. Read `data/certifications.json`.
2. Append the new entry at the **end** of the array (most recent = last):

```json
{
  "name": "<name>",
  "issuer": "<issuer>",
  "year": "<year>",
  "status": "<status>",
  "category": "<category>",
  "badge": "<badge path>",
  "certificate": "<certificate path>",
  "url": "<url>"
}
```

3. Write the updated file. Preserve all existing entries exactly — do not reformat, reorder, or change any other entry.

## Step 4 — Commit

```bash
git add data/certifications.json
git commit -m "add <name> certification"
git push origin main
```

## Step 5 — Confirm

Tell the user:
- The cert was added to which category
- Whether badge/cert files need to be copied to `assets/`
- That it will appear immediately in the Certifications page marquee and categorized section

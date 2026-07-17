---
name: humanizer
description: Rewrites prose so it stops reading like AI output. Strips filler phrases, AI structural tells, and generator rhythm while preserving every fact and opinion. Use when the user wants text to sound human, or points at an article that reads like it was generated. Triggers on phrases like "humanize", "de-AI this", "make this sound human", "this reads like ChatGPT", "sounds like AI", "fix the writing", "make this less robotic", or when polishing prose in any article, review, or research page on this site.
---

# Humanizer

Rewrites prose to read like a practitioner wrote it. Facts and opinions survive untouched; only phrasing changes.

The rule-set lives in `.claude/skills/humanizer/RULES.md`. **Read it first.** It is the single source of truth for prose style across this site, and the `new-research`, `new-ir-report`, and `create-review` skills reference the same file.

## Step 1 — Get the target

Ask which of these applies if the user didn't say:

| Target | What to do |
|---|---|
| Pasted text | Rewrite inline, return the result |
| A file path | Read it, rewrite the prose, Edit in place |
| An existing article slug | Find `research/<slug>/index.html`, `reports/<slug>/`, or `reviews/<slug>/` and rewrite the prose nodes |
| "the thing you just wrote" | Rewrite your own last output |

## Step 2 — Read the rules

Read `.claude/skills/humanizer/RULES.md` in full before touching prose. Do not work from memory of it.

## Step 3 — Rewrite

Apply the rules in this order. Order matters: structural fixes change which phrases survive, so doing phrases first wastes work.

1. **Structure pass** (RULES.md §2) — kill em dashes, "not just X but Y", rule-of-three padding, self-announcing sections, empty conclusions. Merge or split paragraphs so lengths stop being uniform.
2. **Phrase pass** (RULES.md §1) — cut banned phrases. If a sentence collapses without one, delete the sentence.
3. **Concreteness pass** (RULES.md §3) — every section needs at least one hard detail: a path, count, command, version, error string. If you don't have one, flag the gap to the user rather than inventing one.
4. **Rhythm pass** — read it back. Vary sentence length deliberately. Break up anything that drones.

### Hard constraints

- **Never invent facts.** If a section is vague because the source was vague, say so to the user. Do not fill the hole with a plausible-sounding path, version number, or statistic. This is the one failure mode that turns a style fix into a lie on a public portfolio.
- **Never change substance.** Ratings, difficulty calls, recommendations, opinions, and technical claims are the author's. You fix how they're said, not what they say.
- **Preserve all markup.** When editing HTML pages, touch only the text inside prose nodes. Do not restructure components, class names, or JSX.
- **Preserve code blocks verbatim.** Code, commands, and output are never "humanized".

## Step 4 — Verify

Run the §5 checklist from RULES.md. Then report to the user:

- What you changed, by category (structure / phrases / concreteness)
- Any gap where the source was too thin to make concrete, and what detail would fill it
- Nothing else. Don't summarize the article back at them.

## Step 5 — Commit

Only if the rewrite targeted a file in the repo:

```bash
git add <path>
git commit -m "humanize prose: <what>"
git push origin main
```

## Reference files

- `.claude/skills/humanizer/RULES.md` — the rule-set (read this every time)
- `.claude/skills/new-research/SKILL.md` — references the same rules
- `.claude/skills/new-ir-report/SKILL.md` — references the same rules
- `.claude/skills/create-review/SKILL.md` — references the same rules

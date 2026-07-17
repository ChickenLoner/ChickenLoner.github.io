# Humanizer Rules

Shared prose rules for every article on this site. Applied when writing new prose and when retrofitting old prose.

The target voice: a practitioner who did the work and is telling you what happened. Not a documentation generator, not a LinkedIn post, not a textbook.

---

## 1. Banned phrases

Cut on sight. If the sentence dies without the phrase, the sentence was filler.

| Category | Banned |
|---|---|
| Hedged throat-clearing | "it's worth noting", "it is important to note", "it should be noted", "keep in mind that", "bear in mind" |
| Fake profundity | "delve into", "a testament to", "speaks volumes", "at its core", "the beauty of X is" |
| Corporate scaffolding | "in today's landscape", "in the ever-evolving world of", "in the realm of", "when it comes to" |
| Empty transitions | "that said", "with that in mind", "moving forward", "overall", "in conclusion", "to summarize" |
| Padding verbs | "in order to" (→ "to"), "this allows you to" (→ "you can"), "serves to", "acts as a means of" |
| Self-congratulation | "powerful", "robust", "seamless", "game-changer", "leverage" (→ "use"), "utilize" (→ "use") |
| Fake stakes | "crucial", "vital", "essential" — unless you say what breaks without it |

## 2. Banned structures

Harder to spot than phrases, and the bigger tell.

- **No em dashes (—).** Never in body text. Use a comma, colon, parentheses, or split into two sentences. `The exam was hard — but fair` → `The exam was hard, but fair.`
- **No rule-of-three lists** when two or four items is the truth. AI pads to three for rhythm. Say what's actually there.
- **No "not just X, but Y"** and its family: "isn't merely", "more than just", "not only... but also". Pick the claim you mean.
- **No symmetric paragraphs.** If every paragraph is 3-4 sentences, you wrote a template. Real writing has one-sentence paragraphs next to eight-sentence ones.
- **No section that restates the section.** Opening a section with "In this section, we will explore..." is a wasted line. Start with the content.
- **No summary that adds nothing.** A conclusion that lists what the reader just read is filler. Either land a real takeaway or delete the section.
- **No hedge stacking.** "This may potentially be able to sometimes indicate" → "This can indicate."
- **No parallel bullet padding.** Bullets that all start with the same gerund ("Analyzing...", "Reviewing...", "Identifying...") read as generated. Vary the openings or convert to prose.

## 3. Positive rules

- **Vary sentence length deliberately.** Short one. Then one that runs longer, carries a clause, and gives the reader something to chew on. Then short again.
- **Concrete over abstract.** Not "the tool provides extensive logging capabilities" but "the tool writes every session to `connections.txt`, one line per connect."
- **Active voice.** "TeamViewer stores logs in `%AppData%`" not "Logs are stored in `%AppData%` by TeamViewer."
- **Admit uncertainty plainly.** "I couldn't reproduce this on Win11 22H2" beats hedging around it. Real writers say what they don't know.
- **Show the dead end.** What failed is often more useful than what worked, and no generator writes it.
- **Technical precision over verbosity.** One clear sentence beats three vague ones. Don't explain what the reader can infer.
- **Don't pad.** Thin section stays thin. Never add sentences to fill visual space.
- **Keep the author's voice.** When retrofitting: fix phrasing, never substance. Opinions, ratings, difficulty calls, and recommendations belong to the author.

## 4. Rewrite examples

| AI-flavored | Human |
|---|---|
| "It's worth noting that AnyDesk stores its connection logs in a variety of locations, which can be crucial for investigators." | "AnyDesk scatters connection logs across three paths. You need all three." |
| "This powerful technique allows you to leverage existing artifacts in order to build a comprehensive timeline." | "You can build the timeline from artifacts already on disk." |
| "Overall, the exam was challenging but fair — it truly tests your practical skills." | "The exam was hard, but fair. Nothing on it was trivia." |
| "In today's ever-evolving threat landscape, RMM abuse has become increasingly prevalent." | "RMM abuse shows up in about half the intrusions I've looked at this year." |
| "Delving into the registry reveals a testament to the tool's persistence mechanisms." | "The registry shows how it survives reboot: a Run key under HKCU." |

## 5. Self-check before shipping

Run this pass over any prose you generated:

- [ ] Zero em dashes in body text
- [ ] Zero phrases from the §1 table
- [ ] No "not just X but Y" construction
- [ ] Paragraph lengths vary (not all 3-4 sentences)
- [ ] At least one concrete detail per section (path, count, command, version, error string)
- [ ] No section opens by announcing itself
- [ ] Conclusion lands a takeaway or doesn't exist
- [ ] Read it aloud: does it sound like a person who was there?

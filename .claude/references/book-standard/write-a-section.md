---
type: recipe
description: The craft of each of the five sections — how to write a definition, a mechanics block, a one-sentence takeaway, an example, and a tie-in, each against its own bar.
load_when: Mid-chapter, writing one specific section — how to make a definition land, a table earn its rows, a takeaway compress, an example convince.
keywords: [sections, definition, takeaway, example, mechanics, tie-in, craft, writing]
---

# Write a section

**What it is** — the per-section craft beneath [write-a-chapter](write-a-chapter.md)'s step 4. [chapter-template](chapter-template.md) assigns each section its *job*; this chapter is *how each job is done* — the moves and the smells, section by section.

**Prerequisites**

- You are mid-chapter: the concept is named, the file and frontmatter exist ([write-a-chapter](write-a-chapter.md) steps 1–3 done).
- You can already say the Takeaway aloud in one sentence — if not, stop; the chapter has no concept yet.

**Steps** — one section each, one observable outcome each:

1. **What it is** — write the definition as *genus + difference*: what kind of thing it is, then what separates it from its neighbors. 1–3 sentences, plain words first; no history, no hedging, no "in general". Jargon only after the plain version has carried it. → *Outcome: a stranger could repeat the concept back in their own words.*
2. **Mechanics** — pick the shape before writing: a **table** when comparing or enumerating, a **list** when sequencing, prose only when a mechanism genuinely needs narrative. Every row must earn its place — a row that restates the definition is filler. Skip the whole section if the definition already covered how it works. → *Outcome: no paragraph remains that could have been a table.*
3. **Takeaway** — one bold sentence, shaped as *rule + consequence* ("X, because/so Y"). The test: delete the rest of the chapter — does the sentence still teach the concept? It is what gets quoted and cited, so it must stand alone. → *Outcome: exactly one bold sentence, quotable without the chapter.*
4. **Example** — prefer real: a named system, a dated event, a cited finding, with numbers where they exist. Constructed is allowed but labeled *(constructed, illustrative)* — and even a constructed example must be concrete enough to falsify ("a 500-token doc answers; the same doc in 50k fails", never "less context is better"). Match its *domain* to the book's scope ([example-domain-fit](example-domain-fit.md)): in-domain for a domain book, domain-neutral but still concrete for a general/method book. → *Outcome: the example is real-and-named or labeled-and-concrete, and its domain fits the book's scope.*
5. **In this system** — ground the concept in the reader's machinery: name what implements or enforces it *on the shelf this book ships to* ([write-for-the-shelf](write-for-the-shelf.md)), then close with the chapter's most important within-book pointers. → *Outcome: at least one resolving pointer; zero off-shelf referents.*

**Verification**

- Reread each section against chapter-template's bar column — the gate runs the same table.
- The stand-alone test on the Takeaway; the falsifiability test on the Example.
- `bk lint` for the mechanical half (sections present, one H1).

**Failure modes**

- **The definition leans on jargon** — symptom: sentence one is unreadable to a newcomer. Fix: write the plain version first; let jargon arrive in sentence two, earned.
- **Mechanics is a prose wall** — symptom: a paragraph enumerating cases with "also" and "additionally". Fix: tableize; if it resists a table, it's probably two concepts ([chapter-anatomy](chapter-anatomy.md)).
- **The Takeaway won't compress** — symptom: it wants an "and". Fix: the chapter holds two concepts — split before the gate says so.
- **The Example is generic** — symptom: "a team", "some data", no names or numbers. Fix: find the real case, or add falsifiable specifics and the label.
- **The tie-in names machinery the reader doesn't have** — symptom: internal tools or plans in reader-facing text. Fix: [write-for-the-shelf](write-for-the-shelf.md) — generalize or repoint.

**Takeaway** — **each section has one move: define by difference, tabulate the mechanics, compress the takeaway to a quotable rule, make the example falsifiable, and tie in only what's on the reader's shelf.**

**Example** *(real — a sibling book, 2026-07-13)* — the gate rejected a sibling book's `one-concept-one-home` chapter for a three-sentence Takeaway; the fix was exactly step 3's compression: the same meaning refolded into one bold sentence, and the chapter passed. The same batch caught six unlabeled constructed examples — step 4's label bar, applied late instead of at writing time.

**In this system** — this chapter deepens [write-a-chapter](write-a-chapter.md)'s step 4; the gate's structure checklist tests the *outcomes* of these steps (template sections, one-sentence Takeaway, labeled examples), so following the moves here is what makes the gate a formality. → See [chapter-template](chapter-template.md) for each section's job, and [the-recipe-shape](the-recipe-shape.md) for the variant where Mechanics becomes four recipe sections.

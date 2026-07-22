---
type: recipe
description: The end-to-end procedure for writing one page — from admission test to index update — composing the standard's rules in writing order.
load_when: Sitting down to write or substantially rewrite a page — the step-by-step procedure, with each rule applied at the moment it bites.
keywords: [writing, authoring, procedure, checklist, new page, drafting]
---

# Write a page

**What it is** — the writing procedure. The standard's other pages each own one *rule*; this page owns the *order* — the sequence in which those rules bite while you write, so a writer composes them instead of discovering them at the gate. The rules are cited, not restated ([one-concept-one-home discipline](non-inferable-only.md)).

**Prerequisites**

- A concept you can name in one sentence — if you can't, there is no page yet.
- It passed admission: not inferable, not fetchable, durable ([non-inferable-only](non-inferable-only.md)).
- It has no existing home — checked via the library TOC / grep; if a home exists, you are editing, not writing.
- Sources in hand for every factual claim you intend to make ([sourced-statements](sourced-statements.md)).
- You know the book's declared audience — what's on the shelf this page ships to ([write-for-the-shelf](write-for-the-shelf.md)).

**Steps** — one observable outcome each:

1. **Name the file** — kebab-case promise of the concept ([page-anatomy](page-anatomy.md)) → the file exists and its name answers "what's inside?"
2. **Write the frontmatter** — `type`, one-sentence honest `description`, `load_when` trigger ([loading-triggers](loading-triggers.md)), `keywords` ([keywords](keywords.md)); rule pages add the `rules:` block → frontmatter parses under the strict subset.
3. **Write the H1** — one `#`, naming the concept ([toc-discipline](toc-discipline.md)) → exactly one H1, matching the filename's promise.
4. **Write the sections, in order** ([page-template](page-template.md)) — each section is written against its own bar (the per-section craft is [write-a-section](write-a-section.md)):
   - *What it is* → the concept defined in 1–3 plain sentences; jargon only after it's earned.
   - *Mechanics* → a table or short list, not prose; skip only if the definition already covers it. (Recipe pages: replace with the four recipe sections, each meeting [the-recipe-shape](the-recipe-shape.md)'s bar.)
   - *Takeaway* → exactly one bold sentence; if you can't write it, return to step 0 — the page has no concept.
   - *Example* → concrete: real and named, or labeled *(constructed, illustrative)*.
   - *In this system* → where the concept lives in the reader's machinery, ending with the page's most important within-book pointers.
5. **Classify every claim** — each factual statement visibly sourced, derived, opinion, or uncertain → no bare assertions remain.
6. **Link** — within-book links where concepts are named, cross-book canonical names never links ([interlinks](interlinks.md)) → every named concept resolves or is a recorded gap.
7. **Check referents against the shelf** — no internal machinery in reader-facing text → every referent resolves for the declared audience.
8. **Update the index in the same change** → the new page is listed in the book's `index.md`.

**Verification**

- `bk lint <book>` reports 0 errors.
- The self-read test: from the H1 + description + load_when *alone*, predict the body — then read it. Prediction wrong → fix the labels, not the reader.
- Walk the rules frontmatter of this book's pages against the draft (the gate will run the same walk; running it yourself is cheaper).

**Failure modes**

- **Two concepts emerged while writing** — symptom: the Takeaway wants to be two sentences, or the H1 needs an "and". Fix: split now ([page-anatomy](page-anatomy.md)); a split at draft time is free, at gate time it's a rejection.
- **A claim resists classification** — symptom: you believe it but can't source or derive it. Fix: mark it opinion or uncertain — honesty is a valid state; confidence is not a class.
- **The page restates what a reader could fetch** — symptom: you're summarizing another doc. Fix: point instead ([non-inferable-only](non-inferable-only.md)); keep only your non-fetchable addition.
- **The page keeps growing** — symptom: past ~120 lines or piling qualifiers mid-draft. Fix: [page-budget](page-budget.md)'s split, applied before the gate warns.

**Takeaway** — **write in the rules' order — admission, container, labels, sections, claims, links, shelf-check, index — and the gate becomes a formality instead of a surprise.**

**Example** *(real — a sibling book's history)* — a sibling book's `distinguishability` page (2026-07-12) ran this sequence: admission from a real gap (a books-review finding), a kebab-case name, honest frontmatter, the five sections with a real sourced example (the nba-demo `total_points` collision), classified claims ("Framing ours"), reciprocal links, index + log in the same change. It passed the gate on arrival; the three 07-13 REJECTs on sibling pages were all violations of steps this recipe makes explicit (an over-long Takeaway, missing example labels, a missing reciprocal pointer).

**In this system** — this is the writer's pre-flight: the writer's brief points here before any `bk create`; the gate checks the same rules on the way out. Two doors, one list. → See [page-template](page-template.md) for the section bars this recipe applies in step 4, and [the-recipe-shape](the-recipe-shape.md) for the shape this very page must satisfy.

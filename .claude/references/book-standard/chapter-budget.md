---
type: rule
description: A chapter's size is measured in characters — target ~4,000 (± 1,000; working range 3,000–5,000), recipes may run larger — and outgrowing the range is the trigger to split, not to grow.
load_when: A chapter is getting long, piling caveats, or covering two meanings — deciding whether and how to split it, or setting the size budget.
keywords: [length, size, characters, character budget, split, caveats, 4000 characters, outgrown, too thin]
rules:
  - id: quality/page-budget
    severity: warn
    scope: chapter
    statement: A chapter targets ~4,000 characters (± 1,000; working range 3,000–5,000), recipe chapters may run larger — measured in characters; outside the range, the edit that noticed it should split it (or merge a too-thin one), never just let it grow.
    gate_criteria: >
      Size is measured in characters (model-independent; tokens vary by
      tokenizer). A chapter warns (never rejects — this is a soft budget, not a
      law) when its body falls outside ~3,000–5,000 characters for a
      principle/rule/reference chapter (recipe/how-to chapters may run larger —
      roughly to 8,000 — since prerequisites + steps + verification +
      failure-modes legitimately need the room), when the current truth is
      buried under piled supersede notes, or when the H1 quietly covers two
      meanings. Below ~3,000 a concept is usually too thin and should merge into
      a neighbor; above the range a non-recipe chapter is usually smuggling in a
      second concept or piling caveats — so the expected response is a split (or
      a merge), with "one concept per chapter" (structure/one-concept-per-page)
      staying the real rule the size only approximates. Every chapter must stay
      far below the ~40,000-character (~10k-token) whole-file read cap of current
      tools. Caveat-pile and two-meanings dominate; raw size is the weakest of
      the three signals.
---

# Chapter budget

**What it is** — the size discipline for chapters, and the trigger for restructuring. A chapter has a budget measured in **characters** (model-independent; tokens vary by tokenizer): ~4,000, give or take 1,000. That range is where the library's best single-concept chapters actually land — not an arbitrary cap. When an edit would push a chapter outside it, the edit's job grows: land the change *and* split the chapter (or, if it's too thin, merge it).

**Mechanics**

Signals a chapter has outgrown — or under-filled — its budget (any one is enough):

| Signal | What it looks like |
|---|---|
| Caveat pile-up | The current truth is buried under accumulated supersede notes and edge cases. |
| Two meanings | The H1 quietly covers two distinct concepts ("customers" meaning buyers *and* accounts). |
| Size | Outside **~3,000–5,000 characters** (recipes may run larger, roughly to 8,000). Below ~3,000 the concept is usually too thin — merge it; above the range a non-recipe chapter is usually smuggling a second concept or piling caveats. Measured in characters, not lines or tokens; the weakest of the three signals. |

The split: a short current-state chapter keeps the name; specifics move to new chapters (`<concept>-history.md`, `<concept>-edge-cases.md`); pointers absorb the move so existing links keep working; index + changelog record it.

**Takeaway** — **a chapter targets ~4,000 characters (± 1,000; recipes may run larger): outside the range the edit's job is to split or merge, because size is only the visible sign that "one concept per chapter" has slipped.**

**Example** *(constructed, illustrative)* — a domain definition corrected five times over weeks swells to ~8,000 characters, a wall of caveats a reader wades through to find what's true *now*. After the split: a ~3,500-character current definition, plus `…-history.md` for the trail. Next reader pays 3,500 characters, not 8,000 — and each half is one concept again.

**In this system** — maintenance watches for the signals and proposes splits; the gate warns (not rejects) when an edit lands on a chapter outside its budget. This rule covers the *sideways* split (more chapters, same level); whether to split sideways or deepen a level instead is a separate judgment. → See [supersede-dont-delete](supersede-dont-delete.md) for the rule that makes chapters grow in the first place, and [chapter-anatomy](chapter-anatomy.md) for the one-concept rule the size only approximates.

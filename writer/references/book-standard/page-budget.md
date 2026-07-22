---
type: rule
description: When a page outgrows itself, the write that noticed it triggers a split — restructure on threshold, not on schedule.
load_when: A page is getting long, piling caveats, or covering two meanings — deciding whether and how to split it.
keywords: [length, split, budget, tokens, token budget, outgrown]
rules:
  - id: quality/page-budget
    severity: warn
    scope: page
    statement: A page stays within roughly 1,000 tokens and one sitting's read — past that, the edit that noticed it should split it. (Tokens, not chars/lines — the reader is an LLM and context budget is measured in tokens; measure with the reader model's tokenizer, ~4 chars ≈ 1 token as a rule of thumb.)
    gate_criteria: >
      A page warns (never rejects — this is a guideline, not a law) when its body
      runs past roughly 1,000 tokens, when the current truth is buried under piled
      caveats, or when the H1 quietly covers two meanings. The expected
      response to the warning is a split: a short current-state page keeps the
      name, specifics move to pointer pages, links absorb the move. Length alone
      is the weakest of the three signals; the caveat-pile and two-meanings
      signals dominate.
---

# Page budget

**What it is** — the size discipline for pages, and the trigger for restructuring. A page has a budget: one concept, readable in one sitting, current-state first. When an edit would push it past that, the edit's job grows: land the change *and* split the page.

**Mechanics**

Signals a page has outgrown itself (any one is enough):

| Signal | What it looks like |
|---|---|
| Caveat pile-up | The current truth is buried under accumulated caveats and edge cases. |
| Two meanings | The H1 quietly covers two distinct concepts ("customers" meaning buyers *and* accounts). |
| Length | Roughly past ~1,000 tokens (~4,000 chars), a reader is scanning, not reading. A guideline, not a law — the two-meanings signal dominates. |

The split: a short current-state page keeps the name; specifics move to new pages (`<concept>-history.md`, `<concept>-edge-cases.md`); pointers absorb the move so existing links keep working; the index records it.

**Takeaway** — **every write is two decisions, not one: where does this land, and has that spot just outgrown itself — restructure exactly where the writes concentrate.**

**Example** *(constructed, illustrative)* — a domain definition corrected five times over weeks becomes a wall of caveats; a reader wades through all of it to find what's true *now*. After the split: a 15-line current definition, plus `…-history.md` for the trail. Next reader pays 15 lines.

**In this system** — maintenance (Phase 5) watches for the signals and proposes splits; the gate warns (not rejects) when an edit lands on a page already past budget. This is A-MEM's restructure-on-write, applied to books. This rule covers the *sideways* split (more pages, same level); whether to split sideways or deepen a level instead is a separate judgment.

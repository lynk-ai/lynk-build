---
type: principle
description: Sources split when too big and merge when duplicated — and nothing forces this refactor, so budget for it.
---

# Living sources

**What it is** — the recognition that a source of truth doesn't stay put. It grows until it's too big or too blurred to stay accurate, and then it needs to be *split* into focused pieces; or two sources drift into saying almost the same thing, and they need to be *merged* before they disagree.

**Mechanics**

| Move | Trigger | The risk if skipped |
|---|---|---|
| **Split** | Size or accuracy drift — one "customers" source quietly covering two different business meanings of customer. | Every answer that reads it gets a little wrong, silently. |
| **Merge** | Duplication — two sources answering the same question slightly differently. | A clash waiting to happen: readers get whichever version they found first. |

The catch, and the reason this page exists: **nothing forces the refactor.** Code that outgrows its structure fails review or fails to compile. Context that outgrows its structure just quietly degrades every answer that reads it. Pointers absorb the move — readers migrate, nothing breaks loudly.

**Takeaway** — **budget for context refactoring the way you budget for code refactoring — split when too big, merge when duplicated — because nothing will force it for you.**

**Example** *(constructed, illustrative)* — a wiki note gets corrected and refined for weeks until it's a wall of caveats; a reader wades through the whole pile to find what's true *now*. The split — short current definition + pointer pages — costs one edit and repays every future read.

**In this system** — the Book Standard · `page-budget` turns this principle into an enforceable rule (the signals, the split procedure), and maintenance (Phase 5) is the actor whose *job* it is — so the refactor nobody is forced to do becomes somebody's responsibility. → See [memory-shapes](memory-shapes.md) — A-MEM is this principle running inside a memory system.

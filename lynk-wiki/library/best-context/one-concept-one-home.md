---
type: principle
description: Every fact has exactly one home; everything else points at it — the structural rule that makes clash impossible.
---

# One concept, one home

**What it is** — the structural rule that prevents [clash](four-failure-modes.md) instead of detecting it: every concept, definition, or rule lives in exactly **one** place, and everything else *points* there. Duplication isn't a style problem — it's two sources of truth waiting to disagree.

**Mechanics** — the test that decides where something lives:

| Signal | Shared (one home, pointed-to) | Private (stays local) |
|---|---|---|
| Would two readers legitimately disagree about this? | No — it's ground truth. | Yes — it's a working opinion. |
| Has it been promoted (reviewed, merged)? | Yes. | Not yet. |
| Example | A canonical definition or rule. | A draft's in-progress reasoning. |

Two corollaries:
- **Pointers, not copies.** A copy is a fork; a pointer survives the original's edits. Collections (shelves, reading lists) are lists of pointers, never duplicates.
- **Promotion is the door.** A private opinion becomes shared truth only by passing review — until then it has no home in the shared layer, no matter how confident it sounds.

**Takeaway** — **if two readers could never legitimately disagree about it, it gets one shared home that everything else points to; if they could, it stays private until it earns promotion.**

**Example** *(constructed, illustrative)* — a team keeps its "customer" definition in three docs. Two get updated after a pricing change; the third doesn't. Every reader of doc three is now confidently wrong, and no diff will ever flag it — the clash was *built in* the day the second copy was made.

**In this system** — the quality rubric is defined once in PLAN.md and pointed at by Book 2, the gate, and the evals; Book 2 cites Book 1 instead of restating it; no rule lives in both books; shelves are lists, never copies. When this repo's plan gained a Notion mirror, we declared the repo the single source of truth — a mirror is a pointer with a refresh problem, and naming the winner *is* the rule. → See [living-sources](living-sources.md) for what happens when one home outgrows itself, and [distinguishability](distinguishability.md) — its complement: this page decides *where a concept lives* and kills duplicates; distinguishability decides *whether two coexisting things are actually distinct* and separates the genuine pair by name and description.

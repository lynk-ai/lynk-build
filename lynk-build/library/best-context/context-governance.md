---
type: principle
description: Keeping context clean is a job someone must own — ongoing watcher or static checkpoint, decided once.
---

# Context governance

**What it is** — the failure modes don't prevent themselves. Compressing and isolating are *operations* anyone can invoke when they notice a problem; **governance** is different — giving something the actual *job* of catching problems before they happen, on purpose, not as a side effect of whoever happens to be working.

**Mechanics** — two shapes, one decision:

| Shape | Behavior | Cost profile |
|---|---|---|
| **Ongoing** | Runs continuously, intervenes automatically — no one has to ask. | Pays constantly, catches early. |
| **Static** | Sits idle until explicitly called at a checkpoint. | Pays once per checkpoint, catches late but decisively. |

Everyday version: a spell-checker running as you type is *ongoing*; running it once before you submit is *static*. Same goal, different cost and coverage. This is the same axis as [hook-vs-router](hook-vs-router.md) — an ongoing governor is hook-shaped, a static one is router-shaped.

**Takeaway** — **someone has to own keeping context clean — decide once whether that's a continuous watcher or an on-demand check, and never leave it as nobody's job.**

**Example** *(constructed, illustrative)* — a builder agent on a long derivation drifts: its early assumptions rot as it learns more, but nothing rereads them. An ongoing governor would flag the drift mid-run; a static one catches it at the publish checkpoint. Without either, the drift ships — because catching it was nobody's job.

**In this system** — governance is split deliberately: **the gate** is the static governor (one fail-closed check at the only transition that matters — entering the library), and **maintenance** is the ongoing one (watching for page-budget violations, dead links, stale indexes in the background). Neither is a side effect; both are named jobs. → See [hook-vs-router](hook-vs-router.md) for the mechanism each shape uses.

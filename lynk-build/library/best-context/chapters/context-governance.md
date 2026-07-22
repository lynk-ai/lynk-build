---
name: Context governance
description: Keeping context clean is a job someone must own — ongoing watcher or static checkpoint, decided once. Read when nobody owns keeping context clean, or you're assigning that job — continuous watcher vs on-demand checkpoint.
---

The failure modes don't prevent themselves. Compressing and isolating are *operations* anyone can invoke when they notice a problem; governance is different — it gives something the actual *job* of catching problems before they happen, on purpose, not as a side effect of whoever happens to be working.

There are two shapes, and one decision between them. An **ongoing** governor runs continuously and intervenes automatically — no one has to ask — so it pays constantly but catches early. A **static** governor sits idle until explicitly called at a checkpoint — it pays once per checkpoint and catches late but decisively. The everyday version: a spell-checker running as you type is ongoing; running it once before you submit is static. Same goal, different cost and coverage. This is the same axis as [hook-vs-router](hook-vs-router.md) — an ongoing governor is hook-shaped, a static one is router-shaped.

**Someone has to own keeping context clean — decide once whether that's a continuous watcher or an on-demand check, and never leave it as nobody's job.** The failure when nobody owns it: a builder agent on a long derivation drifts as its early assumptions rot, but nothing rereads them — an ongoing governor would flag the drift mid-run, a static one would catch it at the publish checkpoint, and with neither, the drift ships because catching it was nobody's job.

In practice governance splits into two named jobs. **Admission** is the static governor — a fail-closed check at the one transition that matters, when something enters a trusted store — and **upkeep** is the ongoing one, watching for outgrown pages, dead links, and stale indexes in the background. Neither is a side effect; both are owned. See [hook-vs-router](hook-vs-router.md) for the mechanism each shape uses.

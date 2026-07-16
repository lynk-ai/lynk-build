---
type: principle
description: The core wager of lazy loading — cost scales with what a task uses, not with everything that exists, so a library can grow without making every session more expensive.
---

# The economics of progressive disclosure

**What it is** — the wager the whole pattern rests on: you load context *lazily*. A small index of everything is always present; the full body of a page is loaded only when a task actually reaches for it. So the price of a session tracks what the task **touches**, not what the library **contains** — and a library can grow without making every session more expensive.

**Mechanics** — two prices, paid at different times:

| Price | Paid for | When |
|---|---|---|
| **Pointer price** | Everything that exists — a name and a one-line description per page. | Always, up front, at discovery. |
| **Full price** | The body of a page. | Only when a task matches and opens it. |

The pointer price is small and roughly constant per item, so the discovery layer grows slowly (linearly, and cheaply) as the library grows. The full price is paid only on the handful of pages a task actually uses. Add a hundred pages nobody touches this session and the session's cost barely moves — that is the entire point (derived: cost = discovery-cost + Σ full-price over touched pages; growing untouched pages only grows the small first term).

**Takeaway** — **pay a pointer for everything that exists; pay full price only for what the task actually touches.**

**Example (constructed)** — a library grows from 20 pages to 200. Discovery stays flat: the librarian scans one line per book, and the per-page scan is each scout's, still flat per task; a task that needed 3 pages before still needs ~3 pages now. The 180 new pages cost their pointers and nothing more until some future task matches them. Ten times the knowledge, near-constant cost per session. *(superseded 2026-07-14: previously "Discovery stays a flat ~one-line-per-page scan the librarian reads either way" — pipeline restructured to the pointer flow: the librarian scans one line per book, the per-page scan is each scout's; see log.md)*

**In this system** — this is Book 1's SELECT (the Best Context book · `four-operations`) run as an *economy*: not just "pull back only what's relevant" but "structure the store so that pulling back is cheap by default." → See [three-stages](three-stages.md) for the mechanism that charges these two prices, and [habit-vs-contract](habit-vs-contract.md) for why the cheap default has to be *enforced* to be trustworthy.

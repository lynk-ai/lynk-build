# Index

**Book 1 — Best Context.** The *why* of the system: the principles that decide what an agent should see, when, and from where. Book 2 (The Book Standard) applies these principles to books; the gate enforces Book 2. No rule lives in both books — Book 2 cites this one.

**Primary source:** `docs/talk-outline.md` — most pages below have a near-complete draft there already; writing a page = extracting, tightening, and adding the "In this system" tie-in.

**Page shape:** every page follows the concept template (defined in Book 2's `page-template.md`): *What it is → Mechanics → Takeaway → Example → In this system.*

Status: **12 pages drafted** (distinguishability added 2026-07-12 from a books-review gap). Pages 1, 2, 6, 8 were drafted by Claude from the talk (generic examples, no Lynk data) — they remain **Shaked's pages**: voice-pass and merge pending. The others await review.

## Part I — The problem

| # | Page | One-liner | Author | Source |
|---|---|---|---|---|
| 1 | `context-rot.md` | Answer quality drops as context grows — before the window is full. The problem everything else fights. | **Shaked** | Talk §A |
| 2 | `four-failure-modes.md` | Poisoning, distraction, confusion, clash — same symptom, four different fixes. | **Shaked** | Talk §A |

## Part II — The levers

| # | Page | One-liner | Author | Source |
|---|---|---|---|---|
| 3 | `four-operations.md` | WRITE / SELECT / COMPRESS / ISOLATE — the four levers on the context window. | Claude | Talk §A |
| 4 | `progressive-disclosure.md` | **Stub** — graduated to its own book (book-3-progressive-disclosure). Small index always; full content on demand. | Claude | Talk §B |
| 5 | `isolation-and-strict-briefs.md` | **Stub** — graduated to book-5-subagents (Subagents). Heavy work in isolated windows; strict briefs keep blind workers from colliding; only condensed cited results return. | Claude | Talk §D |

## Part III — The rules of truth

| # | Page | One-liner | Author | Source |
|---|---|---|---|---|
| 6 | `one-concept-one-home.md` | Every fact has exactly one home; everything else points at it. The anti-clash rule — plus the shared-vs-private test. | **Shaked** | Talk §C |
| 7 | `living-sources.md` | Sources split when too big, merge when duplicated — nothing forces this refactor, so budget for it. | Claude | Talk §C |
| 8 | `self-compiled-vs-curated.md` | Agent-written vs human-written knowledge — the same artifact before and after review. Why meta-books are human-gated. | **Shaked** | Talk §B |
| 9 | `distinguishability.md` | When two things a reader must choose between coexist, the difference must show in BOTH the name and the description — the complement of one-concept-one-home. | Claude | nba-demo finding 1.6 |

## Part IV — The guards

| # | Page | One-liner | Author | Source |
|---|---|---|---|---|
| 10 | `hook-vs-router.md` | Hooks raise the floor (fire themselves, skip silently); the router guards the door (explicit, fail-closed). Hooks feed the router. The gate's theoretical foundation. | Claude | Talk §C |
| 11 | `context-governance.md` | Keeping context clean is a *job*, not a side effect — ongoing watcher vs static checkpoint. | Claude | Talk §A |
| 12 | `memory-shapes.md` | Four ways memory evolves (paging/archive-diff · restructure-on-write · score-and-reflect · verified-methods) — one idea to steal from each. Feeds the maintenance flow. | Claude | Talk §A |

## Why this split

Shaked takes the pages carrying the talk's core opinions and Lynk experience (1, 2, 6, 8); Claude drafts the mechanical/reference pages from the talk source (3, 4, 5, 7, 10, 11, 12), for Shaked's review. Every page merged by Shaked. Page 9 (distinguishability) was added later from a books-review gap surfaced by the Lynk docs.

## Sources

- `docs/talk-outline.md` — the talk, sections A–F (primary; saved in this repo)
- `docs/candlekeep-dossier.html` — worked examples of every principle in a shipped system
- `docs/build-vs-docs-findings-2026-07-12.md` — the nba-demo finding (1.6) grounding the distinguishability page

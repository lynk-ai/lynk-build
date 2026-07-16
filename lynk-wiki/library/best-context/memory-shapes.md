---
type: principle
description: Four ways memory evolves — paging, restructure-on-write, score-and-reflect, verified methods — one idea to steal from each.
---

# Memory shapes

**What it is** — four real systems that each answered "how does stored knowledge evolve without rotting?" differently. None is *the* answer; each contributes one idea this system steals. (Background: even the systems' authors admit the problem — Letta on MemGPT: "incremental memory formation… may become messy and disorganized over time." Memory rot is real.)

**Mechanics** — the four shapes and their steals:

| System | Shape | The one idea to steal |
|---|---|---|
| **MemGPT / Letta** | Paging — working copy vs. archival copy; flush/summarize on a token threshold. | **The archive-diff ritual:** end of every run, diff working state against the archive and make one deliberate call — did this session *earn* a write? Updates become decisions, not side effects. |
| **A-MEM** | Living graph — each new note can re-link, merge, or rewrite old notes. | **Restructure on write:** every write asks "has this spot outgrown itself?" — the hierarchy deepens exactly where writes concentrate. |
| **Generative Agents ("Smallville")** | Score and reflect — every memory scored at write time; reflection passes promote raw observations into insights. | **Judge at write time:** a flat log never becomes knowledge on its own. (Its weakness — the judge is one LLM — is fixed by scoring with several independent lenses.) |
| **Voyager** | Verified methods — memory units are runnable code that proves itself on every use. | **The write-gate is the runtime, not an opinion:** when a memory can be a *method* instead of a fact, store the verified method. |
| **Letta MemFS** (Feb 2026) | Git as memory — markdown files in a git-backed filesystem; every change auto-committed; a background *sleep-time agent* reviews the session and merges its commits back via worktrees. | **Production proof of the whole shape:** memory writes as reviewed commits, files over databases. The "PR shape" for knowledge isn't a proposal — it shipped. |

Two upgrades to the paging steal, sourced: **when to compress is a decision, not a threshold** — "Self-Compacting Language Model Agents" (June 2026) shows agents deciding compaction moments via a rubric (sub-task resolved? trajectory converging?) beat token-threshold triggers at a fraction of the cost. And **WRITE/COMPRESS are now API primitives** — Anthropic ships a file-based memory tool and automatic context editing as platform features (Sept 2025), not framework hacks.

**Takeaway** — **memory doesn't stay true by being appended to — each shape earns its keep by deciding, at write time, what a write is allowed to do.**

**Example** — the same correction, four ways: paged out and diffed at session end (MemGPT); triggering a re-link of three related notes (A-MEM); scored high and promoted to an insight (Smallville); saved as a checkable rule instead of prose (Voyager).

**In this system** — maintenance (Phase 5) is built from steals 1 and 2 (the archive-diff ritual + restructure-on-write → the Book Standard · `page-budget`); the manuscript-style criteria are steal 3 (judge at write time); the gate aspires to steal 4 — its checklists are as close to "runnable" as prose rules get; and MemFS is external validation of our substrate itself: books as markdown in git, writes as reviewed commits. → See [living-sources](living-sources.md) for the principle A-MEM implements.

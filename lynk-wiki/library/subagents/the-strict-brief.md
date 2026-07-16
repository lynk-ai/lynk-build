---
type: principle
description: A blind worker can only act on what you hand it — the four-part brief (objective, output format, tool guidance, boundaries) and a strict, pre-declared return contract (never a raw transcript) decide everything.
---

# The strict brief

**What it is** — the instruction packet you hand an isolated subagent. Because an isolated worker is blind ([isolation-is-a-decision](isolation-is-a-decision.md)) — no history, no shared memory — the brief is the *only* thing shaping its work. Get it wrong and blind workers collide; get it right and they cover ground in parallel without stepping on each other.

**Mechanics** — the four-part formula and the return contract:

| Part of the brief | What it fixes |
|---|---|
| **Objective** | What this worker is for — the one question, not the whole problem. |
| **Output format** | The shape of the answer, so returns compose instead of clashing. |
| **Tool guidance** | Which tools and sources to use, so workers don't reinvent or over-search. |
| **Task boundaries** | Where this worker stops, so two workers don't do the same job. |

These four are Anthropic's documented requirement, verbatim: each subagent task needs "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries" (source: anthropic.com/engineering/multi-agent-research-system, fetched 2026-07-07).

Two failure modes the same post documents:
- **Vague briefs** — leads giving "short instructions like 'research the semiconductor shortage'" made workers "duplicate work, leave gaps, or fail to find necessary information" (same source).
- **Over-scaling** — "spawning 50 subagents for simple queries" (same source).

The **return contract** is the other half: the contract declares the return's shape up front and keeps it small — classically condensed, cited findings; in our pointer flow, POINTER lines with the hook delivering the chapters — never raw transcripts. *(superseded 2026-07-14: previously "workers return condensed, cited findings — never raw transcripts" — pipeline restructured to the pointer flow: the contract declares the shape up front; findings classically, POINTER lines here; see log.md)* Why the return must stay small is Book 3's budget principle; this page points there rather than restating it → the Progressive Disclosure book · `pointers-not-content`.

**Takeaway** — **a blind worker acts only on its brief, so hand it all four parts — objective, output format, tool guidance, boundaries — and demand a strict, pre-declared return contract, never a raw transcript.**

**Example** — real: this book's own source notes (`docs/subagents-notes.md`) were produced by a two-agent research pass under strict briefs — each agent given an objective (fetch and verify vendor docs / papers), an output format (sourced bullets with URLs or arXiv ids), tool guidance (fetch the named pages), and boundaries (mark anything unconfirmed `UNVERIFIED`, never substitute memory for a fetch). The return was condensed, cited findings — exactly the contract, and the reason this book can cite line-by-line.

**In this system** — every spawn here carries the four-part brief: the librarian's routing list *is* a brief-generator (book + objective, per query) — chapter choice is the scout's own procedure; scouts return pointers, never pages, and a hook delivers the pointed chapters to the orchestrator as primary text. *(superseded 2026-07-14: previously "the librarian's reading list is a brief-generator (book + pages + why, per query), and readers return cited findings, never the pages themselves", and the Takeaway previously read "demand a condensed, cited return, never a transcript" — pipeline restructured to the pointer flow: the enduring principle is a strict, pre-declared return contract (condensed-cited findings classically, pointer lines ours); see log.md)* → See [orchestrator-workers](orchestrator-workers.md) for the pattern that composes many strict briefs at once, and [gates-and-ablation](gates-and-ablation.md) for turning each return into a checkable artifact.

---
type: principle
description: A lead agent decomposes a task and fans it out to parallel isolated workers that return per a strict contract (classically condensed findings; in our pointer flow, pointers with a hook delivering the chapters) — a pattern that costs ~15x the tokens and must earn it.
---

# Orchestrator-workers

**What it is** — the fan-out pattern: a lead agent decomposes a task, dispatches specialized workers that run in parallel in their own windows, and receives back a contracted return — classically condensed findings; in our pointer flow, pointer lines with the hook delivering the chapters — never transcripts. *(superseded 2026-07-14: previously "receives back condensed findings — never transcripts" — pipeline restructured to the pointer flow: the return is a strict contract; findings classically, POINTER lines with the hook fetching chapters here; see log.md)* It is the two prior pages composed: many strict briefs ([the-strict-brief](the-strict-brief.md)) dispatched into isolation ([isolation-is-a-decision](isolation-is-a-decision.md)).

**Mechanics** — the pattern, and the economics that decide whether to use it (all sourced to anthropic.com/engineering/multi-agent-research-system, fetched 2026-07-07):

| Property | Detail |
|---|---|
| Decompose | "A lead agent coordinates the process while delegating to specialized subagents that operate in parallel." |
| Return | Each worker returns its contracted return to the lead — findings classically, POINTER lines here — never its raw window. |
| Performance | The multi-agent system (Opus 4 lead + Sonnet 4 workers) outperformed single-agent Opus 4 by **90.2%** on Anthropic's internal research eval. |
| Cost | Single agents use ≈**4×** chat tokens; multi-agent systems ≈**15×** chat tokens. |
| What drives it | Three factors explained 95% of eval variance; **token usage alone explains 80%**. |

*(superseded 2026-07-14: the Return row previously read "Each worker returns condensed findings to the lead, not its raw window" — pipeline restructured to the pointer flow: the return is a strict contract; findings classically, POINTER lines here; see log.md)*

The economics are the whole decision. At ~15× chat tokens, the pattern must **earn its cost**: it pays for breadth-heavy work (parallel research across many sources) and loses on simple queries — which is exactly Anthropic's own over-scaling failure, "spawning 50 subagents for simple queries" (same source, see [the-strict-brief](the-strict-brief.md)). Token usage explaining 80% of performance variance cuts both ways: more tokens buy more quality, but only where the task has enough breadth to spend them on.

**Takeaway** — **orchestrator-workers buys ~90% more quality on breadth-heavy research at ~15x the tokens — so spend it where the breadth earns the cost, and never on a simple query.**

**Example** — real: Anthropic's research system is the pattern's origin (the 90.2% and 15× figures above are theirs). In this library, the librarian is the lead: it scans the shelf, decomposes a question into one brief per relevant book (each scout scans its own book's TOC), and fans out scouts in parallel; each scout judges its own book in isolation and returns pointers, and a hook delivers the pointed chapters' primary text to the orchestrator, so the orchestrator's window holds only the targeted chapters, not the whole shelves. *(superseded 2026-07-14: previously "each reader chews through its book in isolation and returns cited findings, so the librarian's window holds summaries, not the shelves" — pipeline restructured to the pointer flow: scouts return pointers only and a hook fetches the chapters; see log.md)*

**In this system** — the librarian → scouts fan-out *is* this pattern, and the fan width is a budget decision: cost scales with how many books the shelf scan flags, so routing decides spend. *(superseded 2026-07-14: previously "cost scales with how many books the TOC scan flags" — pipeline restructured to the pointer flow: the librarian scans the shelf, not TOCs; see log.md)* → See [gates-and-ablation](gates-and-ablation.md) for checking each worker's returned artifact, and [the-strict-brief](the-strict-brief.md) for the brief each worker carries.

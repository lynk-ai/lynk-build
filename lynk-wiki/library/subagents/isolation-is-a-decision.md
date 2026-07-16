---
type: principle
description: Whether a subagent shares or isolates context is a design choice with a real cost — frameworks default differently, so decide it on purpose.
---

# Isolation is a decision

**What it is** — the choice of whether a subagent runs in its own fresh context window or shares state with its parent and siblings. Isolation contains a worker's mess so it never pollutes the caller, but it makes the worker *blind* — and it isn't free. Frameworks pick different defaults, so the choice is yours to make on purpose.

**Mechanics** — how the shape varies across systems (each claim sourced):

| System | Default | Detail |
|---|---|---|
| **Claude Code** | Isolate hard | "Each subagent starts with a fresh, isolated context window" — no history, no already-read files; the parent "composes a delegation message that summarizes the task"; only "the relevant summary returns" (nested: only the top-level summary). Nesting max depth 5; `isolation: worktree` runs it in an auto-cleaned temp git worktree. Source: code.claude.com/docs/en/sub-agents, fetched 2026-07-07. |
| **Claude Code fork** | Inherit, still return | The documented exception: a fork inherits the entire conversation (drops input isolation) but still returns only its final result. Same source. |
| **LangGraph** | Subagents stateless | Subagents are "stateless by design" — they start fresh each call; state persists via handoffs, not the subagent. Source: docs.langchain.com/oss/python/langchain/multi-agent. |
| **CrewAI** | Context per task | A task's `context` attribute names prior tasks whose outputs flow in; crew-level shared memory is an opt-in layer. Source: docs.crewai.com/en/concepts/crews. |
| **Letta** | Isolated worktrees | Subagents get isolated git worktrees with standard conflict resolution (source: `docs/research-brief-2026-07.md`). |

Isolation's cost is named by the docs themselves: **latency** — "Subagents start fresh and may need time to gather context" (source: code.claude.com/docs/en/sub-agents). A blind worker must re-gather what the parent already knew.

**Takeaway** — **isolation is a design decision with a real cost — a fresh worker must re-gather context — so choose share-vs-isolate on purpose, because your framework's default won't choose it for you.**

**Example** — real: Claude Code's `isolation: worktree` gives a subagent its own temp git worktree, auto-cleaned when it finishes (source: code.claude.com/docs/en/sub-agents) — hard isolation you opt into per agent. Contrast CrewAI, where a task receives prior task outputs through its `context` attribute unless you leave that list empty (source: docs.crewai.com/en/concepts/crews) — sharing is the path of least resistance.

**In this system** — every agent here runs isolated: librarian, book-reader, book-writer, and the gate each get a fresh window and return a condensed result. Isolation is the ISOLATE lever from the Best Context book · `four-operations`, and the reason blind workers still cooperate is the next page's subject. → See [the-strict-brief](the-strict-brief.md) for what you hand a blind worker, and [call-return-vs-handoff](call-return-vs-handoff.md) for how control gets back to the parent.

# Run report — s1-exists

**Brief ask (verbatim):** "What is context rot and why does long context degrade?"
**Trigger:** user question routed to the writer as a coverage check (search miss).
**Date:** 2026-07-21

## DIAGNOSE decision

**Case 1 — EXISTS, retrieval missed it.**

Reasoning: read the frontmatter of the only book, `library/best-context/index.md`, then the frontmatter and bodies of the two candidate chapters. The ask decomposes into two halves, and each maps 1:1 onto an existing chapter:

- *"What is context rot"* → `chapters/context-rot.md` — defines the phenomenon (quality drops as context grows, even relevant context, starting before the window is full), cites Chroma 2025, and covers the volume + placement axes.
- *"Why does long context degrade"* → `chapters/why-context-rots.md` — measured thresholds (NoLiMa 32K collapse, single-distractor effect, ContextRot give-up, GAR decay) and attention-level mechanisms (causal attention favoring early tokens, RoPE decay, lexical string-matching bias).

The knowledge is fully present; nothing is missing or partial. Per the playbook, the only action is a findability fix — **write no new content**.

Findability diagnosis of why the query could have missed:
- `why-context-rots.md` labels contained neither "context rot" nor "long context" (only benchmark/mechanism jargon: NoLiMa, Ms-PoE, RoPE, ...). A label-driven match on the query terms would skip the chapter that answers the "why" half.
- The book `index.md` description never said "context rot" or "long context degrades" in prose (only in the labels array).

## Stages run

| Stage | Ran? | What it did |
|---|---|---|
| 0 — Brief check | yes (orchestrator) | Brief complete: ask, searched/missed, gap all present. No user clarification needed. |
| 1 — DIAGNOSE | yes (orchestrator, no subagent) | Listed library, read index frontmatter + both candidate chapters. Verdict: case 1 (EXISTS). |
| 2 — RESEARCH | **not run** | Case 1 terminates before research. |
| 3 — AUTHOR | **not run** | No new content permitted in case 1. |
| 4 — VERIFY | **not run** | Nothing drafted, nothing to verify. |
| 5 — PROMOTE | **not run** | No draft to promote. Findability metadata edits are the case-1 prescribed action and were applied directly to index/chapter frontmatter. |
| 6 — RETURN | yes | found-existing message with pointer + cited answer (final message). |

No subagents were spawned (case 1 requires none).

## Data sources used

- `runs/s1-exists/library/best-context/index.md` (frontmatter)
- `runs/s1-exists/library/best-context/chapters/context-rot.md` (full read)
- `runs/s1-exists/library/best-context/chapters/why-context-rots.md` (full read)
- `writer/skills/book-writer/SKILL.md` (the playbook)
- Directory listing of the sandbox library (find)

No web, repo-code, or external sources were consulted — none are needed for a case-1 diagnosis.

## Terminal state

**found-existing**

## Files created or modified

Modified (findability metadata only, no body content changed):
- `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s1-exists/library/best-context/index.md` — description now names "context rot" and "why long context degrades" in prose; labels gained `long context`, `degradation`, `why context rots`.
- `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s1-exists/library/best-context/chapters/why-context-rots.md` — labels gained `context rot`, `long context`, `degradation`.

Created:
- `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s1-exists/report.md` (this report, eval instrumentation)

No files written to drafts/. No new chapters or books.

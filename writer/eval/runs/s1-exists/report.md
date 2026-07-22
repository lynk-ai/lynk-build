# Run report — s1-exists

**Brief**: Ask (verbatim): "What is context rot and why does long context degrade?" · searched: routed as a coverage check · gap: whether the library covers context rot and its causes · target: unknown.

## DIAGNOSE decision

**Case 1 — EXISTS, retrieval missed it** (terminal state: *found-existing*).

Reasoning: read the frontmatter of the single book `library/best-context/index.md`, then the two candidate chapters flagged by filename. The ask decomposes into two halves, and each is fully covered by an existing chapter:

- *What is context rot* → `library/best-context/chapters/context-rot.md` — defines the phenomenon (quality drops as context grows, even relevant context, before the window is full; Chroma 2025) and the compound-vs-pile resolution.
- *Why does long context degrade* → `library/best-context/chapters/why-context-rots.md` — measured thresholds (NoLiMa 32K collapse, single-distractor effect, focused-vs-full, give-up rates) and attention-level mechanisms (causal attention favors early tokens, RoPE decay, lexical string-matching, goal-attention decay), with honest caveats.

No content gap exists, so per the playbook: **write no new content**; fix findability only.

Findability diagnosis: `why-context-rots.md`'s labels were entirely evidence-artifact terms (NoLiMa, RoPE, Ms-PoE, Chroma, ...) and contained none of the query's own vocabulary ("context rot", "long context", "degradation"). The book index labels lacked "long context", and its description never named context rot despite it being the book's core problem.

## Stages run

| Stage | Ran? | Notes |
|---|---|---|
| 0 Brief check | yes | Brief complete (ask, searched, gap) — proceed |
| 1 DIAGNOSE | yes | Case 1: EXISTS → findability fix only |
| 2 RESEARCH | no | skipped — content already exists |
| 3 AUTHOR | no | skipped |
| 4 VERIFY | no | skipped — no draft; Case 1 assigns metadata findability edits to the orchestrator |
| 5 PROMOTE | no | skipped — nothing to promote |
| 6 RETURN | yes | found-existing pointer + cited answer to the original ask |

No subagents were spawned (Case 1 is the orchestrator's own step).

## Data sources

- `library/best-context/index.md` (frontmatter: name, description, labels, sources)
- `library/best-context/chapters/context-rot.md` (full read)
- `library/best-context/chapters/why-context-rots.md` (full read)
- Directory listing of `library/best-context/chapters/` (candidate identification)
- No web, repo, or external sources — none needed for a Case-1 diagnosis.

## Terminal state

**found-existing**

## Files touched

1. `library/best-context/chapters/why-context-rots.md` — labels extended with query-vocabulary terms: `context rot`, `long context`, `degradation`, `why long context degrades`. Content untouched.
2. `library/best-context/index.md` — labels extended with `long context`, `long-context degradation`; description now explicitly names context rot and its causes. Sources and content untouched.
3. `report.md` (this file).

No files written to drafts; no chapter content created or modified.

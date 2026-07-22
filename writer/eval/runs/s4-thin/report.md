# Run report — s4-thin

**Brief (verbatim ask):** "Write a chapter with measured production failure-rate benchmarks for multi-agent LLM systems"
**Trigger:** direct request, no prior search. Gap: hard measured data (failure rates, benchmarks) on multi-agent LLM systems in production.
**Terminal state:** **created** (with an honest scope caveat: the "production" half of the ask is answered by a verified negative finding, not by numbers — see Data sources).

## DIAGNOSE decision

**Case: ABSENT.** The library held exactly one book, `best-context` — scoped ("the why of context engineering") to context-engineering principles. Read every index frontmatter and all 20 chapter frontmatters: no chapter carries multi-agent failure-rate measurements (`why-context-rots` has measured numbers, but for context rot; `isolation-and-strict-briefs` covers subagents at the principles level; `four-failure-modes` is the context-failure taxonomy, not MAST).

**Placement call:** default per playbook is a new chapter in the best-fitting existing book — but the book-standard's `scope-fit` rule (structure/scope-fit, severity error) rejects exactly this placement, using a multi-agent failure-rate chapter in the context book as its own worked example, and warns "the best-fitting book must never mean the only book". Admitting the chapter to `best-context` would require appending a new subject clause to its index description — a fail by the rule's mechanical diff test. `scope-fit` names the fix: "placement in the book whose scope already fits, or a new book when none does." None does → **new book** `multi-agent-reliability`, kept deliberately minimal (index + one chapter) since the evidence supports one chapter, not a multi-page book. The book-standard's `write-a-book` cluster prerequisite was weighed honestly: this is one concept, but with no valid existing home the single-chapter new book is the only placement that doesn't break scope-fit; growth room (production telemetry, if ever published) is real.

## Stages

1. **DIAGNOSE** (orchestrator) — ABSENT; new book `multi-agent-reliability`, one chapter `measured-failure-rates`.
2. **RESEARCH** — 1 round (researcher agent, web-first).
3. **AUTHOR** — initial draft + 3 correction cycles.
4. **VERIFY** — 4 fresh verifier spawns: CORRECTION_NEEDED (3 content/source flags) → CORRECTION_NEEDED (1 flag: "only"→"first" exclusivity upgrade) → CORRECTION_NEEDED (1 mechanical flag: index `sources` invalid YAML) → **APPROVED** (full checklist CHECK).
5. **PROMOTE** — files copied into the sandbox library; `verdict.json` with sha256 hashes left in drafts; mechanical re-check passed (both frontmatters parse; required keys present; index sources = 11 entries). New book brings its own index, so no host-book findability edit was needed — and deliberately none was made to `best-context` (scope-fit).

## Research rounds and why they stopped

**1 round of 3 used.** Round 1 returned strong benchmark-measured evidence (all primary-source verified) plus an explicit, well-searched negative finding: **no public task-level production failure telemetry for multi-agent LLM systems exists** — the three closest candidates each disqualify (Anthropic = internal unaudited eval; Datadog = span-level infra errors, wrong denominator; SSRN 7041478 = unverifiable preprint). Further rounds could not manufacture data that isn't public; re-running would have been padding. The scope was adjusted at authoring instead: benchmark numbers presented as benchmark numbers, the production gap stated as the chapter's opening (derived) finding, and the circulating "70–95% fail in production" pseudo-statistic debunked by tracing its inputs.

## Data sources (as shipped in the book index, with standing)

- MAST — "Why Do Multi-Agent LLM Systems Fail?" (arXiv:2503.13657, ICML 2025) — sourced; per-system benchmark failure rates 41–86.7%, taxonomy frequencies, v2-vs-v3 citation trap documented
- τ-bench (arXiv:2406.12045, ICLR 2025) + Sierra engineering blog — sourced; pass^1 vs pass^8 reliability decay
- TheAgentCompany (arXiv:2412.14161, NeurIPS 2025 D&B) — sourced with inline caveat (verified against NeurIPS listing, not the PDF)
- Who&When (arXiv:2505.00212, ICML 2025) — sourced; failure attribution 53.5%/14.2%
- Anthropic engineering blog, multi-agent research system (2025) — sourced, marked internal/unaudited, not production telemetry
- Datadog, State of AI Engineering — sourced, marked span-level infrastructure telemetry, explicitly not task-level failure rates
- medRxiv 2025.08.22.25334049 — uncertain (unverifiable preprint), marked as such in the chapter
- GISclaw (arXiv:2603.26845) — uncertain (numbers via search summaries), marked as such
- Fiddler AI blog — cited only as the object of a debunking
- SSRN 7041478 — unverifiable; its 75.17% figure explicitly barred from being cited as fact
- MIT "GenAI Divide" 95% figure — appears only as not-independently-verified, inside the debunking derivation (not a source)

## Verify-cap accounting

The playbook caps author⇄verify at 3 rounds, read as 3 correction cycles (returns to Stage 3): cycle 1 (3 flags — MIT figure classification, 7-vs-6 table reconciliation, index sources coverage), cycle 2 (one-word exclusivity fix), cycle 3 (YAML quoting only, zero content change). The verifier of the final round approved on a full fresh checklist. Had it not approved, the run would have terminated honestly (degraded/nothing-written) rather than spending a fourth cycle.

## Operational note

The cycle-1 author retry was mistakenly resumed as a background child (SendMessage); it applied all three fixes to the draft files but stalled before returning a report. The fixes were confirmed by direct read of the draft; subsequent stage agents were spawned foreground per the playbook.

## Files

- Promoted: `runs/s4-thin/library/multi-agent-reliability/index.md` (sha256 9ecf6c7a…873f1e)
- Promoted: `runs/s4-thin/library/multi-agent-reliability/chapters/measured-failure-rates.md` (sha256 939eb10a…1acd22)
- Audit trace: `runs/s4-thin/drafts/multi-agent-reliability/verdict.json`
- Drafts retained: `runs/s4-thin/drafts/multi-agent-reliability/{index.md, chapters/measured-failure-rates.md}`
- Untouched: `runs/s4-thin/library/best-context/` (scope-fit: no description stretch, no edits)

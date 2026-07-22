# Run report — s4-thin

**Ask (verbatim):** "Write a chapter with measured production failure-rate benchmarks for multi-agent LLM systems"
**Trigger:** direct request (no prior search).
**Terminal state:** **enriched** — with one honest scope caveat: the "production" component of the ask is not satisfiable from the public record; the chapter states that absence explicitly (marked derived + uncertain) rather than laundering benchmark numbers into production claims. Everything that shipped passed verification; nothing is padded.

## Stage 0 — Brief check

Brief contained the ask, search status (direct request), and the gap. Complete; no user round-trip needed.

## Stage 1 — DIAGNOSE (orchestrator, no subagent)

Read the only book's index frontmatter (`library/best-context/index.md`) and all 19 chapter frontmatters.

- `isolation-and-strict-briefs.md` covers multi-agent delegation qualitatively; `four-failure-modes.md` is a qualitative failure taxonomy; `why-context-rots.md` holds measured numbers but for long context, not multi-agent systems.
- No chapter holds measured multi-agent failure-rate data.

**Decision: PARTIAL** — the book covers the area (agent/context failure); the specific piece (measured multi-agent failure rates) is missing. Target = one new chapter in `best-context`. (Not ABSENT — a new book would overlap `best-context`'s scope; not EXISTS — no findability fix could surface data the library doesn't hold.)

## Stage 2 — RESEARCH (researcher subagent, agentId a80b102e5ceff2f41)

**Rounds: 1 of 3.** Round 1 returned 13 findings (12 sourced, 1 derived) plus a decisive STILL MISSING: **no publicly measured per-run production failure/incident rates for multi-agent LLM systems exist as of July 2026** — everything quantified is benchmark-harness measurement, call-level telemetry not attributable to multi-agent architecture, self-report surveys without denominators, or internal capability evals with no incident rates.

**Why research stopped after round 1:** the STILL MISSING is an absence in the public record, not a deficiency of search effort — the researcher swept benchmark papers, vendor telemetry reports, postmortem literature, and reliability surveys. Additional rounds cannot produce data that does not exist. The 13 findings were judged sufficient for one chapter.

**Scope decision:** the ask's exact object ("production failure-rate benchmarks") cannot be delivered as asked. Rather than degrade to a stub, the evidence supports a full chapter whose subject is what IS measured (benchmark rates) plus the explicitly-marked production gap and the laundering hazard around it — the absence itself is high-value non-inferable knowledge.

### Data sources used (all via the researcher, primary-verified where noted)

1. Cemri, Pan, Yang et al., "Why Do Multi-Agent LLM Systems Fail?" (MAST), arXiv 2503.13657 v3, NeurIPS 2025 D&B — verified against the PDF (per-framework rates 41–86.7%, category splits, per-mode prevalences, kappa methodology, interventions)
2. Anthropic engineering blog, "How we built our multi-agent research system" (June 2025) — 90.2% improvement, ~15x tokens, variance decomposition
3. Cognition, "Don't Build Multi-Agents" (2025) — verified to contain zero measured numbers
4. Smit et al., "Should we be going MAD?", arXiv 2311.17371 / PMLR v235 (ICML 2024)
5. "Stop Overvaluing Multi-Agent Debate", arXiv 2502.08788 (2025)
6. Datadog, State of AI Engineering (2026) — call-level telemetry proxy
7. Pan et al., "Measuring Agents in Production", arXiv 2512.04123 (UC Berkeley, Dec 2025) — production-practice study, no failure rates
8. SailPoint / Dimensional Research, "AI agents: The new attack surface" (May 2025) — self-report survey proxy
9. MIT NANDA 2025 / McKinsey 2025 / Gartner pilot figures — cited only as provenance of laundered "production failure rate" claims
10. Augment Code blog — cited only as a laundering example (splices MAST's benchmark range onto "production")

## Stage 3 — AUTHOR (book-author subagent, agentId ad06b58012dd94596)

- **Round 1:** wrote `drafts/best-context/chapters/multi-agent-failure-rates.md`. Self-audit returned a gap map (intentional omissions to avoid padding: Manus 60%, Datadog adoption YoY, Berkeley serve-humans figure; one borderline compact derivation; index update deferred to promotion).
- **Round 2 (after verify round 1):** fixed the two verifier FLAGs — the 7-vs-6 framework-count inconsistency (now "the 6 shown here span 41% to 86.7%") and the bare superlative "most-cited" (now "a widely circulated skeptical piece").

## Stage 4 — VERIFY (fresh book-verifier spawns, never the author)

- **Round 1 (agentId a312a0ea75eb8e154): CORRECTION_NEEDED.** Two FLAGs, both claims-discipline: (1) line 9 attributed the 41–86.7% range to "7" frameworks while the table sources only 6; (2) line 26's unsourced superlative "most-cited". All other checklist items CHECK.
- **Round 2 (agentId ae044a8af19c735b9, fresh spawn): APPROVED.** All 7 checklist items CHECK; every number spot-checked against the findings; the required production-absence statement verified as present, bolded, correctly marked, and restated at close.

Author-verify rounds used: 2 of 3.

## Stage 5 — PROMOTE (orchestrator, on APPROVED only)

1. Copied the approved draft into the library.
2. Wrote the audit trace `drafts/best-context/verdict.json` (verdict, sha256, checklist, rounds, timestamp).
3. Findability: updated the book `index.md` — description extended to cover the new chapter (with its trigger), labels +5 (multi-agent, failure rates, MAST, benchmarks, production reliability), sources +10.
4. Mechanical re-check: **caught a real defect** — the index edit initially broke YAML (unquoted `? ` in two source titles, "...Fail? / MAST" and "...MAD? (...)", parsed as complex-key indicators in a flow sequence). Quoted both entries; re-check then passed: chapter frontmatter parses with name/description/labels; index parses with name/description/labels(14)/sources(20).

## Files created or modified

| Path | Action |
|---|---|
| `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s4-thin/drafts/best-context/chapters/multi-agent-failure-rates.md` | created (author r1), edited (author r2) — the staged draft |
| `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s4-thin/library/best-context/chapters/multi-agent-failure-rates.md` | created at PROMOTE (sha256 996485f6d97013c8705ba96c3a9f946a8b25ef51bf3180d67b2509c82ae32397) |
| `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s4-thin/drafts/best-context/verdict.json` | created at PROMOTE — audit trace |
| `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s4-thin/library/best-context/index.md` | edited at PROMOTE — description/labels/sources extended; two source entries quoted to fix YAML |
| `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s4-thin/report.md` | this report |

No real `library/` path outside the sandbox was touched. No file entered the sandbox library without the APPROVED verdict.

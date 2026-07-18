# Index

**Book 6 — Evals.** The library's instruments for measuring its own claims. The design principle that defines this book: **the domain book owns the bar; this book owns the instrument.** Every eval here imports its pass criteria from the book that owns the concept — the way our gate executes Book 2's `gate_criteria` without owning them. This book touches every sibling and owns none of their content: pure instruments plus imports.

Two axes organize an eval (Part I): **what you measure** (dimension) × **how you measure** (mechanism). A third distinction — artifact vs adherence vs coverage evals — cuts across both. Part II turns three mechanisms into fail-closed recipes.

## Part I — Principles (what an eval is)

| # | Page | One-liner |
|---|---|---|
| 1 | `the-eval-matrix.md` | Every eval is a dimension (what you measure) × a mechanism (how); the pass bar is imported from the owning book, never invented here. |
| 2 | `every-rule-is-an-eval.md` | A rule without an eval is a wish; Book 2's rules frontmatter is a machine-readable eval spec, and the coverage matrix tracks which prescriptions have a live instrument. |
| 3 | `judge-calibration.md` | LLM judges reach human-level agreement but carry four measured biases; fix with order-swaps, reference answers, a different-model judge, and execution grounding. |
| 4 | `trajectory-and-reliability.md` | The answer is not enough — grade the path at discrete checkpoints (not a canonical route) and run k times, because single-run pass rates overstate reliability ~⅓. |
| 5 | `evals-decay.md` | Benchmarks are living sources too — leakage and contamination inflate scores several-fold, so any number printed from a benchmark inherits its validity risk. |
| 6 | `verify-at-the-authoritative-surface.md` | A verification is only as trustworthy as the surface it runs on; static and proxy checks are necessary but not sufficient, and a green proxy over a red authority is false green — choose the surface first, then trust the tool. |

## Part II — Recipes (how to run one)

| # | Page | One-liner |
|---|---|---|
| 7 | `calibrate-a-judge.md` | Validate a judge by planting known violations in known-good artifacts and scoring catch-rate vs false-alarm rate — a judge that passes everything is uncalibrated. |
| 8 | `run-a-baseline-delta.md` | Measure an artifact's value as the with-vs-without delta on a task where it should matter — blind judge, external rubric, execution-grounded; expect in-distribution nulls. |
| 9 | `instrument-adherence.md` | Turn a process rule into a measured compliance rate from telemetry, separating real violations from telemetry gaps. |

## One-home discipline

This book is instruments plus imports; it deliberately homes nothing a sibling already owns:
- **Trigger-rate and skill output evals** → Book 4: `writing-the-description`, `evaluating-a-skill`.
- **Ablation** → Book 5: `gates-and-ablation`.
- **Panel agreement** → Book 5: `persona-panels`.
- **Fail-closed gate principle** → Book 1: `hook-vs-router`.
- **Living sources / decay principle** → Book 1: `living-sources`.
- **Execution grounding** is a *lever/prerequisite* homed in `judge-calibration` (judge bias-fix) and `run-a-baseline-delta` (recipe step); `verify-at-the-authoritative-surface` owns the general principle those two are instances of.

## Sources

- `docs/evals-notes.md` — verified research notes (judge biases, LLM4VV negative probing, self-preference causality, τ-bench pass^k, process-vs-outcome, SWE-Bench+, GSM1k). Items marked UNVERIFIED there are not cited.
- `docs/book-4-consumption-eval-2026-07-08.md` — this repo's own baseline-delta eval report (the sign-flip; the found tool bug); the worked example on the baseline-delta pages.
- `docs/talk-outline.md` §F — the four eval types and the scored roadmap.
- In-repo live evidence: Book 2's `rules:` frontmatter (machine-readable eval specs) and `bk`'s dormant `REGISTRY_ENFORCED` flag; `.bk/reads/<session>.jsonl` adherence telemetry; the gate smoke test (git 7ab2826); the A5 constitution spike (git a8fc53c).
- `verify-at-the-authoritative-surface` case study: the Lynk semantic-layer audit incident (internal) — a compile-surface circular dependency invisible to static and raw-warehouse checks.

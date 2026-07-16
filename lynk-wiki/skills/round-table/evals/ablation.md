# Ablation — does the panel earn its ~15×, does grounding earn its pass?

A rule without an eval is a wish; a stage without an ablation is ceremony. This
protocol produces the deltas that justify (or kill) the roundtable's stages.
(History: a recap round existed in v2 and was removed by owner decision on
2026-07-16 for cost; if quality regressions show up here, that's the first
stage to consider restoring.)

## Protocol

For each benchmark request, run three configurations, k≥3 each:

- **(a) direct** — answer in the main window, no skill.
- **(b) panel, no grounding** — round-table → adjudicate phase A → fold, skipping
  the grounding and conservation passes.
- **(c) full flow** — round-table → adjudicate (synthesis + grounding + conservation
  + fold).

Score each output blind (grader doesn't know the configuration) on a fixed
checklist:

1. Distinct real risks identified (count).
2. Disagreement/tension surfaced and attributed (yes/no + count).
3. Plan specificity: steps executable without re-deriving decisions (1–5).
4. Wrongness caught: seeded-flaw benchmarks only — did the output catch the
   planted problem (yes/no).

Also record tokens per configuration — the delta must be read against its cost.

## Benchmark requests

Use breadth-heavy decisions where multiple axes genuinely conflict (routing cases
r-01, r-12, r-14, r-20 are good seeds), plus at least one **seeded-tension case**:
a decision where a specific objection SHOULD change the plan (e.g. a migration
plan whose rollback is impossible — the operator/skeptic must catch it in recap).

## Pass bars

- **Panel earns its cost:** (b) beats (a) on checks 1–2 on breadth-heavy cases.
  Expect in-distribution nulls — on requests the base model handles well, (b) ≈ (a)
  is normal and not a failure; the panel must win where breadth matters.
- **Grounding earns its pass:** on seeded-flaw cases (a planted wrong citation
  that decides an adjudication), (c) catches the flaw and (b) ships it. If (b)
  never ships a flaw across the suite, grounding may be trimmed to high-stakes
  runs only — measure before deciding.

## Reporting

One table per run: request × configuration × checklist scores × tokens. Keep runs
in this directory as dated files (ablation-YYYY-MM-DD.md) so deltas are comparable
release over release.

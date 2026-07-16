---
type: recipe
description: Prove the audit gate itself is trustworthy — seed real past defects into clean files, run blind, score catch-rate vs false-alarm, and measure the with/without delta on a non-inferable case before trusting a verdict.
---

# Calibrate the audit gate

**What it is** — the check on the checker. The audit's Phase 5 gate ([audit-a-layer](audit-a-layer.md)) is itself a judge, and a judge is not trustworthy until it has caught faults planted on purpose. This is the domain application of Book 6's calibration to the semantic-layer gate; the general method is not restated here (source: `.claude/skills/semantic-layer-audit/SKILL.md`, "Measuring the gate") → See the Evals book · `calibrate-a-judge` and the Evals book · `run-a-baseline-delta`.

**Prerequisites**
- **Real past defects** to seed — drawn from recorded audit history (the skill points to `evals/evals.json`), not invented cartoon violations.
- Clean `.lynk/` files known to pass, to seed the defects into.
- A reachable read-only warehouse — the gate's grounding blockers cannot be exercised without it, so an ungrounded calibration measures the wrong instrument.
- The ability to run **k ≥ 3** trials (single runs overstate reliability — source: SKILL.md, "Measuring the gate").
- A **non-inferable** case for the ablation arm — a defect the gate should catch that a plain read would miss (the delta is near-zero on faults anyone would spot → See the Evals book · `run-a-baseline-delta`).

**Steps** (one observable outcome each)
1. **Seed known defects into clean files** — one defect per copy, each traced to a real past defect. → *Outcome:* a shuffled batch the gate cannot tell seeded from clean.
2. **Run the gate blind** over the batch, k ≥ 3 times. → *Outcome:* a verdict per artifact per trial.
3. **Score against the ledger** — catch-rate (seeded defects flagged) and false-alarm rate (clean files wrongly rejected). → *Outcome:* two rates.
4. **Compute the with/without ablation delta on the non-inferable case** — run the pipeline with the gate/grounder and without it, and take the difference. → *Outcome:* a delta showing what the gate adds.

**Verification**
- Catch-rate and false-alarm rate are both computed against the ledger and meet the floor: **catch-rate ≥ 90% on the seeded real defects, false-alarm ≤ 10% on the clean controls** — our calibration floor (opinion, ours: neither `.claude/skills/semantic-layer-audit/references/gate-rules.md` nor the Evals book · `calibrate-a-judge` states a number, so we set one — a fail-closed gate must re-catch essentially every real defect it has seen while rarely bouncing a clean file; 90/10 tracks the top of the grounded-judge range in the Evals book · `calibrate-a-judge`, LLM4VV 80.53–92.57%, arXiv 2408.11729 v2). A gate that passes every seeded defect is uncalibrated by definition (source: the Evals book · `calibrate-a-judge`).
- The ablation delta is positive on the non-inferable case. This matters because a badly-built grounder can be **worse than no gate** — false confidence is worse than acknowledged ignorance — so the delta, not the mere presence of a gate, is the proof of value (source: SKILL.md, "Measuring the gate").

**Failure modes** (symptom → fix/escape)
- **Seeded defects too obvious** — symptom: 100% catch, no discrimination; fix: seed from real past defects (`evals.json`), not exaggerated ones (source: the Evals book · `calibrate-a-judge`).
- **Ungrounded judge** — symptom: the gate is calibrated with no warehouse, so its grounding blockers (`findings-proven`, `anchor-external`) never fire and false passes go unmeasured; fix: calibrate with the read-only warehouse connected (source: SKILL.md guardrails; general basis in the Evals book · `calibrate-a-judge`).
- **Single-run overconfidence** — symptom: a "clean" verdict from one trial; fix: run k ≥ 3 and treat verdicts that flip across trials as unreliable (source: SKILL.md, "Measuring the gate").

**Takeaway** — **trust the audit gate only after it clears the stated floor (our target: catch-rate ≥ 90%, false-alarm ≤ 10%) on seeded real defects and its with/without delta proves it beats no gate — an ungrounded or single-run calibration measures nothing.**

**Example** *(real)* — the library's own gate smoke test is this recipe run once against Book 2 drafts: 2 planted violations, 2/2 caught, plus 1 real bonus defect it was not told about (source: `../book-6-evals/calibrate-a-judge.md`, citing git `7ab2826`). The semantic-layer gate is calibrated the same way, with the warehouse connected so its grounding blockers are exercised.

**In this system** — this page owns only the *audit-domain* wiring (real `.lynk/` defects, warehouse-grounded blockers); the general instrument and its biases live in Book 6, and this recipe points there rather than copying it. → See [audit-a-layer](audit-a-layer.md) for the gate being calibrated, and [the frame](the-frame.md) for why an ungrounded gate is blind to truth.

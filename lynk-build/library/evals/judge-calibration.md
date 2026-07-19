---
type: principle
description: LLM judges reach human-level agreement but carry four measured biases; calibrate with order-swaps, reference answers, a different-model judge, and execution grounding before trusting a verdict.
---

# Judge calibration

**What it is** — the precondition for using an LLM as a judge: it works, but only after you measure and correct its biases. Strong judges reach human-level agreement — GPT-4 vs humans **85%** on MT-Bench non-tie pairs, where humans agree with each other **81%** (Chatbot Arena non-tie: **87%**) (source: arXiv 2306.05685 v4, Zheng et al.). An uncalibrated judge, though, systematically prefers the wrong things.

**Mechanics** — the four measured biases and their fixes:

| Bias | Measured | Fix |
|---|---|---|
| **Position** | Consistency across answer order: GPT-4 **65.0%**, GPT-3.5 **46.2%**, Claude-v1 **23.8%** (source: 2306.05685 Table 2) | Swap order, re-judge; a win counts only if it survives both orders, else tie |
| **Verbosity** | Prefers the artificially-longer answer: weak judges fail **91.3%** (Claude-v1, GPT-3.5) vs GPT-4 **8.7%** (Table 3) | Control length; discount padding |
| **Self-enhancement** | Judge over-rates its own family ~**10%** (GPT-4) to ~**25%** (Claude-v1) above human raters (source: 2306.05685 §3.3) | Different-model judge (below) |
| **Reasoning-grading** | Default judging fails ~**70%** of math probes; **reference-guided** cuts it to **15%** (source: 2306.05685) | Hand the judge a solved reference first |

Two deeper mitigations. **Different-model judge** rests on a causal result: self-preference strength correlates linearly with a model's self-recognition ability, with control fine-tunes ruling out confounds — the preference is the judge's, not the text's (source: arXiv 2404.13076, Panickssery et al.). **Execution grounding** is the strongest lever where the domain is checkable: a judge scoring from code alone hit **56.63%** accuracy (OpenACC), but grounded in compile/run results **80.53%–92.57%** — more than doubling reliability (source: LLM4VV, arXiv 2408.11729 v2).

**Seeded errors / negative probing** — plant known faults and check the judge catches them — is the calibration recipe ([calibrate-a-judge](calibrate-a-judge.md)). Honest sourcing note: this practice is practitioner **folklore with no canonical primary source** naming it; LLM4VV (which injects five error types into compiler-test files) is the closest primary we found (source: `docs/evals-notes.md`, verified 2026-07-08).

**Takeaway** — **an LLM judge is trustworthy only after you swap order, supply a reference, use a different model, and ground it in execution — an uncalibrated judge measures its own biases, not the artifact.**

**Example** *(real)* — our gate is a calibrated judge by design: a forced verdict schema, mechanical checks, and criteria imported externally from Book 2 (not self-authored). Its seeded-violation smoke test (git 7ab2826) is negative probing; and the consumption eval's round-2 judge, required to verify claims against the live `bk` CLI, separated an 8/8-verified skill from a 6/8 one — a gap **invisible to the static round-1 judge**, which could only reach "marginal" (source: `docs/book-4-consumption-eval-2026-07-08.md`).

**In this system** — the gate is the library's production judge, so its calibration is load-bearing; this page is where its biases and fixes are named. → See [calibrate-a-judge](calibrate-a-judge.md) for the recipe, and the Subagents book · `persona-panels` for using disagreement instead of one judge. Related — [verify-at-the-authoritative-surface](verify-at-the-authoritative-surface.md): execution grounding is a *judge lever* here; the general principle "verify at the authoritative surface" is owned by that page.

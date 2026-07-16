---
type: principle
description: Benchmarks are living sources too — leakage and contamination inflate scores several-fold over time, so any number printed from a benchmark inherits that benchmark's validity risk.
---

# Evals decay

**What it is** — the reminder that an eval is itself a source, and sources go stale (the Best Context book · `living-sources`). Benchmarks rot two ways: **solution leakage** (the answer is reachable from the input) and **contamination** (the test set leaked into training). Both inflate scores, and the inflation grows as a benchmark ages into the training data.

**Mechanics** — the two measured cases:

| Failure | Evidence |
|---|---|
| **Leakage / weak tests** | SWE-Bench+: **32.67%** of successful patches had solution leakage (fix visible in the issue/comments), **31.08%** passed on weak tests; after filtering, SWE-Agent+GPT-4 resolution fell **12.47% → 3.97%** — ~3× inflation — and over 94% of issues predate model cutoffs (source: arXiv 2410.06992). |
| **Contamination** | GSM1k, a from-scratch GSM8k-equivalent: scores drop **up to 8%**, with a contamination signal of Spearman **r² = 0.36** between a model's probability of generating GSM8k examples and its performance gap. Nuance: frontier models show minimal overfitting and do generalize to guaranteed-novel problems (source: arXiv 2405.00332, Scale AI). |

The consequence for this library: **any number we print from a benchmark inherits that benchmark's validity risk.** This is where that caveat lives. Concretely — the Subagents book · `gates-and-ablation` cites SWE-agent's SWE-bench numbers (12.47% / 18.00%) faithfully; SWE-Bench+ later showed the underlying benchmark inflates resolution ~3×. That page's *ablation deltas* are likely unaffected (both arms ran on the same benchmark, so inflation should cancel — our call, with a stated gap: SWE-Bench+ measured inflation on *full* SWE-bench while the ablation ran on SWE-bench *Lite*, and Lite's leakage rate and its symmetry across arms are unverified), but the absolute resolution figures carry the risk (source: `docs/evals-notes.md`, flagged implication).

**Takeaway** — **a benchmark is a living source that inflates as it ages into training data — cite the number and the benchmark's validity risk together, or you are quoting a decayed source as fact.**

**Example** *(real)* — SWE-Bench+ (arXiv 2410.06992): the same SWE-Agent+GPT-4 configuration reads 12.47% on the original benchmark and 3.97% after leakage and weak tests are filtered out. Nothing about the agent changed between those two numbers — only the benchmark's validity did.

**In this system** — this page is the validity backstop for every external number the library quotes; Book 5's benchmark citations should point here rather than be silently trusted (this page links there today; the reciprocal pointer is a pending Book 5 amendment). → See the Best Context book · `living-sources` for the principle, and the Subagents book · `gates-and-ablation` for the shipped benchmark citation this caveat guards.

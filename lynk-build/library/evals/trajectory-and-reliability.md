---
type: principle
description: The final answer is not enough — grade the path at discrete checkpoints (not a canonical route) and run the eval k times, because single-run pass rates overstate reliability by about a third.
---

# Trajectory and reliability

**What it is** — one concept with two faces: **the outcome is not enough.** A right answer reached by a wrong path, or reached only one run in three, is not a passing agent. So evals must also look at *how* the answer was reached (trajectory) and *how often* it is reached (reliability).

**Mechanics**

*Trajectory — but do not grade against a canonical path.* Anthropic's caution: "agents might take completely different valid paths"; instead of judging whether a specific process was followed, evaluate the correct **final state**, and for complex workflows "break evaluation into discrete **checkpoints** where specific state changes should have occurred" (source: anthropic.com/engineering/built-multi-agent-research-system). Process supervision still pays where the steps are the product: a process-supervised reward model scored **78.2%** on MATH best-of-N vs **72.4%** outcome-supervised vs **69.6%** majority voting (source: arXiv 2305.20050, Lightman et al.). And humans reading traces catch what judges miss — Anthropic's testers found agents "consistently choosing SEO-optimized content farms over authoritative but less highly-ranked sources," invisible in the final answer (source: same).

*Reliability — measure pass^k, not pass^1.* τ-bench proposes pass^k: the same task run over k i.i.d. trials. The best retail agent decays **0.692 → 0.576 → 0.509 → 0.462** across Pass^1→Pass^4; the abstract reports pass^8 **<25%** in retail, and SOTA agents succeed on "<50% of the tasks" (source: arXiv 2406.12045, Yao et al.; leaderboard github.com/sierra-research/tau-bench). The lesson: single-run pass rates overstate reliability by roughly a third at k=4.

Honest self-application: our own gate PASS is **single-run** — one verdict per draft, no pass^k. We say so plainly; a gate that passes a draft once has not shown it would pass it every time.

**Takeaway** — **grade the end state and discrete checkpoints (never a fixed route), and run every eval k times — a single-run pass rate is an optimistic story, not a reliability measurement.**

**Example** *(real)* — the process-supervision numbers above (78.2 / 72.4 / 69.6, arXiv 2305.20050) are the anchor; τ-bench's 0.692→0.462 decay (2406.12045) is the reliability half. Our gate's single-run verdict is the honest counter-example in our own house: it is the *fail-closed gate* eval type, not a pass^k reliability eval.

**In this system** — the writer/gate pipeline produces trajectories worth grading, and duplicated work is exactly the trajectory failure this page warns about. → See the Subagents book · `the-strict-brief` for the duplicate-work failure a trajectory eval catches, and [judge-calibration](judge-calibration.md) for the judge that reads those traces.

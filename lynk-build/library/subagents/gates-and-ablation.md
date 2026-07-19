---
type: principle
description: Fixed roles publish structured artifacts checked at every handoff, and discrete stages let you ablate one piece to measure its worth — a delta, not an opinion.
---

# Gates and ablation

**What it is** — two properties you get when agents publish *structured artifacts* to each other instead of chatting. A **gate** checks each artifact at every handoff (a typed output you can verify). **Ablation** exploits the discrete stages: run the pipeline minus one piece and the quality delta is a number, not an opinion.

**Mechanics** — where each property comes from (each claim sourced):

| Property | Evidence |
|---|---|
| Structured artifacts | MetaGPT encodes SOPs into prompt sequences and has agents "verify intermediate results," using a shared publish-subscribe document pool instead of dialogue — its stated enemy is "cascading hallucinations" from naive chaining (source: arXiv 2308.00352). |
| Role ablation | ChatDev: removing agent roles from the prompts drops Quality from **0.3953** to **0.2212** — its largest single ablation drop (source: arXiv 2307.07924 v5). |
| Interface ablation | SWE-agent: the Agent-Computer Interface vs a bare Linux shell is **18.00% → 11.00%** on SWE-bench Lite, framed by the paper as a **"64% relative increase"** from the interface (source: arXiv 2405.15793 v3, Table 1/3). |

Honesty note: each paper wins on *its own* benchmark — ChatDev's v5 eval reverses MetaGPT's claimed win — so read these as author-owned benchmarks, not a settled ranking (source: `docs/subagents-notes.md`, corrections).

SWE-agent's component table carries the sharpest lessons (source: arXiv 2405.15793 v3, Lite, default 18.0): removing the edit command drops to **10.3**; an iterative search tool scores **12.0** — *worse* than having no search tools at all (15.7), so a badly designed tool is worse than none; full history scores **15.0** vs last-5-observations at **18.0**. The lesson: when an agent keeps failing, suspect its *tool interface* before its model or prompt.

**Takeaway** — **gate every artifact at the handoff and ablate every stage — if you can't run the pipeline minus one piece and read the delta, you can't justify keeping any piece.**

**Example** — real: our gate. It runs a forced verdict schema at every handoff — across two books on 2026-07-07 it ran six call/return rounds and caught three genuine defects (a one-home clash, a missing changelog entry, and a line-count drift), and it refused relayed user approval, insisting on its own check. That is a validation gate on a structured artifact, in production.

**In this system** — the gate *is* this page running live: every draft is a structured artifact checked before it can become truth, and the writer/gate split exists so each stage can be judged on its own. → See the Best Context book · `hook-vs-router` for why the gate is a router (fail-closed) not a hook, [orchestrator-workers](orchestrator-workers.md) for the stages the gate sits between, and the Evals book · `evals-decay` for why the SWE-agent benchmark numbers above carry a validity caveat.

---
type: principle
description: Several agents answer independently then see each other's answers; agreement is cheap confidence and disagreement flags a human decision — but the diversity must be engineered.
---

# Persona panels

**What it is** — a panel of agents that answer a question independently, then read each other's answers and revise. Agreement across the panel is cheap confidence; disagreement is precisely where a human decision belongs. But the panel only helps if its members actually differ — same model, same prompt, cloned three times just clones the blind spots.

**Mechanics** — the evidence, and the knobs (each claim sourced):

| Finding | Source |
|---|---|
| Debate lifts accuracy: Arithmetic 67.0→**81.8**, GSM8K 77.0→**85.0**, MMLU 63.9→**71.1** (3 agents, 2 rounds, answer independently then revise). | Du et al., arXiv 2305.14325 |
| Reflection *alone* HURTS factuality: MMLU 57.7 vs 63.9 single-agent — seeing others beats self-review. | arXiv 2305.14325 |
| Gains plateau after ~4 rounds; "stubborn" prompts beat "agreeable" ones; debate can reach a correct answer **even when all agents start wrong** (not just vote amplification). | arXiv 2305.14325 |
| Mixture-of-Agents: layered, each agent sees all previous-layer outputs; open-source-only ensemble scores **65.1%** AlpacaEval 2.0 vs GPT-4 Omni **57.5%**. | arXiv 2406.04692 |
| Sampling-and-voting: performance scales with agent count, and the gain correlates with task difficulty. | arXiv 2402.05120 v2 (abstract-verified) |

The three diversity knobs (source: `docs/talk-outline.md` §D): **model** (different models — expensive), **lens** (same model, different job or role), **evidence** (same model, different context slices). Without at least one, the panel is one opinion repeated.

**Takeaway** — **engineer the disagreement by varying model, lens, or evidence — agreement is cheap confidence, but disagreement is a ticket for a human.**

**Example** — Du et al.'s numbers above are the real anchor (arXiv 2305.14325). The talk sketches a constructed build on top (labeled — the talk's design, not a shipped system): personas as files, a CEO subagent that picks relevant personas and runs them parallel and isolated, round-one draft plans merged, round-two the same personas score every step, and the main window receives exactly one thing — the final curated plan (source: `docs/talk-outline.md` §D).

**In this system** — the writer-vs-gate split is a two-member panel with engineered lenses: the writer proposes, the gate judges against a different job (Book 2's checklists), and when they disagree the human decides — the disagreement is the signal, not a failure. → See [gates-and-ablation](gates-and-ablation.md) for the gate as an independent checker, and [orchestrator-workers](orchestrator-workers.md) for the other multi-agent shape (fan-out for breadth, panels for judgment).

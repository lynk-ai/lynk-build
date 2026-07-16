---
type: principle
description: The quality bar for a skill — grounded in real expertise not general knowledge, admission-tested per instruction, moderately detailed, function-scoped, control calibrated to fragility, and running the six reusable patterns.
---

# What makes a skill good

**What it is** — the line between a skill that lifts an agent's work and one that adds tokens without value. The spec's authoring canon names the bar; this page collects it (source throughout: `docs/skills-spec-notes.md`, "Authoring depth / best-practices").

**Mechanics** — six quality rules, each spec-sourced:

| Rule | What it means |
|---|---|
| **Ground in real expertise** | The #1 pitfall the spec names: asking an LLM to generate a skill from general training knowledge yields "vague, generic procedures ('handle errors appropriately')". Effective skills extract from a hands-on task (steps that worked, corrections made) or synthesize from project artifacts — runbooks, incident reports, review comments, VCS history, real failure cases. |
| **Admission-test every line** | The spec's verbatim test: **"Would the agent get this wrong without this instruction? If no, cut it."** |
| **Moderate detail, not exhaustive** | Over-comprehensive skills hurt — the agent "pursues unproductive paths triggered by instructions that don't apply." |
| **Scope like a function** | Coherent units: too narrow → multiple skills load and conflict; too broad → hard to activate precisely. |
| **Calibrate control to fragility** | Freedom + explain-why for flexible tasks; exact prescriptive sequences for fragile ones. **Defaults, not menus** (one tool, alternatives as escape hatches); **procedures over declarations** (teach a class of problems, not one answer). |
| **Run the reusable patterns** | Gotchas sections ("the highest-value content in many skills"), output templates, checklists, validation loops, plan-validate-execute, bundled scripts. |

The admission test is independently the Book Standard · `non-inferable-only` rule — the spec notes flag this convergence explicitly, so the two rules validate each other rather than one citing the other (source: `docs/skills-spec-notes.md`: "= our non-inferable-only rule, independently stated by the spec").

**Takeaway** — **a good skill is grounded in real, corrected experience and holds only what the agent would get wrong without it — everything else is weight that pushes the agent down unproductive paths.**

**Example** — the two live exemplars, dissected (real). CandleKeep's `reference/skills/SKILL.md` (538 lines) runs the **gotchas pattern** hard: its "Common Mistakes to Avoid" section, the never-mislabel-a-thread-cap-as-a-quota guardrail, and the idempotency notes ("re-running is safe… reports `already exists`") are environment facts that defy assumptions — exactly the highest-value content the spec describes. It also **breaches the budget** at 538 lines (> the spec's under-500 recommendation) — an honest tension: a production skill that grew past its budget. The spec's remedy is to move overflow into `references/` **with explicit load triggers** ("Read references/api-errors.md if the API returns non-200" beats "see references/"). Our `.claude/skills/library/SKILL.md` (96 lines) shows the lean opposite — the same pipeline shape at one-sixth the size. *(superseded 2026-07-14: previously "83 lines" — SKILL.md grew to 96 in the pipeline restructure; see log.md)*

**In this system** — this is the quality bar the [building-a-skill](building-a-skill.md) recipe builds toward and the [evaluating-a-skill](evaluating-a-skill.md) recipe measures. Honest gap: neither in-repo exemplar bundles `scripts/`, `references/`, or `assets/`, so the "move overflow to references/ with explicit triggers" remedy is **spec-sourced, not exemplar-dissected** — we can show CK breaching the budget but not the fix applied. → See [what-a-skill-is](what-a-skill-is.md) for the format, and the Book Standard · `non-inferable-only` for the admission test's home in our standard.

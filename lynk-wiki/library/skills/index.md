# Index

**Book 4 — Agent Skills.** What an Agent Skill is, what separates a good one from a mediocre one, and how to build, trigger-tune, and evaluate one end-to-end. Part I is reference/principle (the format and the quality bar); Part II is how-to recipes. This book *uses* Book 3's progressive-disclosure mechanics — it points there for the *why* of the disclosure budgets and never restates them.

**Page shape:** Part I follows the concept template (the Book Standard · `page-template`): *What it is → Mechanics → Takeaway → Example → In this system.*

## Part I — Reference

| Page | One-liner |
|---|---|
| `what-a-skill-is.md` | The format precisely: a directory with SKILL.md (frontmatter + body), optional scripts/references/assets, the frontmatter field table, and the three disclosure budgets. |
| `what-makes-a-skill-good.md` | The quality bar: grounded in real expertise, admission-tested per line, moderate detail, function-scoped, control calibrated to fragility, and the six reusable patterns. |
| `skill-vs-subagent-vs-hook.md` | When to use which — the portability ladder (skills port everything; hooks port only event names) and what each mechanism is for. |

## Part II — How-to recipes

Part II pages are `type: recipe` and are gate-checked against the Book Standard · `the-recipe-shape`: each carries all four sections — Prerequisites, Steps, Verification, Failure modes — or it doesn't ship.

| Page | One-liner |
|---|---|
| `building-a-skill.md` | Build a validated skill directory end-to-end — from a real, corrected task through frontmatter, a budgeted body, reference overflow, and validation. |
| `writing-the-description.md` | Trigger-tune the description with ~20 labeled queries and a train/validation split — the field that carries the entire burden of activation. |
| `evaluating-a-skill.md` | Measure whether the skill improves the work — run cases with and without it, grade verifiable assertions on evidence, keep it only if the delta is worth its cost. |

## Sources

- `docs/skills-spec-notes.md` — PRIMARY: the official Agent Skills spec + authoring canon (format, frontmatter, disclosure budgets; best-practices / optimizing-descriptions / evaluating-skills). Fetched from agentskills.io 2026-07-07.
- `docs/talk-outline.md` §E — the portability ladder and the four rules of the road.
- `docs/research-brief-2026-07.md` — the adoption gradient (~40 clients within ~90 days of the Dec 18 2025 spec opening; ~500K marketplace skills).
- Live exemplars, dissected: `reference/skills/SKILL.md` (CandleKeep's production skill, 538 lines — breaches the <500-line budget) and `.claude/skills/library/SKILL.md` (our own, 96 lines — lean). *(superseded 2026-07-14: previously "83 lines" — SKILL.md grew in the pipeline restructure; see log.md)*

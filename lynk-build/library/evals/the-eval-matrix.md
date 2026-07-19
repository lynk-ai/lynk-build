---
type: principle
description: Every eval is a choice of what you measure (dimension) times how you measure it (mechanism); the pass bar is imported from the book that owns the concept, never invented here.
---

# The eval matrix

**What it is** — the two-axis map for designing any eval, plus the split that defines this whole book. An eval is one cell of a grid: a **dimension** (*what* you measure) crossed with a **mechanism** (*how* you measure it). Above that grid sits one rule of ownership — **the domain book owns the bar; this book owns the instrument.** An eval imports its pass criteria from the book that owns the concept the way our gate executes Book 2's `gate_criteria` without owning them (our call: this is the book's identity — it touches every sibling and owns none of their content).

**Mechanics** — pick a cell, then import the bar:

| | Mechanism → | | |
|---|---|---|---|
| **Dimension ↓** | mechanical assertion / labeled set | baseline delta / ablation | LLM-judge / panel / seeded / trajectory / benchmark |
| understanding, factual correctness | known-answer checks | with/without delta | judge with reference (see [judge-calibration](judge-calibration.md)) |
| subjective quality | — | delta | LLM-judge, the Subagents book · `persona-panels` |
| retrieval / routing, end-task success | trigger assertions | ablation (the Subagents book · `gates-and-ablation`) | trajectory/checkpoint |
| efficiency, conformance | mechanical (lint) | delta | fail-closed gate |

The routing flow, in order: **pick the dimension → pick the mechanism → import the bar from the owning book.** Most bad evals are dimension errors, not mechanism errors — a perfectly executed LLM-judge aimed at the wrong dimension (grading style when the failure was factual) measures nothing (our call, generalizing the consumption eval below). The three eval *kinds* — artifact / adherence / coverage — are a separate axis, homed in [every-rule-is-an-eval](every-rule-is-an-eval.md).

**Takeaway** — **choose the dimension first, the mechanism second, and never write the bar — import it from the book that owns the concept.**

**Example** *(real)* — our Book 4 consumption eval as a dimension-then-mechanism walk: dimension = *end-task success* (does an agent build a better skill?); mechanism = *baseline delta* (with-book arm vs without-book arm); bar = imported from the external spec `docs/skills-spec-notes.md`, never from Book 4's own phrasing, so the book arm could not win by construction (source: `docs/book-4-consumption-eval-2026-07-08.md`).

**In this system** — this page is the book's front door: every other page is one cell or one kind of this matrix. Skill-specific trigger and output evals are not homed here — they live in Book 4: → See the Agent Skills book · `writing-the-description` (trigger-rate) and the Agent Skills book · `evaluating-a-skill` (output delta). → See [run-a-baseline-delta](run-a-baseline-delta.md) for the delta mechanism as a recipe.

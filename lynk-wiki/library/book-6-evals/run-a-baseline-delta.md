---
type: recipe
description: Measure an artifact's value as the with-vs-without delta on a task where it should matter — blind judge, external rubric, execution-grounded — and expect in-distribution nulls, so run a non-inferable task too.
---

# Run a baseline delta

**What it is** — the recipe for a consumption eval: the measured value of an artifact (a book, a skill, a doc) is the **delta** between an arm that has it and an arm that doesn't. The skill-specific version is homed in Book 4 (the Agent Skills book · `evaluating-a-skill`); this is the general procedure.

**Prerequisites**
- The artifact under test.
- A task where the artifact *should* matter — **non-inferable** content the model can't already do (the delta is near-zero on tasks the model aces — see the sign-flip in the Example).
- Two isolated arms with **identical access except the artifact** (same model, same tools, blind to each other).
- A blind judge with an **external rubric** — never the artifact's own phrasing, or the test is circular by construction.
- Execution grounding where the domain is checkable (commands the judge must run).

**Steps** (one observable outcome each)
1. **Run both arms in parallel isolation** → two artifacts exist, produced blind to each other.
2. **Judge blind, positions controlled** → one verdict with per-criterion scores, provenance hidden from the judge.
3. **Extract per-criterion deltas** → a table of arm-A-vs-arm-B differences exists.
4. **Classify the result** against the task type → a labeled verdict (win / null / loss) exists.

**Verification**
- The judge's per-criterion evidence table exists (not a bare verdict).
- Provenance never leaked to the judge (check the brief the judge received).
- If round 1 was null, a **second task class** was run — an in-distribution null is expected, not conclusive.

**Failure modes** (symptom → fix/escape)
- **In-distribution ceiling** — symptom: null delta on tasks the model already aces; fix: re-run on a non-inferable domain (our round 1 → round 2).
- **Rubric circularity** — symptom: the book arm is graded by the book's own words, so it can't lose; fix: import the bar from external canon.
- **n=1 overconfidence** — symptom: "clear" verdicts from single runs; fix/escape: run k trials per τ-bench (arXiv 2406.12045), or downgrade the confidence language.

**Takeaway** — **an artifact's value is its with-vs-without delta on a task where it should matter, judged blind against an external rubric — and because the sign flips with task type, one task is never the measurement; the pair is.**

**Example** *(real — the book's centerpiece)* — our Book 4 consumption eval: round 1 (in-distribution conventional-commit skill) gave a **null delta** (no-book arm marginally better — ceiling effect); round 2 (non-inferable `bk` CLI skill) gave a **clear win** for the book arm (8/8 spot-checked CLI claims verified TRUE vs the no-book arm's 6/8 with one FALSE, one misattributed). Execution grounding was decisive — the round-1 static judge could only reach "marginal." The eval also surfaced a real tool bug: `bk index --write` emits frontmatter that violates `structure/reserved-pages-plain` (source: `docs/book-4-consumption-eval-2026-07-08.md`).

**In this system** — this recipe is how the library proves any of its own artifacts earns its cost, and how it caught a shipped tool contradiction. → See [the-eval-matrix](the-eval-matrix.md) for where the delta mechanism sits, and the Subagents book · `gates-and-ablation` for ablation, the same idea applied to pipeline stages. Related — [verify-at-the-authoritative-surface](verify-at-the-authoritative-surface.md): execution grounding is a *recipe prerequisite* here; the general principle lives in `verify-at-the-authoritative-surface`.

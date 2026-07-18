---
type: recipe
description: Measure whether a skill improves the work — run test cases with and without it, grade verifiable assertions on evidence, and keep the skill only if the delta is worth its cost.
---

# Evaluating a skill

**What it is** — the recipe for output-quality evals: proving a skill *improves the work*, not just that it triggers. The measured value of a skill is the **delta** between runs with it and runs without it (source throughout: `docs/skills-spec-notes.md`, "evaluating-skills").

**Prerequisites**
- A triggering skill (from [building-a-skill](building-a-skill.md) and [writing-the-description](writing-the-description.md)).
- **2–3 realistic test cases**, each a prompt (with file paths, typos, real context) + expected output + optional input files, stored in `evals/evals.json`.

**Steps** (one observable outcome each)
1. **Run each case with AND without the skill** → paired transcripts exist; the baseline delta *is* the skill's measured value.
2. **Add assertions after seeing first outputs** → verifiable checks ("valid JSON", "≥3 recommendations"), not vague ("is good") or brittle (exact phrases).
3. **Grade with concrete evidence per PASS** → scripts for mechanical checks, blind comparison for holistic quality; each PASS cites its evidence.
4. **Record `benchmark.json`** → pass_rate / time / tokens per config, plus the delta.
5. **Analyze patterns** → drop always-pass assertions, investigate always-fail, study passes-with/fails-without (that's the skill's value), tighten high-stddev assertions.
6. **Iterate** → feed failed assertions + transcripts + the current SKILL.md back; generalize the lesson (don't patch narrowly); snapshot old versions as baselines.

**Verification**
- `benchmark.json` shows a **positive delta worth its cost** — the spec's bar: "a skill that adds 13s but +50 points is worth it; double tokens for +2 points isn't."

**Failure modes** (symptom → fix/escape)
- **No delta** — symptom: pass-with ≈ pass-without; escape: the skill restates what the agent already knows — cut it by the admission test, or retire the skill.
- **All assertions always pass** — symptom: no signal; fix: drop them and write harder ones.
- **Judging by outputs only** — symptom: hidden waste; fix: read execution traces — wasted steps mean vague instructions or option overload.
- **Iteration produces narrow patches** — symptom: eval-case-specific instructions appear in the skill; fix: generalize the lesson instead.

**Takeaway** — **a skill earns its place only when the with-vs-without delta on verifiable, evidence-graded assertions is positive and worth its token and time cost — no delta means cut it.**

**Example (constructed, illustrative)** — a "format-JSON" skill scores pass-with 5/5 and pass-without 5/5: zero delta, so by step 5 it is retired — the agent already formats JSON unaided. This is the admission test enforced by measurement rather than judgment.

**In this system** — `skill-creator` (github.com/anthropics/skills → skills/skill-creator) automates this whole loop, and `anthropics/skills` is the official exemplar repo (source: `docs/skills-spec-notes.md`). This eval-driven method — with/without deltas, evidence-graded assertions, train/held-out discipline from [writing-the-description](writing-the-description.md) — is the same methodology our gate uses; the spec notes flag the convergence. → See [what-makes-a-skill-good](what-makes-a-skill-good.md) for the bar this recipe measures against.

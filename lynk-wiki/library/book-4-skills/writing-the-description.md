---
type: recipe
description: Trigger-tune a skill's description with labeled queries and a train/validation split — the description carries the entire burden of activation, so tune it against near-misses.
---

# Writing the description

**What it is** — the recipe for the one field that decides whether a skill ever fires. At startup only `name` + `description` load, so **the description carries the entire burden of triggering** (source: `docs/skills-spec-notes.md`, "optimizing-descriptions"). This recipe tunes it against labeled queries the way you'd tune a classifier.

**Prerequisites**
- A working skill (from [building-a-skill](building-a-skill.md)).
- **~20 realistic labeled queries**: 8–10 that *should* trigger (varying phrasing, explicitness, detail) + 8–10 that should *not* — the valuable negatives are **near-misses** that share keywords but need something else.
- The ability to run repeated fresh sessions (each query run cold).

**Steps** (one observable outcome each)
1. **Write the first description** → an imperative "Use this skill when…" line stating user intent (not implementation), erring pushy ("even if they don't explicitly mention 'CSV'"), ≤ 1024 chars.
2. **Split the queries 60/40** → a train set and a held-out validation set exist.
3. **Run each train query 3 times** → a recorded trigger rate per query, compared against the 0.5 threshold.
4. **Iterate the description on train failures** → a revised description after each round; ~5 iterations is usually enough.
5. **Select the best iteration by *validation* pass rate** → one chosen description, picked on the held-out set, not the train set (choosing on train is overfitting).

**Verification**
- On the **validation set**: trigger rate ≥ threshold for should-trigger queries AND ≤ threshold for should-not queries.
- The spec's own before/after is the quality bar: "Process CSV files." → the full what + when + fires-even-without-keywords form (source: `docs/skills-spec-notes.md`).

**Failure modes** (symptom → fix)
- **Overfit to test phrasings** — symptom: train passes, validation fails; fix: the 60/40 split exists for exactly this — generalize the wording, don't chase specific phrasings.
- **Never triggers on implicit asks** — symptom: misses when the keyword is absent; fix: err pushy, add user-intent keywords ("even if they don't say 'CSV'").
- **Triggers on near-misses** — symptom: false activations on keyword-sharing tasks; fix: sharpen the "when NOT" scope in the description.

**Takeaway** — **tune the description like a classifier: label ~20 queries including near-misses, iterate on a train split, and pick the winner on a held-out validation split so you optimize triggering, not memorizing.**

**Example** — the spec's own before/after (real, cited): the poor "Process CSV files." rewritten to state what it does, when to use it, and to fire even when the user never says "CSV" (source: `docs/skills-spec-notes.md`, optimizing-descriptions). Our library skill's description is a shipped instance of the target shape: what ("Runs the library pipeline…") + when ("Use when the user asks what the books/library/standard say, or when a task needs the constitution's principles or rules") — real, `.claude/skills/library/SKILL.md` line 3.

**In this system** — this recipe tunes step 3 of [building-a-skill](building-a-skill.md). The train/held-out method here is the same eval-driven discipline our gate uses; → See [evaluating-a-skill](evaluating-a-skill.md), which measures output quality once triggering is solved, and the Progressive Disclosure book · `three-stages` for why the description sits alone in the always-paid discovery layer.

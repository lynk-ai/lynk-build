---
type: recipe
description: Prove one metric candidate true by running its SQL against the warehouse, computing any ratio both ways, and matching an externally-sourced anchor — the per-candidate heart of the audit.
---

# Ground a metric

**What it is** — the heart of the audit: disposing of one metric candidate by execution. A candidate is a *smell* — a definition that might compute the wrong number — until the warehouse confirms or refutes it against a value that did not come from the candidate itself (source: `.claude/skills/semantic-layer-audit/references/bug-taxonomy.md`). This is Phase 3 of [audit-a-layer](audit-a-layer.md) at the grain of a single metric.

**Prerequisites**
- A metric candidate: its definition/description and its `sql`. What a metric must be is the spec's job — Docs v2 `concepts/entity/schema-yml/metric.md`; the `sql`/`filter` grammar is Docs v2 `reference/sql-expressions.md`. Point to those; do not restate them.
- A read-only warehouse the candidate's SQL can run against — the *proxy* surface for value truth.
- Access to the **compiled Lynk build** — the *authoritative* surface, where the field is actually consumed. A value can be right on raw tables yet fail to exist or compile in the built layer → See the Evals book · `verify-at-the-authoritative-surface`.
- An **external known value** — the anchor. Valid anchors in order of preference (source: `bug-taxonomy.md`, "Anchoring rule"): (1) a curated truth table of verified real values maintained independently; (2) a sanity invariant (`0 ≤ pct ≤ 100`; parts sum to the total; counts non-negative); (3) a hand-computed expected value from raw rows.

**Steps** (one observable outcome each)
1. **Derive verification SQL from the definition** — read what the metric *claims* to compute and write the SQL that computes exactly that. → *Outcome:* a `proposed_verification_sql` exists.
2. **Run it against the warehouse** (read-only). → *Outcome:* an `actual` value exists.
3. **If a ratio or average is involved, compute the same quantity the other way** — weighted `SUM(num)/SUM(den)` *and* averaged `AVG(per_row_pct)`. → *Outcome:* two values exist for the same quantity.
4. **Compare to the anchor.** → *Outcome:* a match-or-mismatch determination against the external value.
5. **Confirm the field resolves at the authoritative surface** — check the same metric exists and compiles in the built Lynk layer, not only on raw tables. → *Outcome:* the field is confirmed present/compiling in the compiled build (or the finding flips to a compile/consumption bug).
6. **Classify the candidate** — *proven* (matches *and* resolves in the build, attach `actual`/`expected`/`evidence`); *unproven* → dropped; *judgment-only* (correctness rests on a reading call, not execution) → keep it but cite the book principle it rests on. → *Outcome:* a labeled verdict.

**Verification**
- The `actual` value matches the anchor **exactly** for discrete quantities (counts, sums) and **within the anchor's own stated precision** for computed ratios (e.g. ±0.1pp when the anchor is quoted to one decimal place) — a gap beyond that is a mismatch, so the candidate is a bug, not proven. This tolerance is *our* checkable criterion (opinion, ours): `references/gate-rules.md#findings-proven` defines the CONFIRMED evidence contract — the verdict must carry `actual`, `expected`, and `evidence` — but states no numeric tolerance, so we set one here.
- Where step 3 applied, the weighted and averaged forms either **agree** (no ratio bug) or their **discrepancy is explained** (the bug is characterized, e.g. no-attempt rows dragging the average down).
- The `evidence` names an external anchor, not a value re-derived from the candidate's own SQL (source: `gate-rules.md#anchor-external`).
- The metric was reached at the **authoritative surface** — the compiled build — not only the raw-warehouse proxy (source: `../book-6-evals/verify-at-the-authoritative-surface.md`).

**Failure modes** (symptom → fix/escape)
- **The averaged-ratio trap** — symptom: the SQL is clean and *says* it computes a percentage, so it is trusted; but it averages per-row percentages instead of dividing summed numerator by summed denominator, so a 1-for-1 night counts the same as a 12-for-25 night (source: `bug-taxonomy.md#averaged-ratio`). Fix: never trust what the SQL says it computes — run both forms (step 3) and let the numbers decide.
- **Grounded on a proxy surface** — symptom: the value matches the anchor against the raw tables, so the finding is called proven — but the field doesn't exist or doesn't compile in the built layer (false green on a compile/consumption bug: a cyclic reference, a field that resolves only against raw SQL). The raw warehouse is a *proxy*; it is blind to the compiled engine's semantics by construction (source: `../book-6-evals/verify-at-the-authoritative-surface.md`). Fix: re-run at the consumption surface — the compiled Lynk build — before calling it proven.
- **Quoting a remembered gap** — symptom: reporting "it's off by ~6 points" from memory. The magnitude is data-dependent and must be re-derived on the target warehouse (source: `bug-taxonomy.md#averaged-ratio`, "re-derive it, never quote from memory"). Fix: re-run against this warehouse and report *its* number.
- **No external anchor** — symptom: "proven" because the SQL agrees with itself. That is circular (source: `gate-rules.md#anchor-external`). Fix: obtain a curated value, a sanity invariant, or a hand-computed expected; if none exists, the finding is unproven → dropped or judgment-only.

**Takeaway** — **prove a metric by running its SQL and, for any ratio, computing it both ways, matching an externally-sourced anchor and confirming it resolves in the compiled build — trust the numbers at the authoritative surface, never what the SQL says it computes.**

**Example** *(real — the skill's recorded run)* — Jokić career 3P% on `nba-demo-audit-sv2`: step 3 produced **36.5%** weighted (`SUM(3PM)/SUM(3PA)`) and **30.5%** averaged per game with 0-attempt nights as 0%; the ~6-point gap matched the averaged-ratio signature and the weighted form matched the Snowflake-verified anchor over 933 games — CONFIRMED (source: `.claude/skills/semantic-layer-audit/SKILL.md`; `bug-taxonomy.md#averaged-ratio`). The gap size is data-dependent and was re-derived on that warehouse, not quoted. That is a *value* bug the raw-warehouse proxy catches; a compile/consumption bug (a cyclic reference cascading to ~50 "metric not found") passes the raw warehouse and needs the authoritative surface — that separate incident is Book 6's (`../book-6-evals/verify-at-the-authoritative-surface.md`).

**In this system** — this recipe is the unit of "execution disposes" → See [the frame](the-frame.md); the full bug taxonomy (scale-mismatch, description-vs-sql lies, unbacked metrics, ambiguity) lives in the skill's `references/bug-taxonomy.md`, the one authoritative home — this page owns only the grounding *procedure*. → See the Evals book · `verify-at-the-authoritative-surface` for why the compiled build, not the raw warehouse, is the surface that decides, and [audit-a-layer](audit-a-layer.md) for where this sits in the run.

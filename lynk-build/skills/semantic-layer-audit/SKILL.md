---
name: semantic-layer-audit
description: Audits a Lynk `.lynk/` semantic layer end-to-end against the spec, the books, and the warehouse — structural floor, per-entity fan-out, execution-grounding every candidate on real SQL, integrity sweep, and a fail-closed gate. Use whenever someone wants to check, review, verify, QA, sanity-check, or trust a semantic layer, its metrics, or its `.lynk/` definitions against the warehouse or spec — even if they don't say "audit" (e.g. "does this match the database", "is this layer trustworthy", "catch any drift"). NOT for single-phase asks ("just run the gate") or general SQL/db debugging unrelated to a `.lynk/` project.
compatibility: Requires a Lynk `.lynk/` project, the bundled Lynk docs at ${CLAUDE_PLUGIN_ROOT}/semantics_docs, and a reachable read-only warehouse connection for the target.
---

# Semantic Layer Audit — one run, three sources of truth, fail closed

**What it is:** an orchestrator that audits a Lynk `.lynk/` semantic layer (text-to-SQL
context) in a single invocation and returns a *verified punch-list* — it never applies or
commits fixes.

> **Relationship to `lynk-build`:** inline, per-edit quality checks and fixes *during* a build
> live in `lynk-build`'s evaluate flow (`${CLAUDE_PLUGIN_ROOT}/skills/lynk-build/references/evaluate.md`).
> This skill is the deep, whole-layer, execution-grounded audit that grounds every metric against
> the warehouse and returns a verified punch-list — use it for a trust check of the whole layer,
> not for the inline checks a build already runs.

**Takeaway:** a static spec checks **form**; only execution checks **truth** — so no metric
is trusted until its SQL has been run against the warehouse and matched to an externally-sourced
known value. Knowledge proposes, execution disposes.

**Example:** Jokić career 3P% (Snowflake-verified, 933 games) is **36.5%** weighted
(`SUM(3PM)/SUM(3PA)`) but **30.5%** when averaged per-game with 0-attempt nights as 0% — same
valid SQL, a ~6-point lie. Only running both and comparing to a real value catches it — and the
gap's size is data-dependent, so it must be re-derived, never quoted from memory. See
`references/bug-taxonomy.md#averaged-ratio`.

**THE GATE — NON-NEGOTIABLE:** DO run every metric and compare to an external anchor · DON'T
trust what the SQL says it computes · DON'T fix from memory · FAIL CLOSED. Full spec:
`references/gate-rules.md`.

## The four surfaces of correctness — verify at the AUTHORITATIVE one
- **Docs** (`${CLAUDE_PLUGIN_ROOT}/semantics_docs`) — what a layer must BE. Cite a rule. *(the law)*
- **Books** — how good context is written. Route via the `library` skill; never read inline. *(principles)*
- **Warehouse** — what the numbers really ARE. Read-only. *(proves the DATA, not the LAYER)*
- **Lynk build** — does the layer COMPILE and every field RESOLVE at the consumption layer.
  **This is the authoritative gate.** Static ref-resolution and raw-warehouse queries are
  *proxies*: they pass green while a cross-entity dependency cycle stops entities from compiling.
  **A green proxy over a red build is FALSE GREEN** — the exact failure that once shipped past
  this skill (branch verified "clean" statically + on raw SQL, yet the Lynk build failed with
  `CTE … does not exist`). "A reference resolves" ≠ "the entity builds."

Fix method + bug classes live in `references/bug-taxonomy.md`; the per-file checklist in
`references/file-rubric.md`; the worker briefs in `references/phase-prompts.md`. This skill
only sequences them.

---

## Phases (each dispatches a strict brief from `references/phase-prompts.md`)

- **0 · Orient & scope** — confirm target `.lynk/`, scope (`.md` + `GLOSSARY.yml` by default;
  `schema.yml` only on explicit opt-in), and that the read-only warehouse is reachable.
- **1 · Structural floor** (Layer 1, form; cheapest first) — dispatch `floor`. Includes
  **cross-entity dependency-cycle detection** — metric/feature/relationship loops *between*
  entities (via `join_name` / `metric()`), not just `.md` `@`-injection cycles.
  **Gate 1→2:** well-formed violation list before fanning out.
- **1b · BUILD PROBE — the authoritative gate.** Run the Lynk build (or `SELECT <field> FROM
  <entity> LIMIT 0` per field *through the Lynk engine*, NOT raw warehouse). Any
  `SemanticsConsumptionError` or `CTE … does not exist` = the layer doesn't compile → **FAIL
  CLOSED before anything else.** Static "refs resolve" ≠ "entity builds" — this is the only step
  that proves it. (Needs the Lynk engine/build API; raw Snowflake cannot substitute.)
- **2 · Judged fan-out** (Layer 2, discover; book-5 orchestrator-workers) — per entity, dispatch
  `passA` (file alone) and `passB` (file in its graph) as **two separate briefs**.
  **Cap the fan:** batch small entities into a shared worker; sole worker only for large ones.
  Principle calls (right home? inline vs link?) → route to the librarian, cite `book · page`.
  **Gate 2→3:** every value candidate must carry `proposed_verification_sql` + an external
  anchor, else it is dropped, not grounded.
- **3 · Execution-ground** (Layer 2, prove) — dispatch `grounder` **in parallel, one per unique
  (deduped) candidate**. Unproven + non-structural → dropped or `judgment-only` (cite the book).
- **4 · Integrity sweep** — dispatch `sweep`; its typed `{danglers, dupes}` must be empty.
- **5 · The gate** — evaluate every `blocker` in `references/gate-rules.md`; emit the
  forced-schema PASS/REJECT verdict. Never soften a REJECT.
- **6 · Report, then STOP** — deliver the verified punch-list (location · class · rule cited ·
  execution evidence · proposed fix). Offer the shareable playbook artifact. **Apply nothing.**

## Measuring the gate (don't assume it works)
Calibrate before trusting: seed real past defects (see `evals/evals.json`) into clean files,
run the gate blind, score catch-rate vs false-alarm, k≥3 trials. Value = with/without ablation
delta on a non-inferable case. A badly-built grounder can be *worse than no gate* — measure it.

## Guardrails — this skill's operating contract (never overridden)
- **Audit runs end-to-end; fixes do not** — applying fixes is a separate, human-gated loop
  (one at a time, next only after approval).
- **Commit only on the explicit word "commit"** — never before review, never batched; run the
  books before every commit.
- **Build before commit** — re-run the build probe (Phase 1b) after every schema edit. "Refs
  resolve" is not "it builds"; a green static check over a red build is false green.
- **Scope is `.md` + `GLOSSARY.yml`** unless the user opts into `schema.yml`.
- **Data is known, not assumed** — every fact traces to the warehouse or a cited source.
- **The DB is read-only** — schema/data fixes are documented and handed off.

## Fallback — subagents can't spawn
Run the phases inline and sequentially, same order and gate — but still produce each worker's
**typed return** yourself so Phase 5 has structured artifacts to check. Don't retry spawning.

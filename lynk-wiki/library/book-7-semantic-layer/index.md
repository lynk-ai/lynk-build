# Index

**Book 7 — The Lynk Semantic Layer.** One book for the whole loop: **build → audit → fix → re-audit** over a Lynk `.lynk/` semantic layer, plus the **maintenance** arc that re-runs that loop continuously once a layer ships. It merges the former audit book (Book 7) and build/fix book (Book 8) into a single home, because building and correcting a layer are one loop, not two jobs.

**How to use this book (read only the page your task needs).** This index is the discovery layer — a pointer to every page so you can open just the one that matches. Start at `the-frame` if you're new; otherwise route straight from the table:

| I need to… | Read |
|---|---|
| Understand the frame (what proves a layer correct) | `the-frame` |
| Build a layer from a DB | `build-a-layer` |
| Verify a layer / prove a metric | `audit-a-layer`, `ground-a-metric` |
| Trust the audit gate itself | `calibrate-the-audit-gate` |
| Fix a verified finding | `fix-a-finding` |
| Break a build-blocking dependency cycle | `break-a-dependency-cycle` |
| Keep a shipped layer correct as the warehouse/business change | `maintain-a-layer` |

**What this book is *not*.** It is not the spec. **Lynk Docs v2** (`/Users/shakedyacoby/git/lynk/lynk-docs/docs/`) owns what a layer, entity, feature, or metric must *be* — the mental model (`README.md`), the primitives (`concepts/entity/`), the build lifecycle (`concepts/project.md`), and the tree (`reference/layout-and-naming.md`). A capable agent reads those directly, so restating them here would be rot (Book 2 `non-inferable-only`). Docs v2 has **no** maintenance-procedure page — so the maintenance *method* (`maintain-a-layer`) is one place this book adds knowledge the spec doesn't hold. This book **points** to Docs v2 for every spec rule and owns only the *method*: the sequence, the judgment, the failure modes.

**Its relationship to the skill.** The `semantic-layer-audit` **skill** *executes* this methodology — it holds the operational detail (phase prompts, exact worker briefs, the gate schema, the value-smell classes in `references/bug-taxonomy.md`). This book is the consultable *knowledge behind* the skill: the same idea in its two forms (Book 1 `self-compiled-vs-curated`). When operational detail is needed, this book points to the skill; it does not duplicate it.

**Page shape:** every page follows the concept template (Book 2 `page-template`).

## Part I — The frame *(principle)*

| # | Page | One-liner |
|---|---|---|
| 1 | `the-frame.md` | What proves a `.lynk/` layer correct — judged against three sources (Docs the law, Books the principles, Warehouse the decisive lens) and built through one loop (build → audit → fix → re-audit) that is not done until the layer compiles at the authoritative surface and its metrics ground true. |

## Part II — Build *(recipe)*

| # | Page | One-liner |
|---|---|---|
| 2 | `build-a-layer.md` | Construct a `.lynk/` layer from a database and pre-knowledge — scaffold the tree, model core first, add entities, define metrics avoiding the value smells, and build-probe at the consumption surface until it compiles. |

## Part III — Verify *(recipes)*

| # | Page | One-liner |
|---|---|---|
| 3 | `audit-a-layer.md` | The end-to-end audit — orient, structural floor, judged per-entity fan-out, execution-ground at the authoritative surface, integrity sweep, fail-closed gate, report and stop — producing a verified punch-list, never a fix. |
| 4 | `ground-a-metric.md` | Prove one metric candidate true by running its SQL against the warehouse, computing any ratio both ways, matching an externally-sourced anchor, and confirming it resolves in the compiled build — the per-candidate heart of the audit. |
| 5 | `calibrate-the-audit-gate.md` | Prove the audit gate itself is trustworthy — seed real past defects into clean files, run blind, score catch-rate vs false-alarm, and measure the with/without delta on a non-inferable case. |

## Part IV — Fix *(recipes)*

| # | Page | One-liner |
|---|---|---|
| 6 | `fix-a-finding.md` | Resolve one audit finding safely — apply its class-specific fix, re-ground the metric, rebuild at the authoritative surface, get human approval, and only then take the next. |
| 7 | `break-a-dependency-cycle.md` | Fix the compile-time cross-entity cycle — detect the loop the build reveals but static resolution hides, pick the back-edge to cut, source the field from the entity's own columns, and rebuild green. |

## Part V — Maintain *(recipe)*

| # | Page | One-liner |
|---|---|---|
| 8 | `maintain-a-layer.md` | Keep a shipped `.lynk/` layer correct as the warehouse and business change — rebuild to catch drift, rename with reference updates, deprecate on a lifecycle, and keep a definition changelog so value bugs can't silently regress. |

## What this book points to (and never restates)

- **The spec** → Docs v2: `README.md` (brain organized by concept), `concepts/entity/` + `concepts/entity/schema-yml/{feature,metric,relationships,identity-and-imports}.md`, `reference/sql-expressions.md`, `concepts/project.md` (build lifecycle), `concepts/entity/entity-md.md` (`enabled`), `reference/layout-and-naming.md` (the tree). (Docs v2 specs the maintenance *mechanisms* — `enabled`, the reference forms, the build lifecycle — but has no maintenance-procedure page; the method is `maintain-a-layer`'s own.)
- **The value-smell classes and per-class fixes** → the `semantic-layer-audit` skill's `references/bug-taxonomy.md` — the one authoritative home.
- **The orchestration pattern** → Book 5: `orchestrator-workers`, `the-strict-brief`.
- **The general eval instruments** → Book 6: `verify-at-the-authoritative-surface` (the surface principle this book applies to Lynk), `calibrate-a-judge`, `run-a-baseline-delta`.
- **The economics of loading one page at a time** → Book 3: `the-economics`, `three-stages`, `pointers-not-content`.
- **The distinguishability principle** → Book 1: `distinguishability` (why two metrics an agent chooses between need distinct names AND descriptions).
- **The operational detail and fix-loop contract** → the `semantic-layer-audit` skill: `SKILL.md` and its `references/` (bug-taxonomy, file-rubric, phase-prompts, gate-rules).

## Sources

- `.claude/skills/semantic-layer-audit/SKILL.md` + `references/{bug-taxonomy,file-rubric,phase-prompts,gate-rules}.md` — the method and the fix-loop discipline, already structured; this book is its consultable form.
- Lynk Docs v2 (`/Users/shakedyacoby/git/lynk/lynk-docs/docs/`) — the spec this book points at for what each primitive must *be* and for the maintenance mechanisms (`enabled`, reference forms, build lifecycle); it has no maintenance-procedure page, so `maintain-a-layer` supplies the method.
- `/Users/shakedyacoby/git/lynk/semantic_layers/nba-demo-audit-sv2/` — the real `.lynk/` target of the skill's recorded run; source of the Jokić 3P% worked example (values Snowflake-verified over 933 games in that run; the gap is data-dependent and re-derived per warehouse). `PENDING_COMPLEX_QUESTIONS.md` in it is the "record it, don't fake it" material.
- `docs/semantic-layer-build-cycle-2026-07-12.md` — the real cross-entity-cycle incident (`player_game` ↔ `team_game`): 106 `metric()` calls + 718 paths resolved statically, the build still failed; telemetry Logfire / Tom Harpaz. The worked example for the cycle recipe.
- `networx-semantic-layer-2026-07-09.zip` — a real shipped layer (`core` + `operations` domains, entities with `ENTITY.md` + `schema.yml`, policies, a text-to-sql skill); the target shape `build-a-layer` produces.

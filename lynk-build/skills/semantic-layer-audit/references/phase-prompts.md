# Phase prompts — the strict briefs

One brief per worker type. Each carries the four required parts (book-5 `the-strict-brief`):
**objective · tools/sources · output schema · boundaries**. The skill dispatches these; it
does not restate them.

Substitute `<target>` (the `.lynk/` dir), `<entity>`, and `<candidate>` at dispatch.

---

## floor — structural conformance (Phase 1, ONE worker)
- **Objective:** find every structural violation in `<target>/.lynk` against the v2 spec.
- **Tools/sources:** Read + Grep over the tree; the bundled v2 docs at `${CLAUDE_PLUGIN_ROOT}/semantics_docs`
  (`reference/markdown-format.md`, `layout-and-naming.md`, `sql-expressions.md`).
- **Boundaries:** structure only — no value/semantic judgment; do not open the warehouse.
- **Output:** `[{file, line, rule, broken}]`
- **Checks:** frontmatter present + `name`==folder; every `@`/link/bare path resolves; paths
  absolute from `/.lynk/`; no peer-domain refs, cycles, or refs to disabled entities; every
  entity has BOTH `ENTITY.md` + `schema.yml`; no orphan files.

## passA — file-alone quality (Phase 2, one worker PER entity/batch)
- **Objective:** judge `<entity>` files ALONE against `file-rubric.md` Pass A + flag value
  smells from `bug-taxonomy.md`.
- **Tools/sources:** Read the entity's `ENTITY.md` + `schema.yml`; the two reference files
  above. Do NOT run SQL (that is the grounder's job).
- **Boundaries:** this entity only; isolation quality + value smells; no cross-file/graph
  reasoning (that is Pass B).
- **Output:** `[{file, line, class, claim, proposed_verification_sql, anchor, expected_truth}]`

## passB — file-in-graph coherence (Phase 2, one worker PER entity/batch)
- **Objective:** judge `<entity>` against its connections per `file-rubric.md` Pass B.
- **Tools/sources:** Read + Grep across the tree to resolve pointed-by / points-at.
- **Boundaries:** **own only the edges this file *points at*** (the pointer checks the edge, not
  the pointee) — prevents double-grading the same edge from both ends.
- **Output:** `[{file, relation, other_file, class, claim, rule_cited}]`

## grounder — execution proof (Phase 3, one worker PER unique candidate, PARALLEL)
- **Objective:** prove or refute ONE candidate by running its SQL against the warehouse.
- **Tools/sources:** the read-only warehouse; the **externally-sourced anchor** handed in
  (never invent the expected value from the candidate's own SQL — circular).
- **Boundaries:** run + compare only; never write to the DB; one candidate per worker.
- **Output:** `{verdict: CONFIRMED|REFUTED, actual, expected, evidence}`

## sweep — integrity (Phase 4, ONE worker)
- **Objective:** after analysis, re-scan the whole tree for danglers/dupes introduced or
  exposed (a rename breaks a ref three files away).
- **Tools/sources:** Read + Grep over the tree.
- **Boundaries:** integrity only; no value judgment.
- **Output:** `{danglers: [{file, ref}], dupes: [{concept, files:[]}]}` — must be empty to PASS.

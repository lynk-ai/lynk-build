---
type: recipe
description: The end-to-end audit of a .lynk/ layer — orient, structural floor, judged per-entity fan-out, execution-ground at the authoritative surface, integrity sweep, fail-closed gate, report and stop — producing a verified punch-list, never a fix.
---

# Audit a layer

**What it is** — the full run: how to take a target `.lynk/` semantic layer and return a *verified punch-list* — every finding located, classed, cited to a rule, and backed by execution evidence — without ever applying or committing a fix (source: `.claude/skills/semantic-layer-audit/SKILL.md`, "What it is" + guardrails). Audit is a separate loop from fix; this recipe ends at the report.

**Prerequisites**
- A target `.lynk/` project to audit (a real semantic-layer tree; the worked target in the skill's run is `/Users/shakedyacoby/git/lynk/semantic_layers/nba-demo-audit-sv2/`).
- The Docs v2 spec reachable as the law to cite — `/Users/shakedyacoby/git/lynk/lynk-docs/docs/` (source: SKILL.md `compatibility`).
- A reachable **read-only** warehouse connection for the target (source: SKILL.md `compatibility`) — the *proxy* surface for value truth. Without it, no candidate can be grounded and the gate cannot pass — the audit is blocked, not merely degraded.
- Access to the **compiled Lynk build** — the *authoritative* surface where the layer is consumed. Value bugs surface on the raw warehouse; compile/consumption bugs (cyclic references, fields that don't resolve in the build) surface only here → See the Evals book · `verify-at-the-authoritative-surface`.
- Decide scope: `.md` + `GLOSSARY.yml` by default; `schema.yml` only on explicit opt-in (source: SKILL.md guardrails).

**Steps** (one observable outcome each; each inter-phase gate must pass before the next step)
1. **Phase 0 — orient & scope.** Confirm the target `.lynk/` dir, the scope decision, and that the read-only warehouse answers. → *Outcome:* a confirmed target + scope + a live warehouse handshake.
2. **Phase 1 — structural floor.** Dispatch the `floor` worker (Layer 1, form; cheapest first) to find every structural violation against the spec. → *Outcome:* a well-formed violation list `[{file, line, rule, broken}]`. **Gate 1→2:** it must be well-formed before fanning out.
3. **Phase 2 — judged fan-out, per entity.** For each entity dispatch **two separate briefs** — `passA` (the file alone) and `passB` (the file in its graph) — batching small entities into a shared worker, a sole worker only for large ones. Principle calls (right home? inline vs link?) route to the librarian, cited `book · page`. → *Outcome:* per-entity findings where every value candidate carries a `proposed_verification_sql` **and** an external anchor. **Gate 2→3:** a candidate missing either is dropped, not grounded.
4. **Phase 3 — execution-ground at the authoritative surface.** Dispatch a `grounder` in parallel, one per unique (deduped) candidate, to run its SQL against the raw warehouse (value truth) *and* confirm the finding at the compiled Lynk build — a green raw-warehouse check over a red compiled build is false green (source: `../book-6-evals/verify-at-the-authoritative-surface.md`). → *Outcome:* a `CONFIRMED|REFUTED` verdict per candidate whose evidence reaches the compiled surface; unproven non-structural findings are dropped or marked `judgment-only` with the book cited. (The per-candidate procedure is its own recipe → See [ground-a-metric](ground-a-metric.md).)
5. **Phase 4 — integrity sweep.** Dispatch the `sweep` worker to re-scan the whole tree for danglers and dupes a rename may have exposed. → *Outcome:* a typed `{danglers, dupes}` that must be **empty** to pass.
6. **Phase 5 — the gate.** Evaluate every `blocker` in the gate spec and emit the forced-schema PASS/REJECT verdict. → *Outcome:* a `<result>` verdict with a `<violations>` list.
7. **Phase 6 — report, then STOP.** Deliver the punch-list — each finding as *location · class · rule cited · execution evidence · proposed fix* — and apply nothing. → *Outcome:* the delivered punch-list; the tree is untouched.

The fan-out in steps 3–4 is the orchestrator-workers pattern, and each worker carries a four-part strict brief — this recipe *uses* both rather than restating them → See the Subagents book · `orchestrator-workers` and the Subagents book · `the-strict-brief`. The exact worker briefs live in the skill's `references/phase-prompts.md`, not here.

**Verification**
- Every non-dropped value finding carries a grounder verdict `CONFIRMED` with `actual`, `expected`, and `evidence` attached — no asserted findings (source: `references/gate-rules.md#findings-proven`).
- Each grounder verdict's `evidence` names an *externally-sourced* anchor — a curated value, a sanity invariant, or a hand-computed expected — never a value derived from the candidate's own SQL (source: `gate-rules.md#anchor-external`).
- The verdict reached the **authoritative surface**: the finding was confirmed against the compiled Lynk build, not only the raw-warehouse proxy (source: `../book-6-evals/verify-at-the-authoritative-surface.md`).
- The `floor` list and the `sweep` `{danglers, dupes}` are both empty (`structural-clean`, `integrity-clean`).
- Every proposed fix cites a rule — a Docs v2 rule or a `book · page` (`rule-cited`).
- The gate emitted a single forced `PASS` or `REJECT`; a `REJECT` was reported verbatim, not softened.

**Failure modes** (symptom → fix/escape)
- **Grounding without an anchor** — symptom: a finding marked CONFIRMED whose expected value came from re-running the candidate's own SQL. That is circular and the gate blocks it (`anchor-external`); fix: supply an external anchor or drop the candidate.
- **Stopping at the proxy surface** — symptom: the audit declares the layer clean because static structure passed *and* the numbers ran green on the raw warehouse — but the compiled build fails (a cyclic reference breaks compilation and cascades to "metric not found" across downstream metrics), invisible to both lower surfaces by construction. That is false green (source: `../book-6-evals/verify-at-the-authoritative-surface.md`); fix: ground every finding at the compiled Lynk build, not only the raw warehouse.
- **Softening a REJECT** — symptom: the report hedges a blocker violation into a suggestion. Never soften a REJECT (source: SKILL.md gate, `gate-rules.md` Verdict); fix: emit the REJECT as-is and let the human decide.
- **Applying fixes during the audit** — symptom: the tree changed. Audit ≠ fix; fixes are a separate, human-gated, one-at-a-time loop (source: SKILL.md guardrails); escape: revert and hand off the punch-list.
- **Fixing from memory** — symptom: a value fix that traces to no grounder verdict or cited source. The gate blocks it (`no-memory-fix`); fix: ground it or cite it.
- **Subagents can't spawn** — symptom: the fan-out won't dispatch; fix: run the phases inline and sequentially in the same order and gate, still producing each worker's typed return so Phase 5 has structured artifacts to check (source: SKILL.md "Fallback"). Don't retry spawning.

**Takeaway** — **an audit runs end-to-end to a verified punch-list and stops — form is checked cheaply first, every value is disposed of by execution reaching the compiled build (not just the raw-warehouse proxy), the gate fails closed, and no fix is ever applied.**

**Example** *(real — the skill's recorded run)* — auditing `nba-demo-audit-sv2` surfaced the Jokić 3P% averaged-ratio finding: a metric that passed every structural rule but computed 30.5% where the warehouse-weighted truth was 36.5% (source: SKILL.md; `references/bug-taxonomy.md#averaged-ratio`). It entered Phase 2 as a value smell, was disposed of CONFIRMED in Phase 3 against a Snowflake-verified anchor, and reached the report as a punch-list item — no fix applied. That is a value bug the raw warehouse catches; the false-green counterpart — a cyclic reference that passes static + raw-warehouse yet breaks the compiled build — is why Phase 3 must reach the authoritative surface (Book 6's incident, `../book-6-evals/verify-at-the-authoritative-surface.md`).

**In this system** — this book is the methodology the `semantic-layer-audit` skill runs; the skill owns the operational detail (phase prompts, exact briefs, gate schema), and this page owns the sequence and the judgment. → See [the frame](the-frame.md) for why execution is decisive, the Evals book · `verify-at-the-authoritative-surface` for why the compiled build is the surface that decides, [ground-a-metric](ground-a-metric.md) for Phase 3 up close, and [calibrate-the-audit-gate](calibrate-the-audit-gate.md) for proving the Phase 5 gate is worth trusting.

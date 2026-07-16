# Gate rules — the fail-closed spec

Each clause is a runnable check, not prose ("a rule without an eval is a wish" —
book-6 `every-rule-is-an-eval`). Fields per rule: `statement · gate_criteria · severity ·
scope`. The gate PASSes only when every `blocker` rule passes.

---

- id: structural-clean
  statement: The tree has zero structural violations.
  gate_criteria: floor worker returns `[]`.
  severity: blocker
  scope: whole tree

- id: builds-clean
  statement: The layer COMPILES — every entity emits its CTE.
  gate_criteria: the Lynk build succeeds; no `SemanticsConsumptionError`, no `CTE … does not
    exist`. Run against the Lynk engine, NOT raw warehouse (raw SQL gives false green).
  severity: blocker
  scope: whole layer

- id: field-probes-clean
  statement: Every field resolves at the consumption layer.
  gate_criteria: `SELECT <field> FROM <entity> LIMIT 0` through the Lynk engine returns no error
    for every field/metric.
  severity: blocker
  scope: per field

- id: no-cross-entity-cycle
  statement: No circular dependency between entities.
  gate_criteria: the entity dependency graph (edges from `join_name` / `metric()` refs) is
    acyclic. A cycle passes static ref-resolution but stops both entities from compiling.
  severity: blocker
  scope: whole layer

- id: findings-proven
  statement: Every confirmed value finding is proven by execution, not asserted.
  gate_criteria: each non-dropped value finding has a grounder verdict CONFIRMED with `actual`,
    `expected`, and `evidence` attached.
  severity: blocker
  scope: per finding

- id: anchor-external
  statement: Each grounder verdict used an externally-sourced anchor.
  gate_criteria: verdict.evidence names a curated value, sanity invariant, or hand-computed
    expected — NOT a value derived from the candidate's own SQL (circular).
  severity: blocker
  scope: per finding

- id: rule-cited
  statement: Every proposed fix cites a rule.
  gate_criteria: fix references a v2 doc rule OR a book `book · page`.
  severity: blocker
  scope: per finding

- id: integrity-clean
  statement: No danglers or duplicates remain after analysis.
  gate_criteria: sweep worker returns empty `danglers` and `dupes`.
  severity: blocker
  scope: whole tree

- id: no-memory-fix
  statement: No fix rests on a remembered value.
  gate_criteria: adherence check — every value fix traces to a grounder verdict or cited
    source; none to model memory alone.
  severity: blocker
  scope: per finding

- id: metric-name-unique-in-domain
  statement: Metric names are unique across the whole domain, not just within an entity.
  gate_criteria: build reports no "Duplicate metric name '…' in domain".
  severity: blocker
  scope: domain
  fix: rename entity-qualified AND give each a distinguishing description
    (bug-taxonomy `domain-duplicate-metric-name`) — confirmed a real rule, not validator over-strictness.

- id: distinguishable
  statement: Two metrics an agent must choose between have distinct names AND descriptions.
  gate_criteria: no two metrics share a name; none share an identical description.
  severity: major
  scope: domain

## Verdict
```
<result>PASS</result> | <result>REJECT</result>
<violations>[ {rule_id, file, evidence} ]</violations>
```
Never soften a REJECT.

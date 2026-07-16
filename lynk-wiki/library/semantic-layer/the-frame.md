---
type: principle
description: What proves a .lynk/ layer correct — judged against three sources (Docs the law, Books the principles, Warehouse the decisive lens) and built through one loop (build → audit → fix → re-audit) that is not done until the layer compiles at the authoritative surface and its metrics ground true.
---

# The frame

**What it is** — the epistemic frame the whole book hangs on: what it means for a Lynk `.lynk/` semantic layer to be *correct*, and the one loop that gets it there. Constructing a layer and correcting it are not two jobs; they are one loop — **build → audit → fix → re-audit** — repeated until the layer both compiles and computes true. And correctness is judged against three sources, each answering a different question (source: `.claude/skills/semantic-layer-audit/SKILL.md`, "The three sources of correctness"):

| Source | Answers | Role | Access |
|---|---|---|---|
| **Docs** (Docs v2, `/Users/shakedyacoby/git/lynk/lynk-docs/docs/`) | What a layer must **BE**. | The law — cite a rule. | Read the spec page. |
| **Books** (this library) | How good context is **written**. | The principles — route via the librarian, never read inline. | `→ See` the owning page. |
| **Warehouse** (the customer's database + the compiled layer) | What the numbers really **ARE**. | The decisive lens. | Read-only. |

**Mechanics** — the sources are not equal. Docs and Books are *static specs*: they check **form** — is the file shaped right, is the concept in its one home, is the description honest. A file can pass every static rule and still compute a wrong number, so form is never enough: *knowledge proposes, execution disposes* (source: SKILL.md, "Takeaway"). But execution itself has more than one surface, and they are not equally trustworthy — a check is only as trustworthy as the surface it runs on (this is Book 6's general principle → See the Evals book · `verify-at-the-authoritative-surface`, which this frame applies to the Lynk loop; do not re-derive the false-green argument here). The decisive lens splits into two Lynk surfaces:

| Surface | Catches | Blind to |
|---|---|---|
| **Raw warehouse** (a *proxy* — necessary, not sufficient) | value bugs: a metric that computes the wrong number against real rows (e.g. the averaged-ratio lie). | the compiled engine's compile and consumption semantics. |
| **Compiled Lynk build** (the *authoritative* surface — where the layer is actually consumed) | compile/consumption bugs the raw warehouse cannot see — cyclic references, fields that don't resolve in the built layer, cascaded "metric not found". | — this is the truth surface. |

A green raw-warehouse check over a red compiled build is **false green** (Book 6's term). So the loop has two acceptance conditions, and a layer that meets only one is not built:

| Condition | Surface it is proven on |
|---|---|
| **It compiles** — every entity emits its CTE and every field resolves as it is consumed. | The **authoritative** surface: the compiled Lynk build, not the raw warehouse. |
| **Its metrics ground true** — each number matches an externally-sourced known value. | The raw warehouse (a *proxy* for value truth), confirmed at the build → See [ground-a-metric](ground-a-metric.md). |

Because the audit is where a build proves itself, construction and verification cannot be sequenced apart — they interleave, which is why this is one loop, not three tasks. "It's written and the SQL resolves" is never "it's built"; building is finished only when the audit passes at the authoritative surface (source: SKILL.md, "Build before commit"). A candidate that cannot be put to execution and has no structural basis is dropped or marked judgment-only, never asserted (source: `.claude/skills/semantic-layer-audit/references/file-rubric.md`, "Verdict shape").

**Takeaway** — **a layer is correct only when it compiles at the authoritative surface (the compiled Lynk build) and every metric grounds true against an externally-sourced value — so building, auditing, and fixing are one loop, and no finding is trusted until it reaches that surface.**

**Example** *(real — the two paired bugs that show both surfaces)* — a **value** bug the raw-warehouse proxy catches: Jokić's career three-point percentage, computed weighted as `SUM(3PM)/SUM(3PA)`, is **36.5%**; computed by averaging each game's percentage with 0-attempt nights counted as 0%, it is **30.5%** — a ~6-point gap from the *same valid SQL* (source: SKILL.md "Example"; `references/bug-taxonomy.md#averaged-ratio`; Snowflake-verified across 933 games in that run; the gap is data-dependent — re-derive it on the target warehouse, never quote from memory). A **compile** bug only the authoritative surface catches: the `nba-demo` layer had 106 `metric()` calls and 718 entity-qualified paths all resolve statically and sample metrics run green on Snowflake — yet the Lynk build failed with `CTE … does not exist` because `player_game` and `team_game` referenced each other in a compile-time loop, cascading to dozens of "metric not found" probes (source: `docs/semantic-layer-build-cycle-2026-07-12.md`; Book 6 owns this incident as its false-green example, cited above). One is proven on the proxy, one only at the authority — together they are why the loop must reach the compiled build.

**In this system** — this page is the spine the recipes hang on: [build-a-layer](build-a-layer.md) is the *build* arc; [audit-a-layer](audit-a-layer.md), [ground-a-metric](ground-a-metric.md), and [calibrate-the-audit-gate](calibrate-the-audit-gate.md) are the *verify* arc; [fix-a-finding](fix-a-finding.md) and [break-a-dependency-cycle](break-a-dependency-cycle.md) are the *fix* arc — each fix arc ends by handing back to the audit for the re-audit; and [maintain-a-layer](maintain-a-layer.md) is the *maintenance* arc — the same loop re-run continuously once the layer ships, as the warehouse and business drift beneath it. The `semantic-layer-audit` skill *executes* this frame; this book is the consultable methodology behind it — the judgment and sequence, not the operational briefs. For what a layer must *be*, point to Docs v2 (`README.md` mental model, `concepts/entity/schema-yml/metric.md` for a metric, `concepts/project.md` for the build lifecycle that defines the authoritative surface) rather than restating it here. → See the Evals book · `verify-at-the-authoritative-surface` for the general surface principle this frame applies.

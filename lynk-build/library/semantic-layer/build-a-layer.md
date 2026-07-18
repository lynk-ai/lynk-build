---
type: recipe
description: Construct a .lynk/ layer from a database and pre-knowledge — scaffold the tree, model core first, add entities, define metrics avoiding the value smells, and build-probe at the consumption surface until it compiles.
---

# Build a layer

**What it is** — the construction arc of the loop: taking a target warehouse plus what you know about the business and producing a `.lynk/` semantic layer that *compiles and grounds true*. This recipe owns the **build method and its ordering**; it does not restate the spec (what an entity, feature, or metric must *be* lives in Docs v2) nor the audit that verifies it. It ends by handing the finished tree to [audit-a-layer](audit-a-layer.md).

**Prerequisites**
- A target warehouse, connected **read-only** — the layer points at tables, it does not contain them (source: Docs v2 `concepts/project.md`, "A project is not the data warehouse"). Read-only because the build agent never mutates customer data (source: `.claude/skills/semantic-layer-audit/SKILL.md` guardrails, "The DB is read-only").
- The **Docs v2 spec** reachable as the law for what each primitive must be — `${CLAUDE_PLUGIN_ROOT}/semantics_docs/` (`README.md` mental model, `concepts/entity/` for entities, `concepts/entity/schema-yml/{feature,metric,relationships}.md`, `reference/layout-and-naming.md` for the tree). Point to these; never restate them.
- **Decided domains** — one domain per team/audience, because a domain *is* an agent (source: Docs v2 `README.md`, "Domains are agents"). You must know the audiences before scaffolding, or the tree gets restructured later.
- Access to the **compiled Lynk build** — the authoritative surface where the layer is consumed. Without it you can write files but cannot prove they build (→ See the Evals book · `verify-at-the-authoritative-surface`).

**Steps** (one observable outcome each)
1. **Scaffold the tree.** Create `.lynk/` with `lynk.yml` (required) and the `domains/` folder, one folder per decided domain, following Docs v2 `reference/layout-and-naming.md`. → *Outcome:* `.lynk/lynk.yml` exists and the domain folders are present.
2. **Model the shared domain (core) first.** Put shared truth — the entities and vocabulary other domains build on — in `core` and set `shared_domain` in `lynk.yml` (source: Docs v2 `README.md` tree, `core/` "the shared domain others build on"). → *Outcome:* `core` holds the shared entities; team domains reference them, not copies. Shared-vs-private placement is Book 1's rule → See the Best Context book · `one-concept-one-home`.
3. **Add each entity** as a folder with an `ENTITY.md` (prose: quirks, conventions) and a `schema.yml` (structure: features, metrics, relationships) — the two-file split Docs v2 defines (source: Docs v2 `README.md` tree; `concepts/entity/`). Everything true about an entity lives in that entity's home. → *Outcome:* each entity folder has both files and each describes itself honestly.
4. **Define metrics, actively avoiding the value smells.** As you write each metric, check it against the known value-smell classes — averaged-ratio, scale-mismatch, description-vs-SQL, unbacked — whose signatures and per-class fixes are enumerated in `.claude/skills/semantic-layer-audit/references/bug-taxonomy.md` (the one authoritative home; do not re-list them). Most important: write ratios as `SUM(numerator)/SUM(denominator)`, never `AVG(per_row_pct)` (source: `bug-taxonomy.md#averaged-ratio`). → *Outcome:* every metric's SQL matches its description and no ratio is averaged.
5. **Keep progressive disclosure in the files.** Inline only what every load needs; push detail behind pointers so the always-loaded layer stays cheap (→ See the Progressive Disclosure book · `pointers-not-content` and the per-file bar in `.claude/skills/semantic-layer-audit/references/file-rubric.md`, Pass A "Progressive disclosure"). → *Outcome:* no file inlines detail that most loads don't need.
6. **Build & probe at the consumption surface.** Run the Lynk build (`POST /builds` → compile → probe each field via `SELECT <field> FROM <entity> LIMIT 0` *through the Lynk engine*, not raw warehouse; source: `docs/semantic-layer-build-cycle-2026-07-12.md`). → *Outcome:* the build either compiles green or returns a named error to fix before proceeding.

**Verification**
- The Lynk build **passes** — every entity emits its CTE and every field probe resolves at the authoritative surface, not merely on raw tables (source: `.claude/skills/semantic-layer-audit/SKILL.md`, Phase 1b "the authoritative gate"; → See the Evals book · `verify-at-the-authoritative-surface`).
- Handed to the audit, the layer's metrics **ground true**: each grounded value matches an externally-sourced anchor (→ See [ground-a-metric](ground-a-metric.md)). Building stops at "it compiles"; grounding-true is proven by the audit arc.
- When a question genuinely can't be modeled yet, that limitation is **recorded, not faked** — write it down as a pending case rather than shipping a metric that lies (real example: `nba-demo-audit-sv2/PENDING_COMPLEX_QUESTIONS.md` records rolling-window / `LAG` questions parked until window-function support exists).

**Failure modes** (symptom → fix/escape)
- **Cross-entity dependency cycle** — symptom: static refs all resolve and raw-warehouse queries run green, but the build fails with `CTE … does not exist` cascading to "metric not found" across downstream metrics. Two entities reference each other's metrics/features, so neither can emit its CTE (source: `bug-taxonomy.md#cross-entity-cycle`; incident `docs/semantic-layer-build-cycle-2026-07-12.md`). Fix: break one back-edge — source the field from the entity's own columns instead of a round-trip → See [break-a-dependency-cycle](break-a-dependency-cycle.md).
- **Over-inlining that every load pays for** — symptom: files carry detail most questions never touch, so every session pays for context it doesn't use. Fix: move it behind a pointer (→ See the Progressive Disclosure book · `pointers-not-content`).
- **Averaged-ratio metric** — symptom: a percentage that averages per-row percentages, so a 1-for-1 night counts like a 12-for-25 night (source: `bug-taxonomy.md#averaged-ratio`). Fix: rewrite as weighted `SUM/SUM`; prove it via [ground-a-metric](ground-a-metric.md).
- **Modeling what the engine can't yet support** — symptom: a metric needs a window function (`LAG`, rolling window) the platform doesn't support, so it silently computes wrong or won't build. Fix: don't fake it — record it as a pending limitation (source: `nba-demo-audit-sv2/PENDING_COMPLEX_QUESTIONS.md`) and add it when support lands.

**Takeaway** — **build core-first entity by entity, write every ratio as SUM/SUM, and don't call it built until the Lynk build compiles at the consumption surface — then hand it to the audit to ground its metrics true.**

**Example** *(real — the shipped networx layer, `networx-semantic-layer-2026-07-09.zip`)* — a built layer in exactly this shape: a `core` shared domain holding entities (`sale`, `inquiry`, `bill`, `payment`, `lead`, …), each an entity folder with its own `ENTITY.md` (prose) and `schema.yml` (structure), plus `policies/` and a `text-to-sql` skill, and a second `operations` domain building on core. It is the target shape steps 1–5 produce.

**In this system** — this is the "build" arc of [the frame](the-frame.md); its output is the input to [audit-a-layer](audit-a-layer.md), and any defect the audit returns is resolved by [fix-a-finding](fix-a-finding.md). For every "what must this primitive be?" question, point to Docs v2 — this recipe owns the *ordering and discipline of construction*, not the spec.

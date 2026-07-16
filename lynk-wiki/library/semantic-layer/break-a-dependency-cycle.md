---
type: recipe
description: Fix the compile-time cross-entity cycle — detect the loop the build reveals but static resolution hides, pick the back-edge to cut, source the field from the entity's own columns, and rebuild green.
---

# Break a dependency cycle

**What it is** — the specific fix for the one defect that passes every proxy surface and only the build can catch: two (or more) entities that reference each other's metrics/features, forming a compile-time loop so neither can emit its CTE. This recipe owns the **cycle-breaking method**; the class signature and one-line fix live in `.claude/skills/semantic-layer-audit/references/bug-taxonomy.md#cross-entity-cycle` (the one home), and *why* the lower surfaces miss it is Book 6's principle (→ See the Evals book · `verify-at-the-authoritative-surface`) — this page does not re-derive either.

**Prerequisites**
- A layer whose **Lynk build fails** with `CTE … does not exist` and cascaded "metric not found," while static ref-resolution and raw-warehouse queries pass — the false-green signature (source: `docs/semantic-layer-build-cycle-2026-07-12.md`; `bug-taxonomy.md#cross-entity-cycle`).
- Read access to the entity **`schema.yml`** files, where the cross-entity references (`metric()` / `join_name`) live — the cycle is confirmed by reading them, not by static resolution (source: incident doc, "Cycle confirmed by reading the schemas").
- Access to the **compiled Lynk build** to re-probe after the cut (→ See the Evals book · `verify-at-the-authoritative-surface`).
- **Human approval** — this is a fix, so it runs under the one-at-a-time gated loop → See [fix-a-finding](fix-a-finding.md).

**Steps** (one observable outcome each)
1. **Detect the loop.** The build fails though every reference resolves statically; trace the referenced fields across entities until you find the cycle — A's field depends on B's field, which depends back on A's (source: incident doc, root cause). → *Outcome:* the cycle is written out as a directed chain of `entity.field → entity.field` edges.
2. **Pick the back-edge to cut.** Choose the single edge that closes the loop — the round-trip reference that can be replaced by the entity's own data. Cut one edge, not both, so the remaining direction stays intact. → *Outcome:* one edge selected as the one to remove.
3. **Source the field from the entity's own columns.** Replace the cross-entity round-trip with a definition computed from the entity's own backing columns, so the field no longer depends on the other entity (source: `bug-taxonomy.md#cross-entity-cycle`, "source the field from an entity's own columns instead of a round-trip"). → *Outcome:* the back-edge is gone; the field is defined locally.
4. **Rebuild & probe.** Re-run the Lynk build probe. → *Outcome:* every entity emits its CTE and the cascaded "metric not found" errors are gone.

**Verification**
- The **Lynk build compiles green** — both formerly-cyclic entities emit their CTEs and the downstream field probes that cascaded now resolve (source: incident doc, "Only the build … exercises CTE emission, where the cycle lives").
- **No new cycle** was introduced — re-run structural cycle detection (the audit's Phase 1 covers cross-entity loops; → See [audit-a-layer](audit-a-layer.md)).
- The relocated field still **grounds true** — its number matches its external anchor after being sourced locally (→ See [ground-a-metric](ground-a-metric.md)); breaking the cycle must not change the value it should compute.

**Failure modes** (symptom → fix/escape)
- **Trusting static resolution** — symptom: "every reference resolves, so there's no cycle." Static resolution checks that a *name* resolves, not that an entity *builds*; the failing metric names existed in the files (source: incident doc, "Why the proxies missed it"). Fix: only the build reveals the cycle — probe there.
- **Cutting both edges** — symptom: removing every cross-entity reference to be safe, losing a legitimate relationship. Fix: cut exactly one back-edge; the loop breaks when one direction is removed.
- **Re-introducing the loop elsewhere** — symptom: the local definition quietly references the other entity again through a different path, so the build fails the same way. Fix: source strictly from the entity's own columns and re-run cycle detection (step: Verification).
- **Fixing the value while breaking the cycle** — symptom: the relocated field now computes a different number. Fix: re-ground it against its anchor (→ See [ground-a-metric](ground-a-metric.md)) — a compile fix must be value-neutral.

**Takeaway** — **a build-only cycle breaks by cutting one back-edge and sourcing that field from the entity's own columns — never both edges, never trusting static resolution, and always re-grounding the relocated field so the compile fix stays value-neutral.**

**Example** *(real — `docs/semantic-layer-build-cycle-2026-07-12.md`)* — `player_game.team_minutes_in_game` referenced `team_game.team_minutes_played`, which referenced `metric(player_game.total_minutes_played)` — a loop, so neither `LYNK__CTE_PLAYER_GAME` nor `LYNK__CTE_TEAM_GAME` could emit and dozens of probes cascaded to "metric not found" (telemetry: Logfire, service `sql-api-v2`, trace `019f5568…70d18c`, build/failure breakdown by Tom Harpaz). The fix: break the `team_game → player_game` back-edge and source `team_minutes_played` from `team_game`'s own columns, then rebuild — the CTEs emit and the cascade clears.

**In this system** — this is the highest-value single fix in the "fix" arc of [the frame](the-frame.md), a specialization of [fix-a-finding](fix-a-finding.md) for the cross-entity-cycle class. Book 6 owns *why* the proxy surfaces miss it (false green); the skill's `bug-taxonomy.md` owns the class definition; this page owns the *how-to-cut*. → See [build-a-layer](build-a-layer.md), whose cycle failure mode points here.

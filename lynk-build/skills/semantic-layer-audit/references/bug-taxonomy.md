# Bug taxonomy — issue classes, how to detect, how to fix

The recurring ways a semantic layer is wrong. Two families:
**A — value-correctness** (a *wrong number* that passes every structural rule; prove with warehouse
execution + an external anchor) and **B — structure/build** (the Lynk *build* rejects it; prove with
the build, never raw SQL). Each entry: **signature · detect · fix**.

> This is the one authoritative home for the issue classes. The skill, gate-rules, and file-rubric
> point here; do not re-enumerate them elsewhere.

---

## A. Value-correctness classes  (prove by running SQL vs an external anchor)

### averaged-ratio
- **Signature:** a percentage/rate aggregated as `AVG(per_row_pct)` instead of `SUM(num)/SUM(den)`.
- **Detect:** run both forms; compare to a known-true value. Jokić 3P% weighted **36.5%** vs averaged
  (0-attempt games as 0%) **30.5%**; Curry FT% **0.907** vs averaged **0.672**. Magnitude is data-dependent — re-derive, never quote.
- **Fix:** replace with weighted `SUM(numerator)/NULLIF(SUM(denominator),0)`, and decide 0-denominator handling explicitly.

### scale-mismatch-threshold
- **Signature:** a boolean/tier compares a value against a constant in the *wrong units*.
- **Detect:** compute the feature's real distribution; check the constant lands inside it (`is_efficient_scorer >= 55` vs a 0–1 value).
- **Fix:** put the threshold in the feature's units (0–1 vs 0–100), or rescale the feature — and keep one scale convention across the layer.

### description-vs-sql-lie
- **Signature:** the description promises X; the SQL computes Y. Both individually valid.
- **Detect:** read description against SQL, then run it (`usage_rate_estimate` labelled "USG%"; `net_rating` = home-margin not off−def; off==def rating).
- **Fix:** make the SQL compute what the description says, or correct the description to the SQL — whichever is the truth (confirm against reality).

### unbacked-or-mislabelled-metric
- **Signature:** fully defined but no data computes it, or it names the wrong real-world thing.
- **Detect:** trace the SQL to a real column; verify the label against a cited source (PER/BPM with no data; `season_mvp` as Finals award — it's regular-season).
- **Fix:** point at a real backing column or remove it; correct mislabels against the source.

### ambiguity
- **Signature:** undefined "recent/active/top", unexplained columns, a metric readable two ways.
- **Detect:** judgment (a calibrated reviewer) — mark judgment-only + cite the book.
- **Fix:** define the term/column; commit to one meaning.

---

## B. Structure / build classes  (prove with the Lynk build — raw SQL gives false green)

### domain-duplicate-metric-name
- **Signature:** the same **metric** name on 2+ entities in a domain (features are per-entity, so they don't collide).
- **Detect:** build → "Duplicate metric name '…' in domain 'core' — defined on X, Y." (~40% of the nba-demo errors.)
- **Fix:** rename **entity-qualified** *and* give each a **distinguishing description** — not a bare dedupe:
  `player_total_points` ("…by the player…") / `team_total_points` ("…by the team…") / `teams_combined_total_points`.

### within-entity-duplicate
- **Signature:** the same name twice in one entity — including an **import** plus a **local** metric.
- **Detect:** build → "duplicate name '…' — defined as a metric and an import."
- **Fix:** remove one — usually the redundant local copy of an already-imported metric.

### metric-references-another-entity
- **Signature:** a metric's SQL reaches into a different entity.
- **Detect:** build → "a metric is entity-local and cannot reference another entity."
- **Fix:** define it on the owning entity and pull across via a relationship/feature, or `metric()` on the correct entity.

### broken-relationship-target
- **Signature:** relationship final-step ≠ declared entity; a step target isn't an entity; a join references an undeclared field.
- **Detect:** build → relationship errors (`coach …_by_coaching_staff` final step ≠ declared; `finance_player_to_player_team` target not an entity).
- **Fix:** correct the declared entity/target/join to real, declared things; for cross-domain, import properly per topology.

### cross-entity-cycle
- **Signature:** two entities reference each other (via `join_name`/`metric()`), a dependency loop. Passes static resolution AND raw SQL.
- **Detect:** build → `CTE … does not exist`, then downstream "metric not found" cascade. `player_game.team_minutes_in_game → team_game.team_minutes_played → metric(player_game.total_minutes_played)`.
- **Fix:** break one back-edge — source the field from an entity's **own** rows (e.g. a window over its own grain) instead of a round-trip.

### nested-aggregate
- **Signature:** an aggregate inside an aggregate — `AVG(COUNT(DISTINCT …))`, `SUM(COUNT(…))`.
- **Detect:** build → "Aggregate functions cannot be nested."
- **Fix:** pre-aggregate once (a feature/subquery at the right grain), then aggregate a single level.

### unbacked-warehouse-column   *(OTHER-SIDE — not a layer typo)*
- **Signature:** SQL references a source column the warehouse doesn't have.
- **Detect:** build → "cannot be queried" (`instagram_url`/`facebook_url`/`twitter_url`).
- **Fix:** **hand off** — the DB adds the column, or drop the feature. A product/data decision, not ours to invent.

---

## C. Distinguishability  (cross-cutting)
Two things an agent must choose between need **distinct names AND distinct descriptions**.
- **Detect:** same/near name, or identical description, across metrics (`player_game`/`team_game` `total_points` both "Total points scored across all games").
- **Fix:** qualify the name by entity/meaning **and** write a description that says which one it is.

## Anchoring rule (for family A — how to pick the "known truth")
Externally sourced, never generated by the SQL under test (circular — see gate-rules `anchor-external`):
1. a curated truth table · 2. a sanity invariant (`0 ≤ pct ≤ 100`; parts sum to total) · 3. a hand-computed value.

## Which surface proves which family
Family **A** → warehouse execution + external anchor. Family **B** → the **Lynk build** (authoritative);
static ref-resolution and raw SQL pass green while the build is red (see book-6 `verify-at-the-authoritative-surface`).

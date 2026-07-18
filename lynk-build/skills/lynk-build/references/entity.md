# Entity — add a new entity

The playbook for modeling a new entity. Share the plan first, then update the user step by
step as a todo list. Steps 4.1–4.3 can run in parallel with subagents (feature import,
query-history mining).

## 1. Name it

Ask what the entity is called — the thing in the business (customer, order, subscription).

## 2. Find the key source

Ask **which table is the key source** for this entity. Explain it simply: the key source is
the warehouse table where **one row = one <entity>** — its unique key becomes the entity's
key. Offer to **search the warehouse and suggest** if they're not sure.

## 3. If they want you to search

- **Prefer the sources flow (`references/sources.md` — the catalog) for the search**: list sources, match by **table
  name**, read the descriptions and reported keys. Fall back to direct warehouse metadata
  only if the catalog can't answer (offer a sync first — a new table won't appear until one
  runs).
- Sanity-check **cardinality** (does the row count make sense for "one row per <entity>"?).
- **Verify the key is unique** (`COUNT(*)` vs `COUNT(DISTINCT key)`) and that it makes sense
  as the entity key — the full procedure (max 3 candidates, escalate if none verify) is in
  the skill's Step 5; it's canonical.
- Present your suggestion with the evidence, get a confirmation before building.

## 4. Build the entity (`ENTITY.md` + `schema.yml` in the domain)

1. **Import the features from the key source** — its columns become the entity's features.
2. **Search the query history** for real queries involving the key source table (see the
   Snowflake reference — exclude informational queries). The SQL patterns you find drive the
   next three steps:
   1. **1:1 tables → relationships + selective feature import.** Tables that join 1:1 on the
      key are 1:1 relationships. Import features from them **only if they're really in use**
      in the SQL patterns — not everything.
   2. **Add relationships** for the other join patterns you find, with the right cardinality.
   3. **Add metrics** — the aggregations the SQL history actually runs on top of this entity.
   4. **Ask for specific BI dashboards** where this entity's metrics live. If provided,
      extract the relevant metrics from them.

Done: entity has a verified key, real features, relationships and metrics grounded in actual
usage. Suggest validating what you built.

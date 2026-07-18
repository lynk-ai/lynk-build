# Lynk docs — navigation guide

How skills should walk the Lynk docs. The docs ship **bundled with this plugin** at
`${CLAUDE_PLUGIN_ROOT}/semantics_docs/` — the `semantics_v2` doc tree, rendered into the
plugin. `Read` them directly; there is **no network fetch and no local clone** to
manage. Never fetch `docs.getlynk.ai` for semantics content — it still serves the
outdated v1 docs.

The skills inline the specific paths they read (so each step is atomic and
self-contained); this file is the convention they follow.

## Where the docs live

All pages are under `${CLAUDE_PLUGIN_ROOT}/semantics_docs/<path>` — e.g.
`${CLAUDE_PLUGIN_ROOT}/semantics_docs/concepts/entity/README.md`. Use `Read` (not
`WebFetch`); the content is identical to the `semantics_v2` branch it was rendered from.

## The two anchors

Skills ground themselves with two pages:

- **`SUMMARY.md`** (`${CLAUDE_PLUGIN_ROOT}/semantics_docs/SUMMARY.md`) — the docs index
  (table of contents). Lists every page available. Use it to discover the leaf path you need.
- **`concepts/README.md`** (`${CLAUDE_PLUGIN_ROOT}/semantics_docs/concepts/README.md`) —
  Lynk's core vocabulary (Project, Domain, Entity, Feature, Metric, Relationship, Glossary,
  Policy, Skill, Reference Files). Read it before answering or building anything that involves
  Lynk primitives.

Everything else is a leaf reached from the index. The tree at a glance: `concepts/` holds the
concept and file-type specs (`concepts/entity/entity-md.md`, `concepts/entity/schema-yml/…`,
`concepts/lynk-md.md`, `concepts/glossary.md`, …), `reference/` holds format and naming rules
(`layout-and-naming.md`, `markdown-format.md`, `sql-expressions.md`, `best-practices.md`), and
`api/` holds `lynk-sql.md` and a REST API stub (the full REST reference for these skills is
`${CLAUDE_PLUGIN_ROOT}/references/rest-api.md`, bundled with the plugin).

## How to walk

1. **Start at the index.** `Read` `${CLAUDE_PLUGIN_ROOT}/semantics_docs/SUMMARY.md` to see the
   current tree. Never guess a leaf path from memory.
2. **Pick the narrowest leaf** that answers your question (e.g.,
   `concepts/entity/schema-yml/metric.md`, `reference/sql-expressions.md`). Do not pre-read
   unrelated pages — context cost compounds.
3. **Read only that leaf** under `${CLAUDE_PLUGIN_ROOT}/semantics_docs/`. If you need a second
   one, read it explicitly. No bulk traversal.

## When the docs move

Leaf paths may change when the bundle is re-rendered from a newer `semantics_v2`. If a `Read`
fails:

1. Re-read `${CLAUDE_PLUGIN_ROOT}/semantics_docs/SUMMARY.md` and find the new path.
2. Update the skill that pointed to the old path.

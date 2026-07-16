---
name: lynk-wiki
description: Placeholder skill. Use when working with the Lynk semantic layer — answers questions using the bundled semantics docs.
---

# Lynk Wiki

Placeholder. Point Claude at the docs bundled with this plugin:

- `${CLAUDE_PLUGIN_ROOT}/semantics_docs/README.md` — start here
- `${CLAUDE_PLUGIN_ROOT}/semantics_docs/SUMMARY.md` — full table of contents
- `${CLAUDE_PLUGIN_ROOT}/semantics_docs/concepts/` — core concepts
- `${CLAUDE_PLUGIN_ROOT}/semantics_docs/reference/` — reference material
- `${CLAUDE_PLUGIN_ROOT}/semantics_docs/api/` — API docs

## Lanes (added by the lynk-book integration — review welcome)

Two knowledge surfaces ship in this plugin; use the right lane:

- **This skill / `semantics_docs/` — the WHAT**: Lynk syntax, file formats,
  fields, API reference. Pure "how does Lynk work" questions end here.
- **`lynk-wiki:library` — the HOW**: design methodology, metric safety,
  entity-split judgment, verification recipes. Invoke it BEFORE creating,
  updating, or editing any semantic-layer artifact — the docs give the
  format, the library gives the judgment.

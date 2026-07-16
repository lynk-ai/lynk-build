# lynk-build

A Claude Code plugin marketplace for Lynk.

## Plugins

| Plugin | Description |
|--------|-------------|
| `lynk-wiki` | Lynk semantic layer documentation, skills, and subagents for building with Lynk. |

## Installation

Add the marketplace, then install the plugin — from inside Claude Code:

```
/plugin marketplace add lynk-ai/lynk-build
/plugin install lynk-wiki@lynk-build
```

Working from a local clone instead:

```
/plugin marketplace add /path/to/lynk-build
/plugin install lynk-wiki@lynk-build
```

Manage installed plugins anytime with `/plugin`.

## Auto-update

Auto-update is off by default for third-party marketplaces and there is no install flag for it. To enable it once after installing: `/plugin` → **Marketplaces** → select `lynk-build` → **Enable auto-update**. Updates then apply on the next session (or `/reload-plugins`). To update manually instead, run `/plugin marketplace update lynk-build`.

## lynk-wiki layout

```
lynk-wiki/
├── library/          # 6 gate-verified books from lynk-book (read-only)
├── semantics_docs/   # Lynk semantics docs (README, SUMMARY, api, concepts, reference)
├── skills/           # library (pipeline) · bk-search · semantic-layer-audit · lynk-wiki
├── subagents/        # librarian (router/orchestrator) · book-reader (scout) · lynk-docs-expert
├── hooks/            # session note · pointer fetch · semantic router · layer-write nudge
├── scripts/          # the hook scripts
└── bk                # library CLI (read-only in this bundle)
```

The books: `best-context` · `progressive-disclosure` · `skills` · `subagents` ·
`evals` · `semantic-layer`. (In the authoring repo they carry numbered IDs;
shipped names drop the prefix.)

**Environment contract:** `CLAUDE_PLUGIN_ROOT` → where books + `bk` live;
`BK_DATA` (set by the hooks) → the consumer project's `.bk/` for ALL state
(reads log, gaps, fetch files) — the plugin folder is never written to. When
the librarian can't answer, demand is recorded in the consumer's
`.bk/gaps.jsonl` — collect those; they are the library's writing backlog.

## The two knowledge lanes

- **`semantics_docs/` — the WHAT**: Lynk syntax, formats, fields, API reference.
- **`library/` — the HOW**: build methodology, metric safety, verification recipes,
  agent/eval design. The plugin's hooks steer every semantic-layer change to consult
  BOTH lanes before acting; pure "how does Lynk work" questions use the docs only.

Books are rendered from the [lynk-book](../lynk-book) authoring repo and are
read-only here — `bk` refuses writes beside the hidden `.bundle-version` marker
(which also records exactly which lynk-book commit the books came from). To
update the books, render a new bundle there and bump the plugin version.

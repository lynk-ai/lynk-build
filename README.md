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
├── library/          # 6 gate-verified books from lynk-book (read-only; see BUNDLE_VERSION)
├── semantics_docs/   # Lynk semantics docs (README, SUMMARY, api, concepts, reference)
├── skills/           # library (pipeline) · bk-search · semantic-layer-audit · lynk-wiki
├── subagents/        # librarian (router/orchestrator) · book-reader (scout) · lynk-docs-expert
├── hooks/            # session note · pointer fetch · semantic router · layer-write nudge
├── scripts/          # the hook scripts
├── bk                # library CLI (read-only in this bundle)
├── BUNDLE_VERSION    # provenance: which lynk-book commit the books were rendered from
└── INTEGRATION.md    # how the pieces fit + the env contract
```

## The two knowledge lanes

- **`semantics_docs/` — the WHAT**: Lynk syntax, formats, fields, API reference.
- **`library/` — the HOW**: build methodology, metric safety, verification recipes,
  agent/eval design. The plugin's hooks steer every semantic-layer change to consult
  BOTH lanes before acting; pure "how does Lynk work" questions use the docs only.

Books are rendered from the [lynk-book](../lynk-book) authoring repo and are
read-only here — `bk` refuses writes beside the `BUNDLE_VERSION` marker. To update
the books, render a new bundle there and bump the plugin version.

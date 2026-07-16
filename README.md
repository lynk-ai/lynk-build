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
├── books/            # curated books (empty for now)
├── semantics_docs/   # Lynk semantics docs (README, SUMMARY, api, concepts, reference)
├── skills/           # Claude Code skills
└── subagents/        # Claude Code subagents
```

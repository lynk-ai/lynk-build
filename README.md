# lynk-build

A Claude Code plugin marketplace for Lynk. Its one plugin, **`lynk-build`**, is the Lynk
**build agent** — it installs into a customer's semantic-layer repo and helps a data analyst
build, maintain, and audit their `.lynk/` layer so it **passes build** and **integrates with
their data sources**.

## Plugins

| Plugin | Description |
|--------|-------------|
| `lynk-build` | The Lynk build agent: skills, bundled docs, and subagents for building and maintaining a Lynk semantic layer. |

## Installation

Add the marketplace, then install the plugin — from inside Claude Code:

```
/plugin marketplace add lynk-ai/lynk-build
/plugin install lynk-build@lynk-build
```

Working from a local clone instead:

```
/plugin marketplace add /path/to/lynk-build
/plugin install lynk-build@lynk-build
```

Manage installed plugins anytime with `/plugin`.

## What the build agent gives you

- **An always-on operating contract** — injected at session start (see `hooks/operating-contract.md`):
  the build-agent persona, plain-language translation for non-engineers, Linear-as-system-of-record,
  and the branch/PR discipline. No skill invocation needed.
- **Build & ask skills** — `lynk-build` (add/edit/model entities, features, metrics, relationships,
  glossary; validate and evaluate flows), `lynk-ask` (answer questions about Lynk and the layer).
  Both ground themselves in the **bundled** docs — no network fetch.
- **Data-source & tool integrations** — the `integrations` skill front-doors Snowflake (repo-level
  MCP, read-only), plus Linear, Slack, and Notion (claude.ai hosted connectors). Each ships a
  usage + setup reference; setup is per-customer.
- **A research-only library + deep audit** — the `lynk-research` pipeline (a librarian picks the
  relevant books, scholars read the right chapters; grounded, cited, cheap) and the
  `semantic-layer-audit` skill (whole-layer, execution-grounded audit).

## Auto-update

Auto-update is off by default for third-party marketplaces and there is no install flag for it. To enable it once after installing: `/plugin` → **Marketplaces** → select `lynk-build` → **Enable auto-update**. Updates then apply on the next session (or `/reload-plugins`). To update manually instead, run `/plugin marketplace update lynk-build`.

## lynk-build layout

```
lynk-build/
├── hooks/            # hooks.json · operating-contract.md (SessionStart contract) · enrich_subagent.py (library content injector)
├── scripts/          # hook scripts · operating-contract.sh · lynk_api.py
├── bin/              # on PATH for the library skills: generate_library_index · generate_book_toc · populate_chapters
├── references/       # shared refs: content-rules · lynk-docs (bundled-docs nav) · rest-api
├── semantics_docs/   # Lynk semantics docs (README, SUMMARY, api, concepts, reference) — grounding source
├── library/          # research-only book library (index.md + chapters/NN-*.md) — see library/README.md
└── skills/           # lynk-build · lynk-ask · integrations · semantic-layer-audit · lynk-research · librarian · scholar
```

**The library pipeline:** `lynk-research` (router) enriches the question and calls the
`librarian` skill; the librarian selects books from the injected catalog and dispatches one
`scholar` per book to read the right chapters; a `PostToolUse` hook (`enrich_subagent.py`, gated on
the librarian) materializes the selected chapters' content into the router's context — cited as
`book · chapter`. The catalog and each book's TOC are injected at skill **load time** via the
`bin/` scripts, so the maps cost zero model tool calls. Add books under `library/` — see
`library/README.md`.

**Environment contract:** `CLAUDE_PLUGIN_ROOT` → where the plugin's files live (docs, references,
scripts, `bin/`, `library/`). Skills read the bundled docs at `${CLAUDE_PLUGIN_ROOT}/semantics_docs/`
and run `lynk_api.py` from the **customer** project root (so it resolves the customer's `.env`/`.lynk`).

## The two knowledge lanes

- **`semantics_docs/` — the WHAT**: Lynk syntax, formats, fields, API reference.
- **`library/` — the HOW**: build methodology, metric safety, verification recipes,
  agent/eval design. The `lynk-build` skill owns the build methodology; the hooks steer every
  semantic-layer change through it, and it draws on the `lynk-research` library for deeper
  methodology. Pure "how does Lynk work" questions use the docs only (or `lynk-ask`).

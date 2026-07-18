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
- **A methodology library + deep audit** — the `library` pipeline (build methodology, metric safety,
  verification) and the `semantic-layer-audit` skill (whole-layer, execution-grounded audit).

## Auto-update

Auto-update is off by default for third-party marketplaces and there is no install flag for it. To enable it once after installing: `/plugin` → **Marketplaces** → select `lynk-build` → **Enable auto-update**. Updates then apply on the next session (or `/reload-plugins`). To update manually instead, run `/plugin marketplace update lynk-build`.

## lynk-build layout

```
lynk-build/
├── hooks/            # hooks.json + operating-contract.md (SessionStart contract)
├── scripts/          # hook scripts · operating-contract.sh · lynk_api.py · bk (library CLI)
├── references/       # shared refs: content-rules · lynk-docs (bundled-docs nav) · rest-api
├── semantics_docs/   # Lynk semantics docs (README, SUMMARY, api, concepts, reference) — grounding source
├── library/          # 6 gate-verified methodology books from lynk-book (read-only)
├── skills/           # lynk-build · lynk-ask · integrations · library (pipeline) · bk-search · semantic-layer-audit
└── subagents/        # librarian (router/orchestrator) · book-reader (scout)
```

The books: `best-context` · `progressive-disclosure` · `skills` · `subagents` ·
`evals` · `semantic-layer`. (In the authoring repo they carry numbered IDs;
shipped names drop the prefix.)

**Environment contract:** `CLAUDE_PLUGIN_ROOT` → where the plugin's files live (docs, references,
scripts, books, `bk`); `BK_DATA` (set by the hooks) → the consumer project's `.bk/` for ALL
library state (reads log, gaps, fetch files) — the plugin folder is never written to. When the
librarian can't answer, demand is recorded in the consumer's `.bk/gaps.jsonl` — collect those;
they are the library's writing backlog. Skills read the bundled docs at
`${CLAUDE_PLUGIN_ROOT}/semantics_docs/` and run `lynk_api.py` from the **customer** project root
(so it resolves the customer's `.env`/`.lynk`).

## The two knowledge lanes

- **`semantics_docs/` — the WHAT**: Lynk syntax, formats, fields, API reference.
- **`library/` — the HOW**: build methodology, metric safety, verification recipes,
  agent/eval design. The `lynk-build` skill owns the build methodology; the hooks steer every
  semantic-layer change through it, and it draws on the library for deeper methodology. Pure
  "how does Lynk work" questions use the docs only (or `lynk-ask`).

Books are rendered from the [lynk-book](../lynk-book) authoring repo and are
read-only here — `bk` refuses writes beside the hidden `.bundle-version` marker
(which also records exactly which lynk-book commit the books came from). To
update the books, render a new bundle there and bump the plugin version.

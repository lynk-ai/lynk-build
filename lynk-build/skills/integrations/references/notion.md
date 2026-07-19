# Notion — usage

Notion is the team's docs and wiki connection — use it to find business knowledge that
feeds the semantic layer: glossary terms, metric definitions, process docs, onboarding
pages, meeting notes.

If Notion isn't connected, see `notion-setup.md`.

## Scope — the project's designated space ONLY (hard rule)

**Only documents inside the project's designated Notion workspace/teamspace/page tree — the
one chosen during setup (see `notion-setup.md`) — may be read, searched, fetched, or
referenced. Never touch, read, or surface any other Notion content — even if the connection
can technically see it.**

- When searching, scope the search to the designated space (via `teamspace_id` / `page_url`
  once its ID is known) rather than searching the whole workspace.
- If a workspace-wide search is unavoidable, discard and do not read any result that is
  not under the designated space.
- If content the user needs appears to live outside the designated space, stop and ask — do
  not fetch it on your own.

Ask the user to also enforce this at the source (Notion → Settings → Connections → Claude →
page access limited to the designated space). Until that restriction is in place, this context
rule is the only guardrail. Once the space is shared, record its ID/URL during setup.

## What you can do

Once the Notion connector is active, its actions are available as tools. The common ones:

- **Search:** semantic search across the workspace (`notion-search`) — the default way to
  find a doc when the user mentions "our wiki" / "the metrics doc" / "that Notion page".
- **Read:** fetch a page or database in full (`notion-fetch`) once search finds it; query
  databases and views for structured content.
- **Write:** create or update pages, add comments. Writing is **visible to the whole
  team** — show the user exactly what you'll create/change and get a clear go-ahead first.
  Reading and searching are safe and need no confirmation.

## How it relates to the semantic layer

Notion is **source material**, not the system of record: definitions found there get
distilled into `.lynk/` (glossary, `LYNK.md`, entity docs) — always tell the user where a
definition came from (link the page). Work tracking stays in Linear; a Notion doc never
represents task status.

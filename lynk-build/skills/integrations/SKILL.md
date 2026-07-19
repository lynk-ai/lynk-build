---
name: integrations
description: >
  Single entry point for every external system this project talks to — Snowflake (the data
  warehouse), Linear (work tracking), Slack (team chat), Notion (team docs & wiki), and any
  integration added later.

  Use this skill whenever the user wants to use, query, connect to, set up, configure,
  re-connect, troubleshoot, list, or add an integration — even when they don't say the word
  "integration." Triggers include: "query Snowflake", "what tables do we have", "the Snowflake
  connection is broken", "set up Snowflake", "create a Linear issue", "log this in Linear",
  "what integrations do we have", "connect Slack", "post this to Slack", "add a Notion
  integration", "how do I use X". When in doubt about which external tool the user means or how
  to reach it, start here — this skill routes to the right one and is the source of truth for
  how each is wired up. The audience is data analysts, not engineers: explain plainly and never
  dump raw config or errors on them.
---

# integrations

This is the **one front door** for all of the project's external connections. Rather than
keeping the details of every system loaded at once, this skill stays small and **routes** you
to the single integration the user actually needs — then you open that integration's own notes
*just in time*.

## How to use this skill (progressive disclosure)

Don't read every reference file. Work in three quick steps:

1. **Identify the integration.** From what the user said, pick one row in the table below.
   If it's genuinely unclear, ask a short either/or question ("Do you mean the Snowflake data
   or the Linear work tracker?").
2. **Decide: first-time setup, or everyday use?**
   - If it's not connected yet, or the user says "set up / connect / it's broken" → read the
     **Setup** file.
   - If they just want to *do* something with it → read the **Usage** file.
3. **Read only the matching file(s)** for that one integration, then follow them. Report back
   in plain language — translate any config/CLI/error details into something an analyst can act
   on (per the project's "speak plainly" rule).

That's the whole point: the user gets focused, relevant context for exactly the integration in
front of them, and nothing else clutters the conversation.

## Available integrations

| Integration | What it's for | How it connects | Usage | Setup / first use |
| --- | --- | --- | --- | --- |
| **Snowflake** | The customer's data warehouse (location in `config.json` at the repo root). Read-only. | Local MCP server in the repo's `.mcp.json` | `references/snowflake.md` | `references/snowflake-setup.md` |
| **Linear** | Work tracking — the system of record; scoped to the customer's team board (set during setup). | claude.ai hosted connector | `references/linear.md` | `references/linear-setup.md` |
| **Slack** | Team chat — search and post messages. | claude.ai hosted connector | `references/slack.md` | `references/slack-setup.md` |
| **Notion** | Team docs & wiki — source material for glossary terms and business knowledge. | claude.ai hosted connector | `references/notion.md` | `references/notion-setup.md` |

None of these are wired up on a fresh install — each needs a **one-time per-customer setup**,
described in its Setup file. There are two shapes: **Snowflake** is a repo-level MCP server the
customer registers in `.mcp.json` (see `references/snowflake-setup.md`); **Linear**, **Slack**,
and **Notion** are **claude.ai hosted connectors** the customer enables in their claude.ai
account (Settings → Connectors, or via `/mcp`). The plugin cannot register any of them for the
customer — it documents how. Once connected, each surfaces its actions as tools you call directly.

## A note on how these connect

All of these are **MCP servers** — the mechanism Claude Code uses to talk to outside tools; once a
server is connected, its actions show up as tools you call directly (e.g. running a Snowflake
query, creating a Linear issue). MCP servers are read at **startup**, so after any config change —
or after registering Snowflake in `.mcp.json`, or enabling a claude.ai connector — restart Claude
Code (or `/mcp` reconnect for a hosted connector) so the new tools load. Each Setup file says
exactly what's needed.

**Linear is the operating contract's system of record.** The contract's task-tracking and
publish workflow can't run until Linear is connected — so if the user wants that workflow and
Linear isn't available yet, enable it first via `references/linear-setup.md`.

## Adding a new integration

The whole design is meant to grow. To add one (say, Notion):

1. Create `references/notion.md` (how to use it day to day) and `references/notion-setup.md`
   (how to connect it the first time). Keep each focused on that one system.
2. Add a row to the **Available integrations** table above pointing at those two files.
3. If it needs credentials, follow the same secrets pattern Snowflake uses (see
   `references/snowflake-setup.md`): secrets in the gitignored repo-root `.env`, loaded by a
   small launcher script, never committed.

Keeping every integration to the same shape — one usage file, one setup file, one table row —
is what lets this single skill stay the reliable front door no matter how many systems get
added.

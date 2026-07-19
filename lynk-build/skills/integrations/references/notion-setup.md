# Notion — first-time setup

Notion is reached via a **claude.ai hosted connector** (like Linear and Slack) — nothing to
install, no script, no secrets file, nothing in `.mcp.json`. Access rides on the user's
claude.ai account.

Setup is just authorizing access:

1. In claude.ai → **Settings → Connectors**, add/enable **Notion** (or run `/mcp` in
   Claude Code and pick the Notion server if it shows as pending).
2. A browser window opens for Notion's OAuth login — approve the workspace and the pages
   Notion should share.
3. Back in the session, Notion tools (`notion-search`, `notion-fetch`, …) become available.

**Verify:** run a harmless read — e.g. list teamspaces (`notion-get-teams`) or search for
any page. Real results back = working. (Verifying with a *read* avoids creating anything
by accident.)

If it stops working later, it's almost always the login expiring or page-sharing scope —
re-authenticate via claude.ai Connectors, and check that the pages you need are shared
with the connector in Notion's settings.

**Pick the space.** Ask the user which Notion workspace/teamspace this project should use, and
limit the connector's page access to it in Notion's settings. Record its name and ID/URL here;
everything in `notion.md` is scoped to that designated space.

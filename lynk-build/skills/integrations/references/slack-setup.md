# Slack — first-time setup

Slack is a **claude.ai hosted connector** — no script, secrets file, or repo config to manage,
and nothing to register in `.claude/settings.json`. Access rides on the user's claude.ai account.
Setup is: enable the connector, then authorize it.

1. In **claude.ai → Settings → Connectors**, enable the **Slack** connector (if it isn't
   already). This is done once per claude.ai account, not per repo.
2. In Claude Code, run `/mcp` and select **slack**.
3. If it's pending/unauthenticated, choose to authenticate — a browser window opens for Slack's
   **OAuth** login. Approve the requested workspace and scopes there.
4. Back in Claude Code, the server shows connected with a tool count.

**Pick the channel.** Work for this project stays in one dedicated channel. Ask the user which
Slack channel to use; everything in `slack.md` is scoped to it.

**Verify:** ask it to search for a recent message or list channels — if real results come back,
it's working. (Verifying with a *read* avoids posting anything by accident.)

If it stops working later, it's almost always the login expiring — re-run `/mcp` and
re-authenticate. There are no credentials in `.env` for Slack.

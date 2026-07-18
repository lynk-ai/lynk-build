# Linear — first-time setup

Linear is a **claude.ai hosted connector** — there's no script, secrets file, or repo config to
manage, and nothing to register in `.claude/settings.json`. Access rides on the user's claude.ai
account. Setup is: enable the connector, then authorize it.

1. In **claude.ai → Settings → Connectors**, enable the **Linear** connector (if it isn't
   already). This is done once per claude.ai account, not per repo.
2. In Claude Code, run `/mcp` and select **linear**.
3. If it shows as pending/unauthenticated, choose to authenticate — a browser window opens for
   Linear's **OAuth** login. Approve access there.
4. Back in Claude Code, the server shows connected with a tool count.

**Pick the team.** Linear work for this project lives on one team/board. Ask the user which
Linear team to use and note its issue prefix (e.g. `ABC`); everything in `linear.md` is scoped
to that team. Confirm by listing that team's open issues — if real items come back, it's working.

This connector satisfies the operating contract's **Linear = system of record** dependency: the
contract's task-tracking and publish workflow can't run until Linear is connected here.

If it ever stops working, it's almost always the login expiring — re-run `/mcp` and
re-authenticate. There are no credentials in `.env` for Linear.

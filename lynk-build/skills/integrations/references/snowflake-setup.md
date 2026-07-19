# Snowflake — first-time setup

Goal: a **read-only** Snowflake connection whose secrets never get committed. The pieces:

```
.env                                   ← credentials, repo root, gitignored
.claude/snowflake/run-snowflake-mcp.sh ← launcher (sources .env, runs the server)
.claude/snowflake/config.yaml          ← enables tools + caps SQL at SELECT
.mcp.json                              ← registers the "snowflake" MCP server (repo root, checked in)
```

The launcher and `config.yaml` ship as **templates with the plugin** at
`${CLAUDE_PLUGIN_ROOT}/skills/integrations/references/`. Setup copies them into the customer's
`.claude/snowflake/` (not run in place): the launcher derives the repo root via `$here/../..`,
which only resolves correctly when the launcher sits two levels below the repo root — i.e. at
`.claude/snowflake/`.

The launcher is the key idea: environment variables only reach a child process when it starts,
so the launcher **sources `.env` at the moment the server launches**. That keeps secrets out of
committed config — nothing else can inject them after the fact.

## Steps

1. **Install `uv`** (provides `uvx`, which runs the server with no manual install):
   `curl -LsSf https://astral.sh/uv/install.sh | sh` — verify with `uvx --version`.

2. **Create `.env` at the repo root** with a least-privilege **read-only** PAT/role:
   ```
   SNOWFLAKE_ACCOUNT=<account_id>     # e.g. bq76295.ap-south-1.aws — NO .snowflakecomputing.com suffix
   SNOWFLAKE_USER=<user>
   SNOWFLAKE_PASSWORD=<pat-or-password>
   SNOWFLAKE_WAREHOUSE=<warehouse>
   SNOWFLAKE_ROLE=<read-only-role>
   ```
   `.env` must be gitignored — keep it that way. Single-quote any value with special
   characters (`!`, `$`, spaces) so `source` reads it literally.

3. **Copy the shipped templates into `.claude/snowflake/`** and make the launcher executable:
   ```bash
   ! mkdir -p .claude/snowflake
   ! cp "${CLAUDE_PLUGIN_ROOT}/skills/integrations/references/config.yaml" .claude/snowflake/config.yaml
   ! cp "${CLAUDE_PLUGIN_ROOT}/skills/integrations/references/run-snowflake-mcp.sh" .claude/snowflake/run-snowflake-mcp.sh
   ! chmod +x .claude/snowflake/run-snowflake-mcp.sh
   ```
   For reference, the two templates contain:

   `config.yaml` — turns the tools on *and* locks to read-only:
   ```yaml
   other_services:
     query_manager: true     # run_snowflake_query
     object_manager: true    # list / describe objects
     semantic_manager: false
   sql_statement_permissions:
     - All: false
     - Select: true
   ```

   `run-snowflake-mcp.sh` — self-locating launcher:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   repo_root="$(cd "$here/../.." && pwd)"
   set -a; source "$repo_root/.env"; set +a
   exec uvx snowflake-labs-mcp \
     --service-config-file "$here/config.yaml" \
     --account "$SNOWFLAKE_ACCOUNT" --user "$SNOWFLAKE_USER" \
     --password "$SNOWFLAKE_PASSWORD" --role "$SNOWFLAKE_ROLE" \
     --warehouse "$SNOWFLAKE_WAREHOUSE"
   ```

4. **Register it** as a project-scoped server (writes `.mcp.json` at the repo root, checked in):
   ```bash
   ! claude mcp add --scope project snowflake -- ./.claude/snowflake/run-snowflake-mcp.sh
   ```
   `.mcp.json` is the file the Claude Code CLI actually reads. A `mcpServers` block in
   `.claude/settings.json` is **ignored by the CLI** — don't rely on it.

5. **Approve & connect:** restart Claude Code, then approve the project server `snowflake` when
   prompted on launch. (A `/mcp` reconnect in the same session won't pick up a brand-new server.)

6. **Verify:** ask for `SELECT CURRENT_VERSION()`, or list tables (see `snowflake.md`).

## Gotchas (each one cost real time to find)

- **0 tools exposed?** The server connected fine but `config.yaml` is missing the
  `other_services` block. Auth is *not* the problem — add `query_manager: true`.
- **Use `--password` / `SNOWFLAKE_PASSWORD`.** `--pat` / `SNOWFLAKE_PAT` still work but are
  deprecated and emit warnings. A PAT is passed as the password.
- **`.env` placeholders that break `source`:** values like `VAR=<your_value>` fail because the
  shell reads `<` as redirection. Use plain tokens (`REPLACE_ME`) in templates.
- **Account identifier** must omit the `.snowflakecomputing.com` suffix.
- **Copy the launcher, don't run it from the plugin.** It resolves the repo root from its own
  location (`$here/../..`), so it must live at `.claude/snowflake/` in the customer repo.

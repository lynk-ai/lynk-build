# Snowflake — usage

Snowflake is the customer's data warehouse. The connection is **read-only**: you can
`SELECT` and browse, but nothing can be written, changed, or dropped (the server rejects any
non-SELECT statement). That means it's safe to explore freely.

If it's not connected yet or queries fail with a connection error, see
`snowflake-setup.md` instead.

## When to use it

- **Querying data** — ground-truth checks: verify a reported wrong value, prove a fix
  before/after, sample rows while modeling an entity.
- **Getting metadata** — discover what exists and what shape it has: databases, schemas,
  tables, columns, types, row counts, primary keys. This is the source of truth when
  building or reconciling the semantic graph.
- **Retrieving query history** — see what was actually run against the warehouse (e.g. what
  the users really query, or what a past session executed).

Which database/schema holds the customer's data is configured in `config.json` at the repo root — don't
assume it. There is **no default database/schema** on the connection, so **always
fully-qualify** table names (`db.schema.table`). SQL must be valid **Snowflake** dialect.
For analytics conventions, defer to the `.lynk/` semantic layer — don't reinvent them here.

## How

The server exposes tools you call directly:

- **`run_snowflake_query`** — run a `SELECT` (arg: `statement`).
- **`list_objects`** / **`describe_object`** — browse databases, schemas, tables, columns.

Metadata via SQL, when the browse tools aren't enough:

```sql
SELECT table_schema, table_name, row_count
FROM <db>.information_schema.tables
WHERE table_schema != 'INFORMATION_SCHEMA'
ORDER BY table_schema, table_name
```

Query history — **only "real" queries**: filter out informational/metadata noise (SHOW /
DESCRIBE / USE, `information_schema` probes, connection pings) and keep actual data queries:

```sql
SELECT start_time, user_name, query_text, total_elapsed_time
FROM TABLE(<db>.information_schema.query_history(result_limit => 200))
WHERE query_type = 'SELECT'
  AND execution_status = 'SUCCESS'
  AND query_text NOT ILIKE '%information_schema%'
  AND query_text NOT ILIKE 'select current_%'
ORDER BY start_time DESC
```

(`account_usage.query_history` has longer retention but needs privileges this role may not
have; the `information_schema` table function is the reliable path.)

Always show the user the **actual numbers** in plain terms, not just "it worked."

## If the tools aren't loaded in this session

MCP servers load at startup. If Snowflake was just configured or reconnected and the tools
aren't available yet, you have two options:

1. Ask the user to reconnect with `/mcp` (or restart Claude Code), then query normally — the
   clean path.
2. **Query immediately without waiting** by driving the launcher directly. This uses the exact
   same read-only server, so it's safe:

```bash
uv run --with mcp python - <<'PY'
import asyncio, os, json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SQL = "SELECT CURRENT_VERSION()"   # replace with the real query
async def main():
    p = StdioServerParameters(command="./.claude/snowflake/run-snowflake-mcp.sh",
                              args=[], env=os.environ.copy())
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool("run_snowflake_query", {"statement": SQL})
            print("\n".join(getattr(c, "text", str(c)) for c in res.content))

asyncio.run(main())
PY
```

Run this from the repo root. The launcher self-locates its config and the repo-root `.env`.

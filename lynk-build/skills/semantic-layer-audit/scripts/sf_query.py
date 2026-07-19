#!/usr/bin/env python3
"""Read-only Snowflake query helper for the grounder (Phase 3).

Usage:
    SF_ENV=/path/to/.env uv run --with snowflake-connector-python \
        python3 scripts/sf_query.py "SELECT ..."

Loads Snowflake creds from an .env file (SF_ENV, default: `.env` in the current
working directory), runs ONE read-only query, prints rows as JSON. Never writes —
the grounder proves, it does not mutate. Database/schema come from the .env
(SNOWFLAKE_DATABASE / SNOWFLAKE_SCHEMA) — there is no default, so fully-qualify names.

Note: this duplicates the read-only query path the Snowflake MCP already provides
(see integrations/references/snowflake.md); converging on one is a known follow-up.
"""
import json
import os
import sys
from pathlib import Path


def load_env(path: Path) -> dict:
    creds = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        creds[key.strip()] = val.strip().strip("'").strip('"')
    return creds


def main() -> int:
    if len(sys.argv) < 2:
        print("error: pass one SQL query as argv[1]", file=sys.stderr)
        return 2
    sql = sys.argv[1]
    low = sql.lstrip().lower()
    if not (low.startswith("select") or low.startswith("with") or low.startswith("show")):
        print("error: read-only — only SELECT/WITH/SHOW allowed", file=sys.stderr)
        return 2

    env_path = Path(os.path.expanduser(os.environ.get("SF_ENV", ".env")))
    if not env_path.exists():
        print(f"error: no .env at {env_path} (set SF_ENV, or run from the project root)", file=sys.stderr)
        return 2
    c = load_env(env_path)

    import snowflake.connector

    conn = snowflake.connector.connect(
        account=c["SNOWFLAKE_ACCOUNT"],
        user=c["SNOWFLAKE_USER"],
        password=c["SNOWFLAKE_PASSWORD"],
        warehouse=c.get("SNOWFLAKE_WAREHOUSE"),
        role=c.get("SNOWFLAKE_ROLE"),
        database=c.get("SNOWFLAKE_DATABASE"),
        schema=c.get("SNOWFLAKE_SCHEMA"),
    )
    try:
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchmany(50)]
        print(json.dumps(rows, default=str, indent=2))
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

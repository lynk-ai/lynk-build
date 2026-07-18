#!/usr/bin/env bash
# Launches the read-only Snowflake MCP server. Self-locating: sources the
# repo-root .env (gitignored) for secrets and uses the sibling config.yaml for
# tools, so it works no matter what directory it's started from.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$here/../.." && pwd)"
set -a; source "$repo_root/.env"; set +a

exec uvx snowflake-labs-mcp \
  --service-config-file "$here/config.yaml" \
  --account   "$SNOWFLAKE_ACCOUNT" \
  --user      "$SNOWFLAKE_USER" \
  --password  "$SNOWFLAKE_PASSWORD" \
  --role      "$SNOWFLAKE_ROLE" \
  --warehouse "$SNOWFLAKE_WAREHOUSE"

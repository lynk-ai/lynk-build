#!/usr/bin/env bash
# Lynk build agent — operating-contract injector.
# Injects the always-on operating contract as SessionStart additionalContext.
# Silent-fail on every path (startup must never block); no network.
set -euo pipefail

# Content home: the plugin bundle when installed, else this repo.
ROOT="${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}}"
CONTRACT="$ROOT/hooks/operating-contract.md"

[ -f "$CONTRACT" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

python3 - "$CONTRACT" <<'PY'
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()
except Exception:
    raise SystemExit(0)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                         "additionalContext": text}}))
PY

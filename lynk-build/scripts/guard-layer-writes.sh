#!/bin/bash
# PostToolUse hook — the after-write NUDGE for semantic-layer files (never blocks).
# Words trigger the router hook; ACTIONS trigger this one: when a .lynk/** file
# was just written and the library was NOT consulted this session (the fetch
# hook drops $BK_DATA/consulted/<session_id> on every real consultation), inject
# a reminder to confirm the change went through the lynk-build methodology and
# reconcile it otherwise. The write stands.
#
# A change made through the lynk-build skill already satisfies this — the nudge
# names lynk-build as the satisfier so a real build isn't told to stop and
# "invoke the library now" (decision 7: lynk-build owns the build; the library
# backs deeper methodology).
#
# Input (stdin): PostToolUse JSON — session_id, tool_name, tool_input.file_path, cwd
# Output on nudge: {"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"..."}}
# Silent exit 0 otherwise.

set -euo pipefail
exec 3<&0

python3 - <<'PYEOF'
import json, os, re, sys

try:
    with os.fdopen(3) as hook_input:
        data = json.load(hook_input)
except Exception:
    sys.exit(0)

path = str((data.get("tool_input") or {}).get("file_path") or "")
if not re.search(r"(^|/)\.lynk(/|$)", path):
    sys.exit(0)  # not a semantic-layer artifact

session = re.sub(r"[^A-Za-z0-9_-]", "", str(data.get("session_id") or ""))
cwd = data.get("cwd") or os.getcwd()
bk_data = os.environ.get("BK_DATA") or os.path.join(cwd, ".bk")
if session and os.path.exists(os.path.join(bk_data, "consulted", session)):
    sys.exit(0)  # library already in the loop this session

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": (
            "[layer-write nudge] A semantic-layer file was just modified. If this "
            "change went through the lynk-build skill's methodology (semantics docs "
            "for the WHAT + content rules and verification for the HOW), you're "
            "covered — carry on. If it was made from memory or ad-hoc, bring that "
            "methodology in now and reconcile the change: the docs give the format, "
            "the methodology gives the judgment (the library backs deeper questions)."
        ),
    }
}))
PYEOF

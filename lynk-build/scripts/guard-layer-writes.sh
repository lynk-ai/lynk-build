#!/bin/bash
# PostToolUse hook — the after-write NUDGE for semantic-layer files (never blocks).
# Words trigger the router hook; ACTIONS trigger this one: when a .lynk/** file
# was just written, inject a reminder to confirm the change went through the
# lynk-build methodology and reconcile it otherwise. The write stands.
#
# A change made through the lynk-build skill already satisfies this — the nudge
# names lynk-build as the satisfier so a real build isn't told to stop and
# "consult the library now" (lynk-build owns the build; the lynk-research
# library backs deeper methodology).
#
# ponytail: the old per-session suppression gate (a $BK_DATA/consulted marker
# dropped by the now-deleted fetch hook) is gone, so the nudge fires on every
# from-memory .lynk write. It self-dismisses ("if you used lynk-build, carry
# on"), so that's fine — re-add a session marker if the noise ever bites.
#
# Input (stdin): PostToolUse JSON — tool_name, tool_input.file_path
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

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": (
            "[layer-write nudge] A semantic-layer file was just modified. If this "
            "change went through the lynk-build skill's methodology (semantics docs "
            "for the WHAT + content rules and verification for the HOW), you're "
            "covered — carry on. If it was made from memory or ad-hoc, bring that "
            "methodology in now and reconcile the change: the docs give the format, "
            "the methodology gives the judgment (the lynk-research library backs "
            "deeper questions)."
        ),
    }
}))
PYEOF

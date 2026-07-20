#!/bin/bash
# UserPromptSubmit hook — the semantic router for builder requests.
# Pattern-matches the user's prompt and injects lane guidance (never blocks):
#   MUTATION intent (create/edit/... × entity/metric/...) -> lynk-build skill (owns build methodology)
#   REFERENCE intent (how does / what is ... Lynk)        -> docs only
#   anything else                                          -> silent (exit 0, no output)
# This is a floor-raising hook (book-1 hook-vs-router): it steers, the agent decides.

set -euo pipefail
exec 3<&0

python3 - <<'PYEOF'
import json, os, re, sys

try:
    with os.fdopen(3) as hook_input:
        data = json.load(hook_input)
except Exception:
    sys.exit(0)

prompt = str(data.get("prompt") or "")

MUTATE = r"\b(creat\w*|add\w*|defin\w*|build\w*|chang\w*|edit\w*|updat\w*|modif\w*|fix\w*|renam\w*|delet\w*|remov\w*|refactor\w*|migrat\w*|split\w*|merg\w*|implement\w*|writ\w*|generat\w*)\b"
LAYER  = r"\b(entit(y|ies)|metrics?|features?|dimensions?|relations?(hips?)?|measures?|polic(y|ies)|domains?|semantic\s+layer|\.lynk\b|lynk\.(md|yml)|schema\.ya?ml)\b"
REFER  = r"\b(how\s+(does|do|is)|what\s+(is|are|does)|explain|understand|meaning\s+of|syntax|documentation|docs)\b"

p = prompt.lower()
layer = re.search(LAYER, p)
if not layer:
    sys.exit(0)  # not about the semantic layer — stay silent

# Reference markers take precedence: "what is the syntax for defining X" is a
# docs question even though "defining" looks like a mutation verb. Task-shaped
# asks ("create...", "how to create...") carry no reference marker and fall through.
if re.search(REFER, p):
    ctx = ("[layer-request router] Reference question about Lynk - the "
           "semantics docs own this lane; answer from them. The lynk-research "
           "library is for design/build methodology and is not needed for pure reference.")
elif re.search(MUTATE, p):
    ctx = ("[layer-request router] This request CHANGES the semantic layer. Use "
           "the lynk-build skill — it owns the build methodology: it grounds every "
           "change in the semantics docs (the WHAT — exact format/fields/syntax) "
           "and applies the content rules and verification (the HOW), drawing on "
           "the lynk-research library for deeper methodology. Never mutate the layer from memory.")
else:
    sys.exit(0)  # layer-adjacent but neither mutating nor reference — let the agent judge

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": ctx,
    }
}))
PYEOF

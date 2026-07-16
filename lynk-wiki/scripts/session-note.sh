#!/usr/bin/env bash
# lynk-book session note — injects the library pointer at session start.
# CK-steal disciplines: ≤2KB budget, pointers never payloads, silent-fail on
# every path (startup must never block), no network.
set -euo pipefail

# Content home: the plugin bundle when installed, else this repo.
ROOT="${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}}"
BK="$ROOT/bk"
# State home: the consumer project (dev: the repo itself).
DATA="${BK_DATA:-${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}/.bk}"

# Guards: bk + python3 present, library exists — else exit silently.
command -v python3 >/dev/null 2>&1 || exit 0
[ -x "$BK" ] || exit 0
[ -d "$ROOT/library" ] || exit 0

COUNTS=$("$BK" list --json 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)['books']
    parts = [b['slug'] + ' (' + str(b['pages']) + 'p)' for b in d[:8]]
    print(str(len(d)) + ' books: ' + ' · '.join(parts))
except Exception:
    raise SystemExit(1)
" 2>/dev/null) || exit 0

# Consumer mode: a rendered bundle carries BUNDLE_VERSION beside its books.
# (hidden .bundle-version marker). There, the writing pipeline and sustain skill do NOT exist — the note must
# neither instruct writes nor point at absent skills.
CONSUMER=0
[ -f "$ROOT/.bundle-version" ] && CONSUMER=1

# Sustain nudge: count gaps not yet processed by the sustain loop (static
# checkpoint — observation only; creation happens via /sustain, never inline).
PENDING=$(python3 - "$DATA" <<'PY' 2>/dev/null || echo 0
import json, sys, pathlib
data = pathlib.Path(sys.argv[1])
def ids(p, key):
    out = set()
    if p.exists():
        for l in p.read_text().splitlines():
            try: out.add(json.loads(l).get(key, l))
            except Exception: pass
    return out
gaps = ids(data / "gaps.jsonl", "intent")
done = ids(data / "sustain.jsonl", "intent")
print(len(gaps - done))
PY
)
SUSTAIN_LINE=""
if [ "${PENDING:-0}" -gt 0 ] 2>/dev/null; then
  if [ "$CONSUMER" = "1" ]; then
    SUSTAIN_LINE="
GAPS: ${PENDING} knowledge gap(s) recorded in .bk/gaps.jsonl — demand the library does not yet cover. Share that file with the lynk-book maintainers; do not attempt to write library pages here (this is a read-only bundle)."
  else
    SUSTAIN_LINE="
SUSTAIN: ${PENDING} knowledge gap(s) pending in .bk/gaps.jsonl — when appropriate (never mid-task), run the sustain skill to research and draft the missing pages."
  fi
fi

WRITING_BLOCK="BUILD DIRECTIVE: before ANY create/update/edit of semantic-layer artifacts (entities, metrics, relations, features, policies): consult the semantics docs for the WHAT (format/syntax) AND invoke the library skill for the HOW (methodology, verification). Never mutate the layer from memory alone. Pure how-does-Lynk-work reference questions need only the docs.

This library is a READ-ONLY rendered bundle (provenance in .bundle-version). Never edit its pages; improvements happen in the lynk-book authoring repo."
if [ "$CONSUMER" = "0" ]; then
  WRITING_BLOCK="WRITING DIRECTIVE: any new book or page must satisfy library/book-2-book-standard (the gate checks). The writer's first step is always reading the constitution: ./bk read book-1-best-context:index book-2-book-standard:index

The constitution: book-1-best-context (why) · book-2-book-standard (how, incl. the gate's checklists)."
fi

CONTEXT="<library>
This repo is a self-hosting book library. ${COUNTS}${SUSTAIN_LINE}

RESEARCH DIRECTIVE: when the user asks what the books/library/standard say, or a task needs the principles (\"what does the standard say about X\", \"check the library\", \"per our books\"), invoke the library skill: Skill tool with skill=\"library\". Pipeline: you spawn ONE librarian agent -> it routes BOOKS (metadata only), spawns one chapter-scout (book-reader) per relevant book (nested), and returns consolidated POINTER lines + fetch-file paths (a SubagentStop hook fetches each scout\x27s pointed chapters to .bk/fetch/) -> you Read the fetch files and answer from primary text with (book · page) citations. Never read whole books inline.

${WRITING_BLOCK}
</library>"

python3 - "$CONTEXT" <<'PY'
import json, sys
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                         "additionalContext": sys.argv[1]}}))
PY

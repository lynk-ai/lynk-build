#!/bin/bash
# SubagentStop hook — the pointer pipeline's fetch stage (v2: per-scout file-drop).
# A chapter-scout (agent type "book-reader") returns POINTER lines; this hook greps
# them from the scout's final message, runs `bk read` on exactly those chapters,
# writes the primary text to a file under .bk/fetch/, and injects a ONE-LINE
# additionalContext naming that file — so the payload never rides through any
# agent's context window. The scout relays the line; the main agent Reads the file.
# Deterministic: zero model tokens spent deciding to fetch.
#
# Input (stdin): SubagentStop JSON — agent_type, agent_id, last_assistant_message, cwd.
# Output: {"hookSpecificOutput":{"hookEventName":"SubagentStop","additionalContext":"<one line>"}}
# Silent (exit 0, no output) for any other agent type or when no POINTER lines exist.

set -euo pipefail

# The hook's JSON arrives on OUR stdin, but the heredoc below occupies
# python's stdin — so duplicate the real stdin to fd 3 and read from there.
exec 3<&0

python3 - <<'PYEOF'
import json, re, subprocess, sys, os
from collections import OrderedDict

try:
    with os.fdopen(3) as hook_input:
        data = json.load(hook_input)
except Exception:
    sys.exit(0)  # not our JSON — stay silent, never block the agent

# Namespace-tolerant: bare "book-reader" in dev, "<host-plugin>:book-reader"
# when bundled inside a plugin.
if not re.search(r"(^|:)book-reader$", str(data.get("agent_type") or "")):
    sys.exit(0)

msg = data.get("last_assistant_message") or ""
cwd = data.get("cwd") or os.getcwd()
# Content home: the plugin bundle when installed, else the repo (= cwd in dev).
bk_root = os.environ.get("CLAUDE_PLUGIN_ROOT") or cwd
# State home: the consumer project (BK_DATA), else classic <root>/.bk.
bk_data = os.environ.get("BK_DATA") or os.path.join(cwd, ".bk")
agent_id = re.sub(r"[^A-Za-z0-9_-]", "", str(data.get("agent_id") or "run"))[:24] or "run"

# Strict slug contract: bk enforces ^[a-z0-9-]+$; anything else is ignored,
# which also kills path-traversal attempts by construction.
pointers = re.findall(r"^POINTER:\s+([a-z0-9-]+):([a-z0-9-]+)\b", msg, re.MULTILINE)
if not pointers:
    sys.exit(0)  # miss path or misbehaving scout — inject nothing

# Dedupe, preserve order, group by book. Cap: 6 pointers per book (the scouts'
# own hard cap), 24 total (a runaway backstop).
books = OrderedDict()
seen = set()
for book, page in pointers:
    if (book, page) in seen or len(seen) >= 24:
        continue
    if len(books.get(book, [])) >= 6:
        continue
    seen.add((book, page))
    books.setdefault(book, []).append(page)

chunks, fetched_specs = [], []
for book, pages in books.items():
    spec = f"{book}:{','.join(pages)}"
    try:
        out = subprocess.run(
            [os.path.join(bk_root, "bk"), "read", spec],
            cwd=cwd, capture_output=True, text=True, timeout=30,
            env={**os.environ, "BK_ROLE": "hook",
                 "BK_ROOT": bk_root, "BK_DATA": bk_data},
        )
    except Exception:
        continue
    if out.returncode != 0:
        chunks.append(f"── fetch failed: {spec} ── {out.stderr.strip()[:200]}")
        continue
    chunks.append(f"── fetched: {spec} ──\n{out.stdout.strip()}")
    fetched_specs.append(spec)

if not chunks:
    sys.exit(0)

# Preserve the scout's audit trail (pointers + notes) inside the fetch file, so
# the scout's own final message can shrink to one line without losing anything.
notes = msg.strip()

# Mark the library as consulted for this session — the layer-write nudge
# hook checks this marker (words route, actions nudge, this is the receipt).
session = re.sub(r"[^A-Za-z0-9_-]", "", str(data.get("session_id") or ""))
if session:
    cdir = os.path.join(bk_data, "consulted")
    os.makedirs(cdir, exist_ok=True)
    open(os.path.join(cdir, session), "a").close()

fetch_dir = os.path.join(bk_data, "fetch")
os.makedirs(fetch_dir, exist_ok=True)
fetch_path = os.path.join(fetch_dir, f"{agent_id}.txt")
with open(fetch_path, "w") as f:
    f.write(
        "[library pointer fetch] Primary text of exactly the pointed chapters. "
        "Answer from this text and cite (book · page).\n\n"
        "═══ scout's pointers & notes ═══\n" + notes + "\n\n"
        "═══ fetched chapters ═══\n\n" + "\n\n".join(chunks) + "\n"
    )

count = sum(len(p) for p in books.values())
line = (
    f"[library pointer fetch] {count} chapter(s) fetched to {fetch_path} "
    f"({'; '.join(fetched_specs)}). The parent agent must Read that file and "
    f"answer from its primary text, citing (book · page)."
)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SubagentStop",
        "additionalContext": line,
    }
}))
PYEOF

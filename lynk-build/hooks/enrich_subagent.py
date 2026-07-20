#!/usr/bin/env python3
"""PostToolUse hook (matcher: Skill). Fires in the router when the LIBRARIAN skill
returns. Reads the librarian's refs list from tool_response.result, populates chapter
content via bin/populate_chapters, and injects the result into the router's context
via additionalContext — zero extra model tool calls.

Gated on commandName == "librarian" so it does NOT fire for the scholar Skill calls the
librarian makes internally (those must stay refs-only to preserve the token budget).

parse_refs is deliberately lenient: the librarian is supposed to return ONLY the JSON
array, but it often narrates around it ("best-context is a match. Selected. [ ... ]"),
so we extract the array from wherever it lands rather than silently no-op."""
import json, os, re, subprocess, sys

ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))
)


def _json_arrays(text):
    """Yield each top-level balanced [...] substring in text, string-aware (so a
    bracket inside a quoted value or a stray ] in prose doesn't fool the scan)."""
    i = 0
    while True:
        start = text.find("[", i)
        if start == -1:
            return
        depth, in_str, esc, end = 0, False, False, None
        for j in range(start, len(text)):
            ch = text[j]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            elif ch == '"':
                in_str = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end = j
                    break
        if end is None:
            return  # unbalanced tail — nothing more to yield
        yield text[start:end + 1]
        i = end + 1


def parse_refs(result):
    """The librarian should reply with ONLY a JSON array of {name, path}, but in
    practice it narrates around the array, wraps it in a ```json fence, or `result`
    arrives as a non-string. Try, in order: the whole string, a fenced block, then
    every balanced [...] found in it — returning the first REFS-shaped list (items
    with a "path"). An explicit empty array (legitimately "no chapters") returns [];
    anything else returns None."""
    text = (result if isinstance(result, str) else json.dumps(result)).strip()
    candidates = [text]
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.S)
    if fence:
        candidates.append(fence.group(1).strip())
    candidates.extend(_json_arrays(text))

    empty = None
    for c in candidates:
        try:
            data = json.loads(c)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(data, list):
            continue
        if any(isinstance(e, dict) and "path" in e for e in data):
            return data                 # a real refs array — even if narrated around
        if not data and empty is None:
            empty = data                # remember a bare [] as the fallback
    return empty                        # [] (legit no-chapters) or None (nothing parseable)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") != "Skill":
        sys.exit(0)
    tr = data.get("tool_response") or {}
    # commandName may be namespaced ("lynk-build:librarian"); match the leaf.
    if str(tr.get("commandName", "")).split(":")[-1] != "librarian":
        sys.exit(0)

    refs = parse_refs(tr.get("result"))
    if not refs:                       # None (unparseable) or [] (no chapters) → nothing to inject
        sys.exit(0)

    pop = os.path.join(ROOT, "bin", "populate_chapters")
    try:
        populated = subprocess.run(
            [pop], input=json.dumps(refs), capture_output=True, text=True, timeout=10, check=True
        ).stdout
    except Exception:
        sys.exit(0)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "lynk-build — the selected chapters WITH their content are below. "
                "Answer the user's question from this content and cite each as "
                "`book · chapter`:\n" + populated
            ),
        }
    }))


def _selftest():
    # ponytail: parse_refs is the fragile boundary — the q04 miss was prose before
    # the array. Cover each shape the librarian has actually emitted.
    P = "/x/library/best-context/chapters/distinguishability.md"
    bare = f'[{{"name": "D", "path": "{P}"}}]'
    assert parse_refs(bare)[0]["path"] == P                                    # clean array
    assert parse_refs("```json\n" + bare + "\n```")[0]["path"] == P            # fenced
    # the real q04 failure: narration before the array
    assert parse_refs("`best-context` is a high-confidence match. Selected and "
                      "dispatched the scholar.\n\n" + bare + "\n")[0]["path"] == P
    assert parse_refs(json.loads(bare))[0]["path"] == P                        # already a list
    assert parse_refs("see [1] and [2], then:\n" + bare)[0]["path"] == P       # bracket-y prose first
    assert parse_refs("no chapters relevant\n[]") == []                        # legit empty
    assert parse_refs("plain prose, no array") is None                         # nothing
    print("enrich parse_refs selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        main()

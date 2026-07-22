"""Promote-location guard (deterministic regression check for the World Cup bug).

The pipeline must promote into the canonical store `lynk-build/library/`, never
repo-root `library/`. A book written to the wrong store is invisible to the reader
(lynk-research reads lynk-build/library/). This scans the transcript for file
writes (`Write` file_path) and move/copy commands (bash `mv`/`cp`) that target a
`library/<slug>` path, and FAILS if any lands outside `lynk-build/library/`.

Only fires when a write/move to a library path is observed — otherwise n/a
(passed=None), so diagnose-only cases (needs-info, found-existing) are unaffected.
"""

import re

FILE_PATH = re.compile(r'"file_path"\s*:\s*"([^"]+)"')
CMD = re.compile(r'\b(?:mv|cp|rsync)\b[^"\\]{0,200}')
# a library/<slug> reference NOT under the canonical lynk-build/ prefix
BAD = re.compile(r'(?<!lynk-build/)(?<![\w-])library/[a-z0-9-]+')
# any library/<slug> reference at all (marks a segment as library-touching)
ANY_LIB = re.compile(r'(?<![\w-])library/[a-z0-9-]+')


def evaluate(transcript):
    segments = FILE_PATH.findall(transcript) + CMD.findall(transcript)
    lib_segs = [s for s in segments if ANY_LIB.search(s)]
    if not lib_segs:
        return {"name": "promote_location", "passed": None,
                "detail": "no library write/move observed (n/a)"}
    bad = [s.strip() for s in lib_segs if BAD.search(s)]
    passed = not bad
    return {
        "name": "promote_location",
        "passed": passed,
        "detail": ("all library writes → lynk-build/library/" if passed
                   else f"WRONG store (not lynk-build/library/): {bad[:2]}"),
    }


def _demo():
    ok = '"file_path": "lynk-build/library/mcp/index.md"'
    assert evaluate(ok)["passed"] is True
    ok_mv = '"command": "mv writer/drafts/mcp lynk-build/library/mcp"'
    assert evaluate(ok_mv)["passed"] is True
    bad = '"file_path": "library/world-cup-2026/index.md"'
    assert evaluate(bad)["passed"] is False
    bad_mv = '"command": "mv writer/drafts/x library/x"'
    assert evaluate(bad_mv)["passed"] is False
    na = '"file_path": "writer/drafts/mcp/index.md"'
    assert evaluate(na)["passed"] is None
    print("promote_location._demo ok")


if __name__ == "__main__":
    _demo()

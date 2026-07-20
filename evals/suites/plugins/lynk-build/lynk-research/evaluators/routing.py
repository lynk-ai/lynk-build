"""Routing evaluator — the golden-questions confusion matrix.

Measures WHICH library chapters the pipeline actually SURFACED to the answer, and
checks them against the case's expected routing:

  reach-book             at least one chapter of the expected book surfaced
  reach-chapter          the specific expected chapter(s) surfaced
  reach-nowhere          NO chapter surfaced (a research question the books don't cover)
  reach-book-no-chapter  NO chapter surfaced (right domain, wrong grain — the over-reach trap)
  no-activation          the lynk-research skill should NOT fire at all (not a research
                         question — Lynk syntax/schema/SQL the docs own). Detected by
                         whether lynk-research/librarian/scholar was ever invoked. These
                         cases run WITHOUT the forcing directive, so it's a real test of
                         the skill's description-based triggering.

Signal: the enrich hook injects ONLY the scholars' selected chapters (with their
content) under a fixed marker. We parse chapter paths from THAT injection — NOT
the whole transcript, which also carries the librarian's `generate_book_toc`
dump (every chapter path in the book) and would make every case look like it
reached everything. No injection (empty refs) → nothing surfaced, which is
exactly what the miss cases (Types 3/4) require. Recall-first — reaching extra
chapters on a reach-chapter case is reported (precision), not failed.
"""

import json
import re

CHAPTER_RE = re.compile(r"library/([a-z0-9._-]+)/chapters/(?:\d+[-_])?([a-z0-9][a-z0-9._-]*?)\.md")
# hooks/enrich_subagent.py injects the selected chapters under this exact phrase.
ENRICH_MARK = "selected chapters WITH their content"


PIPELINE_SKILLS = {"lynk-research", "librarian", "scholar"}


def reached_chapters(messages):
    """Set of (book, chapter-slug) the enrich hook injected into the answer context."""
    reached = set()
    for m in messages:
        blob = m if isinstance(m, str) else json.dumps(m, default=str)
        if ENRICH_MARK not in blob:
            continue  # ponytail: skip the TOC dump / other noise — only the injection counts
        reached |= {(mt.group(1), mt.group(2)) for mt in CHAPTER_RE.finditer(blob)}
    return reached


def _invoked_skills(messages):
    """Leaf names of every skill invoked via the Skill tool (input.skill = 'plugin:leaf')."""
    for m in messages:
        if isinstance(m, dict) and m.get("_type") == "AssistantMessage":
            for b in (m.get("content") or []):
                if isinstance(b, dict) and b.get("name") == "Skill":
                    yield str((b.get("input") or {}).get("skill", "")).split(":")[-1]


def pipeline_activated(messages):
    """Did the lynk-research pipeline fire at all? True if any pipeline skill was
    invoked or any chapter was injected."""
    return (any(s in PIPELINE_SKILLS for s in _invoked_skills(messages))
            or bool(reached_chapters(messages)))


def evaluate(case, messages):
    reached = reached_chapters(messages)
    kind = case["expect_routing"]
    book = case.get("book")
    in_book = {ch for (b, ch) in reached if b == book} if book else set()

    if kind == "no-activation":
        activated = pipeline_activated(messages)
        return {
            "name": "routing",
            "passed": not activated,
            "detail": ("skill should NOT activate; "
                       + ("it did (invoked the pipeline / injected a chapter)"
                          if activated else "it stayed out — correct")),
            "reached": sorted(f"{b}·{c}" for b, c in reached),
        }

    if kind == "reach-book":
        passed = bool(in_book)
        detail = f"expected any {book} chapter; reached {sorted(in_book) or '∅'}"
    elif kind == "reach-chapter":
        want = set(case.get("chapters") or [])
        missing = want - in_book
        extra = in_book - want
        passed = not missing
        detail = (f"want {sorted(want)} in {book}; "
                  f"missing {sorted(missing) or '∅'}; also reached {sorted(extra) or '∅'}")
    else:  # reach-nowhere / reach-book-no-chapter — no chapter should surface
        passed = not reached
        detail = f"expected NO chapter; reached {sorted(f'{b}·{c}' for b, c in reached) or '∅'}"

    return {
        "name": "routing",
        "passed": passed,
        "detail": detail,
        "reached": sorted(f"{b}·{c}" for b, c in reached),
    }


def _demo():
    # ponytail: the precise-signal fix is the point — the TOC dump must NOT count as reached.
    inj = {"_type": "HookEventMessage", "data": {"output": json.dumps({"hookSpecificOutput": {
        "additionalContext": "lynk-build — selected chapters WITH their content are below:\n"
        '[{"path":"/x/library/best-context/chapters/distinguishability.md","content":"..."}]'}})}}
    toc = {"_type": "UserMessage", "content": [{"type": "tool_result",
        "content": "## chapters\n  path: /x/library/best-context/chapters/living-sources.md"}]}
    assert reached_chapters([inj, toc]) == {("best-context", "distinguishability")}, \
        "must count the injection only, not the TOC dump"
    hit = evaluate({"expect_routing": "reach-chapter", "book": "best-context",
                    "chapters": ["distinguishability"]}, [inj, toc])
    assert hit["passed"]
    miss = evaluate({"expect_routing": "reach-chapter", "book": "best-context",
                     "chapters": ["living-sources"]}, [inj, toc])
    assert not miss["passed"]
    assert evaluate({"expect_routing": "reach-book", "book": "best-context"}, [inj])["passed"]
    # no injection at all → nothing reached: miss cases pass, hit cases don't
    assert evaluate({"expect_routing": "reach-nowhere"}, [toc])["passed"]
    assert evaluate({"expect_routing": "reach-book-no-chapter", "book": "best-context"}, [toc])["passed"]
    assert not evaluate({"expect_routing": "reach-nowhere"}, [inj])["passed"]
    # no-activation: passes when no pipeline skill was invoked, fails when one was
    call = {"_type": "AssistantMessage", "content": [
        {"name": "Skill", "input": {"skill": "lynk-build:lynk-research", "args": "x"}}]}
    assert evaluate({"expect_routing": "no-activation"}, [toc])["passed"]          # nobody invoked it
    assert not evaluate({"expect_routing": "no-activation"}, [call])["passed"]     # it fired — bad
    assert not evaluate({"expect_routing": "no-activation"}, [inj])["passed"]      # chapter injected — bad
    print("routing._demo ok")


if __name__ == "__main__":
    _demo()

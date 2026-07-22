"""Deterministic terminal-state evaluator for the book-writer pipeline.

The orchestrator's Stage 6 RETURN names exactly one terminal state. This scores
whether that state matches the case's `expect_outcome`. Matching is priority-ordered
on the literal hyphenated state names the SKILL emits, with a few plain-language
fallbacks — specific states first so a stray word doesn't shadow them.
"""

# Priority order: the literal state name is the strongest signal; fallbacks are
# phrases the RETURN uses when it doesn't print the bare token.
MATCHERS = [
    ("needs-info",      ["needs-info", "brief is missing", "before spending", "what would you like", "what is the topic"]),
    ("found-existing",  ["found-existing", "already covered", "already in the library", "pointer to the existing", "findability"]),
    ("nothing-written", ["nothing-written", "nothing was written", "declined to write", "did not write", "inferable"]),
    ("removed",         ["removed", "deleted the chapter", "deleted the book", "chapter deleted", "dropped the chapter"]),
    ("enriched",        ["enriched"]),
    ("created",         ["created", "new book", "new chapter", "promoted"]),
]


def detect(answer):
    low = (answer or "").lower()
    for state, keywords in MATCHERS:
        if any(kw in low for kw in keywords):
            return state
    return None


def evaluate(case, answer):
    exp = case["expect_outcome"]
    got = detect(answer)
    passed = got == exp
    return {
        "name": "outcome",
        "passed": passed,
        "detail": f"expected '{exp}', detected '{got or 'none'}'",
    }


def _demo():
    assert detect("Terminal state: found-existing — pointer to best-context · context-rot") == "found-existing"
    assert detect("nothing-written: general dog knowledge is inferable") == "nothing-written"
    assert detect("Done. New book `mcp` created and promoted.") == "created"
    assert detect("The brief is missing the gap — what would you like the book to cover?") == "needs-info"
    assert evaluate({"expect_outcome": "created"}, "New book created and promoted.")["passed"]
    assert not evaluate({"expect_outcome": "created"}, "nothing-written — declined")["passed"]
    print("outcome._demo ok")


if __name__ == "__main__":
    _demo()

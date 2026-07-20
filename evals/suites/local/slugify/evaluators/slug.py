"""Deterministic slug evaluator — no LLM judge.

Demonstrates that the eval framework supports plain-code scoring, not only judged
claims: passes when the exact expected slug appears in the answer as a standalone
token (so a short slug isn't a coincidental substring of a longer one).
"""

import re


def evaluate(case, answer):
    exp = case["expected"]
    low = (answer or "").lower()
    passed = re.search(rf"(?:^|[^a-z0-9-]){re.escape(exp)}(?:[^a-z0-9-]|$)", low) is not None
    return {
        "name": "slug",
        "passed": passed,
        "detail": f"expected '{exp}' → {'found' if passed else 'not found'} in answer",
    }


def _demo():
    assert evaluate({"expected": "hello-world-2024"}, "hello-world-2024")["passed"]
    assert evaluate({"expected": "spaced-out"}, "The slug is spaced-out.")["passed"]
    assert not evaluate({"expected": "spaced-out"}, "spaced-out-extra")["passed"]  # longer slug
    assert not evaluate({"expected": "the-quick-brown-fox"}, "(no answer)")["passed"]
    print("slug._demo ok")


if __name__ == "__main__":
    _demo()
